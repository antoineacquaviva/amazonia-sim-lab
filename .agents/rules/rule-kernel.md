---
trigger: glob
description: Règles d'architecture et invariants v6.2 du noyau déterministe scellé
globs: "engine/state.py, engine/rng.py, engine/primitives.py, engine/core_engine.py"
---

# Règles du Noyau (`engine/`) — Cible SSOT `v6.2`

> **Statut transitoire (Chantiers 1 à 3)** : les 4 fichiers du noyau (`engine/rng.py`, `engine/state.py`, `engine/primitives.py`, `engine/core_engine.py`) restent **officiellement scellés** dans `contracts/kernel_locks.sha256` jusqu'au **Chantier 4**, où ils basculeront de manière atomique et approuvée sur `contracts/rules_canon_v6_2.json` et `contracts/physical_and_edge_invariants.json`. Interdiction absolue d'y toucher sans feu vert explicite de l'auteur.

## 1. Représentation de l'état (`engine/state.py`)
- `GameState` utilise `__slots__ = ("_buf", "_continuation", "cfg")` sur un `bytearray` compact alloué séquentiellement via `_Layout.alloc()` — **zéro magic number**, **100 % stdlib PyPy 3.11 / CPython 3.12**.
- `clone()` s'effectue par copie brute `bytearray(self._buf)` et copie légère de `_continuation`.
- Une plage dédiée d'octets transitoires de tour est remise à zéro systématiquement au ménage de fin de tour (`mem_debt == 0` : tout état persistant est porté par une pièce physique du plateau).
- **Isolation État Public / Privé** : `get_observation(seat_id)` masque strictement les jetons piochés, le Perchoir de l'Oiseau et les dés secrets tant que les paravents sont fermés.

## 2. Déterminisme & PRNG (`engine/rng.py`)
- PRNG déterministe adressable par compteur : `rand_event(exp_seed, rep_id, source_type, tour, entity_id, draw_idx)`.
- **Aucun `branch_id`** sur les événements comparables :
  - Jets de dés universels indexés par `(DICE, tour, peuple_id)` (tous les joueurs lancent leurs dés sous paravent fermé, y compris sur Sabotage ou Écaille dont le jet est ignoré).
  - Tirage au sac opaque (2N jetons Machine + Sabotages + jusqu'à 4 Écailles) à mélange stable indexé par `(MACHINE_DECK_SHUFFLE, tour)`.

## 3. Machine à états suspendable BGA-ready (`engine/core_engine.py`)
- Interface `step_until_decision() -> DecisionRequest | GameOver` et `apply_choice(choice)`.
- Le **Coordonnateur du tour** tourne en sens horaire : il sert de point de départ en cas de pénurie au sac (avec l'Oiseau toujours servi en dernier) et tranche les ordres globaux non attribués.
- Sur un même rayon au même rang (ou en Ratissage), **l'Abatteuse agit toujours avant le Bulldozer**.

## 4. Invariants métier cibles `v6.2` (`contracts/rules_canon_v6_2.json` & `INV-01..INV-22`)
- **Châssis canonique unique** : piste `P4_2233` (`[2, 2, 3, 3]`, dotation finie exacte de `10 × N` pions uniques recto-verso `Arbre debout` / `Souche`), départ décalé `Bulldozer p=1` / `Abatteuse p=2`.
- **Sac opaque & Dés universels** : `2N` jetons Machine épais + Sabotages + jusqu'à `4` Écailles ; non piochés cachés ; pénurie horaire depuis le Coordonnateur (Oiseau dernier) ; tous les joueurs lancent 2 dés (+ Dé d'Envol `1–6` chez `O`) sous paravent fermé.
- **2 Défenseurs recto-verso (`Réflexion` / `Définitif`)** : 1er pion posé face `Définitif` (jamais sur les Gardiens ; repli sur parcelle alliée si aucun emplacement légal), 2e pion posé face `Réflexion` puis validé face `Définitif` (figeant Duel/Plume ; clôture à `N−1` validés → au plus 1 ultime ajustement) ; chez `H`, 2 Chamanes uniques (`1 Tambour`, `1 Chant`).
- **Réglette fixe `1–6` + bandelette d'Acte réversible** : bandelette retournée seule au début du Tour 5 (Acte 1 `1–3 Charge / 4–6 Assaut`, Acte 2 inversé) sans déplacer ni Rêves ni Insectes.
- **Piste des Gardiens à 6 icônes (`[PARADE, PIEGEAGE, SABOTAGE, REVE, INSECTE, RESONANCE]`)** : Résonance en 6e position avec compteur individuel sans écrasement de bit et reprise gauche → droite ; 2 encoches visibles par Gardien (`≥ 1` pion dessus = pari perdu ; `0` dessus et `≥ 1` encoche = pari gagné → Face 2 ; `0` dessus et `0` encoche = aucune mise → reste en place sans évoluer).
- **Seuil de Parade unifié** : en Mode Charge, seuls les jetons rouges sont ignorés ; les **jetons bleus Surchauffe (`−1`) s'appliquent dans TOUS les modes** (Charge, Assaut, Ratissage), `−1` aux rangs `3` et `6`, `minimum 1`. Gain Charge = `+1` rouge max/activation (`FRAPPE_NON_PAREE`).
- **Ratissage physique** : au ménage, toute machine terminant sur la dernière parcelle glisse son jeton Machine sous elle (hors sac), conserve ses jetons Puissance et gagne `+1` jeton rouge physique (convertible en bleu ; zéro bonus imprimé). Immobile absolu, mais sa parcelle compte comme « parcelle ciblée » tant qu'elle n'a pas frappé.
- **Cibles figées & Repli de bordure** : parcelles ciblées figées au début de l'activation (toute cible devenue Route est annulée sans report). Une poussée de Route en bordure vers le cœur couvre et remplace l'avancée finale de `En avançant` (zéro double bond `+2`).
- **Ouverture & Rêves** : jetons Machine visibles jusqu'à Furtivité (inclinés 90° si annulés) ; ordre Sabotage/Écaille un par un (+ balayage) → déviation `±1` une par une (+ balayage) → Rêves défendus de gauche à droite (le propriétaire choisit les machines annulées y compris déviées, résout le pouvoir propre dès que défendu hors *« Quand ce Rêve annule… »*, puis allume `REVE` + balayage si `≥ 1` annulation ; Défenseurs solidaires des déplacements du Rêve).
- **Contacts & Routes** : zéro écrasement au contact hors Route (Nids, Insectes, Pièges, Duel intacts). Seule la création d'une Route Forestière vide la case (Nid en lisière reconstructible, Défenseurs en main, Piège/Croc/Insectes/Duel en réserve). Max 1 Piège ordinaire autonome (`SINGLE_STRIKE`) par parcelle ; le `Croc` Reptile cohabite et pare en premier.
- **Modules `3 + 3` & Enracinement** : Module Gardiens & Éveil (`M/R/O`), Module Rêves & Sommeil (`H/E`), Module Essaim clos sur `I` (incluant Déviation `±1` et Bouclier de lisière facultatif gouverné par `I`, descente sur place de l'Insecte passager au ménage) ; accessoires `3 + 3` (`H/M/O` Tour 1 ; `E` Altération, `R` Écailles/Croc/Cale, `I` Essaim) ; Enracinement volontaire au ménage (`1` Souche F1/unique, `2` F2 au décompte final ; Rêve enraciné interdit le Sommeil).
