'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..', '..');
const DOCS_DATA = path.join(ROOT, 'docs', 'data');

const DST_SPEC = path.join(DOCS_DATA, 'spec_formelle_v6_0.json');
const DST_CAT = path.join(DOCS_DATA, 'catalog_v6_0.json');
const DST_JS = path.join(DOCS_DATA, 'amazonia_data_v6_0.js');

function writeUtf8Lf(filePath, content) {
  const normalized = content.replace(/\r\n/g, '\n');
  fs.writeFileSync(filePath, normalized, { encoding: 'utf8' });
}

// 1. Load current v6.0 Studio layers cleanly via JSON.parse & Node vm
const spec = JSON.parse(fs.readFileSync(DST_SPEC, 'utf8'));
const catalog = JSON.parse(fs.readFileSync(DST_CAT, 'utf8'));
const jsSrc = fs.readFileSync(DST_JS, 'utf8');

const sandbox = { window: {} };
vm.createContext(sandbox);
const extracted = vm.runInContext(
  jsSrc +
    '\n;({ PEUPLES, MATRICE_PAIRES, TOPOLOGIES_PISTE_SPEC, CHASSIS_AXES_SPEC, CATALOGUE_TUILES, VERSION_CHANGELOG });',
  sandbox
);

// 2. Upgrade spec_formelle_v6_0.json -> schema_version 6.1.0-alpha
spec.schema_version = '6.1.0-alpha';
spec.date_consolidation = '2026-11-22';
spec.architecture_reference.repousse_finale_base = 0;
spec.architecture_reference.score_final = 'arbres_debout_uniquement (0 Repousse Finale automatique de base)';

spec.principes_transverses.pont_routier_routes_forestieres =
  "Le long d'un rayon de Forêt, toute Route Forestière est systématiquement sautée : viser devant, avancer, reculer ou migrer désignent toujours la prochaine parcelle non rasée dans cette direction. Dès qu'un rayon est intégralement transformé en Routes Forestières (ses 2 machines définitivement retirées), sa zone de Furtivité au pied du rayon devient fermée et inaccessible en 2.1 et 2.2.";

spec.principes_transverses.suppression_dette_et_verrouillage =
  "Zéro Insecte engagé et zéro verrouillage des parcelles ciblées. Les Insectes requis lors d’une parade classique sont défaussés immédiatement à la frappe. Tant qu'un Insecte est sur le plateau, il est libre. Tout Piège posé est autonome (aucune condition de présence sur la parcelle) : il pare exactement 1 frappe puis est défaussé aussitôt (SINGLE_STRIKE).";

spec.principes_transverses.cascades_gardiens_a_plat =
  "On résout toujours intégralement l'action ou la tuile en cours avant d'examiner la Piste des Gardiens (signal binaire allumé/éteint par case 1..6, sans cumul de cardinalité). Partition stricte des 6 déclencheurs (« 1 événement = au plus 1 déclencheur ») : en 3.2 (par carte révélée) 3. Sabotage > 6. Insecte (déviation ±1 sur la Réglette des Tactiques) > 5. Rêve (REVE_TRIG=ACTIF : s'allume uniquement lorsqu'un Rêve portant >= 1 Défenseur annule effectivement >= 1 machine non déviée en 3.2 ; un Rêve sans Défenseur est totalement inerte) ; en 4.1 Furtivité et en 4.2 production de Nid aucun déclencheur n'est allumé ; en 5.1/5.2 (par frappe bloquée) 2. Piégeage (Piège autonome SINGLE_STRIKE défaussé aussitôt) > 6. Insecte (Parade classique avec dépense >= 1 Insecte) > 1. Parade (Défenseurs seuls ou parade automatique). Case 4. Gardien : 1re ouverture du tour de chaque autre Gardien distinct (anti-boucle conservé). Pari uniforme de 0, 1 ou 2 Défenseurs maximum par Gardien construit en 2.2 (glissés sous la tuile à chaque déclenchement). Balayage à plat de 1 à 6.";

