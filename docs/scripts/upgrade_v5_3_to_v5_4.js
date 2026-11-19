'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..', '..');
const DOCS_DATA = path.join(ROOT, 'docs', 'data');

function readUtf8(p) {
  return fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '');
}

function writeUtf8Lf(p, content) {
  const normalized = content.replace(/\r\n/g, '\n');
  fs.writeFileSync(p, normalized, { encoding: 'utf8' });
}

function validateJsSyntax(code, filename) {
  new vm.Script(code, { filename });
}

function replaceSiegeTerms(str) {
  if (typeof str !== 'string') return str;
  return str
    .replace(/Siège T4 irréversible/g, 'Ratissage irréversible')
    .replace(/Siège T4/g, 'Ratissage')
    .replace(/en <strong>Siège<\/strong>/g, 'en <strong>Ratissage</strong>')
    .replace(/en Siège/g, 'en Ratissage')
    .replace(/d’entrée en Siège/g, 'd’entrée en Ratissage')
    .replace(/l’entrée en Siège/g, 'l’entrée en Ratissage')
    .replace(/statut de Siège/g, 'mode Ratissage')
    .replace(/statut Siège/g, 'mode Ratissage')
    .replace(/un Siège/g, 'un Ratissage')
    .replace(/du Siège/g, 'du Ratissage')
    .replace(/hors Siège/g, 'hors Ratissage')
    .replace(/Siège = active/g, 'Ratissage = active')
    .replace(/Siège irréversible/g, 'Ratissage irréversible')
    .replace(/en Sièges/g, 'en Ratissage')
    .replace(/puis Sièges/g, 'puis Ratissages')
    .replace(/machines en Siège/g, 'machines en Ratissage')
    .replace(/Machines en Siège/g, 'Machines en Ratissage');
}

// ---------------------------------------------------------------------------
// 1. Charger les 4 sources v5.3
// ---------------------------------------------------------------------------
const specV53 = JSON.parse(readUtf8(path.join(DOCS_DATA, 'spec_formelle_v5_3.json')));
const catalogV53 = JSON.parse(readUtf8(path.join(DOCS_DATA, 'catalog_v5_3.json')));
const amazoniaJsSrc = readUtf8(path.join(DOCS_DATA, 'amazonia_data_v5_3.js'));
const livretJsSrc = readUtf8(path.join(DOCS_DATA, 'livret_v5_3.js'));

const ctx = {};
const loaded = vm.runInNewContext(
  amazoniaJsSrc +
    '\n;({ PEUPLES, MATRICE_PAIRES, CHASSIS_AXES_SPEC, CATALOGUE_TUILES, VERSION_CHANGELOG, SPEC_FORMELLE_V5_3 });',
  ctx
);

// ---------------------------------------------------------------------------
// 2. Construire spec_formelle_v5_4.json
// ---------------------------------------------------------------------------
const specV54 = JSON.parse(JSON.stringify(specV53));
specV54.schema_version = '5.4.0';
specV54.date_consolidation = '2026-11-19';
specV54.architecture_reference.topologies_validees = {
  P4_2233: [2, 2, 3, 3],
  P4_2223: [2, 2, 2, 3],
  P4_1223: [1, 2, 2, 3],
  P5_22233: [2, 2, 2, 3, 3],
  P5_22223: [2, 2, 2, 2, 3],
  P5_12223: [1, 2, 2, 2, 3],
};

// Mise à jour des étapes du tour
specV54.etapes_tour[0].nom = 'Ratissage, Distribution et Dés secrets (1.1–1.3)';
specV54.etapes_tour[0].regles[0] =
  '1.1 Machines en Ratissage : les pions machine sont double face (initialisés sur face normale). Dès qu’une machine se trouve sur la dernière parcelle non rasée de son rayon, elle est retournée définitivement sur sa face Ratissage (carte retirée du paquet Machine). En mode Ratissage : +1 en puissance directement applicable inscrit sur le pion (traité comme +1 rouge à tous égards, en conservant les éventuels jetons Puissance ajoutés précédemment) et application systématique de la tactique T1 Sur place (T1 inscrit sur le pion). Son attaque en fin d’Étape 5 est autonome même si la tuile T1 a été éjectée par un Rêve ; en 6.1, elle alimente la tuile T1 en jetons d’Apprentissage si et seulement si T1 est encore présente sur la piste.';

