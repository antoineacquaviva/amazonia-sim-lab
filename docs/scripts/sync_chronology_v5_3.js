'use strict';
/**
 * docs/scripts/sync_chronology_v5_3.js
 * Aligne etapes_tour dans les 4 couches Doc Studio (v5.3) sur la chronologie réelle
 * du livret (livret_v5_3.js) et du moteur Python (engine/core_engine.py) :
 *   1 (1.1-1.3) Préparation & Dés secrets
 *   2 (2.1-2.2) Pose des Défenseurs & Furtivité (4 emplacements)
 *   3 (3.1-3.2) Construction obligatoire -> Ouverture des Paravents & Rêves
 *   4 (4.1-4.3) Furtivité -> Production des Nids -> Migration des Insectes
 *   5 (5.1-5.3) Attaques des Machines & Vérification de Fin de Partie
 *   6 (6.1-6.3) Apprentissage du Contremaître & Ménage de fin de tour
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const DOCS_DIR = path.resolve(__dirname, '..');
const LIVRET_PATH = path.join(DOCS_DIR, 'data', 'livret_v5_3.js');
const JS_PATH = path.join(DOCS_DIR, 'data', 'amazonia_data_v5_3.js');
const SPEC_JSON_PATH = path.join(DOCS_DIR, 'data', 'spec_formelle_v5_3.json');
const CATALOG_JSON_PATH = path.join(DOCS_DIR, 'data', 'catalog_v5_3.json');

function findBalancedSpan(src, varName, openChar, closeChar) {
  const re = new RegExp(`(?:const|let|var)\\s+${varName}\\s*=\\s*`);
  const m = re.exec(src);
  if (!m) throw new Error(`Déclaration introuvable pour ${varName}`);
  const start = src.indexOf(openChar, m.index + m[0].length);
  if (start < 0) throw new Error(`Délimiteur ${openChar} introuvable pour ${varName}`);
  let depth = 0;
  let inStr = false;
  let strChar = '';
  let escaped = false;
  for (let i = start; i < src.length; i++) {
    const ch = src[i];
    if (inStr) {
      if (escaped) {
        escaped = false;
      } else if (ch === '\\') {
        escaped = true;
      } else if (ch === strChar) {
        inStr = false;
      }
      continue;
    }
    if (ch === '"' || ch === "'" || ch === '`') {
      inStr = true;
      strChar = ch;
    } else if (ch === openChar) {
      depth++;
    } else if (ch === closeChar) {
      depth--;
      if (depth === 0) return [start, i + 1];
    }
  }
  throw new Error(`Bloc non refermé pour ${varName}`);
}

function main() {
  // 1. Vérifier que livret_v5_3.js porte déjà la chronologie canonique 3.1 -> 3.2 -> 4.1
  const livretSrc = fs.readFileSync(LIVRET_PATH, 'utf8').replace(/\r\n/g, '\n');
  new vm.Script(livretSrc, { filename: 'livret_v5_3.js' });
  const livretCtx = vm.createContext({ window: {} });
  vm.runInContext(livretSrc + '\n;globalThis.__SYN = REGLES_COEUR_SYNTHESE;', livretCtx);
  const seqKeys = Object.keys(livretCtx.__SYN.sequence_tour_6_etapes);
  if (
    seqKeys.indexOf('3_1_construction') === -1 ||
    seqKeys.indexOf('3_2_revelation_et_sabotages') === -1 ||
    seqKeys.indexOf('4_1_furtivite') === -1
  ) {
    throw new Error('livret_v5_3.js ne contient pas les clés 3_1 / 3_2 / 4_1 attendues.');
  }
  console.log('[OK] livret_v5_3.js vérifié (chronologie canonique 3.1 -> 3.2 -> 4.1)');

  // 2. Charger spec_formelle_v5_3.json et réordonner etapes_tour sur la chronologie réelle v5.3
  const specObj = JSON.parse(fs.readFileSync(SPEC_JSON_PATH, 'utf8'));
  const oldSteps = specObj.etapes_tour;
  if (!Array.isArray(oldSteps) || oldSteps.length !== 6) {
    throw new Error('etapes_tour doit contenir exactement 6 étapes.');
  }

  const step5 = {
    numero: 5,
    code: 'ATTAQUES_ET_TEST_FIN',
    nom: 'Attaques des Machines et Vérification de Fin de Partie (5.1–5.3)',
    regles: oldSteps[4].regles,
  };
  const step6 = {
    numero: 6,
    code: 'APPRENTISSAGE_ET_MENAGE',
    nom: 'Apprentissage du Contremaître et Ménage de fin de tour (6.1–6.3)',
    regles: oldSteps[5].regles,
  };

  specObj.etapes_tour = [
    {
      numero: 1,
      code: 'PREPARATION_ET_DES_SECRETS',
      nom: 'Siège T4, Distribution et Dés secrets (1.1–1.3)',
      regles: [
        "1.1 Machines en Siège : toute machine déjà située sur la dernière parcelle non rasée de son rayon est en Siège T4 irréversible (carte posée sur sa parcelle). Son attaque en fin d’Étape 5 est autonome même si la tuile T4 a été éjectée par un Rêve ; en 6.1, elle alimente la tuile T4 en jetons d’Apprentissage si et seulement si T4 est encore présente sur la piste.",
        "1.2 Distribution : chaque joueur hors pénurie pioche secrètement 1 carte du paquet Machine (incluant toutes les cartes Sabotage intégrées définitivement). Une carte Sabotage tirée n’active aucune machine (action du Contremaître perdue). S’il reste moins de cartes que de joueurs, distribution dans le sens horaire à partir du peuple ayant le plus d’Arbres debout.",
        "1.3 Dés secrets sous paravent fermé (silence complet) : chaque joueur ayant reçu une carte Machine lance ses 2D6 et retient M = min(D1, D2) (modifié par les éventuelles Lois actives), qui désigne le rang sur la Piste des Tactiques. Si ce rang contient une tuile Rêve en 3.2 (y compris un Rêve construit en 3.1), l’activation de cette machine est annulée."
      ]
    },
    {
      numero: 2,
      code: 'POSE_DES_DEFENSEURS',
      nom: 'Pose des Défenseurs et Piste de Furtivité (2.1–2.2)',
      regles: [
        "2.1 / 2.2 Pose sous paravent fermé : 1er Défenseur irrévocable sur sa Forêt ou ses 2 lisières ; puis 2e Défenseur global (réflexion -> choix définitif). Anti-blocage : pose interdite sur Route Forestière, tuile construite/pleine/inconstructible ou rive Furtivité bordant une Route (si parcelle requise).",
        "Piste de Furtivité à 4 emplacements par case (2 jumeaux rive J1, 2 jumeaux rive J2 ; max 2 Défenseurs par case). Lorsqu'un Défenseur ENTRE sur une case de Furtivité (1er Défenseur, 2e en réflexion ou 2e posé directement en choix définitif), on le pose sur l'un des 4 emplacements valides et l'éventuel autre Défenseur présent glisse aussitôt sur l'emplacement jumeau du même bord (orientant l'unique action du binôme). Retourner sur place un jeton de sa face réflexion à sa face choix définitif se fait strictement sur son emplacement actuel, sans déplacement ni tirage."
      ]
    },
    {
      numero: 3,
      code: 'CONSTRUCTION_ET_REVELATION',
      nom: 'Construction obligatoire (3.1), Ouverture des Paravents et Rêves (3.2)',
      regles: [
        "3.1 Construction obligatoire : toute tuile réunissant ses 2 constructeurs (ou 1 Défenseur + 1 Insecte avec La Brèche du Tamanoir) est obligatoirement construite AVANT l’ouverture des paravents.",
        "3.1 Nid : posé sur une parcelle non rasée de l'un de ses 2 rayons ne contenant aucune machine ni aucun autre Nid, accompagné de tous ses Défenseurs constructeurs.",
        "3.1 Rêve : la Tactique la plus à droite sur la piste est définitivement éjectée ; seules les tuiles situées à droite de ce trou glissent d'un cran vers la gauche ; le nouveau Rêve prend place en case 6 (les Insectes Bug restent sur leur numéro d'emplacement imprimé). Ce Rêve est immédiatement présent sur la piste pour l’étape 3.2.",
        "3.1 Libération de bâtisseurs (Gardien/Rêve) : si 1 seul Défenseur est libéré parmi 2 (3 joueurs standard, ou 4-6 joueurs avec La Danse des Esprits-Fauves), le joueur du Peuple d'origine de la tuile choisit lequel et sa rive (1re parcelle adjacente non rasée). Si tous les Défenseurs bâtisseurs sont libérés (3 joueurs + Danse), chaque propriétaire choisit sa rive, dans la limite des Défenseurs réellement présents.",
        "3.2 Ouverture simultanée des paravents et fin du silence tactique. Toute carte Sabotage révélée n’a aucun autre effet que d’avoir fait perdre une activation au Contremaître : elle est mise de côté pour être remélangée dans le paquet Machine en 6.3.",
        "3.2 Résolution des Rêves : tout dé M désignant le rang d’un Rêve (y compris un Rêve qui vient d’être construit en 3.1 en case 6) annule sa machine, ouvre ce Rêve et le fait avancer d’1 cran vers la gauche (max 1 ouverture par Rêve et par tour en châssis standard UNIQUE_PAR_TOUR, résolue de gauche à droite)."
      ]
    },
    {
      numero: 4,
      code: 'FURTIVITE_NIDS_ET_MIGRATION',
      nom: 'Furtivité (4.1), Production des Nids (4.2) et Migration des Insectes (4.3)',
      regles: [
        "4.1 Furtivité : chaque binôme complet sur une case de Furtivité (2 Défenseurs sur la même rive, ou 1 Défenseur + 1 Insecte défaussé) déclenche 1 seule action, gouvernée par le joueur de la rive occupée — Piège si aucune machine présente (Déclencheur 2) OU Sabotage si au moins 1 machine présente et aucune active ce tour (Siège = active ; une machine annulée par un Rêve en 3.2 est inactive et donc sabotable ; allume Déclencheur 3).",
        "4.2 Production des Nids : chaque Nid actif est résolu comme un bloc indivisible : (1) création de 1 ou 2 Insectes selon le nombre d'Insectes physiquement présents sur sa parcelle à cet instant précis (y compris pour l'activation autonome des Guêpes Cazadores), puis (2) pouvoir 'après production' du Nid, puis seulement (3) balayage 1..6 des Gardiens. Une production hors phase (Le Miel des Ancêtres) ne crée que les jetons Insecte sans déclencher le pouvoir propre du Nid.",
        "4.3 Migration : chaque Insecte sur la roue peut se déplacer de 0 ou 1 cran (jusqu'à 2 avec L'Envol du Batará Suiveur), même s'il a bougé lors de la production d'un Nid. On retourne chaque jeton déplacé sur sa face verso pour suivi, puis on remet tous les jetons à l'endroit en fin de Migration avant d'évaluer la Colonisation.",
        "4.3 Pistes globales : depuis la dernière parcelle non rasée d'un rayon, 1 cran permet d'entrer sur n'importe quelle case 1..6 d'une piste globale (Bug du Cerveau ou Colonisation des Gardiens), sans limite de jetons par case. Cet aller simple est définitif."
      ]
    },
    step5,
    step6,
  ];

  // 3. Écrire spec_formelle_v5_3.json (UTF-8 sans BOM, LF)
  fs.writeFileSync(SPEC_JSON_PATH, JSON.stringify(specObj, null, 2) + '\n', 'utf8');
  console.log('[OK] docs/data/spec_formelle_v5_3.json mis à jour');

  // 4. Patcher SPEC_FORMELLE_V5_3 dans amazonia_data_v5_3.js via Node vm + JSON.stringify
  let jsSrc = fs.readFileSync(JS_PATH, 'utf8').replace(/\r\n/g, '\n');
  const [spStart, spEnd] = findBalancedSpan(jsSrc, 'SPEC_FORMELLE_V5_3', '{', '}');
  jsSrc = jsSrc.slice(0, spStart) + JSON.stringify(specObj, null, 2) + jsSrc.slice(spEnd);
  new vm.Script(jsSrc, { filename: 'amazonia_data_v5_3.js' });
  fs.writeFileSync(JS_PATH, jsSrc, 'utf8');
  console.log('[OK] docs/data/amazonia_data_v5_3.js mis à jour et validé par vm.Script');

  // 5. Synchroniser catalog_v5_3.json
  const catJson = JSON.parse(fs.readFileSync(CATALOG_JSON_PATH, 'utf8'));
  catJson.spec_formelle_v5_3 = specObj;
  fs.writeFileSync(CATALOG_JSON_PATH, JSON.stringify(catJson, null, 2) + '\n', 'utf8');
  console.log('[OK] docs/data/catalog_v5_3.json synchronisé');
}

main();