for (const step of spec.etapes_tour) {
  if (step.numero === 1) {
    step.nom = 'Acte / Réglette, Distribution et Dés secrets (1.0–1.3)';
    step.regles = [
      "1.0 Réglette des Tactiques réversible par blocs : Acte 1 (Tours 1–4, Face A) place les cases 1, 2, 3 en mode CHARGE et les cases 4, 5, 6 en mode ASSAUT. Au début du Tour 5, retournez la Réglette sur sa Face B (Acte 2, Tours 5–8) : permutation des deux blocs — cases 1, 2, 3 en mode ASSAUT et cases 4, 5, 6 en mode CHARGE. Actions fixes sur les deux faces : 1/4 = Sur place (mod_seuil = 0), 2/5 = Devant (mod_seuil = 0), 3/6 = En avançant (SUR_PLACE + DEVANT, avancée +1, mod_seuil = -1).",
      "1.1 Élagage du test d'entrée en Ratissage : aucun passage en Ratissage n'est re-testé en début de tour (seule l'étape 6.3 fait basculer définitivement en Ratissage les machines situées sur la dernière parcelle non rasée de leur rayon). Mise en place canonique décalée (chassis_id = 24) : Bulldozer en parcelle 1, Abatteuse en parcelle 2 sur chaque rayon.",
      "1.2 Distribution : chaque joueur hors pénurie pioche secrètement 1 carte du paquet Machine (incluant toutes les cartes Sabotage intégrées définitivement). Une carte Sabotage tirée n'active aucune machine (action du Contremaître perdue). S'il reste moins de cartes que de joueurs, distribution dans le sens horaire à partir du peuple ayant le plus d'Arbres debout.",
      "1.3 Dés secrets sous paravent fermé (silence complet) : chaque joueur ayant reçu une carte Machine lance ses 2D6 et retient la plus petite valeur (Dé MIN unique du Tour 1 au Tour 8, modifié par les éventuelles Lois actives), qui désigne le rang 1..6 sur la Réglette des Tactiques."
    ];
  } else if (step.numero === 2) {
    step.nom = 'Pose des Défenseurs, Rêves et Furtivité par rayon (2.1–2.2)';
    step.regles = [
      "2.1 Première pose simultanée et fixe (paravent fermé) : chaque joueur place son 1er Défenseur irrévocable sur sa propre Forêt (parcelle non rasée), sur l'une des Tuiles de Synergie non construites de ses 2 lisières, sur un Rêve déjà présent sur la Réglette des Tactiques (1..6), ou sur une rive ouverte de Furtivité (Rive Piège ou Rive Sabotage, max 2 Défenseurs par rive) au pied de n'importe quel rayon non rasé (1..N). Seule la Piste des Gardiens reste réservée à la pose 2.2.",
      "Topologie de Furtivité (« Chaud vs Calme » par rayon) : au pied de chaque rayon de forêt r (1..N), la zone de Furtivité comporte 2 rives indépendantes de 2 emplacements — Rive Piège (max 2 Défenseurs) et Rive Sabotage (max 2 Défenseurs) — ouvertes à tout joueur de la table en 2.1 comme en 2.2 (zéro glissement automatique). Garde-fou piste rasée : dès qu'un rayon r est intégralement transformé en Routes Forestières (ses 2 machines retirées), sa zone de Furtivité est fermée et inaccessible en 2.1 et 2.2.",
      "2.2 Deuxième pose globale (réflexion -> choix définitif) : chaque joueur place son 2e Défenseur partout sur le plateau — Forêt non rasée, Tuile de Synergie en lisière, Rêve sur la Réglette des Tactiques (cumulable avec les Défenseurs posés en 2.1), rive ouverte de Furtivité d'un rayon non rasé, ou pari d'activation sur tout Gardien déjà construit (si >= 1 Animal Sauvage M/R/O ; 0, 1 ou 2 Défenseurs maximum par Gardien, glissés sous la tuile à chaque déclenchement). Un Gardien sans Défenseur reste inactif ce tour-ci."
    ];
  } else if (step.numero === 3) {
    step.regles[2] =
      "3.1 Rêve : un Rêve construit se pose par-dessus la case libre la plus à droite de la Réglette des Tactiques fixe 1..6 (case 6, puis case 5 si 6 est déjà occupée par un Rêve, etc.). Aucune Tactique n'est éjectée (les Insectes restent sur leur numéro de case imprimé). Ce Rêve est immédiatement présent sur la piste (sans Défenseur s'il vient d'être construit en 3.1).";
    step.regles[4] =
      "3.2 Révélation simultanée (paravents ouverts) — partition stricte « 1 carte révélée = au plus 1 déclencheur » : (a) 3. Sabotage si la carte révélée est un Sabotage ; (b) sinon 6. Insecte si un pion Insecte de la Réglette des Tactiques (SLOT_BUG_CERVEAU=B) dévie le dé M de ±1 rang ; (c) sinon 5. Rêve (REVE_TRIG=ACTIF figé) uniquement lorsqu'un Rêve portant >= 1 Défenseur s'active réellement en 3.2 en annulant au moins 1 machine sur une carte non déviée de ce rang (un Rêve sans Défenseur est totalement inerte). Résolution épurée des Rêves dans le socle (CLEAR_RANK_ONLY) : tout Rêve portant >= 1 Défenseur (posé en 2.1 et/ou 2.2) et visé par >= 1 machine applique uniquement le blocage — chaque Défenseur annule 1 machine du rang en priorisant la plus menaçante, les machines restantes exécutent la Tactique imprimée dessous, et le Rêve ne bouge pas (le déplacement des Rêves est porté exclusivement par les tuiles du Mode 4).";
  } else if (step.numero === 4) {
    step.regles[0] =
      "4.1 Furtivité « Chaud vs Calme » par rayon (1..N) : un pion seul sur une rive ne produit aucun effet (perdu à blanc) ; seule une rive portant un binôme complet de 2 Défenseurs est évaluée. Pour le rayon r, on compte m(r) = (cartes Machine du rayon r révélées en 3.2) + (machines du rayon r déjà en Ratissage permanent), soit 0, 1 ou 2. Garde-fou d'indépendance : m(r) dépend uniquement des cartes révélées à l'ouverture des paravents et des Ratissages actifs (ni une déviation d'Insecte ±1 en 3.2, ni une annulation par un Rêve en 3.2 ne modifie m(r) ; une carte Sabotage révélée en 3.2 ne compte pour aucun rayon). Rive Piège (pari « double menace ») : pari GAGNÉ si m(r) == 2 -> 1 jeton Piège est posé sur une parcelle non-Route (non piégée) du rayon r choisie uniquement par le joueur propriétaire du rayon r (gouvernance unitaire 1-clic, zéro débat) ; pari PERDU si m(r) == 0 ou 1. Rive Sabotage (pari « piste calme ») : pari GAGNÉ si m(r) == 0 -> 1 carte Sabotage est mise de côté pour rejoindre définitivement le paquet Machine au remélange 6.3 (sans allumer 3. Sabotage en 4.1) ; pari PERDU si m(r) == 1 ou 2.";
    step.regles[2] =
      "4.3 Migration des Insectes (sans Furtivité) : chaque Insecte présent sur un rayon de Forêt peut rester sur place (0 cran) ou se déplacer d'1 cran le long de son rayon vers une parcelle non rasée voisine (en sautant les Routes Forestières ; jusqu'à 2 crans avec L'Envol du Batará Suiveur). Les zones de Furtivité ne sont pas accessibles aux Insectes. On retourne chaque jeton déplacé sur sa face verso pour suivi, puis on remet tous les jetons à l'endroit en fin de Migration.";
    step.regles[3] =
      "4.3 Pistes centrales globales : depuis la dernière parcelle non rasée d'un rayon, 1 cran de Migration permet d'entrer en aller simple définitif sur n'importe quelle case 1..6 de la Réglette des Tactiques (Bug du Cerveau) ou de la Piste des Gardiens (Colonisation / Bouclier de lisière), sans limite de jetons par case.";
  } else if (step.numero === 5) {
    step.regles[0] =
      "Ordre des machines : Réglette des Tactiques de la case 1 à la case 6, puis machines en Ratissage (mode ASSAUT permanent, détaché de la case 1). Sur un même rayon au même rang (ou en Ratissage), l'Abatteuse agit toujours avant le Bulldozer ; entre rayons distincts au même rang, ordre libre entre les joueurs concernés.";
    step.regles[1] =
      "Modes CHARGE et ASSAUT (Réglette réversible) : chaque machine est résolue d'un seul tenant (lecture dynamique des cibles -> frappes -> avancée éventuelle sur 3/6 -> gain éventuel de jeton Puissance). En mode CHARGE (Acte 1 cases 1–3 ; Acte 2 cases 4–6) : les jetons Puissance déjà sur la machine sont ignorés dans le calcul du seuil de parade ; gain plafonné à +1 jeton Puissance par activation dès qu'au moins 1 frappe sur parcelle réelle non-Route n'est ni parée ni piégée (FRAPPE_NON_PAREE figé — une attaque Devant lancée hors-plateau depuis la dernière parcelle ne fait jamais gagner de jeton). En mode ASSAUT (Acte 1 cases 4–6 ; Acte 2 cases 1–3 ; et Ratissage permanent) : tous les jetons Puissance comptent dans le seuil de parade ; aucun jeton Puissance n'est gagné. Dégâts non parés : l'Abatteuse coupe TOUS les Arbres debout de la parcelle en Souches et ne touche jamais aux Souches (micro-règle souche supprimée) ; le Bulldozer coupe 1 Arbre en Souche puis retire toutes les Souches non protégées (0/0 = Route Forestière + Repli).";
    step.regles[2] =
      "Chaîne stricte des parades à chaque frappe : (1) Bond du Jaguar (Loi auto : 2 jetons bleus défaussés -> toutes frappes restantes de la machine parées + recul) -> (2) Piquée de la Harpie -> (3) Piège autonome SINGLE_STRIKE (dès qu'un jeton Piège est présent sur la parcelle attaquée, il se déclenche de lui-même même avec 0 Défenseur et 0 Insecte sur place, sans consommer les Défenseurs ou Insectes présents, pare exactement cette unique frappe, est immédiatement défaussé et allume uniquement 2. Piégeage) -> (4) Parade classique (Défenseurs seuls -> 1. Parade ; Défenseurs + défausse immédiate des Insectes manquants -> 6. Insecte).";
  } else if (step.numero === 6) {
    step.regles[0] =
      "Ménage systématique (6.2) : Réglette des Tactiques 1..6 fixe (retournée sur Face B au début du Tour 5 pour l'Acte 2), retour en main de tous les Défenseurs (y compris ceux posés en 2.1/2.2 sur des Rêves, en Furtivité ou sur les Gardiens et ceux glissés sous une tuile) et remise à zéro des modificateurs transitoires.";
    step.regles[1] =
      "Entrée en Ratissage & Clôture du tour (6.3) : passage du pion Coordonnateur au siège suivant, retournement définitif sur sa face Ratissage de toute machine située sur la dernière parcelle non rasée de son rayon (carte retirée définitivement du paquet Machine ; Assaut permanent Sur place avec +1 puissance imprimée), puis remélange des cartes Machine actives avec toutes les cartes Sabotage (révélées/écartées ce tour + nouvellement acquises en 4.1).";
  }
}