specV54.etapes_tour[3].regles[0] = replaceSiegeTerms(specV54.etapes_tour[3].regles[0]);

specV54.etapes_tour[4].regles[0] = replaceSiegeTerms(specV54.etapes_tour[4].regles[0]);
specV54.etapes_tour[4].regles[4] = replaceSiegeTerms(specV54.etapes_tour[4].regles[4]);
specV54.etapes_tour[4].regles[6] =
  'Vérification de fin de partie : fin du Tour 8, Sommeil du Contremaître (toutes les tuiles Rêves en jeu — 2 par peuple onirique présent à la table, soit 2 ou 4 ; inactif si 0 — occupent en bloc les premières positions à gauche de la Piste des Tactiques), ou seuil fixe de Réveil atteint sur la Piste des Gardiens (seuil calculé une fois pour toutes à la mise en place : inactif si moins de 3 Gardiens dans la partie, sinon min(nb_joueurs, total_gardiens_partie) avec minimum 3 et plafond 5 à 6 joueurs ; tout Gardien renvoyé en lisière perd son marqueur). Si atteint : saut de l’Apprentissage et passage direct à la Repousse Finale.';

specV54.etapes_tour[5].regles[0] =
  'Calcul par machine active ce tour-ci (activée par carte OU en Ratissage) pour sa Tactique (T1 pour un Ratissage ; sans effet si T1 a été éjectée de la piste) : +1 par parcelle réellement endommagée (>= 1 Arbre coupé ou >= 1 Souche retirée) +1 par jeton Puissance rouge acquis ce tour -1 par jeton bleu Surchauffe présent sur la machine (plancher 0 par machine).';
specV54.etapes_tour[5].regles[3] =
  'Avancement : la Tactique strictement seule en tête avec au moins 1 jeton échange sa place avec sa voisine de gauche (y compris un Rêve, qui recule d’un cran à droite ; immobile si déjà en case 1). En cas d’égalité avec L’Écho des Voix Célestes regroupant en bloc à gauche toutes les tuiles Rêves en jeu, la fin de partie se déclenche immédiatement à la fin de ce tour (Repousse Finale).';
specV54.etapes_tour[5].regles[4] = replaceSiegeTerms(specV54.etapes_tour[5].regles[4]);

specV54.arbitrages_valides.A09 = replaceSiegeTerms(specV54.arbitrages_valides.A09);
specV54.arbitrages_valides.A10 =
  'Autonomie et Apprentissage du Ratissage : pion double face retourné définitivement sur la dernière parcelle non rasée ; +1 puissance imprimée (traité comme +1 rouge à tous égards, jetons rouges antérieurs conservés) et application systématique de T1 Sur place ; attaque autonome même si T1 est éjectée ; en 6.1, alimente T1 en Apprentissage tant que T1 figure sur la Piste des Tactiques.';
specV54.arbitrages_valides.A15 =
  'Test de fin de partie : maintenu en fin d’attaques (saut Apprentissage) sur Tour 8, Réveil Gardiens ou Sommeil (toutes les tuiles Rêves en jeu regroupées en bloc à gauche de la Piste des Tactiques), avec déclenchement en fin d’Apprentissage si L’Écho des Voix Célestes complète ce bloc.';
specV54.arbitrages_valides.A25 = replaceSiegeTerms(specV54.arbitrages_valides.A25);

