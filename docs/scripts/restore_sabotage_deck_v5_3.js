#!/usr/bin/env node
/**
 * scripts/restore_sabotage_deck_v5_3.js
 * Rétablit la mécanique pure de Sabotage par dilution permanente du paquet Machine
 * sur les 4 couches d'Amazonia Doc Studio (v5.3) + met à jour AMAZONIA_STUDIO_CONTEXT.md.
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const LIVRET_PATH = path.join(ROOT, 'data', 'livret_v5_3.js');
const JS_PATH = path.join(ROOT, 'data', 'amazonia_data_v5_3.js');
const CATALOG_JSON_PATH = path.join(ROOT, 'data', 'catalog_v5_3.json');
const SPEC_JSON_PATH = path.join(ROOT, 'data', 'spec_formelle_v5_3.json');

// ---------------------------------------------------------------------------
// 1. UTILITAIRES D'EXTRACTION / REMPLACEMENT ÉQUILIBRÉ DANS LES FICHIERS JS
// ---------------------------------------------------------------------------
function findBalancedSpan(src, varName, openCh, closeCh) {
  const re = new RegExp(`\\b(?:const|let|var)\\s+${varName}\\s*=\\s*\\${openCh}`);
  const m = re.exec(src);
  if (!m) throw new Error(`Variable ${varName} introuvable.`);
  const openIdx = m.index + m[0].length - 1;
  let depth = 0, inQuote = null;
  for (let i = openIdx; i < src.length; i++) {
    const ch = src[i];
    if (inQuote) {
      if (ch === '\\') { i++; continue; }
      if (ch === inQuote) inQuote = null;
      continue;
    }
    if (ch === '/' && src[i + 1] === '/') {
      const nl = src.indexOf('\n', i + 2);
      if (nl === -1) break;
      i = nl;
      continue;
    }
    if (ch === '/' && src[i + 1] === '*') {
      const ec = src.indexOf('*/', i + 2);
      if (ec === -1) break;
      i = ec + 1;
      continue;
    }
    if (ch === "'" || ch === '"' || ch === '`') inQuote = ch;
    else if (ch === openCh) depth++;
    else if (ch === closeCh && --depth === 0) return [openIdx, i + 1];
  }
  throw new Error(`Fermeture ${closeCh} introuvable pour ${varName}`);
}

function replaceExactOnce(src, needle, replacement, label) {
  if (src.includes(replacement) && !src.includes(needle)) {
    console.log(`  [SKIP] Déjà à jour : ${label}`);
    return src;
  }
  const idx = src.indexOf(needle);
  if (idx === -1) {
    throw new Error(`Ancre introuvable pour : ${label}\nAttendu : ${needle.slice(0, 120)}...`);
  }
  console.log(`  [OK]   ${label}`);
  return src.slice(0, idx) + replacement + src.slice(idx + needle.length);
}

