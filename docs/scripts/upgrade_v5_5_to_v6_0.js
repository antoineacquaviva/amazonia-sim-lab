'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..', '..');
const DOCS_DATA = path.join(ROOT, 'docs', 'data');

const SRC_SPEC = path.join(DOCS_DATA, 'spec_formelle_v5_5.json');
const SRC_CAT = path.join(DOCS_DATA, 'catalog_v5_5.json');
const SRC_JS = path.join(DOCS_DATA, 'amazonia_data_v5_5.js');

const DST_SPEC = path.join(DOCS_DATA, 'spec_formelle_v6_0.json');
const DST_CAT = path.join(DOCS_DATA, 'catalog_v6_0.json');
const DST_JS = path.join(DOCS_DATA, 'amazonia_data_v6_0.js');

function writeUtf8Lf(filePath, content) {
  const normalized = content.replace(/\r\n/g, '\n');
  fs.writeFileSync(filePath, normalized, { encoding: 'utf8' });
}

// 1. Load v5.5 source layers cleanly via JSON.parse & Node vm
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

// 2. Build spec_formelle_v6_0.json (schema_version 6.0.0-alpha)
spec.schema_version = '6.0.0-alpha';
spec.date_consolidation = '2026-11-21';
spec.architecture_reference.repousse_finale_base = 0;
spec.architecture_reference.score_final = 'arbres_debout_uniquement (0 Repousse Finale automatique de base)';

spec.principes_transverses.cascades_gardiens_a_plat =
  "On résout toujours intégralement l'action ou la tuile en cours avant d'examiner la Piste des Gardiens (signal binaire allumé/éteint par case 1..6, sans cumul de cardinalité). Partition stricte des 6 déclencheurs (« 1 événement = au plus 1 déclencheur ») : en 3.2 (par carte révélée) 3. Sabotage > 6. Insecte (déviation sur la Réglette des Tactiques) > 5. Rêve (dé M sur rang occupé par un Rêve, quel que soit le choix Bloquer/Avancer) ; en 4.1 Furtivité et en 4.2 production de Nid aucun déclencheur n'est allumé ; en 5.1/5.2 (par frappe bloquée) 2. Piégeage (Piège armé) > 6. Insecte (Parade classique avec dépense >= 1 Insecte) > 1. Parade (Défenseurs seuls). Case 4. Gardien : 1re ouverture du tour de chaque autre Gardien distinct (anti-boucle conservé). Pari uniforme de 0, 1 ou 2 Défenseurs maximum par Gardien construit en 2.2 (glissés sous la tuile à chaque déclenchement). Balayage à plat de 1 à 6.";