// ---------------------------------------------------------------------------
// 3. Construire CHASSIS_AXES_SPEC v5.4 (7 axes, 6 * 2^6 = 384 configurations)
// ---------------------------------------------------------------------------
const TOPOLOGIES_PISTE_SPEC = {
  P4_2233: { p_max: 4, dotation: [2, 2, 3, 3], somme: 10, label: 'P4_2233 : 4 parcelles [2,2,3,3] (10N Arbres · Standard)' },
  P4_2223: { p_max: 4, dotation: [2, 2, 2, 3], somme: 9, label: 'P4_2223 : 4 parcelles [2,2,2,3] (9N Arbres)' },
  P4_1223: { p_max: 4, dotation: [1, 2, 2, 3], somme: 8, label: 'P4_1223 : 4 parcelles [1,2,2,3] (8N Arbres)' },
  P5_22233: { p_max: 5, dotation: [2, 2, 2, 3, 3], somme: 12, label: 'P5_22233 : 5 parcelles [2,2,2,3,3] (12N Arbres)' },
  P5_22223: { p_max: 5, dotation: [2, 2, 2, 2, 3], somme: 11, label: 'P5_22223 : 5 parcelles [2,2,2,2,3] (11N Arbres)' },
  P5_12223: { p_max: 5, dotation: [1, 2, 2, 2, 3], somme: 10, label: 'P5_12223 : 5 parcelles [1,2,2,2,3] (10N Arbres)' },
};

const CHASSIS_AXES_SPEC_V54 = [
  {
    key: 'Profil_Piste',
    num: 1,
    label: '1. Profil de Piste & Dotation Seuil Imprimé',
    defaultVal: 'P4_2233',
    options: Object.entries(TOPOLOGIES_PISTE_SPEC).map(([val, meta]) => ({
      val,
      text: meta.label,
    })),
  },
  loaded.CHASSIS_AXES_SPEC[1],
  loaded.CHASSIS_AXES_SPEC[2],
  loaded.CHASSIS_AXES_SPEC[3],
  {
    key: 'Placement_Initial_Machines',
    num: 5,
    label: '5. Placement initial des Machines',
    defaultVal: 'MEME_PARCELLE_P1',
    options: [
      { val: 'MEME_PARCELLE_P1', text: 'Standard : Abatteuse et Bulldozer en p=1' },
      { val: 'BULLDOZER_P1_ABATTEUSE_P2', text: 'Échelonné : Bulldozer en p=1, Abatteuse en p=2' },
    ],
  },
  {
    key: 'Role_Abatteuse_Fin_De_Piste',
    num: 6,
    label: '6. Rôle de l’Abatteuse en Ratissage',
    defaultVal: 'STANDARD_COUPE_ARBRE',
    options: [
      { val: 'STANDARD_COUPE_ARBRE', text: 'Standard (Coupe uniquement les Arbres)' },
      { val: 'ARRACHE_1_SOUCHE_SI_SANS_ARBRE', text: 'Arrache 1 Souche s’il n’y a plus d’Arbre' },
    ],
  },
  loaded.CHASSIS_AXES_SPEC[6],
];

// ---------------------------------------------------------------------------
// 4. Mettre à jour CATALOGUE_TUILES (texte + temoin) pour Ratissage & Sommeil
// ---------------------------------------------------------------------------
const CATALOGUE_TUILES_V54 = JSON.parse(JSON.stringify(loaded.CATALOGUE_TUILES));
for (const [slotId, slotObj] of Object.entries(CATALOGUE_TUILES_V54)) {
  for (const [pk, prof] of Object.entries(slotObj.profils || {})) {
    if (prof.texte) prof.texte = replaceSiegeTerms(prof.texte);
    if (prof.temoin) prof.temoin = replaceSiegeTerms(prof.temoin);
  }
}

// Ajustements ciblés texte + temoin sur les tuiles directement concernées
CATALOGUE_TUILES_V54.R7.profils.B.texte =
  '<strong>Loi 5 (Endiguement du Ratissage) :</strong> Les machines en <strong>Ratissage</strong> sur les rayons E et M et leurs rayons voisins immédiats subissent -1 à leur Seuil de Parade (annulant le +1 imprimé de la face Ratissage).';