// ---------------------------------------------------------------------------
// 2. PATCHS DES 5 TUILES CONCERNÉES (CHOIX VALIDÉS : G9_B = 1a, R4_B = 2b)
// ---------------------------------------------------------------------------
const SABOTAGE_TILE_PATCHES = {
  G9: {
    A: {
      fenetre: "OUVERTURE",
      primitive: "CREATION_ENTITE (SABOTAGE)",
      texte: "<strong>Face 1 :</strong> Ajoutez définitivement 1 carte Sabotage de la réserve au paquet Machine (mise de côté pour le remélange de 6.3 ; allume la case 3).<br><strong>Face 2 :</strong> Ajoutez définitivement 2 cartes Sabotage de la réserve au paquet Machine (allume la case 3).",
      temoin: "Dilue durablement le paquet Machine en réaction à n’importe quel Déclencheur (réserve de cartes Sabotage illimitée)."
    },
    B: {
      fenetre: "LOI 4.1 / LOI 3.2",
      primitive: "MOD_LOI_DU_COEUR (LOI_SABOTAGE_ACTIF_ET_REVELATION)",
      texte: "<strong>Face 1 (Loi 4.1) :</strong> Un binôme en Furtivité peut saboter sa parcelle cible même si une machine y est active ce tour-ci ou en <strong>Siège</strong>.<br><strong>Face 2 (Loi 4.1 & 3.2) :</strong> Un binôme en Furtivité peut saboter sa parcelle cible même si une machine y est active ce tour-ci ou en <strong>Siège</strong> ; de plus, en 3.2, chaque carte Sabotage révélée derrière un paravent allume la <strong>case 3. Sabotage</strong> et retire <strong>1 jeton Puissance rouge</strong> d’une machine sur les rayons R ou H.",
      temoin: "En Face 2, chaque panne tirée en 3.2 déclenche une cascade sur la case 3 (une seule activation max du Gardien câblé en 3) et affaiblit les machines sur R/H avant que la carte Sabotage ne soit remélangée en 6.3."
    }
  },
  G10: {
    C: {
      fenetre: "OUVERTURE (CASE 6)",
      primitive: "CREATION_ENTITE (SABOTAGE) avec coût",
      texte: "<em>(Câblage obligatoire sur 6. Insecte)</em> À l’ouverture, vous pouvez défausser 1 Insecte d’une parcelle Forêt pour ajouter définitivement 1 carte Sabotage de la réserve au paquet Machine (allume la case 3).",
      temoin: "En 4.2, l’Insecte produit par un Nid peut payer ce coût après le bloc indivisible du Nid pour diluer durablement le paquet Machine."
    }
  },
  R4: {
    B: {
      fenetre: "LOI 3.2",
      primitive: "MOD_LOI_DU_COEUR (LOI_SABOTAGE_REVELE_PROLIFERE)",
      texte: "<strong>Loi 3.2 :</strong> En 3.2, si au moins 1 Défenseur occupe une case Furtivité et qu’au moins 1 carte Sabotage est révélée à l’ouverture des paravents, ajoutez définitivement <strong>+1 nouvelle carte Sabotage</strong> de la réserve au paquet Machine (sans allumer la case 3).",
      temoin: "Amplifie boule de neige la dilution du paquet Machine (1 carte bonus max par tour) tant qu’une présence furtive accompagne la révélation d’une panne."
    }
  },
  M4: {
    A: {
      fenetre: "4.2 APRÈS PRODUCTION",
      primitive: "CREATION_ENTITE (SABOTAGE) avec coût",
      texte: "Après production en 4.2, vous pouvez défausser 1 Insecte de ce Nid pour ajouter définitivement 1 carte Sabotage de la réserve au paquet Machine (allume la case 3).",
      temoin: "Résolu dans le bloc indivisible du Nid : enrichit définitivement le paquet Machine, puis au balayage suivant les cases 3 et 6 sont examinées dans l’ordre 1 → 6."
    }
  }
};