for (const step of spec.etapes_tour) {
  if (step.numero === 1) {
    step.nom = 'Acte / Réglette, Ratissage, Distribution et Dés secrets (1.1–1.3)';
    step.regles = [
      "1.0 Réglette des Tactiques réversible par blocs : Acte 1 (Tours 1–4, Face A) place les cases 1, 2, 3 en mode CHARGE et les cases 4, 5, 6 en mode ASSAUT. Au début du Tour 5, retournez la Réglette sur sa Face B (Acte 2, Tours 5–8) : permutation des deux blocs — cases 1, 2, 3 en mode ASSAUT et cases 4, 5, 6 en mode CHARGE. Actions fixes sur les deux faces : 1/4 = Sur place (mod_seuil = 0), 2/5 = Devant (mod_seuil = 0), 3/6 = En avançant (SUR_PLACE + DEVANT, avancée +1, mod_seuil = -1).",
      "1.1 Machines en Ratissage : dès qu'une machine se trouve sur la dernière parcelle non rasée de son rayon, elle est retournée définitivement sur sa face Ratissage (carte retirée du paquet Machine). Le Ratissage est détaché de la case 1 et opère en mode ASSAUT permanent : attaque Sur place (mod_seuil = 0), tous ses jetons Puissance actifs dont son +1 imprimé (traité comme +1 jeton Puissance rouge, jetons antérieurs conservés), aucun gain de jeton Puissance. Sous l'option Abatteuse en Ratissage, si sa parcelle cible n'a plus d'Arbre debout, elle arrache 1 Souche (préservant la création de Route Forestière et le cycle de Repli).",
      "1.2 Distribution : chaque joueur hors pénurie pioche secrètement 1 carte du paquet Machine (incluant toutes les cartes Sabotage intégrées définitivement). Une carte Sabotage tirée n'active aucune machine (action du Contremaître perdue). S'il reste moins de cartes que de joueurs, distribution dans le sens horaire à partir du peuple ayant le plus d'Arbres debout.",
      "1.3 Dés secrets sous paravent fermé (silence complet) : chaque joueur ayant reçu une carte Machine lance ses 2D6 et retient la plus petite valeur (Dé MIN unique du Tour 1 au Tour 8, modifié par les éventuelles Lois actives), qui désigne le rang 1..6 sur la Réglette des Tactiques."
    ];
  } else if (step.numero === 2) {
    step.regles = [
      "2.1 / 2.2 Pose sous paravent fermé : 1er Défenseur irrévocable sur sa Forêt ou ses 2 lisières ; puis Défenseur de portée globale (réflexion -> choix définitif). Anti-blocage : pose interdite sur Route Forestière, tuile construite/pleine/inconstructible ou rive Furtivité bordant une Route.",
      "Furtivité libre (A1) : 4 emplacements indépendants par case de Furtivité (2 rives de 2 cases, maximum 2 Défenseurs par rive, jusqu'à 4 Défenseurs par case). Aucun déplacement forcé ni glissement sur case jumelle : chaque joueur pose librement son Défenseur sur l'une des 2 cases de la rive qu'il choisit.",
      "2.2 Portée globale, Rêves & Pari sur les Gardiens : pose en réflexion puis définitive partout sur le plateau, y compris sur un Rêve de la Réglette des Tactiques (pour ouvrir le choix exclusif Bloquer OU Avancer en 3.2) ou en pari d'activation sur tout Gardien déjà construit (si >= 1 Animal Sauvage M/R/O ; 0, 1 ou 2 Défenseurs maximum par Gardien, glissés sous la tuile à chaque déclenchement). Un Gardien sans Défenseur reste inactif ce tour-ci."
    ];
  } else if (step.numero === 3) {
    step.regles[2] =
      "3.1 Rêve : un Rêve construit se pose par-dessus la case libre la plus à droite de la Réglette des Tactiques fixe 1..6 (case 6, puis case 5 si 6 est déjà occupée par un Rêve, etc.). Aucune Tactique n'est éjectée (les Insectes restent sur leur numéro de case imprimé). Ce Rêve est immédiatement présent sur la piste pour l'étape 3.2.";
    step.regles[4] =
      "3.2 Révélation simultanée (paravents ouverts) — partition stricte « 1 carte révélée = au plus 1 déclencheur » : (a) 3. Sabotage si la carte révélée est un Sabotage ; (b) sinon 6. Insecte si un pion Insecte de la Réglette des Tactiques (SLOT_BUG_CERVEAU=B) dévie le dé M de ±1 rang ; (c) sinon 5. Rêve si le dé retenu M d'une carte Machine pointe sur un rang occupé par une tuile Rêve (quel que soit le choix Bloquer ou Avancer). Résolution des Rêves (choix exclusif Bloquer OU Avancer) : pour chaque Rêve portant >= 1 Défenseur et visé par >= 1 machine non déviée, le Peuple Onirique choisit une seule issue — BLOQUER (chaque Défenseur posé annule 1 machine de ce rang en priorisant la plus menaçante ; les machines restantes exécutent la Tactique imprimée dessous ; le Rêve ne bouge pas) OU AVANCER (1 seul Défenseur suffit quel que soit le nombre de machines ; aucune machine n'est annulée et toutes exécutent la Tactique imprimée dessous ; le Rêve saute vers la 1re case libre à sa gauche). Par défaut, le pouvoir propre du Rêve s'active sur les deux choix.";
  } else if (step.numero === 4) {
    step.regles[0] =
      "4.1 Furtivité libre (A1) : sur chaque case de Furtivité, chacune des 2 rives est évaluée indépendamment et déclenche son action uniquement si elle porte un binôme complet (2 Défenseurs sur ses 2 cases ; un pion seul ne déclenche rien). Si les 4 cases sont occupées (2 binômes complets), les 2 rives s'exécutent toutes les deux. Chaque rive déclenchée est gouvernée par le joueur de son bord : Piège si aucune machine sur la parcelle en face, OU Sabotage si au moins 1 machine y stationne et aucune n'est active ce tour (Ratissage = active ; une machine annulée par Bloquer en 3.2 est inactive et sabotable). Aucun déclencheur Gardien n'est allumé en 4.1.";
  } else if (step.numero === 5) {
    step.regles[0] =
      "Ordre des machines : Réglette des Tactiques de la case 1 à la case 6, puis machines en Ratissage (mode ASSAUT permanent, détaché de la case 1). Sur un même rayon au même rang (ou en Ratissage), l'Abatteuse agit toujours avant le Bulldozer ; entre rayons distincts au même rang, ordre libre entre les joueurs concernés.";
    step.regles[1] =
      "Modes CHARGE et ASSAUT (Réglette réversible) : chaque machine est résolue d'un seul tenant (lecture dynamique des cibles -> frappes -> avancée éventuelle sur 3/6 -> gain éventuel de jeton Puissance). En mode CHARGE (Acte 1 cases 1–3 ; Acte 2 cases 4–6) : les jetons Puissance déjà sur la machine sont ignorés dans le calcul du seuil de parade ; si l'activation inflige au moins 1 dégât effectif (>= 1 Arbre coupé ou >= 1 Souche arrachée), la machine gagne +1 jeton Puissance (plafonné à +1 par activation même sur double cible 3/6). En mode ASSAUT (Acte 1 cases 4–6 ; Acte 2 cases 1–3 ; et Ratissage permanent) : tous les jetons Puissance comptent dans le seuil de parade ; aucun jeton Puissance n'est gagné.";
    step.regles[4] =
      "Création d'une Route Forestière (0 Arbre et 0 Souche après un Bulldozer, ou après une Abatteuse en Ratissage arrachant la dernière Souche sous l'option correspondante) : recul automatique des machines présentes vers la prochaine parcelle non rasée côté bordure, ou vers le cœur uniquement si tout est déjà rasé côté bordure (maintien irréversible du mode Ratissage ; retrait définitif de la partie si tout le rayon est rasé).";
    step.regles[6] =
      "Issue des paris Gardiens, Bouclier de lisière & Vérification de fin de partie (5.3) : retrait des Pièges déclenchés, puis résolution des paris Gardiens (0 Défenseur restant -> pari gagné : le Gardien reste en piste et passe Face 2 s'il est double-face ; >= 1 Défenseur restant -> pari perdu : si Bouclier de lisière SLOT_COLONISATION_GARDIENS=B et >= 1 Insecte sur sa case, défausser 1 Insecte pour garder le Gardien en piste sur sa face actuelle tout en laissant le pari PERDU, sinon retour immédiat en lisière Face 1). Test de fin de partie : priorité absolue au Tour 8 ; aux Tours 1..7, Sommeil du Contremaître (toutes les tuiles Rêves en jeu en bloc continu 1..k) ou Réveil de la Forêt 100 % Piste des Gardiens (les N Défenseurs de la table engagés en 2.2 sur les Gardiens et aucun pari perdu). Si atteint : fin immédiate de la partie et décompte des Arbres debout (0 Repousse Finale automatique de base).";
  } else if (step.numero === 6) {
    step.regles[0] =
      "Ménage systématique (6.2) : Réglette des Tactiques 1..6 fixe (retournée sur Face B au début du Tour 5 pour l'Acte 2), retour en main de tous les Défenseurs (y compris ceux posés sur des Rêves ou Gardiens et ceux glissés sous une tuile) et remise à zéro des modificateurs transitoires.";
  }
}

