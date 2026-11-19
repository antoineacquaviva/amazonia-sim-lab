#!/usr/bin/env node
/**
 * scripts/audit_and_fix_core_v5_3.js
 * 1. Retire la règle non voulue du "double aux dés" du châssis v5.3 (retour à M = min(D1,D2) pur).
 * 2. Affiche l'audit complet des 25 arbitrages actifs + le diff Git depuis le commit initial.
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { execSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const LIVRET_PATH = path.join(ROOT, 'data', 'livret_v5_3.js');
const JS_PATH = path.join(ROOT, 'data', 'amazonia_data_v5_3.js');
const CATALOG_JSON_PATH = path.join(ROOT, 'data', 'catalog_v5_3.json');
const SPEC_JSON_PATH = path.join(ROOT, 'data', 'spec_formelle_v5_3.json');

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
    if (ch === '/' && src[i + 1] === '/') { const nl = src.indexOf('\n', i + 2); if (nl === -1) break; i = nl; continue; }
    if (ch === '/' && src[i + 1] === '*') { const ec = src.indexOf('*/', i + 2); if (ec === -1) break; i = ec + 1; continue; }
    if (ch === "'" || ch === '"' || ch === '`') inQuote = ch;
    else if (ch === openCh) depth++;
    else if (ch === closeCh && --depth === 0) return [openIdx, i + 1];
  }
  throw new Error(`Fermeture ${closeCh} introuvable pour ${varName}`);
}