CATALOGUE_TUILES_V54.R7.profils.B.temoin =
  'En mode Ratissage sur E, M ou leurs voisins immédiats, le Seuil de Parade est réduit de -1 (compensant le +1 de puissance imprimé sur la face Ratissage).';
CATALOGUE_TUILES_V54.R7.profils.B.primitive = 'MOD_LOI_DU_COEUR (LOI_ENDIGUEMENT_RATISSAGE)';
CATALOGUE_TUILES_V54.R7.profils.B.tags = ['LOI_5', 'RATISSAGE'];

CATALOGUE_TUILES_V54.G12.profils.A.temoin =
  'Si l’échange regroupe ainsi en bloc à gauche toutes les tuiles Rêves en jeu (rangs 1..k), le Sommeil du Contremaître sera validé lors de la vérification de fin de partie en 5.3.';

CATALOGUE_TUILES_V54.R1.profils.B.temoin =
  'Accélère le regroupement des tuiles Rêves en tête de piste (rangs 1..k) pour déclencher le Sommeil du Contremaître.';

CATALOGUE_TUILES_V54.R9.profils.B.texte =
  '<strong>Loi 6.2 :</strong> En cas d’égalité en tête de l’Apprentissage à l’Étape 6.2 (y compris égalité générale à 0), c’est ce Rêve qui avance d’1 rang vers la gauche (r → r−1). S’il complète ainsi le bloc de toutes les tuiles Rêves en jeu en tête de piste (rangs 1..k), la fin de partie par Sommeil se déclenche immédiatement (Repousse Finale).';
CATALOGUE_TUILES_V54.R9.profils.B.temoin =
  'Si l’avancée de R9 sur égalité en 6.2 place en bloc toutes les tuiles Rêves en jeu aux premiers rangs à gauche, la fin de partie par Sommeil se déclenche immédiatement avant le ménage.';

CATALOGUE_TUILES_V54.R10.profils.B.temoin =
  'Convertit un Insecte de la roue en 1 rang d’avancée supplémentaire pour R10 vers le bloc de tête (rangs 1..k).';

// ---------------------------------------------------------------------------
// 5. VERSION_CHANGELOG : ajout v5.4 en tête
// ---------------------------------------------------------------------------
const VERSION_CHANGELOG_V54 = [
  {
    version: 'v5.4',
    date: '2026-11-19',
    titre: '6 Profils de Pistes, Placement Échelonné, Sommeil en Bloc & Mode Ratissage (384 configs)',
    resume:
      'Évolution majeure du cœur de jeu : 4 nouveaux profils de pistes à tester (2223, 1223, 22223, 12223), option de placement initial échelonné (Bulldozer p=1, Abatteuse p=2), victoire par Sommeil exigeant le regroupement en bloc à gauche de toutes les tuiles Rêves en jeu, et remplacement définitif du Siège T4 par le mode Ratissage (pion double face, +1 puissance imprimée, T1 Sur place, entrée définitive sur la dernière parcelle).',
    points: [
      'Profils de pistes (Axe 1) : 6 profils testables (P4_2233, P4_2223, P4_1223, P5_22233, P5_22223, P5_12223) ; suppression définitive de DEPASSEMENT_DERNIERE_PARCELLE -> 7 axes, 384 configurations.',
      'Placement initial des machines (Axe 5) : Standard (Abatteuse & Bulldozer en p=1) ou Échelonné (Bulldozer en p=1, Abatteuse en p=2).',
      'Victoire par Sommeil : toutes les tuiles Rêves en jeu (2 par peuple onirique à la table, soit 2 ou 4 ; inactif si 0) doivent occuper en bloc les premières positions à gauche de la Piste des Tactiques.',
      'Mode Ratissage (remplace Siège) : pion machine double face retourné définitivement sur la dernière parcelle non rasée ; +1 puissance imprimée (traité comme +1 rouge à tous égards, jetons rouges antérieurs conservés) et application systématique de T1 Sur place (alimente T1 en Apprentissage en 6.1).',
      'Cohérence catalogue : terminologie Ratissage harmonisée sur toutes les tuiles, R7:B (Endiguement du Ratissage) recentrée sur -1 Seuil, textes/témoins Sommeil alignés (G12:A, R1:B, R9:B, R10:B).',
    ],
  },
  ...loaded.VERSION_CHANGELOG,
];

