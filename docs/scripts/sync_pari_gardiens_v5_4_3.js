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

const NEW_A15 =
  "Test de fin de partie (5.3) : priorité absolue à Tour 8 (au Tour 8, la fin est toujours TOUR_8) ; sur les Tours 1..7, vérification directe après issue des paris Gardiens de Sommeil du Contremaître (toutes les tuiles Rêves en jeu en bloc continu à gauche cases 1..k de la Piste des Tactiques) ou d'Éveil de la Forêt (les N seconds Défenseurs de la table engagés sur la Piste des Gardiens en 2.2 et tous les paris gagnés : 0 Défenseur restant en 5.3). Passage direct à la Repousse Finale.";

const NEW_A22 =
  "Pari d'activation des Gardiens & Éveil de la Forêt (v5.4.3) : actif si >= 1 Peuple Animal Sauvage (M/R/O) est à la table. Plus aucun marqueur 'utilisé' sur les cases 1..6 : un Gardien sans 2e Défenseur est inactif ce tour-ci. En 2.2, tout 2e Défenseur peut être posé en pari sur un Gardien construit (cumul libre, plafond optionnel MAX_1_DEF sur 4. Résonance). À chaque déclencheur allumé sur une case portant >= 1 Défenseur, retirer 1 Défenseur (mis de côté jusqu'au ménage 6.2/6.3) et ouvrir le Gardien immédiatement. Anti-boucle 4. Résonance : l'ouverture du Gardien sur 4. Résonance ne ré-allume jamais 4. Résonance. En 5.3 : pari gagné (>=1 posé en 2.2 et 0 restant) -> le Gardien reste sur la piste (et passe Face 2 s'il est double-face en Mode 4) ; pari perdu (>=1 Défenseur non consommé) -> retour immédiat en lisière d'origine (Face 1). Si les N 2es Défenseurs ont tous été engagés sur la Piste des Gardiens en 2.2 et tous les paris sont gagnés (Tours 1..7), l'Éveil de la Forêt déclenche immédiatement la fin de partie.";

const NEW_ETAPE2_PARI =
  "2.2 Deuxième Défenseur (portée globale, activation Rêves & Pari d'activation des Gardiens) : pose en réflexion puis définitive partout sur le plateau, y compris sur un Rêve de la piste fixe (activation 3.2) ou en pari d'activation sur tout Gardien déjà construit (si >= 1 Animal Sauvage M/R/O ; cumul de plusieurs 2es Défenseurs autorisé, paramètre hors-châssis gardien_resonance_cap = UNLIMITED ou MAX_1_DEF sur 4. Résonance). Un Gardien sans 2e Défenseur reste inactif ce tour-ci.";

const NEW_ETAPE5_FIN =
  "Issue des paris Gardiens & Vérification de fin de partie (5.3) : retrait des Pièges déclenchés, puis résolution des paris Gardiens (pari gagné : >=1 Défenseur posé en 2.2 et 0 restant -> le Gardien reste en piste et passe Face 2 s'il est double-face en Mode 4 ; pari perdu : >=1 Défenseur restant -> retour immédiat en lisière d'origine Face 1). Test de fin de partie : priorité absolue au Tour 8 (fin TOUR_8) ; aux Tours 1..7, Sommeil du Contremaître (toutes les tuiles Rêves en jeu en bloc continu 1..k) ou Éveil de la Forêt (les N seconds Défenseurs engagés sur la Piste des Gardiens en 2.2 ET tous les paris gagnés, 0 Défenseur restant). Si atteint : passage direct à la Repousse Finale.";

const NEW_ETAPE6_REGLES = [
  "Ménage systématique (6.2) : piste des Tactiques T1..T6 fixe (aucun jeton ni déplacement de Tactique), retour en main de tous les Défenseurs (y compris ceux posés sur des Rêves ou Gardiens et ceux mis de côté après activation) et remise à zéro des modificateurs transitoires.",
  "Clôture du tour (6.3) : passage du pion Coordonnateur au siège suivant et remélange du paquet Machine (hors machines en Ratissage) avec toutes les cartes Sabotage (révélées/écartées ce tour + nouvellement acquises ce tour)."
];

const NEW_VERIF_FIN =
  "Vérification unique à la fin des attaques (5.3, après résolution des paris Gardiens, passage direct à la Repousse Finale). Priorité absolue au Tour 8 (CAUSE_TOUR_8). Aux Tours 1..7 : Sommeil du Contremaître (tous les Rêves en jeu en bloc continu cases 1..k de la Piste des Tactiques fixe T1..T6) ou Éveil de la Forêt (v5.4.3, actif si >= 1 Peuple Animal Sauvage M/R/O : les N seconds Défenseurs de la table engagés sur la Piste des Gardiens en 2.2 ET tous les paris gagnés, soit 0 Défenseur restant en 5.3).";

