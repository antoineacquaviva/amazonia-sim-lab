'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..', '..');
const DATA_DIR = path.join(ROOT, 'docs', 'data');

const SPEC_PATH = path.join(DATA_DIR, 'spec_formelle_v5_4.json');
const CATALOG_PATH = path.join(DATA_DIR, 'catalog_v5_4.json');
const AMAZONIA_JS_PATH = path.join(DATA_DIR, 'amazonia_data_v5_4.js');

const NEW_A14 =
  "Réveil de la Forêt (v5.4.1) : actif uniquement si au moins 1 Peuple Animal Sauvage (M, R ou O) est autour de la table. Éveil universel Face 1 -> Face 2 à l'ouverture d'un Gardien (y compris monofaces et Mode 2 neutre ; G14:C éligible sur Face 2 Rassasié). En 2.2 (2e Défenseur), les joueurs peuvent cibler un Gardien Face 2 (max 1 Gardien engagé/tour) : si le quota Q est atteint en choix définitif, le Gardien est retiré de la piste (pouvoir/Loi inactifs ce tour, case 1..6 libre dès 3.1) ; sinon les Défenseurs orphelins restent sans effet. En 5.3, déclenchement immédiat du Réveil si 0 dommage réel ce tour (aucun Arbre coupé ni Souche retirée) ; en cas d'échec, résolution du sort du Gardien en 6.3 (retour lisière Face 1 ou retrait définitif). Les marqueurs « utilisé » des cases 1..6 servent uniquement à l'ouverture unique/tour, aux cascades 1->6, à la Résonance 4 et aux Lois passives.";

const NEW_A15 =
  "Test de fin de partie : maintenu en fin d’attaques (5.3, saut Apprentissage) sur Tour 8, Réveil de la Forêt (Gardien Face 2 engagé au quota Q en 2.2 et 0 dommage réel subi ce tour) ou Sommeil du Contremaître (toutes les tuiles Rêves en jeu regroupées en bloc à gauche de la Piste des Tactiques), avec déclenchement en fin d’Apprentissage (6.2) si L’Écho des Voix Célestes complète ce bloc.";

const NEW_ETAPE5_FIN =
  "Vérification de fin de partie (5.3) : fin du Tour 8, Sommeil du Contremaître (toutes les tuiles Rêves en jeu — 2 par peuple onirique présent à la table, soit 2 ou 4 ; inactif si 0 — occupent en bloc les premières positions à gauche de la Piste des Tactiques), ou Réveil de la Forêt (actif si >= 1 Peuple Animal Sauvage M/R/O à la table : un Gardien Face 2 engagé au quota Q de 2es Défenseurs en fin de 2.2 et 0 dommage réel infligé par les machines ce tour — aucun Arbre coupé ni Souche retirée). Si atteint : saut de l’Apprentissage et passage direct à la Repousse Finale.";

const NEW_ETAPE6_MENAGE =
  "Ménage systématique : remise en réserve de 100 % des jetons d’Apprentissage de toutes les tuiles dans tous les cas, retrait des marqueurs 'utilisé' des Gardiens, retour en main des Défenseurs, résolution en 6.3 d'un éventuel Gardien engagé pour un Réveil échoué (retour en lisière Face 1 par défaut ou retrait définitif), et remélange du paquet Machine (hors machines en Ratissage) avec toutes les cartes Sabotage (révélées/écartées ce tour + nouvellement acquises ce tour).";

const NEW_VERIF_FIN =
  "Vérification unique à la fin des attaques (5.3, saut de l'Apprentissage et passage direct à la Repousse Finale), complétée par le déclenchement en fin d'Apprentissage si L'Écho des Voix Célestes complète le bloc de Rêves en tête de piste. Sommeil du Contremaître (v5.4) : tous les Rêves en jeu (2 × peuples oniriques : 2 ou 4 ; impossible à 0) doivent occuper en bloc toutes les premières positions à gauche de la Piste des Tactiques. Réveil de la Forêt (v5.4.1) : actif si >= 1 Peuple Animal Sauvage (M/R/O) ; un Gardien Face 2 engagé au quota Q de 2es Défenseurs en fin de 2.2 déclenche immédiatement le Réveil en 5.3 si 0 dommage réel n'a été subi durant le tour.";

const NEW_TEMOINS = {
  'G4:A':
    "Le renvoi en lisière libère la case Gardien pour une future construction ; le Gardien repasse Face 1 et perd son marqueur « utilisé ».",
  'R1:C':
    "Coût volontaire : ne déclenche pas un pouvoir de sacrifice et renvoie le Gardien en lisière Face 1 sans marqueur « utilisé ».",
  'M5:D':
    "Allume la case 6 en 5.3 juste avant la vérification de fin de partie (pouvant ainsi ouvrir un dernier Gardien et l'éveiller en Face 2 pour le tour suivant !)."
};