// ---------------------------------------------------------------------------
// 3. MISE À JOUR DE data/livret_v5_3.js
// ---------------------------------------------------------------------------
function patchLivretJs() {
  console.log('=== 1. Mise à jour de data/livret_v5_3.js ===');
  let src = fs.readFileSync(LIVRET_PATH, 'utf8').replace(/\r\n/g, '\n');

  // 3.1. REGLES_COEUR_SYNTHESE
  const ctx = vm.createContext({ window: {} });
  vm.runInContext(src.split('function renderDidacticRulebook')[0] + '\n;globalThis.__RCS = REGLES_COEUR_SYNTHESE;', ctx);
  const rcs = ctx.__RCS;

  rcs.but_et_format = "Coopératif asymétrique à communication limitée (3 à 6 joueurs parmi M,R,O,H,E,I · max 8 tours). Objectif unique : maximiser le total d'Arbres debout après la Repousse Finale (plafonnée à la dotation initiale de chaque parcelle). Réserves de jetons et de cartes Sabotage illimitées.";
  rcs.principes_transverses.gouvernance_unitaire = "Chaque Tuile de Synergie (G, R, M) et piste de Migration est gouvernée exclusivement par le joueur de son Peuple d'origine (champ origine). Zéro vote de groupe. Les cartes Sabotage sont toutes identiques et sans décision de jeu (dilution automatique du paquet Machine).";
  rcs.sequence_tour_6_etapes["1_siege_et_plan"] = "Machines sur la dernière parcelle non rasée = Siège irréversible (autonome même si T4 éjectée, 0 Apprentissage). Distribution 1 carte/joueur depuis le paquet Machine (incluant les cartes Sabotage déjà intégrées ; si moins de cartes que de joueurs : sens horaire depuis le Peuple ayant le plus d'Arbres debout ; joueur sans carte lance quand même 2D6). Sous paravent : double aux dés peut ouvrir un Rêve en 3.2. Si carte Sabotage tirée : aucune machine activée par cette carte (action du Contremaître perdue, aucune Tactique choisie). Si carte Machine tirée : hors double, M = min(D1,D2) désigne le rang sur la Piste Tactiques (modifié par Lois ; si rang M = Rêve, activation machine annulée).";
  rcs.sequence_tour_6_etapes["3_2_revelation_et_sabotages"] = "Ouverture simultanée des paravents ; fin du silence. Toute carte Sabotage révélée est simplement mise de côté (action du Contremaître perdue ce tour) pour être remélangée dans le paquet en 6.3. Double aux dés ou dé M sur un Rêve : ouvre le Rêve et l'avance r -> r-1 (max 1 ouverture/Rêve/tour en standard ; machine sur Rêve annulée).";
  rcs.sequence_tour_6_etapes["4_1_furtivite"] = "Par binôme complet sur une case Furtivité (2 Défenseurs sur la même rive, ou 1 Déf + 1 Insecte défaussé) : 1 seule action gouvernée par le joueur de cette rive sur la parcelle Forêt non rasée de son bord — Piège si 0 machine présente (Déclencheur 2) OU Sabotage si >=1 machine présente et aucune active ce tour (Siège = active) : prenez 1 carte Sabotage de la réserve et mettez-la de côté pour l'intégrer définitivement au paquet Machine en 6.3 (allume Déclencheur 3).";
  rcs.sequence_tour_6_etapes["5_attaques_sans_verrouillage"] = "Zéro dette d'Insectes et zéro verrouillage des parcelles (seul un Piège déjà déclenché ce tour ne peut plus payer de coût volontaire). Ordre : Tactiques 1..6 puis Sièges (Abatteuse avant Bulldozer sur un même rayon ; libre entre rayons distincts). Chaque machine résolue d'un seul tenant : cibles lues depuis sa position réelle à l'instant de l'attaque -> chaîne parades [1° Jaguar (2 bleus) -> 2° Harpie -> 3° Piège si Déf totale >= 1 -> 4° Parade classique avec défausse immédiate des Insectes manquants] -> dégâts (Abatteuse 2 Arbres ; Bulldozer 1 Arbre + toutes Souches, si 0/0 Route Forestière et repli machines vers bordure par défaut) -> avancée T3/T6 -> +1 Rouge T4/T5/T6 -> Siège si dernière parcelle. Contact Machine-Nid (tout mouvement entrant) : Nid renvoyé en lisière reconstructible + tous Insectes de la parcelle défaussés. Fin 5.3 : effets fin d'attaques, retrait Pièges déclenchés, puis test Fin de Partie (Tour 8, Rêve rang 1, ou marqueurs Gardiens >= seuil fixe -> Repousse Finale directe sans Étape 6).";
  rcs.sequence_tour_6_etapes["6_apprentissage"] = "Machines activées par carte uniquement (Siège = 0) : +1/parcelle réellement endommagée (>=1 Arbre coupé ou Souche retirée) +1/Rouge acquis -1/Bleu présent (plancher 0/machine). Retraits tuiles volontaires AVANT Insectes Bug (Bug économisé si déjà 0). Tactique strictement seule en tête avec >=1 jeton échange à gauche (si Écho des Voix Célestes amène son Rêve en case 1 -> Repousse Finale fin de tour). Remise à zéro de 100 % des jetons Apprentissage dans tous les cas, raz marqueurs Gardiens, retour Défenseurs, et remélange du paquet Machine (hors Siège) avec TOUTES les cartes Sabotage (révélées ce tour + nouvellement acquises).";

  const [rcsStart, rcsEnd] = findBalancedSpan(src, 'REGLES_COEUR_SYNTHESE', '{', '}');
  src = src.slice(0, rcsStart) + JSON.stringify(rcs, null, 2) + src.slice(rcsEnd);

  // 3.2. Remplacements ciblés dans renderDidacticRulebook()
  src = src.replace("  const hasHumains = state.peuplesCercle.includes('H');\n", "");

  src = replaceExactOnce(
    src,
    `Une fois les paravents ouverts, chaque Tuile de Synergie et piste de Migration est gouvernée par le seul joueur de son <strong>Peuple d'origine</strong> ; les cartes <strong>Sabotage</strong> visibles sont gouvernées par <span class="dyn-span">\${hasHumains ? 'le joueur des <strong>Humains</strong>' : 'le joueur qui vient d’acquérir la carte (les Humains étant absents de cette table)'}</span>.`,
    `Une fois les paravents ouverts, chaque Tuile de Synergie et piste de Migration est gouvernée exclusivement par le joueur de son <strong>Peuple d'origine</strong> (zéro vote de groupe).`,
    'Section 1 : retrait de la gouvernance Humains sur les cartes Sabotage'
  );

  src = replaceExactOnce(
    src,
    `<strong>Paquets & Piste des Tactiques :</strong> formez d'une part le paquet mélangé des <span class="dyn-span">\${2 * n} cartes Machine</span>, et d'autre part la pioche séparée des cartes <strong>Sabotage</strong> (avec sa défausse, remélangée dès que la pioche s'épuise).`,
    `<strong>Paquet des Machines & Réserve de Sabotage :</strong> formez le paquet mélangé initial des <span class="dyn-span">\${2 * n} cartes Machine</span>, et placez à proximité la réserve de cartes <strong>Sabotage</strong> (toutes identiques, réserve illimitée : chaque Sabotage réussi ajoutera définitivement 1 carte Sabotage dans le paquet Machine pour lui faire perdre des activations).`,
    'Section 2 : mise en place du paquet Machine et de la réserve de cartes Sabotage identiques'
  );

  src = replaceExactOnce(
    src,
    `          <li>
            <strong>Distribution secrète :</strong> Distribuez 1 carte Machine face cachée à chaque joueur depuis le paquet restant, puis écartez le surplus sans le regarder. <em>(S'il reste moins de cartes que de joueurs, servez dans le sens horaire à partir du Peuple ayant le plus d'Arbres debout ; un joueur sans carte lance quand même ses 2 dés pour tenter un double Rêve).</em>
          </li>
          <li>
            <strong>Lancer de 2D6 sous le mini-paravent (en silence complet) :</strong>
            <ul class="list-disc list-inside ml-5 mt-1 space-y-1 text-slate-700">
              <li><strong>Double aux dés :</strong> permettra en 3.2 d'ouvrir un Rêve présent sur la piste.</li>
              <li><strong>Lecture pour la carte Machine :</strong> hors double (ou pour votre machine), le plus petit dé <code>M = min(D1, D2)</code> désigne le rang sur la Piste des Tactiques (sauf Loi modifiant le dé retenu). Si ce rang contient un <strong>Rêve</strong>, l'activation de votre machine sera annulée en 3.2 !</li>
            </ul>
          </li>`,
    `          <li>
            <strong>Distribution secrète (Paquet Machine + Sabotages intégrés) :</strong> Distribuez 1 carte face cachée à chaque joueur depuis le paquet (qui contient les cartes Machine hors Siège ainsi que toutes les cartes Sabotage déjà ajoutées lors des tours précédents), puis écartez le surplus sans le consulter. <em>(S'il reste moins de cartes que de joueurs, servez dans le sens horaire à partir du Peuple ayant le plus d'Arbres debout ; un joueur sans carte lance quand même ses 2 dés pour tenter un double Rêve).</em>
          </li>
          <li>
            <strong>Lancer de 2D6 sous le mini-paravent (en silence complet) :</strong>
            <ul class="list-disc list-inside ml-5 mt-1 space-y-1 text-slate-700">
              <li><strong>Double aux dés :</strong> permettra en 3.2 d'ouvrir un Rêve présent sur la piste (même si vous avez pioché une carte Sabotage ou reçu aucune carte).</li>
              <li><strong>Si vous avez pioché une carte Sabotage :</strong> bonne nouvelle secrète, <strong>cette action du Contremaître est perdue</strong> (aucune machine n'est activée par cette carte ; ne sélectionnez aucune Tactique sous votre paravent).</li>
              <li><strong>Si vous avez pioché une carte Machine :</strong> le plus petit dé <code>M = min(D1, D2)</code> désigne le rang sur la Piste des Tactiques (sauf Loi modifiant le dé retenu). Si ce rang contient un <strong>Rêve</strong>, l'activation de votre machine sera annulée en 3.2 !</li>
            </ul>
          </li>`,
    'Étape 1.2 & 1.3 : tirage secret d’une carte Sabotage = action perdue du Contremaître'
  );

  src = replaceExactOnce(
    src,
    `          <li>
            <strong>3.2. Ouverture simultanée des paravents, Rêves & Fenêtre Sabotage :</strong>
            <ul class="list-disc list-inside ml-5 mt-1 text-slate-700 space-y-1">
              <li><strong>Fin du silence & Cartes Sabotage :</strong> dès maintenant et <strong>jusqu'au lancement de la 1<sup>re</sup> attaque en Étape 5</strong>, les cartes Sabotage visibles en réserve peuvent être jouées librement par leur gouverneur.</li>
              <li><strong>Rêves (double aux dés ou dé M sur un Rêve) :</strong> si le dé <code>M</code> d'une carte Machine désigne un Rêve, <strong>l'activation de cette machine est annulée</strong> pour le tour. <span class="dyn-span">\${c.Regle_Ouverture_Reve_Multiple === 'UNIQUE_PAR_TOUR' ? 'Chaque Rêve sollicité (par un double ou par au moins un dé M) peut s’ouvrir et avancer d’1 cran vers la gauche (<code>r → r−1</code>) <strong>au maximum 1 fois ce tour-ci</strong>.' : 'Chaque sollicitation ouvre le Rêve désigné et le fait avancer d’1 cran vers la gauche (<strong>mode cumulatif</strong>).'}</span></li>
            </ul>
          </li>`,
    `          <li>
            <strong>3.2. Ouverture simultanée des paravents, Pannes de Sabotage & Rêves :</strong>
            <ul class="list-disc list-inside ml-5 mt-1 text-slate-700 space-y-1">
              <li><strong>Fin du silence & Cartes Sabotage révélées :</strong> toute carte <strong>Sabotage</strong> révélée derrière un paravent fait simplement perdre une activation au Contremaître ce tour-ci ! Mettez-la de côté près du paquet Machine : elle y sera remélangée en 6.3.</li>
              <li><strong>Rêves (double aux dés ou dé M sur un Rêve) :</strong> si le dé <code>M</code> d'une carte Machine désigne un Rêve, <strong>l'activation de cette machine est annulée</strong> pour le tour. <span class="dyn-span">\${c.Regle_Ouverture_Reve_Multiple === 'UNIQUE_PAR_TOUR' ? 'Chaque Rêve sollicité (par un double ou par au moins un dé M) peut s’ouvrir et avancer d’1 cran vers la gauche (<code>r → r−1</code>) <strong>au maximum 1 fois ce tour-ci</strong>.' : 'Chaque sollicitation ouvre le Rêve désigné et le fait avancer d’1 cran vers la gauche (<strong>mode cumulatif</strong>).'}</span></li>
            </ul>
          </li>`,
    'Étape 3.2 : révélation d’une carte Sabotage mise de côté pour remélange'
  );

  src = replaceExactOnce(
    src,
    `              <li><strong>Saboter le chantier :</strong> s'il y a <strong>au moins 1 machine présente mais aucune active ce tour-ci</strong> (une machine en Siège est active), piochez 1 carte Sabotage face visible en réserve (allume <em>3. Sabotage</em> si une carte est effectivement piochée).</li>`,
    `              <li><strong>Saboter le chantier :</strong> s'il y a <strong>au moins 1 machine présente mais aucune active ce tour-ci</strong> (une machine en Siège est active), prenez <strong>1 carte Sabotage</strong> de la réserve et mettez-la de côté pour l'intégrer <strong>définitivement</strong> au paquet Machine en 6.3 (allume <em>3. Sabotage</em>).</li>`,
    'Étape 4.1 : Saboter = +1 carte Sabotage ajoutée définitivement au paquet Machine'
  );

  src = replaceExactOnce(
    src,
    `        <p class="text-xs text-slate-600 mb-2">
          <em>La fenêtre libre des cartes Sabotage se ferme au coup d'envoi de la 1<sup>re</sup> attaque — toutefois, toute carte Sabotage fraîchement piochée pendant les attaques peut être jouée sur-le-champ ! Il n'existe aucun verrouillage des parcelles ciblées : seul un Piège ayant déjà paré ce tour-ci ne peut plus payer de coût volontaire avant son retrait en 5.3.</em>
        </p>`,
    `        <p class="text-xs text-slate-600 mb-2">
          <em>Rappel : il n'existe aucune dette d'Insectes ni aucun verrouillage des parcelles ciblées — tant qu'un Insecte est sur le plateau, il est libre ; seul un Piège ayant déjà paré ce tour-ci ne peut plus payer de coût volontaire avant son retrait en 5.3.</em>
        </p>`,
    'Étape 5 : suppression de la fausse fenêtre de jeu des cartes Sabotage'
  );

  src = replaceExactOnce(
    src,
    `          <li>
            <strong>6.3. Ménage :</strong> Récupérez vos Défenseurs, retirez les marqueurs <em>« utilisé »</em> des Gardiens, et remélangez le paquet des cartes Machine (hors machines en Siège). Les cartes Sabotage non jouées restent visibles en réserve.
          </li>`,
    `          <li>
            <strong>6.3. Ménage & Dilution permanente :</strong> Récupérez vos Défenseurs, retirez les marqueurs <em>« utilisé »</em> des Gardiens, et formez le paquet du tour suivant en remélangeant toutes les cartes Machine (hors machines en Siège) <strong>avec toutes les cartes Sabotage</strong> (celles révélées ou écartées ce tour-ci + toutes les nouvelles cartes Sabotage acquises ce tour-ci).
          </li>`,
    'Étape 6.3 : remélange définitif de toutes les cartes Sabotage dans le paquet Machine'
  );

  new vm.Script(src, { filename: 'livret_v5_3.js' });
  fs.writeFileSync(LIVRET_PATH, src, 'utf8');
}