spec.arbitrages_valides.A01 =
  "Lecture unique du Dé MIN (Tours 1 à 8) sous paravent : seul un joueur ayant tiré une carte Machine retient M = min(D1, D2) (ou max sous Loi). Ce rang 1..6 désigne la case visée sur la Réglette des Tactiques.";
spec.arbitrages_valides.A02 =
  "Rêve sur dé Machine (v6.0) : un Rêve muni d'au moins 1 Défenseur et visé par >= 1 machine non déviée en 3.2 propose au Peuple Onirique le choix exclusif BLOQUER ou AVANCER (max 1 ouverture par Rêve et par tour par défaut).";
spec.arbitrages_valides.A03 =
  "Furtivité libre A1 (v6.0) : 4 emplacements indépendants par case (2 rives de 2 cases, max 2 Défenseurs par rive, zéro glissement sur case jumelle). En 4.1, une rive déclenche son action uniquement si elle porte un binôme complet (2 Défenseurs sur ses 2 cases ; un pion seul ne déclenche rien). Si les 4 cases sont occupées (2 binômes complets), les 2 rives s'exécutent toutes les deux.";
spec.arbitrages_valides.A10 =
  "Autonomie du Ratissage en Assaut permanent (v6.0) : pion double face retourné définitivement sur la dernière parcelle non rasée ; détaché de la case 1, il attaque Sur place (mod_seuil = 0) en mode ASSAUT permanent (tous les jetons Puissance actifs dont son +1 imprimé, aucun gain de jeton Puissance). Sous l'option Abatteuse en Ratissage, si la parcelle n'a plus d'Arbre debout, elle arrache 1 Souche (préservant Route Forestière et Repli).";
