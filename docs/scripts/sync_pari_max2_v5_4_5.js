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
  "On résout toujours intégralement l'action ou la tuile en cours avant d'examiner la Piste des Gardiens (signal binaire allumé/éteint par case 1..6, sans cumul de cardinalité). Zéro marqueur 'utilisé' : chaque Gardien construit (cases 1..6) peut recevoir au maximum 2 Défenseurs en 2.2 (0 = inactif, 1 = 1 déclenchement attendu, 2 = 2 déclenchements attendus ; variante MAX_2_RES_MAX_1 plafonnant 4. Gardien à 1 Défenseur max). Chaque déclencheur allumé sur une case portant un Défenseur consomme 1 Défenseur et ouvre le Gardien immédiatement ; l'ouverture sur 4. Gardien ne ré-allume jamais 4. Gardien. Balayage à plat dans l'ordre croissant des cases 1 à 6.";

const NEW_A14 =
  "Éveil de la Forêt 100 % Piste des Gardiens (v5.4.5) : actif uniquement si au moins 1 Peuple Animal Sauvage (M, R ou O) est autour de la table, aux Tours 1..7 (priorité absolue à Tour 8). Sortie complète des Rêves de l'Éveil : en 5.3, la Forêt s'éveille si les N Défenseurs de la table ont tous été engagés en 2.2 sur la Piste des Gardiens et qu'aucun pari n'est perdu (0 Défenseur restant sur la Piste des Gardiens).";

const NEW_A15 =
  "Test de fin de partie (5.3) : priorité absolue à Tour 8 (au Tour 8, la fin est toujours TOUR_8) ; sur les Tours 1..7, vérification directe après issue des paris Gardiens de Sommeil du Contremaître (toutes les tuiles Rêves en jeu en bloc continu à gauche cases 1..k de la Piste des Tactiques) ou d'Éveil de la Forêt 100 % Gardiens (les N Défenseurs de la table engagés en 2.2 sur la Piste des Gardiens et 0 Défenseur restant en 5.3). Passage direct à la Repousse Finale.";

const NEW_A21 =
  "Activation et avancée des Rêves (v5.4.5) : en 2.2, un joueur peut poser son Défenseur sur un Rêve déjà présent sur la piste fixe T1..T6 (coût d'activation indépendant de l'Éveil). En 3.2 (Option A par défaut : 1_DEF_1_MACHINE), chaque Défenseur posé sur un Rêve annule 1 machine pointant sur ce rang M (en priorisant la plus menaçante) ; toute machine non annulée exécute la Tactique T1..T6 imprimée sous la case. Dès qu'au moins 1 machine est annulée, le Rêve s'ouvre toujours (allume 5. Rêve) et avance vers la gauche (par saut/poussée vers la 1re case libre à gauche) selon reve_advance_mode (JUMP_PUSH : avance dès >= 1 machine annulée ; CLEAR_RANK_ONLY : avance uniquement si TOUTES les machines de ce rang M ont été annulées ce tour-ci, sinon reste sur sa case).";

const NEW_A22 =
  "Pari d'activation sur les Gardiens — plafond 2 Défenseurs max (v5.4.5) : actif si >= 1 Peuple Animal Sauvage (M/R/O) est à la table. Zéro marqueur 'utilisé' sur les cases 1..6 : un Gardien sans Défenseur est inactif ce tour-ci. En 2.2, chaque Gardien construit (cases 1..6) peut recevoir au maximum 2 Défenseurs selon gardien_bet_cap_policy (UNIFORM_MAX_2 : max 2 Défenseurs sur les 6 cases ; MAX_2_RES_MAX_1 : max 2 Défenseurs sur cases 1, 2, 3, 5, 6 et max 1 Défenseur sur 4. Gardien). Chaque déclenchement de la case consomme 1 Défenseur (mis de côté jusqu'au ménage 6.2) et ouvre le Gardien immédiatement. Anti-boucle 4. Gardien : l'ouverture du Gardien sur 4. Gardien ne ré-allume jamais 4. Gardien. En 5.3 : 0 Défenseur restant -> pari gagné (reste en piste, passe Face 2 en Mode 4 si double-face) ; >= 1 Défenseur restant -> pari perdu (retour immédiat en lisière Face 1).";