// ---------------------------------------------------------------------------
// 4. MISE À JOUR DE spec_formelle_v5_3.json, amazonia_data_v5_3.js & catalog_v5_3.json
// ---------------------------------------------------------------------------
function patchDataAndSpec() {
  console.log('\n=== 2. Mise à jour des données JS / JSON & Spec formelle ===');

  let jsSrc = fs.readFileSync(JS_PATH, 'utf8').replace(/\r\n/g, '\n');
  const ctx = vm.createContext({ window: {} });
  vm.runInContext(
    jsSrc + '\n;globalThis.__CAT = CATALOGUE_TUILES; globalThis.__CL = VERSION_CHANGELOG; globalThis.__SPEC = typeof SPEC_FORMELLE_V5_3 !== "undefined" ? SPEC_FORMELLE_V5_3 : null;',
    ctx
  );

  // 4.1. Patch des 5 tuiles dans CATALOGUE_TUILES
  for (const [tId, profMap] of Object.entries(SABOTAGE_TILE_PATCHES)) {
    for (const [letter, patch] of Object.entries(profMap)) {
      Object.assign(ctx.__CAT[tId].profils[letter], patch);
    }
  }
  console.log('  [OK]   5 profils Sabotage mis à jour (G9_A, G9_B, G10_C, R4_B, M4_A)');

  // 4.2. Mise à jour de VERSION_CHANGELOG[0] (v5.3)
  const v53 = ctx.__CL[0];
  v53.deltas[1].apres =
    "v5.3 : 4 emplacements par case Furtivité (2 jumeaux/rive, max 2 Défenseurs). Entrer sur la case " +
    "(toute face) tire l’autre pion sur le jumeau de son bord et oriente l’unique action du binôme ; " +
    "retourner de réflexion à définitif se fait strictement sur place. Silence tactique sous paravent fermé ; " +
    "chaque Tuile et piste de Migration est gouvernée par son seul Peuple d’origine. Sabotage pur : +1 carte Sabotage " +
    "identique ajoutée définitivement au paquet Machine (1 carte Sabotage tirée en Étape 1 = 1 activation machine perdue).";

  // 4.3. Mise à jour de SPEC_FORMELLE_V5_3
  const specObj = fs.existsSync(SPEC_JSON_PATH)
    ? JSON.parse(fs.readFileSync(SPEC_JSON_PATH, 'utf8'))
    : ctx.__SPEC;

  if (specObj) {
    specObj.architecture_reference.reserves_materiel = "illimitees (jetons et cartes Sabotage identiques)";
    specObj.etapes_tour[0].regles[1] =
      "Chaque joueur hors pénurie pioche secrètement 1 carte du paquet Machine (qui inclut toutes les cartes Sabotage ajoutées définitivement lors des tours précédents). Une carte Sabotage tirée n’active aucune machine (action du Contremaître perdue). S’il reste moins de cartes que de joueurs, distribution dans le sens horaire à partir du peuple ayant le plus d’Arbres debout ; tout joueur (avec Sabotage ou sans carte) lance quand même ses 2 dés pour tenter un double Rêve.";
    specObj.etapes_tour[1].regles[0] =
      "Ouverture simultanée des paravents et fin du silence tactique. Toute carte Sabotage révélée n’a aucun autre effet que d’avoir fait perdre une activation au Contremaître : elle est mise de côté pour être remélangée dans le paquet Machine en fin de tour.";
    specObj.etapes_tour[4].regles.shift(); // Retire l'ancienne règle de fenêtre de jeu des cartes Sabotage en début d'Étape 5
    specObj.etapes_tour[5].regles[4] =
      "Ménage systématique : remise en réserve de 100 % des jetons d’Apprentissage de toutes les tuiles dans tous les cas, retrait des marqueurs 'utilisé' des Gardiens, retour en main des Défenseurs, et remélange du paquet Machine (hors machines en Siège) avec toutes les cartes Sabotage (révélées/écartées ce tour + nouvellement acquises ce tour).";
    specObj.arbitrages_valides.A24 =
      "Cartes Sabotage (dilution permanente) : toutes identiques et sans effet propre (réserve illimitée). 1 Sabotage acquis ajoute définitivement 1 carte Sabotage au paquet Machine (allume 3. Sabotage) ; 1 carte Sabotage tirée à l’Étape 1 fait perdre 1 activation au Contremaître puis est remélangée en fin de tour.";

    fs.writeFileSync(SPEC_JSON_PATH, JSON.stringify(specObj, null, 2) + '\n', 'utf8');
    console.log('  [OK]   data/spec_formelle_v5_3.json synchronisé');
  }

  // 4.4. Réécriture propre dans data/amazonia_data_v5_3.js
  const [clStart, clEnd] = findBalancedSpan(jsSrc, 'VERSION_CHANGELOG', '[', ']');
  jsSrc = jsSrc.slice(0, clStart) + JSON.stringify(ctx.__CL, null, 2) + jsSrc.slice(clEnd);

  const [catStart, catEnd] = findBalancedSpan(jsSrc, 'CATALOGUE_TUILES', '{', '}');
  jsSrc = jsSrc.slice(0, catStart) + JSON.stringify(ctx.__CAT, null, 2) + jsSrc.slice(catEnd);

  if (specObj && jsSrc.includes('const SPEC_FORMELLE_V5_3 =')) {
    const [spStart, spEnd] = findBalancedSpan(jsSrc, 'SPEC_FORMELLE_V5_3', '{', '}');
    jsSrc = jsSrc.slice(0, spStart) + JSON.stringify(specObj, null, 2) + jsSrc.slice(spEnd);
  }

  new vm.Script(jsSrc, { filename: 'amazonia_data_v5_3.js' });
  fs.writeFileSync(JS_PATH, jsSrc, 'utf8');
  console.log('  [OK]   data/amazonia_data_v5_3.js mis à jour et validé par Node vm');

  // 4.5. Synchronisation de data/catalog_v5_3.json
  if (fs.existsSync(CATALOG_JSON_PATH)) {
    const catJson = JSON.parse(fs.readFileSync(CATALOG_JSON_PATH, 'utf8'));
    catJson.gouvernance_autorite =
      "Autorité unitaire par Peuple d’origine (tuiles de Synergie et pistes de Migration). Zéro vote de groupe. Cartes Sabotage identiques agissant par dilution permanente du paquet Machine.";
    if (specObj) catJson.spec_formelle_v5_3 = specObj;

    const syncTree = (node) => {
      if (Array.isArray(node)) return node.forEach(syncTree);
      if (node && typeof node === 'object') {
        for (const [k, v] of Object.entries(node)) {
          if (ctx.__CAT[k] && v && v.profils) {
            for (const [pL, pO] of Object.entries(ctx.__CAT[k].profils)) {
              if (v.profils[pL]) Object.assign(v.profils[pL], pO);
            }
          }
          if (v && typeof v === 'object') syncTree(v);
        }
      }
    };
    syncTree(catJson);
    fs.writeFileSync(CATALOG_JSON_PATH, JSON.stringify(catJson, null, 2) + '\n', 'utf8');
    console.log('  [OK]   data/catalog_v5_3.json synchronisé');
  }

  // 4.6. Contrôle d'absence de tout résidu de l'ancienne fausse règle Sabotage
  const checkStr = fs.readFileSync(LIVRET_PATH, 'utf8') + '\n' + fs.readFileSync(JS_PATH, 'utf8');
  const forbidden = [
    /Sabotage(?:s)?\s+visibles?\s+gouvern/i,
    /fenêtre\s+(?:libre\s+)?(?:des\s+cartes\s+)?Sabotage/i,
    /piochée\s+pendant\s+les\s+attaques\s+peut\s+être\s+jouée/i,
    /Sabotages?\s+visibles?\s+par\s+H\b/i
  ];
  for (const rx of forbidden) {
    const m = rx.exec(checkStr);
    if (m) throw new Error(`Résidu de l'ancienne mécanique Sabotage détecté : "${m[0]}"`);
  }
  console.log('\n[SUCCÈS] Sabotage par dilution permanente rétabli à 100 % sans aucun résidu !');
}

patchLivretJs();
patchDataAndSpec();