spec.arbitrages_valides.A02 =
  "Rêves épurés & 1re pose 2.1 ouverte aux Rêves (v6.1) : un joueur peut poser son 1er Défenseur (2.1) comme son 2e Défenseur (2.2) sur un Rêve déjà présent sur la Réglette des Tactiques. En 3.2 dans le socle (CLEAR_RANK_ONLY), chaque Défenseur sur un Rêve visé annule 1 machine du rang (en priorisant la plus menaçante) et le Rêve ne bouge pas.";
spec.arbitrages_valides.A03 =
  "Furtivité « Chaud vs Calme » par piste de forêt (v6.1) : au pied de chaque rayon r (1..N), 2 rives de 2 emplacements (Rive Piège et Rive Sabotage) ouvertes à toute la table en 2.1 et 2.2 tant que le rayon r n'est pas intégralement rasé. En 4.1, seule une rive complète (2 Défenseurs) est évaluée selon m(r) = cartes Machine de r révélées en 3.2 + machines de r en Ratissage (indépendant de déviation Insecte ±1 et d'annulation Rêve ; Sabotage révélé = 0). Rive Piège gagnée si m(r) == 2 (le propriétaire du rayon r pose 1 Piège sur une parcelle non-Route non piégée de r) ; Rive Sabotage gagnée si m(r) == 0 (+1 carte Sabotage mise de côté pour 6.3 sans allumer 3. Sabotage).";
