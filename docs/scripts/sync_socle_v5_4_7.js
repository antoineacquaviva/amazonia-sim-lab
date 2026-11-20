'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..', '..');
const DATA_DIR = path.join(ROOT, 'docs', 'data');

const SPEC_PATH = path.join(DATA_DIR, 'spec_formelle_v5_4.json');
const CATALOG_PATH = path.join(DATA_DIR, 'catalog_v5_4.json');
const AMAZONIA_JS_PATH = path.join(DATA_DIR, 'amazonia_data_v5_4.js');
const LIVRET_JS_PATH = path.join(DATA_DIR, 'livret_v5_4.js');

const NEW_CASCADES =
  "On résout toujours intégralement l'action ou la tuile en cours avant d'examiner la Piste des Gardiens (signal binaire allumé/éteint par case 1..6, sans cumul de cardinalité). Partition stricte des 6 déclencheurs (« 1 événement = au plus 1 déclencheur ») : en 3.2 (par carte révélée) 3. Sabotage > 6. Insecte (déviation Bug) > 5. Rêve (dé M sur rang Rêve, annulée ou non) ; en 4.1 Furtivité aucun déclencheur 2 ni 3 ; la production d'un Nid en 4.2 n'allume jamais 6. Insecte ; en 5.1/5.2 (par frappe bloquée) 2. Piégeage (Piège armé) > 6. Insecte (Parade classique avec dépense >= 1 Insecte) > 1. Parade (Défenseurs seuls). Case 4. Gardien verrouillée sur DISTINCT_OPEN_1 (anti-boucle conservé : 1re ouverture du tour de chaque autre Gardien distinct). Zéro marqueur 'utilisé' : plafond uniforme UNIFORM_MAX_2 (max 2 Défenseurs par Gardien en 2.2). Balayage à plat de 1 à 6.";

const NEW_A14 =
  "Éveil de la Forêt 100 % Piste des Gardiens (v5.4.7) : actif uniquement si au moins 1 Peuple Animal Sauvage (M, R ou O) est autour de la table, aux Tours 1..7 (priorité absolue à Tour 8). En 5.3, la Forêt s'éveille si les N Défenseurs de la table ont tous été engagés en 2.2 sur la Piste des Gardiens et qu'aucun pari n'est perdu (0 Défenseur restant sur la Piste des Gardiens). Un Gardien sauvé par Bouclier de lisière (SLOT_COLONISATION_GARDIENS=B) reste en piste mais son pari reste PERDU (ne compte pas pour l'Éveil).";

const NEW_A22 =
  "Pari d'activation sur les Gardiens & Partition stricte des 6 déclencheurs (v5.4.7) : actif si >= 1 Peuple Animal Sauvage (M/R/O) est à la table. Plafond uniforme UNIFORM_MAX_2 (max 2 Défenseurs par Gardien construit cases 1..6 ; 0 = inactif). Partition stricte (« 1 événement = au plus 1 déclencheur ») : 3.2 (Sabotage > Insecte Bug > Rêve) ; 4.1 sans déclencheur 2/3 ; la production d'un Nid en 4.2 n'allume jamais 6. Insecte ; 5.1/5.2 (Piégeage > Insecte Parade >=1 Insecte > Parade Défenseurs seuls) ; 4. Gardien verrouillée sur DISTINCT_OPEN_1 (anti-boucle conservé : 1re ouverture du tour de chaque autre Gardien distinct). En 5.3 : 0 Défenseur restant -> pari gagné (reste en piste, passe Face 2 en Mode 4 si double-face) ; >= 1 Défenseur restant -> pari perdu (retour en lisière Face 1, sauf Bouclier de lisière SLOT_COLONISATION_GARDIENS=B qui défausse 1 Insecte de la case pour garder la tuile sur sa face actuelle, le pari restant PERDU).";

const NEW_ETAPE4_NIDS =
  "4.2 Production des Nids : chaque Nid actif est résolu comme un bloc indivisible : (1) création de 1 ou 2 Insectes selon le nombre d'Insectes physiquement présents sur sa parcelle à cet instant précis (la production d'un Nid n'allume jamais 6. Insecte), puis (2) pouvoir 'après production' du Nid, puis seulement (3) balayage 1..6 des Gardiens. Une production hors phase (Le Miel des Ancêtres) ne crée que les jetons Insecte sans déclencher le pouvoir propre du Nid.";