spec.arbitrages_valides.A11 =
  "Réglette des Tactiques réversible par blocs & placement des Rêves (v6.0) : actions fixes 1/4 Sur place (0), 2/5 Devant (0), 3/6 En avançant (+1 parcelle, -1 seuil). Acte 1 (Tours 1–4, Face A) : 1–3 CHARGE / 4–6 ASSAUT. Acte 2 (Tours 5–8, Face B retournée début Tour 5) : 1–3 ASSAUT / 4–6 CHARGE. Un Rêve construit en 3.1 se pose par-dessus la case libre la plus à droite (6, puis 5, etc.) sans éjecter les Tactiques ni déplacer les Insectes.";
spec.arbitrages_valides.A14 =
  "Éveil / Réveil de la Forêt 100 % Piste des Gardiens (v6.0) : actif uniquement si >= 1 Peuple Animal Sauvage (M, R ou O) est autour de la table, aux Tours 1..7 (priorité absolue au Tour 8). En 5.3, la Forêt s'éveille si les N Défenseurs de la table ont tous été engagés en 2.2 sur la Piste des Gardiens et qu'aucun pari n'est perdu (0 Défenseur restant). Un Gardien sauvé par Bouclier de lisière (SLOT_COLONISATION_GARDIENS=B) reste en piste sur sa face actuelle mais son pari reste PERDU.";
spec.arbitrages_valides.A15 =
  "Test de fin de partie & Suppression de la Repousse Finale de base (5.3, v6.0) : priorité absolue au Tour 8 (fin TOUR_8) ; aux Tours 1..7, vérification directe après issue des paris Gardiens de Sommeil du Contremaître (tous les Rêves en jeu en bloc continu cases 1..k) ou de Réveil de la Forêt 100 % Gardiens. En fin de partie, 0 Souche ne repousse automatiquement dans le cœur : le score compte uniquement les Arbres debout.";
spec.arbitrages_valides.A21 =
  "Rêves en choix exclusif « Bloquer OU Avancer » (v6.0) : en 3.2, pour chaque Rêve portant >= 1 Défenseur et visé par >= 1 machine non déviée, le Peuple Onirique choisit une seule issue : BLOQUER (chaque Défenseur annule 1 machine du rang en priorisant la plus menaçante ; les machines restantes jouent la Tactique dessous ; le Rêve ne bouge pas) OU AVANCER (1 seul Défenseur suffit ; 0 machine annulée, toutes jouent la Tactique dessous ; le Rêve saute vers la 1re case libre à sa gauche). Déclencheur 5. Rêve inchangé (allumé dès qu'une machine non déviée pointe sur un rang Rêve, quel que soit le choix). Pouvoir propre du Rêve actif par défaut sur les deux choix.";
spec.arbitrages_valides.A22 =
  "Pari uniforme sur les Gardiens & Partition stricte des 6 déclencheurs (v6.0) : actif si >= 1 Animal Sauvage (M/R/O) est à la table. Pari uniforme UNIFORM_MAX_2 (0, 1 ou 2 Défenseurs maximum par Gardien construit cases 1..6, glissés sous la tuile à chaque déclenchement). Partition stricte (« 1 événement = au plus 1 déclencheur ») : en 3.2 Sabotage > Insecte sur Tactiques > Rêve ; en 4.1 et 4.2 Nids aucun déclencheur ; en 5.1/5.2 Piégeage > Insecte en Parade >= 1 Insecte > Parade par Défenseurs seuls ; 4. Gardien sur 1re ouverture du tour de chaque autre Gardien distinct (DISTINCT_OPEN_1, anti-boucle conservé). En 5.3 : pari gagné -> reste en piste et passe Face 2 si double-face ; pari perdu -> retour en lisière Face 1, sauf Bouclier de lisière (SLOT_COLONISATION_GARDIENS=B) qui défausse 1 Insecte de la case pour garder le Gardien en piste sur sa face actuelle, le pari restant PERDU.";
