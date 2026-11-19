'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..', '..');
const DATA_DIR = path.join(ROOT, 'docs', 'data');

const SPEC_PATH = path.join(DATA_DIR, 'spec_formelle_v5_4.json');
const CATALOG_PATH = path.join(DATA_DIR, 'catalog_v5_4.json');
const AMAZONIA_JS_PATH = path.join(DATA_DIR, 'amazonia_data_v5_4.js');

const NEW_A10 =
  "Autonomie du Ratissage : pion double face retourné définitivement sur la dernière parcelle non rasée ; +1 puissance imprimée (traité comme +1 rouge à tous égards, jetons rouges antérieurs conservés) et application systématique de T1 Sur place sur la piste fixe.";

const NEW_A11 =
  "Piste des Tactiques fixe (T1..T6 imprimées en dur) et placement des Rêves (v5.4.2) : aucune tuile Tactique mobile ni éjection de Tactique. Un Rêve construit en 3.1 se pose par-dessus la case libre la plus à droite (6, puis 5, etc.). Les Insectes Bug restent sur leur numéro d'emplacement imprimé.";

const NEW_A15 =
  "Test de fin de partie : vérification unique en fin d’attaques (5.3, passage direct à la Repousse Finale) sur Tour 8, Réveil de la Forêt (Gardien Face 2 engagé au quota Q en 2.2 et 0 dommage réel subi ce tour) ou Sommeil du Contremaître (toutes les tuiles Rêves en jeu regroupées en bloc continu à gauche cases 1..k de la Piste des Tactiques).";

const NEW_A21 =
  "Activation et avancée des Rêves (v5.4.2) : en 2.2, un joueur peut poser son 2e Défenseur sur un Rêve déjà présent sur la piste (immobilisé jusqu'au ménage de fin de tour). En 3.2, selon le mode actif (Option A par défaut : 1 Défenseur annule 1 carte Machine sur ce rang M en priorisant la plus menaçante ; Option B : >=1 Défenseur annule tout le rang ; Option C : binôme >=2 Défenseurs annule tout le rang), toute machine non annulée exécute la Tactique T1..T6 imprimée sous la case. Dès qu'au moins 1 machine est annulée, le Rêve s'ouvre (max 1 ouverture/tour par défaut) et avance d'1 cran vers la gauche en sautant/poussant tout bloc contigu de Rêves vers la première case libre à sa gauche (plafonné au Rang 1).";

const NEW_A23 =
  "Apprentissage supprimé (v5.4.2) : plus aucun jeton Apprentissage ni déplacement des Tactiques en Étape 6 (piste T1..T6 imprimée en dur). SLOT_BUG_CERVEAU bascule par défaut sur le profil B (Déviation Synaptique ±1 rang en 3.2).";

const NEW_ETAPE1_RATISSAGE =
  "1.1 Machines en Ratissage : les pions machine sont double face (initialisés sur face normale). Dès qu’une machine se trouve sur la dernière parcelle non rasée de son rayon, elle est retournée définitivement sur sa face Ratissage (carte retirée du paquet Machine). En mode Ratissage : +1 en puissance directement applicable inscrit sur le pion (traité comme +1 rouge à tous égards, en conservant les éventuels jetons Puissance ajoutés précédemment) et application systématique de la tactique T1 Sur place (T1 inscrit sur le pion) en fin d’Étape 5.";

const NEW_ETAPE3_REVE =
  "3.1 Rêve : un Rêve construit se pose par-dessus la case libre la plus à droite de la piste fixe T1..T6 (case 6, puis case 5 si 6 est déjà occupée par un Rêve, etc.). Aucune Tactique n'est éjectée (les Insectes Bug restent sur leur numéro d'emplacement imprimé). Ce Rêve est immédiatement présent sur la piste pour l’étape 3.2.";