const NEW_VERIF_FIN =
  "Vérification unique à la fin des attaques (5.3, après résolution des paris Gardiens et Bouclier de lisière éventuel, passage direct à la Repousse Finale). Priorité absolue au Tour 8 (CAUSE_TOUR_8). Aux Tours 1..7 : Sommeil du Contremaître (tous les Rêves en jeu en bloc continu cases 1..k de la Piste des Tactiques fixe T1..T6) ou Éveil de la Forêt 100 % Piste des Gardiens (v5.4.7, actif si >= 1 Peuple Animal Sauvage M/R/O : les N Défenseurs de la table engagés en 2.2 sur la Piste des Gardiens et 0 Défenseur restant en 5.3 ; un Gardien sauvé par Bouclier de lisière reste un pari perdu).";

function patchSpecObj(spec) {
  spec.schema_version = '5.4.7';
  spec.date_consolidation = '2026-11-20';
  if (spec.principes_transverses) {
    spec.principes_transverses.cascades_gardiens_a_plat = NEW_CASCADES;
  }
  spec.arbitrages_valides.A14 = NEW_A14;
  spec.arbitrages_valides.A22 = NEW_A22;
  for (const et of spec.etapes_tour || []) {
    if (et.numero === 4 && Array.isArray(et.regles)) {
      et.regles = et.regles.map((r) =>
        String(r).startsWith('4.2 ') ? NEW_ETAPE4_NIDS : r
      );
    }
  }
}

// 1. Patch spec_formelle_v5_4.json
const specObj = JSON.parse(fs.readFileSync(SPEC_PATH, 'utf8'));
patchSpecObj(specObj);
fs.writeFileSync(SPEC_PATH, JSON.stringify(specObj, null, 2) + '\n', 'utf8');

// 2. Patch catalog_v5_4.json (Cœur uniquement — sans toucher aux 100 profils archivés)
const catObj = JSON.parse(fs.readFileSync(CATALOG_PATH, 'utf8'));
catObj.verification_fin_de_partie = NEW_VERIF_FIN;
if (catObj.spec_formelle) {
  patchSpecObj(catObj.spec_formelle);
}
if (catObj.spec_formelle_v5_4) {
  patchSpecObj(catObj.spec_formelle_v5_4);
}
if (catObj.regles_coeur && catObj.regles_coeur.spec_formelle) {
  patchSpecObj(catObj.regles_coeur.spec_formelle);
}
fs.writeFileSync(CATALOG_PATH, JSON.stringify(catObj, null, 2) + '\n', 'utf8');

// 3. Patch amazonia_data_v5_4.js via Node vm + JSON.stringify
const rawJs = fs.readFileSync(AMAZONIA_JS_PATH, 'utf8');
const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(
  rawJs +
    '\n;window.__EXPORT__ = { PEUPLES, MATRICE_PAIRES, TOPOLOGIES_PISTE_SPEC, CHASSIS_AXES_SPEC, CATALOGUE_TUILES, VERSION_CHANGELOG, SPEC_FORMELLE_V5_4 };',
  sandbox
);
const exp = sandbox.window.__EXPORT__;
patchSpecObj(exp.SPEC_FORMELLE_V5_4);

const v547Entry = {
  version: 'v5.4.7',
  date: 'Version en vigueur (2026-11-20)',
  titre: 'Finalisation du socle : 6. Insecte strict (sans 4.2 Nids) & 4. Gardien verrouillé sur DISTINCT_OPEN_1',
  resume:
    'Correction des deux biais détectés sur calibration_declencheurs_v5_4 : la production d’un Nid en 4.2 n’allume plus jamais 6. Insecte (partition stricte exclusivement en 3.2 déviation Bug ou 5.1 Parade classique avec dépense >= 1 Insecte), verrouillage définitif de 4. Gardien sur DISTINCT_OPEN_1 (suppression de DISTINCT_WON_2), et recalibrage de B2 (valorisation réaliste du Sabotage en 4.1 et arbitrage Migration 4.3 forêt / Bug / Bouclier de lisière).',
  deltas: [
    {
      domaine: 'Déclencheur 6. Insecte (partition stricte sans 4.2 Nids)',
      avant:
        'v5.4.6 : La production de jetons Insecte par un Nid en 4.2 allumait aussi 6. Insecte (~92–100 % des tours).',
      apres:
        'v5.4.7 : La production d’un Nid en 4.2 n’allume jamais 6. Insecte. 6. Insecte s’allume exclusivement en 3.2 (déviation Bug prioritaire sur 5. Rêve) ou en 5.1 (Parade classique défaussant >= 1 Insecte, prioritaire sur 1. Parade).'
    },
    {
      domaine: 'Case 4. Gardien verrouillée sur DISTINCT_OPEN_1',
      avant:
        'v5.4.6 : Duel expérimental DISTINCT_OPEN_1 vs DISTINCT_WON_2.',
      apres:
        'v5.4.7 : Verrouillage sur DISTINCT_OPEN_1 (1re ouverture du tour de chaque autre Gardien distinct, anti-boucle conservé) et suppression de DISTINCT_WON_2.'
    }
  ]
};
exp.VERSION_CHANGELOG = [
  v547Entry,
  ...exp.VERSION_CHANGELOG.filter((entry) => entry.version !== 'v5.4.7')
];