function patchSpecObj(spec) {
  spec.arbitrages_valides.A14 = NEW_A14;
  spec.arbitrages_valides.A15 = NEW_A15;
  for (const et of spec.etapes_tour || []) {
    if (et.numero === 5 && Array.isArray(et.regles)) {
      et.regles[et.regles.length - 1] = NEW_ETAPE5_FIN;
    } else if (et.numero === 6 && Array.isArray(et.regles)) {
      et.regles[et.regles.length - 1] = NEW_ETAPE6_MENAGE;
    }
  }
}

// 1. Patch spec_formelle_v5_4.json
const specObj = JSON.parse(fs.readFileSync(SPEC_PATH, 'utf8'));
patchSpecObj(specObj);
fs.writeFileSync(SPEC_PATH, JSON.stringify(specObj, null, 2) + '\n', 'utf8');

// 2. Patch catalog_v5_4.json
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
if (catObj.catalogue_tuiles) {
  for (const [key, val] of Object.entries(NEW_TEMOINS)) {
    const [slot, prof] = key.split(':');
    if (catObj.catalogue_tuiles[slot] && catObj.catalogue_tuiles[slot].profils[prof]) {
      catObj.catalogue_tuiles[slot].profils[prof].temoin = val;
    }
  }
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

for (const [key, val] of Object.entries(NEW_TEMOINS)) {
  const [slot, prof] = key.split(':');
  if (exp.CATALOGUE_TUILES[slot] && exp.CATALOGUE_TUILES[slot].profils[prof]) {
    exp.CATALOGUE_TUILES[slot].profils[prof].temoin = val;
  }
}
patchSpecObj(exp.SPEC_FORMELLE_V5_4);

// Replace or prepend v5.4.1 entry in VERSION_CHANGELOG with full schema (resume + domaine)
const v541Entry = {
  version: 'v5.4.1',
  date: 'Version en vigueur (2026-11-19)',
  titre: 'Réveil de la Forêt par engagement collectif sur Gardien Face 2 (purge du Seuil fixe)',
  resume:
    'Remplacement définitif du Seuil de Réveil fixe par le Réveil de la Forêt : actif si >= 1 Peuple Animal Sauvage (M/R/O), éveil universel Face 1 -> Face 2 à l’ouverture d’un Gardien, engagement collectif en 2.2 au quota Q sur 1 Gardien Face 2 (case libérée dès 3.1) et déclenchement en 5.3 si 0 dommage réel subi ce tour.',
  deltas: [
    {
      domaine: 'Réveil de la Forêt (Condition de victoire Gardiens)',
      avant:
        'v5.4 : Seuil de Réveil fixe calculé à la mise en place sur le nombre de marqueurs « utilisé » en fin de 5.3.',
      apres:
        'v5.4.1 : Actif uniquement si >= 1 Peuple Animal Sauvage (M/R/O) à la table. Éveil universel Face 1 -> Face 2 à l’ouverture d’un Gardien (G14:C éligible sur Face 2 Rassasié). En 2.2, engagement collectif au quota Q de 2es Défenseurs sur 1 Gardien Face 2 (retiré de la piste, case libre dès 3.1) ; déclenchement immédiat en 5.3 si 0 dommage réel ce tour, sinon sort du Gardien résolu en 6.3.'
    }
  ]
};
exp.VERSION_CHANGELOG = [
  v541Entry,
  ...exp.VERSION_CHANGELOG.filter((entry) => entry.version !== 'v5.4.1')
];

const header = `// =========================================================================\n// data/amazonia_data_v5_4.js — Données canoniques Amazonia v5.4.1 (6 profils · 384 châssis · Ratissage T1 · Sommeil en bloc · Réveil de la Forêt)\n// =========================================================================\n`;
const rebuiltJs =
  header +
  `const PEUPLES = ${JSON.stringify(exp.PEUPLES, null, 2)};\n\n` +
  `const MATRICE_PAIRES = ${JSON.stringify(exp.MATRICE_PAIRES, null, 2)};\n\n` +
  `const TOPOLOGIES_PISTE_SPEC = ${JSON.stringify(exp.TOPOLOGIES_PISTE_SPEC, null, 2)};\n\n` +
  `const CHASSIS_AXES_SPEC = ${JSON.stringify(exp.CHASSIS_AXES_SPEC, null, 2)};\n\n` +
  `const CATALOGUE_TUILES = ${JSON.stringify(exp.CATALOGUE_TUILES, null, 2)};\n\n` +
  `const VERSION_CHANGELOG = ${JSON.stringify(exp.VERSION_CHANGELOG, null, 2)};\n\n` +
  `const SPEC_FORMELLE_V5_4 = ${JSON.stringify(exp.SPEC_FORMELLE_V5_4, null, 2)};\n`;

// Syntax check via new vm.Script()
new vm.Script(rebuiltJs);
fs.writeFileSync(AMAZONIA_JS_PATH, rebuiltJs, 'utf8');
console.log('Synchronized spec_formelle_v5_4.json, catalog_v5_4.json, and amazonia_data_v5_4.js OK.');
