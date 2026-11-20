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
  "On résout toujours intégralement l'action ou la tuile en cours avant d'examiner la Piste des Gardiens (signal binaire allumé/éteint par case 1..6, sans cumul de cardinalité). Partition stricte des 6 déclencheurs (« 1 événement = au plus 1 déclencheur ») : en 3.2 (par carte révélée) 3. Sabotage > 6. Insecte (déviation Bug) > 5. Rêve (dé M sur rang Rêve, annulée ou non) ; en 4.1 Furtivité aucun déclencheur 2 ni 3 ; en 4.2 Nids -> 6. Insecte ; en 5.1/5.2 (par frappe bloquée) 2. Piégeage (Piège armé) > 6. Insecte (Parade classique avec dépense >= 1 Insecte) > 1. Parade (Défenseurs seuls). Case 4. Gardien (anti-boucle conservé) : DISTINCT_OPEN_1 (1re ouverture du tour de chaque autre Gardien distinct) ou DISTINCT_WON_2 (lorsque le 2e, puis 3e, autre Gardien distinct achève son pari). Zéro marqueur 'utilisé' : plafond uniforme UNIFORM_MAX_2 (max 2 Défenseurs par Gardien en 2.2). Balayage à plat de 1 à 6.";

const NEW_A14 =
  "Éveil de la Forêt 100 % Piste des Gardiens (v5.4.6) : actif uniquement si au moins 1 Peuple Animal Sauvage (M, R ou O) est autour de la table, aux Tours 1..7 (priorité absolue à Tour 8). En 5.3, la Forêt s'éveille si les N Défenseurs de la table ont tous été engagés en 2.2 sur la Piste des Gardiens et qu'aucun pari n'est perdu (0 Défenseur restant sur la Piste des Gardiens). Un Gardien sauvé par Bouclier de lisière (SLOT_COLONISATION_GARDIENS=B) reste en piste mais son pari reste PERDU (ne compte pas pour l'Éveil).";

const NEW_A15 =
  "Test de fin de partie (5.3) : priorité absolue à Tour 8 (au Tour 8, la fin est toujours TOUR_8) ; sur les Tours 1..7, vérification directe après issue des paris Gardiens (et Bouclier de lisière éventuel) de Sommeil du Contremaître (toutes les tuiles Rêves en jeu en bloc continu à gauche cases 1..k de la Piste des Tactiques) ou d'Éveil de la Forêt 100 % Gardiens (les N Défenseurs de la table engagés en 2.2 sur la Piste des Gardiens et 0 Défenseur restant en 5.3). Passage direct à la Repousse Finale.";

const NEW_A21 =
  "Activation et avancée des Rêves (v5.4.6) : en 2.2, un joueur peut poser son Défenseur sur un Rêve déjà présent sur la piste fixe T1..T6 (coût d'activation indépendant de l'Éveil). En 3.2 (Option A : 1_DEF_1_MACHINE), chaque Défenseur posé sur un Rêve annule 1 machine pointant sur ce rang M (en priorisant la plus menaçante) ; toute machine non annulée exécute la Tactique T1..T6 imprimée sous la case. Dès qu'au moins 1 machine est annulée, le Rêve s'ouvre et avance vers la gauche (par saut/poussée vers la 1re case libre à gauche) en mode CLEAR_RANK_ONLY uniquement si TOUTES les machines de ce rang M ont été annulées ce tour-ci. Déclencheur 5. Rêve (partition stricte 3.2) : s'allume pour chaque carte Machine non déviée par un Bug dont le dé retenu M pointe sur un rang occupé par un Rêve (que la machine soit annulée ou joue la Tactique dessous).";

const NEW_A22 =
  "Pari d'activation sur les Gardiens & Partition stricte des 6 déclencheurs (v5.4.6) : actif si >= 1 Peuple Animal Sauvage (M/R/O) est à la table. Plafond uniforme UNIFORM_MAX_2 (max 2 Défenseurs par Gardien construit cases 1..6 ; 0 = inactif). Partition stricte (« 1 événement = au plus 1 déclencheur ») : 3.2 (Sabotage > Insecte Bug > Rêve) ; 4.1 sans déclencheur 2/3 ; 4.2 Nids (6. Insecte) ; 5.1/5.2 (Piégeage > Insecte Parade >=1 Insecte > Parade Défenseurs seuls) ; 4. Gardien (anti-boucle conservé) selon gardien_4_trigger_mode (DISTINCT_OPEN_1 : 1re ouverture du tour de chaque autre Gardien distinct ; DISTINCT_WON_2 : 2e puis 3e autre Gardien distinct achevant son pari). En 5.3 : 0 Défenseur restant -> pari gagné (reste en piste, passe Face 2 en Mode 4 si double-face) ; >= 1 Défenseur restant -> pari perdu (retour en lisière Face 1, sauf Bouclier de lisière SLOT_COLONISATION_GARDIENS=B qui défausse 1 Insecte de la case pour garder la tuile sur sa face actuelle, le pari restant PERDU).";