function patchSpecObj(spec) {
  spec.schema_version = '5.4.3';
  spec.arbitrages_valides.A15 = NEW_A15;
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

const v543Entry = {
  version: 'v5.4.3',
  date: 'Version en vigueur (2026-11-20)',
  titre: 'Pari d’activation des Gardiens & Éveil de la Forêt (symétrique de l’activation des Rêves)',
  resume:
    'Purge de l’ancien Réveil par unanimité/Face 2 et des marqueurs « utilisé » sur la Piste des Gardiens : les 2es Défenseurs posés en 2.2 sur un Gardien deviennent eux-mêmes son compteur d’activations restantes. Anti-boucle sur 4. Résonance (plafond hors-châssis UNLIMITED vs MAX_1_DEF). En 5.3 : pari gagné (reste en piste + passage Face 2 en Mode 4 si double-face), pari perdu (retour en lisière Face 1), priorité absolue à Tour 8, et Éveil de la Forêt aux Tours 1..7 si les N seconds Défenseurs étaient sur la Piste des Gardiens et que tous les paris sont gagnés.',
  deltas: [
    {
      domaine: 'Pari d’activation des Gardiens (Étape 2.2)',
      avant:
        'v5.4.2 : Marqueurs « utilisé » 1/tour sur cases 1..6, retournement Face 1 -> Face 2 universel à l’ouverture, engagement collectif sur 1 Gardien Face 2 avec retrait de la piste et condition 0 dommage réel.',
      apres:
        'v5.4.3 : Zéro marqueur « utilisé ». Un Gardien sans 2e Défenseur est inactif. En 2.2 (si >= 1 Animal Sauvage M/R/O), pose cumulable de 2es Défenseurs sur tout Gardien construit (paramètre hors-châssis gardien_resonance_cap = UNLIMITED ou MAX_1_DEF sur 4. Résonance). Chaque déclencheur retire 1 Défenseur et ouvre le Gardien ; l’ouverture sur 4. Résonance ne ré-allume jamais 4. Résonance.'
    },
    {
      domaine: 'Issue des paris & Éveil de la Forêt (Étape 5.3)',
      avant:
        'v5.4.2 : Test 0 dommage réel en 5.3 et résolution de l’échec en 6.3.',
      apres:
        'v5.4.3 : En 5.3, pari gagné (>=1 posé en 2.2 et 0 restant) -> le Gardien reste en piste (passage Face 2 en Mode 4 si double-face) ; pari perdu (>=1 Défenseur restant) -> retour immédiat en lisière d’origine Face 1. Priorité absolue à Tour 8 ; aux Tours 1..7, Éveil de la Forêt si les N seconds Défenseurs étaient sur la Piste des Gardiens et tous les paris sont gagnés.'
    }
  ]
};
exp.VERSION_CHANGELOG = [
  v543Entry,
  ...exp.VERSION_CHANGELOG.filter((entry) => entry.version !== 'v5.4.3')
];

const header = `// =========================================================================\n// data/amazonia_data_v5_4.js — Données canoniques Amazonia v5.4.3 (6 profils · 192 châssis · Piste T1..T6 fixe · Activation Rêves 2.2 · Pari Gardiens & Éveil)\n// =========================================================================\n`;
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
    `"cascades_gardiens": "Finir intégralement l'action ou le Nid en cours avant d'examiner la Piste des Gardiens. Marquage 'utilisé' immédiat dès l'ouverture ; balayage à plat des cases allumées de 1 à 6 (répété tant qu'une case allumée porte un Gardien disponible). Faces 2 autonomes (seule la face visible s'applique) ; Loi passive marquée automatiquement dès que sa case s'allume."`,
    `"cascades_gardiens": "Finir intégralement l'action ou le Nid en cours avant d'examiner la Piste des Gardiens. Plus aucun marqueur de disponibilité : les 2es Défenseurs posés sur un Gardien sont son compteur d'activations restantes (à 0, le Gardien est inactif). Balayage à plat des cases allumées de 1 à 6 ; anti-boucle 4. Résonance (l'ouverture du Gardien sur 4. Résonance ne ré-allume jamais 4. Résonance)."`
  ],
  [
    `"reveil_de_la_foret": "Actif uniquement si >= 1 Peuple Animal Sauvage (M, R ou O) est autour de la table. Tout Gardien ouvert sur sa Face 1 passe physiquement en Face 2 (« Éveillé », éligible au Réveil dès le tour suivant ; G14:C éligible sur Face 2 Rassasié). En 2.2 (2e Défenseur), engagement collectif au quota Q (défaut N) sur 1 Gardien Face 2 : tuile retirée de la piste (pouvoir/Loi inactifs ce tour, case libre dès 3.1). En 5.3, déclenchement immédiat du Réveil si 0 dommage réel subi ce tour ; sinon sort du Gardien résolu en 6.3 (retour lisière Face 1 ou retrait définitif)."`,
    `"reveil_de_la_foret": "Pari d'activation des Gardiens & Éveil de la Forêt (actif si >= 1 Peuple Animal Sauvage M, R ou O) : en 2.2, pose cumulable de 2es Défenseurs sur tout Gardien construit (0 Défenseur = inactif ; paramètre hors-châssis UNLIMITED ou MAX_1_DEF sur 4. Résonance). Chaque déclencheur retire 1 Défenseur et ouvre le Gardien immédiatement. En 5.3 : pari gagné (>=1 posé en 2.2 et 0 restant) -> reste en piste (Face 2 en Mode 4 si double-face) ; pari perdu (>=1 restant) -> retour immédiat en lisière d'origine Face 1. Aux Tours 1..7 (priorité à Tour 8), si les N 2es Défenseurs ont tous été engagés sur la Piste des Gardiens et tous les paris sont gagnés, l'Éveil de la Forêt déclenche immédiatement la fin de partie."`
  ],
  [
    `"2_defenseurs_et_furtivite_4_slots": "Anti-blocage : pose interdite sur Route Forestière, tuile construite/pleine/inconstructible, ou rive Furtivité bordant une Route (si parcelle requise). 1er Défenseur irrévocable sur sa Forêt ou ses 2 lisières ; puis 2e Défenseur global (réflexion -> définitif), pouvant aussi cibler : (a) un Rêve déjà présent sur la piste fixe pour l'activer en 3.2 (immobilisé jusqu'en 6.2), ou (b) 1 Gardien Face 2 pour le Réveil de la Forêt (si >= 1 Animal Sauvage M/R/O ; max 1 Gardien engagé/tour : si le quota Q est atteint en choix définitif, le Gardien est retiré de la piste et sa case 1..6 est immédiatement libre pour 3.1 ; sinon les Défenseurs orphelins restent sans effet). Case Furtivité = 4 emplacements (2 jumeaux rive J1, 2 jumeaux rive J2 ; max 2 Défenseurs). ENTRER sur la case (toute face) tire l'éventuel autre Défenseur sur l'emplacement jumeau du même bord ; RETOURNER de réflexion à définitif se fait strictement sur place sans déplacement.",`,
    `"2_defenseurs_et_furtivite_4_slots": "Anti-blocage : pose interdite sur Route Forestière, tuile construite/pleine/inconstructible, ou rive Furtivité bordant une Route (si parcelle requise). 1er Défenseur irrévocable sur sa Forêt ou ses 2 lisières ; puis 2e Défenseur global (réflexion -> définitif), pouvant aussi cibler : (a) un Rêve déjà présent sur la piste fixe pour l'activer en 3.2 (immobilisé jusqu'en 6.2), ou (b) un Gardien déjà construit sur la Piste des Gardiens en pari d'activation (si >= 1 Animal Sauvage M/R/O ; cumul autorisé, paramètre hors-châssis UNLIMITED ou MAX_1_DEF sur 4. Résonance ; 0 Défenseur = Gardien inactif ce tour). Case Furtivité = 4 emplacements (2 jumeaux rive J1, 2 jumeaux rive J2 ; max 2 Défenseurs). ENTRER sur la case (toute face) tire l'éventuel autre Défenseur sur l'emplacement jumeau du même bord ; RETOURNER de réflexion à définitif se fait strictement sur place sans déplacement.",`
  ],
  [
    `Fin 5.3 : effets fin d'attaques, retrait Pièges déclenchés, puis test Fin de Partie (Tour 8, Sommeil (toutes les tuiles Rêves en jeu en bloc continu à gauche 1..k), ou Réveil de la Forêt (Gardien Face 2 engagé au quota Q en 2.2 et 0 dommage réel subi ce tour) -> Repousse Finale directe sans Étape 6)."`,
    `Fin 5.3 : effets fin d'attaques, retrait Pièges déclenchés, résolution des paris Gardiens (gagné -> reste en piste + Face 2 en Mode 4 si double-face ; perdu -> retour lisière Face 1), puis test Fin de Partie (priorité Tour 8 ; aux Tours 1..7 : Sommeil (toutes les tuiles Rêves en jeu en bloc continu à gauche 1..k) ou Éveil de la Forêt (N 2es Défenseurs engagés sur la Piste des Gardiens et tous les paris gagnés) -> Repousse Finale directe sans Étape 6)."`
  ],
  [
    `<div><strong>Version :</strong> v5.4.1 (Réveil de la Forêt)</div>`,
    `<div><strong>Version :</strong> v5.4.3 (Pari d'activation des Gardiens &amp; Éveil de la Forêt)</div>`
  ],
  [
    `<li>• <strong>Réveil de la Forêt :</strong> <span class="dyn-span">\${reveilActif ? \`Actif (\${nbAnimauxSauvages} Peuple(s) Animal Sauvage M/R/O · quota Q = \${n} 2es Défenseurs en 2.2 sur 1 Gardien Face 2)\` : \`Inactif (aucun Peuple Animal Sauvage M/R/O autour de la table)\`}</span></li>`,
    `<li>• <strong>Pari Gardiens &amp; Éveil de la Forêt :</strong> <span class="dyn-span">\${reveilActif ? \`Actif (\${nbAnimauxSauvages} Peuple(s) Animal Sauvage M/R/O · \${n} 2es Défenseurs engagés sur la Piste des Gardiens et tous les paris gagnés aux Tours 1..7)\` : \`Inactif (aucun Peuple Animal Sauvage M/R/O autour de la table)\`}</span></li>`
  ],
  [
    `<li><strong>Réveil de la Forêt :</strong> <span class="dyn-span">\${reveilActif ? \`Un <strong>Gardien Face 2 (« Éveillé »)</strong> a été engagé pour le Réveil en fin d'Étape 2.2 (quota de <strong>\${n} Deuxièmes Défenseurs</strong> en choix définitif) <strong>ET aucun dommage réel</strong> n'a été infligé par les machines ce tour-ci (aucun Arbre coupé ni Souche retirée) en fin de 5.3.\` : \`<em>Condition inactive dans cette partie (aucun Peuple Animal Sauvage M/R/O autour de la table).</em>\`}</span></li>`,
    `<li><strong>Éveil de la Forêt (Tours 1 à 7) :</strong> <span class="dyn-span">\${reveilActif ? \`Les <strong>\${n} Deuxièmes Défenseurs</strong> de la table ont tous été engagés en <strong>pari d'activation</strong> sur la Piste des Gardiens en 2.2 (répartis librement sur un ou plusieurs Gardiens) <strong>ET tous les paris sont gagnés</strong> (<code>0</code> Défenseur restant sur la piste en 5.3 ; priorité absolue au Tour 8).\` : \`<em>Condition inactive dans cette partie (aucun Peuple Animal Sauvage M/R/O autour de la table).</em>\`}</span></li>`
  ],
  [
    `<strong>2<sup>e</sup> Défenseur (Portée globale, Activation de Rêve & Réveil de la Forêt) :</strong> Une fois tous les Premiers Défenseurs posés, chacun pose son Deuxième Défenseur partout sur le plateau (face <em>« en réflexion »</em> déplaçable d'une case à une autre, ou directement face <em>« définitive »</em>). Vous pouvez le poser sur un <strong>Rêve déjà présent sur la piste fixe</strong> pour l'activer en 3.2 (le Défenseur validé y reste immobilisé jusqu'au ménage de fin de tour). <span class="dyn-span">\${reveilActif ? \`Vous pouvez aussi cibler un <strong>Gardien déjà en Face 2 (« Éveillé »)</strong> sur la Piste des Gardiens pour tenter un <strong>Réveil</strong> (au maximum 1 seul Gardien engagé par tour). En fin de 2.2, une fois tous les 2<sup>es</sup> Défenseurs en choix définitif : si le quota de <strong>\${n} Défenseurs</strong> est atteint sur ce Gardien, sa tuile est immédiatement retirée de la piste (mise de côté avec ses Défenseurs jusqu'en 6.3, pouvoir/Loi inactifs ce tour, case <code>1..6</code> immédiatement libre pour 3.1) ; sinon les Défenseurs orphelins restent sans effet ce tour-ci.\` : ''}</span> Le passage se clôt quand tous sont sur leur face <em>« définitive »</em>.`,
    `<strong>2<sup>e</sup> Défenseur (Portée globale, Activation de Rêve &amp; Pari d'activation des Gardiens) :</strong> Une fois tous les Premiers Défenseurs posés, chacun pose son Deuxième Défenseur partout sur le plateau (face <em>« en réflexion »</em> déplaçable d'une case à une autre, ou directement face <em>« définitive »</em>). Vous pouvez le poser sur un <strong>Rêve déjà présent sur la piste fixe</strong> pour l'activer en 3.2 (le Défenseur validé y reste immobilisé jusqu'au ménage de fin de tour). <span class="dyn-span">\${reveilActif ? \`Vous pouvez aussi poser un <strong>pari d'activation</strong> sur tout <strong>Gardien déjà construit</strong> sur la Piste des Gardiens (plusieurs 2<sup>es</sup> Défenseurs peuvent se cumuler sur un même Gardien = autant d'activations potentielles ; un Gardien portant <code>0</code> Défenseur reste inactif ce tour-ci).\` : ''}</span> Le passage se clôt quand tous sont sur leur face <em>« définitive »</em>.`
  ],
  [
    `<strong>6.2–6.3. Ménage, Issue du Réveil échoué & Dilution permanente :</strong> La Piste des Tactiques <code>T1..T6</code> étant imprimée en dur, aucun déplacement de Tactique n'a lieu. Récupérez tous vos Défenseurs (y compris ceux immobilisés sur des Rêves ou Gardiens), retirez les marqueurs <em>« utilisé »</em> des Gardiens, résolvez le sort d'un éventuel Gardien engagé pour un Réveil échoué (retour en lisière d'origine Face 1 par défaut, ou retrait définitif selon la variante), et formez le paquet du tour suivant en remélangeant toutes les cartes Machine (hors machines en Ratissage) <strong>avec toutes les cartes Sabotage</strong> (celles révélées ou écartées ce tour-ci + toutes les nouvelles cartes Sabotage acquises ce tour-ci).`,
    `<strong>6.2–6.3. Ménage &amp; Dilution permanente :</strong> La Piste des Tactiques <code>T1..T6</code> étant imprimée en dur, aucun déplacement de Tactique n'a lieu. Récupérez tous vos Défenseurs (y compris ceux posés sur des Rêves ou Gardiens et ceux mis de côté après activation), et formez le paquet du tour suivant en remélangeant toutes les cartes Machine (hors machines en Ratissage) <strong>avec toutes les cartes Sabotage</strong> (celles révélées ou écartées ce tour-ci + toutes les nouvelles cartes Sabotage acquises ce tour-ci).`
  ],
  [
    `<h3 class="font-bold text-amber-950 text-sm mb-1.5">4.1. Piste des Gardiens (Cascades 1 → 6 & Éveil Face 2)</h3>`,
    `<h3 class="font-bold text-amber-950 text-sm mb-1.5">4.1. Piste des Gardiens (Pari d'activation 1 → 6 &amp; Anti-boucle 4. Résonance)</h3>`
  ],
  [
    `<strong>Balayage à plat & Éveil universel :</strong> terminez toujours l'effet en cours, marquez le Gardien <em>« utilisé »</em> dès son ouverture, puis parcourez les cases allumées de <strong>1 à 6</strong> (répété tant qu'une case allumée porte un Gardien disponible). Tout Gardien ouvert sur sa Face 1 passe physiquement en <strong>Face 2 (« Éveillé »)</strong> et devient éligible au <strong>Réveil de la Forêt</strong> dès le tour suivant <em>(G14:C est éligible lorsqu'il est sur sa Face 2 Rassasié)</em>. Seule la face visible s'applique ; une Loi passive reçoit automatiquement son marqueur dès que sa case s'allume.`,
    `<strong>Compteur par 2<sup>es</sup> Défenseurs &amp; Anti-boucle 4. Résonance :</strong> terminez toujours l'effet en cours, puis parcourez les cases allumées de <strong>1 à 6</strong>. Chaque fois qu'un déclencheur s'allume sur une case occupée par un Gardien portant <code>≥ 1</code> Défenseur, retirez <strong>1 Défenseur</strong> (mis de côté jusqu'au ménage 6.2/6.3) et ouvrez immédiatement le Gardien. L'ouverture du Gardien placé sur <strong>4. Résonance</strong> ne ré-allume jamais <strong>4. Résonance</strong> elle-même. En <strong>5.3</strong> : tout pari gagné (<code>0</code> Défenseur restant) maintient le Gardien sur la piste (et retourne en Face 2 un Gardien double-face en Mode 4) ; tout pari perdu (<code>≥ 1</code> Défenseur non consommé) renvoie immédiatement le Gardien sur sa lisière d'origine (Face 1).`
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
console.log('Synchronized 4 layers (spec_formelle, catalog, amazonia_data, livret) for v5.4.3 Pari Gardiens OK.');
