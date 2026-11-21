'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..', '..');
const DOCS_DATA = path.join(ROOT, 'docs', 'data');

const SRC_SPEC = path.join(DOCS_DATA, 'spec_formelle_v5_4.json');
const SRC_CAT = path.join(DOCS_DATA, 'catalog_v5_4.json');
const SRC_JS = path.join(DOCS_DATA, 'amazonia_data_v5_4.js');

const DST_SPEC = path.join(DOCS_DATA, 'spec_formelle_v5_5.json');
const DST_CAT = path.join(DOCS_DATA, 'catalog_v5_5.json');
const DST_JS = path.join(DOCS_DATA, 'amazonia_data_v5_5.js');

function writeUtf8Lf(filePath, content) {
  const normalized = content.replace(/\r\n/g, '\n');
  fs.writeFileSync(filePath, normalized, { encoding: 'utf8' });
}

// 1. Load source data cleanly via JSON.parse & Node vm
const spec = JSON.parse(fs.readFileSync(SRC_SPEC, 'utf8'));
const catalog = JSON.parse(fs.readFileSync(SRC_CAT, 'utf8'));
const jsSrc = fs.readFileSync(SRC_JS, 'utf8');

const sandbox = { window: {} };
vm.createContext(sandbox);
const extracted = vm.runInContext(
  jsSrc +
    '\n;({ PEUPLES, MATRICE_PAIRES, TOPOLOGIES_PISTE_SPEC, CHASSIS_AXES_SPEC, CATALOGUE_TUILES, VERSION_CHANGELOG });',
  sandbox
);

// 2. Build spec_formelle_v5_5.json (schema_version 5.5.0, all rules consolidated & aligned)
spec.schema_version = '5.5.0';
spec.date_consolidation = '2026-11-20';

spec.principes_transverses.cascades_gardiens_a_plat =
  "On résout toujours intégralement l'action ou la tuile en cours avant d'examiner la Piste des Gardiens (signal binaire allumé/éteint par case 1..6, sans cumul de cardinalité). Partition stricte des 6 déclencheurs (« 1 événement = au plus 1 déclencheur ») : en 3.2 (par carte révélée) 3. Sabotage > 6. Insecte (déviation sur Tactiques) > 5. Rêve (dé M sur rang Rêve, annulée ou non) ; en 4.1 Furtivité et en 4.2 production de Nid aucun déclencheur n'est allumé ; en 5.1/5.2 (par frappe bloquée) 2. Piégeage (Piège armé) > 6. Insecte (Parade classique avec dépense >= 1 Insecte) > 1. Parade (Défenseurs seuls). Case 4. Gardien : 1re ouverture du tour de chaque autre Gardien distinct (anti-boucle conservé). Pari uniforme de 0, 1 ou 2 Défenseurs maximum par Gardien construit en 2.2 (glissés sous la tuile à chaque déclenchement). Balayage à plat de 1 à 6.";