const NEW_ETAPE3_REVELATION =
  "3.2 Révélation simultanée (paravents ouverts) : résolution des déviations Bug (SLOT_BUG_CERVEAU profil B par défaut : défausser 1 Insecte posé sur la case M pour décaler le dé M de ±1 rang), puis résolution des rangs portant un Rêve selon les 2es Défenseurs posés dessus en 2.2 (Option A par défaut : 1 Défenseur annule 1 machine sur ce rang en priorisant la plus menaçante ; toute machine non annulée exécute la Tactique imprimée T1..T6 sous la case). Dès qu'au moins 1 machine est annulée, le Rêve s'ouvre et avance vers la première case libre à sa gauche (saut/poussée d'un éventuel bloc contigu de Rêves).";

const NEW_ETAPE5_FIN =
  "Vérification de fin de partie (5.3) : fin du Tour 8, Sommeil du Contremaître (toutes les tuiles Rêves en jeu — 2 par peuple onirique présent à la table, soit 2 ou 4 ; inactif si 0 — occupent en bloc continu les premières positions à gauche 1..k de la Piste des Tactiques), ou Réveil de la Forêt (actif si >= 1 Peuple Animal Sauvage M/R/O à la table : un Gardien Face 2 engagé au quota Q de 2es Défenseurs en fin de 2.2 et 0 dommage réel infligé par les machines ce tour — aucun Arbre coupé ni Souche retirée). Si atteint : passage direct à la Repousse Finale.";

const NEW_ETAPE6_NOM = "Ménage de fin de tour (6.2–6.3)";

const NEW_ETAPE6_REGLES = [
  "Ménage systématique (6.2) : piste des Tactiques T1..T6 fixe (aucun jeton ni déplacement de Tactique), retrait des marqueurs 'utilisé' des Gardiens, retour en main de tous les Défenseurs (y compris ceux engagés sur des Rêves ou Gardiens) et remise à zéro des modificateurs transitoires.",
  "Clôture du tour (6.3) : résolution d'un éventuel Gardien engagé pour un Réveil échoué (retour en lisière Face 1 par défaut ou retrait définitif), passage du pion Coordonnateur au siège suivant et remélange du paquet Machine (hors machines en Ratissage) avec toutes les cartes Sabotage (révélées/écartées ce tour + nouvellement acquises ce tour)."
];

const NEW_VERIF_FIN =
  "Vérification unique à la fin des attaques (5.3, passage direct à la Repousse Finale). Sommeil du Contremaître (v5.4.2) : tous les Rêves en jeu (2 × peuples oniriques : 2 ou 4 ; impossible à 0) doivent occuper en bloc continu toutes les premières positions à gauche (cases 1..k) de la Piste des Tactiques fixe T1..T6. Réveil de la Forêt (v5.4.1) : actif si >= 1 Peuple Animal Sauvage (M/R/O) ; un Gardien Face 2 engagé au quota Q de 2es Défenseurs en fin de 2.2 déclenche immédiatement le Réveil en 5.3 si 0 dommage réel n'a été subi durant le tour.";