// ---------------------------------------------------------------------------
// 6. Écrire docs/data/spec_formelle_v5_4.json et docs/data/catalog_v5_4.json
// ---------------------------------------------------------------------------
const catalogV54 = JSON.parse(JSON.stringify(catalogV53));
catalogV54.schema_version = '5.4.0';
catalogV54.date_consolidation = '2026-11-19';
catalogV54.spec_formelle = specV54;

writeUtf8Lf(path.join(DOCS_DATA, 'spec_formelle_v5_4.json'), JSON.stringify(specV54, null, 2) + '\n');
writeUtf8Lf(path.join(DOCS_DATA, 'catalog_v5_4.json'), JSON.stringify(catalogV54, null, 2) + '\n');

// ---------------------------------------------------------------------------
// 7. Écrire docs/data/amazonia_data_v5_4.js (sérialisé via JSON.stringify + validé vm.Script)
// ---------------------------------------------------------------------------
const amazoniaJsV54 =
  '// Amazonia : Dernier Rempart — Données Canoniques v5.4 (Source Unique)\n' +
  'const PEUPLES = ' + JSON.stringify(loaded.PEUPLES, null, 2) + ';\n\n' +
  'const MATRICE_PAIRES = ' + JSON.stringify(loaded.MATRICE_PAIRES, null, 2) + ';\n\n' +
  'const TOPOLOGIES_PISTE_SPEC = ' + JSON.stringify(TOPOLOGIES_PISTE_SPEC, null, 2) + ';\n\n' +
  'const CHASSIS_AXES_SPEC = ' + JSON.stringify(CHASSIS_AXES_SPEC_V54, null, 2) + ';\n\n' +
  'const CATALOGUE_TUILES = ' + JSON.stringify(CATALOGUE_TUILES_V54, null, 2) + ';\n\n' +
  'const VERSION_CHANGELOG = ' + JSON.stringify(VERSION_CHANGELOG_V54, null, 2) + ';\n\n' +
  'const SPEC_FORMELLE_V5_4 = ' + JSON.stringify(specV54, null, 2) + ';\n';

validateJsSyntax(amazoniaJsV54, 'amazonia_data_v5_4.js');
writeUtf8Lf(path.join(DOCS_DATA, 'amazonia_data_v5_4.js'), amazoniaJsV54);

