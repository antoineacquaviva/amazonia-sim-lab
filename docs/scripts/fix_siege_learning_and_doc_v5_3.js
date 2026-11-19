#!/usr/bin/env node
/**
 * scripts/fix_siege_learning_and_doc_v5_3.js
 * 1. Rétablit l'Apprentissage des machines en Siège sur la tuile T4 (tant que T4 est en piste) [Arbitrage A10 / Étape 6.1].
 * 2. Génère AMAZONIA_STUDIO_CONTEXT.md à la racine du dépôt (100 % aligné sur v5.3).
 * 3. Exécute un contrôle différentiel contre le commit pré-audit ab987e0.
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
const CONTEXT_MD_PATH = path.join(ROOT, 'AMAZONIA_STUDIO_CONTEXT.md');

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

function patchSiegeLearning() {
  console.log('=== 1. RÉTABLISSEMENT DE L’APPRENTISSAGE DU SIÈGE SUR T4 (A10 & 6.1) ===');

  // A. data/livret_v5_3.js
  let livSrc = fs.readFileSync(LIVRET_PATH, 'utf8').replace(/\r\n/g, '\n');
  const livCtx = vm.createContext({ window: {} });
  vm.runInContext(livSrc.split('function renderDidacticRulebook')[0] + '\n;globalThis.__RCS = REGLES_COEUR_SYNTHESE;', livCtx);
  const rcs = livCtx.__RCS;

  rcs.sequence_tour_6_etapes["1_siege_et_plan"] =
    "Machines sur la dernière parcelle non rasée = Siège T4 irréversible (attaque autonome même si la tuile T4 a été éjectée). Distribution 1 carte/joueur depuis le paquet Machine (incluant les cartes Sabotage déjà intégrées ; si moins de cartes que de joueurs : sens horaire depuis le Peuple ayant le plus d'Arbres debout). Sous paravent : si carte Sabotage (ou sans carte), aucune machine activée et pas de dé M retenu ; si carte Machine, lancer 2D6 et retenir M = min(D1,D2) (modifié par Lois) qui désigne le rang sur la Piste Tactiques (si rang M = Rêve, activation machine annulée en 3.2).";

  rcs.sequence_tour_6_etapes["6_apprentissage"] =
    "6.1 Toute machine active ce tour-ci (activée par carte OU en Siège T4) rapporte à sa Tactique (T4 pour un Siège, uniquement si T4 est encore sur la piste) : +1/parcelle réellement endommagée (>=1 Arbre coupé ou Souche retirée) +1/Rouge acquis ce tour -1/Bleu présent (plancher 0/machine). Retraits tuiles volontaires AVANT Insectes Bug (Bug économisé si déjà 0). 6.2 Tactique strictement seule en tête avec >=1 jeton échange à gauche (si Écho des Voix Célestes amène son Rêve en case 1 -> Repousse Finale fin de tour). Remise à zéro de 100 % des jetons Apprentissage dans tous les cas. 6.3 Raz marqueurs Gardiens, retour Défenseurs, et remélange du paquet Machine (hors Siège) avec TOUTES les cartes Sabotage (révélées ce tour + nouvellement acquises).";

  const [rcsStart, rcsEnd] = findBalancedSpan(livSrc, 'REGLES_COEUR_SYNTHESE', '{', '}');
  livSrc = livSrc.slice(0, rcsStart) + JSON.stringify(rcs, null, 2) + livSrc.slice(rcsEnd);

  // Remplacements dans renderDidacticRulebook()
  livSrc = livSrc.replace(
    `<strong>même si la tuile <code>T4</code> a été éjectée de la piste</strong>, et ne génère jamais d'Apprentissage.`,
    `<strong>même si la tuile <code>T4</code> a été éjectée de la piste</strong> (tant que <code>T4</code> est sur la piste, une machine en Siège lui rapporte normalement de l'Apprentissage en 6.1).`
  );

  livSrc = livSrc.replace(
    `<strong>6.1. Décompte (hors machines en Siège, qui rapportent toujours 0) :</strong> Chaque machine activée par une carte ce tour-ci rapporte à sa Tactique :`,
    `<strong>6.1. Décompte (cartes Machine + machines en Siège sur <code>T4</code>) :</strong> Chaque machine active ce tour-ci rapporte à la tuile Tactique qu'elle a exécutée (<code>T4</code> pour une machine en Siège, si <code>T4</code> figure encore sur la piste) :`
  );

  if (/Siège\s*=\s*0|hors machines en Siège, qui rapportent toujours 0|ne génère jamais d'Apprentissage/i.test(livSrc)) {
    throw new Error('Résidu "Siège = 0 Apprentissage" encore présent dans livret_v5_3.js');
  }

  new vm.Script(livSrc, { filename: 'livret_v5_3.js' });
  fs.writeFileSync(LIVRET_PATH, livSrc, 'utf8');
  console.log('  [OK] data/livret_v5_3.js mis à jour');

  // B. data/spec_formelle_v5_3.json, data/amazonia_data_v5_3.js & data/catalog_v5_3.json
  let jsSrc = fs.readFileSync(JS_PATH, 'utf8').replace(/\r\n/g, '\n');
  const dataCtx = vm.createContext({ window: {} });
  vm.runInContext(
    jsSrc + '\n;globalThis.__CL = VERSION_CHANGELOG; globalThis.__SPEC = typeof SPEC_FORMELLE_V5_3 !== "undefined" ? SPEC_FORMELLE_V5_3 : null;',
    dataCtx
  );

  dataCtx.__CL[0].deltas[3].apres = dataCtx.__CL[0].deltas[3].apres.replace(
    'Siège autonome (0 Apprentissage).',
    'Siège T4 autonome (alimente T4 en 6.1 tant que T4 est en piste).'
  );

  const specObj = fs.existsSync(SPEC_JSON_PATH)
    ? JSON.parse(fs.readFileSync(SPEC_JSON_PATH, 'utf8'))
    : dataCtx.__SPEC;

  if (specObj) {
    specObj.etapes_tour[0].regles[0] =
      "Machines en Siège : toute machine déjà située sur la dernière parcelle non rasée de son rayon est en Siège T4 irréversible (carte posée sur sa parcelle). Son attaque en fin d’Étape 5 est autonome même si la tuile T4 a été éjectée par un Rêve ; en 6.1, elle alimente la tuile T4 en jetons d’Apprentissage si et seulement si T4 est encore présente sur la piste.";

    specObj.etapes_tour[5].regles[0] =
      "Calcul par machine active ce tour-ci (activée par carte OU en Siège T4) pour sa Tactique (T4 pour un Siège ; sans effet si T4 a été éjectée de la piste) : +1 par parcelle réellement endommagée (>= 1 Arbre coupé ou >= 1 Souche retirée) +1 par jeton Puissance rouge acquis ce tour -1 par jeton bleu Surchauffe présent sur la machine (plancher 0 par machine).";

    specObj.arbitrages_valides.A10 =
      "Autonomie et Apprentissage du Siège : l’attaque d’une machine en Siège reste active même si la tuile T4 est éjectée ; en 6.1, une machine en Siège génère normalement ses jetons d’Apprentissage sur T4 tant que T4 figure sur la Piste des Tactiques (ignorés si T4 est éjectée).";

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
  console.log('  [OK] data/amazonia_data_v5_3.js et data/catalog_v5_3.json synchronisés');
}

function writeContextMarkdown() {
  console.log('\n=== 2. GÉNÉRATION DE AMAZONIA_STUDIO_CONTEXT.MD ===');
  const md = `# AMAZONIA DOC STUDIO — Référentiel Fonctionnel & Technique (v5.3)

> **Usage IA (Pièce Jointe de Prompt)** : Ce document décrit l'architecture, le périmètre fonctionnel, les modèles de données et les règles strictes de maintenance de l'application **Amazonia Doc Studio**. Toute modification proposée par une IA doit respecter le découplage des 4 couches et les invariants techniques détaillés en Section 5.

---

## 1. Identité & Rôle dans l'Écosystème

- **Projet** : *Amazonia : Dernier Rempart* — Jeu de société coopératif asymétrique à communication muette (3 à 6 joueurs, 8 tours max).
- **Application** : **Amazonia Doc Studio** (\`v5.3\` consolidée — 25 arbitrages formels).
- **Dépôt & Hébergement** :
  - GitHub : \`https://github.com/antoineacquaviva/amazonia-doc-studio\`
  - Production (GitHub Pages) : \`https://antoineacquaviva.github.io/amazonia-doc-studio/\`
- **Vocation (« Source Unique de Vérité »)** : Maintenir dans un référentiel unique et sans dérive documentaire :
  1. Le **Livret de Règles Didactique** dynamique destiné aux joueurs humains (imprimable en PDF propre).
  2. La **Bibliothèque complète d'asymétrie** (32 emplacements / **100 profils** \`A\`, \`B\`, \`C\`, \`D\`).
  3. Le **Journal de traçabilité des versions et arbitrages** (\`v4.3\` → \`v5.3\`).
  4. Le **Contrat formel JSON** consommé par le simulateur Monte-Carlo Python (\`amazonia-sim\` / \`foret-automate-lab\`) et le portage **Board Game Arena (BGA)**.

---

## 2. Périmètre Fonctionnel (Interface Utilisateur)

L'application est une **SPA statique sans bundler** (compatible \`file://\` et HTTPS) articulée autour d'un bandeau configurateur persistant et de 4 vues synchronisées en temps réel via l'état réactif \`state\`.

### 2.1. Bandeau Supérieur & Configurateur d'Instance
- **Presets (\`bundleId\`)** : \`STANDARD_A\`, \`ESSAI_52_EMBUSCADE\`, 5 modules \`N=3\` joueurs (\`52_CAPYBARA_D\`, \`52_HARPIE_D\`, \`52_DENDROBATE_D\`, \`52_PIERRE_D\`, \`52_ATELE_D\`) ou \`CUSTOM\`.
- **Cercle des Peuples (\`peuplesCercle\`)** : 3 à 6 Peuples actifs ordonnés autour de la table parmi \`M\` (Mammifères), \`R\` (Reptiles), \`O\` (Oiseaux), \`H\` (Humains), \`E\` (Entités Magiques), \`I\` (Insectes). Détermine via \`MATRICE_PAIRES\` les \`2N\` Tuiles de Synergie sur les \`N\` lisières.
- **Slots de Migration (\`slotsInsectes\`)** : \`SLOT_BUG_CERVEAU\` (\`A/B/C\`) et \`SLOT_COLONISATION_GARDIENS\` (\`A/C\`).
- **Les 7 Axes du Châssis (\`CHASSIS_AXES_SPEC\` — $2^7 = 128$ configurations)** :
  1. \`P_Max\` : \`4\` (\`P4_2233\` \`[2,2,3,3]\` = $10N$ Arbres, défaut) | \`5\` (\`P5_22233\` \`[2,2,2,3,3]\` = $12N$ Arbres).
  2. \`Regle_Ouverture_Reve_Multiple\` : \`UNIQUE_PAR_TOUR\` (défaut) | \`PAR_DE_M_DESIGNE\`.
  3. \`Offset_Seuil_Parade\` : \`0\` (défaut) | \`1\`.
  4. \`Mise_En_Place_Tactiques\` : \`ORDRE_FIXE_T1_T6\` (défaut) | \`ALEATOIRE\`.
  5. \`Declenchement_Fin_De_Piste\` : \`ARRIVEE_DERNIERE_PARCELLE\` (défaut) | \`DEPASSEMENT_DERNIERE_PARCELLE\`.
  6. \`Role_Abatteuse_Fin_De_Piste\` : \`STANDARD_COUPE_ARBRE\` (défaut) | \`ARRACHE_1_SOUCHE_SI_SANS_ARBRE\`.
  7. \`Synergie_Binome_Machines\` : \`INDIVIDUELLE\` (défaut) | \`MUTUALISATION_PUISSANCE_MEME_PARCELLE\`.
- **Export IA contextuel (\`✨ Copier contexte Gemini\`)** : Copie un JSON structuré (\`_meta\`, \`regles_coeur\`, \`instance\`, \`tuiles_ciblees\`) limité aux tuiles en jeu ou filtrées (\`Shift + Clic\` = export complet des 100 profils + tête du changelog).

### 2.2. Les 4 Vues Synchronisées
1. **📖 1. Livret Didactique (\`#view-livret\`)** : Règles humaines complètes compilées dynamiquement pour l'instance active, avec tableau des \`2N\` tuiles, autorité par Peuple d'origine et surlignage ambre commutable des blocs dynamiques.
2. **🧩 2. Explorateur des 100 Profils (\`#view-catalogue\`)** : Recherche plein texte, filtres par famille/peuple/lettre/tags, comparaison côte à côte \`A/B/C/D\` et activation directe dans l'instance.
3. **🔍 3. Évolutions & Arbitrages (\`#view-changelog\`)** : Différentiel historique structuré \`Avant / Après\` de \`v4.3\` à \`v5.3\`.
4. **💻 4. Spec & JSON Simulateur (\`#view-json\`)** : Export, téléchargement \`.json\` et réimportation d'un manifeste d'instance (\`schema_version: "5.3"\`) + mémento des 8 Primitives Atomiques.

---

## 3. Architecture Technique & Découplage des 4 Couches

\`\`\`text
amazonia-doc-studio/
├── index.html                      # Coquille UI (Tailwind CDN), état réactif state, filtres, export JSON/Gemini
├── AMAZONIA_STUDIO_CONTEXT.md      # Présent référentiel fonctionnel & technique pour prompts IA
├── data/
│   ├── amazonia_data_v5_3.js       # Source JS : PEUPLES, MATRICE_PAIRES, CHASSIS_AXES_SPEC,
│   │                               # CATALOGUE_TUILES (32 slots / 100 profils), VERSION_CHANGELOG, SPEC_FORMELLE_V5_3
│   ├── livret_v5_3.js              # Règles humaines découplées : REGLES_COEUR_SYNTHESE + renderDidacticRulebook()
│   ├── catalog_v5_3.json           # Miroir JSON pur du catalogue et du châssis (pour Python / BGA)
│   └── spec_formelle_v5_3.json     # Contrat formel normé des 6 étapes du tour et des 25 arbitrages v5.3
└── scripts/                        # Scripts incrémentaux d'audit et de synchronisation (Node.js & Python)
\`\`\`

**Ordre de chargement dans \`index.html\`** : \`data/amazonia_data_v5_3.js\` → \`data/livret_v5_3.js\` → script inline d'UI (\`refreshAllUI()\`).

---

## 4. Modèles de Données & Invariants Mécaniques Cœur (v5.3)

### 4.1. Répartition des 32 Emplacements (100 Profils exactement)
- **Gardiens \`G1..G15\`** (43 profils) · **Rêves \`R1..R10\`** (31 profils) · **Nids de Croissance \`M1..M5\`** (19 profils) · **Slots Migration \`SLOT_BUG_CERVEAU\` & \`SLOT_COLONISATION_GARDIENS\`** (5 profils — \`Colonisation B\` et les anciens profils \`E\` sont supprimés en v5.3, plus 2 profils additionnels sur les lisières portant le total à 100).
- Chaque profil possède : \`nom\`, \`cycle\`, \`cablage\`, \`fenetre\`, \`primitive\` (parmi les 8 primitives : \`MOD_SEUIL\`, \`CREATION_ENTITE\`, \`DEPLACEMENT\`, \`MOD_PUISSANCE\`, \`MOD_APPRENTISSAGE\`, \`PERMUTATION_PISTE\`, \`PARTAGE_INFO_ETAT_GARDIEN\`, \`MOD_LOI_DU_COEUR\`), \`tags\`, \`requires_options\`, \`texte\` et \`temoin\`.

### 4.2. Invariants Mécaniques Cœur Consolidés (Socle des 25 Arbitrages)
- **Tirage & Dés épurés (Étape 1)** : Paquet contenant les cartes Machine hors Siège + toutes les cartes Sabotage acquises. Seul un joueur ayant tiré une **carte Machine** lance 2D6 sous paravent et retient \`M = min(D1, D2)\` (ou \`max\` sous Loi). Si le rang \`M\` porte un Rêve en \`3.2\`, la machine est annulée et le Rêve s'ouvre.
- **Sabotage par dilution permanente** : Toutes les cartes Sabotage sont identiques et sans effet propre (réserve illimitée). **1 Sabotage acquis** (\`4.1\`, \`4.2\`, Gardien) = \`+1\` carte Sabotage mise de côté et intégrée **définitivement** au paquet Machine au remélange de \`6.3\` (allume \`3. Sabotage\`). **1 carte Sabotage piochée à l'Étape 1** = 1 action du Contremaître perdue ce tour-ci (puis remélangée en \`6.3\`).
- **Gouvernance unitaire** : Chaque Tuile (\`G\`, \`R\`, \`M\`) et piste de Migration est décidée uniquement par le joueur de son \`peuple_origine\` (\`origine\`). Zéro vote de groupe.
- **Furtivité à 4 emplacements jumeaux** : 2 emplacements jumeaux par rive (max 2 Défenseurs/case). **Entrer** sur la case (toute face) tire l'éventuel autre Défenseur sur l'emplacement jumeau du même bord et oriente l'unique action du binôme en \`4.1\` (sur la parcelle de cette seule rive) ; **retourner** de *réflexion* à *définitif* se fait strictement sur place sans déplacement.
- **Combat d'un seul tenant & Chaîne des parades** : Ordre Tactiques \`1 → 6\` puis Sièges (Abatteuse avant Bulldozer sur un même rayon ; libre entre rayons distincts). Chaque machine résout d'un seul tenant ses cibles (lues depuis sa position réelle à l'instant de l'attaque en sautant les Routes Forestières), ses frappes (\`1° Jaguar [2 bleus] → 2° Harpie → 3° Piège Embuscade [si Défense totale >= 1] → 4° Parade classique [défausse immédiate des Insectes manquants]\`), son avancée \`T3/T6\` et son gain \`+1 Rouge\` \`T4/T5/T6\`. **Zéro dette d'Insectes et zéro verrouillage des parcelles ciblées** (seul un Piège déjà déclenché ce tour ne peut plus payer un coût volontaire avant son retrait en \`5.3\`).
- **Siège \`T4\` & Apprentissage (\`6.1 / 6.2\`)** : Toute machine sur la dernière parcelle non rasée est en Siège irréversible : son attaque reste autonome même si \`T4\` est éjectée, et en \`6.1\` elle génère normalement de l'Apprentissage sur \`T4\` tant que \`T4\` figure sur la piste (\`+1\`/parcelle réellement endommagée \`+1\`/Rouge acquis \`-1\`/Bleu présent, plancher 0). Retraits volontaires avant Bugs ; remise à zéro de 100 % des jetons Apprentissage en \`6.2\` dans tous les cas.
- **Cascades à plat (\`1 → 6\`) & Fin de partie** : Fin complète de l'effet/Nid en cours, marquage immédiat à l'ouverture, balayage croissant \`1..6\` répété, Faces 2 autonomes. Seuil de Réveil fixe calculé à la mise en place (inactif si \`< 3\` Gardiens). Vérification en fin de \`5.3\` (+ exception \`R9 B\` en \`6.2\`).

---

## 5. Règles d'Or de Maintenance pour une IA Collaboratrice

1. **Synchronisation obligatoire des 4 couches** : Toute évolution de règle doit mettre à jour simultanément \`data/livret_v5_3.js\` (\`renderDidacticRulebook\` **ET** \`REGLES_COEUR_SYNTHESE\`), \`data/amazonia_data_v5_3.js\` (\`CATALOGUE_TUILES\`, \`VERSION_CHANGELOG\`, \`SPEC_FORMELLE_V5_3\`), \`data/catalog_v5_3.json\` et \`data/spec_formelle_v5_3.json\`.
2. **Patchs différentiels via Node \`vm\` + \`JSON.stringify\`** : Ne jamais réécrire tout le catalogue à la main dans une réponse LLM ni injecter des chaînes JS par regex brutes (risque de casse sur les apostrophes \`'\` vs \`’\`). Charger l'objet dans un contexte Node \`vm\`, muter les clés ciblées, resérialiser via \`JSON.stringify\` et vérifier par \`new vm.Script()\`.
3. **Couple \`texte\` + \`temoin\` & Faces 2 autonomes** : Ne jamais laisser \`temoin\` vide et toujours mettre à jour \`temoin\` quand \`texte\` change. Sur un Gardien double-face, le texte de la **Face 2** doit se suffire à lui-même sans renvoyer à la Face 1 cachée.
4. **Encodage & PowerShell** : Écrire tous les fichiers en **UTF-8 sans BOM** avec fins de ligne \`\\n\`. Sous Windows PowerShell 5.1, préférer l'exécution d'un fichier script (\`node "scripts/xxx.js"\`) aux one-liners \`node -e "..."\` (qui altèrent les guillemets doubles).
`;
  fs.writeFileSync(CONTEXT_MD_PATH, md.replace(/\r\n/g, '\n'), 'utf8');
  console.log('  [OK] AMAZONIA_STUDIO_CONTEXT.md écrit à la racine du dépôt');
}

function auditAgainstPreAuditCommit() {
  console.log('\n=== 3. DIFF DES MÉCANIQUES DE TUILES CONTRE LE COMMIT PRÉ-AUDIT (ab987e0) ===');
  const oldJs = execSync('git show ab987e0:data/amazonia_data_v5_3.js', { encoding: 'utf8', cwd: ROOT });
  const oldCtx = vm.createContext({ window: {} });
  vm.runInContext(oldJs + '\n;globalThis.__CAT = CATALOGUE_TUILES;', oldCtx);

  const curCtx = vm.createContext({ window: {} });
  vm.runInContext(fs.readFileSync(JS_PATH, 'utf8') + '\n;globalThis.__CAT = CATALOGUE_TUILES;', curCtx);

  let changedPrimitives = 0;
  for (const [id, curT] of Object.entries(curCtx.__CAT)) {
    const oldT = oldCtx.__CAT[id];
    if (!oldT) continue;
    for (const [l, curP] of Object.entries(curT.profils)) {
      const oldP = oldT.profils[l];
      if (!oldP) continue;
      if (oldP.primitive !== curP.primitive || oldP.fenetre !== curP.fenetre) {
        changedPrimitives++;
        console.log(`  • ${id}_${l} (${curP.nom}) : [${oldP.fenetre} | ${oldP.primitive}] -> [${curP.fenetre} | ${curP.primitive}]`);
      }
    }
  }
  console.log(`  Total profils avec fenêtre/primitive ajustée depuis ab987e0 : ${changedPrimitives} / 100`);
}

patchSiegeLearning();
writeContextMarkdown();
auditAgainstPreAuditCommit();