const header = `// =========================================================================\n// data/amazonia_data_v5_4.js — Données canoniques Amazonia v5.4.7 (6 profils · 192 châssis · Partition stricte 6 déclencheurs · 4. Gardien DISTINCT_OPEN_1 · Bouclier de lisière · Éveil 100 % Gardiens · Rêves CLEAR_RANK_ONLY)\n// =========================================================================\n`;
const rebuiltJs =
  header +
  `const PEUPLES = ${JSON.stringify(exp.PEUPLES, null, 2)};\n\n` +
  `const MATRICE_PAIRES = ${JSON.stringify(exp.MATRICE_PAIRES, null, 2)};\n\n` +
  `const TOPOLOGIES_PISTE_SPEC = ${JSON.stringify(exp.TOPOLOGIES_PISTE_SPEC, null, 2)};\n\n` +
  `const CHASSIS_AXES_SPEC = ${JSON.stringify(exp.CHASSIS_AXES_SPEC, null, 2)};\n\n` +
  `const CATALOGUE_TUILES = ${JSON.stringify(exp.CATALOGUE_TUILES, null, 2)};\n\n` +
  `const VERSION_CHANGELOG = ${JSON.stringify(exp.VERSION_CHANGELOG, null, 2)};\n\n` +
  `const SPEC_FORMELLE_V5_4 = ${JSON.stringify(exp.SPEC_FORMELLE_V5_4, null, 2)};\n`;

new vm.Script(rebuiltJs);
fs.writeFileSync(AMAZONIA_JS_PATH, rebuiltJs, 'utf8');

// 4. Patch livret_v5_4.js (UTF-8 sans BOM, validation new vm.Script)
let livretJs = fs.readFileSync(LIVRET_JS_PATH, 'utf8');

