#!/usr/bin/env node
/**
 * scripts/patch_tuiles_passe4.js
 * Passe 4 : Consolidation chirurgicale des 32 emplacements (100 profils)
 * Synchronise data/amazonia_data_v5_3.js et data/catalog_v5_3.json sans regex fragile.
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const JS_PATH = path.join(ROOT, 'data', 'amazonia_data_v5_3.js');
const LIVRET_PATH = path.join(ROOT, 'data', 'livret_v5_3.js');
const JSON_PATH = path.join(ROOT, 'data', 'catalog_v5_3.json');

// Dictionnaire exact des profils corrigés (G1..G15, R1..R10, M1..M5 + Slots Migration)
const PATCHES = {
  G1: {
    B: {
      fenetre: "OUVERTURE / LOI 5",
      texte: "<strong>Face 1 :</strong> Réduisez de -2 le Seuil de Parade d’une machine portant au moins 1 jeton Puissance (rouge ou bleu) pour le reste du tour.<br><strong>Face 2 (Loi 5) :</strong> Dès qu’une machine porte ≥ 2 jetons bleus (<em>Surchauffe</em>) au moment de frapper, défaussez 2 bleus pour <strong>parer automatiquement toutes ses frappes encore à résoudre</strong> et la faire reculer immédiatement d’1 parcelle non rasée vers la bordure au lieu de son avancée (si elle n’est pas en Siège).",
      temoin: "1er maillon de la chaîne des parades (avant Harpie et Piège) : consomme automatiquement 2 bleus, allume 1. Parade et laisse un éventuel Piège intact (non déclenché)."
    }
  },
  G2: {
    A: {
      temoin: "Saute les Routes Forestières (et détruit par contact un éventuel Nid non protégé à l’arrivée). Les cibles de la machine se liront depuis sa nouvelle position réelle à l’instant où elle attaque."
    },
    B: {
      fenetre: "LOI 5",
      texte: "<strong>Face 1 (Loi 5) :</strong> Une machine dont toutes les frappes sont parées <strong>n’avance pas</strong> sur T3/T6.<br><strong>Face 2 (Loi 5) :</strong> Une machine dont toutes les frappes sont parées <strong>n’avance pas ET ne gagne pas de jeton Puissance rouge</strong> sur T3 à T6 (y compris en Siège).",
      temoin: "Une frappe annulée sur une parcelle déjà rasée en Route Forestière ne compte pas comme parée pour cette loi."
    },
    C: {
      temoin: "3 Insectes en p=1, Route en p=2, Nid en p=3 : les 3 arrivent ensemble en p=3 sans allumer la case 6 (tous les Insectes présents sur la roue sont libres)."
    }
  },
  G3: {
    A: {
      texte: "Déplacez 1 Défenseur (y compris un constructeur resté en bordure de lisière en 3.1) vers une parcelle Forêt non rasée adjacente."
    },
    B: {
      texte: "<strong>Loi 4.1 :</strong> Une fois par tour, après l’action d’un binôme sur l’une des lisières de M ou O, 1 de ses Défenseurs glisse gratuitement sur une parcelle Forêt non rasée adjacente en face pour l’Étape 5."
    }
  },
  G4: {
    A: {
      texte: "<strong>Face 1 (Ouverture) :</strong> Réduisez de -1 le Seuil de Parade sur une parcelle des rayons O ou M pour le reste du tour.<br><strong>Sacrifice (en 3.2 après révélation) :</strong> Déplacez jusqu’à 2 Défenseurs vers des parcelles ciblées (renvoyez G4 sur sa Face 1 en lisière ; il libère sa case et perd son marqueur « utilisé »).",
      temoin: "Le sacrifice libère la case Gardien pour une future construction ; le seuil fixe de Réveil calculé à la mise en place ne change pas."
    },
    B: {
      texte: "<strong>Face 1 (Loi 2.1) :</strong> Le peuple d’origine (O) et son voisin (M) posent leur 1er Défenseur à portée globale.<br><strong>Sacrifice (Début Étape 2) :</strong> Ouvrez tous les mini-paravents <strong>avant</strong> de placer les Défenseurs ce tour-ci (renvoyez G4 en lisière ; il perd son marqueur « utilisé »).",
      temoin: "Offre une visibilité publique complète des cartes et dés, mais la pose reste individuelle et sans concertation orale."
    }
  },
  G5: {
    A: {
      texte: "<strong>Face 1 :</strong> Désignez 1 parcelle non rasée : pour ce tour, réduisez de <strong>−1</strong> son Seuil de Parade à chaque frappe trouvant au moins 1 Souche sur place à cet instant.<br><strong>Face 2 :</strong> Désignez jusqu’à 2 parcelles non rasées : pour ce tour, réduisez de <strong>−1</strong> leur Seuil de Parade à chaque frappe trouvant au moins 1 Souche sur place à cet instant.",
      temoin: "Vérification dynamique à chaque frappe : si une Abatteuse crée une Souche sur la parcelle désignée, le Bulldozer suivant subit immédiatement le −1 au Seuil."
    },
    B: {
      temoin: "Vérifié dynamiquement à chaque frappe sur le Seuil Imprimé : dès qu’au moins 1 Souche est présente sur la parcelle à cet instant, le Seuil diminue de −1."
    }
  },
  G6: {
    C: {
      texte: "Vous pouvez échanger simultanément 1 Défenseur d’une parcelle des Oiseaux ou des Reptiles avec 1 Insecte de la case Furtivité qui lui fait face sur leur lisière commune (posez ce Défenseur sur un emplacement valide de la case en tirant l’éventuel autre Défenseur sur son jumeau).",
      temoin: "Avant 4.1, permet de former et d’orienter un binôme de 2 Défenseurs en Furtivité tout en envoyant l’Insecte défendre la forêt."
    }
  },
  G8: {
    A: {
      texte: "En 3.2 (ou à l’ouverture avant l’attaque de la machine), décalez d’1 parcelle non rasée dans le même sens le long de son rayon l’ensemble des frappes d’une machine non en Siège pour ce tour, sans déplacer la machine.",
      temoin: "Saute les Routes Forestières ; le décalage s’applique aux cibles lues depuis la position réelle de la machine à l’instant où elle attaque."
    },
    B: {
      texte: "<strong>Loi 5 :</strong> Sur 1 rayon au choix par tour, si l’Abatteuse et le Bulldozer sont tous deux actifs, vous pouvez résoudre le <strong>Bulldozer avant l’Abatteuse</strong> (quel que soit leur rang ou en Siège).",
      temoin: "Sur 3 Arbres sans Souche : le Bulldozer coupe 1 Arbre (0 Souche à terrasser), puis l’Abatteuse coupe les 2 Arbres restants en 2 Souches (évite la Route Forestière !)."
    }
  },
  G9: {
    A: {
      texte: "<strong>Face 1 :</strong> Piochez 1 carte Sabotage face visible en réserve (allume la case 3 si une carte est piochée).<br><strong>Face 2 :</strong> Piochez jusqu’à 2 cartes Sabotage face visible en réserve (allume la case 3).",
      temoin: "Si la pioche et la défausse Sabotage sont vides (toutes les cartes déjà en réserve), aucune carte n’est piochée et la case 3 ne s’allume pas."
    },
    B: {
      fenetre: "LOI 4.1 / LOI 5",
      texte: "<strong>Face 1 (Loi 4.1) :</strong> Un binôme en Furtivité peut saboter sa parcelle cible même si une machine y est active ce tour-ci ou en <strong>Siège</strong>.<br><strong>Face 2 (Loi 4.1 & 5) :</strong> Un binôme en Furtivité peut saboter sa parcelle cible même si une machine y est active ce tour-ci ou en <strong>Siège</strong> ; de plus, les cartes Sabotage en réserve peuvent être jouées librement <strong>à tout moment pendant l’Étape 5</strong>.",
      temoin: "En Face 2, lève à la fois l’interdiction de saboter une machine active en 4.1 et la fermeture de la fenêtre Sabotage pendant les attaques."
    }
  },
  G10: {
    A: {
      temoin: "Mémorisé jusqu’en 6.1 et appliqué avant les Insectes Bug (permettant d’épargner un Bug si la Tactique tombe à 0 jeton)."
    },
    B: {
      texte: "<strong>Loi 5.3 :</strong> À la fin des attaques, chaque Piège déclenché ce tour-ci retire 1 jeton Puissance rouge (ou retourne 1 rouge en bleu) sur chaque machine dont il a paré au moins une frappe.",
      temoin: "S’applique en 5.3 avant le retrait des Pièges déclenchés, une fois par couple Piège–machine parée."
    },
    C: {
      texte: "<em>(Câblage obligatoire sur 6. Insecte)</em> À l’ouverture, vous pouvez défausser 1 Insecte d’une parcelle Forêt pour piocher 1 carte Sabotage face visible en réserve (allume la case 3 si une carte est piochée).",
      temoin: "En 4.2, l’Insecte produit par un Nid peut payer ce coût ; si ouverte pendant l’Étape 5, la carte Sabotage piochée peut être jouée immédiatement !"
    }
  },
  G11: {
    A: {
      temoin: "2e maillon de la chaîne des parades (après Jaguar, avant Piège) : pare la frappe sans déclencher un éventuel Piège présent."
    },
    B: {
      texte: "<strong>Face 1 (Loi 5) :</strong> Tout Défenseur isolé sur une case Furtivité ajoute +1 en Défense aux deux parcelles Forêt non rasées en face (même profondeur p).<br><strong>Face 2 (Loi 5) :</strong> Tout Défenseur isolé sur une case Furtivité ajoute +1 en Défense aux deux parcelles Forêt non rasées en face (même profondeur p), et chaque Défenseur constructeur resté en bordure de lisière ajoute +1 en Défense aux parcelles p=1 non rasées adjacentes."
    },
    C: {
      temoin: "Offre un point d’ancrage global dès 2.1 (le Défenseur se pose sur l’un des 4 emplacements valides de la case)."
    }
  },
  G12: {
    A: {
      temoin: "Si le Rêve atteint ainsi le Rang 1, le Sommeil du Contremaître sera validé lors de la vérification de fin d’attaques en 5.3."
    },
    C: {
      texte: "<em>(Câblage obligatoire sur 2. Piégeage)</em> À l’ouverture, vous pouvez retirer de la forêt 1 Piège non déclenché ce tour-ci pour faire avancer d’1 rang vers la gauche le Rêve le plus à gauche.",
      temoin: "Peut consommer le Piège tout juste posé en 4.1 pour amener un Rêve au Rang 1 (victoire vérifiée en fin de 5.3). Un Piège ayant déjà paré ce tour ne peut pas payer ce coût."
    }
  },
  G13: {
    A: {
      texte: "Posez 1 jeton Insecte sur une parcelle non rasée ou une case Furtivité contenant au moins 1 Défenseur (allume la case 6)."
    }
  },
  G14: {
    A: {
      texte: "Défaussez 1 Insecte d’une parcelle Forêt pour poser 1 Piège sur cette parcelle ou une parcelle non rasée adjacente du même rayon sans Piège (allume la case 2).",
      temoin: "Attention : ne défaussez pas le dernier pion qui devait fournir le point de Défense armant ce Piège !"
    },
    B: {
      temoin: "Protège les Nids et leurs Insectes contre tout mouvement de machine (avancée, recul, repli), mais pas contre la transformation de la parcelle en Route Forestière."
    },
    C: {
      texte: "<strong>Face 1 (À jeun) :</strong> Défaussez 1 Insecte d’une parcelle du rayon des Reptiles pour retourner ce Gardien sur <em>Rassasié</em>.<br><strong>Face 2 (Rassasié) :</strong> Posez 1 Piège sur une parcelle non rasée des Reptiles sans machine ni Piège, puis retournez ce Gardien sur <em>À jeun</em> (allume la case 2)."
    },
    D: {
      texte: "Vous pouvez déplacer 1 Insecte d’une parcelle des Reptiles ou des Insectes vers une autre parcelle piégée du <strong>même rayon</strong>, à toute distance."
    }
  },
  G15: {
    A: {
      texte: "Faites migrer immédiatement 1 Insecte depuis n’importe quelle parcelle ou case Furtivité de la roue vers une case 1..6 d’une piste globale (<code>Bug</code> ou <code>Colonie</code>, aller simple définitif).",
      temoin: "Permet de coloniser le Cerveau ou les Gardiens sans attendre d’atteindre la dernière parcelle non rasée."
    },
    B: {
      texte: "<strong>Loi 4.3 :</strong> En 4.3, chaque Insecte sur la roue peut se déplacer de <strong>0, 1 ou 2 crans</strong> (au lieu de 0 ou 1)."
    }
  },

  R1: {
    B: {
      texte: "<strong>Loi 3.2 :</strong> Lorsqu’il s’ouvre en 3.2, ce Rêve avance de <strong>jusqu’à 2 rangs</strong> vers la gauche (plafonné au Rang 1) au lieu d’1.",
      temoin: "Accélère l’arrivée au Rang 1 pour déclencher le Sommeil du Contremaître en fin de 5.3."
    },
    C: {
      texte: "À chaque ouverture en 3.2, vous pouvez renvoyer 1 Gardien de la piste vers sa lisière (sur sa Face 1, en retirant son marqueur « utilisé ») pour faire avancer ce Rêve de <strong>jusqu’à 2 rangs</strong> au lieu d’1.",
      temoin: "Coût volontaire : ne déclenche pas un pouvoir de sacrifice et ne modifie pas le seuil fixe de Réveil."
    }
  },
  R2: {
    A: {
      temoin: "Appliqué en 6.1 avant les Insectes Bug : permet de provoquer une égalité en tête ou d’épargner un Bug sur une case ramenée à 0."
    },
    B: {
      temoin: "Une frappe annulée sur une parcelle déjà rasée en Route Forestière ne compte pas comme parée."
    }
  },
  R3: {
    A: {
      texte: "À l’ouverture en 3.2, déplacez jusqu’à 2 Défenseurs (y compris des constructeurs restés en lisière en 3.1) vers des parcelles Forêt non rasées."
    },
    B: {
      texte: "<strong>Loi 3.1 :</strong> Lors d’une construction (G ou R), le Peuple d’origine de la tuile construite libère <strong>1 des 2 Défenseurs bâtisseurs</strong> vers la 1re parcelle adjacente non rasée de son choix (ou <strong>tous les Défenseurs bâtisseurs à N=3 joueurs</strong>, chacun choisissant sa rive).",
      temoin: "Prend effet dès la construction de R3 B pour ses propres bâtisseurs (dans la limite des Défenseurs réellement présents)."
    }
  },
  R4: {
    B: {
      fenetre: "LOI SABOTAGE",
      texte: "<strong>Loi Sabotage :</strong> Une fois par tour, lorsqu’une carte Sabotage est jouée alors qu’au moins 1 Défenseur occupe une case Furtivité, conservez cette carte visible en réserve pour un tour ultérieur au lieu de la défausser (une même carte ne peut être jouée qu’une fois par tour).",
      temoin: "Recycle gratuitement une carte Sabotage par tour tant qu’une présence furtive est maintenue."
    }
  },
  R5: {
    C: {
      temoin: "Pose un Piège d’urgence sur cible vide : il suffira d’y amener 1 point de Défense (local ou soutenu à distance) avant la frappe pour déclencher l’Embuscade."
    }
  },
  R6: {
    A: {
      texte: "Posez 1 Insecte de la réserve sur une parcelle non rasée d’un rayon de cette paire (H ou I, allume la case 6)."
    },
    B: {
      texte: "Déclenchez immédiatement la création de jetons Insecte d’1 Nid en jeu (+1 ou +2 selon les Insectes présents sur sa parcelle à cet instant, même sans Défenseur dessus ; allume la case 6 sans déclencher le pouvoir propre du Nid).",
      temoin: "Production hors phase restreinte aux seuls jetons Insecte ; l’activation complète du Nid en 4.2 reste disponible."
    },
    C: {
      texte: "<strong>Loi de Repousse finale :</strong> À la fin de la partie, sur chaque parcelle non rasée des Humains ou des Insectes ayant conservé au moins 1 Souche, retournez jusqu’à <strong>2 Souches</strong> en Arbres debout (dans la limite de la dotation initiale de la parcelle)."
    }
  },
  R7: {
    A: {
      texte: "Faites reculer d’1 parcelle non rasée vers la bordure une machine non en Siège située sur les rayons E ou M.",
      temoin: "Retarde l’entrée en Siège et modifie dynamiquement les cibles que cette machine lira à l’Étape 5."
    },
    B: {
      fenetre: "LOI 5",
      texte: "<strong>Loi 5 (Endiguement du Siège) :</strong> Les machines en <strong>Siège</strong> sur les rayons E et M et leurs rayons voisins immédiats ne gagnent plus de jeton Puissance rouge après leur attaque et subissent -1 à leur Seuil de Parade.",
      temoin: "Neutralise l’escalade de Puissance des machines en Siège sans annuler leur statut."
    }
  },
  R8: {
    A: {
      texte: "Posez 1 Piège sur une parcelle non rasée sans Piège des rayons E ou R, même occupée par une machine ou ciblée (allume la case 2)."
    },
    B: {
      temoin: "Tant qu’au moins 1 Défenseur ou 1 Insecte tient la parcelle lors de la frappe, un Bulldozer non paré ne peut pas créer de Route Forestière sur E et R."
    }
  },
  R9: {
    B: {
      texte: "<strong>Loi 6.2 :</strong> En cas d’égalité en tête de l’Apprentissage à l’Étape 6.2 (y compris égalité générale à 0), c’est ce Rêve qui avance d’1 rang vers la gauche (r → r−1). S’il atteint ainsi le Rang 1, la fin de partie se déclenche immédiatement à la fin de ce tour (Repousse Finale).",
      temoin: "Exception unique au test de 5.3 : atteindre le Rang 1 en 6.2 déclenche aussitôt la Repousse Finale. Un blocage par la Cigale (Bug C) d’un vainqueur unique n’est pas une égalité."
    }
  },
  R10: {
    B: {
      texte: "<strong>Conversion 3.2 :</strong> À l’ouverture de ce Rêve, vous pouvez défausser 1 Insecte présent sur la roue pour le faire avancer d’1 rang supplémentaire vers la gauche (plafonné au Rang 1).",
      temoin: "Convertit un Insecte de la roue en avancée accélérée vers le Rang 1 (les Insectes déjà migrés sur Bug ou Colonie ne peuvent pas payer ce coût)."
    },
    D: {
      texte: "Vous pouvez poser 1 Piège sur une parcelle sans Piège des Entités ou des Insectes contenant au moins 1 Défenseur et 1 Insecte, puis déplacer 1 Insecte de cette parcelle vers une autre parcelle non rasée du même rayon, à toute distance (groupe atomique, allume la case 2)."
    }
  },

  M1: {
    A: {
      texte: "Après production en 4.2, déplacez 1 Défenseur présent sur ce Nid vers n’importe quelle autre parcelle Forêt non rasée du plateau.",
      temoin: "Résolu au sein du bloc indivisible du Nid avant le balayage de la case 6 ; le Défenseur rejoint n’importe quel front pour l’Étape 5."
    },
    B: {
      fenetre: "LOI 5",
      texte: "<strong>Loi 5 (Carapaces) :</strong> Une fois par tour, lors d’une Parade classique sur la parcelle de ce Nid à laquelle contribue au moins 1 Défenseur, épargnez 1 des Insectes qui devaient être défaussés immédiatement.",
      temoin: "Économise immédiatement 1 Insecte au moment de la frappe parée et maintient la masse critique sur le Nid."
    },
    C: {
      temoin: "Un Insecte envoyé sur la dernière parcelle non rasée en 4.2 peut ensuite migrer vers une piste globale dès 4.3 du même tour !"
    }
  },
  M2: {
    B: {
      temoin: "L’action du binôme s’oriente sur la rive occupée par le Défenseur, et l’Insecte reste disponible sur la case Furtivité."
    },
    C: {
      temoin: "Une Abatteuse T3 qui crée 2 Souches devant elle permet au Nid de survivre lors de son avancée immédiate après ses frappes."
    },
    D: {
      temoin: "Comme un Piège déclenché reste en place jusqu’en 5.3, il protège encore le Nid lors de l’avancée immédiate d’une machine T3/T6 parée ! En revanche, si plus aucun Défenseur ni Insecte n’est présent à l’entrée de la machine, le Nid retourne en lisière."
    }
  },
  M3: {
    C: {
      texte: "<strong>Loi 5 :</strong> Sur la parcelle de ce Nid, chaque Insecte physiquement présent apporte <strong>2 points de Défense</strong> (lors d’une Parade classique, défaussez immédiatement le nombre d’Insectes arrondi au supérieur du manque).",
      temoin: "1 Défenseur + 2 Insectes (5 en Défense) parent un Seuil de 5 en ne défaussant immédiatement que 2 Insectes au lieu de 4."
    }
  },
  M4: {
    A: {
      texte: "Après production en 4.2, vous pouvez défausser 1 Insecte de ce Nid pour piocher 1 carte Sabotage face visible en réserve (allume la case 3 si une carte est piochée).",
      temoin: "Résolu dans le bloc indivisible du Nid : au balayage suivant, les cases 3 et 6 seront examinées dans l’ordre 1 → 6."
    },
    B: {
      texte: "<strong>Loi 5.3 :</strong> À la fin des attaques, sur ce rayon, chaque Piège ayant paré au moins une frappe ce tour-ci glisse sur la prochaine parcelle non rasée vers le cœur (si elle est sans Piège, sans allumer la case 2) au lieu d’être retiré."
    },
    D: {
      texte: "<strong>Loi 5.3 :</strong> À la fin des attaques, une fois par tour, vous pouvez faire glisser ensemble 1 Piège déclenché ce tour-ci de ce rayon ET 1 Insecte présent sur sa parcelle vers la prochaine parcelle non rasée côté cœur, si elle est sans Piège."
    }
  },
  M5: {
    B: {
      temoin: "Permet un aller simple définitif vers une case 1..6 de Bug ou Colonie dès p=1, sans traverser tout le rayon."
    },
    C: {
      temoin: "Même non paré, un Bulldozer ne peut jamais raser cette parcelle en Route Forestière tant que le Nid est en place et qu’il reste au moins 1 Arbre ou 1 Souche."
    },
    D: {
      temoin: "Allume la case 6 en 5.3 juste avant la vérification de fin de partie (pouvant ainsi ouvrir un dernier Gardien pour atteindre le seuil de Réveil !)."
    }
  },

  SLOT_BUG_CERVEAU: {
    A: {
      temoin: "Appliqué en 6.1 après les retraits volontaires de tuiles : si la case est déjà à 0 jeton, l’Insecte Bug n’est pas défaussé et reste sur son numéro d’emplacement."
    },
    C: {
      temoin: "Même lorsque la Cigale bloque l’avancée du vainqueur en 6.2, 100 % des jetons d’Apprentissage de toutes les tuiles sont remis à zéro."
    }
  }
};

function findBalancedObjectSpan(src, varName) {
  const re = new RegExp(`\\b(?:const|let|var)\\s+${varName}\\s*=\\s*\\{`);
  const m = re.exec(src);
  if (!m) throw new Error(`Variable ${varName} introuvable dans ${JS_PATH}`);
  const openIdx = m.index + m[0].length - 1;
  let depth = 0;
  let inQuote = null;
  for (let i = openIdx; i < src.length; i++) {
    const ch = src[i];
    if (inQuote) {
      if (ch === '\\') { i++; continue; }
      if (ch === inQuote) inQuote = null;
      continue;
    }
    if (ch === '/' && src[i + 1] === '/') {
      const nl = src.indexOf('\n', i + 2);
      if (nl === -1) break;
      i = nl;
      continue;
    }
    if (ch === '/' && src[i + 1] === '*') {
      const endC = src.indexOf('*/', i + 2);
      if (endC === -1) break;
      i = endC + 1;
      continue;
    }
    if (ch === "'" || ch === '"' || ch === '`') {
      inQuote = ch;
    } else if (ch === '{') {
      depth++;
    } else if (ch === '}') {
      depth--;
      if (depth === 0) return [openIdx, i + 1];
    }
  }
  throw new Error(`Accolade fermante introuvable pour ${varName}`);
}

