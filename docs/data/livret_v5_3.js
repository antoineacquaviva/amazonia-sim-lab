// =========================================================================
// data/livret_v5_3.js — Socle Humain & Synthèse IA (v5.3 consolidée · 25 arbitrages)
// =========================================================================

const REGLES_COEUR_SYNTHESE = {
  "but_et_format": "Coopératif asymétrique à communication limitée (3 à 6 joueurs parmi M,R,O,H,E,I · max 8 tours). Objectif unique : maximiser le total d'Arbres debout après la Repousse Finale (plafonnée à la dotation initiale de chaque parcelle). Réserves de jetons et de cartes Sabotage illimitées.",
  "principes_transverses": {
    "gouvernance_unitaire": "Chaque Tuile de Synergie (G, R, M) et piste de Migration est gouvernée exclusivement par le joueur de son Peuple d'origine (champ origine). Zéro vote de groupe. Les cartes Sabotage sont toutes identiques et sans décision de jeu (dilution automatique du paquet Machine).",
    "communication_muette": "Silence tactique complet tant que les paravents sont fermés (seuls les placements/ajustements de Défenseurs communiquent). Sous l'ouverture anticipée de l'Ara : simple visibilité publique des cartes et dés, sans concertation orale.",
    "pont_routier": "Le long d'un rayon Forêt, toute Route Forestière est systématiquement sautée (viser devant, avancer, reculer, glisser un Piège, migrer = prochaine parcelle non rasée). Latéralement (Forêt <-> Furtivité), une Route est infranchissable et inoccupable.",
    "cascades_gardiens": "Finir intégralement l'action ou le Nid en cours avant d'examiner la Piste des Gardiens. Marquage 'utilisé' immédiat dès l'ouverture ; balayage à plat des cases allumées de 1 à 6 (répété tant qu'une case allumée porte un Gardien disponible). Faces 2 autonomes (seule la face visible s'applique) ; Loi passive marquée automatiquement dès que sa case s'allume."
  },
  "topologie_et_seuils_imprimes": {
    "roue": "N pistes Forêt (rayons p=1 bordure vers p=P_Max cœur) alternées avec N pistes Furtivité (lisières X<->Y portant 2 Tuiles de Synergie en bordure et 4 emplacements jumeaux par case Furtivité).",
    "P4_2233": "4 parcelles : arbres initiaux et Seuils Imprimés fixes [2, 2, 3, 3] (10xN arbres).",
    "P5_22233": "5 parcelles : arbres initiaux et Seuils Imprimés fixes [2, 2, 2, 3, 3] (12xN arbres).",
    "seuil_reveil_fixe": "Calculé une fois pour toutes à la mise en place : inactif si < 3 Gardiens dans la partie ; sinon min(N, gardiensEnJeu) avec plafond 5 à 6 joueurs (minimum 3). Un Gardien renvoyé en lisière perd son marqueur."
  },
  "sequence_tour_6_etapes": {
    "1_siege_et_plan": "Machines sur la dernière parcelle non rasée = Siège T4 irréversible (attaque autonome même si la tuile T4 a été éjectée). Distribution 1 carte/joueur depuis le paquet Machine (incluant les cartes Sabotage déjà intégrées ; si moins de cartes que de joueurs : sens horaire depuis le Peuple ayant le plus d'Arbres debout). Sous paravent : si carte Sabotage (ou sans carte), aucune machine activée et pas de dé M retenu ; si carte Machine, lancer 2D6 et retenir M = min(D1,D2) (modifié par Lois) qui désigne le rang sur la Piste Tactiques (si rang M = Rêve, activation machine annulée en 3.2).",
    "2_defenseurs_et_furtivite_4_slots": "Anti-blocage : pose interdite sur Route Forestière, tuile construite/pleine/inconstructible, ou rive Furtivité bordant une Route (si parcelle requise). 1er Défenseur irrévocable sur sa Forêt ou ses 2 lisières ; puis 2e Défenseur global (réflexion -> définitif). Case Furtivité = 4 emplacements (2 jumeaux rive J1, 2 jumeaux rive J2 ; max 2 Défenseurs). ENTRER sur la case (toute face) tire l'éventuel autre Défenseur sur l'emplacement jumeau du même bord ; RETOURNER de réflexion à définitif se fait strictement sur place sans déplacement.",
    "3_1_construction": "Construction obligatoire dès 2 constructeurs (ou 1 Déf + 1 Insecte avec Tamanoir). Gardien -> case libre 1..6. Rêve -> éjecte la Tactique la plus à droite, seules les tuiles à droite du trou glissent d'1 cran à gauche, pose en case 6 (Bugs fixes sur numéros). Libération d'1 bâtisseur sur 2 (N=3 ou Danse) choisie par Peuple d'origine ; si 2 libérés (N=3 + Danse), chacun choisit sa rive (limité aux Défenseurs réels). Nid -> parcelle non rasée sans machine ni autre Nid (max 1 Nid/parcelle), suivi par ses Défenseurs constructeurs.",
    "3_2_revelation_et_sabotages": "Ouverture simultanée des paravents ; fin du silence. Toute carte Sabotage révélée est simplement mise de côté (action du Contremaître perdue ce tour) pour être remélangée dans le paquet en 6.3. Dé M désignant un Rêve : annule la machine, ouvre le Rêve et l'avance r -> r-1 (max 1 ouverture/Rêve/tour en standard, ou cumulatif selon axe).",
    "4_1_furtivite": "Par binôme complet sur une case Furtivité (2 Défenseurs sur la même rive, ou 1 Déf + 1 Insecte défaussé) : 1 seule action gouvernée par le joueur de cette rive sur la parcelle Forêt non rasée de son bord — Piège si 0 machine présente (Déclencheur 2) OU Sabotage si >=1 machine présente et aucune active ce tour (Siège = active) : prenez 1 carte Sabotage de la réserve et mettez-la de côté pour l'intégrer définitivement au paquet Machine en 6.3 (allume Déclencheur 3).",
    "4_2_nids": "Chaque Nid avec >=1 Défenseur est un bloc indivisible : (1) +1 Insecte (si 0-1 présent à cet instant) ou +2 (si >=2 présents à cet instant, y compris Cazadores), puis (2) pouvoir propre du Nid, puis (3) balayage Gardiens 1..6 (Déclencheur 6). Miel des Ancêtres hors phase = jetons Insecte seuls.",
    "4_3_migration": "Chaque Insecte sur la roue peut bouger de 0 ou 1 cran (retourner le pion déplacé pour suivi, remettre à l'endroit en fin de 4.3). Depuis la dernière parcelle non rasée, aller simple définitif sans limite vers une case 1..6 de Bug du Cerveau ou Colonisation des Gardiens.",
    "5_attaques_sans_verrouillage": "Zéro dette d'Insectes et zéro verrouillage des parcelles (seul un Piège déjà déclenché ce tour ne peut plus payer de coût volontaire). Ordre : Tactiques 1..6 puis Sièges (Abatteuse avant Bulldozer sur un même rayon ; libre entre rayons distincts). Chaque machine résolue d'un seul tenant : cibles lues depuis sa position réelle à l'instant de l'attaque -> chaîne parades [1° Jaguar (2 bleus) -> 2° Harpie -> 3° Piège si Déf totale >= 1 -> 4° Parade classique avec défausse immédiate des Insectes manquants] -> dégâts (Abatteuse 2 Arbres ; Bulldozer 1 Arbre + toutes Souches, si 0/0 Route Forestière et repli machines vers bordure par défaut) -> avancée T3/T6 -> +1 Rouge T4/T5/T6 -> Siège si dernière parcelle. Contact Machine-Nid (tout mouvement entrant) : Nid renvoyé en lisière reconstructible + tous Insectes de la parcelle défaussés. Fin 5.3 : effets fin d'attaques, retrait Pièges déclenchés, puis test Fin de Partie (Tour 8, Rêve rang 1, ou marqueurs Gardiens >= seuil fixe -> Repousse Finale directe sans Étape 6).",
    "6_apprentissage": "6.1 Toute machine active ce tour-ci (activée par carte OU en Siège T4) rapporte à sa Tactique (T4 pour un Siège, uniquement si T4 est encore sur la piste) : +1/parcelle réellement endommagée (>=1 Arbre coupé ou Souche retirée) +1/Rouge acquis ce tour -1/Bleu présent (plancher 0/machine). Retraits tuiles volontaires AVANT Insectes Bug (Bug économisé si déjà 0). 6.2 Tactique strictement seule en tête avec >=1 jeton échange à gauche (si Écho des Voix Célestes amène son Rêve en case 1 -> Repousse Finale fin de tour). Remise à zéro de 100 % des jetons Apprentissage dans tous les cas. 6.3 Raz marqueurs Gardiens, retour Défenseurs, et remélange du paquet Machine (hors Siège) avec TOUTES les cartes Sabotage (révélées ce tour + nouvellement acquises)."
  },
  "supports_et_grammaire": {
    "declencheurs_gardiens_6": "1: Parade, 2: Piégeage, 3: Sabotage, 4: Gardien (Résonance), 5: Rêve, 6: Insecte.",
    "primitives_8": [
      "MOD_SEUIL",
      "CREATION_ENTITE",
      "DEPLACEMENT",
      "MOD_PUISSANCE",
      "MOD_APPRENTISSAGE",
      "PERMUTATION_PISTE",
      "PARTAGE_INFO_ETAT_GARDIEN",
      "MOD_LOI_DU_COEUR"
    ]
  }
};