spec.arbitrages_valides.A06 =
  "Pièges autonomes SINGLE_STRIKE (v6.1 figé) : suppression de la condition d'Embuscade — dès qu'un jeton Piège est présent sur une parcelle attaquée en 5.1/5.2, il se déclenche de lui-même (même avec 0 Défenseur et 0 Insecte sur place), ne consomme ni Défenseur ni Insecte présent, pare exactement 1 frappe puis est défaussé aussitôt, en allumant uniquement 2. Piégeage.";
spec.arbitrages_valides.A10 =
  "Autonomie du Ratissage en Assaut permanent, départ décalé & Abatteuse coupe-tout (v6.1) : mise en place canonique décalée BULLDOZER_P1_ABATTEUSE_P2 (chassis_id = 24 : Bulldozer en parcelle 1, Abatteuse en parcelle 2). L'Abatteuse coupe TOUS les Arbres debout de la parcelle en Souches et ne touche jamais aux Souches (suppression définitive de la micro-règle souche). En 6.3 uniquement (test redondant en 1.1 supprimé), toute machine située sur la dernière parcelle non rasée de son rayon est retournée définitivement sur sa face Ratissage (carte retirée du paquet Machine ; Assaut permanent Sur place +1 puissance imprimée, 0 gain).";
spec.arbitrages_valides.A17 =
  "Migration des Insectes recentrée Forêt & Pistes centrales (v6.1) : 0 ou 1 cran facultatif le long du rayon (en sautant les Routes Forestières) ou aller simple définitif depuis la dernière parcelle non rasée vers une case 1..6 de la Réglette des Tactiques ou de la Piste des Gardiens (retrait de la Furtivité des destinations d'Insectes).";