function patchSpecObj(spec) {
  spec.schema_version = '5.4.2';
  spec.arbitrages_valides.A10 = NEW_A10;
  spec.arbitrages_valides.A11 = NEW_A11;
  spec.arbitrages_valides.A15 = NEW_A15;
  spec.arbitrages_valides.A21 = NEW_A21;
  spec.arbitrages_valides.A23 = NEW_A23;
  for (const et of spec.etapes_tour || []) {
    if (et.numero === 1 && Array.isArray(et.regles) && et.regles.length > 0) {
      et.regles[0] = NEW_ETAPE1_RATISSAGE;
    } else if (et.numero === 3 && Array.isArray(et.regles)) {
      for (let i = 0; i < et.regles.length; i++) {
        if (String(et.regles[i]).startsWith('3.1 Rêve')) {
          et.regles[i] = NEW_ETAPE3_REVE;
        } else if (String(et.regles[i]).startsWith('3.2 ')) {
          et.regles[i] = NEW_ETAPE3_REVELATION;
        }
      }
    } else if (et.numero === 5 && Array.isArray(et.regles)) {
      et.regles[et.regles.length - 1] = NEW_ETAPE5_FIN;
    } else if (et.numero === 6) {
      et.nom = NEW_ETAPE6_NOM;
      et.regles = [...NEW_ETAPE6_REGLES];
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
if (Array.isArray(catObj.chassis_axes)) {
  catObj.chassis_axes = catObj.chassis_axes.filter(
    (ax) => String(ax.key || '').toLowerCase() !== 'mise_en_place_tactiques'
  );
}
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

exp.CHASSIS_AXES_SPEC = exp.CHASSIS_AXES_SPEC.filter(
  (ax) => String(ax.key || '').toLowerCase() !== 'mise_en_place_tactiques'
);
patchSpecObj(exp.SPEC_FORMELLE_V5_4);

const v542Entry = {
  version: 'v5.4.2',
  date: 'Version en vigueur (2026-11-19)',
  titre: 'Piste des Tactiques fixe (T1..T6), purge de l’Étape 6.1 et activation des Rêves en 2.2 (192 châssis)',
  resume:
    'Piste des Tactiques T1..T6 imprimée en dur (zéro éjection, 6 axes = 192 châssis), suppression complète de l’Étape 6.1 et bascule de SLOT_BUG_CERVEAU sur le profil B par défaut, et activation des Rêves par pose de 2e Défenseur en 2.2 (Option A par défaut : 1 Déf = 1 Machine annulée, Options B/C paramétrables) avec avancée par saut/poussée vers la première case libre à gauche.',
  deltas: [
    {
      domaine: 'Piste des Tactiques fixe (T1..T6) & Châssis 192',
      avant:
        'v5.4.1 : 6 tuiles Tactique mobiles, axe Mise_En_Place_Tactiques (384 châssis), éjection de Tactique à la construction d’un Rêve.',
      apres:
        'v5.4.2 : Cases 1..6 imprimées en dur T1..T6. Suppression de Mise_En_Place_Tactiques (6 axes = 192 châssis). Un Rêve construit se pose par-dessus la case libre la plus à droite (6, puis 5, etc.) sans aucune éjection.'
    },
    {
      domaine: 'Suppression de l’Étape 6.1 & SLOT_BUG_CERVEAU',
      avant:
        'v5.4.1 : Collecte de jetons en 6.1, avancée de la Tactique en tête en 6.2, SLOT_BUG_CERVEAU profil A par défaut.',
      apres:
        'v5.4.2 : Étape 6 réduite au seul ménage de fin de tour (6.2–6.3). SLOT_BUG_CERVEAU bascule par défaut sur le profil B (déviation ±1 rang en 3.2 par défausse d’1 Bug).'
    },
    {
      domaine: 'Activation des Rêves en 2.2 & Avancée par saut/poussée',
      avant:
        'v5.4.1 : Tout dé M tombant sur un Rêve annulait automatiquement la machine et ouvrait le Rêve (avancée simple d’1 cran).',
      apres:
        'v5.4.2 : Pose légale du 2e Défenseur en 2.2 sur un Rêve de la piste. En 3.2, 1 Défenseur annule 1 machine sur ce rang (Option A par défaut ; Options B/C paramétrables) ; toute machine non annulée exécute la Tactique imprimée sous le Rêve. Dès >=1 machine annulée, le Rêve s’ouvre et avance vers la première case libre à sa gauche (saut/poussée du bloc contigu).'
    }
  ]
};
exp.VERSION_CHANGELOG = [
  v542Entry,
  ...exp.VERSION_CHANGELOG.filter((entry) => entry.version !== 'v5.4.2')
];

const header = `// =========================================================================\n// data/amazonia_data_v5_4.js — Données canoniques Amazonia v5.4.2 (6 profils · 192 châssis · Piste T1..T6 fixe · Activation Rêves 2.2 · Réveil de la Forêt)\n// =========================================================================\n`;
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
console.log('Synchronized spec_formelle_v5_4.json, catalog_v5_4.json, and amazonia_data_v5_4.js (v5.4.2, 192 chassis) OK.');