const NEW_ETAPE2_1 =
  "2.1 / 2.2 Pose sous paravent fermé : 1er Défenseur irrévocable sur sa Forêt ou ses 2 lisières ; puis Défenseur de portée globale (réflexion -> choix définitif). Anti-blocage : pose interdite sur Route Forestière, tuile construite/pleine/inconstructible ou rive Furtivité bordant une Route (si parcelle requise).";

const NEW_ETAPE2_PARI =
  "2.2 Portée globale, Activation des Rêves & Pari sur les Gardiens : pose en réflexion puis définitive partout sur le plateau, y compris sur un Rêve de la Piste des Tactiques fixe (coût d'activation en 3.2) ou en pari d'activation sur tout Gardien déjà construit (si >= 1 Animal Sauvage M/R/O ; max 2 Défenseurs par Gardien selon gardien_bet_cap_policy : UNIFORM_MAX_2 ou MAX_2_RES_MAX_1 sur 4. Gardien). Un Gardien sans Défenseur reste inactif ce tour-ci.";

const NEW_ETAPE3_REV =
  "3.2 Révélation simultanée (paravents ouverts) : résolution des déviations Bug (SLOT_BUG_CERVEAU profil B par défaut : défausser 1 Insecte posé sur la case M pour décaler le dé M de ±1 rang), puis résolution des rangs portant un Rêve selon les Défenseurs posés dessus en 2.2 (Option A par défaut : 1_DEF_1_MACHINE, chaque Défenseur annule 1 machine en priorisant la plus menaçante ; toute machine non annulée exécute la Tactique imprimée T1..T6 sous la case). Dès qu'au moins 1 machine est annulée, le Rêve s'ouvre toujours (allume 5. Rêve) et avance vers la gauche (saut/poussée vers la 1re case libre à gauche) selon reve_advance_mode (JUMP_PUSH : avance dès >= 1 machine annulée ; CLEAR_RANK_ONLY : avance uniquement si toutes les machines du rang M ont été annulées ce tour-ci).";

const NEW_ETAPE5_FIN =
  "Issue des paris Gardiens & Vérification de fin de partie (5.3) : retrait des Pièges déclenchés, puis résolution des paris Gardiens (0 Défenseur restant -> pari gagné, le Gardien reste en piste et passe Face 2 s'il est double-face en Mode 4 ; >= 1 Défenseur restant -> pari perdu, retour immédiat en lisière d'origine Face 1). Test de fin de partie : priorité absolue au Tour 8 (fin TOUR_8) ; aux Tours 1..7, Sommeil du Contremaître (toutes les tuiles Rêves en jeu en bloc continu 1..k) ou Éveil de la Forêt 100 % Piste des Gardiens (les N Défenseurs de la table engagés en 2.2 sur la Piste des Gardiens et 0 Défenseur restant en 5.3). Si atteint : passage direct à la Repousse Finale.";

const NEW_ETAPE6_REGLES = [
  "Ménage systématique (6.2) : piste des Tactiques T1..T6 fixe (aucun jeton ni déplacement de Tactique), retour en main de tous les Défenseurs (y compris ceux posés sur des Rêves ou Gardiens et ceux consommés après activation) et remise à zéro des modificateurs transitoires.",
  "Clôture du tour (6.3) : passage du pion Coordonnateur au siège suivant et remélange du paquet Machine (hors machines en Ratissage) avec toutes les cartes Sabotage (révélées/écartées ce tour + nouvellement acquises ce tour)."
];

const NEW_VERIF_FIN =
  "Vérification unique à la fin des attaques (5.3, après résolution des paris Gardiens, passage direct à la Repousse Finale). Priorité absolue au Tour 8 (CAUSE_TOUR_8). Aux Tours 1..7 : Sommeil du Contremaître (tous les Rêves en jeu en bloc continu cases 1..k de la Piste des Tactiques fixe T1..T6) ou Éveil de la Forêt 100 % Piste des Gardiens (v5.4.5, actif si >= 1 Peuple Animal Sauvage M/R/O : les N Défenseurs de la table engagés en 2.2 sur la Piste des Gardiens et 0 Défenseur restant en 5.3).";