spec.arbitrages_valides.A21 =
  "Déclencheur 5. Rêve actif uniquement & transfert de l'avancée au Mode 4 (v6.1) : REVE_TRIG=ACTIF figé — 5. Rêve s'allume uniquement lorsqu'un Rêve portant >= 1 Défenseur annule effectivement au moins 1 machine (non déviée) en 3.2. Un Rêve sans Défenseur est totalement inerte. Grâce à l'ouverture de 2.1 aux Rêves, une table à 5J–6J peut allumer 5. Rêve via 2.1 tout en engageant ses N Défenseurs de 2.2 sur les Gardiens pour l'Éveil.";
spec.arbitrages_valides.A22 =
  "Pari uniforme sur les Gardiens & Partition stricte des 6 déclencheurs (v6.1) : actif si >= 1 Animal Sauvage (M/R/O) est à la table. Pari uniforme UNIFORM_MAX_2 réservé à 2.2 (0, 1 ou 2 Défenseurs maximum par Gardien construit cases 1..6, glissés sous la tuile à chaque déclenchement). Partition stricte (« 1 événement = au plus 1 déclencheur ») : en 3.2 Sabotage > Insecte sur Tactiques > Rêve actif ; en 4.1 et 4.2 Nids aucun déclencheur ; en 5.1/5.2 Piégeage (Piège autonome SINGLE_STRIKE) > Insecte en Parade >= 1 Insecte > Parade par Défenseurs seuls ; 4. Gardien sur 1re ouverture du tour de chaque autre Gardien distinct.";
spec.arbitrages_valides.A23 =
  "Réglette des Tactiques réversible Face A/B, gain Charge FRAPPE_NON_PAREE & Déviation par Insectes (v6.1 gelé) : en mode CHARGE les jetons Puissance existants sont ignorés au seuil et au plus +1 jeton Puissance est gagné par activation dès qu'au moins 1 frappe sur parcelle réelle non-Route n'est ni parée ni piégée (FRAPPE_NON_PAREE figé, hors attaque Devant dans le vide depuis la dernière parcelle). En mode ASSAUT tous les jetons Puissance comptent au seuil et 0 jeton n'est gagné.";

writeUtf8Lf(DST_SPEC, JSON.stringify(spec, null, 2) + '\n');

