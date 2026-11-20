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
  "On résout toujours intégralement l'action ou la tuile en cours avant d'examiner la Piste des Gardiens (signal binaire allumé/éteint par case 1..6, sans cumul de cardinalité). Zéro marqueur 'utilisé' : un Gardien construit ne peut recevoir qu'1 seul Défenseur en 2.2 (un Gardien sans Défenseur est inactif). Chaque déclencheur allumé sur une case portant un Défenseur consomme ce Défenseur et ouvre le Gardien ; l'ouverture sur 4. Gardien ne ré-allume jamais 4. Gardien. Balayage à plat dans l'ordre croissant des cases 1 à 6.";

const NEW_A14 =
  "Mobilisation croisée & Éveil de la Forêt (v5.4.4) : actif uniquement si au moins 1 Peuple Animal Sauvage (M, R ou O) est autour de la table, aux Tours 1..7 (priorité absolue à Tour 8). En 5.3, la Forêt s'éveille si les N Défenseurs de la table ont tous été engagés en 2.2 sur la Piste des Gardiens et la Piste des Tactiques (Rêves), qu'aucun pari n'est perdu (0 Défenseur restant sur Gardiens et Rêves), et que la politique reveil_reves_policy est respectée (PARITY : gardiens_won >= reves_won ; PARITY_CAP_ONIRIQUE : gardiens_won >= reves_won et reves_won <= nb_peuples_oniriques H/E).";

const NEW_A15 =
  "Test de fin de partie (5.3) : priorité absolue à Tour 8 (au Tour 8, la fin est toujours TOUR_8) ; sur les Tours 1..7, vérification directe après issue des paris Gardiens de Sommeil du Contremaître (toutes les tuiles Rêves en jeu en bloc continu à gauche cases 1..k de la Piste des Tactiques) ou d'Éveil de la Forêt par mobilisation croisée (les N Défenseurs de la table engagés en 2.2 sur Gardiens et Rêves, 0 Défenseur restant en 5.3 et contrainte reveil_reves_policy respectée). Passage direct à la Repousse Finale.";

const NEW_A21 =
  "Activation, consommation symétrique et avancée des Rêves (v5.4.4) : en 2.2, un joueur peut poser son Défenseur sur un Rêve déjà présent sur la piste fixe T1..T6. En 3.2 (Option A par défaut : 1_DEF_1_MACHINE), chaque Défenseur posé sur un Rêve qui annule effectivement 1 machine (en priorisant la plus menaçante) est consommé (pari gagné) ; sinon il reste non consommé sur le Rêve jusqu'au ménage 6.2. Toute machine non annulée exécute la Tactique T1..T6 imprimée sous la case. Dès qu'au moins 1 machine est annulée, le Rêve s'ouvre (allume 5. Rêve) et avance selon reve_advance_mode (JUMP_PUSH : saut/poussée vers la 1re case libre à gauche ; FREE_SLOT_ONLY : avance d'1 cran à gauche uniquement si la case immédiatement à gauche est libre, sinon reste sur place).";

const NEW_A22 =
  "Pari unique sur les Gardiens (v5.4.4) : actif si >= 1 Peuple Animal Sauvage (M/R/O) est à la table. Zéro marqueur 'utilisé' sur les cases 1..6 : un Gardien sans Défenseur est inactif ce tour-ci. En 2.2, chaque Gardien construit (cases 1..6) ne peut recevoir au maximum qu'1 seul Défenseur (limite uniforme sur les 6 cases). Dès que son déclencheur s'allume, son Défenseur est consommé (mis de côté jusqu'au ménage 6.2) et le Gardien s'ouvre immédiatement. Anti-boucle 4. Gardien : l'ouverture du Gardien sur 4. Gardien ne ré-allume jamais 4. Gardien. En 5.3 : pari gagné (Défenseur consommé) -> le Gardien reste sur la piste (et passe Face 2 s'il est double-face en Mode 4) ; pari perdu (Défenseur non consommé) -> retour immédiat en lisière d'origine (Face 1).";