spec.arbitrages_valides.A23 =
  "Réglette des Tactiques réversible Face A/B, Charge/Assaut & Déviation par Insectes (v6.0) : en mode CHARGE les jetons Puissance existants sont ignorés au seuil et +1 jeton Puissance est gagné uniquement sur >= 1 dégât effectif (plafonné à +1/activation) ; en mode ASSAUT tous les jetons Puissance comptent au seuil et 0 jeton n'est gagné. SLOT_BUG_CERVEAU=B (Déviation ±1 en 3.2) et SLOT_COLONISATION_GARDIENS=B (Bouclier de lisière en 5.3) sont actifs par défaut.";
spec.arbitrages_valides.A25 =
  "Séquence des attaques (v6.0) : Réglette 1..6 (mode CHARGE ou ASSAUT selon l'Acte) puis Ratissages (ASSAUT permanent détaché de la case 1) ; Abatteuse avant Bulldozer sur un même rayon, libre entre rayons distincts ; machine résolue d'un seul tenant.";

writeUtf8Lf(DST_SPEC, JSON.stringify(spec, null, 2) + '\n');

// 3. Build catalog_v6_0.json
const catOut = {
  schema_version: '6.0.0-alpha',
  total_emplacements: catalog.total_emplacements,
  total_profils: catalog.total_profils,
  topologies: catalog.topologies,
  formule_seuil_parade:
    "Seuil imprimé fixe + modificateur de Tactique (0 sur 1/2/4/5, -1 sur 3/6) + jetons Puissance actifs en ASSAUT/Ratissage (ignorés en mode CHARGE) - jetons Surchauffe bleus. Chaîne stricte : Bond du Jaguar -> Piquée de la Harpie -> Piège -> Parade classique (Défenseurs + défausse immédiate des Insectes manquants).",
  verification_fin_de_partie:
    "Vérification unique à la fin des attaques (5.3, après résolution des paris Gardiens et Bouclier de lisière éventuel). Priorité absolue au Tour 8 (CAUSE_TOUR_8). Aux Tours 1..7 : Sommeil du Contremaître (tous les Rêves en jeu en bloc continu cases 1..k de la Réglette des Tactiques) ou Réveil de la Forêt 100 % Piste des Gardiens (actif si >= 1 Peuple Animal Sauvage M/R/O : les N Défenseurs de la table engagés en 2.2 sur la Piste des Gardiens et aucun pari perdu). Score final immédiat = Arbres debout (0 Repousse Finale automatique de base).",
  regle_piege: catalog.regle_piege,
  furtivite_4_1_autorise_ciblee_sans_machine: catalog.furtivite_4_1_autorise_ciblee_sans_machine,
  verrouillage_etape_5_parcelles_ciblees: catalog.verrouillage_etape_5_parcelles_ciblees,
  bonus_constructeur_n3: catalog.bonus_constructeur_n3,
  regle_furtivite:
    "Furtivité libre (A1) : 4 emplacements indépendants par case (2 rives de 2 cases, max 2 Défenseurs par rive, aucun glissement automatique). En 4.1, une rive déclenche son action uniquement si elle porte un binôme complet (2 Défenseurs sur ses 2 cases ; un pion seul ne déclenche rien). Si les 4 cases sont occupées, les 2 rives s'exécutent toutes les deux.",
  gouvernance_autorite: catalog.gouvernance_autorite,
  date_consolidation: '2026-11-21',
  spec_formelle: spec,
  spec_formelle_v6_0: spec,
};
writeUtf8Lf(DST_CAT, JSON.stringify(catOut, null, 2) + '\n');

