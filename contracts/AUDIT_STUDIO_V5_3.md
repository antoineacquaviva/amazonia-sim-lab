# Audit du Contrat Studio `amazonia-doc-studio` (v5.3 consolidée)

**Sources inspectées (lecture seule, après commits `0716c70d` et `22de237d` du 2026-11-17)** :
- `C:\Dev\Jeu\amazonia-doc-studio\AMAZONIA_STUDIO_CONTEXT.md`
- `C:\Dev\Jeu\amazonia-doc-studio\data\catalog_v5_3.json` (synchronisé vers `data/catalog_v5_3.json`)
- `C:\Dev\Jeu\amazonia-doc-studio\data\spec_formelle_v5_3.json` (synchronisé vers `data/spec_formelle_v5_3.json`)
- `C:\Dev\Jeu\amazonia-doc-studio\data\amazonia_data_v5_3.js`
- `C:\Dev\Jeu\amazonia-doc-studio\data\livret_v5_3.js`

---

## 1. Décompte exact des emplacements et profils

- **Écart d'export JSON** : `data/catalog_v5_3.json` ne contient que les métadonnées globales (`schema_version: "5.3.1-audit"`, `total_emplacements: 32`, `total_profils: 100`, `topologies`, `spec_formelle_v5_3`). Le catalogue complet (`CATALOGUE_TUILES`), les 7 axes du châssis (`CHASSIS_AXES_SPEC`), `PEUPLES` et `MATRICE_PAIRES` résident dans `amazonia_data_v5_3.js`.
- **Décompte vérifié dans `CATALOGUE_TUILES`** : **32 emplacements / 100 profils** exactement :
  - `GARDIEN` (`G1..G15`) : 15 emplacements, **45** profils *(note : `AMAZONIA_STUDIO_CONTEXT.md` §4.1 indique par coquille « 43 profils » alors que le catalogue en contient bien 45)*
  - `REVE` (`R1..R10`) : 10 emplacements, **31** profils
  - `CROISSANCE` (`M1..M5`) : 5 emplacements, **19** profils
  - `MIGRATION` (`SLOT_BUG_CERVEAU`, `SLOT_COLONISATION_GARDIENS`) : 2 emplacements, **5** profils
- **Champs opérationnels** :
  - `temoin` : **100 / 100** profils renseignés.
  - `requires_options` : **100 / 100** profils présents avec liste/objet vide (les 7 axes du châssis sont orthogonaux aux tuiles).
  - `economie_bot` : **0 / 100** profils (à générer dans `spec_bundle_v5_3_1.json` au Palier 2).

---

## 2. Spécification complète : Sabotage, Paquet Machine, Dés & Tactiques `T1..T6`

### (a) Cartes Sabotage — **100 % spécifié (dilution permanente du paquet Machine)**
- **Modèle exact** : toutes les cartes Sabotage sont **identiques et sans effet propre** (réserve illimitée). Il n'existe ni pioche séparée, ni fenêtre d'activation en `3.2` ou `5`, ni gouvernance par les Humains.
- **Acquisition** (`4.1` *Saboter le chantier*, `4.2` Nids, ou pouvoirs `G9`/`G10`/`R4`/`M4`) : ajoute **définitivement** `+1` carte Sabotage de la réserve au paquet Machine (mise de côté pour le remélange de `6.3` ; allume le déclencheur `3. Sabotage`).
- **Résolution à l'Étape 1 & 3.2** : un joueur qui pioche une carte Sabotage en Étape 1 perd simplement cette activation du Contremaître (aucune machine activée, aucun lancer de dés). En `3.2`, la carte Sabotage révélée est mise de côté puis remélangée dans le paquet Machine en `6.3`.

### (b) Paquet de cartes Machine & Tirage / Dés (`N = 3..6`)
- **Composition initiale** : `2 * N` cartes Machine (**1 Abatteuse + 1 Bulldozer par rayon**, soit 6 à `N=3`, 8 à `N=4`, 10 à `N=5`, 12 à `N=6`), plus toutes les cartes Sabotage ajoutées définitivement au fil des tours.
- **Siège `T4` (`A10` corrigé)** : toute machine sur la dernière parcelle non rasée de son rayon est en **Siège `T4` irréversible** (carte posée face visible sur sa parcelle, hors paquet). Son attaque en fin d'Étape 5 est autonome même si `T4` a été éjectée par un Rêve ; en `6.1`, elle génère normalement de l'Apprentissage sur `T4` **si et seulement si `T4` figure encore sur la Piste des Tactiques**.
- **Pénurie de cartes** : s'il reste moins de cartes dans le paquet que de joueurs, distribution dans le sens horaire à partir du peuple ayant le plus d'Arbres debout.
- **Dés épurés (retrait complet du « double aux dés »)** : seul un joueur ayant tiré une **carte Machine** lance 2D6 sous paravent et retient `M = min(D1, D2)` (ou `max` sous Loi). Un joueur ayant tiré une carte Sabotage ou n'ayant reçu aucune carte ne lance pas de dés. Si le rang `M` porte un Rêve en `3.2`, la machine est annulée, le Rêve s'ouvre et avance d'1 cran à gauche (résolu de gauche à droite en `UNIQUE_PAR_TOUR`, ou cumulatif en `PAR_DE_M_DESIGNE`).