function purgeDoubleDiceFromCore() {
  console.log('=== 1. PURGE DU "DOUBLE AUX DÉS" DANS LE CHÂSSIS v5.3 ===');

  // A. data/livret_v5_3.js
  let livSrc = fs.readFileSync(LIVRET_PATH, 'utf8').replace(/\r\n/g, '\n');
  const livCtx = vm.createContext({ window: {} });
  vm.runInContext(livSrc.split('function renderDidacticRulebook')[0] + '\n;globalThis.__RCS = REGLES_COEUR_SYNTHESE;', livCtx);
  const rcs = livCtx.__RCS;

  rcs.sequence_tour_6_etapes["1_siege_et_plan"] =
    "Machines sur la dernière parcelle non rasée = Siège irréversible (autonome même si T4 éjectée, 0 Apprentissage). Distribution 1 carte/joueur depuis le paquet Machine (incluant les cartes Sabotage déjà intégrées ; si moins de cartes que de joueurs : sens horaire depuis le Peuple ayant le plus d'Arbres debout). Sous paravent : si carte Sabotage (ou sans carte), aucune machine activée et pas de dé M retenu ; si carte Machine, lancer 2D6 et retenir M = min(D1,D2) (modifié par Lois) qui désigne le rang sur la Piste Tactiques (si rang M = Rêve, activation machine annulée en 3.2).";
  rcs.sequence_tour_6_etapes["3_2_revelation_et_sabotages"] =
    "Ouverture simultanée des paravents ; fin du silence. Toute carte Sabotage révélée est simplement mise de côté (action du Contremaître perdue ce tour) pour être remélangée dans le paquet en 6.3. Dé M désignant un Rêve : annule la machine, ouvre le Rêve et l'avance r -> r-1 (max 1 ouverture/Rêve/tour en standard, ou cumulatif selon axe).";
  delete rcs.sequence_tour_6_etapes["3_2_revelation"];

  const [rcsStart, rcsEnd] = findBalancedSpan(livSrc, 'REGLES_COEUR_SYNTHESE', '{', '}');
  livSrc = livSrc.slice(0, rcsStart) + JSON.stringify(rcs, null, 2) + livSrc.slice(rcsEnd);

  // Remplacements dans renderDidacticRulebook()
  livSrc = livSrc.replace(
    /; un joueur sans carte lance quand même ses 2 dés pour tenter un double Rêve\)\.<\/em>/g,
    ').</em>'
  );
  livSrc = livSrc.replace(
    /<li><strong>Double aux dés :<\/strong>[\s\S]*?<\/li>\s*/g,
    ''
  );
  livSrc = livSrc.replace(
    /<strong>Si vous avez pioché une carte Machine :<\/strong>/g,
    '<strong>Si vous avez pioché une carte Machine :</strong> lancez vos 2 dés ;'
  );
  livSrc = livSrc.replace(
    /<strong>Rêves \(double aux dés ou dé M sur un Rêve\) :<\/strong>/g,
    '<strong>Rêves (dé M désignant un Rêve) :</strong>'
  );
  livSrc = livSrc.replace(
    /Chaque Rêve sollicité \(par un double ou par au moins un dé M\)/g,
    'Chaque Rêve désigné par au moins un dé M'
  );

  new vm.Script(livSrc, { filename: 'livret_v5_3.js' });
  fs.writeFileSync(LIVRET_PATH, livSrc, 'utf8');
  console.log('  [OK] data/livret_v5_3.js épuré (lecture par M = min(D1, D2) uniquement)');

  // B. data/spec_formelle_v5_3.json & data/amazonia_data_v5_3.js & data/catalog_v5_3.json
  let jsSrc = fs.readFileSync(JS_PATH, 'utf8').replace(/\r\n/g, '\n');
  const dataCtx = vm.createContext({ window: {} });
  vm.runInContext(
    jsSrc + '\n;globalThis.__CL = VERSION_CHANGELOG; globalThis.__SPEC = typeof SPEC_FORMELLE_V5_3 !== "undefined" ? SPEC_FORMELLE_V5_3 : null;',
    dataCtx
  );

  // Changelog v5.3 delta 4
  dataCtx.__CL[0].deltas[3].apres = dataCtx.__CL[0].deltas[3].apres.replace(
    'Double = Rêve ; hors double, min(D1,D2) sur la machine (annulée si Rêve).',
    'Lecture pure M = min(D1,D2) sur carte Machine (annulée si rang M = Rêve).'
  );

  const specObj = fs.existsSync(SPEC_JSON_PATH)
    ? JSON.parse(fs.readFileSync(SPEC_JSON_PATH, 'utf8'))
    : dataCtx.__SPEC;

  if (specObj) {
    specObj.etapes_tour[0].regles[1] =
      "Chaque joueur hors pénurie pioche secrètement 1 carte du paquet Machine (incluant toutes les cartes Sabotage intégrées définitivement). Une carte Sabotage tirée n’active aucune machine (action du Contremaître perdue). S’il reste moins de cartes que de joueurs, distribution dans le sens horaire à partir du peuple ayant le plus d’Arbres debout.";
    specObj.etapes_tour[0].regles[2] =
      "Sous paravent fermé (silence complet) : chaque joueur ayant reçu une carte Machine lance ses 2D6 et retient M = min(D1, D2) (modifié par les éventuelles Lois actives), qui désigne le rang sur la Piste des Tactiques. Si ce rang contient une tuile Rêve, l’activation de cette machine sera annulée en 3.2.";
    specObj.etapes_tour[1].regles[2] =
      "Résolution des Rêves : tout dé M désignant le rang d’un Rêve annule sa machine, ouvre ce Rêve et le fait avancer d’1 cran vers la gauche (max 1 ouverture par Rêve et par tour en châssis standard UNIQUE_PAR_TOUR, résolue de gauche à droite).";
    if (specObj.arbitrages_valides) {
      for (const [k, v] of Object.entries(specObj.arbitrages_valides)) {
        if (/double/i.test(v) && /rêve|dés|des/i.test(v)) {
          specObj.arbitrages_valides[k] =
            "Lecture épurée des dés sous paravent : seul un joueur ayant tiré une carte Machine retient M = min(D1, D2) (ou max sous Loi). Si le rang M porte un Rêve en 3.2, la machine est annulée et le Rêve s’ouvre.";
        }
      }
    }
    fs.writeFileSync(SPEC_JSON_PATH, JSON.stringify(specObj, null, 2) + '\n', 'utf8');
    console.log('  [OK] data/spec_formelle_v5_3.json mis à jour');
  }

  const [clStart, clEnd] = findBalancedSpan(jsSrc, 'VERSION_CHANGELOG', '[', ']');
  jsSrc = jsSrc.slice(0, clStart) + JSON.stringify(dataCtx.__CL, null, 2) + jsSrc.slice(clEnd);
  if (specObj && jsSrc.includes('const SPEC_FORMELLE_V5_3 =')) {
    const [spStart, spEnd] = findBalancedSpan(jsSrc, 'SPEC_FORMELLE_V5_3', '{', '}');
    jsSrc = jsSrc.slice(0, spStart) + JSON.stringify(specObj, null, 2) + jsSrc.slice(spEnd);
  }
  new vm.Script(jsSrc, { filename: 'amazonia_data_v5_3.js' });
  fs.writeFileSync(JS_PATH, jsSrc, 'utf8');

  if (fs.existsSync(CATALOG_JSON_PATH) && specObj) {
    const catJson = JSON.parse(fs.readFileSync(CATALOG_JSON_PATH, 'utf8'));
    catJson.spec_formelle_v5_3 = specObj;
    fs.writeFileSync(CATALOG_JSON_PATH, JSON.stringify(catJson, null, 2) + '\n', 'utf8');
  }
  console.log('  [OK] data/amazonia_data_v5_3.js et data/catalog_v5_3.json synchronisés\n');
}