const livretReplacements = [
  [
    `"cascades_gardiens": "Finir intégralement l'action ou le Nid en cours avant d'examiner la Piste des Gardiens. Partition stricte des 6 déclencheurs (1 événement = au plus 1 déclencheur) : 3.2 (3. Sabotage > 6. Insecte Bug > 5. Rêve) ; 4.1 sans déclencheur 2/3 ; 4.2 Nids (6. Insecte) ; 5.1/5.2 (2. Piégeage > 6. Insecte Parade >=1 Insecte > 1. Parade Défenseurs seuls) ; 4. Gardien (anti-boucle conservé : DISTINCT_OPEN_1 ou DISTINCT_WON_2). Plafond uniforme UNIFORM_MAX_2 (max 2 Défenseurs par Gardien en 2.2). Balayage à plat de 1 à 6."`,
    `"cascades_gardiens": "Finir intégralement l'action ou le Nid en cours avant d'examiner la Piste des Gardiens. Partition stricte des 6 déclencheurs (1 événement = au plus 1 déclencheur) : 3.2 (3. Sabotage > 6. Insecte Bug > 5. Rêve) ; 4.1 sans déclencheur 2/3 ; la production d'un Nid en 4.2 n'allume jamais 6. Insecte ; 5.1/5.2 (2. Piégeage > 6. Insecte Parade >=1 Insecte > 1. Parade Défenseurs seuls) ; 4. Gardien verrouillée sur DISTINCT_OPEN_1 (anti-boucle conservé). Plafond uniforme UNIFORM_MAX_2 (max 2 Défenseurs par Gardien en 2.2). Balayage à plat de 1 à 6."`
  ],
  [
    `<div><strong>Version :</strong> v5.4.6 (Partition stricte 6 déclencheurs Gardiens &amp; Bouclier de lisière)</div>`,
    `<div><strong>Version :</strong> v5.4.7 (Socle finalisé : 6. Insecte strict sans 4.2 Nids &amp; 4. Gardien DISTINCT_OPEN_1)</div>`
  ],
  [
    `<strong>4.2. Production des Nids (bloc indivisible) :</strong> Chaque Nid portant au moins 1 Défenseur est résolu <strong>d'un seul tenant</strong> avant d'examiner les Gardiens : (1) posez <strong>+1 Insecte</strong> (si 0 ou 1 Insecte est présent sur la parcelle <em>à cet instant précis</em>) ou <strong>+2 Insectes</strong> (s'il y en a déjà ≥ 2 <em>à cet instant</em>), puis (2) résolvez immédiatement le pouvoir propre du Nid, et seulement ensuite (3) balayez les Gardiens de 1 à 6 (<em>6. Insecte</em>). <em>(Une production hors phase comme Le Miel des Ancêtres ne crée que les jetons Insecte).</em>`,
    `<strong>4.2. Production des Nids (bloc indivisible) :</strong> Chaque Nid portant au moins 1 Défenseur est résolu <strong>d'un seul tenant</strong> avant d'examiner les Gardiens : (1) posez <strong>+1 Insecte</strong> (si 0 ou 1 Insecte est présent sur la parcelle <em>à cet instant précis</em>) ou <strong>+2 Insectes</strong> (s'il y en a déjà ≥ 2 <em>à cet instant</em> ; cette production n'allume jamais <em>6. Insecte</em>), puis (2) résolvez immédiatement le pouvoir propre du Nid, et seulement ensuite (3) balayez les Gardiens de 1 à 6. <em>(Une production hors phase comme Le Miel des Ancêtres ne crée que les jetons Insecte).</em>`
  ],
  [
    `<strong>Pari par Défenseur (UNIFORM_MAX_2) &amp; Partition stricte 1 → 6 :</strong> terminez toujours l'effet en cours, puis parcourez les cases allumées de <strong>1 à 6</strong>. Chaque Gardien construit (cases 1..6) peut recevoir au maximum <strong>2 Défenseurs</strong> en 2.2. Chaque déclenchement consomme <strong>1 Défenseur</strong> et ouvre le Gardien. Case <strong>4. Gardien</strong> (anti-boucle conservé) : <code>DISTINCT_OPEN_1</code> (1<sup>re</sup> ouverture du tour de chaque autre Gardien distinct) ou <code>DISTINCT_WON_2</code> (2<sup>e</sup> puis 3<sup>e</sup> autre Gardien distinct achevant son pari). En <strong>5.3</strong> : <code>0</code> Défenseur restant → pari gagné (reste en piste, Face 2 en Mode 4 si double-face) ; <code>≥ 1</code> Défenseur restant → pari perdu (<strong>Bouclier de lisière</strong> <code>SLOT_COLONISATION_GARDIENS=B</code> : défausser 1 Insecte de la case empêche le retour en lisière tout en gardant le pari PERDU ; sinon retour en lisière Face 1).`,
    `<strong>Pari par Défenseur (UNIFORM_MAX_2) &amp; Partition stricte 1 → 6 :</strong> terminez toujours l'effet en cours, puis parcourez les cases allumées de <strong>1 à 6</strong>. Chaque Gardien construit (cases 1..6) peut recevoir au maximum <strong>2 Défenseurs</strong> en 2.2. Chaque déclenchement consomme <strong>1 Défenseur</strong> et ouvre le Gardien. Case <strong>4. Gardien</strong> verrouillée sur <code>DISTINCT_OPEN_1</code> (anti-boucle conservé : 1<sup>re</sup> ouverture du tour de chaque autre Gardien distinct). En <strong>5.3</strong> : <code>0</code> Défenseur restant → pari gagné (reste en piste, Face 2 en Mode 4 si double-face) ; <code>≥ 1</code> Défenseur restant → pari perdu (<strong>Bouclier de lisière</strong> <code>SLOT_COLONISATION_GARDIENS=B</code> : défausser 1 Insecte de la case empêche le retour en lisière tout en gardant le pari PERDU ; sinon retour en lisière Face 1).`
  ]
];

for (const [oldStr, newStr] of livretReplacements) {
  if (!livretJs.includes(oldStr)) {
    throw new Error(`Pattern introuvable dans livret_v5_4.js : ${oldStr.slice(0, 90)}`);
  }
  livretJs = livretJs.replace(oldStr, newStr);
}

new vm.Script(livretJs);
fs.writeFileSync(LIVRET_JS_PATH, livretJs, 'utf8');
console.log('Synchronized 4 layers (spec_formelle, catalog, amazonia_data, livret) for v5.4.7 OK.');