// Align Etape 2, 3, 4, 5, 6 in spec_formelle
for (const step of spec.etapes_tour) {
  if (step.numero === 2) {
    step.regles[2] =
      "2.2 Portée globale, Activation des Rêves & Pari sur les Gardiens : pose en réflexion puis définitive partout sur le plateau, y compris sur un Rêve de la Piste des Tactiques fixe (coût d'activation en 3.2 : 1 Défenseur annule 1 machine) ou en pari d'activation sur tout Gardien déjà construit (si >= 1 Animal Sauvage M/R/O ; 0, 1 ou 2 Défenseurs maximum par Gardien, glissés sous la tuile à chaque déclenchement). Un Gardien sans Défenseur reste inactif ce tour-ci.";
  } else if (step.numero === 3) {
    step.regles[4] =
      "3.2 Révélation simultanée (paravents ouverts) — partition stricte « 1 carte révélée = au plus 1 déclencheur » : (a) 3. Sabotage si la carte révélée est un Sabotage ; (b) sinon 6. Insecte si un pion Insecte de la Piste des Tactiques (SLOT_BUG_CERVEAU=B) dévie le dé M de ±1 rang ; (c) sinon 5. Rêve si le dé retenu M d'une carte Machine pointe sur un rang occupé par une tuile Rêve (que la machine soit annulée par un Défenseur sur ce Rêve ou joue la Tactique imprimée dessous). Résolution des Rêves (1_DEF_1_MACHINE) : chaque Défenseur dessus annule 1 machine (en priorisant la plus menaçante) ; le Rêve avance vers la gauche (CLEAR_RANK_ONLY) uniquement si toutes les machines du rang M ont été annulées ce tour-ci.";
  } else if (step.numero === 4) {
    step.regles[0] =
      "4.1 Furtivité : chaque binôme complet sur une case de Furtivité (2 Défenseurs sur la même rive, ou 1 Défenseur + 1 Insecte défaussé) déclenche 1 seule action, gouvernée par le joueur de la rive occupée — Piège si aucune machine présente OU Sabotage si au moins 1 machine présente et aucune active ce tour (Ratissage = active ; une machine annulée par un Rêve en 3.2 est inactive et donc sabotable). La pose d'un Piège ou l'acquisition d'un Sabotage en 4.1 n'allume aucun déclencheur Gardien.";
    step.regles[1] =
      "4.2 Production des Nids : chaque Nid actif est résolu comme un bloc indivisible : (1) création de 1 ou 2 Insectes selon le nombre d'Insectes physiquement présents sur sa parcelle à cet instant précis (sans allumer le déclencheur 6. Insecte), puis (2) pouvoir 'après production' du Nid, puis seulement (3) balayage 1..6 des Gardiens.";
  } else if (step.numero === 5) {
    step.regles[6] =
      "Issue des paris Gardiens, Bouclier de lisière & Vérification de fin de partie (5.3) : retrait des Pièges déclenchés, puis résolution des paris Gardiens (0 Défenseur restant -> pari gagné : le Gardien reste en piste et passe Face 2 s'il est double-face ; >= 1 Défenseur restant -> pari perdu : si Bouclier de lisière SLOT_COLONISATION_GARDIENS=B et >= 1 Insecte sur sa case, défausser 1 Insecte pour garder le Gardien en piste sur sa face actuelle tout en laissant le pari PERDU, sinon retour immédiat en lisière Face 1). Test de fin de partie : priorité absolue au Tour 8 ; aux Tours 1..7, Sommeil du Contremaître (toutes les tuiles Rêves en jeu en bloc continu 1..k) ou Réveil de la Forêt 100 % Piste des Gardiens (les N Défenseurs de la table engagés en 2.2 sur les Gardiens et aucun pari perdu). Si atteint : passage direct à la Repousse Finale.";
  }
}

spec.arbitrages_valides.A11 =
  "Piste des Tactiques fixe (T1..T6 imprimées en dur) et placement des Rêves (v5.5) : aucune Tactique mobile ni éjection de Tactique. Un Rêve construit en 3.1 se pose par-dessus la case libre la plus à droite (6, puis 5, etc.). Les Insectes sur la Piste des Tactiques restent sur leur numéro de case imprimé.";
spec.arbitrages_valides.A14 =
  "Éveil / Réveil de la Forêt 100 % Piste des Gardiens (v5.5) : actif uniquement si >= 1 Peuple Animal Sauvage (M, R ou O) est autour de la table, aux Tours 1..7 (priorité absolue au Tour 8). En 5.3, la Forêt s'éveille si les N Défenseurs de la table ont tous été engagés en 2.2 sur la Piste des Gardiens et qu'aucun pari n'est perdu (0 Défenseur restant). Un Gardien sauvé par Bouclier de lisière (SLOT_COLONISATION_GARDIENS=B) reste en piste sur sa face actuelle mais son pari reste PERDU (ne compte pas pour le Réveil).";
spec.arbitrages_valides.A15 =
  "Test de fin de partie (5.3, v5.5) : priorité absolue au Tour 8 (fin TOUR_8) ; aux Tours 1..7, vérification directe après issue des paris Gardiens (et Bouclier de lisière éventuel) de Sommeil du Contremaître (toutes les tuiles Rêves en jeu en bloc continu cases 1..k) ou de Réveil de la Forêt 100 % Piste des Gardiens (tous les N Défenseurs engagés en 2.2 sur les Gardiens et aucun pari perdu). Passage direct à la Repousse Finale.";