function syncJsonTree(node, cat) {
  if (Array.isArray(node)) {
    node.forEach(item => syncJsonTree(item, cat));
    return;
  }
  if (node && typeof node === 'object') {
    for (const [k, v] of Object.entries(node)) {
      if (cat[k] && v && typeof v === 'object' && v.profils) {
        v.origine = cat[k].origine;
        v.peuple_origine = cat[k].peuple_origine;
        for (const [pLet, pObj] of Object.entries(cat[k].profils)) {
          if (v.profils[pLet]) Object.assign(v.profils[pLet], pObj);
        }
      }
    }
    if (typeof node.id === 'string' && cat[node.id] && node.profils) {
      node.origine = cat[node.id].origine;
      node.peuple_origine = cat[node.id].peuple_origine;
      for (const [pLet, pObj] of Object.entries(cat[node.id].profils)) {
        if (node.profils[pLet]) Object.assign(node.profils[pLet], pObj);
      }
    }
    for (const v of Object.values(node)) {
      if (v && typeof v === 'object') syncJsonTree(v, cat);
    }
  }
}

function main() {
  const jsSrc = fs.readFileSync(JS_PATH, 'utf8');
  const ctx = vm.createContext({ window: {} });
  vm.runInContext(jsSrc + '\n;globalThis.__CAT = CATALOGUE_TUILES;', ctx);
  const cat = ctx.__CAT;

  let patchedProfiles = 0;
  let clearedRequires = 0;

  // 1. Nettoyage transversal sur les 32 emplacements
  for (const [tileId, tileObj] of Object.entries(cat)) {
    if (!tileObj.origine && tileId.startsWith('SLOT_')) tileObj.origine = 'I';
    tileObj.peuple_origine = tileObj.origine;

    for (const [letter, prof] of Object.entries(tileObj.profils)) {
      if (prof.requires_options && 'Regle_Resolution_Piege' in prof.requires_options) {
        delete prof.requires_options.Regle_Resolution_Piege;
        clearedRequires++;
      }
      if (PATCHES[tileId] && PATCHES[tileId][letter]) {
        Object.assign(prof, PATCHES[tileId][letter]);
        patchedProfiles++;
      }
    }
  }

  // 2. Réinjection propre dans data/amazonia_data_v5_3.js
  const [startIdx, endIdx] = findBalancedObjectSpan(jsSrc, 'CATALOGUE_TUILES');
  const newJsSrc = jsSrc.slice(0, startIdx) + JSON.stringify(cat, null, 2) + jsSrc.slice(endIdx);
  new vm.Script(newJsSrc, { filename: 'amazonia_data_v5_3.js' });
  if (fs.existsSync(LIVRET_PATH)) {
    new vm.Script(fs.readFileSync(LIVRET_PATH, 'utf8'), { filename: 'livret_v5_3.js' });
  }
  fs.writeFileSync(JS_PATH, newJsSrc.replace(/\r\n/g, '\n'), 'utf8');

  // 3. Synchronisation de data/catalog_v5_3.json
  if (fs.existsSync(JSON_PATH)) {
    const jsonObj = JSON.parse(fs.readFileSync(JSON_PATH, 'utf8'));
    syncJsonTree(jsonObj, cat);
    fs.writeFileSync(JSON_PATH, JSON.stringify(jsonObj, null, 2) + '\n', 'utf8');
  }

  // 4. Audit final des 100 profils (zéro résidu banni, zéro témoin manquant)
  const banned = [
    [/amortiss/i, 'Mention Amortisseur'],
    [/engag[ée]/i, 'Mention engagé'],
    [/verrouill/i, 'Mention verrouillage'],
    [/valent\s+(?:aussi\s+)?0/i, 'Ancien poids des Souches = 0'],
    [/poids\s+dans\s+le\s+calcul\s+du\s+seuil/i, 'Ancien calcul du Seuil']
  ];
  const warnings = [];
  let totalProfiles = 0;

  for (const [tileId, tileObj] of Object.entries(cat)) {
    for (const [letter, prof] of Object.entries(tileObj.profils)) {
      totalProfiles++;
      if (!prof.temoin || !prof.temoin.trim()) {
        warnings.push(`${tileId}_${letter} : champ 'temoin' vide ou manquant !`);
      }
      const combined = `${prof.texte} || ${prof.temoin}`;
      for (const [rx, label] of banned) {
        const m = rx.exec(combined);
        if (m) warnings.push(`${tileId}_${letter} (${label}) : "${m[0]}"`);
      }
    }
  }

  console.log(`=== Passe 4 terminée avec succès ===`);
  console.log(`• Emplacements vérifiés         : ${Object.keys(cat).length} (${totalProfiles} profils)`);
  console.log(`• Profils réécrits / précisés   : ${patchedProfiles}`);
  console.log(`• requires_options nettoyés (D) : ${clearedRequires}`);

  if (warnings.length > 0) {
    console.warn(`\n[!] ${warnings.length} alerte(s) détectée(s) :`);
    warnings.forEach(w => console.warn(`  - ${w}`));
    process.exit(1);
  } else {
    console.log(`[SUCCÈS] 0 résidu banni, 100 % des témoins présents, syntaxe JS et JSON validée.`);
  }
}

main();