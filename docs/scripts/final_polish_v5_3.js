#!/usr/bin/env node
/**
 * scripts/final_polish_v5_3.js
 * Clôture v5.3 : dédoublonnage de VERSION_CHANGELOG, 4 micro-finitions tuiles et libellés index.html.
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const JS_PATH = path.join(ROOT, 'data', 'amazonia_data_v5_3.js');
const JSON_PATH = path.join(ROOT, 'data', 'catalog_v5_3.json');
const INDEX_PATH = path.join(ROOT, 'index.html');

const CANONICAL_V5_3_CHANGELOG = {
  version: "v5.3",
  date: "Version consolidée en vigueur (Audit · 25 arbitrages)",
  titre: "Seuil Imprimé Fixe, Embuscade unique (100 profils), Furtivité à 4 emplacements jumeaux & Zéro Verrouillage",
  resume: "Alignement intégral Livret Humain / Catalogue (100 profils) / Simulateur / BGA : Seuil Imprimé fixe (P4_2233 / P5_22233), Furtivité orientée à 4 emplacements jumeaux, gouvernance unitaire par Peuple d’origine, défausse immédiate des Insectes à la parade (zéro dette et zéro verrouillage des parcelles), cascades de Gardiens à plat (1→6) et résolution complète machine par machine.",
  deltas: [
    {
      domaine: "1. Topologie, Seuil Imprimé & Chaîne des Parades (100 profils)",
      avant: "v5.2 : Seuil comptant Arbres + Souches ; 2 options de Pièges avec Amortisseur (116 profils D/E).",
      apres: "v5.3 : P4_2233 [2,2,3,3] (10N Arbres) ou P5_22233 [2,2,2,3,3] (12N Arbres). Seuil = max(1, Seuil_Imprimé(p) + Offset + Rouges - Bleus + Mod_Tactique + Mod_Tuiles). Suppression de l’Amortisseur (100 profils). Chaîne stricte à chaque frappe : 1° Jaguar (2 bleus) -> 2° Harpie -> 3° Piège Embuscade (si Défense totale >= 1, locale ou à distance) -> 4° Parade classique."
    },
    {
      domaine: "2. Furtivité à 4 emplacements jumeaux, Silence & Gouvernance",
      avant: "Action bilatérale sur les 2 rives ou mémoire de l’ordre d’arrivée ; décisions collectives sur les tuiles.",
      apres: "v5.3 : 4 emplacements par case Furtivité (2 jumeaux/rive, max 2 Défenseurs). Entrer sur la case (toute face) tire l’autre pion sur le jumeau de son bord et oriente l’unique action du binôme ; retourner de réflexion à définitif se fait strictement sur place. Silence tactique sous paravent fermé ; chaque Tuile et piste de Migration est gouvernée par son seul Peuple d’origine (Sabotages visibles par H)."
    },
    {
      domaine: "3. Combat d’un seul tenant, Zéro Verrouillage, Routes & Contact Nid",
      avant: "Dette d’Insectes engagés ou verrouillage des parcelles ciblées durant l’Étape 5 ; cibles figées à la révélation.",
      apres: "v5.3 : Défausse immédiate des Insectes requis à la frappe et zéro verrouillage des parcelles (seul un Piège déjà déclenché ne paie plus de coût volontaire). Ordre Tactiques 1..6 puis Sièges (Abatteuse avant Bulldozer sur un même rayon), chaque machine résolue d’un seul tenant depuis sa position réelle. Routes sautées le long du rayon ; tout mouvement machine entrant sur un Nid le renvoie reconstructible en lisière et défausse les Insectes de la case."
    },
    {
      domaine: "4. Dés, Rêves, Nids, Cascades à plat (1→6), Siège & Fin de partie",
      avant: "Cascades imbriquées, seuil de Réveil recalculé après sacrifice, Siège dépendant de T4.",
      apres: "v5.3 : Double = Rêve ; hors double, min(D1,D2) sur la machine (annulée si Rêve). Rêve inséré en case 6 (éjecte la Tactique la plus à droite, glissement partiel). Nid indivisible avant Gardiens ; Migration 0 ou 1 cran (aller simple vers pistes globales). Cascades à plat de 1 à 6 (marquage immédiat, Faces 2 autonomes). Siège autonome (0 Apprentissage). Seuil de Réveil fixe vérifié en fin de 5.3 (+ Écho en 6.2) ; raz totale des jetons Apprentissage en 6.2."
    }
  ]
};

const MICRO_PATCHES = {
  G2: {
    A: {
      texte: "<strong>Face 1 :</strong> Faites reculer d’1 parcelle non rasée vers la bordure une machine non en Siège située sur une parcelle avec au moins 1 Défenseur.<br><strong>Face 2 :</strong> Faites reculer d’1 parcelle non rasée vers la bordure n’importe quelle machine non en Siège."
    }
  },
  G7: {
    D: {
      texte: "Vous pouvez poser 1 Piège sur une parcelle non rasée sans Piège des Mammifères ou des Humains contenant au moins 1 Défenseur ou 1 Insecte, même occupée par une machine ou ciblée (allume la case 2)."
    }
  },
  R4: {
    C: {
      texte: "Face à une Route Forestière de l’autre rayon sur la lisière Humains–Reptiles, vous pouvez poser 1 Piège sur la parcelle non rasée sans Piège en face, même ne portant que des Souches, ciblée ou occupée par une machine (allume la case 2)."
    }
  },
  SLOT_BUG_CERVEAU: {
    B: {
      texte: "Lorsqu’un joueur obtient ce rang avec son dé M en 3.2, le gouverneur de la piste (Insectes, ou ce joueur si I est absent) peut défausser l’Insecte pour décaler la lecture de ce dé M d’1 rang (M−1 ou M+1, borné de 1 à 6)."
    }
  }
};

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

function syncJsonTree(node, cat) {
  if (Array.isArray(node)) return node.forEach(x => syncJsonTree(x, cat));
  if (node && typeof node === 'object') {
    for (const [k, v] of Object.entries(node)) {
      if (cat[k] && v && v.profils) {
        for (const [pL, pO] of Object.entries(cat[k].profils)) {
          if (v.profils[pL]) Object.assign(v.profils[pL], pO);
        }
      }
      if (v && typeof v === 'object') syncJsonTree(v, cat);
    }
  }
}

function main() {
  let jsSrc = fs.readFileSync(JS_PATH, 'utf8');
  const ctx = vm.createContext({ window: {} });
  vm.runInContext(jsSrc + '\n;globalThis.__CAT = CATALOGUE_TUILES; globalThis.__CL = VERSION_CHANGELOG;', ctx);

  // 1. Dédoublonnage strict de VERSION_CHANGELOG (1 seule entrée v5.3 en tête)
  const cleanChangelog = [
    CANONICAL_V5_3_CHANGELOG,
    ...ctx.__CL.filter(entry => entry.version !== 'v5.3')
  ];

  // 2. Micro-finitions sur les 4 profils
  for (const [tId, profs] of Object.entries(MICRO_PATCHES)) {
    for (const [letter, patch] of Object.entries(profs)) {
      Object.assign(ctx.__CAT[tId].profils[letter], patch);
    }
  }

  // Remplacement dans amazonia_data_v5_3.js + suppression d'éventuels .unshift(...) résiduels
  const [clStart, clEnd] = findBalancedSpan(jsSrc, 'VERSION_CHANGELOG', '[', ']');
  jsSrc = jsSrc.slice(0, clStart) + JSON.stringify(cleanChangelog, null, 2) + jsSrc.slice(clEnd);
  const [catStart, catEnd] = findBalancedSpan(jsSrc, 'CATALOGUE_TUILES', '{', '}');
  jsSrc = jsSrc.slice(0, catStart) + JSON.stringify(ctx.__CAT, null, 2) + jsSrc.slice(catEnd);
  jsSrc = jsSrc.replace(/VERSION_CHANGELOG\.unshift\([\s\S]*?\);\s*/g, '');

  // Vérification runtime dans une sandbox vierge
  const checkCtx = vm.createContext({ window: {} });
  vm.runInContext(jsSrc + '\n;globalThis.__CL_CHECK = VERSION_CHANGELOG;', checkCtx);
  const v53Count = checkCtx.__CL_CHECK.filter(e => e.version === 'v5.3').length;
  if (v53Count !== 1 || !checkCtx.__CL_CHECK[0].titre.includes('4 emplacements jumeaux')) {
    throw new Error(`Échec vérification VERSION_CHANGELOG (v5.3 count=${v53Count}).`);
  }
  fs.writeFileSync(JS_PATH, jsSrc.replace(/\r\n/g, '\n'), 'utf8');

  // 3. Synchronisation de data/catalog_v5_3.json
  if (fs.existsSync(JSON_PATH)) {
    const jsonObj = JSON.parse(fs.readFileSync(JSON_PATH, 'utf8'));
    syncJsonTree(jsonObj, ctx.__CAT);
    fs.writeFileSync(JSON_PATH, JSON.stringify(jsonObj, null, 2) + '\n', 'utf8');
  }

  // 4. Nettoyage des 4 libellés statiques dans index.html
  let html = fs.readFileSync(INDEX_PATH, 'utf8');
  html = html
    .replace('Pièges : Embuscade Assistée', 'Pièges : Embuscade (Déf ≥ 1)')
    .replace('Capital : 48 Arbres (4×3)', 'Capital : 40 Arbres (P4_2233 · 10×4)')
    .replace(/les 10 axes/g, 'les 7 axes')
    .replace('ou compatibilité avec l\'option de Piège active.', 'ou présence autour de la table.')
    .replace('<option value="COMPATIBLE_ONLY">Compatibles avec l\'option Piège active</option>\n', '');
  fs.writeFileSync(INDEX_PATH, html.replace(/\r\n/g, '\n'), 'utf8');

  console.log('[SUCCÈS] VERSION_CHANGELOG dédoublonné (1 seule v5.3), 4 profils polis et UI index.html nettoyée.');
}

main();