// ---------------------------------------------------------------------------
// 8. Écrire docs/data/livret_v5_4.js (REGLES_COEUR_SYNTHESE + renderDidacticRulebook)
// ---------------------------------------------------------------------------
let livretV54 = livretJsSrc;
livretV54 = livretV54
  .replace(/v5\.3/g, 'v5.4')
  .replace(/5\.3/g, '5.4')
  .replace(/Config #\$\{configNum\} \/ 128/g, 'Config #${configNum} / 384')
  .replace(
    /const totalArbres = n \* \(c\.P_Max === 5 \? 12 : 10\);/g,
    'const topoSpec = TOPOLOGIES_PISTE_SPEC[c.Profil_Piste] || TOPOLOGIES_PISTE_SPEC.P4_2233;\n  const totalArbres = n * topoSpec.somme;\n  const pMax = topoSpec.p_max;'
  )
  .replace(
    /\$\{c\.P_Max === 5 \? 'P5_22233 \(5 parcelles : 2-2-2-3-3\)' : 'P4_2233 \(4 parcelles : 2-2-3-3\)'\}/g,
    '${c.Profil_Piste} (${pMax} parcelles : ${topoSpec.dotation.join("-")})'
  )
  .replace(/p=\$\{c\.P_Max\}/g, 'p=${pMax}')
  .replace(
    /\$\{c\.P_Max === 5 \? 'P5_22233 \[2, 2, 2, 3, 3\]' : 'P4_2233 \[2, 2, 3, 3\]'\}/g,
    '${c.Profil_Piste} [${topoSpec.dotation.join(", ")}]'
  )
  .replace(
    /ainsi qu'1 Abatteuse et 1 Bulldozer en p=1 sur chaque rayon\./g,
    "ainsi qu'1 Abatteuse et 1 Bulldozer sur chaque rayon (<span class=\"dyn-span\">${c.Placement_Initial_Machines === 'BULLDOZER_P1_ABATTEUSE_P2' ? 'Bulldozer en p=1, Abatteuse en p=2' : 'Abatteuse et Bulldozer en p=1'}</span>, face normale)."
  )
  .replace(
    /\[\$\{c\.P_Max === 5 \? '2,2,2,3,3' : '2,2,3,3'\}\]/g,
    '[${topoSpec.dotation.join(",")}]'
  )
  .replace(
    /gagne <strong>\+1 jeton Rouge<\/strong> si <code>T4\/T5\/T6<\/code> \(ou Siège\), et entre en <strong>Siège<\/strong> si elle occupe la <span class="dyn-span">\$\{c\.Declenchement_Fin_De_Piste === 'ARRIVEE_DERNIERE_PARCELLE' \? 'dernière parcelle non rasée' : 'case de dépassement'\}<\/span>\./g,
    'gagne <strong>+1 jeton Rouge</strong> si <code>T4/T5/T6</code>, et passe définitivement en mode <strong>Ratissage</strong> (pion retourné : +1 puissance imprimée et <code>T1</code> Sur place) dès qu’elle occupe la dernière parcelle non rasée.'
  )
  .replace(
    /selon le profil de Siège \(frappe sur place, modificateur <code>-1<\/code>, <code>\+1 Rouge<\/code>\), <strong>même si la tuile <code>T4<\/code> a été éjectée de la piste<\/strong> \(tant que <code>T4<\/code> est sur la piste, une machine en Siège lui rapporte normalement de l'Apprentissage en 6\.1\)\./g,
    "selon sa face Ratissage (<code>+1</code> puissance imprimée traitée comme +1 Rouge à tous égards, jetons rouges antérieurs conservés, tactique <code>T1</code> Sur place), <strong>même si la tuile <code>T1</code> a été éjectée de la piste</strong> (tant que <code>T1</code> est sur la piste, une machine en Ratissage lui rapporte normalement de l'Apprentissage en 6.1)."
  )
  .replace(/ <em>\(profil identique au Siège\)<\/em>/g, '')
  .replace(/"1_siege_et_plan":/g, '"1_ratissage_et_plan":')
  .replace(/-> Siège si dernière parcelle\./g, '-> Ratissage définitif si dernière parcelle (face Ratissage : +1 puissance imprimée + T1 Sur place).')
  .replace(/Tour 8, Rêve rang 1,/g, 'Tour 8, Sommeil (toutes les tuiles Rêves en jeu en bloc à gauche),');

livretV54 = replaceSiegeTerms(livretV54);
livretV54 = livretV54
  .replace(/un Rêve atteint le Rang 1/g, 'toutes les tuiles Rêves en jeu (2 par peuple onirique) occupent en bloc les premiers rangs à gauche')
  .replace(/Rêve en case 1/g, 'toutes les tuiles Rêves en jeu en bloc à gauche (rangs 1..k)')
  .replace(/Rêve au Rang 1/g, 'Sommeil en bloc (tous les Rêves en tête)')
  .replace(/tuile T4/g, 'tuile T1');

validateJsSyntax(livretV54, 'livret_v5_4.js');
writeUtf8Lf(path.join(DOCS_DATA, 'livret_v5_4.js'), livretV54);

console.log('OK: 4 couches v5.4 générées et validées par vm.Script().');