const NEW_A24 =
  "Cartes Sabotage (dilution permanente, v5.4.6) : toutes identiques et sans effet propre (réserve illimitée). 1 Sabotage acquis en Furtivité 4.1 ajoute définitivement 1 carte Sabotage au paquet Machine en 6.3 (n'allume plus 3. Sabotage à l'acquisition) ; 1 carte Sabotage révélée à l'ouverture des paravents en 3.2 fait perdre 1 activation au Contremaître, allume 3. Sabotage (partition stricte 3.2), puis est remélangée en fin de tour.";

const NEW_ETAPE3_REV =
  "3.2 Révélation simultanée (paravents ouverts) — partition stricte « 1 carte révélée = au plus 1 déclencheur » : (a) 3. Sabotage si la carte révélée est un Sabotage ; (b) sinon 6. Insecte si un pion Insecte Bug (SLOT_BUG_CERVEAU=B) dévie le dé M de ±1 rang ; (c) sinon 5. Rêve si le dé retenu M d'une carte Machine pointe sur un rang occupé par une tuile Rêve (que la machine soit annulée par un Défenseur sur ce Rêve ou joue la Tactique imprimée dessous). Résolution des Rêves (Option A 1_DEF_1_MACHINE) : chaque Défenseur dessus annule 1 machine (en priorisant la plus menaçante) ; le Rêve avance vers la gauche (CLEAR_RANK_ONLY : uniquement si toutes les machines du rang M ont été annulées ce tour-ci).";

const NEW_ETAPE5_FIN =
  "Issue des paris Gardiens, Bouclier de lisière & Vérification de fin de partie (5.3) : retrait des Pièges déclenchés, puis résolution des paris Gardiens (0 Défenseur restant -> pari gagné, le Gardien reste en piste et passe Face 2 s'il est double-face en Mode 4 ; >= 1 Défenseur restant -> pari perdu : si SLOT_COLONISATION_GARDIENS=B et >= 1 Insecte sur sa case, défausser 1 Insecte pour empêcher le retour en lisière tout en gardant le pari PERDU et la face actuelle, sinon retour immédiat en lisière Face 1). Test de fin de partie : priorité absolue au Tour 8 (fin TOUR_8) ; aux Tours 1..7, Sommeil du Contremaître (toutes les tuiles Rêves en jeu en bloc continu 1..k) ou Éveil de la Forêt 100 % Piste des Gardiens (les N Défenseurs de la table engagés en 2.2 sur la Piste des Gardiens et 0 Défenseur restant en 5.3). Si atteint : passage direct à la Repousse Finale.";

const NEW_VERIF_FIN =
  "Vérification unique à la fin des attaques (5.3, après résolution des paris Gardiens et Bouclier de lisière éventuel, passage direct à la Repousse Finale). Priorité absolue au Tour 8 (CAUSE_TOUR_8). Aux Tours 1..7 : Sommeil du Contremaître (tous les Rêves en jeu en bloc continu cases 1..k de la Piste des Tactiques fixe T1..T6) ou Éveil de la Forêt 100 % Piste des Gardiens (v5.4.6, actif si >= 1 Peuple Animal Sauvage M/R/O : les N Défenseurs de la table engagés en 2.2 sur la Piste des Gardiens et 0 Défenseur restant en 5.3 ; un Gardien sauvé par Bouclier de lisière reste un pari perdu).";