const NEW_ETAPE2_PARI =
  "2.2 Portée globale, Activation des Rêves & Pari unique sur les Gardiens : pose en réflexion puis définitive partout sur le plateau, y compris sur un Rêve de la Piste des Tactiques fixe (activation 3.2) ou en pari d'activation sur tout Gardien déjà construit (si >= 1 Animal Sauvage M/R/O ; max 1 seul Défenseur par Gardien sur l'ensemble des 6 cases). Un Gardien sans Défenseur reste inactif ce tour-ci.";

const NEW_ETAPE3_REV =
  "3.2 Révélation simultanée (paravents ouverts) : résolution des déviations Bug (SLOT_BUG_CERVEAU profil B par défaut : défausser 1 Insecte posé sur la case M pour décaler le dé M de ±1 rang), puis résolution des rangs portant un Rêve selon les Défenseurs posés dessus en 2.2 (Option A par défaut : chaque Défenseur qui annule effectivement 1 machine en priorisant la plus menaçante est consommé ; sinon il reste non consommé sur le Rêve jusqu'au ménage ; toute machine non annulée exécute la Tactique imprimée T1..T6 sous la case). Dès qu'au moins 1 machine est annulée, le Rêve s'ouvre (allume 5. Rêve) et avance vers la gauche selon reve_advance_mode (JUMP_PUSH ou FREE_SLOT_ONLY).";

const NEW_ETAPE5_FIN =
  "Issue des paris Gardiens & Vérification de fin de partie (5.3) : retrait des Pièges déclenchés, puis résolution des paris Gardiens (pari gagné : Défenseur consommé -> le Gardien reste en piste et passe Face 2 s'il est double-face en Mode 4 ; pari perdu : Défenseur non consommé -> retour immédiat en lisière d'origine Face 1). Test de fin de partie : priorité absolue au Tour 8 (fin TOUR_8) ; aux Tours 1..7, Sommeil du Contremaître (toutes les tuiles Rêves en jeu en bloc continu 1..k) ou Éveil de la Forêt par mobilisation croisée (les N Défenseurs de la table engagés en 2.2 sur Gardiens et Rêves, 0 Défenseur restant en 5.3, et contrainte reveil_reves_policy respectée : PARITY ou PARITY_CAP_ONIRIQUE). Si atteint : passage direct à la Repousse Finale.";

const NEW_ETAPE6_REGLES = [
  "Ménage systématique (6.2) : piste des Tactiques T1..T6 fixe (aucun jeton ni déplacement de Tactique), retour en main de tous les Défenseurs (y compris ceux posés sur des Rêves ou Gardiens et ceux consommés après activation) et remise à zéro des modificateurs transitoires.",
  "Clôture du tour (6.3) : passage du pion Coordonnateur au siège suivant et remélange du paquet Machine (hors machines en Ratissage) avec toutes les cartes Sabotage (révélées/écartées ce tour + nouvellement acquises ce tour)."
];

const NEW_VERIF_FIN =
  "Vérification unique à la fin des attaques (5.3, après résolution des paris Gardiens, passage direct à la Repousse Finale). Priorité absolue au Tour 8 (CAUSE_TOUR_8). Aux Tours 1..7 : Sommeil du Contremaître (tous les Rêves en jeu en bloc continu cases 1..k de la Piste des Tactiques fixe T1..T6) ou Éveil de la Forêt par mobilisation croisée (v5.4.4, actif si >= 1 Peuple Animal Sauvage M/R/O : les N Défenseurs de la table engagés en 2.2 sur Gardiens et Rêves, 0 Défenseur restant en 5.3, et contrainte reveil_reves_policy respectée : PARITY ou PARITY_CAP_ONIRIQUE).";

