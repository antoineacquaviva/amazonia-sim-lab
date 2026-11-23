// =========================================================================
// data/livret_v6_0.js — Livret de Règles Joueur & Synthèse Cœur (Amazonia)
// Architecture didactique à deux vitesses & 12 briques « Coup d’œil »
// =========================================================================

const REGLES_COEUR_SYNTHESE = {
  "but_et_format": "Jeu coopératif asymétrique à communication muette (3 à 6 joueurs parmi Mammifères, Reptiles, Oiseaux, Humains, Entités Magiques, Insectes ; 8 tours maximum répartis en 2 Actes). Objectif commun : maximiser le nombre d'Arbres encore debout à la fin de la partie (les Souches ne valent aucun point par défaut). Réserves de jetons et de cartes Sabotage illimitées.",
  "principes_transverses": {
    "gouvernance_unitaire": "Chaque Tuile de Synergie (Gardien, Rêve ou Nid) et chaque piste de Migration est décidée uniquement par le joueur de son Peuple d'origine ; en Furtivité, la pose d'un Piège gagné sur une piste est choisie uniquement par le propriétaire de cette piste. Zéro vote collectif : les autres joueurs respectent la décision. Les cartes Sabotage sont toutes identiques et diluent définitivement le paquet Machine.",
    "communication_muette": "Silence tactique complet tant que les paravents sont fermés : aucune annonce verbale ni allusion à sa carte ou ses dés. Seuls les placements et ajustements visibles des Défenseurs communiquent les intentions jusqu'à l'ouverture simultanée des paravents.",
    "pont_routier": "Le long d'une piste de forêt, toute Route Forestière est sautée automatiquement comme un pont : viser Devant, avancer, reculer ou migrer désignent toujours la prochaine parcelle non rasée dans cette direction (les Routes restent infranchissables latéralement). Dès qu'une piste est entièrement transformée en Routes Forestières, ses deux rives de Furtivité deviennent définitivement fermées.",
    "cascades_gardiens": "Terminez intégralement l'action ou la tuile en cours avant de parcourir la Piste des Gardiens à plat de la case 1 à la case 6. Chaque événement allume au plus un seul déclencheur : à l'ouverture des paravents, 3. Sabotage prime sur 6. Insecte (déviation ±1 sur la Réglette des Tactiques), qui prime sur 5. Rêve (allumé uniquement lorsqu'un Rêve défendu annule au moins une machine non déviée) ; pendant les attaques, 2. Piégeage (Piège autonome) prime sur 6. Insecte (Parade avec dépense d'au moins un Insecte), qui prime sur 1. Parade (Défenseurs seuls ou pouvoir automatique) ; la case 4. Gardien s'allume à la première ouverture du tour de chaque autre Gardien distinct (sans boucle sur elle-même) ; la Furtivité et la production des Nids n'allument aucun déclencheur."
  },
  "topologie_et_seuils_imprimes": {
    "roue": "N pistes de forêt (de la parcelle 1 en bordure vers le cœur, munies chacune à leur pied d'une zone de Furtivité à 2 rives indépendantes de 2 places : Rive Piège et Rive Sabotage) alternées avec N lisières portant chacune 2 Tuiles de Synergie. Mise en place canonique à départ décalé : Bulldozer sur la parcelle 1 (bordure) et Abatteuse sur la parcelle 2 de chaque piste.",
    "dotations": "Chaque parcelle porte un chiffre gravé qui indique à la fois sa dotation initiale d'Arbres et son Seuil de Parade imprimé (profil canonique 2–2–3–3, soit 10 Arbres par piste).",
    "reglette_tactiques": "Réglette réversible de 6 cases aux actions fixes : 1 et 4 = Sur place (modif. 0), 2 et 5 = Devant (modif. 0), 3 et 6 = En avançant (Sur place puis Devant, avancée +1, modif. −1). Acte 1 (Tours 1 à 4, Face A) : cases 1–3 en Mode Charge, cases 4–6 en Mode Assaut. Acte 2 (Tours 5 à 8, Face B retournée physiquement au début du Tour 5) : permutation des blocs — cases 1–3 en Mode Assaut, cases 4–6 en Mode Charge. En Mode Charge : jetons Puissance existants ignorés au Seuil, dégâts normaux sur frappe non parée et +1 jeton Puissance rouge maximum par activation dès qu'au moins une frappe sur une parcelle réelle non-Route n'est ni parée ni piégée (une attaque Devant hors-plateau depuis la dernière parcelle ne rapporte jamais de jeton). En Mode Assaut (et Ratissage permanent) : tous les jetons Puissance comptent, 0 gain. Les Rêves se posent par-dessus depuis la droite (case 6 puis 5, etc.) sans retirer les Tactiques ni les Insectes.",
    "eveil_de_la_foret": "Actif dès qu'au moins un Peuple Animal Sauvage (Mammifères, Reptiles ou Oiseaux) participe à la partie. Chaque Gardien construit peut recevoir 0, 1 ou 2 Défenseurs maximum en pari d'activation lors de la pose du Défenseur d'ajustement, glissés sous la tuile à chaque déclenchement. À la fin des attaques : si tous ses Défenseurs ont été glissés, le pari est gagné (le Gardien reste en piste et passe sur sa Face 2 s'il est double-face) ; s'il reste au moins un Défenseur dessus, le pari est perdu (retour en lisière Face 1, sauf Bouclier de lisière par défausse d'1 Insecte de sa case pour le maintenir sur sa face actuelle, le pari demeurant perdu). Aux Tours 1 à 7, si tous les N Défenseurs d'ajustement de la table ont été engagés sur la Piste des Gardiens et que tous les paris du tour sont gagnés, l'Éveil de la Forêt met immédiatement fin à la partie."
  },
  "sequence_tour_6_etapes": {
    "1_preparation": "Début du Tour 5 uniquement : retournez la Réglette des Tactiques sur sa Face B (Acte 2). Pioche secrète d'1 carte du paquet Machine par joueur sous paravent (en cas de pénurie, distribution horaire depuis le Peuple ayant le plus d'Arbres debout). Seul un joueur ayant tiré une carte Machine lance ses 2 dés et retient le dé le plus faible (case 1 à 6 visée) ; une carte Sabotage ne lance aucun dé.",
    "2_pose_defenseurs": "Sous paravent fermé : 1) premier Défenseur posé simultanément et définitivement (sa propre piste non-Route, ses deux lisières libres, toute rive ouverte de Furtivité d'une piste active, ou tout Rêve déjà en piste) ; 2) Défenseur d'ajustement posé librement partout sur le plateau (face Réflexion déplaçable en réaction aux poses visibles jusqu'à validation unanime face Définitif), incluant la Piste des Gardiens (0, 1 ou 2 Défenseurs maximum par Gardien).",
    "3_ouverture_et_reves": "Construction obligatoire de chaque tuile de lisière réunissant 2 Défenseurs avant d'ouvrir les paravents (Gardien case libre 1–6 ; Rêve sur la case libre la plus à droite 6, 5… ; Nid sur parcelle libre sans machine ni autre Nid). Ouverture simultanée des paravents : cartes Sabotage écartées (allument 3. Sabotage), déviations d'Insectes (±1 cran, allument 6. Insecte), puis Rêves défendus (chaque Défenseur présent annule 1 machine prioritaire, les machines restantes jouent la Tactique dessous ; allume 5. Rêve uniquement si un Rêve muni d'au moins 1 Défenseur annule au moins 1 machine non déviée). Balayage 1 à 6 des Gardiens.",
    "4_furtivite_nids_migration": "Furtivité « Chaud vs Calme » par piste active : seule une rive portant un binôme complet de 2 Défenseurs est évaluée selon le nombre (0, 1 ou 2) de machines de cette piste mobilisées ce tour-ci (cartes Machine révélées + machines déjà en Ratissage, indépendamment de toute déviation d'Insecte ou annulation par Rêve). Rive Piège gagnée si 2 machines (le propriétaire pose 1 Piège sur une parcelle non-Route sans Piège de sa piste) ; Rive Sabotage gagnée si 0 machine (+1 carte Sabotage mise de côté pour le remélange). Production des Nids : chaque Nid portant au moins 1 Défenseur crée +1 Insecte (0–1 présent) ou +2 Insectes (2 ou plus), puis applique son éventuel pouvoir propre. Migration : chaque Insecte en forêt peut bouger de 0 ou 1 cran (suivi par retournement) vers une parcelle voisine non-Route ou en aller simple définitif depuis la dernière parcelle non rasée vers une case 1 à 6 des pistes centrales.",
    "5_attaques_et_verdict": "Ordre de passage : cases 1 à 6 de la Réglette des Tactiques puis machines en Ratissage (Assaut permanent Sur place avec +1 Puissance imprimé) ; Abatteuse avant Bulldozer sur une même piste. Seuil de Parade = Seuil imprimé de la parcelle + jetons Puissance rouges (en Assaut et Ratissage uniquement ; ignorés en Charge) − jetons Surchauffe bleus + modificateur de Tactique (−1 sur 3 et 6 En avançant), minimum 1. Chaîne des parades : pouvoirs spéciaux automatiques (1. Parade) -> Piège autonome (pare automatiquement 1 unique frappe même sans Défenseur ni Insecte, allume 2. Piégeage et est défaussé aussitôt) -> Parade classique (Défenseurs seuls -> 1. Parade ; avec défausse immédiate d'Insectes -> 6. Insecte). Frappe non parée : Abatteuse coupe tous les Arbres debout en Souches sans jamais toucher aux Souches ; Bulldozer coupe 1 Arbre en Souche puis retire toutes les Souches (0 Arbre et 0 Souche = Route Forestière + Repli vers la bordure par défaut). En Mode Charge : +1 jeton Puissance rouge maximum par activation sur toute frappe non parée ciblant une parcelle réelle non-Route. Fin d'attaques : verdict des paris Gardiens puis test de fin de partie (priorité absolue Tour 8 ; Tours 1 à 7 : Sommeil du Contremaître ou Éveil de la Forêt).",
    "6_menage_fin_de_tour": "Retour en main des 2 Défenseurs de chaque joueur (y compris ceux glissés sous un Gardien après verdict), remise à zéro des effets temporaires, passage définitif sur face Ratissage de toute machine terminant le tour sur la dernière parcelle non rasée de sa piste (carte retirée du paquet), remélange complet du paquet Machine avec toutes les cartes Sabotage, passage du jeton Coordonnateur (Premier Joueur) à gauche et avancée du marqueur de Tour."
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
  const dotationStr = topoSpec.dotation.join(' – ');
  const configNum = computeConfigurationIndex();
  const totalConfigs = CHASSIS_AXES_SPEC.reduce((acc, ax) => acc * ax.options.length, 1);

  const nbAnimauxSauvages = state.peuplesCercle.filter(p => p === 'M' || p === 'R' || p === 'O').length;
  const reveilActif = nbAnimauxSauvages >= 1;
  const nbPeuplesOniriques = state.peuplesCercle.filter(p => p === 'H' || p === 'E').length;
  const nbRevesEnJeu = 2 * nbPeuplesOniriques;
  const hasInsectes = state.peuplesCercle.includes('I');
  const hasActiveSynergyTiles = lisieres.some(l => Array.isArray(l.tuiles) && l.tuiles.length > 0);

  const placementTxt = c.Placement_Initial_Machines === 'BULLDOZER_P1_ABATTEUSE_P2'
    ? '<strong>départ décalé</strong> : placez le <strong>Bulldozer sur la parcelle 1 (bordure)</strong> et l’<strong>Abatteuse sur la parcelle 2</strong> de chaque piste de forêt'
    : '<strong>départ groupé</strong> : placez l’<strong>Abatteuse et le Bulldozer ensemble sur la parcelle 1 (bordure)</strong> de chaque piste de forêt';

  const seuilOffsetTxt = Number(c.Offset_Seuil_Parade) === 1
    ? ' <span class="dyn-span">+ 1 (décalage de difficulté actif)</span>'
    : '';

  const synergieMachineTxt = c.Synergie_Binome_Machines === 'MUTUALISATION_PUISSANCE_MEME_PARCELLE'
    ? '<span class="dyn-span"><strong>Option active — Mutualisation :</strong> en Mode Assaut ou Ratissage, lorsque les deux machines d’une même piste occupent la même parcelle, la machine active additionne ses propres jetons Puissance rouges et ceux de sa partenaire.</span>'
    : '<span class="dyn-span">Chaque machine combat avec sa propre puissance, indépendamment de l’autre machine de sa piste.</span>';

  const reveMultiTxt = c.Regle_Ouverture_Reve_Multiple === 'PAR_DE_M_DESIGNE'
    ? 'son pouvoir de tuile s’applique une fois par machine visée sur cette case'
    : 'son pouvoir de tuile s’applique une seule fois par tour, quel que soit le nombre de machines sur cette case';

  const bugProf = typeof getMigrationProfile === 'function'
    ? getMigrationProfile('tactiques')
    : { nom: 'Déviation de dé', texte: 'Défaussez 1 Insecte de la case visée pour décaler le dé d’une machine de −1 ou +1 cran (entre 1 et 6).' };
  const colonieProf = typeof getMigrationProfile === 'function'
    ? getMigrationProfile('gardiens')
    : { nom: 'Bouclier de lisière', texte: 'Défaussez 1 Insecte de la case d’un Gardien ayant perdu son pari pour le garder en piste sur sa face actuelle (le pari reste perdu).' };

  const tableSummary = state.peuplesCercle.map(code => `${PEUPLES[code].icon} ${PEUPLES[code].nom}`).join(' · ');

  const container = document.getElementById('rulebook-article');
  container.innerHTML = `
    <!-- EN-TÊTE ÉDITORIAL -->
    <header class="border-b-4 border-forest-800 pb-6 mb-8">
      <div class="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div class="text-xs font-semibold uppercase tracking-[0.18em] text-forest-700 mb-1">
            Livret de Règles Officiel
          </div>
          <h1 class="text-3xl sm:text-4xl font-bold text-forest-950 tracking-tight">
            AMAZONIA : DERNIER REMPART
          </h1>
          <p class="text-sm text-slate-600 mt-1.5 font-medium">
            Jeu coopératif asymétrique à communication silencieuse · <strong>3 à 6 joueurs</strong> · <strong>8 tours en 2 Actes</strong>
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
            ${reveilActif ? `🐾 Gardiens &amp; Éveil actifs (${nbAnimauxSauvages} Peuple${nbAnimauxSauvages > 1 ? 's' : ''})` : '🐾 Sans Animaux Sauvages'}
          </span>
          <span class="px-2 py-0.5 rounded-full ${nbRevesEnJeu > 0 ? 'bg-purple-100 text-purple-900' : 'bg-slate-200 text-slate-600'} font-semibold">
            ${nbRevesEnJeu > 0 ? `🌙 ${nbRevesEnJeu} Rêves en jeu` : '🌙 Sans Peuples Oniriques'}
          </span>
          <span class="px-2 py-0.5 rounded-full ${hasInsectes ? 'bg-lime-100 text-lime-900' : 'bg-slate-200 text-slate-600'} font-semibold">
            ${hasInsectes ? '🐜 Peuple des Insectes présent' : '🐜 Sans Insectes'}
          </span>
        </div>
      </div>
    </header>

    <!-- =================================================================== -->
    <!-- 1. PRÉSENTATION & OBJECTIF                                          -->
    <!-- =================================================================== -->
    <section id="sec-presentation" class="mb-10 scroll-mt-24">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5 mb-4">
        1. Présentation &amp; Objectif
      </h2>

      <p class="text-sm text-slate-700 leading-relaxed mb-3">
        Les engins du Contremaître encerclent la grande forêt amazonienne. Depuis chaque bordure, Abatteuses et Bulldozers s’enfoncent vers le cœur sacré, transformant les arbres centenaires en souches puis en routes de terre battue. Face à cette avancée méthodique, les <strong>Peuples de la forêt</strong> — Mammifères, Reptiles, Oiseaux, Humains, Entités Magiques et Insectes — coordonnent leur résistance dans un silence tendu.
      </p>

      <p class="text-sm text-slate-700 leading-relaxed mb-4">
        <strong>Amazonia : Dernier Rempart</strong> est un jeu <strong>100 % coopératif</strong> : vous gagnez ou perdez ensemble autour d’un score commun, égal au <strong>nombre total d’Arbres encore debout</strong> à la fin de la partie. Chaque arbre sauvé compte directement dans votre score final, tandis que chaque souche préservée retarde la création de Routes Forestières. La partie dure <strong>8 tours maximum</strong>, découpés en <strong>deux Actes</strong> inversant le rythme des attaques au début du 5<sup>e</sup> tour.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4 text-xs">
        <div class="bg-forest-50 border border-forest-200 rounded-xl p-3.5">
          <div class="font-bold text-forest-900 mb-1">⏳ Fin du 8<sup>e</sup> tour</div>
          <p class="text-slate-600">Tenez bon jusqu’au terme du 8<sup>e</sup> tour (priorité absolue). Plus votre canopée aura survécu, plus votre score d’Arbres debout sera élevé.</p>
        </div>
        <div class="bg-purple-50 border border-purple-200 rounded-xl p-3.5">
          <div class="font-bold text-purple-900 mb-1">🌙 Sommeil du Contremaître</div>
          <p class="text-slate-600">
            ${nbRevesEnJeu > 0
              ? `<span class="dyn-span">Tours 1 à 7 : réunissez les <strong>${nbRevesEnJeu} tuiles Rêve</strong> en bloc continu à gauche de la Réglette (cases 1 à ${nbRevesEnJeu}) grâce aux pouvoirs de vos Tuiles de Synergie.</span>`
              : '<span class="dyn-span">Inactif sur votre table actuelle (aucun Peuple Onirique présent).</span>'}
          </p>
        </div>
        <div class="bg-amber-50 border border-amber-200 rounded-xl p-3.5">
          <div class="font-bold text-amber-900 mb-1">🌿 Éveil de la Forêt</div>
          <p class="text-slate-600">
            ${reveilActif
              ? `<span class="dyn-span">Tours 1 à 7 : engagez les <strong>${n} Défenseurs d’ajustement</strong> de la table sur la Piste des Gardiens et remportez tous les paris du tour.</span>`
              : '<span class="dyn-span">Inactif sur votre table actuelle (aucun Peuple Animal Sauvage présent).</span>'}
          </p>
        </div>
      </div>

      <div class="callout-principe">
        <div class="callout-title">✨ Principe clé — Gouvernance unitaire fluide</div>
        <p>Aucun débat collectif interminable ni vote autour de la table : chaque <strong>Tuile de Synergie</strong> (Gardien, Rêve ou Nid) et chaque piste de Migration est décidée uniquement par le joueur de son <strong>Peuple d’origine</strong> ; de même, lorsqu’un Piège est gagné en Furtivité sur une piste, seul le <strong>propriétaire de cette piste</strong> choisit la parcelle où le poser. Ce rythme net rend la partie aussi fluide sur table qu’en ligne.</p>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- 2. MATÉRIEL & MISE EN PLACE                                         -->
    <!-- =================================================================== -->
    <section id="sec-materiel" class="mb-10 scroll-mt-24">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5 mb-4">
        2. Matériel &amp; Mise en place
      </h2>

      <div id="brique-mise-en-place" class="brique-card scroll-mt-24 space-y-5">
        <div class="brique-header">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge">Mise en place</span>
            <h3 class="text-lg font-bold text-forest-950">Mise en place &amp; Lisières</h3>
          </div>
          <span class="text-xs font-mono text-forest-700"><span class="dyn-span">${n} pistes · ${totalArbres} Arbres · ${2 * n} tuiles</span></span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
            <h4 class="font-bold text-forest-900 mb-2">🌳 Le plateau circulaire</h4>
            <ul class="space-y-1.5 text-xs text-slate-700 list-disc pl-4">
              <li><span class="dyn-span"><strong>${n} pistes de forêt</strong></span> (une par joueur), composées chacune de <span class="dyn-span"><strong>${pMax} parcelles</strong></span> allant de la <strong>parcelle 1 (bordure)</strong> jusqu’à la <strong>parcelle ${pMax} (cœur)</strong>.</li>
              <li>Chaque parcelle affiche un chiffre gravé : c’est à la fois sa <strong>dotation initiale d’Arbres</strong> et son <strong>Seuil de Parade imprimé</strong> (<span class="dyn-span">${dotationStr}</span>, soit <span class="dyn-span"><strong>${topoSpec.somme} Arbres par piste</strong></span> et <span class="dyn-span"><strong>${totalArbres} Arbres</strong></span> pour toute la table).</li>
              <li>Au pied de chaque piste se trouve une zone de <strong>Furtivité</strong> à <strong>2 rives indépendantes</strong> de 2 emplacements : la <strong>🎯 Rive Piège</strong> et la <strong>🔧 Rive Sabotage</strong>. Entre deux pistes voisines, chaque <strong>lisière</strong> accueille <strong>2 Tuiles de Synergie</strong> communes aux deux Peuples adjacents.</li>
            </ul>
          </div>
          <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
            <h4 class="font-bold text-forest-900 mb-2">🧭 Les pistes centrales &amp; le matériel</h4>
            <ul class="space-y-1.5 text-xs text-slate-700 list-disc pl-4">
              <li><strong>Réglette des Tactiques réversible (Face A / Face B) :</strong> 6 cases numérotées <strong>1 à 6</strong> aux actions fixes (<em>1 &amp; 4 : Sur place</em>, <em>2 &amp; 5 : Devant</em>, <em>3 &amp; 6 : En avançant</em>), réparties en deux blocs <strong>Charge</strong> et <strong>Assaut</strong> permutés au début du Tour 5.</li>
              <li><strong>Piste des Gardiens (fixe) :</strong> 6 cases numérotées <strong>1 à 6</strong> dédiées aux 6 déclencheurs (<em>1. Parade, 2. Piégeage, 3. Sabotage, 4. Gardien, 5. Rêve, 6. Insecte</em>).</li>
              <li><strong>Par joueur :</strong> 1 paravent, 2 dés à 6 faces et <strong>2 jetons Défenseur</strong> double face (<em>Réflexion</em> / <em>Définitif</em>).</li>
              <li><strong>Machines &amp; Réserves :</strong> 1 Abatteuse et 1 Bulldozer double face (face normale / face <em>Ratissage</em>) par piste, les <span class="dyn-span"><strong>${2 * n} cartes Machine</strong></span> correspondantes, et des réserves illimitées d’Arbres/Souches, Pièges, Insectes, jetons Puissance (rouge / bleu <em>Surchauffe</em>) et cartes Sabotage identiques.</li>
            </ul>
          </div>
        </div>

        <div>
          <h4 class="text-sm font-bold text-forest-900 uppercase tracking-wider mb-2">Mise en place en 5 gestes rapides</h4>
          <ol class="space-y-1.5 text-sm text-slate-700 list-decimal pl-5">
            <li><strong>Formez le cercle de la forêt :</strong> chaque joueur choisit un Peuple et s’installe face à sa piste. Garnissez chaque parcelle de sa dotation initiale d’Arbres (<span class="dyn-span">${dotationStr}</span>).</li>
            <li><strong>Posez les pistes centrales :</strong> installez la <strong>Réglette des Tactiques sur sa Face A (Acte 1)</strong> et la Piste des Gardiens au centre de la table.</li>
            <li><strong>Garnissez les lisières :</strong> placez face visible (Face 1) les <span class="dyn-span"><strong>${2 * n} Tuiles de Synergie</strong></span> correspondant à votre cercle de Peuples (tableau ci-dessous).</li>
            <li><strong>Installez les Machines &amp; le paquet :</strong> <span class="dyn-span">${placementTxt}</span>, toutes sur leur face normale et sans jeton Puissance. Mélangez face cachée les <span class="dyn-span"><strong>${2 * n} cartes Machine</strong></span> (Abatteuse et Bulldozer de chaque piste) et posez la réserve de cartes Sabotage à côté.</li>
            <li><strong>Distribuez les accessoires :</strong> chaque joueur prend son paravent, ses 2 dés et ses 2 jetons Défenseur. Remettez le jeton <strong>Coordonnateur (Premier Joueur)</strong> au premier joueur et placez le marqueur de Tour sur <strong>1</strong>.</li>
          </ol>
        </div>

        <div>
          <h4 class="text-sm font-bold text-forest-900 uppercase tracking-wider mb-2">Emplacements de lisière actifs pour votre table (<span class="dyn-span">${2 * n} tuiles</span>)</h4>
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
        </div>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- 3. VUE D'ENSEMBLE D'UN TOUR                                         -->
    <!-- =================================================================== -->
    <section id="sec-vue-tour" class="mb-10 scroll-mt-24 space-y-4">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5">
        3. Vue d’ensemble d’un tour
      </h2>

      <p class="text-sm text-slate-700">
        Chaque tour suit toujours les <strong>6 temps</strong> ci-dessous dans l’ordre. Les deux premiers temps se jouent <strong>paravents fermés dans un silence absolu</strong> ; à l’Étape 3, les paravents s’ouvrent et la parole redevient libre jusqu’à la fin du tour.
      </p>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
        <a href="#brique-preparation" class="block border border-slate-200 hover:border-forest-400 rounded-xl p-3.5 bg-slate-50 transition">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-forest-900 text-sm">1. Préparation &amp; Dés</span>
            <span class="px-2 py-0.5 rounded bg-slate-200 text-slate-700 font-semibold">🤫 Silence</span>
          </div>
          <p class="text-slate-600">Retournement de la Réglette début Tour 5, pioche secrète d’1 carte et lancer de 2 dés (dé le plus faible retenu).</p>
        </a>

        <a href="#brique-pose" class="block border border-slate-200 hover:border-forest-400 rounded-xl p-3.5 bg-slate-50 transition">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-forest-900 text-sm">2. Pose des Défenseurs</span>
            <span class="px-2 py-0.5 rounded bg-slate-200 text-slate-700 font-semibold">🤫 Silence</span>
          </div>
          <p class="text-slate-600">Premier Défenseur simultané et fixe, puis Défenseur d’ajustement déplaçable librement jusqu’à validation unanime.</p>
        </a>

        <a href="#brique-ouverture-reves" class="block border border-emerald-200 hover:border-emerald-400 rounded-xl p-3.5 bg-emerald-50/50 transition">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-forest-900 text-sm">3. Ouverture &amp; Rêves</span>
            <span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-semibold">🗣️ Parole libre</span>
          </div>
          <p class="text-slate-600">Constructions obligatoires, ouverture des paravents, Sabotages, déviations Insectes et blocage par les Rêves défendus.</p>
        </a>

        <a href="#brique-furtivite" class="block border border-emerald-200 hover:border-emerald-400 rounded-xl p-3.5 bg-emerald-50/50 transition">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-forest-900 text-sm">4. Furtivité, Nids &amp; Migration</span>
            <span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-semibold">🗣️ Forêt vivante</span>
          </div>
          <p class="text-slate-600">Furtivité « Chaud vs Calme » par piste (Piège / Sabotage), production des Nids actifs, puis Migration des Insectes.</p>
        </a>

        <a href="#brique-attaques-piegeages" class="block border border-rose-200 hover:border-rose-400 rounded-xl p-3.5 bg-rose-50/50 transition">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-rose-900 text-sm">5. Attaques &amp; Verdict</span>
            <span class="px-2 py-0.5 rounded bg-rose-100 text-rose-800 font-semibold">⚔️ Résolution</span>
          </div>
          <p class="text-slate-600">Cases 1 à 6 (Charge / Assaut) puis Ratissages, Pièges autonomes, dégâts, verdict des Gardiens et test de fin.</p>
        </a>

        <a href="#brique-menage" class="block border border-slate-200 hover:border-forest-400 rounded-xl p-3.5 bg-slate-50 transition">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-forest-900 text-sm">6. Ménage de fin de tour</span>
            <span class="px-2 py-0.5 rounded bg-slate-200 text-slate-700 font-semibold">🔄 Remélange</span>
          </div>
          <p class="text-slate-600">Retour des Défenseurs, entrée en Ratissage au cœur, remélange complet avec les Sabotages et tour suivant.</p>
        </a>
      </div>

      <!-- Encadré Basculement dramatique Acte 1 -> Acte 2 -->
      <div class="rounded-2xl border-2 border-forest-300 bg-gradient-to-r from-amber-50/70 via-white to-rose-50/70 p-4 text-xs">
        <div class="font-bold uppercase tracking-wider text-forest-900 mb-2 flex items-center gap-1.5">
          <span>🎭 Le basculement en 2 Actes — Retournement physique de la Réglette au début du Tour 5</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-11 gap-2 items-center">
          <div class="md:col-span-5 bg-white/90 border border-amber-200 rounded-xl p-3">
            <div class="font-bold text-amber-950 text-sm mb-1">Acte 1 · Tours 1 à 4 (Face A)</div>
            <p class="text-slate-700"><strong>Cases 1–3 : ⚡ Mode Charge</strong> · <strong>Cases 4–6 : 🔥 Mode Assaut</strong></p>
            <p class="text-slate-500 mt-1">Comme vous retenez toujours le plus petit de 2 dés, les cases 1–3 sortent souvent : les engins montent en puissance si vous ne bloquez pas leurs frappes.</p>
          </div>
          <div class="md:col-span-1 text-center font-bold text-forest-800 text-base py-1">
            ↻<br><span class="text-[10px] uppercase tracking-wider">Tour 5</span>
          </div>
          <div class="md:col-span-5 bg-white/90 border border-rose-200 rounded-xl p-3">
            <div class="font-bold text-rose-950 text-sm mb-1">Acte 2 · Tours 5 à 8 (Face B)</div>
            <p class="text-slate-700"><strong>Cases 1–3 : 🔥 Mode Assaut</strong> · <strong>Cases 4–6 : ⚡ Mode Charge</strong></p>
            <p class="text-slate-500 mt-1">Retournez physiquement la Réglette (Rêves et Insectes restent sur leurs numéros de case) : les cases 1–3 libèrent désormais toute la puissance accumulée !</p>
          </div>
        </div>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- 4. DÉROULÉ D'UN TOUR ÉTAPE PAR ÉTAPE (7 BRIQUES AUTONOMES)          -->
    <!-- =================================================================== -->
    <section id="sec-deroule" class="mb-10 scroll-mt-24 space-y-5">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5">
        4. Déroulé d’un tour étape par étape
      </h2>

      <!-- BRIQUE : PRÉPARATION & DÉS -->
      <div id="brique-preparation" class="brique-card scroll-mt-24">
        <div class="brique-header">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge">Étape 1</span>
            <h3 class="text-lg font-bold text-forest-950">Préparation &amp; Dés secrets</h3>
          </div>
          <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700">🤫 Paravents fermés</span>
        </div>

        <ul class="space-y-2 text-sm text-slate-700 list-disc pl-5">
          <li><strong>Passage à l’Acte 2 (début du Tour 5 uniquement) :</strong> retournez physiquement la <strong>Réglette des Tactiques sur sa Face B</strong> en conservant les Rêves et les Insectes posés sur leurs numéros de case (1 à 6).</li>
          <li><strong>Pioche secrète :</strong> chaque joueur pioche secrètement <strong>1 carte</strong> du paquet Machine (qui contient les cartes Machine actives ainsi que toutes les cartes Sabotage intégrées au fil de la partie) et la glisse derrière son paravent.</li>
          <li><strong>Lancer de dés secret :</strong> seul un joueur ayant tiré une <strong>carte Machine</strong> lance ses <strong>2 dés secrets</strong> derrière son paravent et retient toujours le <strong>dé le plus faible</strong> (du Tour 1 au Tour 8) : ce chiffre (<code>1</code> à <code>6</code>) indique la case visée sur la Réglette des Tactiques. Un joueur ayant tiré une carte <strong>Sabotage</strong> ne lance aucun dé : le Contremaître perd cette activation.</li>
        </ul>

        <div class="callout-gardefou">
          <div class="callout-title">🛡️ Cas particuliers &amp; Garde-fous</div>
          <p><strong>Pénurie de cartes Machine :</strong> s’il reste moins de cartes dans le paquet que de joueurs autour de la table, distribuez les cartes disponibles dans le sens horaire en commençant par le joueur ayant le plus d’<strong>Arbres debout</strong> (en cas d’égalité, le plus proche du Coordonnateur dans le sens horaire). Un joueur qui ne reçoit aucune carte ne lance pas de dés mais joue normalement et pose ses deux Défenseurs à l’Étape 2.</p>
        </div>
      </div>

      <!-- BRIQUE : POSE DES DÉFENSEURS -->
      <div id="brique-pose" class="brique-card scroll-mt-24">
        <div class="brique-header">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge">Étape 2</span>
            <h3 class="text-lg font-bold text-forest-950">Pose des Défenseurs</h3>
          </div>
          <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700">🤫 Silence tactique</span>
        </div>

        <p class="text-sm text-slate-700 mb-3">
          Paravents fermés, chaque joueur engage ses <strong>2 jetons Défenseur</strong> en deux temps distincts :
        </p>

        <ol class="space-y-2.5 text-sm text-slate-700 list-decimal pl-5 mb-4">
          <li>
            <strong>Premier Défenseur (pose simultanée et définitive) :</strong> tous les joueurs posent simultanément leur premier Défenseur (face <em>Définitif</em>) sur l’une de ces destinations :
            <ul class="list-disc pl-5 mt-1 space-y-0.5 text-slate-600 text-xs sm:text-sm">
              <li>une parcelle non-Route de <strong>sa propre piste de forêt</strong> ;</li>
              <li>une Tuile de Synergie non construite de <strong>ses deux lisières</strong> (max 2 Défenseurs par tuile) ;</li>
              <li>une <strong>Rive de Furtivité</strong> libre (<em>Rive Piège</em> ou <em>Rive Sabotage</em>, max 2 Défenseurs par rive) au pied de n’importe quelle piste active ;</li>
              <li>une tuile <strong>Rêve déjà présente sur la Réglette des Tactiques</strong>.</li>
            </ul>
            Une fois posé, ce pion ne bouge plus jusqu’à l’ouverture des paravents.
          </li>
          <li>
            <strong>Autre Défenseur — ajustement muet (face <em>Réflexion</em> → <em>Définitif</em>) :</strong> chaque joueur place ensuite son <strong>Défenseur d’ajustement</strong> n’importe où sur le plateau — toutes les destinations ci-dessus (sur n’importe quelle piste de forêt non-Route, n’importe quelle lisière libre, toute rive ouverte de Furtivité ou tout Rêve en piste) <strong>plus la Piste des Gardiens</strong> (pour parier sur un Gardien déjà construit, <strong>maximum 2 Défenseurs par Gardien</strong>). Tant qu’il est face <em>Réflexion</em>, vous pouvez le déplacer librement en réaction aux poses visibles des autres joueurs ; dès que votre choix est arrêté, retournez-le face <strong>Définitif</strong>. Lorsque toute la table a validé, passez à l’Étape 3.
          </li>
        </ol>

        <div class="callout-principe">
          <div class="callout-title">✨ Principe clé — Négociation muette</div>
          <p>Aucune annonce verbale, aucun hochement de tête ni allusion à votre carte ou vos dés sous paravent : tout passe par la lecture des poses visibles. Amorcer une <em>Rive Piège</em> avec votre premier Défenseur indique silencieusement au partenaire détenant l’autre machine de cette piste qu’il peut compléter le binôme avec son Défenseur d’ajustement !</p>
        </div>

        <div class="callout-gardefou">
          <div class="callout-title">🛡️ Cas particuliers &amp; Garde-fous</div>
          <p><strong>Portée exclusive &amp; capacités :</strong> seule la <strong>Piste des Gardiens</strong> est réservée au Défenseur d’ajustement. Les rives de Furtivité accueillent au maximum <strong>2 Défenseurs par rive</strong> (sans aucun glissement automatique d’une rive à l’autre), et chaque Tuile de Synergie en lisière accueille au maximum <strong>2 Défenseurs</strong>.</p>
        </div>
      </div>

      <!-- BRIQUE : OUVERTURE & RÊVES -->
      <div id="brique-ouverture-reves" class="brique-card scroll-mt-24">
        <div class="brique-header">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge">Étape 3</span>
            <h3 class="text-lg font-bold text-forest-950">Ouverture &amp; Rêves</h3>
          </div>
          <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">🗣️ Paravents ouverts</span>
        </div>

        <ol class="space-y-2.5 text-sm text-slate-700 list-decimal pl-5">
          <li>
            <strong>Construction obligatoire (avant ouverture des paravents) :</strong> chaque tuile de lisière réunissant <strong>2 Défenseurs</strong> est construite immédiatement (en cas de constructions multiples, le Coordonnateur choisit l’ordre), suivie de son éventuel pouvoir immédiat :
            <ul class="list-disc pl-5 mt-1 space-y-0.5 text-slate-600 text-xs sm:text-sm">
              <li><strong>Gardien :</strong> placé Face 1 sur une case libre (<code>1</code> à <code>6</code>) de la Piste des Gardiens choisie par son Peuple d’origine.</li>
              <li><strong>Rêve :</strong> posé par-dessus la <strong>case libre la plus à droite</strong> de la Réglette des Tactiques (<code>6</code>, puis <code>5</code>…), sans éjecter les Tactiques ni les Insectes ; il pourra recevoir des Défenseurs dès le tour suivant.</li>
              <li><strong>Nid :</strong> posé sur une parcelle non-Route de l’une de ses deux pistes voisines sans machine ni autre Nid ; ses Défenseurs bâtisseurs l’accompagnent sur cette parcelle.</li>
            </ul>
          </li>
          <li>
            <strong>Ouverture simultanée des paravents (la parole est libre !) :</strong> tous les joueurs révèlent ensemble leurs cartes et leurs dés. Chaque carte <strong>Sabotage</strong> révélée fait perdre son activation au Contremaître, est mise de côté pour le remélange de fin de tour et allume <strong>3. Sabotage</strong>. Les cartes <strong>Machine</strong> pointent sur leur case (<code>1</code> à <code>6</code>) de la Réglette des Tactiques.
          </li>
          <li>
            <strong>Déviation éventuelle par Insecte :</strong> si un Insecte se trouve sur la case visée de la Réglette, le joueur Insectes peut le défausser pour décaler le dé d’une machine de <strong>±1 cran</strong> (entre <code>1</code> et <code>6</code>), ce qui allume <strong>6. Insecte</strong> (prioritaire sur <em>5. Rêve</em>).
          </li>
          <li>
            <strong>Rêves défendus :</strong> sur chaque case portant un <strong>Rêve muni d’au moins 1 Défenseur</strong> et visé par au moins 1 machine non déviée, chaque Défenseur présent <strong>annule 1 machine</strong> de cette case (les machines restantes exécutent la Tactique imprimée dessous à l’Étape 5). Le pouvoir propre du Rêve s’applique (<span class="dyn-span">${reveMultiTxt}</span>${hasActiveSynergyTiles ? ' ; <span class="dyn-span">avec les Tuiles de Synergie actives, certains pouvoirs permettent aussi de déplacer un Rêve vers la gauche</span>' : ''}). Le déclencheur <strong>5. Rêve</strong> s’allume uniquement lorsqu’un Rêve portant au moins 1 Défenseur s’active ainsi (selon la priorité stricte de l’ouverture : <em>3. Sabotage</em> &gt; <em>6. Insecte</em> &gt; <em>5. Rêve</em>). Un Rêve sans Défenseur reste totalement inerte.
          </li>
          <li>
            <strong>Balayage des Gardiens :</strong> parcourez la Piste des Gardiens de <code>1</code> à <code>6</code> pour résoudre les cases allumées durant l’ouverture.
          </li>
        </ol>

        <div class="callout-gardefou">
          <div class="callout-title">🛡️ Cas particuliers &amp; Garde-fous</div>
          <ul class="list-disc pl-4 space-y-1">
            <li>
              <strong>Sort des bâtisseurs (Gardien / Rêve) :</strong>
              ${n === 3
                ? '<span class="dyn-span"><strong>Table à 3 joueurs :</strong> le Peuple d’origine libère aussitôt <strong>1 des 2 Défenseurs</strong> bâtisseurs sur la première parcelle non-Route de l’une des deux pistes de la lisière ; l’autre reste en bordure jusqu’au ménage de fin de tour.</span>'
                : `<span class="dyn-span"><strong>Table à ${n} joueurs :</strong> les 2 Défenseurs bâtisseurs restent en bordure de lisière jusqu’au ménage de fin de tour.</span>`}
            </li>
            <li><strong>Priorité sur un Rêve très convoité :</strong> lorsque plusieurs machines visent un même Rêve défendu et qu’il y a moins de Défenseurs que de machines, les Défenseurs neutralisent d’abord la machine la plus menaçante ; les machines restantes exécutent ensuite la Tactique imprimée sous le Rêve.</li>
          </ul>
        </div>
      </div>

      <!-- BRIQUE : FURTIVITÉ — PIÈGE & SABOTAGE -->
      <div id="brique-furtivite" class="brique-card scroll-mt-24">
        <div class="brique-header">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge">Étape 4.1</span>
            <h3 class="text-lg font-bold text-forest-950">Furtivité — Piège &amp; Sabotage</h3>
          </div>
          <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">🎯 Chaud vs 🔧 Calme</span>
        </div>

        <p class="text-sm text-slate-700 mb-3">
          Au pied de chaque piste de forêt active figurent <strong>2 rives indépendantes</strong> de 2 places : la <strong>🎯 Rive Piège</strong> et la <strong>🔧 Rive Sabotage</strong>. Seul un <strong>binôme complet de 2 Défenseurs</strong> sur une rive est évalué. Comptez le nombre (<code>0</code>, <code>1</code> ou <code>2</code>) de machines de cette piste <strong>mobilisées ce tour-ci</strong> = <strong>cartes Machine de cette piste révélées à l’ouverture + éventuelle machine de cette piste déjà en Ratissage</strong> (indépendamment de toute déviation d’Insecte ou annulation par Rêve ; une carte Sabotage révélée ne compte pour aucune piste).
        </p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3 text-xs sm:text-sm">
          <div class="rounded-xl border border-amber-200 bg-amber-50/50 p-3.5">
            <div class="font-bold text-amber-950 mb-1">🎯 Rive Piège (« piste chaude »)</div>
            <p class="text-slate-700">Réussi si <strong>2 machines</strong> sont mobilisées → le <strong>propriétaire de la piste</strong> pose <strong>1 jeton Piège</strong> sur une parcelle non-Route (sans Piège) de sa piste. Perdu si <code>0</code> ou <code>1</code> machine.</p>
          </div>
          <div class="rounded-xl border border-sky-200 bg-sky-50/50 p-3.5">
            <div class="font-bold text-sky-950 mb-1">🔧 Rive Sabotage (« piste calme »)</div>
            <p class="text-slate-700">Réussi si <strong>0 machine</strong> n’est mobilisée → <strong>1 carte Sabotage</strong> de la réserve est mise de côté pour rejoindre le paquet Machine au remélange de fin de tour. Perdu si <code>1</code> ou <code>2</code> machines.</p>
          </div>
        </div>

        <div class="callout-exemple">
          <div class="callout-title">💡 Exemple sur le plateau — Chaud vs Calme</div>
          <ul class="list-disc pl-4 space-y-0.5">
            <li><strong>Piste chaude (2 machines) :</strong> l’Abatteuse des Mammifères est révélée à l’ouverture et leur Bulldozer est déjà en Ratissage (<code>1 + 1 = 2</code>) → le binôme en <em>Rive Piège</em> réussit et le joueur Mammifères pose 1 Piège sur sa piste.</li>
            <li><strong>Piste calme (0 machine) :</strong> aucune machine des Oiseaux n’a été tirée ni n’est en Ratissage (<code>0</code>) → le binôme en <em>Rive Sabotage</em> gagne 1 carte Sabotage pour le remélange.</li>
            <li><strong>Cas mixte (1 machine) :</strong> une seule machine mobilisée fait échouer aussi bien la Rive Piège que la Rive Sabotage.</li>
          </ul>
        </div>

        <div class="callout-gardefou">
          <div class="callout-title">🛡️ Cas particuliers &amp; Garde-fous</div>
          <ul class="list-disc pl-4 space-y-1">
            <li><strong>Pion solitaire perdu :</strong> 1 seul Défenseur posé sur une rive ne déclenche rien (et ne bascule jamais vers l’autre rive).</li>
            <li><strong>Piste intégralement rasée en Routes :</strong> dès que toutes les parcelles d’une piste sont transformées en Routes Forestières, ses deux rives deviennent immédiatement fermées et inaccessibles.</li>
            <li><strong>Aucun déclencheur Gardien :</strong> gagner un Piège ou un Sabotage en Furtivité n’allume jamais la Piste des Gardiens.</li>
          </ul>
        </div>
      </div>

      <!-- BRIQUE : NIDS & MIGRATION -->
      <div id="brique-nids-migration" class="brique-card scroll-mt-24">
        <div class="brique-header">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge">Étapes 4.2 – 4.3</span>
            <h3 class="text-lg font-bold text-forest-950">Nids &amp; Migration des Insectes</h3>
          </div>
          <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold ${hasInsectes ? 'bg-lime-100 text-lime-900' : 'bg-slate-200 text-slate-600'}">
            ${hasInsectes ? '🐜 Actif sur votre table' : '🐜 Table sans Insectes'}
          </span>
        </div>

        <p class="text-xs text-slate-600 mb-3">
          ${hasInsectes
            ? '<span class="dyn-span">Le <strong>Peuple des Insectes</strong> siège autour de votre table : résolvez la production des Nids puis la Migration à chaque tour.</span>'
            : '<span class="dyn-span">Le Peuple des Insectes est absent de votre table actuelle : passez directement à la résolution des attaques (brique suivante).</span>'}
        </p>

        <ol class="space-y-2 text-sm text-slate-700 list-decimal pl-5">
          <li><strong>Production des Nids en forêt :</strong> chaque Nid présent en forêt et occupé par <strong>au moins 1 Défenseur</strong> se résout dans l’ordre choisi par le joueur Insectes comme un bloc indivisible : créez <strong>1 jeton Insecte</strong> sur sa parcelle s’il y a 0 ou 1 Insecte à cet instant (ou <strong>2 jetons Insecte</strong> s’il y en a déjà 2 ou plus), puis appliquez son éventuel pouvoir propre avant de balayer la Piste des Gardiens. <em>(Cette production n’allume pas la case 6. Insecte.)</em></li>
          <li><strong>Migration facultative (0 ou 1 cran) :</strong> chaque jeton Insecte présent en forêt peut rester sur place ou se déplacer d’<strong>1 cran</strong> vers une parcelle voisine non-Route de sa piste (en sautant les Routes Forestières). Retournez chaque pion déplacé sur son autre face pour suivre vos mouvements, puis remettez-les tous à l’endroit une fois terminé. Depuis la <strong>dernière parcelle non rasée</strong> d’une piste, 1 cran permet un <strong>aller simple définitif</strong> vers n’importe quelle case (<code>1</code> à <code>6</code>) des pistes centrales (<strong>Réglette des Tactiques</strong> ou <strong>Piste des Gardiens</strong>, sans limite par case).</li>
        </ol>

        <div class="callout-gardefou">
          <div class="callout-title">🛡️ Cas particuliers &amp; Garde-fous</div>
          <ul class="list-disc pl-4 space-y-1">
            <li><strong>Contact Machine–Nid :</strong> toute machine entrant sur la parcelle d’un Nid (par avancée, recul ou repli depuis une Route) renvoie immédiatement le Nid en lisière (reconstructible plus tard) et défausse tous les Insectes de la parcelle. Les Défenseurs et un éventuel Piège restent en place.</li>
            <li><strong>Hors Furtivité :</strong> les Insectes ne migrent jamais dans les zones de Furtivité.</li>
          </ul>
        </div>
      </div>

      <!-- BRIQUE : RÉSOLUTION DES ATTAQUES & PIÉGEAGES -->
      <div id="brique-attaques-piegeages" class="brique-card scroll-mt-24">
        <div class="brique-header">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge">Étape 5</span>
            <h3 class="text-lg font-bold text-forest-950">Résolution des attaques &amp; Piégeages</h3>
          </div>
          <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-rose-100 text-rose-800">⚔️ Cases 1 → 6 puis Ratissage</span>
        </div>

        <p class="text-sm text-slate-700 mb-3">
          <strong>Ordre de passage :</strong> résolvez d’abord les machines actives des <strong>cases 1 à 6 de la Réglette des Tactiques</strong> (y compris sous un Rêve si elles n’ont pas été annulées), puis toutes les machines en <strong>Ratissage</strong> (<strong>Assaut permanent</strong> Sur place avec <strong>+1 Puissance imprimé</strong>). Sur une même piste au même rang (ou en Ratissage), l’<strong>Abatteuse agit toujours avant le Bulldozer</strong> ; entre pistes distinctes, choisissez librement l’ordre. Résolvez chaque machine entièrement (cibles réelles → frappes → avancée éventuelle sur <code>3</code>/<code>6</code> → gain éventuel en Charge → balayage des Gardiens <code>1</code> à <code>6</code>).
        </p>

        <div class="space-y-3 text-sm text-slate-700 mb-3">
          <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-1.5">
            <div class="font-bold text-forest-900">1. Calcul du Seuil de Parade (pour chaque parcelle ciblée)</div>
            <p class="text-xs sm:text-sm text-slate-700">
              <strong>Seuil de Parade</strong> = <strong>Seuil imprimé de la parcelle</strong> (<span class="dyn-span">${dotationStr}</span>) + <strong>jetons Puissance rouges</strong> de la machine (en <strong>Mode Assaut</strong> et en <strong>Ratissage</strong> avec son bonus <strong>+1 imprimé</strong> ; <strong>ignorés en Mode Charge</strong>) − <strong>jetons Surchauffe bleus</strong> + <strong>modificateur de Tactique</strong> (<code>0</code> sur <code>1/2/4/5</code>, <strong>−1</strong> sur les cases <code>3</code> et <code>6</code> <em>En avançant</em>)${seuilOffsetTxt}, <strong>minimum 1</strong>.
            </p>
            <p class="text-xs text-slate-600">${synergieMachineTxt}</p>
          </div>

          <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-1.5">
            <div class="font-bold text-forest-900">2. Chaîne impérative des parades</div>
            <ol class="list-decimal pl-5 space-y-1 text-xs sm:text-sm text-slate-700">
              <li><strong>Pouvoirs spéciaux éventuels</strong> de parade automatique → allume <strong>1. Parade</strong>.</li>
              <li><strong>Piège autonome :</strong> s’il y a un jeton <strong>Piège</strong> sur la parcelle attaquée, il <strong>pare automatiquement cette frappe</strong> (même sans aucun Défenseur ni Insecte sur la parcelle, sans consommer les pions présents), allume uniquement <strong>2. Piégeage</strong>, puis est <strong>défaussé aussitôt</strong> (1 Piège = 1 unique frappe bloquée).</li>
              <li><strong>Parade par Défenseurs et Insectes :</strong> si <code>Défenseurs présents + Insectes présents ≥ Seuil</code>, la frappe est parée. Défenseurs seuls → allume <strong>1. Parade</strong> ; si des jetons Insecte complètent le Seuil, défaussez à la volée le nombre exact d’Insectes manquants → allume <strong>6. Insecte</strong>.</li>
            </ol>
          </div>

          <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-2">
            <div class="font-bold text-forest-900">3. Si la frappe n’est pas parée</div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2.5 text-xs">
              <div class="bg-white border border-slate-200 rounded-lg p-2.5">
                <div class="font-bold text-slate-900 mb-1">🪓 Dégâts immédiats (Charge &amp; Assaut)</div>
                <ul class="list-disc pl-4 space-y-0.5 text-slate-700">
                  <li><strong>Abatteuse :</strong> coupe <strong>tous les Arbres debout</strong> de la parcelle (transformés en Souches) et <strong>ne touche jamais aux Souches</strong>.</li>
                  <li><strong>Bulldozer :</strong> coupe <strong>1 Arbre</strong> (en Souche) puis retire <strong>toutes les Souches</strong> non protégées — si la parcelle n’a plus ni Arbre ni Souche, elle devient définitivement une <strong>Route Forestière</strong>.</li>
                </ul>
              </div>
              <div class="bg-white border border-slate-200 rounded-lg p-2.5 space-y-1.5">
                <div>
                  <span class="font-bold text-amber-900">⚡ En Mode Charge</span> <span class="text-slate-500">(Acte 1 : 1–3 · Acte 2 : 4–6)</span> :
                  si au moins une frappe ciblant une parcelle réelle non-Route n’est ni parée ni piégée, la machine gagne <strong>+1 jeton Puissance rouge</strong> (<strong>1 jeton maximum par activation</strong>, même sur double cible <em>En avançant</em>).
                </div>
                <div>
                  <span class="font-bold text-rose-900">🔥 En Mode Assaut</span> <span class="text-slate-500">(Acte 1 : 4–6 · Acte 2 : 1–3 · Ratissage)</span> :
                  tous les jetons Puissance rouges comptent au Seuil ; aucun nouveau jeton n’est gagné.
                </div>
              </div>
            </div>
          </div>
        </div>

        <p class="text-xs sm:text-sm text-slate-700 mb-3">
          <strong>Fin des attaques :</strong> une fois toutes les machines résolues, tranchez les <strong>paris Gardiens</strong> (brique <em>Gardiens &amp; Éveil</em>) puis vérifiez les <strong>conditions de fin de partie</strong> (Section 6). Si la partie continue, passez au Ménage de fin de tour.
        </p>

        <div class="callout-exemple">
          <div class="callout-title">💡 Exemple sur le plateau — Piège autonome, Mode Charge &amp; Mode Assaut</div>
          <ul class="list-disc pl-4 space-y-1">
            <li><strong>Piège autonome (1 frappe puis retrait immédiat) :</strong> une Abatteuse et un Bulldozer attaquent la même parcelle dotée d’un seul Piège et d’aucun Défenseur. L’Abatteuse passe en premier : le Piège bloque automatiquement sa frappe, allume <em>2. Piégeage</em> et est <strong>défaussé aussitôt</strong>. Le Bulldozer qui suit trouve la parcelle sans Piège !</li>
            <li><strong>Charge vs Assaut :</strong> au Tour 2 (<em>Face A</em>), un Bulldozer portant 2 jetons Puissance révèle <code>1</code> (<strong>Charge · Sur place</strong>) sur une parcelle de Seuil imprimé 2 : ses 2 jetons sont ignorés (Seuil = <code>2</code>). Non paré, il coupe/terrasse et gagne <strong>+1 jeton Puissance</strong> (il passe à 3). Au Tour 6 (<em>Face B</em>), ce même <code>1</code> est passé en <strong>Assaut</strong> : ses 3 jetons frappent au Seuil (<code>2 + 3 = 5</code>) !</li>
          </ul>
        </div>

        <div class="callout-gardefou">
          <div class="callout-title">🛡️ Cas particuliers &amp; Garde-fous</div>
          <ul class="list-disc pl-4 space-y-1">
            <li><strong>Pont routier &amp; Repli sur création de Route :</strong> le long d’une piste, les Routes Forestières sont toujours <strong>sautées comme un pont</strong> (pour viser <em>Devant</em>, avancer, reculer ou migrer), mais restent infranchissables latéralement et ne portent aucun pion. Quand une parcelle devient Route (0 Arbre et 0 Souche), défaussez tout pion dessus : chaque machine présente <strong>recule vers la bordure par défaut</strong> (1<sup>re</sup> parcelle non rasée côté bordure), avance <strong>vers le cœur uniquement si toutes les parcelles côté bordure sont déjà en Routes</strong>, et <strong>quitte définitivement la partie</strong> si toute la piste est en Routes (une machine déjà en Ratissage conserve sa face Ratissage en cas de repli).</li>
            <li><strong>Attaque « Devant » hors-plateau :</strong> lancée depuis la dernière parcelle non rasée d’une piste, une frappe <em>Devant</em> tape dans le vide et ne rapporte jamais de jeton Puissance en Mode Charge.</li>
          </ul>
        </div>
      </div>

      <!-- BRIQUE : MÉNAGE DE FIN DE TOUR -->
      <div id="brique-menage" class="brique-card scroll-mt-24">
        <div class="brique-header">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge">Étape 6</span>
            <h3 class="text-lg font-bold text-forest-950">Ménage de fin de tour</h3>
          </div>
          <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700">🔄 Préparation du tour suivant</span>
        </div>

        <ol class="space-y-1.5 text-sm text-slate-700 list-decimal pl-5">
          <li><strong>Retour des Défenseurs :</strong> chaque joueur reprend en main ses <strong>2 jetons Défenseur</strong> (y compris ceux glissés sous un Gardien une fois les paris résolus en fin d’attaques, ainsi que ceux posés sur les Rêves, en Furtivité ou en bordure de lisière). Les effets temporaires du tour prennent fin.</li>
          <li><strong>Passage définitif en Ratissage :</strong> toute machine qui termine le tour sur la <strong>dernière parcelle non rasée</strong> de sa piste est retournée définitivement sur sa face <strong>Ratissage</strong> et sa carte est retirée définitivement du paquet Machine (détachée de la Réglette, elle agira désormais en <strong>Assaut permanent</strong> Sur place avec <strong>+1 Puissance imprimé</strong>).</li>
          <li><strong>Remélange complet du paquet Machine :</strong> rassemblez toutes les cartes Machine encore actives avec <strong>toutes les cartes Sabotage</strong> (déjà dans le paquet, révélées ce tour-ci ou nouvellement gagnées en Rive Sabotage) et mélangez-les face cachée.</li>
          <li><strong>Passage du Premier Joueur &amp; Tour suivant :</strong> passez le jeton <strong>Coordonnateur (Premier Joueur)</strong> au joueur à votre gauche et avancez le marqueur de Tour. <em>(Au début du Tour 5, retournez la Réglette des Tactiques sur sa Face B !)</em></li>
        </ol>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- 5. LES PEUPLES ET LEURS MÉCANIQUES PROPRES (3 BRIQUES COLORÉES)     -->
    <!-- =================================================================== -->
    <section id="sec-peuples" class="mb-10 scroll-mt-24 space-y-5">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5">
        5. Les Peuples et leurs mécaniques propres
      </h2>

      <!-- 5.1 ANIMAUX SAUVAGES — GARDIENS & ÉVEIL -->
      <div id="brique-gardiens-eveil" class="brique-card brique-card-amber scroll-mt-24 space-y-3.5">
        <div class="brique-header border-amber-200">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge bg-amber-100 text-amber-950 border-amber-300">5.1 Animaux Sauvages</span>
            <h3 class="text-lg font-bold text-amber-950">Gardiens &amp; Éveil (🐆 Mammifères, 🐍 Reptiles, 🦜 Oiseaux)</h3>
          </div>
          <span class="px-2.5 py-0.5 rounded-full text-xs font-bold ${reveilActif ? 'bg-amber-200 text-amber-950' : 'bg-slate-200 text-slate-600'}">
            ${reveilActif ? `Actif sur votre table (${nbAnimauxSauvages} Peuple${nbAnimauxSauvages > 1 ? 's' : ''})` : 'Inactif sur votre table'}
          </span>
        </div>

        <p class="text-sm text-slate-700">
          ${reveilActif
            ? '<span class="dyn-span">Au moins un Peuple Animal Sauvage siège autour de votre table : la <strong>Piste des Gardiens</strong> et l’<strong>Éveil de la Forêt</strong> sont pleinement actifs.</span>'
            : '<span class="dyn-span">Aucun Peuple Animal Sauvage ne siège autour de votre table : la Piste des Gardiens et l’Éveil de la Forêt restent inactifs durant cette partie.</span>'}
        </p>

        <ul class="space-y-2 text-sm text-slate-700 list-disc pl-5">
          <li><strong>Pari uniforme (0, 1 ou 2 Défenseurs maximum par Gardien) :</strong> lors de la pose du Défenseur d’ajustement, les joueurs peuvent placer <strong>0, 1 ou 2 Défenseurs</strong> sur chaque Gardien construit sur les cases <code>1</code> à <code>6</code> (sans Défenseur, le Gardien reste paisiblement inactif sans risque). À chaque déclenchement de sa case, <strong>glissez 1 Défenseur sous la tuile</strong> et appliquez aussitôt son pouvoir (avec 2 Défenseurs et 2 déclenchements dans le tour, il s’ouvre deux fois).</li>
          <li><strong>Verdict en fin d’attaques :</strong>
            <ul class="list-disc pl-5 mt-1 space-y-0.5 text-slate-600 text-xs sm:text-sm">
              <li><strong>Pari exact gagné</strong> (tous ses Défenseurs ont été glissés sous la tuile) → le Gardien reste en piste et, s’il est double-face encore en Face 1, passe sur sa <strong>Face 2</strong> pour les tours suivants.</li>
              <li><strong>Pari manqué</strong> (il reste 1 ou 2 Défenseurs dessus) → le Gardien retourne immédiatement en lisière Face 1 (reconstructible plus tard), sauf <em>Bouclier de lisière</em>.</li>
            </ul>
          </li>
          <li><strong>Éveil de la Forêt (Tours 1 à 7) :</strong> si tous les <span class="dyn-span"><strong>${n} Défenseurs d’ajustement</strong></span> de la table ont été engagés sur la Piste des Gardiens et que <strong>tous les paris du tour sont gagnés</strong>, la Forêt s’éveille et met immédiatement fin à la partie !</li>
        </ul>

        <div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-amber-900 mb-2">Les 6 déclencheurs &amp; leur ordre strict de priorité</h4>
          <div class="overflow-x-auto border border-amber-200 rounded-xl bg-white">
            <table class="w-full text-xs text-left border-collapse">
              <thead class="bg-amber-900 text-white">
                <tr>
                  <th class="p-2 w-28">Case</th>
                  <th class="p-2 w-36">Moment</th>
                  <th class="p-2">Condition exacte d’allumage (ordre strict)</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-amber-100 text-slate-700">
                <tr>
                  <td class="p-2 font-bold text-amber-950">1. Parade</td>
                  <td class="p-2">Attaques (Étape 5)</td>
                  <td class="p-2">Frappe bloquée par <strong>Défenseurs seuls</strong> (sans Piège ni dépense d’Insecte) ou par pouvoir automatique de parade.</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-amber-950">2. Piégeage</td>
                  <td class="p-2">Attaques (Étape 5)</td>
                  <td class="p-2">Un <strong>Piège autonome</strong> arrête une frappe de machine (prioritaire sur la Parade et les Insectes).</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-amber-950">3. Sabotage</td>
                  <td class="p-2">Ouverture (Étape 3)</td>
                  <td class="p-2">Une <strong>carte Sabotage</strong> est révélée à l’ouverture des paravents (prioritaire à l’ouverture).</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-amber-950">4. Gardien</td>
                  <td class="p-2">Tout le tour</td>
                  <td class="p-2">À la <strong>1<sup>re</sup> ouverture du tour de chaque autre Gardien distinct</strong> (cases 1, 2, 3, 5 ou 6 ; jamais en boucle sur elle-même).</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-amber-950">5. Rêve</td>
                  <td class="p-2">Ouverture (Étape 3)</td>
                  <td class="p-2">Un <strong>Rêve muni d’au moins 1 Défenseur</strong> annule au moins 1 machine non déviée par un Insecte.</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-amber-950">6. Insecte</td>
                  <td class="p-2">Ouverture ou Attaques</td>
                  <td class="p-2">Un Insecte de la Réglette <strong>dévie un dé</strong> à l’ouverture (prioritaire sur <em>5. Rêve</em>) <strong>OU</strong> une Parade en forêt défausse <strong>au moins 1 Insecte</strong> (prioritaire sur <em>1. Parade</em>).</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="callout-principe">
          <div class="callout-title">✨ Principe clé — 1 événement = au plus 1 déclencheur</div>
          <p>Chaque carte révélée à l’ouverture et chaque frappe bloquée durant les attaques allume <strong>au plus une seule case</strong> selon la priorité ci-dessus, sans cumul ambigu. La Furtivité et la production des Nids n’allument jamais la Piste des Gardiens.</p>
        </div>

        <div class="callout-gardefou">
          <div class="callout-title">🛡️ Cas particuliers &amp; Garde-fous</div>
          <ul class="list-disc pl-4 space-y-1">
            <li><strong>Cascades de la case 4. Gardien :</strong> la case 4 est marquée lors de la <strong>1<sup>re</sup> ouverture du tour de chaque autre Gardien distinct</strong> (un Gardien qui s’ouvre deux fois ne l’allume qu’une fois, et la case 4 ne s’auto-alimente jamais). Terminez toujours intégralement l’effet en cours avant d’exécuter les Gardiens marqués par <strong>balayage à plat de 1 à 6</strong> (pour valider un pari à 2 Défenseurs sur la case 4, il faut donc ouvrir 2 autres Gardiens distincts dans le tour).</li>
            <li><strong>Bouclier de lisière :</strong> si un jeton Insecte se trouve sur la case d’un Gardien ayant perdu son pari, le joueur Insectes peut le défausser pour maintenir la tuile en piste sur sa face actuelle ; le pari demeure néanmoins <strong>perdu</strong> pour le test d’Éveil de la Forêt.</li>
          </ul>
        </div>
      </div>

      <!-- 5.2 PEUPLES ONIRIQUES — RÊVES & SOMMEIL -->
      <div id="brique-reves-sommeil" class="brique-card brique-card-purple scroll-mt-24 space-y-3">
        <div class="brique-header border-purple-200">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge bg-purple-100 text-purple-950 border-purple-300">5.2 Peuples Oniriques</span>
            <h3 class="text-lg font-bold text-purple-950">Rêves &amp; Sommeil (🏹 Humains, ✨ Entités Magiques)</h3>
          </div>
          <span class="px-2.5 py-0.5 rounded-full text-xs font-bold ${nbRevesEnJeu > 0 ? 'bg-purple-200 text-purple-950' : 'bg-slate-200 text-slate-600'}">
            ${nbRevesEnJeu > 0 ? `${nbRevesEnJeu} tuiles Rêve sur votre table` : 'Inactif sur votre table'}
          </span>
        </div>

        <p class="text-sm text-slate-700">
          ${nbRevesEnJeu > 0
            ? `<span class="dyn-span">Votre table compte <strong>${nbRevesEnJeu} tuiles Rêve</strong> en jeu. Pour remporter le <strong>Sommeil du Contremaître</strong> aux Tours 1 à 7, réunissez toutes ces ${nbRevesEnJeu} tuiles en un bloc continu sur les <strong>cases 1 à ${nbRevesEnJeu}</strong> de la Réglette des Tactiques.</span>`
            : '<span class="dyn-span">Aucun Peuple Onirique ne siège autour de votre table : aucune tuile Rêve n’est présente et le Sommeil du Contremaître est inactif durant cette partie.</span>'}
        </p>

        <ul class="space-y-2 text-sm text-slate-700 list-disc pl-5">
          <li><strong>Pose sans éjection :</strong> tout Rêve construit se pose par-dessus la <strong>case libre la plus à droite</strong> de la Réglette (<code>6</code>, puis <code>5</code>…), sans jamais retirer les Tactiques imprimées ni déplacer les Insectes présents.</li>
          <li><strong>Bouclier d’annulation (accessible dès le premier Défenseur) :</strong> dès les tours suivants, n’importe quel joueur peut placer son <strong>premier Défenseur</strong> comme son <strong>Défenseur d’ajustement</strong> sur un Rêve en piste (ce qui permet notamment de défendre un Rêve avec son premier Défenseur tout en engageant tous les Défenseurs d’ajustement sur la Piste des Gardiens pour tenter un Éveil !). À l’ouverture, chaque Défenseur présent sur un Rêve visé <strong>annule 1 machine</strong> de cette case, applique le pouvoir du Rêve (<span class="dyn-span">${reveMultiTxt}</span>) et allume <strong>5. Rêve</strong> s’il annule au moins 1 machine non déviée. Sans Défenseur, un Rêve reste totalement inerte.</li>
          <li><strong>Sommeil du Contremaître (Tours 1 à 7) :</strong> remporté dès que toutes les tuiles Rêve de la partie sont réunies en bloc continu à gauche (<code>cases 1 à k</code>). Le déplacement des Rêves vers la gauche est porté par les pouvoirs des <strong>Tuiles de Synergie</strong> lorsqu’elles sont actives ; lorsque l’on joue avec des tuiles neutres, cette condition reste naturellement en veille.</li>
        </ul>
      </div>

      <!-- 5.3 PEUPLE DES INSECTES — NIDS & MIGRATIONS -->
      <div id="brique-peuple-insectes" class="brique-card brique-card-lime scroll-mt-24 space-y-3.5">
        <div class="brique-header border-lime-200">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge bg-lime-100 text-lime-950 border-lime-300">5.3 Peuple des Insectes</span>
            <h3 class="text-lg font-bold text-lime-950">Peuple des Insectes (🐜) — Nids &amp; Migrations</h3>
          </div>
          <span class="px-2.5 py-0.5 rounded-full text-xs font-bold ${hasInsectes ? 'bg-lime-200 text-lime-950' : 'bg-slate-200 text-slate-600'}">
            ${hasInsectes ? 'Actif sur votre table' : 'Absent de votre table'}
          </span>
        </div>

        <p class="text-sm text-slate-700">
          Les jetons Insecte naissent sur les <strong>Nids</strong> occupés par au moins 1 Défenseur (<code>+1</code> Insecte s’il y en a 0 ou 1 sur la parcelle, <code>+2</code> s’il y en a déjà 2 ou plus) puis migrent d’1 cran par tour le long des pistes ou en aller simple depuis la dernière parcelle non rasée vers les pistes centrales. Un jeton Insecte offre <strong>4 usages complémentaires</strong> :
        </p>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
          <div class="bg-white border border-lime-200 rounded-xl p-3">
            <div class="font-bold text-lime-950 mb-1">1. 🛡️ Renfort (+1) en Parade forêt</div>
            <p class="text-slate-700">Défaussé à la volée pendant une attaque pour compléter le Seuil de Parade d’une parcelle → allume <strong>6. Insecte</strong>.</p>
          </div>
          <div class="bg-white border border-lime-200 rounded-xl p-3">
            <div class="font-bold text-lime-950 mb-1">2. 🎲 Déviation (±1) sur la Réglette — ${bugProf.nom}</div>
            <p class="text-slate-700"><span class="dyn-span">${bugProf.texte}</span> → allume <strong>6. Insecte</strong>.</p>
          </div>
          <div class="bg-white border border-lime-200 rounded-xl p-3">
            <div class="font-bold text-lime-950 mb-1">3. 🌿 Bouclier de lisière (Gardiens) — ${colonieProf.nom}</div>
            <p class="text-slate-700"><span class="dyn-span">${colonieProf.texte}</span></p>
          </div>
          <div class="bg-white border border-lime-200 rounded-xl p-3">
            <div class="font-bold text-lime-950 mb-1">4. ✨ Coût ou catalyseur de tuile</div>
            <p class="text-slate-700">Certains pouvoirs de Tuiles de Synergie dépensent ou valorisent la présence de jetons Insecte sur le plateau.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- 6. FIN DE PARTIE & SCORE FINAL                                      -->
    <!-- =================================================================== -->
    <section id="sec-fin" class="mb-10 scroll-mt-24 space-y-4">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5">
        6. Fin de partie &amp; Score final
      </h2>

      <p class="text-sm text-slate-700">
        La fin de partie est vérifiée à un unique moment : <strong>en fin d’attaques</strong>, juste après le verdict des paris Gardiens. Dès qu’une condition est remplie, ignorez le Ménage de fin de tour et comptez immédiatement votre score final.
      </p>

      <div class="space-y-2.5 text-sm text-slate-700">
        <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
          <div class="font-bold text-slate-900">1. Fin du 8<sup>e</sup> tour (priorité absolue)</div>
          <p class="text-xs text-slate-600 mt-0.5">Au terme des attaques du <strong>Tour 8</strong>, la partie s’achève toujours sur cette fin temporelle, quelle que soit la position des Rêves ou des Gardiens.</p>
        </div>

        <div class="p-3.5 rounded-xl bg-purple-50/70 border border-purple-200">
          <div class="font-bold text-purple-950">2. Sommeil du Contremaître (Tours 1 à 7)</div>
          <p class="text-xs text-slate-700 mt-0.5">
            ${nbRevesEnJeu > 0
              ? `<span class="dyn-span">Les <strong>${nbRevesEnJeu} tuiles Rêve</strong> de la partie sont toutes construites et regroupées en bloc continu sur les <strong>cases 1 à ${nbRevesEnJeu}</strong> de la Réglette des Tactiques.</span>`
              : '<span class="dyn-span">Condition inactive dans cette partie (aucun Peuple Onirique autour de la table).</span>'}
          </p>
        </div>

        <div class="p-3.5 rounded-xl bg-amber-50/70 border border-amber-200">
          <div class="font-bold text-amber-950">3. Éveil de la Forêt (Tours 1 à 7)</div>
          <p class="text-xs text-slate-700 mt-0.5">
            ${reveilActif
              ? `<span class="dyn-span">Les <strong>${n} joueurs</strong> de la table ont tous engagé leur Défenseur d’ajustement sur la Piste des Gardiens et <strong>tous les paris du tour sont gagnés</strong> (aucun Défenseur restant sur une tuile Gardien ; un Gardien sauvé par Bouclier de lisière reste un pari perdu).</span>`
              : '<span class="dyn-span">Condition inactive dans cette partie (aucun Peuple Animal Sauvage autour de la table).</span>'}
          </p>
        </div>
      </div>

      <div class="bg-emerald-50 border-2 border-emerald-300 rounded-2xl p-4 text-sm text-emerald-950">
        <h3 class="font-bold text-base text-emerald-900 mb-1.5">🌳 Décompte final pur — Arbres encore debout uniquement</h3>
        <p class="text-xs sm:text-sm leading-relaxed">
          Additionnez uniquement les <strong>Arbres encore debout</strong> sur l’ensemble du plateau (les Souches ne valent aucun point par défaut) : c’est votre <strong>score coopératif final sur <span class="dyn-span">${totalArbres} Arbres</span> possibles</strong> !
        </p>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- 7. MÉMENTO DE TABLE (AIDE DE JEU — PAGE PDF AUTONOME)               -->
    <!-- =================================================================== -->
    <section id="sec-memento" class="page-break mb-4 scroll-mt-24 space-y-4">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5">
        7. Mémento de table (Aide de jeu)
      </h2>

      <div id="brique-memento" class="brique-card scroll-mt-24 space-y-4">
        <div class="brique-header">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge">Aide de jeu</span>
            <h3 class="text-lg font-bold text-forest-950">Mémento de table</h3>
          </div>
          <span class="text-xs font-mono text-forest-700">Fiche 1 page imprimable</span>
        </div>

        <!-- 7.1 RÉGLETTE DES TACTIQUES RECTO-VERSO + RATISSAGE -->
        <div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-forest-800 mb-1.5">Réglette des Tactiques recto-verso (Face A / Face B) &amp; Ratissage</h4>
          <div class="overflow-x-auto border border-slate-200 rounded-xl">
            <table class="w-full text-xs text-left border-collapse">
              <thead class="bg-forest-900 text-white">
                <tr>
                  <th class="p-2">Case</th>
                  <th class="p-2">Action fixe</th>
                  <th class="p-2">Parcelles ciblées</th>
                  <th class="p-2">Modif. Seuil</th>
                  <th class="p-2">Avancée</th>
                  <th class="p-2">Acte 1 (Tours 1–4 · Face A)</th>
                  <th class="p-2">Acte 2 (Tours 5–8 · Face B)</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-200 text-slate-700">
                <tr>
                  <td class="p-1.5 font-bold">1</td>
                  <td class="p-1.5 font-semibold">Sur place</td>
                  <td class="p-1.5">Sur place</td>
                  <td class="p-1.5">0</td>
                  <td class="p-1.5">—</td>
                  <td class="p-1.5 font-semibold text-amber-800 bg-amber-50/70">⚡ Charge</td>
                  <td class="p-1.5 font-semibold text-rose-800 bg-rose-50/70">🔥 Assaut</td>
                </tr>
                <tr>
                  <td class="p-1.5 font-bold">2</td>
                  <td class="p-1.5 font-semibold">Devant</td>
                  <td class="p-1.5">Prochaine parcelle non-Route vers le cœur</td>
                  <td class="p-1.5">0</td>
                  <td class="p-1.5">—</td>
                  <td class="p-1.5 font-semibold text-amber-800 bg-amber-50/70">⚡ Charge</td>
                  <td class="p-1.5 font-semibold text-rose-800 bg-rose-50/70">🔥 Assaut</td>
                </tr>
                <tr>
                  <td class="p-1.5 font-bold">3</td>
                  <td class="p-1.5 font-semibold">En avançant</td>
                  <td class="p-1.5">Sur place, puis Devant</td>
                  <td class="p-1.5 font-semibold">−1</td>
                  <td class="p-1.5">+1 parcelle vers le cœur</td>
                  <td class="p-1.5 font-semibold text-amber-800 bg-amber-50/70">⚡ Charge</td>
                  <td class="p-1.5 font-semibold text-rose-800 bg-rose-50/70">🔥 Assaut</td>
                </tr>
                <tr>
                  <td class="p-1.5 font-bold">4</td>
                  <td class="p-1.5 font-semibold">Sur place</td>
                  <td class="p-1.5">Sur place</td>
                  <td class="p-1.5">0</td>
                  <td class="p-1.5">—</td>
                  <td class="p-1.5 font-semibold text-rose-800 bg-rose-50/70">🔥 Assaut</td>
                  <td class="p-1.5 font-semibold text-amber-800 bg-amber-50/70">⚡ Charge</td>
                </tr>
                <tr>
                  <td class="p-1.5 font-bold">5</td>
                  <td class="p-1.5 font-semibold">Devant</td>
                  <td class="p-1.5">Prochaine parcelle non-Route vers le cœur</td>
                  <td class="p-1.5">0</td>
                  <td class="p-1.5">—</td>
                  <td class="p-1.5 font-semibold text-rose-800 bg-rose-50/70">🔥 Assaut</td>
                  <td class="p-1.5 font-semibold text-amber-800 bg-amber-50/70">⚡ Charge</td>
                </tr>
                <tr>
                  <td class="p-1.5 font-bold">6</td>
                  <td class="p-1.5 font-semibold">En avançant</td>
                  <td class="p-1.5">Sur place, puis Devant</td>
                  <td class="p-1.5 font-semibold">−1</td>
                  <td class="p-1.5">+1 parcelle vers le cœur</td>
                  <td class="p-1.5 font-semibold text-rose-800 bg-rose-50/70">🔥 Assaut</td>
                  <td class="p-1.5 font-semibold text-amber-800 bg-amber-50/70">⚡ Charge</td>
                </tr>
                <tr class="bg-slate-100/90 border-t-2 border-slate-300">
                  <td class="p-1.5 font-bold text-slate-900">★</td>
                  <td class="p-1.5 font-bold text-slate-900">Ratissage <em>(hors Réglette)</em></td>
                  <td class="p-1.5">Sur place (<strong>+1 Puissance imprimé</strong>)</td>
                  <td class="p-1.5">0</td>
                  <td class="p-1.5">—</td>
                  <td class="p-1.5 font-bold text-rose-900 bg-rose-100/70" colspan="2">🔥 Assaut permanent (tous jetons Puissance actifs, 0 gain)</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 7.2 AIDE-MÉMOIRE FURTIVITÉ CHAUD VS CALME -->
        <div class="bg-forest-50/70 border border-forest-200 rounded-xl p-3 text-xs">
          <div class="font-bold uppercase tracking-wider text-forest-900 mb-1.5">🧭 Furtivité par piste active (binôme complet de 2 Défenseurs requis)</div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            <div class="bg-white border border-amber-200 rounded-lg p-2">
              <strong class="text-amber-950">🎯 Rive Piège (Chaud · 2 machines mobilisées) :</strong> le propriétaire de la piste pose <strong>1 Piège autonome</strong> sur une parcelle non-Route de sa piste.
            </div>
            <div class="bg-white border border-sky-200 rounded-lg p-2">
              <strong class="text-sky-950">🔧 Rive Sabotage (Calme · 0 machine mobilisée) :</strong> <strong>+1 carte Sabotage</strong> mise de côté pour rejoindre le paquet Machine au remélange.
            </div>
          </div>
          <p class="text-[11px] text-slate-600 mt-1.5">Comptez : cartes Machine de la piste révélées à l’ouverture + Ratissages de la piste. 1 Défenseur seul = perdu · 1 machine mobilisée = les deux paris échouent.</p>
        </div>

        <!-- 7.3 SÉQUENCE DE FRAPPE & PARTITION PRIORITAIRE -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-1.5">
            <h4 class="font-bold uppercase tracking-wider text-forest-800">⚔️ Résolution d’une frappe (dans l’ordre)</h4>
            <ol class="list-decimal pl-4 space-y-1 text-slate-700">
              <li><strong>Seuil :</strong> Seuil imprimé + rouges (Assaut/Ratissage uniquement ; ignorés en Charge) − bleus + modif. Tactique (min 1).</li>
              <li><strong>Pouvoir auto :</strong> parade automatique par effet de tuile → <em>1. Parade</em>.</li>
              <li><strong>Piège autonome :</strong> pare 1 unique frappe sans dépense puis est <strong>défaussé aussitôt</strong> → <em>2. Piégeage</em>.</li>
              <li><strong>Parade classique :</strong> Défenseurs seuls → <em>1. Parade</em> ; sinon défausse à la volée des Insectes manquants → <em>6. Insecte</em>.</li>
              <li><strong>Non parée :</strong> Abatteuse coupe <strong>tous les Arbres</strong> → Souches (jamais aux Souches) ; Bulldozer = 1 Arbre + toutes Souches (0/0 = Route + Repli). En <strong>Charge</strong> : +1 jeton rouge max/activation.</li>
            </ol>
          </div>

          <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-1.5">
            <h4 class="font-bold uppercase tracking-wider text-forest-800">⚡ Partition prioritaire des 6 déclencheurs</h4>
            <ul class="list-disc pl-4 space-y-1 text-slate-700">
              <li><strong>Ouverture des paravents :</strong> <em>3. Sabotage</em> &gt; <em>6. Insecte</em> (déviation ±1) &gt; <em>5. Rêve</em> (Rêve défendu annulant ≥ 1 machine).</li>
              <li><strong>Pendant les attaques :</strong> <em>2. Piégeage</em> (Piège autonome) &gt; <em>6. Insecte</em> (Parade avec Insecte) &gt; <em>1. Parade</em> (Défenseurs seuls).</li>
              <li><strong>4. Gardien :</strong> 1<sup>re</sup> ouverture du tour de chaque autre Gardien distinct (balayage à plat 1 → 6, sans boucle).</li>
              <li><strong>Hors déclencheurs :</strong> la Furtivité et la production des Nids n’allument jamais la Piste des Gardiens.</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  `;
}