// 4. Prepend v6.0 entry to VERSION_CHANGELOG
const catTiles = extracted.CATALOGUE_TUILES;
const changelog = extracted.VERSION_CHANGELOG;
if (changelog.length > 0 && changelog[0].version === 'v5.5') {
  changelog[0].date = 'Socle figé précédent (2026-11-20)';
}
const v60Entry = {
  version: 'v6.0',
  date: 'Branche expérimentale exp/socle-v6 (2026-11-21)',
  titre: 'Refonte du socle cœur v6.0 : Réglette réversible Charge/Assaut, Rêves Bloquer/Avancer, Furtivité libre & 0 Repousse Finale',
  resume:
    "Évolution majeure du cœur de jeu en branche expérimentale (schema_version 6.0.0-alpha, calibrée d'abord en Mode 2 à tuiles neutres sans toucher au socle figé v5.5 sur main) : Réglette des Tactiques réversible en 2 Actes (Face A Tours 1–4 : 1–3 Charge / 4–6 Assaut ; Face B Tours 5–8 : permutation 1–3 Assaut / 4–6 Charge ; Ratissage détaché en Assaut permanent), Rêves en choix exclusif Bloquer OU Avancer avec saut vers la 1re case libre à gauche, Furtivité libre à 2 rives indépendantes (1 ou 2 binômes complets par case, zéro glissement forcé) et suppression de la Repousse Finale automatique de base (score = Arbres debout).",
  deltas: [
    {
      domaine: 'Réglette des Tactiques réversible par blocs (Charge / Assaut) & Ratissage',
      avant:
        'v5.5 : Piste fixe T1..T6 asymétrique (T4/T5/T6 donnaient +1 jeton rouge systématiquement) et Ratissage rattaché à T1 Sur place.',
      apres:
        'v6.0 : Lecture unique du Dé MIN (Tours 1–8). Actions fixes 1/4 Sur place (0), 2/5 Devant (0), 3/6 En avançant (+1 parcelle, -1 seuil). Face A (Acte 1, Tours 1–4) : 1–3 CHARGE / 4–6 ASSAUT ; Face B (Acte 2, Tours 5–8, retournée début Tour 5) : 1–3 ASSAUT / 4–6 CHARGE. CHARGE ignore les jetons Puissance existants au seuil et donne +1 jeton uniquement si >= 1 dégât effectif (plafonné à +1/activation). ASSAUT active tous les jetons Puissance sans gain. Ratissage détaché de la case 1 en ASSAUT permanent (+1 imprimé).',
    },
    {
      domaine: 'Rêves en choix exclusif « Bloquer OU Avancer »',
      avant:
        'v5.5 : Un Rêve annulait 1 machine par Défenseur et avançait automatiquement uniquement si toutes les machines du rang étaient annulées.',
      apres:
        'v6.0 : Pour chaque Rêve muni d’au moins 1 Défenseur et visé en 3.2, le Peuple Onirique tranche : BLOQUER (1 Défenseur annule 1 machine prioritaire, le Rêve ne bouge pas) OU AVANCER (1 seul Défenseur suffit, 0 machine annulée, toutes jouent la Tactique dessous, et le Rêve saute vers la 1re case libre à sa gauche). Déclencheur 5. Rêve inchangé.',
    },
    {
      domaine: 'Furtivité libre (2 rives indépendantes)',
      avant:
        'v5.5 : Entrer sur une case de Furtivité attirait de force le partenaire sur la case jumelle (max 2 Défenseurs et 1 seule action par case).',
      apres:
        'v6.0 : Zéro glissement forcé. Les 4 emplacements (2 rives de 2 cases) sont libres. En 4.1, chaque rive déclenche son action uniquement si elle forme un binôme complet (2 Défenseurs ; un pion seul ne déclenche rien). Si les 4 emplacements sont occupés, les 2 rives s’exécutent toutes les deux.',
    },
    {
      domaine: 'Suppression de la Repousse Finale de base',
      avant:
        'v5.5 : En fin de partie, 1 Souche par parcelle non rasée repoussait automatiquement en Arbre avant le score.',
      apres:
        'v6.0 : 0 Repousse Finale automatique de base — le score compte uniquement les Arbres debout. La règle de l’Abatteuse en Ratissage (arrache 1 Souche s’il n’y a plus d’Arbre sous l’option correspondante) est conservée intacte pour préserver les Routes Forestières et le Repli.',
    },
  ],
};
const filteredChangelog = [v60Entry, ...changelog.filter((c) => c.version !== 'v6.0')];

// 5. Emit docs/data/amazonia_data_v6_0.js and validate with new vm.Script
const outJs = [
  '// =========================================================================',
  '// data/amazonia_data_v6_0.js — Données canoniques Amazonia v6.0-alpha (Expérimental · 6 profils · 192 châssis · 32 emplacements)',
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
  `const SPEC_FORMELLE_V6_0 = ${JSON.stringify(spec, null, 2)};`,
  '',
].join('\n');

new vm.Script(outJs, { filename: 'amazonia_data_v6_0.js' });
writeUtf8Lf(DST_JS, outJs);

console.log('Generated v6.0 Studio data layers successfully:');
console.log(' -', path.relative(ROOT, DST_SPEC));
console.log(' -', path.relative(ROOT, DST_CAT));
console.log(' -', path.relative(ROOT, DST_JS));