// 3. Upgrade catalog_v6_0.json
const catOut = {
  schema_version: '6.1.0-alpha',
  total_emplacements: catalog.total_emplacements,
  total_profils: catalog.total_profils,
  topologies: catalog.topologies,
  formule_seuil_parade:
    "Seuil imprimé fixe + modificateur de Tactique (0 sur 1/2/4/5, -1 sur 3/6) + jetons Puissance actifs en ASSAUT/Ratissage (ignorés en mode CHARGE) - jetons Surchauffe bleus. Chaîne stricte : Bond du Jaguar -> Piquée de la Harpie -> Piège autonome SINGLE_STRIKE (défaussé aussitôt) -> Parade classique (Défenseurs + défausse immédiate des Insectes manquants).",
  verification_fin_de_partie:
    "Vérification unique à la fin des attaques (5.3, après résolution des paris Gardiens et Bouclier de lisière éventuel). Priorité absolue au Tour 8 (CAUSE_TOUR_8). Aux Tours 1..7 : Sommeil du Contremaître (tous les Rêves en jeu en bloc continu cases 1..k de la Réglette des Tactiques) ou Réveil de la Forêt 100 % Piste des Gardiens (actif si >= 1 Peuple Animal Sauvage M/R/O : les N Défenseurs de la table engagés en 2.2 sur la Piste des Gardiens et aucun pari perdu). Score final immédiat = Arbres debout (0 Repousse Finale automatique de base).",
  regle_piege:
    "Piège autonome SINGLE_STRIKE (suppression de l'Embuscade) : dès qu'un jeton Piège est présent sur une parcelle attaquée en 5.1/5.2, il se déclenche de lui-même dans la chaîne des parades (même avec 0 Défenseur et 0 Insecte sur la parcelle), ne consomme ni Défenseur ni Insecte présent, pare exactement 1 frappe puis est immédiatement défaussé, en allumant uniquement 2. Piégeage.",
  furtivite_4_1_autorise_ciblee_sans_machine: true,
  verrouillage_etape_5_parcelles_ciblees: ['INSECTE', 'PIEGE'],
  bonus_constructeur_n3: catalog.bonus_constructeur_n3,
  regle_furtivite:
    "Furtivité « Chaud vs Calme » par piste de forêt : au pied de chaque rayon r (1..N), 2 rives de 2 emplacements (Rive Piège et Rive Sabotage, max 2 Défenseurs par rive), accessibles à tout joueur en 2.1 ou 2.2 tant que le rayon r n'est pas intégralement transformé en Routes Forestières. En 4.1, seule une rive portant 2 Défenseurs est évaluée selon m(r) = cartes Machine du rayon r révélées en 3.2 + machines du rayon r en Ratissage permanent (indépendant de déviation Insecte ±1 et d'annulation Rêve). Rive Piège gagnée si m(r) == 2 (le propriétaire du rayon r pose 1 Piège sur une parcelle non-Route non piégée de r) ; Rive Sabotage gagnée si m(r) == 0 (+1 carte Sabotage pour 6.3).",
  gouvernance_autorite:
    "Autorité unitaire par Peuple d’origine (tuiles de Synergie et pistes de Migration) et par propriétaire de rayon (pose du Piège en 4.1). Zéro vote de groupe. Cartes Sabotage identiques agissant par dilution permanente du paquet Machine.",
  date_consolidation: '2026-11-22',
  spec_formelle: spec,
  spec_formelle_v6_0: spec,
};
writeUtf8Lf(DST_CAT, JSON.stringify(catOut, null, 2) + '\n');

// 4. Prepend v6.1 entry to VERSION_CHANGELOG
const catTiles = extracted.CATALOGUE_TUILES;
const changelog = extracted.VERSION_CHANGELOG;
for (const entry of changelog) {
  if (entry.version === 'v6.0') {
    entry.date = 'Incrément précédent exp/socle-v6 (2026-11-21)';
  }
}