spec.arbitrages_valides.A21 =
  "Activation et avancée des Rêves (v5.5) : en 2.2, un joueur peut poser son Défenseur sur un Rêve de la Piste des Tactiques fixe. En 3.2 (1_DEF_1_MACHINE), 1 Défenseur annule 1 machine pointant sur ce rang M (priorité à la plus menaçante) ; toute machine non annulée exécute la Tactique T1..T6 imprimée dessous. Le Rêve s'ouvre dès qu'au moins 1 machine est annulée et avance vers la gauche (CLEAR_RANK_ONLY) uniquement si toutes les machines du rang M sont annulées ce tour-ci. Déclencheur 5. Rêve (partition stricte 3.2) : s'allume pour chaque carte Machine non déviée par un Insecte dont le dé retenu M pointe sur un rang occupé par un Rêve.";
spec.arbitrages_valides.A22 =
  "Pari uniforme sur les Gardiens & Partition stricte des 6 déclencheurs (v5.5) : actif si >= 1 Animal Sauvage (M/R/O) est à la table. Pari uniforme UNIFORM_MAX_2 (0, 1 ou 2 Défenseurs maximum par Gardien construit cases 1..6, glissés sous la tuile à chaque déclenchement). Partition stricte (« 1 événement = au plus 1 déclencheur ») : en 3.2 Sabotage > Insecte sur Tactiques > Rêve ; en 4.1 et 4.2 Nids aucun déclencheur ; en 5.1/5.2 Piégeage > Insecte en Parade >= 1 Insecte > Parade par Défenseurs seuls ; 4. Gardien sur 1re ouverture du tour de chaque autre Gardien distinct (DISTINCT_OPEN_1, anti-boucle conservé). En 5.3 : pari gagné -> reste en piste et passe Face 2 si double-face ; pari perdu -> retour en lisière Face 1, sauf Bouclier de lisière (SLOT_COLONISATION_GARDIENS=B) qui défausse 1 Insecte de la case pour garder le Gardien en piste sur sa face actuelle, le pari restant PERDU.";
spec.arbitrages_valides.A23 =
  "Piste des Tactiques fixe & Déviation par Insectes (v5.5) : piste T1..T6 imprimée en dur sans jeton ni déplacement de Tactiques en Étape 6. SLOT_BUG_CERVEAU=B (Déviation Synaptique ±1 rang en 3.2) et SLOT_COLONISATION_GARDIENS=B (Bouclier de lisière en 5.3) sont actifs par défaut.";
spec.arbitrages_valides.A24 =
  "Cartes Sabotage (dilution permanente, v5.5) : toutes identiques et sans effet propre (réserve illimitée). 1 Sabotage acquis en Furtivité 4.1 est mis de côté pour rejoindre définitivement le paquet Machine en 6.3 (sans allumer 3. Sabotage) ; 1 carte Sabotage révélée à l'ouverture des paravents en 3.2 fait perdre 1 activation au Contremaître, allume 3. Sabotage (partition stricte 3.2), puis est remélangée en fin de tour.";

writeUtf8Lf(DST_SPEC, JSON.stringify(spec, null, 2) + '\n');