### (c) Les 6 tuiles Tactiques `T1` à `T6` (`livret_v5_3.js` §2 & §5)
- `T1. Sur place` : cible = parcelle actuelle ; avancée `0` ; gain Rouge `0` ; Mod. Seuil `0`.
- `T2. Devant` : cible = prochaine parcelle non rasée devant ; avancée `0` ; gain Rouge `0` ; Mod. Seuil `0`.
- `T3. En avançant` : cible = sur place + devant ; avancée `+1` parcelle non rasée vers le cœur ; gain Rouge `0` ; Mod. Seuil `-1 / parcelle`.
- `T4. Sur place +` : cible = parcelle actuelle ; avancée `0` ; gain Rouge `+1` ; Mod. Seuil `-1` *(profil identique au Siège)*.
- `T5. Devant +` : cible = devant ; avancée `0` ; gain Rouge `+1` ; Mod. Seuil `-1`.
- `T6. En avançant +` : cible = sur place + devant ; avancée `+1` parcelle non rasée ; gain Rouge `+1` ; Mod. Seuil `-2 / parcelle`.
- **Dégâts** : `Abatteuse` = jusqu'à 2 Arbres debout en Souches (+ 1 Souche arrachée en Siège si axe `ARRACHE_1_SOUCHE_SI_SANS_ARBRE`) ; `Bulldozer` = jusqu'à 1 Arbre debout en Souche puis toutes les Souches non protégées.

---

## 3. Impact sur le simulateur (`GameState`, Modes 1 & 2, Bots & Télémétrie)

- **`GameState` (`bytearray(256)`)** : **256 octets largement suffisants et simplifiés**. Plus besoin de stocker une main de cartes Sabotage typées ni de flags de fenêtre `3.2`/`5` : un simple compteur `uint8` `sabotage_deck_count` (+ `sabotage_pending_count` pour le tour en cours avant remélange `6.3`) suffit.
- **Modes 1 & 2** :
  - **Mode 1 (Cœur symétrique)** : 0 tuile `G/R/M`, 0 piste `Bug/Colonie`, **Sabotage par dilution permanente actif** (via l'action `4.1` *Saboter le chantier*), fin au Tour 8.
  - **Mode 2 (Asymétrie à vide)** : tuiles `G/R/M` présentes sans texte ni pouvoir propre, fonctions structurelles actives (Nids `+1/+2`, Rêves insérés/avancés/annulant une machine sur dé `M`, Gardiens marqués utilisés, fins anticipées `5.3` actives) et Migrations fixées à `A/A`.
- **Vocabulaire `economie_bot` & `telemetry.py`** : `RES_SABOTAGE` modélise désormais la dilution permanente du paquet Machine (`+1` carte neutre) et `TRIG_3` (`3. Sabotage`) est émis à l'acquisition (ou en `3.2` sous `G10 Face 2`). Les 4 capteurs de `telemetry.py` restent inchangés dans leurs formules.

---

## 4. Points de vigilance / Micro-coquille résiduelle dans le Studio

1. **Coquille résiduelle dans `spec_formelle_v5_3.json` (ligne 64)** : `etapes_tour[1].regles[1]` contient encore la phrase obsolète `"Double aux dés : peut ouvrir un Rêve en piste..."` alors que `A01`, `etapes_tour[0].regles[2]`, `livret_v5_3.js` et `AMAZONIA_STUDIO_CONTEXT.md` ont bien supprimé le double aux dés. Le simulateur implémentera la règle corrigée (aucun double aux dés).
2. **Table `T1..T6` & `2*N` cartes Machine absentes de `spec_formelle_v5_3.json`** : présentes en prose dans `livret_v5_3.js`, prêtes à être sérialisées directement dans `spec_bundle_v5_3_1.json`.