const BOUCLIER_LISIERE_PROFILE = {
  nom: 'Bouclier de lisière',
  cycle: 'CONSOMME_ONESHOT',
  cablage: [1, 2, 3, 4, 5, 6],
  fenetre: '5.3 ISSUE PARIS GARDIENS',
  primitive: 'PARTAGE_INFO_ETAT_GARDIEN (PROTEGER_LISIERE)',
  tags: ['MIGRATION', 'PROTECTION'],
  requires_options: {},
  texte:
    "En 5.3, lorsqu'un Gardien perd son pari (≥ 1 Défenseur restant sur sa tuile), s'il y a au moins 1 jeton Insecte sur sa case de la Piste des Gardiens, défaussez 1 jeton Insecte de cette case pour empêcher le retour en lisière (le Gardien reste sur la piste sur sa face actuelle). Le pari reste toutefois considéré comme PERDU (ne compte pas pour l'Éveil de la Forêt et ne fait pas passer en Face 2).",
  temoin:
    'Protège la présence du Gardien sur la piste en cas de pari perdu, sans valider le pari pour l’Éveil ni déclencher Face 2.'
};

function patchSpecObj(spec) {
  spec.schema_version = '5.4.6';
  spec.date_consolidation = '2026-11-20';
  if (spec.principes_transverses) {
    spec.principes_transverses.cascades_gardiens_a_plat = NEW_CASCADES;
  }
  spec.arbitrages_valides.A14 = NEW_A14;
  spec.arbitrages_valides.A15 = NEW_A15;
  spec.arbitrages_valides.A21 = NEW_A21;
  spec.arbitrages_valides.A22 = NEW_A22;
  spec.arbitrages_valides.A24 = NEW_A24;
  for (const et of spec.etapes_tour || []) {
    if (et.numero === 3 && Array.isArray(et.regles)) {
      const filtered = et.regles.filter((r) => !String(r).startsWith('3.2 '));
      filtered.push(NEW_ETAPE3_REV);
      et.regles = filtered;
    } else if (et.numero === 5 && Array.isArray(et.regles)) {
      et.regles[et.regles.length - 1] = NEW_ETAPE5_FIN;
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

// Ajout du profil B (Bouclier de lisière) sur SLOT_COLONISATION_GARDIENS
if (exp.CATALOGUE_TUILES && exp.CATALOGUE_TUILES.SLOT_COLONISATION_GARDIENS) {
  const prevProfils = exp.CATALOGUE_TUILES.SLOT_COLONISATION_GARDIENS.profils || {};
  exp.CATALOGUE_TUILES.SLOT_COLONISATION_GARDIENS.profils = {
    A: prevProfils.A,
    B: BOUCLIER_LISIERE_PROFILE,
    C: prevProfils.C
  };
}

const v546Entry = {
  version: 'v5.4.6',
  date: 'Version en vigueur (2026-11-20)',
  titre: 'Partition stricte des 6 déclencheurs Gardiens & Bouclier de lisière (SLOT_COLONISATION_GARDIENS=B)',
  resume:
    'Recalibrage complet des 6 déclencheurs de la Piste des Gardiens selon la partition stricte « 1 événement = au plus 1 déclencheur » (3.2 : Sabotage > Insecte Bug > Rêve ; 5.1 : Piégeage > Insecte Parade > Parade Défenseurs seuls ; 4.1 Furtivité sans déclencheur 2/3), duel sur 4. Gardien (DISTINCT_OPEN_1 vs DISTINCT_WON_2), et ajout du profil B « Bouclier de lisière » sur SLOT_COLONISATION_GARDIENS.',
  deltas: [
    {
      domaine: 'Partition stricte 3.2 (Ouverture des paravents)',
      avant:
        'v5.4.5 : 3. Sabotage s’allumait en 4.1 Furtivité ; 5. Rêve ne s’allumait qu’à l’annulation d’une machine par un Défenseur sur un Rêve.',
      apres:
        'v5.4.6 : Au plus 1 déclencheur par carte révélée : 3. Sabotage (carte Sabotage révélée) > 6. Insecte (déviation Bug) > 5. Rêve (dé retenu M sur un rang occupé par un Rêve, annulée ou non).'
    },
    {
      domaine: 'Partition stricte 5.1 (Attaques des machines)',
      avant:
        'v5.4.5 : 2. Piégeage s’allumait à la pose en 4.1 ; toute parade (Piège, Insecte ou Défenseurs) allumait 1. Parade.',
      apres:
        'v5.4.6 : Au plus 1 déclencheur par frappe bloquée : 2. Piégeage (Piège armé) > 6. Insecte (Parade classique défaussant >= 1 Insecte) > 1. Parade (Défenseurs seuls sans Piège ni Insecte).'
    },
    {
      domaine: 'Case 4. Gardien & Bouclier de lisière (SLOT_COLONISATION_GARDIENS=B)',
      avant:
        'v5.4.5 : Chaque ouverture d’un autre Gardien allumait 4. Gardien ; tout pari perdu renvoyait le Gardien en lisière.',
      apres:
        'v5.4.6 : Duel DISTINCT_OPEN_1 (1re ouverture du tour de chaque autre Gardien distinct) vs DISTINCT_WON_2 (2e puis 3e autre Gardien distinct achevant son pari). Nouveau profil B Bouclier de lisière : en 5.3 sur pari perdu, défausser 1 Insecte de la case empêche le retour en lisière (le pari reste PERDU).'
    }
  ]
};
exp.VERSION_CHANGELOG = [
  v546Entry,
  ...exp.VERSION_CHANGELOG.filter((entry) => entry.version !== 'v5.4.6')
];

const header = `// =========================================================================\n// data/amazonia_data_v5_4.js — Données canoniques Amazonia v5.4.6 (6 profils · 192 châssis · Partition stricte 6 déclencheurs · Bouclier de lisière · Éveil 100 % Gardiens · Rêves CLEAR_RANK_ONLY)\n// =========================================================================\n`;
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
    `"cascades_gardiens": "Finir intégralement l'action ou le Nid en cours avant d'examiner la Piste des Gardiens. Zéro marqueur de disponibilité : chaque Gardien construit (cases 1..6) peut recevoir au maximum 2 Défenseurs en 2.2 (0 = inactif, 1 = 1 déclenchement attendu, 2 = 2 déclenchements attendus ; variante MAX_2_RES_MAX_1 plafonnant 4. Gardien à 1 Défenseur max). Balayage à plat des cases allumées de 1 à 6 ; anti-boucle 4. Gardien (l'ouverture du Gardien sur 4. Gardien ne ré-allume jamais 4. Gardien)."`,
    `"cascades_gardiens": "Finir intégralement l'action ou le Nid en cours avant d'examiner la Piste des Gardiens. Partition stricte des 6 déclencheurs (1 événement = au plus 1 déclencheur) : 3.2 (3. Sabotage > 6. Insecte Bug > 5. Rêve) ; 4.1 sans déclencheur 2/3 ; 4.2 Nids (6. Insecte) ; 5.1/5.2 (2. Piégeage > 6. Insecte Parade >=1 Insecte > 1. Parade Défenseurs seuls) ; 4. Gardien (anti-boucle conservé : DISTINCT_OPEN_1 ou DISTINCT_WON_2). Plafond uniforme UNIFORM_MAX_2 (max 2 Défenseurs par Gardien en 2.2). Balayage à plat de 1 à 6."`
  ],
  [
    `"reveil_de_la_foret": "Pari Gardiens (max 2 Défenseurs) & Éveil 100 % Gardiens (actif si >= 1 Peuple Animal Sauvage M, R ou O) : en 2.2, chaque Gardien construit (cases 1..6) peut recevoir au maximum 2 Défenseurs (0 = inactif, 1 = 1 déclenchement attendu, 2 = 2 déclenchements attendus ; UNIFORM_MAX_2 ou MAX_2_RES_MAX_1 sur 4. Gardien). Chaque déclenchement consomme 1 Défenseur et ouvre le Gardien. En 5.3 : 0 Défenseur restant -> pari gagné (reste en piste, Face 2 en Mode 4 si double-face) ; >= 1 Défenseur restant -> pari perdu (retour immédiat en lisière Face 1). Aux Tours 1..7 (priorité Tour 8), si les N Défenseurs de la table ont tous été engagés en 2.2 sur la Piste des Gardiens et qu'aucun pari n'est perdu (0 Défenseur restant), la Forêt s'éveille."`,
    `"reveil_de_la_foret": "Pari Gardiens (max 2 Défenseurs, UNIFORM_MAX_2) & Éveil 100 % Gardiens (actif si >= 1 Peuple Animal Sauvage M, R ou O) : en 2.2, chaque Gardien construit (cases 1..6) peut recevoir au maximum 2 Défenseurs. Chaque déclenchement consomme 1 Défenseur et ouvre le Gardien. En 5.3 : 0 Défenseur restant -> pari gagné (reste en piste, Face 2 en Mode 4 si double-face) ; >= 1 Défenseur restant -> pari perdu (Bouclier de lisière SLOT_COLONISATION_GARDIENS=B : défausser 1 Insecte de la case empêche le retour en lisière tout en gardant le pari PERDU et la face actuelle ; sinon retour en lisière Face 1). Aux Tours 1..7 (priorité Tour 8), si les N Défenseurs de la table ont tous été engagés en 2.2 sur la Piste des Gardiens et qu'aucun pari n'est perdu (0 Défenseur restant), la Forêt s'éveille."`
  ],
  [
    `"3_2_revelation_et_sabotages": "Ouverture simultanée des paravents ; fin du silence. Toute carte Sabotage révélée est simplement mise de côté (action du Contremaître perdue ce tour) pour être remélangée dans le paquet en 6.3. Déviations Bug (SLOT_BUG_CERVEAU profil B par défaut : défausser 1 Bug du rang M pour décaler M de ±1). Rêve sur le rang M : chaque Défenseur posé dessus en 2.2 annule 1 machine (Option A : 1_DEF_1_MACHINE, en priorisant la plus menaçante) ; toute machine non annulée exécute la Tactique imprimée T1..T6 sous le Rêve. Dès >=1 machine annulée, le Rêve s'ouvre toujours (allume 5. Rêve) et avance par saut/poussée vers la 1re case libre à gauche selon reve_advance_mode (JUMP_PUSH : avance dès >=1 machine annulée ; CLEAR_RANK_ONLY : avance uniquement si toutes les machines du rang M ont été annulées ce tour-ci).",`,
    `"3_2_revelation_et_sabotages": "Ouverture simultanée des paravents ; fin du silence. Partition stricte 3.2 (au plus 1 déclencheur par carte révélée) : (1) carte Sabotage révélée -> allume 3. Sabotage (mise de côté puis remélangée en 6.3) ; (2) sinon déviation Bug (SLOT_BUG_CERVEAU=B : défausser 1 Bug du rang M pour décaler M de ±1) -> allume 6. Insecte ; (3) sinon dé retenu M d'une carte Machine pointant sur un rang occupé par un Rêve -> allume 5. Rêve (que la machine soit annulée ou joue la Tactique dessous). Activation Rêve (Option A : 1_DEF_1_MACHINE) : chaque Défenseur dessus annule 1 machine (priorité plus menaçante) ; avancée CLEAR_RANK_ONLY si toutes les machines du rang M sont annulées.",`
  ],
  [
    `<div><strong>Version :</strong> v5.4.5 (Éveil 100 % Gardiens, Pari Gardiens max 2 &amp; Rêves CLEAR_RANK_ONLY)</div>`,
    `<div><strong>Version :</strong> v5.4.6 (Partition stricte 6 déclencheurs Gardiens &amp; Bouclier de lisière)</div>`
  ],
  [
    `<li><strong>Fin du silence & Cartes Sabotage révélées :</strong> toute carte <strong>Sabotage</strong> révélée derrière un paravent fait simplement perdre une activation au Contremaître ce tour-ci ! Mettez-la de côté près du paquet Machine : elle y sera remélangée en 6.3.</li>`,
    `<li><strong>Fin du silence &amp; Partition stricte 3.2 (au plus 1 déclencheur par carte révélée) :</strong> (1) toute carte <strong>Sabotage</strong> révélée fait perdre une activation au Contremaître ce tour-ci, allume <strong>3. Sabotage</strong> et est mise de côté pour 6.3 ; (2) sinon, si un pion Insecte <em>Bug</em> (<code>SLOT_BUG_CERVEAU=B</code>) dévie le dé d'une carte Machine, allume <strong>6. Insecte</strong> ; (3) sinon, si le dé retenu <code>M</code> d'une carte Machine pointe sur un rang occupé par une tuile Rêve, allume <strong>5. Rêve</strong> (que la machine soit annulée ou joue la Tactique dessous).</li>`
  ],
  [
    `<li><strong>Rêves (dé M désignant un Rêve) :</strong> chaque Défenseur posé sur ce Rêve en 2.2 <strong>annule 1 carte Machine</strong> pointant sur ce rang <code>M</code> (en priorisant la plus menaçante). Toute machine non annulée exécute la Tactique imprimée <code>T1..T6</code> sous la case. Dès qu'au moins 1 machine est annulée, le Rêve s'ouvre toujours (allume <strong>5. Rêve</strong> ; <span class="dyn-span">\${c.Regle_Ouverture_Reve_Multiple === 'UNIQUE_PAR_TOUR' ? '<strong>max 1 ouverture par Rêve et par tour</strong>' : '<strong>mode cumulatif</strong>'}</span>) et avance vers la gauche par saut/poussée vers la 1<sup>re</sup> case libre à gauche selon le mode actif (<code>JUMP_PUSH</code> : avance dès ≥ 1 machine annulée ; <code>CLEAR_RANK_ONLY</code> : avance uniquement si <strong>toutes</strong> les machines de ce rang <code>M</code> ont été annulées ce tour-ci, sinon reste sur sa case).</li>`,
    `<li><strong>Rêves (dé M désignant un Rêve) :</strong> chaque Défenseur posé sur ce Rêve en 2.2 <strong>annule 1 carte Machine</strong> pointant sur ce rang <code>M</code> (en priorisant la plus menaçante). Toute machine non annulée exécute la Tactique imprimée <code>T1..T6</code> sous la case. Dès qu'au moins 1 machine est annulée, le Rêve s'ouvre (<span class="dyn-span">\${c.Regle_Ouverture_Reve_Multiple === 'UNIQUE_PAR_TOUR' ? '<strong>max 1 ouverture par Rêve et par tour</strong>' : '<strong>mode cumulatif</strong>'}</span>) et avance vers la gauche par saut/poussée vers la 1<sup>re</sup> case libre à gauche en mode <code>CLEAR_RANK_ONLY</code> uniquement si <strong>toutes</strong> les machines de ce rang <code>M</code> ont été annulées ce tour-ci (sinon reste sur sa case).</li>`
  ],
  [
    `<li><strong>Préparer un Piège :</strong> s'il n'y a <strong>aucune machine physiquement présente</strong> sur cette parcelle (même ciblée à distance), posez-y 1 jeton Piège (max 1/parcelle ; allume <em>2. Piégeage</em>).</li>`,
    `<li><strong>Préparer un Piège :</strong> s'il n'y a <strong>aucune machine physiquement présente</strong> sur cette parcelle (même ciblée à distance), posez-y 1 jeton Piège (max 1/parcelle ; n'allume plus <em>2. Piégeage</em> en 4.1).</li>`
  ],
  [
    `<li><strong>Saboter le chantier :</strong> s'il y a <strong>au moins 1 machine présente mais aucune active ce tour-ci</strong> (une machine en Ratissage est active), prenez <strong>1 carte Sabotage</strong> de la réserve et mettez-la de côté pour l'intégrer <strong>définitivement</strong> au paquet Machine en 6.3 (allume <em>3. Sabotage</em>).</li>`,
    `<li><strong>Saboter le chantier :</strong> s'il y a <strong>au moins 1 machine présente mais aucune active ce tour-ci</strong> (une machine en Ratissage est active), prenez <strong>1 carte Sabotage</strong> de la réserve et mettez-la de côté pour l'intégrer <strong>définitivement</strong> au paquet Machine en 6.3 (n'allume plus <em>3. Sabotage</em> en 4.1).</li>`
  ],
  [
    `<li><strong>Chaîne stricte des parades à chaque frappe :</strong> <strong>1° Bond du Jaguar</strong> (Loi auto : 2 bleus défaussés → pare toutes les frappes restantes de la machine + recul) → <strong>2° Piquée de la Harpie</strong> → <strong>3° Piège (Embuscade)</strong> si la parcelle a un Piège <strong>ET une Défense totale ≥ 1</strong> à cet instant (locale ou soutenue à distance ; allume <em>1. Parade</em>, le Piège reste actif pour ce tour et sera retiré en 5.4) → <strong>4° Parade classique</strong> si Défense (Défenseurs + Insectes) ≥ Seuil, en <strong>défaussant immédiatement</strong> les Insectes nécessaires pour atteindre le Seuil (allume <em>1. Parade</em>).</li>`,
    `<li><strong>Chaîne stricte des parades &amp; partition 5.1 (au plus 1 déclencheur par frappe bloquée) :</strong> <strong>1° Bond du Jaguar</strong> → <strong>2° Piquée de la Harpie</strong> → <strong>3° Piège (Embuscade)</strong> si la parcelle a un Piège <strong>ET une Défense totale ≥ 1</strong> à cet instant (allume uniquement <strong>2. Piégeage</strong>, le Piège reste actif pour ce tour et sera retiré en 5.3) → <strong>4° Parade classique</strong> si Défense (Défenseurs + Insectes) ≥ Seuil : si ≥ 1 Insecte est défaussé pour atteindre le Seuil, allume uniquement <strong>6. Insecte</strong> ; sinon (Défenseurs seuls, sans Piège ni Insecte), allume uniquement <strong>1. Parade</strong>.</li>`
  ],
  [
    `<strong>Pari par Défenseur (max 2) &amp; Anti-boucle 4. Gardien :</strong> terminez toujours l'effet en cours, puis parcourez les cases allumées de <strong>1 à 6</strong>. Chaque Gardien construit (cases 1..6) peut recevoir au maximum <strong>2 Défenseurs</strong> en 2.2 (<code>0</code> = inactif, <code>1</code> = 1 déclenchement attendu, <code>2</code> = 2 déclenchements attendus ; variante <code>MAX_2_RES_MAX_1</code> plafonnant <strong>4. Gardien</strong> à 1 Défenseur max). Chaque déclenchement de la case consomme <strong>1 Défenseur</strong> (mis de côté jusqu'au ménage 6.2) et ouvre immédiatement le Gardien. L'ouverture du Gardien placé sur <strong>4. Gardien</strong> ne ré-allume jamais <strong>4. Gardien</strong> elle-même. En <strong>5.3</strong> : <code>0</code> Défenseur restant → pari gagné (le Gardien reste en piste et passe Face 2 en Mode 4 si double-face) ; <code>≥ 1</code> Défenseur restant → pari perdu (retour immédiat sur sa lisière d'origine Face 1).`,
    `<strong>Pari par Défenseur (UNIFORM_MAX_2) &amp; Partition stricte 1 → 6 :</strong> terminez toujours l'effet en cours, puis parcourez les cases allumées de <strong>1 à 6</strong>. Chaque Gardien construit (cases 1..6) peut recevoir au maximum <strong>2 Défenseurs</strong> en 2.2. Chaque déclenchement consomme <strong>1 Défenseur</strong> et ouvre le Gardien. Case <strong>4. Gardien</strong> (anti-boucle conservé) : <code>DISTINCT_OPEN_1</code> (1<sup>re</sup> ouverture du tour de chaque autre Gardien distinct) ou <code>DISTINCT_WON_2</code> (2<sup>e</sup> puis 3<sup>e</sup> autre Gardien distinct achevant son pari). En <strong>5.3</strong> : <code>0</code> Défenseur restant → pari gagné (reste en piste, Face 2 en Mode 4 si double-face) ; <code>≥ 1</code> Défenseur restant → pari perdu (<strong>Bouclier de lisière</strong> <code>SLOT_COLONISATION_GARDIENS=B</code> : défausser 1 Insecte de la case empêche le retour en lisière tout en gardant le pari PERDU ; sinon retour en lisière Face 1).`
  ],
  [
    `Gouverné par son <em>Peuple d'origine</em>. Activé en 2.2 par la pose d'un Défenseur (coût d'activation hors Éveil) : en 3.2, chaque Défenseur dessus annule 1 machine pointant sur ce rang <code>M</code>, ouvre toujours le Rêve (allume <strong>5. Rêve</strong>) et le fait avancer vers la gauche (selon <code>JUMP_PUSH</code> ou <code>CLEAR_RANK_ONLY</code>, vers le bloc continu <code>1..k</code> du Sommeil).`,
    `Gouverné par son <em>Peuple d'origine</em>. Activé en 2.2 par la pose d'un Défenseur (coût d'activation hors Éveil) : en 3.2, chaque Défenseur dessus annule 1 machine pointant sur ce rang <code>M</code> et fait avancer le Rêve vers la gauche en mode <code>CLEAR_RANK_ONLY</code> (uniquement si toutes les machines du rang sont annulées). Tout dé retenu <code>M</code> non dévié par un Bug pointant sur ce rang allume <strong>5. Rêve</strong>.`
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
console.log('Synchronized 4 layers (spec_formelle, catalog, amazonia_data, livret) for v5.4.6 OK.');