// 3. Build catalog_v5_5.json
const catOut = {
  schema_version: '5.5.0',
  total_emplacements: catalog.total_emplacements,
  total_profils: catalog.total_profils,
  topologies: catalog.topologies,
  formule_seuil_parade: catalog.formule_seuil_parade,
  verification_fin_de_partie:
    "Vérification unique à la fin des attaques (5.3, après résolution des paris Gardiens et Bouclier de lisière éventuel, passage direct à la Repousse Finale). Priorité absolue au Tour 8 (CAUSE_TOUR_8). Aux Tours 1..7 : Sommeil du Contremaître (tous les Rêves en jeu en bloc continu cases 1..k de la Piste des Tactiques fixe T1..T6) ou Réveil de la Forêt 100 % Piste des Gardiens (v5.5, actif si >= 1 Peuple Animal Sauvage M/R/O : les N Défenseurs de la table engagés en 2.2 sur la Piste des Gardiens et aucun pari perdu ; un Gardien sauvé par Bouclier de lisière reste un pari perdu).",
  regle_piege: catalog.regle_piege,
  furtivite_4_1_autorise_ciblee_sans_machine: catalog.furtivite_4_1_autorise_ciblee_sans_machine,
  verrouillage_etape_5_parcelles_ciblees: catalog.verrouillage_etape_5_parcelles_ciblees,
  bonus_constructeur_n3: catalog.bonus_constructeur_n3,
  regle_furtivite: catalog.regle_furtivite,
  gouvernance_autorite: catalog.gouvernance_autorite,
  date_consolidation: '2026-11-20',
  spec_formelle: spec,
  spec_formelle_v5_5: spec,
};
writeUtf8Lf(DST_CAT, JSON.stringify(catOut, null, 2) + '\n');

// 4. Patch CATALOGUE_TUILES active STANDARD_A texts for v5.5 strict trigger partition & pari compatibility
const catTiles = extracted.CATALOGUE_TUILES;

catTiles.G4.profils.A.texte =
  "<strong>Face 1 (Ouverture) :</strong> Réduisez de −1 le Seuil de Parade sur une parcelle des rayons O ou M pour le reste du tour.<br><strong>Sacrifice (en 3.2 après révélation) :</strong> Déplacez jusqu’à 2 Défenseurs vers des parcelles ciblées et renvoyez ce Gardien sur sa Face 1 en lisière (sa case est immédiatement libérée).";

catTiles.G7.profils.A.texte =
  "Posez 1 Piège sur une parcelle non rasée contenant au moins 1 Souche et aucun Piège, même occupée par une machine ou ciblée.";

catTiles.G9.profils.A.texte =
  "<strong>Face 1 :</strong> Ajoutez définitivement 1 carte Sabotage de la réserve au paquet Machine (mise de côté pour le remélange de fin de tour).<br><strong>Face 2 :</strong> Ajoutez définitivement 2 cartes Sabotage de la réserve au paquet Machine (mises de côté pour le remélange de fin de tour).";

catTiles.G12.profils.A.texte =
  "Faites avancer d’1 rang vers la gauche une tuile Rêve de la Piste des Tactiques (en poussant d’un cran tout bloc contigu de Rêves, sans activer son effet).";

catTiles.G13.profils.A.texte =
  "Posez 1 jeton Insecte sur une parcelle non rasée ou une case Furtivité contenant au moins 1 Défenseur.";

catTiles.G14.profils.A.texte =
  "Défaussez 1 Insecte d’une parcelle Forêt pour poser 1 Piège sur cette parcelle ou une parcelle non rasée adjacente du même rayon sans Piège.";

catTiles.R6.profils.A.texte =
  "Posez 1 Insecte de la réserve sur une parcelle non rasée d’un rayon de cette paire (H ou I).";

catTiles.R8.profils.A.texte =
  "Posez 1 Piège sur une parcelle non rasée sans Piège des rayons E ou R, même occupée par une machine ou ciblée.";

catTiles.M4.profils.A.texte =
  "Après production en 4.2, vous pouvez défausser 1 Insecte de ce Nid pour ajouter définitivement 1 carte Sabotage de la réserve au paquet Machine (mise de côté pour le remélange de fin de tour).";