function runFullAudit() {
  console.log('=== 2. CONTRÔLE AUTEUR : LES ARBITRAGES ACTIFS DANS SPEC_FORMELLE_V5_3 ===');
  const spec = JSON.parse(fs.readFileSync(SPEC_JSON_PATH, 'utf8'));
  for (const [k, v] of Object.entries(spec.arbitrages_valides || {})) {
    console.log(`  ${k.padEnd(4)} : ${v}`);
  }

  console.log('\n=== 3. HISTORIQUE GIT & DIFF DES MÉCANIQUES DEPUIS LE PREMIER COMMIT ===');
  const logOut = execSync('git log --oneline', { cwd: ROOT }).toString().trim().split('\n');
  logOut.slice(0, 10).forEach(line => console.log('  ' + line));
  const firstCommit = logOut[logOut.length - 1].split(' ')[0];
  console.log(`\nComparaison des primitives/fenêtres entre le commit initial (${firstCommit}) et HEAD :`);

  try {
    const oldJs = execSync(`git show ${firstCommit}:data/amazonia_data_v5_3.js`, { cwd: ROOT, stdio: ['pipe', 'pipe', 'ignore'] }).toString('utf8');
    const oldCtx = vm.createContext({ window: {} });
    vm.runInContext(oldJs + '\n;globalThis.__CAT = CATALOGUE_TUILES;', oldCtx);

    const curCtx = vm.createContext({ window: {} });
    vm.runInContext(fs.readFileSync(JS_PATH, 'utf8') + '\n;globalThis.__CAT = CATALOGUE_TUILES;', curCtx);

    let diffCount = 0;
    for (const [tId, curTile] of Object.entries(curCtx.__CAT)) {
      const oldTile = oldCtx.__CAT[tId];
      if (!oldTile) continue;
      for (const [letter, curProf] of Object.entries(curTile.profils)) {
        const oldProf = oldTile.profils[letter];
        if (!oldProf) continue;
        if (oldProf.primitive !== curProf.primitive || oldProf.fenetre !== curProf.fenetre) {
          diffCount++;
          console.log(`  • ${tId}_${letter} (${curProf.nom}) :`);
          console.log(`      Avant : [${oldProf.fenetre}] ${oldProf.primitive}`);
          console.log(`      Après : [${curProf.fenetre}] ${curProf.primitive}`);
        }
      }
    }
    if (diffCount === 0) console.log('  Aucune mutation de primitive/fenêtre depuis le commit initial.');
  } catch (e) {
    console.log(`  (Note : data/amazonia_data_v5_3.js n'existait pas encore au commit ${firstCommit} : ${e.message.split('\n')[0]})`);
  }
}

purgeDoubleDiceFromCore();
runFullAudit();