const v61Entry = {
  version: 'v6.1',
  date: 'Branche expérimentale exp/socle-v6 (2026-11-22)',
  titre: 'Socle gelé v6.1 : départ décalé, Abatteuse coupe-tout, Pièges autonomes 1 frappe, Charge sur frappe non parée & Furtivité « Chaud vs Calme »',
  resume:
    "Incrément canonique gelé pro-simplicité (schema_version 6.1.0-alpha, P4_2233 + départ décalé Bulldozer p=1 / Abatteuse p=2, chassis_id = 24) : l'Abatteuse coupe tous les Arbres debout de la parcelle ciblée et ne touche jamais aux Souches ; Pièges autonomes sans Embuscade parant exactement 1 frappe puis défaussés aussitôt (SINGLE_STRIKE) ; gain Charge gelé sur FRAPPE_NON_PAREE (+1 jeton Puissance max/activation dès qu'au moins 1 frappe sur parcelle réelle non-Route n'est ni parée ni piégée, hors Devant dans le vide) ; Rêves ouverts en 2.1 et recentrés sur le blocage pur (CLEAR_RANK_ONLY, REVE_TRIG=ACTIF figé) ; Furtivité « Chaud vs Calme » par rayon (Rive Piège m(r)==2 gouvernée par le propriétaire du rayon, Rive Sabotage m(r)==0) ; élagage du test Ratissage en 1.1 et du passage d'Insectes en Furtivité.",
  deltas: [
    {
      domaine: 'Départ décalé canonique & Abatteuse coupe-tout (sans micro-règle souche)',
      avant:
        'v6.0 : Départ groupé en parcelle 1 ; Abatteuse coupait au maximum 2 Arbres debout avec option de souche en Ratissage.',
      apres:
        'v6.1 : Mise en place décalée canonique (Bulldozer en parcelle 1, Abatteuse en parcelle 2 sur chaque rayon, chassis_id = 24) ; l’Abatteuse coupe tous les Arbres debout de la parcelle ciblée en Souches et ne touche jamais aux Souches (suppression définitive de la micro-règle souche) ; maintien strict de T3/T6 mod_seuil = -1 et Bulldozer = 1 Arbre + toutes Souches.',
    },
    {
      domaine: 'Rêves épurés en socle, ouverture de 2.1 aux Rêves & déclencheur 5. Rêve actif',
      avant:
        'v6.0 : Seul le 2e Défenseur (2.2) pouvait cibler un Rêve ; choix exclusif Bloquer OU Avancer en 3.2 ; 5. Rêve allumé même sur un Rêve inerte sans Défenseur.',
      apres:
        'v6.1 : Le 1er Défenseur (2.1, simultané et fixe) peut désormais cibler tout Rêve déjà en piste (seule la Piste des Gardiens reste réservée à 2.2), débloquant l’Éveil à 5J–6J sur un Gardien case 5. Dans le socle, tout Rêve défendu applique uniquement le blocage (1 Défenseur annule 1 machine prioritaire, le Rêve ne bouge pas ; avancée transférée au Mode 4). REVE_TRIG=ACTIF figé : 5. Rêve s’allume uniquement si un Rêve défendu annule réellement >= 1 machine non déviée.',
    },
    {
      domaine: 'Furtivité « Chaud vs Calme » par piste de forêt (Rive Piège vs Rive Sabotage)',
      avant:
        'v6.0 : Furtivité sur lisières par parcelle en face (condition statique présence/activité de machine).',
      apres:
        'v6.1 : Au pied de chaque rayon r (1..N), 2 rives de 2 emplacements (Rive Piège et Rive Sabotage) ouvertes à toute la table en 2.1 et 2.2 (fermées dès que le rayon est 100 % en Routes). En 4.1, seule une rive à 2 Défenseurs est évaluée selon m(r) = cartes Machine de r révélées en 3.2 + Ratissages de r (indépendant de déviation Insecte ±1 et d’annulation Rêve). Rive Piège gagnée si m(r) == 2 (le propriétaire du rayon r pose 1 Piège sur une parcelle non-Route de r) ; Rive Sabotage gagnée si m(r) == 0 (+1 Sabotage pour 6.3).',
    },
    {
      domaine: 'Pièges autonomes 1 frappe (SINGLE_STRIKE) & Charge sur frappe non parée (FRAPPE_NON_PAREE)',
      avant:
        'v6.0 : Un Piège exigeait Défense totale >= 1 (Embuscade) sur la parcelle pour se déclencher ; gain en Charge uniquement sur dégât effectif.',
      apres:
        'v6.1 : Dès qu’un jeton Piège est présent sur une parcelle attaquée en 5.1/5.2, il se déclenche de lui-même (même avec 0 Défenseur et 0 Insecte), pare exactement 1 frappe puis est défaussé aussitôt sans consommer les Défenseurs ou Insectes présents, en allumant uniquement 2. Piégeage. Gain Charge gelé sur FRAPPE_NON_PAREE (+1 jeton Puissance max/activation dès qu’au moins 1 frappe sur parcelle réelle non-Route n’est ni parée ni piégée, hors Devant dans le vide).',
    },
  ],
};

const filteredChangelog = [v61Entry, ...changelog.filter((c) => c.version !== 'v6.1')];

// 5. Emit docs/data/amazonia_data_v6_0.js and validate with new vm.Script
const outJs = [
  '// =========================================================================',
  '// data/amazonia_data_v6_0.js — Données canoniques Amazonia v6.1-alpha (Expérimental · 6 profils · 192 châssis · 32 emplacements)',
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

console.log('Generated v6.1 Studio data layers successfully:');
console.log(' -', path.relative(ROOT, DST_SPEC));
console.log(' -', path.relative(ROOT, DST_CAT));
console.log(' -', path.relative(ROOT, DST_JS));