function patchSpecObj(spec) {
  spec.schema_version = '5.4.4';
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
        if (String(et.regles[i]).startsWith('2.2 ')) {
          et.regles[i] = NEW_ETAPE2_PARI;
          replaced = true;
        }
      }
      if (!replaced) {
        et.regles.push(NEW_ETAPE2_PARI);
      }
    } else if (et.numero === 3 && Array.isArray(et.regles)) {
      // Déduplication éventuelle de 3.2 et mise à jour propre
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

const v544Entry = {
  version: 'v5.4.4',
  date: 'Version en vigueur (2026-11-20)',
  titre: 'Pari unique sur les Gardiens, Consommation symétrique des Rêves & Éveil par mobilisation croisée',
  resume:
    'Uniformisation du pari Gardien à 1 seul Défenseur max par Gardien construit (cases 1..6), consommation symétrique des Défenseurs sur les Rêves qui annulent effectivement 1 machine en 3.2, Éveil de la Forêt par mobilisation croisée (Gardiens + Rêves, politiques PARITY et PARITY_CAP_ONIRIQUE), et mode d’avancée des Rêves reve_advance_mode (JUMP_PUSH vs FREE_SLOT_ONLY). Purge du reliquat v5.4.1 dans spec_formelle.fins_5_3.',
  deltas: [
    {
      domaine: 'Pari unique sur les Gardiens (Étape 2.2)',
      avant:
        'v5.4.3 : Cumul libre de Défenseurs sur un même Gardien (exception gardien_resonance_cap sur 4. Résonance).',
      apres:
        'v5.4.4 : Limite uniforme d’1 seul Défenseur par Gardien construit sur l’ensemble des 6 cases (anti-boucle 4. Gardien conservée).'
    },
    {
      domaine: 'Consommation symétrique & Avancée des Rêves (Étape 3.2)',
      avant:
        'v5.4.3 : Défenseurs sur Rêves non suivis comme paris consommés ; avancée uniquement par saut/poussée (JUMP_PUSH).',
      apres:
        'v5.4.4 : Chaque Défenseur sur un Rêve annulant effectivement 1 machine (Option A : 1_DEF_1_MACHINE) est consommé (pari gagné), sinon reste non consommé jusqu’au ménage. Deux modes d’avancée : JUMP_PUSH et FREE_SLOT_ONLY.'
    },
    {
      domaine: 'Éveil de la Forêt par mobilisation croisée (Étape 5.3)',
      avant:
        'v5.4.3 : Éveil exigeant les N Défenseurs uniquement sur la Piste des Gardiens.',
      apres:
        'v5.4.4 : Aux Tours 1..7 (si A >= 1, priorité Tour 8), la Forêt s’éveille si les N Défenseurs ont été engagés en 2.2 sur Gardiens + Rêves, 0 pari perdu (0 Défenseur restant), et contrainte reveil_reves_policy respectée (PARITY : gardiens_won >= reves_won ; PARITY_CAP_ONIRIQUE : + reves_won <= nb_peuples_oniriques).'
    }
  ]
};
exp.VERSION_CHANGELOG = [
  v544Entry,
  ...exp.VERSION_CHANGELOG.filter((entry) => entry.version !== 'v5.4.4')
];

const header = `// =========================================================================\n// data/amazonia_data_v5_4.js — Données canoniques Amazonia v5.4.4 (6 profils · 192 châssis · Piste T1..T6 fixe · Pari unique Gardiens · Mobilisation croisée)\n// =========================================================================\n`;
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
    `"cascades_gardiens": "Finir intégralement l'action ou le Nid en cours avant d'examiner la Piste des Gardiens. Plus aucun marqueur de disponibilité : les 2es Défenseurs posés sur un Gardien sont son compteur d'activations restantes (à 0, le Gardien est inactif). Balayage à plat des cases allumées de 1 à 6 ; anti-boucle 4. Résonance (l'ouverture du Gardien sur 4. Résonance ne ré-allume jamais 4. Résonance)."`,
    `"cascades_gardiens": "Finir intégralement l'action ou le Nid en cours avant d'examiner la Piste des Gardiens. Zéro marqueur de disponibilité : chaque Gardien construit (cases 1..6) ne peut recevoir au maximum qu'1 seul Défenseur en 2.2 (sans Défenseur, il est inactif). Balayage à plat des cases allumées de 1 à 6 ; anti-boucle 4. Gardien (l'ouverture du Gardien sur 4. Gardien ne ré-allume jamais 4. Gardien)."`
  ],
  [
    `"reveil_de_la_foret": "Pari d'activation des Gardiens & Éveil de la Forêt (actif si >= 1 Peuple Animal Sauvage M, R ou O) : en 2.2, pose cumulable de 2es Défenseurs sur tout Gardien construit (0 Défenseur = inactif ; paramètre hors-châssis UNLIMITED ou MAX_1_DEF sur 4. Résonance). Chaque déclencheur retire 1 Défenseur et ouvre le Gardien immédiatement. En 5.3 : pari gagné (>=1 posé en 2.2 et 0 restant) -> reste en piste (Face 2 en Mode 4 si double-face) ; pari perdu (>=1 restant) -> retour immédiat en lisière d'origine Face 1. Aux Tours 1..7 (priorité à Tour 8), si les N 2es Défenseurs ont tous été engagés sur la Piste des Gardiens et tous les paris sont gagnés, l'Éveil de la Forêt déclenche immédiatement la fin de partie."`,
    `"reveil_de_la_foret": "Pari unique Gardiens & Éveil par mobilisation croisée (actif si >= 1 Peuple Animal Sauvage M, R ou O) : en 2.2, max 1 seul Défenseur par Gardien construit (cases 1..6 ; 0 Défenseur = inactif). En 3.2, chaque Défenseur sur un Rêve annulant 1 machine (1_DEF_1_MACHINE) est consommé. En 5.3 : pari Gardien gagné (Défenseur consommé) -> reste en piste (Face 2 en Mode 4 si double-face) ; pari perdu (Défenseur restant) -> retour immédiat en lisière Face 1. Aux Tours 1..7 (priorité Tour 8), si les N Défenseurs ont été engagés en 2.2 sur Gardiens et Rêves, 0 Défenseur restant, et reveil_reves_policy respectée (PARITY ou PARITY_CAP_ONIRIQUE), la Forêt s'éveille."`
  ],
  [
    `"2_defenseurs_et_furtivite_4_slots": "Anti-blocage : pose interdite sur Route Forestière, tuile construite/pleine/inconstructible, ou rive Furtivité bordant une Route (si parcelle requise). 1er Défenseur irrévocable sur sa Forêt ou ses 2 lisières ; puis 2e Défenseur global (réflexion -> définitif), pouvant aussi cibler : (a) un Rêve déjà présent sur la piste fixe pour l'activer en 3.2 (immobilisé jusqu'en 6.2), ou (b) un Gardien déjà construit sur la Piste des Gardiens en pari d'activation (si >= 1 Animal Sauvage M/R/O ; cumul autorisé, paramètre hors-châssis UNLIMITED ou MAX_1_DEF sur 4. Résonance ; 0 Défenseur = Gardien inactif ce tour). Case Furtivité = 4 emplacements (2 jumeaux rive J1, 2 jumeaux rive J2 ; max 2 Défenseurs). ENTRER sur la case (toute face) tire l'éventuel autre Défenseur sur l'emplacement jumeau du même bord ; RETOURNER de réflexion à définitif se fait strictement sur place sans déplacement.",`,
    `"2_defenseurs_et_furtivite_4_slots": "Anti-blocage : pose interdite sur Route Forestière, tuile construite/pleine/inconstructible, ou rive Furtivité bordant une Route (si parcelle requise). 1er Défenseur irrévocable sur sa Forêt ou ses 2 lisières ; puis Défenseur de portée globale (réflexion -> définitif), pouvant aussi cibler : (a) un Rêve déjà présent sur la Piste des Tactiques fixe pour l'activer en 3.2, ou (b) un Gardien déjà construit sur la Piste des Gardiens en pari d'activation (si >= 1 Animal Sauvage M/R/O ; max 1 seul Défenseur par Gardien sur les 6 cases ; 0 Défenseur = Gardien inactif ce tour). Case Furtivité = 4 emplacements (2 jumeaux rive J1, 2 jumeaux rive J2 ; max 2 Défenseurs). ENTRER sur la case (toute face) tire l'éventuel autre Défenseur sur l'emplacement jumeau du même bord ; RETOURNER de réflexion à définitif se fait strictement sur place sans déplacement.",`
  ],
  [
    `"3_2_revelation_et_sabotages": "Ouverture simultanée des paravents ; fin du silence. Toute carte Sabotage révélée est simplement mise de côté (action du Contremaître perdue ce tour) pour être remélangée dans le paquet en 6.3. Déviations Bug (SLOT_BUG_CERVEAU profil B par défaut : défausser 1 Bug du rang M pour décaler M de ±1). Rêve sur le rang M : chaque 2e Défenseur posé dessus en 2.2 annule 1 machine sur ce rang en priorisant la plus menaçante (Option A par défaut ; Options B/C paramétrables) ; toute machine non annulée exécute la Tactique imprimée T1..T6 sous le Rêve. Dès >=1 machine annulée, le Rêve s'ouvre et avance vers la première case libre à sa gauche (saut/poussée d'un bloc contigu de Rêves).",`,
    `"3_2_revelation_et_sabotages": "Ouverture simultanée des paravents ; fin du silence. Toute carte Sabotage révélée est simplement mise de côté (action du Contremaître perdue ce tour) pour être remélangée dans le paquet en 6.3. Déviations Bug (SLOT_BUG_CERVEAU profil B par défaut : défausser 1 Bug du rang M pour décaler M de ±1). Rêve sur le rang M : chaque Défenseur posé dessus en 2.2 qui annule effectivement 1 machine (Option A : 1_DEF_1_MACHINE, en priorisant la plus menaçante) est consommé (pari gagné), sinon reste non consommé jusqu'au ménage ; toute machine non annulée exécute la Tactique imprimée T1..T6 sous le Rêve. Dès >=1 machine annulée, le Rêve s'ouvre (allume 5. Rêve) et avance selon reve_advance_mode (JUMP_PUSH ou FREE_SLOT_ONLY).",`
  ],
  [
    `Fin 5.3 : effets fin d'attaques, retrait Pièges déclenchés, résolution des paris Gardiens (gagné -> reste en piste + Face 2 en Mode 4 si double-face ; perdu -> retour lisière Face 1), puis test Fin de Partie (priorité Tour 8 ; aux Tours 1..7 : Sommeil (toutes les tuiles Rêves en jeu en bloc continu à gauche 1..k) ou Éveil de la Forêt (N 2es Défenseurs engagés sur la Piste des Gardiens et tous les paris gagnés) -> Repousse Finale directe sans Étape 6)."`,
    `Fin 5.3 : effets fin d'attaques, retrait Pièges déclenchés, résolution des paris Gardiens (gagné -> reste en piste + Face 2 en Mode 4 si double-face ; perdu -> retour lisière Face 1), puis test Fin de Partie (priorité Tour 8 ; aux Tours 1..7 : Sommeil (toutes les tuiles Rêves en jeu en bloc continu à gauche 1..k) ou Éveil de la Forêt par mobilisation croisée (N Défenseurs engagés sur Gardiens + Rêves, 0 restant et politique PARITY/PARITY_CAP_ONIRIQUE respectée) -> Repousse Finale directe sans Étape 6)."`
  ],
  [
    `"6_menage_fin_tour": "Piste T1..T6 fixe (aucun jeton ni déplacement de Tactique). 6.2–6.3 : retrait des marqueurs Gardiens, retour en main de tous les Défenseurs (y compris ceux engagés sur Rêves ou Gardiens), résolution du sort d'un éventuel Gardien engagé pour un Réveil échoué (retour lisière Face 1 ou retrait définitif), et remélange du paquet Machine (hors Ratissage) avec TOUTES les cartes Sabotage (révélées ce tour + nouvellement acquises)."`,
    `"6_menage_fin_tour": "Piste T1..T6 fixe (aucun jeton ni déplacement de Tactique). 6.2–6.3 : retour en main de tous les Défenseurs (y compris ceux posés sur Rêves ou Gardiens et ceux consommés après activation) et remélange du paquet Machine (hors Ratissage) avec TOUTES les cartes Sabotage (révélées ce tour + nouvellement acquises)."`
  ],
  [
    `<div><strong>Version :</strong> v5.4.3 (Pari d'activation des Gardiens &amp; Éveil de la Forêt)</div>`,
    `<div><strong>Version :</strong> v5.4.4 (Pari unique Gardiens &amp; Éveil par mobilisation croisée)</div>`
  ],
  [
    `<li>• <strong>Pari Gardiens &amp; Éveil de la Forêt :</strong> <span class="dyn-span">\${reveilActif ? \`Actif (\${nbAnimauxSauvages} Peuple(s) Animal Sauvage M/R/O · \${n} 2es Défenseurs engagés sur la Piste des Gardiens et tous les paris gagnés aux Tours 1..7)\` : \`Inactif (aucun Peuple Animal Sauvage M/R/O autour de la table)\`}</span></li>`,
    `<li>• <strong>Pari Gardiens &amp; Éveil de la Forêt :</strong> <span class="dyn-span">\${reveilActif ? \`Actif (\${nbAnimauxSauvages} Peuple(s) Animal Sauvage M/R/O · \${n} Défenseurs engagés sur Gardiens et Rêves et tous les paris gagnés aux Tours 1..7)\` : \`Inactif (aucun Peuple Animal Sauvage M/R/O autour de la table)\`}</span></li>`
  ],
  [
    `<li><strong>Éveil de la Forêt (Tours 1 à 7) :</strong> <span class="dyn-span">\${reveilActif ? \`Les <strong>\${n} Deuxièmes Défenseurs</strong> de la table ont tous été engagés en <strong>pari d'activation</strong> sur la Piste des Gardiens en 2.2 (répartis librement sur un ou plusieurs Gardiens) <strong>ET tous les paris sont gagnés</strong> (<code>0</code> Défenseur restant sur la piste en 5.3 ; priorité absolue au Tour 8).\` : \`<em>Condition inactive dans cette partie (aucun Peuple Animal Sauvage M/R/O autour de la table).</em>\`}</span></li>`,
    `<li><strong>Éveil de la Forêt (Tours 1 à 7) :</strong> <span class="dyn-span">\${reveilActif ? \`Les <strong>\${n} Défenseurs</strong> de la table ont tous été engagés en <strong>pari d'activation</strong> sur la Piste des Gardiens (max 1 Défenseur par Gardien) et la Piste des Tactiques (Rêves) en 2.2, <strong>tous les paris sont gagnés</strong> (<code>0</code> Défenseur restant sur Gardiens et Rêves en 5.3) <strong>ET</strong> la contrainte de parité Gardiens ≥ Rêves est respectée (priorité absolue au Tour 8).\` : \`<em>Condition inactive dans cette partie (aucun Peuple Animal Sauvage M/R/O autour de la table).</em>\`}</span></li>`
  ],
  [
    `Si ce rang porte un <strong>Rêve</strong>, posez un 2<sup>e</sup> Défenseur dessus en 2.2 pour l'activer et annuler votre machine en 3.2 !`,
    `Si ce rang porte un <strong>Rêve</strong>, posez un Défenseur dessus en 2.2 pour l'activer et annuler votre machine en 3.2 !`
  ],
  [
    `<strong>2<sup>e</sup> Défenseur (Portée globale, Activation de Rêve &amp; Pari d'activation des Gardiens) :</strong> Une fois tous les Premiers Défenseurs posés, chacun pose son Deuxième Défenseur partout sur le plateau (face <em>« en réflexion »</em> déplaçable d'une case à une autre, ou directement face <em>« définitive »</em>). Vous pouvez le poser sur un <strong>Rêve déjà présent sur la piste fixe</strong> pour l'activer en 3.2 (le Défenseur validé y reste immobilisé jusqu'au ménage de fin de tour). <span class="dyn-span">\${reveilActif ? \`Vous pouvez aussi poser un <strong>pari d'activation</strong> sur tout <strong>Gardien déjà construit</strong> sur la Piste des Gardiens (plusieurs 2<sup>es</sup> Défenseurs peuvent se cumuler sur un même Gardien = autant d'activations potentielles ; un Gardien portant <code>0</code> Défenseur reste inactif ce tour-ci).\` : ''}</span> Le passage se clôt quand tous sont sur leur face <em>« définitive »</em>.`,
    `<strong>Étape 2.2 (Portée globale, Activation de Rêve &amp; Pari unique sur les Gardiens) :</strong> Une fois tous les premiers pions posés, chacun pose son Défenseur partout sur le plateau (face <em>« en réflexion »</em> déplaçable d'une case à une autre, ou directement face <em>« définitive »</em>). Vous pouvez le poser sur un <strong>Rêve déjà présent sur la Piste des Tactiques fixe</strong> pour l'activer en 3.2. <span class="dyn-span">\${reveilActif ? \`Vous pouvez aussi poser un <strong>pari d'activation</strong> sur tout <strong>Gardien déjà construit</strong> sur la Piste des Gardiens (<strong>au maximum 1 seul Défenseur par Gardien</strong> sur l'ensemble des 6 cases ; un Gardien portant <code>0</code> Défenseur reste inactif ce tour-ci).\` : ''}</span> Le passage se clôt quand tous sont sur leur face <em>« définitive »</em>.`
  ],
  [
    `<li><strong>Rêves (dé M désignant un Rêve) :</strong> chaque 2<sup>e</sup> Défenseur posé sur ce Rêve en 2.2 <strong>annule 1 carte Machine</strong> pointant sur ce rang <code>M</code> (s'il y a plus de machines que de Défenseurs, le Peuple d'origine du Rêve priorise la plus menaçante). Toute machine non annulée exécute la Tactique imprimée <code>T1..T6</code> sous la case. Dès qu'au moins 1 machine est annulée, le Rêve s'ouvre (<span class="dyn-span">\${c.Regle_Ouverture_Reve_Multiple === 'UNIQUE_PAR_TOUR' ? '<strong>max 1 ouverture par Rêve et par tour</strong>' : '<strong>mode cumulatif</strong>'}</span>) et avance d'1 cran vers la gauche en sautant/poussant tout bloc contigu de Rêves vers la <strong>première case libre à sa gauche</strong> (plafonné au Rang 1).</li>`,
    `<li><strong>Rêves (dé M désignant un Rêve) :</strong> chaque Défenseur posé sur ce Rêve en 2.2 qui <strong>annule effectivement 1 carte Machine</strong> pointant sur ce rang <code>M</code> (en priorisant la plus menaçante) est <strong>consommé</strong> (pari gagné) ; sinon il reste non consommé sur le Rêve jusqu'au ménage. Toute machine non annulée exécute la Tactique imprimée <code>T1..T6</code> sous la case. Dès qu'au moins 1 machine est annulée, le Rêve s'ouvre (allume <strong>5. Rêve</strong> ; <span class="dyn-span">\${c.Regle_Ouverture_Reve_Multiple === 'UNIQUE_PAR_TOUR' ? '<strong>max 1 ouverture par Rêve et par tour</strong>' : '<strong>mode cumulatif</strong>'}</span>) et avance vers la gauche (selon le mode d'avancée actif : saut/poussée <code>JUMP_PUSH</code> ou case immédiatement libre uniquement <code>FREE_SLOT_ONLY</code>).</li>`
  ],
  [
    `<h3 class="font-bold text-amber-950 text-sm mb-1.5">4.1. Piste des Gardiens (Pari d'activation 1 → 6 &amp; Anti-boucle 4. Résonance)</h3>`,
    `<h3 class="font-bold text-amber-950 text-sm mb-1.5">4.1. Piste des Gardiens (Pari unique 1 → 6 &amp; Anti-boucle 4. Gardien)</h3>`
  ],
  [
    `<strong>Compteur par 2<sup>es</sup> Défenseurs &amp; Anti-boucle 4. Résonance :</strong> terminez toujours l'effet en cours, puis parcourez les cases allumées de <strong>1 à 6</strong>. Chaque fois qu'un déclencheur s'allume sur une case occupée par un Gardien portant <code>≥ 1</code> Défenseur, retirez <strong>1 Défenseur</strong> (mis de côté jusqu'au ménage 6.2/6.3) et ouvrez immédiatement le Gardien. L'ouverture du Gardien placé sur <strong>4. Résonance</strong> ne ré-allume jamais <strong>4. Résonance</strong> elle-même. En <strong>5.3</strong> : tout pari gagné (<code>0</code> Défenseur restant) maintient le Gardien sur la piste (et retourne en Face 2 un Gardien double-face en Mode 4) ; tout pari perdu (<code>≥ 1</code> Défenseur non consommé) renvoie immédiatement le Gardien sur sa lisière d'origine (Face 1).`,
    `<strong>Pari unique par Défenseur &amp; Anti-boucle 4. Gardien :</strong> terminez toujours l'effet en cours, puis parcourez les cases allumées de <strong>1 à 6</strong>. Un Gardien construit (cases 1..6) ne peut recevoir au maximum qu'<strong>1 seul Défenseur</strong> en 2.2. Dès que son déclencheur s'allume, consommez ce <strong>Défenseur</strong> (mis de côté jusqu'au ménage 6.2) et ouvrez immédiatement le Gardien. L'ouverture du Gardien placé sur <strong>4. Gardien</strong> ne ré-allume jamais <strong>4. Gardien</strong> elle-même. En <strong>5.3</strong> : tout pari gagné (Défenseur consommé) maintient le Gardien sur la piste (et retourne en Face 2 un Gardien double-face en Mode 4) ; tout pari perdu (Défenseur non consommé) renvoie immédiatement le Gardien sur sa lisière d'origine (Face 1).`
  ],
  [
    `Gouverné par son <em>Peuple d'origine</em>. Activé en 2.2 par la pose d'un 2<sup>e</sup> Défenseur : en 3.2, chaque Défenseur dessus annule 1 machine pointant sur ce rang <code>M</code> et fait avancer le Rêve vers la première case libre à sa gauche (saut/poussée vers le bloc continu <code>1..k</code> du Sommeil).`,
    `Gouverné par son <em>Peuple d'origine</em>. Activé en 2.2 par la pose d'un Défenseur : en 3.2, chaque Défenseur dessus qui annule 1 machine pointant sur ce rang <code>M</code> est consommé (pari gagné), allume <strong>5. Rêve</strong> et fait avancer le Rêve vers la gauche (vers le bloc continu <code>1..k</code> du Sommeil).`
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
console.log('Synchronized 4 layers (spec_formelle, catalog, amazonia_data, livret) for v5.4.4 Mobilisation Croisée OK.');