// 5. Prepend v5.5 entry to VERSION_CHANGELOG
const changelog = extracted.VERSION_CHANGELOG;
if (changelog.length > 0 && changelog[0].version === 'v5.4.7') {
  changelog[0].date = 'Validation pré-gel (2026-11-20)';
}
const v55Entry = {
  version: 'v5.5',
  date: 'Socle gelé en vigueur (2026-11-20)',
  titre: 'Gel officiel du socle v5.5, refonte éditoriale complète du Livret et état des lieux Mode 4',
  resume:
    "Gel officiel du socle symétrique v5.5 (schema_version 5.5.0) consolidant toutes les règles validées en 5.4.7 : Piste des Tactiques fixe T1..T6, Rêves en coût d'activation (avancée uniquement si toutes les machines du rang sont annulées), Piste des Gardiens à pari uniforme (0/1/2 Défenseurs glissés, Face 2 en 5.3 uniquement sur pari gagné), partition stricte des 6 déclencheurs, Réveil de la Forêt 100 % Gardiens, Insectes Déviation + Bouclier de lisière. Réécriture intégrale du livret de règles joueur en 7 sections didactiques, vérification des 30 tuiles actives STANDARD_A en Mode 4, et enrichissement du digest (defense_attribution + tile_metrics complet).",
  deltas: [
    {
      domaine: 'Gel du socle v5.5 (moteur & 4 couches Studio)',
      avant:
        'v5.4.7 : Phase de stabilisation Mode 2 à blanc (verrous kernel dégelés, défauts hérités JUMP_PUSH et Colonie A).',
      apres:
        'v5.5 (5.5.0) : Socle officiellement gelé et verrouillé (kernel_locks.sha256 rescellé), défauts officiels CLEAR_RANK_ONLY + SLOT_BUG_CERVEAU=B + SLOT_COLONISATION_GARDIENS=B, compatibilité vérifiée des 30 tuiles actives STANDARD_A avec la double activation Gardien et le passage Face 2 en 5.3 uniquement.',
    },
    {
      domaine: 'Refonte complète du Livret de Règles joueur',
      avant:
        'v5.4.7 : Livret accumulant des correctifs successifs, des codes techniques et des formulations rétrospectives.',
      apres:
        'v5.5 : Livret réécrit intégralement de zéro en 7 sections éditoriales modernes (Présentation, Matériel, Vue d’ensemble, Déroulé étape par étape, Les Peuples, Fin & Repousse, Mémento de table), vocabulaire unifié, encadrés Règle d’or & Exemple concret, zéro jargon technique.',
    },
    {
      domaine: 'Digest enrichi & Manifeste Mode 4 baseline_mode4_v5_5',
      avant:
        'v5.4.7 : Campagnes mono-bot sans ventilation defense_attribution ni tile_metrics complet sur les 32 emplacements.',
      apres:
        'v5.5 : Section defense_attribution (7 postes), support multi-bots B0/B1/B2, tile_metrics complet sur les 32 slots, et manifeste baseline_mode4_v5_5.json prêt pour le premier état des lieux Mode 4.',
    },
  ],
};
const filteredChangelog = [v55Entry, ...changelog.filter((c) => c.version !== 'v5.5')];

// 6. Emit docs/data/amazonia_data_v5_5.js and validate with new vm.Script
const outJs = [
  '// =========================================================================',
  '// data/amazonia_data_v5_5.js — Données canoniques Amazonia v5.5 (Socle Gelé · 6 profils · 192 châssis · 32 emplacements actifs)',
  '// =========================================================================',
  `const PEUPLES = ${JSON.stringify(extracted.PEUPLES, null, 2)};`,
  '',
  `const MATRICE_PAIRES = ${JSON.stringify(extracted.MATRICE_PAIRES, null, 2)};`,
  '',
  `const TOPOLOGIES_PISTE_SPEC = ${JSON.stringify(extracted.TOPOLOGIES_PISTE_SPEC, null, 2)};`,
  '',
  `const CHASSIS_AXES_SPEC = ${JSON.stringify(extracted.CHASSIS_AXES_SPEC, null, 2)};`,
  '',
  `const CATALOGUE_TUILES = ${JSON.stringify(catTiles, null, 2)};`,
  '',
  `const VERSION_CHANGELOG = ${JSON.stringify(filteredChangelog, null, 2)};`,
  '',
  `const SPEC_FORMELLE_V5_5 = ${JSON.stringify(spec, null, 2)};`,
  '',
].join('\n');

new vm.Script(outJs, { filename: 'amazonia_data_v5_5.js' });
writeUtf8Lf(DST_JS, outJs);

console.log('Generated v5.5 Studio data layers successfully:');
console.log(' -', path.relative(ROOT, DST_SPEC));
console.log(' -', path.relative(ROOT, DST_CAT));
console.log(' -', path.relative(ROOT, DST_JS));