function renderDidacticRulebook() {
  const n = state.peuplesCercle.length;
  const c = state.chassis;
  const { lisieres, activeTileIds } = getActiveLisieresAndTiles();
  const totalArbres = n * (c.P_Max === 5 ? 12 : 10);
  const modifiedAxes = getModifiedAxesList();
  const configNum = computeConfigurationIndex();

  const gardiensDispoCount = activeTileIds.filter(id => CATALOGUE_TUILES[id].famille === 'GARDIEN').length;
  const reveilActif = gardiensDispoCount >= 3;
  const seuilReveil = reveilActif ? Math.min(n === 6 ? 5 : n, gardiensDispoCount) : null;
  const hasR6C = activeTileIds.includes('R6') && state.profileOverrides['R6'] === 'C';

  const container = document.getElementById('rulebook-article');
  container.innerHTML = `
    <!-- EN-TÊTE ÉDITORIAL -->
    <div class="border-b-4 border-forest-800 pb-6 mb-8">
      <div class="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div class="text-xs font-mono uppercase tracking-widest text-forest-700 font-bold mb-1">
            Livret de Règles Didactique Instancié · Socle Consolidé v5.3 (25 Arbitrages)
          </div>
          <h1 class="text-3xl sm:text-4xl font-bold text-forest-950 tracking-tight">
            AMAZONIA : DERNIER REMPART
          </h1>
          <p class="text-sm text-slate-600 mt-1 font-medium">
            Jeu coopératif asymétrique à communication muette · Instance pour <span class="dyn-span">${n} joueurs (${state.peuplesCercle.map(code => PEUPLES[code].nom).join(', ')})</span> · Durée max : 8 tours
          </p>
        </div>
        <div class="bg-forest-50 border border-forest-200 rounded-xl p-3 text-xs font-mono text-forest-900">
          <div><strong>Version :</strong> v5.3 (Audit consolidé)</div>
          <div><strong>Châssis :</strong> #${configNum} / 128</div>
          <div><strong>Bundle :</strong> ${state.bundleId}</div>
          <div><strong>Pièges :</strong> Embuscade (Déf ≥ 1)</div>
        </div>
      </div>

      <div class="mt-5 grid grid-cols-1 md:grid-cols-2 gap-3 bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs">
        <div>
          <div class="font-bold text-slate-800 uppercase tracking-wider mb-1">🎯 Paramètres de cette instance :</div>
          <ul class="space-y-1 text-slate-600">
            <li>• <strong>Table (${n} Peuples) :</strong> ${state.peuplesCercle.map(p => `${PEUPLES[p].icon} ${PEUPLES[p].nom} (${p})`).join(' → ')}</li>
            <li>• <strong>Forêt & Seuils Imprimés :</strong> <span class="dyn-span">${c.P_Max === 5 ? 'P5_22233 (5 parcelles : 2-2-2-3-3)' : 'P4_2233 (4 parcelles : 2-2-3-3)'} = ${totalArbres} Arbres debout</span></li>
            <li>• <strong>Seuil fixe de Réveil :</strong> <span class="dyn-span">${reveilActif ? `${seuilReveil} Gardiens marqués « utilisé » (${gardiensDispoCount} Gardiens en lisière)` : `Inactif (${gardiensDispoCount} Gardien(s) < 3 minimum)`}</span></li>
            <li>• <strong>Écarts aux 7 axes standard :</strong> ${modifiedAxes.length === 0 ? '<span class="text-emerald-700 font-semibold">Aucun (Châssis Standard v5.3)</span>' : modifiedAxes.map(a => `<span class="px-1.5 py-0.5 bg-amber-100 text-amber-900 rounded font-mono">${a.key}=${c[a.key]}</span>`).join(' ')}</li>
          </ul>
        </div>
        <div class="border-t md:border-t-0 md:border-l border-slate-200 pt-2 md:pt-0 md:pl-4">
          <div class="font-bold text-forest-900 uppercase tracking-wider mb-1">⚖️ Trois règles d’or d’ergonomie (Table & BGA) :</div>
          <ul class="space-y-1 text-slate-600">
            <li>• <strong>Autorité par Peuple d’origine :</strong> chaque Tuile et piste de Migration est décidée uniquement par son <em>Peuple d’origine</em> (zéro vote de groupe).</li>
            <li>• <strong>Furtivité à 4 emplacements jumeaux :</strong> entrer sur une case Furtivité tire l’autre pion sur le jumeau de sa rive et oriente l’unique action du binôme.</li>
            <li>• <strong>Zéro dette & zéro verrouillage :</strong> les Insectes requis en parade sont défaussés sur-le-champ ; tant qu’un Insecte est sur le plateau, il est libre.</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- SECTION 1 : VISION & BUT DU JEU -->
    <section id="sec-vision" class="mb-9">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5 mb-3">
        1. VISION D’ENSEMBLE, GOUVERNANCE & BUT DU JEU
      </h2>
      <p class="mb-3 text-sm">
        Sur chaque parcelle où leur frappe n'est pas parée, les <strong>Abatteuses</strong> coupent jusqu'à <strong>2 Arbres debout</strong> en Souches, et les <strong>Bulldozers</strong> coupent jusqu'à <strong>1 Arbre debout</strong> en Souche puis retirent toutes les Souches non protégées. Une parcelle sans Arbre ni Souche devient une <strong>Route Forestière</strong> définitivement rasée : pour le reste de la partie, elle est <strong>systématiquement sautée le long d'un rayon</strong> (viser devant, avancer, reculer, glisser un Piège ou migrer désignent toujours la <em>prochaine parcelle non rasée</em>), mais reste <strong>infranchissable et inoccupable latéralement</strong> depuis les lisières.
      </p>
      <p class="mb-4 text-sm">
        <strong>Silence sous paravent & Autorité unitaire :</strong> Du tirage des cartes et dés jusqu'à l'ouverture simultanée des paravents (Étape 3.2), <strong>toute communication tactique (parole, signe ou allusion) est interdite</strong> : seuls les placements et ajustements de vos Défenseurs expriment vos intentions <em>(même si Le Cri d'Alarme de l'Ara ouvre les paravents par anticipation, cela n'apporte qu'une visibilité publique sans concertation orale)</em>. Une fois les paravents ouverts, chaque Tuile de Synergie et piste de Migration est gouvernée exclusivement par le joueur de son <strong>Peuple d'origine</strong> (zéro vote de groupe).
      </p>

      <div class="bg-forest-50 border-l-4 border-forest-700 p-4 rounded-r-xl">
        <h3 class="font-bold text-forest-950 text-base uppercase tracking-wide mb-1">
          Un But Unique : Arrêter le Chantier et Sauver les Arbres
        </h3>
        <p class="text-sm text-slate-700 mb-2">
          L'objectif de l'équipe est de <strong>maximiser le nombre total d'Arbres debout après la Repousse Finale</strong> (sur <span class="dyn-span">${totalArbres} Arbres initiaux</span>). La <strong>vérification de fin de partie a lieu à la fin des attaques (fin de 5.3)</strong> : si l'une des conditions ci-dessous est remplie, sautez l'Étape 6 et passez directement à la Repousse Finale <em>(exception unique : si L'Écho des Voix Célestes amène son Rêve au Rang 1 en fin d'Apprentissage 6.2, la Repousse Finale se déclenche aussitôt à la fin de ce tour)</em> :
        </p>
        <ol class="list-decimal list-inside text-sm space-y-1 text-slate-800 font-medium">
          <li><strong>Fin du contrat :</strong> À la fin des attaques du 8<sup>e</sup> tour de jeu.</li>
          <li><strong>Réveil de la Forêt :</strong> <span class="dyn-span">${reveilActif ? `Au moins <strong>${seuilReveil} Gardiens</strong> présents sur la piste portent leur marqueur « utilisé » en fin de 5.3 <em>(seuil fixe calculé à la mise en place ; un Gardien renvoyé en lisière perd son marqueur)</em>.` : `<em>Condition inactive dans cette partie (moins de 3 tuiles Gardien autour de la table).</em>`}</span></li>
          <li><strong>Sommeil du Contremaître :</strong> Une tuile Rêve occupe le <strong>Rang 1</strong> (tout à gauche) de la Piste des Tactiques.</li>
        </ol>
      </div>
    </section>

    <!-- SECTION 2 : TOPOLOGIE & MISE EN PLACE -->
    <section id="sec-topologie" class="mb-9">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5 mb-3">
        2. TOPOLOGIE DU PLATEAU & MISE EN PLACE DE CETTE PARTIE
      </h2>
      <ul class="list-disc list-inside text-sm space-y-1.5 mb-4">
        <li>
          <strong><span class="dyn-span">${n} pistes Forêt</span> (rayons p=1 à <span class="dyn-span">p=${c.P_Max}</span>) :</strong> posez les Arbres debout selon la dotation et le <strong>Seuil Imprimé fixe</strong> <span class="dyn-span">${c.P_Max === 5 ? 'P5_22233 [2, 2, 2, 3, 3]' : 'P4_2233 [2, 2, 3, 3]'}</span> (<span class="dyn-span">${totalArbres} Arbres</span>), ainsi qu'1 Abatteuse et 1 Bulldozer en p=1 sur chaque rayon. Les réserves de jetons (Insectes, Pièges, Puissance Rouge/Bleu, Apprentissage) sont illimitées.
        </li>
        <li>
          <strong><span class="dyn-span">${n} pistes Furtivité intercalées</span> (lisières X↔Y) :</strong> chaque case Furtivité comporte <strong>4 emplacements marqués</strong> : <strong>2 emplacements jumeaux</strong> sur le bord du joueur gauche et <strong>2 emplacements jumeaux</strong> sur le bord du joueur droit (maximum 2 Défenseurs par case). En bordure extérieure de chaque lisière figurent 2 emplacements de Tuiles de Synergie.
        </li>
        <li>
          <strong>Paquet des Machines & Réserve de Sabotage :</strong> formez le paquet mélangé initial des <span class="dyn-span">${2 * n} cartes Machine</span>, et placez à proximité la réserve de cartes <strong>Sabotage</strong> (toutes identiques, réserve illimitée : chaque Sabotage réussi ajoutera définitivement 1 carte Sabotage dans le paquet Machine pour lui faire perdre des activations). <span class="dyn-span">${c.Mise_En_Place_Tactiques === 'ORDRE_FIXE_T1_T6' ? 'Alignez les 6 tuiles Tactique face visible dans l’ordre croissant <code>T1</code> à <code>T6</code> des Rangs 1 à 6.' : 'Mélangez aléatoirement les 6 tuiles Tactique <code>T1</code> à <code>T6</code> des Rangs 1 à 6.'}</span>
        </li>
        <li>
          <strong>Matériel individuel :</strong> 1 Mini-Paravent, 2 dés (2D6), le <em>Premier Défenseur</em> (face définitive) et le <em>Deuxième Défenseur</em> (double-face : <em>« en réflexion »</em> / <em>« définitive »</em>).
        </li>
      </ul>

      <h3 class="text-lg font-bold text-forest-800 mt-5 mb-2">
        Les <span class="dyn-span">${2 * n} Tuiles de Synergie</span> de votre partie (et leur Peuple d’origine décideur)
      </h3>
      <div class="overflow-x-auto rounded-xl border border-slate-200 mb-4">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="bg-forest-900 text-white">
              <th class="p-2.5 border-r border-forest-700">Lisière</th>
              <th class="p-2.5 border-r border-forest-700">Code & Gouvernance</th>
              <th class="p-2.5 border-r border-forest-700">Nom de la Tuile & Support</th>
              <th class="p-2.5 border-r border-forest-700">Profil</th>
              <th class="p-2.5">Effet en jeu pour cette partie</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-200">
            ${lisieres.map(l => l.tuiles.map((tId, idx) => {
              const t = CATALOGUE_TUILES[tId];
              const pLetter = state.profileOverrides[tId] || 'A';
              const prof = t.profils[pLetter];
              const famBadge = t.famille === 'GARDIEN'
                ? 'bg-amber-100 text-amber-900'
                : (t.famille === 'REVE' ? 'bg-purple-100 text-purple-900' : 'bg-lime-100 text-lime-900');
              return `
                <tr class="hover:bg-slate-50">
                  ${idx === 0 ? `<td rowspan="2" class="p-2.5 font-bold bg-slate-50 border-r border-slate-200 align-middle whitespace-nowrap">Lisière ${l.index}<br><span class="text-forest-700">${PEUPLES[l.p1].icon} ${l.p1} ↔ ${PEUPLES[l.p2].icon} ${l.p2}</span></td>` : ''}
                  <td class="p-2.5 font-mono border-r border-slate-200 whitespace-nowrap">
                    <div class="font-bold">${tId} <span class="text-slate-500">(${t.couple.join(',')})</span></div>
                    <div class="text-[11px] text-emerald-800 font-semibold">Autorité : ${PEUPLES[t.origine] ? PEUPLES[t.origine].nom : t.origine}</div>
                  </td>
                  <td class="p-2.5 border-r border-slate-200">
                    <div class="font-bold text-slate-900">${prof.nom}</div>
                    <span class="inline-block mt-0.5 px-1.5 py-0.2 rounded text-[10px] font-semibold ${famBadge}">${t.famille} · ${prof.cycle}</span>
                  </td>
                  <td class="p-2.5 font-mono font-bold text-center border-r border-slate-200">
                    <span class="px-2 py-0.5 rounded bg-forest-100 text-forest-900 border border-forest-300">Profil ${pLetter}</span>
                  </td>
                  <td class="p-2.5 text-slate-700 leading-snug">${prof.texte}</td>
                </tr>
              `;
            }).join('')).join('')}
          </tbody>
        </table>
      </div>
    </section>

    <!-- SECTION 3 : DÉROULEMENT D'UN TOUR (6 ÉTAPES) -->
    <section id="sec-tour" class="mb-9 page-break">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5 mb-4">
        3. DÉROULEMENT DÉTAILLÉ D’UN TOUR DE JEU (6 ÉTAPES)
      </h2>

      <!-- ÉTAPE 1 -->
      <div class="mb-6">
        <h3 class="text-lg font-bold text-forest-800 mb-1.5">
          Étape 1 : Machines en Siège, Distribution secrète & Lancer des dés
        </h3>
        <ol class="list-decimal list-inside text-sm space-y-1.5">
          <li>
            <strong>Machines en Siège autonome :</strong> Toute machine déjà située sur la <strong>dernière parcelle non rasée de son rayon</strong> est en <strong>Siège</strong> irréversible (carte posée face visible sur sa parcelle). Elle agit de façon autonome en fin d'Étape 5 selon le profil de Siège (frappe sur place, modificateur <code>-1</code>, <code>+1 Rouge</code>), <strong>même si la tuile <code>T4</code> a été éjectée de la piste</strong> (tant que <code>T4</code> est sur la piste, une machine en Siège lui rapporte normalement de l'Apprentissage en 6.1).
          </li>
          <li>
            <strong>Distribution secrète (Paquet Machine + Sabotages intégrés) :</strong> Distribuez 1 carte face cachée à chaque joueur depuis le paquet (qui contient les cartes Machine hors Siège ainsi que toutes les cartes Sabotage déjà ajoutées lors des tours précédents), puis écartez le surplus sans le consulter. <em>(S'il reste moins de cartes que de joueurs, servez dans le sens horaire à partir du Peuple ayant le plus d'Arbres debout ).</em>
          </li>
          <li>
            <strong>Lancer de 2D6 sous le mini-paravent (en silence complet) :</strong>
            <ul class="list-disc list-inside ml-5 mt-1 space-y-1 text-slate-700">
              <li><strong>Si vous avez pioché une carte Sabotage :</strong> bonne nouvelle secrète, <strong>cette action du Contremaître est perdue</strong> (aucune machine n'est activée par cette carte ; ne sélectionnez aucune Tactique sous votre paravent).</li>
              <li><strong>Si vous avez pioché une carte Machine :</strong> lancez vos 2 dés ; le plus petit dé <code>M = min(D1, D2)</code> désigne le rang sur la Piste des Tactiques (sauf Loi modifiant le dé retenu). Si ce rang contient un <strong>Rêve</strong>, l'activation de votre machine sera annulée en 3.2 !</li>
            </ul>
          </li>
        </ol>

        <div class="overflow-x-auto rounded-xl border border-slate-200 mt-3">
          <table class="w-full text-left border-collapse text-xs">
            <thead>
              <tr class="bg-slate-800 text-white">
                <th class="p-2 border-r border-slate-600">Tactique</th>
                <th class="p-2 border-r border-slate-600">Cibles (lues à l’instant de l’attaque en sautant les Routes) & Effet après frappe</th>
                <th class="p-2">Mod. Seuil</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-200">
              <tr>
                <td class="p-2 font-bold font-mono">T1. Sur place</td>
                <td class="p-2">Frappe sa parcelle actuelle et y reste.</td>
                <td class="p-2 font-mono">0</td>
              </tr>
              <tr class="bg-slate-50">
                <td class="p-2 font-bold font-mono">T2. Devant</td>
                <td class="p-2">Frappe la prochaine parcelle non rasée devant elle et reste sur place.</td>
                <td class="p-2 font-mono">0</td>
              </tr>
              <tr>
                <td class="p-2 font-bold font-mono">T3. En avançant</td>
                <td class="p-2">Frappe sur place <strong>ET</strong> devant elle, puis avance d’1 parcelle non rasée vers le cœur.</td>
                <td class="p-2 font-mono text-emerald-700 font-semibold">-1 / parcelle</td>
              </tr>
              <tr class="bg-slate-50">
                <td class="p-2 font-bold font-mono">T4. Sur place +</td>
                <td class="p-2">Frappe sur place, reste, puis gagne <strong>+1 jeton Puissance rouge</strong> <em>(profil identique au Siège)</em>.</td>
                <td class="p-2 font-mono text-emerald-700 font-semibold">-1</td>
              </tr>
              <tr>
                <td class="p-2 font-bold font-mono">T5. Devant +</td>
                <td class="p-2">Frappe devant elle, reste sur place, puis gagne <strong>+1 jeton Puissance rouge</strong>.</td>
                <td class="p-2 font-mono text-emerald-700 font-semibold">-1</td>
              </tr>
              <tr class="bg-slate-50">
                <td class="p-2 font-bold font-mono">T6. En avançant +</td>
                <td class="p-2">Frappe sur place <strong>ET</strong> devant elle, avance d’1 parcelle non rasée, puis gagne <strong>+1 jeton Puissance rouge</strong>.</td>
                <td class="p-2 font-mono text-emerald-700 font-semibold">-2 / parcelle</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ÉTAPE 2 -->
      <div class="mb-6">
        <h3 class="text-lg font-bold text-forest-800 mb-1.5">
          Étape 2 : Placez vos Défenseurs en silence (et orientez les cases Furtivité)
        </h3>
        <p class="text-sm mb-2">
          <strong>Interdictions à la pose (zéro coup stérile) :</strong> Il est interdit de poser un Défenseur sur une Route Forestière, sur un emplacement de Tuile déjà construite ou déjà complet (2 pions), sur une Tuile impossible à construire (Gardien sans case libre autorisée, Nid sans parcelle légale), ou sur les 2 emplacements d'une rive de Furtivité bordant une Route Forestière.
        </p>
        <ol class="list-decimal list-inside text-sm space-y-1.5 mb-3">
          <li>
            <strong>1<sup>er</sup> Défenseur (Ancrage local irrévocable) :</strong> Chacun pose son Premier Défenseur sur sa propre piste Forêt (parcelle non rasée) ou sur l'une de ses deux lisières adjacentes (case Furtivité ou Tuile constructible).
          </li>
          <li>
            <strong>2<sup>e</sup> Défenseur (Portée globale) :</strong> Une fois tous les Premiers Défenseurs posés, chacun pose son Deuxième Défenseur partout sur le plateau (face <em>« en réflexion »</em> déplaçable d'une case à une autre, ou directement face <em>« définitive »</em>). Le passage se clôt quand tous sont sur leur face <em>« définitive »</em>.
          </li>
        </ol>
        <div class="bg-emerald-50/80 border-l-4 border-emerald-600 p-3.5 rounded-r-xl text-xs text-slate-800">
          <div class="font-bold text-emerald-950 mb-1">🧭 Règle des 4 emplacements jumeaux sur une case Furtivité (max 2 Défenseurs par case) :</div>
          • <strong>À chaque entrée d’un Défenseur sur la case</strong> (1<sup>er</sup> Défenseur, 2<sup>e</sup> en réflexion ou 2<sup>e</sup> posé directement en choix définitif) : posez-le sur l'un des 4 emplacements valides ; s'il y a déjà un autre Défenseur sur cette case (même définitif), <strong>déplacez-le aussitôt sur l'emplacement jumeau de votre bord</strong>.<br>
          • <strong>Verrouillage strictement sur place :</strong> retourner un 2<sup>e</sup> Défenseur déjà posé de sa face <em>« en réflexion »</em> à sa face <em>« définitive »</em> se fait <strong>exactement sur son emplacement actuel</strong>, sans pouvoir changer de bord ni tirer l'autre jeton (pour refuser un bord imposé tant que vous êtes en réflexion, vous devez quitter la case).
        </div>
      </div>

      <!-- ÉTAPE 3 -->
      <div class="mb-6">
        <h3 class="text-lg font-bold text-forest-800 mb-1.5">
          Étape 3 : Construisez les Tuiles de Synergie & Révélez les paravents
        </h3>
        <ol class="list-decimal list-inside text-sm space-y-1.5">
          <li>
            <strong>3.1. Construction automatique et obligatoire :</strong> Toute Tuile en lisière réunissant ses 2 constructeurs (ou <code>1 Défenseur + 1 Insecte</code> avec <em>La Brèche du Tamanoir</em>) entre obligatoirement en jeu dès ce tour :
            <ul class="list-disc list-inside ml-5 mt-1 text-slate-700 space-y-1">
              <li><strong>Gardien (G) :</strong> le joueur de son <em>Peuple d'origine</em> le pose sur une case libre autorisée (1 à 6).</li>
              <li><strong>Rêve (R) :</strong> éjectez définitivement la tuile Tactique la plus à droite sur la piste ; <strong>seules les tuiles situées à droite de ce trou</strong> glissent d'1 cran vers la gauche, puis posez le nouveau Rêve en <strong>case 6</strong> <em>(les Insectes Bug éventuels restent sur leur numéro de case)</em>.</li>
              <li><strong>Devenir des bâtisseurs (G / R) :</strong> ils restent en bordure <span class="dyn-span">${n === 3 ? '(Bonus N=3 actif : le joueur du <em>Peuple d’origine de la tuile</em> choisit 1 des 2 Défenseurs bâtisseurs pour rejoindre gratuitement la 1<sup>re</sup> parcelle adjacente non rasée de son choix ; si <em>La Danse des Esprits-Fauves</em> libère les 2, chaque propriétaire choisit sa rive, dans la limite des Défenseurs réellement présents)' : '(à 4–6 joueurs, ils restent en bordure sauf Loi comme <em>La Danse des Esprits-Fauves</em> où le Peuple d’origine libère 1 bâtisseur)'}</span>.</li>
              <li><strong>Nid de Croissance (M) :</strong> son <em>Peuple d'origine</em> le pose sur une parcelle non rasée <strong>sans machine ni autre Nid</strong> (max 1 Nid/parcelle) de l'un de ses 2 rayons ; <strong>tous ses Défenseurs constructeurs l'accompagnent sur cette parcelle</strong>.</li>
            </ul>
          </li>
          <li>
            <strong>3.2. Ouverture simultanée des paravents, Pannes de Sabotage & Rêves :</strong>
            <ul class="list-disc list-inside ml-5 mt-1 text-slate-700 space-y-1">
              <li><strong>Fin du silence & Cartes Sabotage révélées :</strong> toute carte <strong>Sabotage</strong> révélée derrière un paravent fait simplement perdre une activation au Contremaître ce tour-ci ! Mettez-la de côté près du paquet Machine : elle y sera remélangée en 6.3.</li>
              <li><strong>Rêves (dé M désignant un Rêve) :</strong> si le dé <code>M</code> d'une carte Machine désigne un Rêve, <strong>l'activation de cette machine est annulée</strong> pour le tour. <span class="dyn-span">${c.Regle_Ouverture_Reve_Multiple === 'UNIQUE_PAR_TOUR' ? 'Chaque Rêve désigné par au moins un dé M peut s’ouvrir et avancer d’1 cran vers la gauche (<code>r → r−1</code>) <strong>au maximum 1 fois ce tour-ci</strong>.' : 'Chaque sollicitation ouvre le Rêve désigné et le fait avancer d’1 cran vers la gauche (<strong>mode cumulatif</strong>).'}</span></li>
            </ul>
          </li>
        </ol>
      </div>

      <!-- ÉTAPE 4 -->
      <div class="mb-6">
        <h3 class="text-lg font-bold text-forest-800 mb-1.5">
          Étape 4 : Furtivité orientée, Nids indivisibles & Migration des Insectes
        </h3>
        <ol class="list-decimal list-inside text-sm space-y-1.5">
          <li>
            <strong>4.1. Actions des binômes en Furtivité :</strong> Sur chaque case Furtivité réunissant un binôme (2 Défenseurs alignés sur les jumeaux d'une même rive, ou <code>1 Défenseur + 1 Insecte</code> défaussé), le joueur de <strong>cette rive</strong> résout <strong>1 seule action sur la parcelle Forêt non rasée de son bord</strong> :
            <ul class="list-disc list-inside ml-5 mt-1 text-slate-700 space-y-0.5">
              <li><strong>Préparer un Piège :</strong> s'il n'y a <strong>aucune machine physiquement présente</strong> sur cette parcelle (même ciblée à distance), posez-y 1 jeton Piège (max 1/parcelle ; allume <em>2. Piégeage</em>).</li>
              <li><strong>Saboter le chantier :</strong> s'il y a <strong>au moins 1 machine présente mais aucune active ce tour-ci</strong> (une machine en Siège est active), prenez <strong>1 carte Sabotage</strong> de la réserve et mettez-la de côté pour l'intégrer <strong>définitivement</strong> au paquet Machine en 6.3 (allume <em>3. Sabotage</em>).</li>
            </ul>
          </li>
          <li>
            <strong>4.2. Production des Nids (bloc indivisible) :</strong> Chaque Nid portant au moins 1 Défenseur est résolu <strong>d'un seul tenant</strong> avant d'examiner les Gardiens : (1) posez <strong>+1 Insecte</strong> (si 0 ou 1 Insecte est présent sur la parcelle <em>à cet instant précis</em>) ou <strong>+2 Insectes</strong> (s'il y en a déjà ≥ 2 <em>à cet instant</em>), puis (2) résolvez immédiatement le pouvoir propre du Nid, et seulement ensuite (3) balayez les Gardiens de 1 à 6 (<em>6. Insecte</em>). <em>(Une production hors phase comme Le Miel des Ancêtres ne crée que les jetons Insecte).</em>
          </li>
          <li>
            <strong>4.3. Migration facultative des Insectes :</strong> Chaque Insecte présent sur la roue <strong>peut se déplacer de 0 ou 1 cran</strong> (même s'il vient de bouger en 4.2 ; retournez chaque jeton déplacé sur son verso pour suivi, puis remettez-les tous à l'endroit en fin de 4.3). Depuis la <strong>dernière parcelle non rasée d'un rayon</strong>, 1 cran permet un <strong>aller simple définitif</strong> (sans limite de pions par case) vers une case <code>1..6</code> de :
            <ul class="list-disc list-inside ml-5 mt-1 text-slate-700 space-y-0.5">
              <li><strong>Bug du Cerveau :</strong> <span class="dyn-span">${CATALOGUE_TUILES.SLOT_BUG_CERVEAU.profils[state.slotsInsectes.SLOT_BUG_CERVEAU].texte}</span></li>
              <li><strong>Colonisation des Gardiens :</strong> <span class="dyn-span">${CATALOGUE_TUILES.SLOT_COLONISATION_GARDIENS.profils[state.slotsInsectes.SLOT_COLONISATION_GARDIENS].texte}</span></li>
            </ul>
          </li>
        </ol>
      </div>

      <!-- ÉTAPE 5 -->
      <div class="mb-6">
        <h3 class="text-lg font-bold text-forest-800 mb-1.5">
          Étape 5 : Attaques des Machines (d’un seul tenant) & Test de Fin de Partie
        </h3>
        <p class="text-xs text-slate-600 mb-2">
          <em>Rappel : il n'existe aucune dette d'Insectes ni aucun verrouillage des parcelles ciblées — tant qu'un Insecte est sur le plateau, il est libre ; seul un Piège ayant déjà paré ce tour-ci ne peut plus payer de coût volontaire avant son retrait en 5.3.</em>
        </p>

        <div class="bg-slate-900 text-emerald-300 font-mono text-xs p-3 rounded-xl mb-3 text-center">
          Seuil Classique = max(1, Seuil_Imprimé(p) [${c.P_Max === 5 ? '2,2,2,3,3' : '2,2,3,3'}]${c.Offset_Seuil_Parade === 1 ? ' + 1 (Offset)' : ''} + Rouges${c.Synergie_Binome_Machines === 'MUTUALISATION_PUISSANCE_MEME_PARCELLE' ? ' (mutualisés)' : ''} − Bleus + Mod_Tactique + Mod_Tuiles)
        </div>

        <ol class="list-decimal list-inside text-sm space-y-2">
          <li>
            <strong>5.1. Ordre de passage des machines :</strong> Parcourez la <strong>Piste des Tactiques du Rang 1 au Rang 6</strong>, puis terminez par les machines en <strong>Siège</strong>. Sur un même rayon partageant le même rang (ou en Siège), <strong>l'Abatteuse agit toujours avant le Bulldozer</strong> ; entre rayons distincts au même rang, les joueurs s'organisent librement.
          </li>
          <li>
            <strong>5.2. Résolution complète de chaque machine avant de passer à la suivante :</strong>
            <ul class="list-disc list-inside ml-5 mt-1 text-slate-700 space-y-1">
              <li><strong>Cibles dynamiques :</strong> lisez la ou les parcelles visées depuis la <strong>position physique réelle de la machine à cet instant précis</strong> (en sautant les Routes Forestières ; si une cible a été rasée entre-temps, cette frappe est annulée).</li>
              <li><strong>Chaîne stricte des parades à chaque frappe :</strong> <strong>1° Bond du Jaguar</strong> (Loi auto : 2 bleus défaussés → pare toutes les frappes restantes de la machine + recul) → <strong>2° Piquée de la Harpie</strong> → <strong>3° Piège (Embuscade)</strong> si la parcelle a un Piège <strong>ET une Défense totale ≥ 1</strong> à cet instant (locale ou soutenue à distance ; allume <em>1. Parade</em>, le Piège reste actif pour ce tour et sera retiré en 5.3) → <strong>4° Parade classique</strong> si Défense (Défenseurs + Insectes) ≥ Seuil, en <strong>défaussant immédiatement</strong> les Insectes nécessaires pour atteindre le Seuil (allume <em>1. Parade</em>).</li>
              <li><strong>Dégâts si non parée :</strong> l'<strong>Abatteuse</strong> coupe jusqu'à <strong>2 Arbres</strong> en Souches <span class="dyn-span">${c.Role_Abatteuse_Fin_De_Piste === 'ARRACHE_1_SOUCHE_SI_SANS_ARBRE' ? '(et arrache 1 Souche en Siège s’il n’y a plus d’Arbre)' : '(frappe à vide sans Arbre)'}</span> ; le <strong>Bulldozer</strong> (1 seul test de parade) coupe jusqu'à <strong>1 Arbre</strong> en Souche puis retire toutes les Souches non protégées. S'il ne reste ni Arbre ni Souche, posez une <strong>Route Forestière</strong> (Nid en lisière, Pièges/Insectes défaussés, Défenseurs rendus ; les machines présentes reculent vers la prochaine parcelle non rasée côté bordure, ou vers le cœur uniquement si tout est rasé côté bordure ; retrait si tout le rayon est rasé).</li>
              <li><strong>Mouvement, Puissance & Contact Nid :</strong> la machine avance immédiatement d'1 parcelle non rasée si <code>T3/T6</code>, gagne <strong>+1 jeton Rouge</strong> si <code>T4/T5/T6</code> (ou Siège), et entre en <strong>Siège</strong> si elle occupe la <span class="dyn-span">${c.Declenchement_Fin_De_Piste === 'ARRIVEE_DERNIERE_PARCELLE' ? 'dernière parcelle non rasée' : 'case de dépassement'}</span>. <strong>Contact :</strong> tout mouvement de machine (avancée, recul ou repli) entrant sur un Nid non protégé renvoie ce Nid en lisière (reconstructible) et défausse tous les Insectes de la parcelle (Défenseurs et Piège restent).</li>
            </ul>
          </li>
          <li>
            <strong>5.3. Fin des attaques & Vérification de Fin de Partie :</strong> Résolvez les effets <em>« à la fin des attaques »</em>, retirez tous les Pièges ayant paré au moins 1 frappe ce tour-ci, puis vérifiez les 3 conditions de Fin de Partie (Section 1) : si l'une est atteinte, passez directement à la Repousse Finale !
          </li>
        </ol>
      </div>

      <!-- ÉTAPE 6 -->
      <div>
        <h3 class="text-lg font-bold text-forest-800 mb-1.5">
          Étape 6 : Apprentissage du Contremaître & Ménage de fin de tour
        </h3>
        <ol class="list-decimal list-inside text-sm space-y-1.5">
          <li>
            <strong>6.1. Décompte (cartes Machine + machines en Siège sur <code>T4</code>) :</strong> Chaque machine active ce tour-ci rapporte à la tuile Tactique qu'elle a exécutée (<code>T4</code> pour une machine en Siège, si <code>T4</code> figure encore sur la piste) : <strong>+1</strong> par parcelle où elle a <strong>effectivement coupé au moins 1 Arbre ou retiré au moins 1 Souche</strong>, <strong>+1</strong> par jeton Rouge acquis ce tour, <strong>−1</strong> par jeton Bleu <em>Surchauffe</em> qu'elle porte (minimum 0 par machine). Appliquez ensuite les <strong>retraits volontaires de tuiles avant les Insectes Bug</strong> <em>(un Bug sur une case déjà à 0 jeton n'est pas défaussé)</em>.
          </li>
          <li>
            <strong>6.2. Avancée & Remise à zéro totale :</strong> La Tactique <strong>strictement seule en tête avec au moins 1 jeton</strong> échange sa place avec sa voisine de gauche (<code>r → r−1</code>, y compris un Rêve qui recule alors à droite ; immobile au Rang 1). <strong>Dans 100 % des cas</strong> (avancée, égalité ou blocage), remettez en réserve <strong>tous les jetons Apprentissage de toutes les tuiles</strong>.
          </li>
          <li>
            <strong>6.3. Ménage & Dilution permanente :</strong> Récupérez vos Défenseurs, retirez les marqueurs <em>« utilisé »</em> des Gardiens, et formez le paquet du tour suivant en remélangeant toutes les cartes Machine (hors machines en Siège) <strong>avec toutes les cartes Sabotage</strong> (celles révélées ou écartées ce tour-ci + toutes les nouvelles cartes Sabotage acquises ce tour-ci).
          </li>
        </ol>
      </div>
    </section>

    <!-- SECTION 4 : SUPPORTS & CASCADES -->
    <section id="sec-supports" class="mb-9">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5 mb-3">
        4. LES 3 SUPPORTS D’ASYMÉTRIE & LA RÈGLE DES CASCADES À PLAT
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        <div class="p-4 rounded-xl bg-amber-50/70 border border-amber-200">
          <h3 class="font-bold text-amber-950 text-sm mb-1.5">4.1. Piste des Gardiens (Cascades 1 → 6)</h3>
          <p class="text-slate-700 mb-2">
            Déclencheurs : <strong>1. Parade, 2. Piégeage, 3. Sabotage, 4. Gardien, 5. Rêve, 6. Insecte</strong> (max 1 ouverture/tour).
          </p>
          <p class="text-slate-700">
            <strong>Balayage à plat :</strong> terminez toujours l'effet en cours, marquez le Gardien <em>« utilisé »</em> dès son ouverture, puis parcourez les cases allumées de <strong>1 à 6</strong> (répété tant qu'une case allumée porte un Gardien disponible). Seule la face visible s'applique ; une Loi passive reçoit automatiquement son marqueur dès que sa case s'allume.
          </p>
        </div>
        <div class="p-4 rounded-xl bg-purple-50/70 border border-purple-200">
          <h3 class="font-bold text-purple-950 text-sm mb-1.5">4.2. Cerveau du Rêve (Tuiles R)</h3>
          <p class="text-slate-700 mb-2">
            Entrée en <strong>case 6</strong> en éjectant la Tactique la plus à droite (seules les tuiles à droite du trou glissent à gauche).
          </p>
          <p class="text-slate-700">
            Gouverné par son <em>Peuple d'origine</em>. S'ouvre sur un double aux dés ou un dé <code>M</code> tombant sur son rang (ce qui annule la machine) et avance vers le Rang 1.
          </p>
        </div>
        <div class="p-4 rounded-xl bg-lime-50/70 border border-lime-200">
          <h3 class="font-bold text-lime-950 text-sm mb-1.5">4.3. Réseau de Croissance (Tuiles M)</h3>
          <p class="text-slate-700 mb-2">
            1 seul Nid max par parcelle (sans machine). S'il est touché par un mouvement de machine, il retourne en lisière (reconstructible) et tous les Insectes de la case sont défaussés.
          </p>
          <p class="text-slate-700">
            Ses Insectes soutiennent ou paient la Parade (défausse immédiate), forment des binômes en 4.1 et migrent librement (0 ou 1 cran) en 4.3.
          </p>
        </div>
      </div>
    </section>

    <!-- SECTION 5 : REPOUSSE FINALE -->
    <section id="sec-fin">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5 mb-3">
        5. REPOUSSE FINALE & SCORE D’ÉQUIPE
      </h2>
      <ul class="list-disc list-inside text-sm space-y-1.5 mb-3">
        <li>
          Sur chaque parcelle non rasée conservant au moins une Souche, <strong>retournez 1 Souche sur sa face Arbre debout</strong> <em>(aucune parcelle ne peut jamais dépasser sa dotation initiale d'Arbres ; les Routes Forestières restent définitivement rasées)</em>.
        </li>
        ${hasR6C ? `<li class="dyn-span"><strong>Effet actif (R6 Profil C · La Terra Preta) :</strong> Si R6 est sur la Piste des Tactiques lors de la Repousse, retournez jusqu'à <strong>2 Souches en Arbres debout</strong> sur chaque parcelle non rasée des Humains et des Insectes (dans la limite de la dotation initiale) !</li>` : ''}
      </ul>
      <p class="text-sm font-bold text-forest-950">
        Comptez le nombre total d'Arbres debout sur tout le plateau (sur <span class="dyn-span">${totalArbres} Arbres initiaux</span>) : c'est le score final de votre équipe !
      </p>
    </section>
  `;
}

if (typeof window !== 'undefined') {
  window.REGLES_COEUR_SYNTHESE = REGLES_COEUR_SYNTHESE;
  window.renderDidacticRulebook = renderDidacticRulebook;
}