function patchSpecObj(spec) {
  spec.schema_version = '5.4.5';
  spec.date_consolidation = '2026-11-20';
  if (spec.principes_transverses) {
    spec.principes_transverses.cascades_gardiens_a_plat = NEW_CASCADES;
  }
  spec.arbitrages_valides.A14 = NEW_A14;
  spec.arbitrages_valides.A15 = NEW_A15;
  spec.arbitrages_valides.A21 = NEW_A21;
  spec.arbitrages_valides.A22 = NEW_A22;
  for (const et of spec.etapes_tour || []) {
    if (et.numero === 2 && Array.isArray(et.regles)) {
      let replaced = false;
      for (let i = 0; i < et.regles.length; i++) {
        if (String(et.regles[i]).startsWith('2.1 / 2.2 ')) {
          et.regles[i] = NEW_ETAPE2_1;
        } else if (String(et.regles[i]).startsWith('2.2 ')) {
          et.regles[i] = NEW_ETAPE2_PARI;
          replaced = true;
        }
      }
      if (!replaced) {
        et.regles.push(NEW_ETAPE2_PARI);
      }
    } else if (et.numero === 3 && Array.isArray(et.regles)) {
      const filtered = et.regles.filter((r) => !String(r).startsWith('3.2 '));
      filtered.push(NEW_ETAPE3_REV);
      et.regles = filtered;
    } else if (et.numero === 5 && Array.isArray(et.regles)) {
      et.regles[et.regles.length - 1] = NEW_ETAPE5_FIN;
    } else if (et.numero === 6) {
      et.regles = [...NEW_ETAPE6_REGLES];
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

const v545Entry = {
  version: 'v5.4.5',
  date: 'Version en vigueur (2026-11-20)',
  titre: 'Éveil 100 % Gardiens, Plafond Pari Gardiens max 2 & Avancée Rêves CLEAR_RANK_ONLY',
  resume:
    'Sortie complète des Rêves de l’Éveil de la Forêt (100 % Piste des Gardiens, Tours 1..7, A >= 1), plafond de pari sur les Gardiens à 2 Défenseurs max (gardien_bet_cap_policy : UNIFORM_MAX_2 vs MAX_2_RES_MAX_1 sur 4. Gardien), et avancée des Rêves paramétrable (JUMP_PUSH vs CLEAR_RANK_ONLY : un Rêve qui annule >= 1 machine s’ouvre toujours mais n’avance que si toutes les machines du rang M sont annulées).',
  deltas: [
    {
      domaine: 'Éveil de la Forêt 100 % Piste des Gardiens (Étape 5.3)',
      avant:
        'v5.4.4 : Mobilisation croisée Gardiens + Rêves avec politiques PARITY / PARITY_CAP_ONIRIQUE.',
      apres:
        'v5.4.5 : Sortie complète des Rêves de l’Éveil. Aux Tours 1..7 (si A >= 1, priorité Tour 8), la Forêt s’éveille uniquement si les N Défenseurs de la table ont tous été engagés en 2.2 sur la Piste des Gardiens et qu’aucun pari n’est perdu (0 Défenseur restant).'
    },
    {
      domaine: 'Plafond de pari sur les Gardiens (Étape 2.2)',
      avant:
        'v5.4.4 : Plafond uniforme d’1 seul Défenseur par Gardien sur les cases 1..6.',
      apres:
        'v5.4.5 : Plafond à 2 Défenseurs max par Gardien construit (0 = inactif, 1 = 1 déclenchement attendu, 2 = 2 déclenchements attendus), avec duel UNIFORM_MAX_2 (max 2 sur 1..6) vs MAX_2_RES_MAX_1 (max 1 sur 4. Gardien). Anti-boucle 4. Gardien maintenue.'
    },
    {
      domaine: 'Activation & Avancée des Rêves (Étape 3.2)',
      avant:
        'v5.4.4 : Avancée JUMP_PUSH vs FREE_SLOT_ONLY.',
      apres:
        'v5.4.5 : Rêves en coût d’activation indépendant de l’Éveil. Ajout de CLEAR_RANK_ONLY (face au témoin JUMP_PUSH) : un Rêve qui annule >= 1 machine s’ouvre toujours (allume 5. Rêve), mais n’avance vers la gauche (saut/poussée vers la 1re case libre à gauche) que si toutes les machines de ce rang M sont annulées ce tour-ci.'
    }
  ]
};
exp.VERSION_CHANGELOG = [
  v545Entry,
  ...exp.VERSION_CHANGELOG.filter((entry) => entry.version !== 'v5.4.5')
];

const header = `// =========================================================================\n// data/amazonia_data_v5_4.js — Données canoniques Amazonia v5.4.5 (6 profils · 192 châssis · Piste T1..T6 fixe · Pari Gardiens max 2 · Éveil 100 % Gardiens · Rêves CLEAR_RANK_ONLY)\n// =========================================================================\n`;
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
    `"cascades_gardiens": "Finir intégralement l'action ou le Nid en cours avant d'examiner la Piste des Gardiens. Zéro marqueur de disponibilité : chaque Gardien construit (cases 1..6) ne peut recevoir au maximum qu'1 seul Défenseur en 2.2 (sans Défenseur, il est inactif). Balayage à plat des cases allumées de 1 à 6 ; anti-boucle 4. Gardien (l'ouverture du Gardien sur 4. Gardien ne ré-allume jamais 4. Gardien)."`,
    `"cascades_gardiens": "Finir intégralement l'action ou le Nid en cours avant d'examiner la Piste des Gardiens. Zéro marqueur de disponibilité : chaque Gardien construit (cases 1..6) peut recevoir au maximum 2 Défenseurs en 2.2 (0 = inactif, 1 = 1 déclenchement attendu, 2 = 2 déclenchements attendus ; variante MAX_2_RES_MAX_1 plafonnant 4. Gardien à 1 Défenseur max). Balayage à plat des cases allumées de 1 à 6 ; anti-boucle 4. Gardien (l'ouverture du Gardien sur 4. Gardien ne ré-allume jamais 4. Gardien)."`
  ],
  [
    `"reveil_de_la_foret": "Pari unique Gardiens & Éveil par mobilisation croisée (actif si >= 1 Peuple Animal Sauvage M, R ou O) : en 2.2, max 1 seul Défenseur par Gardien construit (cases 1..6 ; 0 Défenseur = inactif). En 3.2, chaque Défenseur sur un Rêve annulant 1 machine (1_DEF_1_MACHINE) est consommé. En 5.3 : pari Gardien gagné (Défenseur consommé) -> reste en piste (Face 2 en Mode 4 si double-face) ; pari perdu (Défenseur restant) -> retour immédiat en lisière Face 1. Aux Tours 1..7 (priorité Tour 8), si les N Défenseurs ont été engagés en 2.2 sur Gardiens et Rêves, 0 Défenseur restant, et reveil_reves_policy respectée (PARITY ou PARITY_CAP_ONIRIQUE), la Forêt s'éveille."`,
    `"reveil_de_la_foret": "Pari Gardiens (max 2 Défenseurs) & Éveil 100 % Gardiens (actif si >= 1 Peuple Animal Sauvage M, R ou O) : en 2.2, chaque Gardien construit (cases 1..6) peut recevoir au maximum 2 Défenseurs (0 = inactif, 1 = 1 déclenchement attendu, 2 = 2 déclenchements attendus ; UNIFORM_MAX_2 ou MAX_2_RES_MAX_1 sur 4. Gardien). Chaque déclenchement consomme 1 Défenseur et ouvre le Gardien. En 5.3 : 0 Défenseur restant -> pari gagné (reste en piste, Face 2 en Mode 4 si double-face) ; >= 1 Défenseur restant -> pari perdu (retour immédiat en lisière Face 1). Aux Tours 1..7 (priorité Tour 8), si les N Défenseurs de la table ont tous été engagés en 2.2 sur la Piste des Gardiens et qu'aucun pari n'est perdu (0 Défenseur restant), la Forêt s'éveille."`
  ],
  [
    `"2_defenseurs_et_furtivite_4_slots": "Anti-blocage : pose interdite sur Route Forestière, tuile construite/pleine/inconstructible, ou rive Furtivité bordant une Route (si parcelle requise). 1er Défenseur irrévocable sur sa Forêt ou ses 2 lisières ; puis Défenseur de portée globale (réflexion -> définitif), pouvant aussi cibler : (a) un Rêve déjà présent sur la Piste des Tactiques fixe pour l'activer en 3.2, ou (b) un Gardien déjà construit sur la Piste des Gardiens en pari d'activation (si >= 1 Animal Sauvage M/R/O ; max 1 seul Défenseur par Gardien sur les 6 cases ; 0 Défenseur = Gardien inactif ce tour). Case Furtivité = 4 emplacements (2 jumeaux rive J1, 2 jumeaux rive J2 ; max 2 Défenseurs). ENTRER sur la case (toute face) tire l'éventuel autre Défenseur sur l'emplacement jumeau du même bord ; RETOURNER de réflexion à définitif se fait strictement sur place sans déplacement.",`,
    `"2_defenseurs_et_furtivite_4_slots": "Anti-blocage : pose interdite sur Route Forestière, tuile construite/pleine/inconstructible, ou rive Furtivité bordant une Route (si parcelle requise). 1er Défenseur irrévocable sur sa Forêt ou ses 2 lisières ; puis Défenseur de portée globale (réflexion -> définitif), pouvant aussi cibler : (a) un Rêve déjà présent sur la Piste des Tactiques fixe (coût d'activation en 3.2), ou (b) un Gardien déjà construit sur la Piste des Gardiens en pari d'activation (si >= 1 Animal Sauvage M/R/O ; max 2 Défenseurs par Gardien selon gardien_bet_cap_policy : UNIFORM_MAX_2 ou MAX_2_RES_MAX_1 sur 4. Gardien ; 0 Défenseur = Gardien inactif ce tour). Case Furtivité = 4 emplacements (2 jumeaux rive J1, 2 jumeaux rive J2 ; max 2 Défenseurs). ENTRER sur la case (toute face) tire l'éventuel autre Défenseur sur l'emplacement jumeau du même bord ; RETOURNER de réflexion à définitif se fait strictement sur place sans déplacement.",`
  ],
  [
    `"3_2_revelation_et_sabotages": "Ouverture simultanée des paravents ; fin du silence. Toute carte Sabotage révélée est simplement mise de côté (action du Contremaître perdue ce tour) pour être remélangée dans le paquet en 6.3. Déviations Bug (SLOT_BUG_CERVEAU profil B par défaut : défausser 1 Bug du rang M pour décaler M de ±1). Rêve sur le rang M : chaque Défenseur posé dessus en 2.2 qui annule effectivement 1 machine (Option A : 1_DEF_1_MACHINE, en priorisant la plus menaçante) est consommé (pari gagné), sinon reste non consommé jusqu'au ménage ; toute machine non annulée exécute la Tactique imprimée T1..T6 sous le Rêve. Dès >=1 machine annulée, le Rêve s'ouvre (allume 5. Rêve) et avance selon reve_advance_mode (JUMP_PUSH ou FREE_SLOT_ONLY).",`,
    `"3_2_revelation_et_sabotages": "Ouverture simultanée des paravents ; fin du silence. Toute carte Sabotage révélée est simplement mise de côté (action du Contremaître perdue ce tour) pour être remélangée dans le paquet en 6.3. Déviations Bug (SLOT_BUG_CERVEAU profil B par défaut : défausser 1 Bug du rang M pour décaler M de ±1). Rêve sur le rang M : chaque Défenseur posé dessus en 2.2 annule 1 machine (Option A : 1_DEF_1_MACHINE, en priorisant la plus menaçante) ; toute machine non annulée exécute la Tactique imprimée T1..T6 sous le Rêve. Dès >=1 machine annulée, le Rêve s'ouvre toujours (allume 5. Rêve) et avance par saut/poussée vers la 1re case libre à gauche selon reve_advance_mode (JUMP_PUSH : avance dès >=1 machine annulée ; CLEAR_RANK_ONLY : avance uniquement si toutes les machines du rang M ont été annulées ce tour-ci).",`
  ],
  [
    `Fin 5.3 : effets fin d'attaques, retrait Pièges déclenchés, résolution des paris Gardiens (gagné -> reste en piste + Face 2 en Mode 4 si double-face ; perdu -> retour lisière Face 1), puis test Fin de Partie (priorité Tour 8 ; aux Tours 1..7 : Sommeil (toutes les tuiles Rêves en jeu en bloc continu à gauche 1..k) ou Éveil de la Forêt par mobilisation croisée (N Défenseurs engagés sur Gardiens + Rêves, 0 restant et politique PARITY/PARITY_CAP_ONIRIQUE respectée) -> Repousse Finale directe sans Étape 6)."`,
    `Fin 5.3 : effets fin d'attaques, retrait Pièges déclenchés, résolution des paris Gardiens (0 Défenseur restant -> gagné, reste en piste + Face 2 en Mode 4 si double-face ; >=1 Défenseur restant -> perdu, retour lisière Face 1), puis test Fin de Partie (priorité Tour 8 ; aux Tours 1..7 : Sommeil (toutes les tuiles Rêves en jeu en bloc continu à gauche 1..k) ou Éveil de la Forêt 100 % Gardiens (les N Défenseurs engagés en 2.2 sur la Piste des Gardiens et 0 restant en 5.3) -> Repousse Finale directe sans Étape 6)."`
  ],
  [
    `<div><strong>Version :</strong> v5.4.4 (Pari unique Gardiens &amp; Éveil par mobilisation croisée)</div>`,
    `<div><strong>Version :</strong> v5.4.5 (Éveil 100 % Gardiens, Pari Gardiens max 2 &amp; Rêves CLEAR_RANK_ONLY)</div>`
  ],
  [
    `<li>• <strong>Pari Gardiens &amp; Éveil de la Forêt :</strong> <span class="dyn-span">\${reveilActif ? \`Actif (\${nbAnimauxSauvages} Peuple(s) Animal Sauvage M/R/O · \${n} Défenseurs engagés sur Gardiens et Rêves et tous les paris gagnés aux Tours 1..7)\` : \`Inactif (aucun Peuple Animal Sauvage M/R/O autour de la table)\`}</span></li>`,
    `<li>• <strong>Pari Gardiens &amp; Éveil de la Forêt :</strong> <span class="dyn-span">\${reveilActif ? \`Actif (\${nbAnimauxSauvages} Peuple(s) Animal Sauvage M/R/O · \${n} Défenseurs engagés sur la Piste des Gardiens et tous les paris gagnés aux Tours 1..7)\` : \`Inactif (aucun Peuple Animal Sauvage M/R/O autour de la table)\`}</span></li>`
  ],
  [
    `<li><strong>Éveil de la Forêt (Tours 1 à 7) :</strong> <span class="dyn-span">\${reveilActif ? \`Les <strong>\${n} Défenseurs</strong> de la table ont tous été engagés en <strong>pari d'activation</strong> sur la Piste des Gardiens (max 1 Défenseur par Gardien) et la Piste des Tactiques (Rêves) en 2.2, <strong>tous les paris sont gagnés</strong> (<code>0</code> Défenseur restant sur Gardiens et Rêves en 5.3) <strong>ET</strong> la contrainte de parité Gardiens ≥ Rêves est respectée (priorité absolue au Tour 8).\` : \`<em>Condition inactive dans cette partie (aucun Peuple Animal Sauvage M/R/O autour de la table).</em>\`}</span></li>`,
    `<li><strong>Éveil de la Forêt (Tours 1 à 7) :</strong> <span class="dyn-span">\${reveilActif ? \`Les <strong>\${n} Défenseurs</strong> de la table ont tous été engagés en <strong>pari d'activation</strong> sur la <strong>Piste des Gardiens</strong> en 2.2 (max 2 Défenseurs par Gardien ; Rêves hors Éveil) <strong>ET tous les paris sont gagnés</strong> (<code>0</code> Défenseur restant sur la Piste des Gardiens en 5.3 ; priorité absolue au Tour 8).\` : \`<em>Condition inactive dans cette partie (aucun Peuple Animal Sauvage M/R/O autour de la table).</em>\`}</span></li>`
  ],
  [
    `<strong>Étape 2.2 (Portée globale, Activation de Rêve &amp; Pari unique sur les Gardiens) :</strong> Une fois tous les premiers pions posés, chacun pose son Défenseur partout sur le plateau (face <em>« en réflexion »</em> déplaçable d'une case à une autre, ou directement face <em>« définitive »</em>). Vous pouvez le poser sur un <strong>Rêve déjà présent sur la Piste des Tactiques fixe</strong> pour l'activer en 3.2. <span class="dyn-span">\${reveilActif ? \`Vous pouvez aussi poser un <strong>pari d'activation</strong> sur tout <strong>Gardien déjà construit</strong> sur la Piste des Gardiens (<strong>au maximum 1 seul Défenseur par Gardien</strong> sur l'ensemble des 6 cases ; un Gardien portant <code>0</code> Défenseur reste inactif ce tour-ci).\` : ''}</span> Le passage se clôt quand tous sont sur leur face <em>« définitive »</em>.`,
    `<strong>Étape 2.2 (Portée globale, Activation de Rêve &amp; Pari sur les Gardiens) :</strong> Une fois tous les premiers pions posés, chacun pose son Défenseur partout sur le plateau (face <em>« en réflexion »</em> déplaçable d'une case à une autre, ou directement face <em>« définitive »</em>). Vous pouvez le poser sur un <strong>Rêve déjà présent sur la Piste des Tactiques fixe</strong> (coût d'activation en 3.2). <span class="dyn-span">\${reveilActif ? \`Vous pouvez aussi poser un <strong>pari d'activation</strong> sur tout <strong>Gardien déjà construit</strong> sur la Piste des Gardiens (<strong>max 2 Défenseurs par Gardien</strong> : <code>0</code> = inactif, <code>1</code> = 1 déclenchement attendu, <code>2</code> = 2 déclenchements attendus ; variante <code>MAX_2_RES_MAX_1</code> plafonnant <strong>4. Gardien</strong> à 1 Défenseur max).\` : ''}</span> Le passage se clôt quand tous sont sur leur face <em>« définitive »</em>.`
  ],
  [
    `• <strong>Verrouillage strictement sur place :</strong> retourner un 2<sup>e</sup> Défenseur déjà posé de sa face <em>« en réflexion »</em> à sa face <em>« définitive »</em>`,
    `• <strong>Verrouillage strictement sur place :</strong> retourner un Défenseur déjà posé de sa face <em>« en réflexion »</em> à sa face <em>« définitive »</em>`
  ],
  [
    `<li><strong>Rêves (dé M désignant un Rêve) :</strong> chaque Défenseur posé sur ce Rêve en 2.2 qui <strong>annule effectivement 1 carte Machine</strong> pointant sur ce rang <code>M</code> (en priorisant la plus menaçante) est <strong>consommé</strong> (pari gagné) ; sinon il reste non consommé sur le Rêve jusqu'au ménage. Toute machine non annulée exécute la Tactique imprimée <code>T1..T6</code> sous la case. Dès qu'au moins 1 machine est annulée, le Rêve s'ouvre (allume <strong>5. Rêve</strong> ; <span class="dyn-span">\${c.Regle_Ouverture_Reve_Multiple === 'UNIQUE_PAR_TOUR' ? '<strong>max 1 ouverture par Rêve et par tour</strong>' : '<strong>mode cumulatif</strong>'}</span>) et avance vers la gauche (selon le mode d'avancée actif : saut/poussée <code>JUMP_PUSH</code> ou case immédiatement libre uniquement <code>FREE_SLOT_ONLY</code>).</li>`,
    `<li><strong>Rêves (dé M désignant un Rêve) :</strong> chaque Défenseur posé sur ce Rêve en 2.2 <strong>annule 1 carte Machine</strong> pointant sur ce rang <code>M</code> (en priorisant la plus menaçante). Toute machine non annulée exécute la Tactique imprimée <code>T1..T6</code> sous la case. Dès qu'au moins 1 machine est annulée, le Rêve s'ouvre toujours (allume <strong>5. Rêve</strong> ; <span class="dyn-span">\${c.Regle_Ouverture_Reve_Multiple === 'UNIQUE_PAR_TOUR' ? '<strong>max 1 ouverture par Rêve et par tour</strong>' : '<strong>mode cumulatif</strong>'}</span>) et avance vers la gauche par saut/poussée vers la 1<sup>re</sup> case libre à gauche selon le mode actif (<code>JUMP_PUSH</code> : avance dès ≥ 1 machine annulée ; <code>CLEAR_RANK_ONLY</code> : avance uniquement si <strong>toutes</strong> les machines de ce rang <code>M</code> ont été annulées ce tour-ci, sinon reste sur sa case).</li>`
  ],
  [
    `<h3 class="font-bold text-amber-950 text-sm mb-1.5">4.1. Piste des Gardiens (Pari unique 1 → 6 &amp; Anti-boucle 4. Gardien)</h3>`,
    `<h3 class="font-bold text-amber-950 text-sm mb-1.5">4.1. Piste des Gardiens (Pari max 2 Défenseurs 1 → 6 &amp; Anti-boucle 4. Gardien)</h3>`
  ],
  [
    `<strong>Pari unique par Défenseur &amp; Anti-boucle 4. Gardien :</strong> terminez toujours l'effet en cours, puis parcourez les cases allumées de <strong>1 à 6</strong>. Un Gardien construit (cases 1..6) ne peut recevoir au maximum qu'<strong>1 seul Défenseur</strong> en 2.2. Dès que son déclencheur s'allume, consommez ce <strong>Défenseur</strong> (mis de côté jusqu'au ménage 6.2) et ouvrez immédiatement le Gardien. L'ouverture du Gardien placé sur <strong>4. Gardien</strong> ne ré-allume jamais <strong>4. Gardien</strong> elle-même. En <strong>5.3</strong> : tout pari gagné (Défenseur consommé) maintient le Gardien sur la piste (et retourne en Face 2 un Gardien double-face en Mode 4) ; tout pari perdu (Défenseur non consommé) renvoie immédiatement le Gardien sur sa lisière d'origine (Face 1).`,
    `<strong>Pari par Défenseur (max 2) &amp; Anti-boucle 4. Gardien :</strong> terminez toujours l'effet en cours, puis parcourez les cases allumées de <strong>1 à 6</strong>. Chaque Gardien construit (cases 1..6) peut recevoir au maximum <strong>2 Défenseurs</strong> en 2.2 (<code>0</code> = inactif, <code>1</code> = 1 déclenchement attendu, <code>2</code> = 2 déclenchements attendus ; variante <code>MAX_2_RES_MAX_1</code> plafonnant <strong>4. Gardien</strong> à 1 Défenseur max). Chaque déclenchement de la case consomme <strong>1 Défenseur</strong> (mis de côté jusqu'au ménage 6.2) et ouvre immédiatement le Gardien. L'ouverture du Gardien placé sur <strong>4. Gardien</strong> ne ré-allume jamais <strong>4. Gardien</strong> elle-même. En <strong>5.3</strong> : <code>0</code> Défenseur restant → pari gagné (le Gardien reste en piste et passe Face 2 en Mode 4 si double-face) ; <code>≥ 1</code> Défenseur restant → pari perdu (retour immédiat sur sa lisière d'origine Face 1).`
  ],
  [
    `Gouverné par son <em>Peuple d'origine</em>. Activé en 2.2 par la pose d'un Défenseur : en 3.2, chaque Défenseur dessus qui annule 1 machine pointant sur ce rang <code>M</code> est consommé (pari gagné), allume <strong>5. Rêve</strong> et fait avancer le Rêve vers la gauche (vers le bloc continu <code>1..k</code> du Sommeil).`,
    `Gouverné par son <em>Peuple d'origine</em>. Activé en 2.2 par la pose d'un Défenseur (coût d'activation hors Éveil) : en 3.2, chaque Défenseur dessus annule 1 machine pointant sur ce rang <code>M</code>, ouvre toujours le Rêve (allume <strong>5. Rêve</strong>) et le fait avancer vers la gauche (selon <code>JUMP_PUSH</code> ou <code>CLEAR_RANK_ONLY</code>, vers le bloc continu <code>1..k</code> du Sommeil).`
  ]
];

for (const [oldStr, newStr] of livretReplacements) {
  if (!livretJs.includes(oldStr)) {
    throw new Error(`Pattern introuvable dans livret_v5_4.js : ${oldStr.slice(0, 80)}`);
  }
  livretJs = livretJs.replace(oldStr, newStr);
}

new vm.Script(livretJs);
fs.writeFileSync(LIVRET_JS_PATH, livretJs, 'utf8');
console.log('Synchronized 4 layers (spec_formelle, catalog, amazonia_data, livret) for v5.4.5 OK.');
