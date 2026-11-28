# Contrat API Publique du Noyau Scellé (`core_state_api.md`)

Ce document est généré automatiquement par `scripts_cloud/export_api_doc.py` via inspection AST.
Les modules d'effets stateless dans `engine/effects/*.py` doivent utiliser **exclusivement**
les constantes, structures, accesseurs et primitives listés ci-dessous (zéro accès à `_buf`,
zéro `import random`, zéro état global mutable).

---

## État de jeu (`engine.state`)

*Source : `engine/state.py`*

> État de jeu déterministe scellé sur bytearray(384) et vue isolée PlayerObservation (v6.4).

### Constantes publiques

- `STATE_BUF_SIZE: int = 384`
- `BUF_CAPACITY: int = STATE_BUF_SIZE`
- `MIN_FREE_RESERVE_BYTES: int = 32`
- `MAX_N: int = 6`
- `MAX_P: int = 5`
- `NUM_PARCELS: int = MAX_N * MAX_P`
- `NUM_SYNERGY_SLOTS: int = 2 * MAX_N`
- `NUM_MACHINES: int = 2 * MAX_N`
- `NUM_NIDS: int = 5`
- `TRACK_LEN: int = 6`
- `DECK_SLOTS_CAPACITY: int = 64`
- `CANONICAL_PROFIL_PISTE: str = 'P4_2233'`
- `CANONICAL_P_MAX: int = 4`
- `CANONICAL_DOTATION: tuple[int, ...] = (2, 2, 3, 3)`
- `CANONICAL_ARBRES_PAR_RAYON: int = 10`
- `BULLDOZER_INIT_PARCEL: int = 1`
- `ABATTEUSE_INIT_PARCEL: int = 2`
- `GARDIEN_BET_CAP: int = 2`
- `TRIG_PARADE: int = 1`
- `TRIG_PIEGEAGE: int = 2`
- `TRIG_SABOTAGE: int = 3`
- `TRIG_REVE: int = 4`
- `TRIG_INSECTE: int = 5`
- `TRIG_RESONANCE: int = 6`
- `GUARDIAN_ICONS_ORDER: tuple[str, ...] = ('PARADE', 'PIEGEAGE', 'SABOTAGE', 'REVE', 'INSECTE', 'RESONANCE')`
- `PFLAG_SANCTUAIRE_SOUCHE: int = 1 << 0`
- `PFLAG_MATAMATA_MARK: int = 1 << 1`
- `PFLAG_AUTO_PARADE_ONCE: int = 1 << 2`
- `MACHINE_ABATTEUSE: int = 0`
- `MACHINE_BULLDOZER: int = 1`
- `MACHINE_STATUS_NORMAL: int = 0`
- `MACHINE_STATUS_RATISSAGE: int = 1`
- `MACHINE_STATUS_RETIRED: int = 2`
- `PIEGE_AUCUN: int = 0`
- `PIEGE_ACTIF: int = 1`
- `FACE_VIDE: int = 0`
- `FACE_REFLEXION: int = 1`
- `FACE_DEFINITIF: int = 2`
- `FURT_RIVE_PIEGE: int = 0`
- `FURT_RIVE_SABOTAGE: int = 1`
- `CHAMAN_NONE: int = 0`
- `CHAMAN_TAMBOUR: int = 1`
- `CHAMAN_CHANT: int = 2`
- `DUEL_NONE: int = 0`
- `DUEL_DEFI: int = 1`
- `DUEL_TERRITOIRE_TENU: int = 2`
- `PERCHOIR_NONE: int = 0`
- `PERCHOIR_CHAUD: int = 1`
- `PERCHOIR_CALME: int = 2`
- `PERCHOIR_KIND_RAY: int = 0`
- `PERCHOIR_KIND_RANK: int = 1`
- `PLUME_NONE: int = PERCHOIR_NONE`
- `PLUME_CHAUD: int = PERCHOIR_CHAUD`
- `PLUME_CALME: int = PERCHOIR_CALME`
- `PLUME_KIND_RAY: int = PERCHOIR_KIND_RAY`
- `PLUME_KIND_RANK: int = PERCHOIR_KIND_RANK`
- `CALE_NONE: int = 0`
- `CALE_CAIMAN: int = 1`
- `CALE_SABOTAGE: int = 1`
- `CALE_ECAILLE: int = 2`
- `MAX_ECAILLES: int = 4`
- `LISIERE_ABSENT: int = 0`
- `LISIERE_UNCONSTRUCTED: int = 1`
- `LISIERE_CONSTRUCTED: int = 2`
- `LISIERE_EJECTED: int = 3`
- `LISIERE_ROOTED: int = 3`
- `FAMILLE_GARDIEN: str = 'GARDIEN'`
- `FAMILLE_REVE: str = 'REVE'`
- `FAMILLE_CROISSANCE: str = 'CROISSANCE'`
- `CARD_NONE: int = 0`
- `CARD_SABOTAGE: int = 13`
- `CARD_ECAILLE: int = 14`
- `TILE_R_BASE: int = 100`
- `STEP_1_2_DEAL: int = 12`
- `STEP_1_3_DICE: int = 13`
- `STEP_2_1_DEF1: int = 21`
- `STEP_2_2_DEF2: int = 22`
- `STEP_3_1_CONSTRUCT: int = 31`
- `STEP_3_2_REVEAL: int = 32`
- `STEP_4_1_FURTIVITE: int = 41`
- `STEP_4_2_NIDS: int = 42`
- `STEP_5_1_TACTIQUES: int = 51`
- `STEP_5_2_RATISSAGE: int = 52`
- `STEP_5_3_END_CHECK: int = 53`
- `STEP_6_1_ENRACINEMENT: int = 61`
- `STEP_6_2_EVOLUTION: int = 62`
- `STEP_6_3_END_TURN: int = 63`
- `STEP_GAME_OVER: int = 99`
- `DOUBLE_FACE_UPGRADE_GARDIENS: frozenset[tuple[str, str]] = frozenset(((f'G{i}', 'A') for i in range(1, 16)))`
- `PEUPLES_ORDER: tuple[str, ...] = ('M', 'R', 'O', 'H', 'E', 'I')`
- `ANIMAUX_SAUVAGES: frozenset[str] = frozenset(('M', 'R', 'O'))`
- `PEUPLES_ONIRIQUES: frozenset[str] = frozenset(('H', 'E'))`
- `PEUPLE_TO_ID: dict[str, int] = {code: idx for idx, code in enumerate(PEUPLES_ORDER)}`
- `MATRICE_PAIRES: dict[str, tuple[str, str]] = ...`
- `SYNERGY_META: dict[str, tuple[str, str, int]] = ...`
- `TACTIQUES_SPEC: dict[int, TactiqueSpec] = ...`
- `RATISSAGE_TACTIQUE_SPEC: TactiqueSpec = TactiqueSpec(0, 'RATISSAGE', ('SUR_PLACE',), 0, 0, 0, True)`

### Fonctions publiques

- `is_act2_tour(tour: int) -> bool` — Retourne True à partir du Tour 5 (Acte 2, Face B de la Réglette des Tactiques).
- `is_tactique_charge(rank_1_6: int, tour: int) -> bool` — Retourne True si la case `1..6` est en mode CHARGE au tour donné. - Acte 1 (Tours 1–4, Face A) : cases 1, 2, 3 = CHARGE ; cases 4, 5, 6 = ASSAUT. - Acte 2 (Tours 5–8, Face B) : cases 1, 2, 3 = ASSAUT ; cases 4, 5, 6 = CHARGE.
- `tactique_mode_for_rank(rank_1_6: int, tour: int) -> str` — Retourne 'CHARGE' ou 'ASSAUT' pour la case `1..6` au tour donné (Réglette Face A / Face B).
- `is_tactique_code(code: int) -> bool`
- `is_reve_code(code: int) -> bool`
- `code_to_tile_id(code: int) -> str`
- `tile_id_to_code(tile_id: str) -> int`
- `machine_card_code(ray: int, m_type: int) -> int`
- `unpack_machine_card(card_code: int) -> tuple[int, int]`
- `machine_threat_key_3_2(seat: int, pos: int, status: int, eff_red: int) -> tuple[int, int, int, int, int]` — Clé canonique partagée (moteur & bots) de priorité décroissante de menace sur un Rêve en 3.2.
- `resolve_reve_rank_cancellations(entries: Sequence[tuple[int, int, int, int]], n_defenders: int) -> frozenset[int]` — Résout exactement quels sièges sont annulés par `n_defenders` sur un rang portant un Rêve. Chaque entrée est `(seat, pos, status, eff_red)`. Retourne le `frozenset` des `seat` annulés (1 machine par Défenseur, en priorisant la plus menaçante selon `machine_threat_key_3_2`).
- `slot_id_to_once_index(slot_id: str) -> int` — Convertit un identifiant d'emplacement (G1..G15, R1..R10, M1..M5, Migration) en index 0..63.
- `get_layout_report() -> dict[str, Any]` — Retourne le bilan détaillé d'allocation mémoire sur les 384 octets (6 cache lines).

### Classe `TactiqueSpec`

Profil structurel immuable d'une tuile Tactique T1..T6.

**Champs :**
- `code: int`
- `tile_id: str`
- `cibles: tuple[str, ...]`
- `avancee: int`
- `gain_rouge: int`
- `mod_seuil: int`
- `est_ratissage_profil: bool`

### Classe `GameConfig`

Configuration immuable d'une partie sur le socle canonique v6.4 (`P4_2233`, Mode 1..4).

**Champs :**
- `n_players: int`
- `mode: int`
- `peuples: tuple[str, ...]`
- `exp_seed: int`
- `rep_id: int`
- `coordonnateur_initial: int`
- `max_revision_passes: int`
- `tile_profiles: tuple[tuple[str, str], ...]`
- `symmetric_core_only: bool`
- `profil_piste: str`
- `p_max: int`
- `dotation_arbres: tuple[int, ...]`
- `lisiere_slots: tuple[str, ...]`
- `total_gardiens_partie: int`
- `total_reves_partie: int`
- `nb_animaux_sauvages: int`
- `nb_peuples_oniriques: int`

**Propriétés :**
- `has_insectes_peuple: bool` — Vrai uniquement si le Peuple Insectes ('I') siège autour de la table (clôture Essaim INV-21).
- `accessories_enabled: bool` — Vrai si les accessoires 3+3 sont actifs (actifs par défaut en Mode >= 2 sauf symmetric_core_only).
- `enracinement_enabled: bool` — Vrai si l'Enracinement volontaire au ménage est actif (actif par défaut en Mode >= 2 sauf symmetric_core_only).

**Méthodes :**
- `seat_of_peuple(self, peuple_code: str) -> int | None` — Retourne le siège contrôlant ce Peuple, ou None s'il est absent de la table.
- `profile_for_slot(self, slot_id: str) -> str | None` — Retourne le profil actif d'un emplacement (v6.2 : Bug=B & Colonie=B ; Mode 3/4 : STANDARD_A ou NEUTRE).

### Classe `ParcelObs`

**Champs :**
- `arbres: int`
- `souches: int`
- `insectes: int`
- `piege: int`
- `defenseurs: int`
- `nid_id: int`
- `nid_active_ce_tour: bool`
- `est_route: bool`

### Classe `FurtiviteCellObs`

**Champs :**
- `slots_faces: tuple[int, int, int, int]`
- `nb_def_rive_0: int`
- `nb_def_rive_1: int`
- `insectes: int`

### Classe `LisiereTileObs`

**Champs :**
- `tile_id: str`
- `status: int`
- `constructors: int`

### Classe `GardienSlotObs`

**Champs :**
- `gardien_num: int`
- `tile_id: str | None`
- `face: int`
- `remaining_defenders: int`

### Classe `TactiqueSlotObs`

**Champs :**
- `code: int`
- `tile_id: str`
- `bugs: int`

### Classe `MachineObs`

**Champs :**
- `ray: int`
- `m_type: int`
- `position: int`
- `status: int`
- `rouges: int`
- `bleus: int`

### Classe `HandObs`

Main observée d'un siège : None sur les champs secrets si paravents fermés pour autrui.

**Champs :**
- `has_card: bool`
- `card: int | None`
- `d1: int | None`
- `d2: int | None`
- `lecture_m: int | None`
- `bound_tactique: int | None`

### Classe `PlayerObservation`

Vue immuable strictement isolée sur snapshot 384 octets assaini (zéro fuite paquet/mains).

**Propriétés :**
- `n_players: int`
- `mode: int`
- `tour: int`
- `step: int`
- `coordonnateur: int`
- `paravents_ouverts: bool`
- `repousse_finale_applied: bool`
- `nb_peuples_oniriques: int`
- `gardien_pari_enabled: bool`
- `triggers_lit: int`
- `deck_remaining_count: int`
- `sabotage_deck_count: int`
- `sabotage_pending_count: int`
- `reshuffle_count: int`
- `hands: tuple[HandObs, ...]`
- `foret: tuple[tuple[ParcelObs, ...], ...]`
- `furtivite: tuple[tuple[FurtiviteCellObs, ...], ...]`
- `lisieres: tuple[LisiereTileObs, ...]`
- `piste_gardiens: tuple[GardienSlotObs, ...]`
- `piste_tactiques: tuple[TactiqueSlotObs, ...]`
- `piste_colonie: tuple[int, ...]`
- `machines: tuple[MachineObs, ...]`
- `has_insectes_peuple: bool`
- `accessories_enabled: bool`
- `enracinement_enabled: bool`
- `resonance_pending_count: int` — 1 si Résonance (icône 6) est armée pour cette vague, 0 sinon (INV-09 v6.4).
- `ecaille_deck_count: int`
- `ecaille_pending_count: int`
- `croc_parcel: tuple[int, int] | None` — Retourne `(ray, p)` si le Croc Reptile est posé sur le plateau, sinon None (en réserve).
- `duel_state: tuple[int, int, int]` — Retourne `(status, ray, p)` du jeton Duel Mammifère (`(DUEL_NONE, 0, 0)` si en réserve).
- `oiseau_has_perchoir: bool` — Vrai si un jeton est actuellement posé face cachée sur le Perchoir de Vigie de O.
- `oiseau_perchoir_card: int | None` — Code carte sur le Perchoir de O (None si masqué pour autrui ou vide si CARD_NONE).
- `is_oiseau_perchoir_revealed: bool` — Vrai si le jeton du Perchoir de O a été révélé publiquement ce tour.
- `oiseau_chose_d2: bool` — Vrai si O a retenu son 2e dé (`d2`) plutôt que `d1` (masqué aux autres paravents fermés).
- `oiseau_perchoir_signal: tuple[int, int, int, bool]` — Retourne `(face, kind, idx, locked)` du Perchoir de Vigie orientable (`face=0` si non posé).
- `oiseau_plume: tuple[int, int, int, bool]` — Alias rétro-compatible vers `oiseau_perchoir_signal`.
- `has_any_rooted_reve: bool` — Vrai si au moins un Rêve bloquant le Sommeil a été enraciné (tous Rêves sauf R1, INV-22).
- `rooted_tiles: tuple[tuple[int, str, int, int, int], ...]` — Tuiles enracinées : tuple de `(slot_idx, tile_id, ray, slot_on_rive, tier_souches)`.

**Méthodes :**
- `hand_of(self, seat: int) -> HandObs` — Accès direct O(1) à la main observée d'un siège (masquée si paravent fermé).
- `is_route(self, r: int, p: int) -> bool` — Retourne True si la parcelle (r, p) est une Route Forestière (0 Arbre, 0 Souche).
- `parcel_arbres(self, r: int, p: int) -> int` — Nombre d'Arbres debout sur (r, p) en O(1).
- `parcel_souches(self, r: int, p: int) -> int` — Nombre de Souches sur (r, p) en O(1).
- `parcel_insectes(self, r: int, p: int) -> int` — Nombre d'Insectes sur (r, p) en O(1).
- `parcel_piege(self, r: int, p: int) -> int` — État du Piège (0=aucun, 1=actif) sur (r, p) en O(1).
- `parcel_defenseurs(self, r: int, p: int) -> int` — Nombre de Défenseurs en forêt sur (r, p) en O(1).
- `parcel_def1_count(self, r: int, p: int) -> int` — Nombre de 1ers Défenseurs (Étape 2.1, publics) posés sur la parcelle (r, p).
- `parcel_has_nid(self, r: int, p: int) -> bool` — Retourne True si un Nid est présent sur (r, p) en Mode >= 2.
- `furtivite_defs_and_ins(self, lisiere: int, p: int) -> tuple[int, int]` — Retourne (nb_total_defenseurs, nb_insectes=0) sur la case Furtivité (lisiere, p) en O(1).
- `furtivite_rive_defs(self, lisiere: int, p: int, rive: int) -> int` — Retourne le nombre de Défenseurs (0..2) sur la rive `rive` (0 ou 1) de (lisiere, p) en O(1).
- `is_ray_furtivite_open(self, ray: int) -> bool` — Vrai si la piste de forêt `ray` n'est pas intégralement rasée (au moins 1 parcelle non-Route et >= 1 machine non retirée).
- `rooted_sentinels_on_ray(self, ray: int) -> int` — Nombre de tuiles enracinées en Sentinelle permanente sur la Rive Sabotage du rayon `ray` (0..2).
- `furtivite_rive_capacity(self, ray: int, rive: int) -> int` — Nombre maximal de Défenseurs actifs posables sur la rive `rive` de `ray` (Effet Sentinelle INV-14).
- `furtivite_rive_total_occupancy(self, ray: int, rive: int) -> int` — Occupation totale (Défenseurs actifs + tuiles enracinées en Sentinelle si Rive Sabotage, 0..2).
- `furtivite_ray_rive_defs(self, ray: int, rive: int) -> int` — Nombre de Défenseurs actifs (0..2) sur la rive `rive` (0=Piège, 1=Sabotage) au pied du rayon `ray`.
- `furtivite_ray_rive_split(self, ray: int, rive: int) -> tuple[int, int]` — Retourne `(nb_reflexion, nb_definitif)` sur la rive `rive` au pied du rayon `ray`.
- `furtivite_ray_def1_rive_count(self, ray: int, rive: int) -> int` — Nombre de 1ers Défenseurs (2.1, publics) posés sur la rive `rive` au pied du rayon `ray`.
- `player_def1_furtivite_target(self, seat: int) -> tuple[int, int] | None` — Retourne `(ray, rive)` si le 1er Défenseur de `seat` est en Furtivité, sinon None.
- `player_def2_furtivite_target(self, seat: int) -> tuple[int, int] | None` — Retourne `(ray, rive)` si le 2e Défenseur de `seat` est en Furtivité, sinon None.
- `mobilized_machines_for_ray(self, ray: int) -> int` — Retourne `m(ray)` (0..2) lorsque les paravents sont ouverts : jetons visibles (hors face cachée R2) + Ratissages.
- `lisiere_tile_info(self, slot_idx: int) -> tuple[str, int, int]` — Retourne (tile_id, status, constructors) pour l'emplacement de lisière `slot_idx`.
- `player_def1_lisiere_slot(self, seat: int) -> int | None` — Retourne `slot_idx` si le 1er Défenseur de `seat` est sur une tuile en lisière, sinon None.
- `player_def2_lisiere_slot(self, seat: int) -> int | None` — Retourne `slot_idx` si le 2e Défenseur de `seat` est sur une tuile en lisière, sinon None.
- `machine_pos_status(self, r: int, m_type: int) -> tuple[int, int]` — Retourne (position, status) de la machine `(r, m_type)` en O(1).
- `machine_effective_rouges(self, r: int, m_type: int) -> int` — Retourne le nombre de jetons rouges physiques (INV-12 : 0 bonus imprimé en Ratissage).
- `is_sommeil_victory(self) -> bool` — Vrai si tous les Rêves non enracinés sont en bloc à gauche ET aucun Rêve bloquant n'est enraciné (INV-22, R1).
- `count_face2_gardiens_on_track(self) -> int` — Nombre de Gardiens actuellement en piste sur leur Face 2 (Éveil cumulatif INV-10).
- `has_gardien_bet_lost_this_turn(self) -> bool` — Vrai si au moins un pari de Gardien a été perdu ce tour (y compris sauvé par Bouclier).
- `is_eveil_gardiens_victory(self) -> bool` — Éveil de la Forêt cumulatif v6.4 (INV-10, Tours 1..7, A >= 1) : au moins A + 1 Gardiens en piste en Face 2 ET 0 pari de Gardien perdu ce tour.
- `gardien_available_at_case(self, case_1_6: int) -> bool` — Retourne True si un Gardien occupe la case `1..6` et porte >= 1 2e Défenseur actif.
- `gardien_present_at_case(self, case_1_6: int) -> bool` — Retourne True si un Gardien est construit sur la case `1..6`.
- `gardien_face_at_case(self, case_1_6: int) -> int` — Retourne 0 (vide), 1 (Face 1) ou 2 (Face 2) sur la case `1..6`.
- `gardien_pari_defenders(self, case_1_6: int) -> int` — Nombre de 2es Défenseurs actifs (non consommés) posés en pari sur la case `1..6`.
- `gardien_pari_consumed(self, case_1_6: int) -> int` — Nombre de 2es Défenseurs déjà consommés par ouverture sur la case `1..6` ce tour.
- `gardien_pari_defenders_split(self, case_1_6: int) -> tuple[int, int]` — Retourne `(nb_reflexion, nb_definitif)` des 2es Défenseurs actifs sur la case `1..6`.
- `total_gardien_pari_defenders(self) -> int` — Nombre total de 2es Défenseurs actifs (non consommés) sur la Piste des Gardiens.
- `total_gardien_pari_engaged(self) -> int` — Nombre total de 2es Défenseurs engagés en 2.2 sur la Piste des Gardiens (actifs + consommés).
- `player_def2_gardien_pari_case(self, seat: int) -> int` — Retourne la case `1..6` ciblée en pari Gardien par le 2e Défenseur actif de `seat`, ou 0.
- `reve_at_case(self, case_1_6: int) -> int` — Retourne r_num (1..10) si un Rêve occupe la case `1..6`, sinon 0.
- `reve_activation_defenders(self, case_1_6: int) -> int` — Nombre de Défenseurs debout (2.1 + 2.2, encore à résoudre) posés sur le Rêve en case `1..6`.
- `reve_def1_count(self, case_1_6: int) -> int` — Nombre de 1ers Défenseurs (2.1, fixes) posés debout sur le Rêve en case `1..6`.
- `reve_activation_consumed(self, case_1_6: int) -> int` — Nombre de Défenseurs couchés (Rêve déjà résolu) sur le Rêve en case `1..6` ce tour.
- `total_reve_activation_defenders(self) -> int` — Nombre total de Défenseurs debout (2.1 + 2.2) posés sur des Rêves.
- `total_reve_activation_engaged(self) -> int` — Nombre total de Défenseurs engagés en 2.1 ou 2.2 sur des Rêves (debout + couchés).
- `reve_activation_defenders_split(self, case_1_6: int) -> tuple[int, int]` — Retourne `(nb_reflexion, nb_definitif)` des Défenseurs debout sur le Rêve en case `1..6`.
- `player_def1_reve_case(self, seat: int) -> int` — Retourne la case `1..6` ciblée sur un Rêve par le 1er Défenseur (`2.1`) de `seat`, ou 0.
- `player_def2_reve_case(self, seat: int) -> int` — Retourne la case `1..6` ciblée sur un Rêve par le 2e Défenseur (`2.2`) de `seat`, ou 0.
- `tactique_code_bugs(self, rank_0_5: int) -> tuple[int, int]` — Retourne (code, bugs) au rang `0..5` de la Réglette des Tactiques.
- `is_trigger_lit(self, case_num: int) -> bool` — Retourne True si l'icône Gardien `1..6` est allumée (bit 5 pour 6=RESONANCE, 1 fois/vague).
- `nid_has_ponte(self, m_num: int) -> bool` — Vrai si une ponte Écaille (G14) est glissée sous le Nid `M{m_num}`.
- `count_nid_pontes(self) -> int` — Nombre total de pontes G14 actuellement glissées sous des Nids.
- `machine_cale(self, r: int, m_type: int) -> int` — Retourne CALE_NONE (0) ou CALE_CAIMAN (1) sous la machine (exclusif G9).
- `machine_has_alteration(self, r: int, m_type: int) -> bool` — Retourne True si la machine porte un jeton d'Altération des Entités (E).
- `machine_is_etouffee(self, r: int, m_type: int) -> bool` — Retourne True si la machine (mobile ou Ratissage) est Étouffée (90°) ce tour.
- `machine_is_facedown(self, r: int, m_type: int) -> bool` — Retourne True si le jeton de la machine est retourné face cachée (R2 = 0 en m(r)).
- `machine_passenger_insects(self, r: int, m_type: int) -> int` — Nombre d'Insectes passagers (M1) embarqués sur cette machine.
- `humain_chaman_archetype(self, def_idx: int) -> int` — Archétype Chamane (CHAMAN_NONE/TAMBOUR/CHANT) du Défenseur `def_idx` (0 ou 1) de H.
- `discarded_die_of(self, seat: int) -> int | None` — Dé écarté (1..6) sous le paravent de `seat`, ou None si masqué/non lancé (INV-07).
- `is_slot_rooted(self, slot_idx: int) -> bool` — Vrai si la tuile de lisière `slot_idx` a été enracinée volontairement sur la Rive Sabotage.
- `slot_rooted_gue_marque(self, slot_idx: int) -> bool` — Vrai si la tuile enracinée `slot_idx` est en Gué marqué (R2 90° -> 2 Souches).
- `slot_rooted_info(self, slot_idx: int) -> tuple[int, int, int, bool] | None` — Retourne `(ray, slot_on_rive 0|1, tier_souches 1|2, blocks_sommeil)` si enraciné, sinon None.
- `list_rooted_tiles(self) -> list[tuple[int, str, int, int, int]]` — Liste toutes les tuiles enracinées : `(slot_idx, tile_id, ray, slot_on_rive, tier_souches)`.
- `waiting_defenders_count(self, seat: int) -> int` — Nombre de Défenseurs couchés « en attente » devant `seat` (après construction 3.1).

### Classe `GameState`

État complet d'une partie, intégralement contenu dans bytearray(384) + _continuation légère.

**Propriétés :**
- `tour: int`
- `step: int`
- `coordonnateur: int`
- `paravents_ouverts: bool`
- `step2_locked: bool`
- `repousse_finale_applied: bool`
- `triggers_lit: int`
- `deck_len: int`
- `deck_cursor: int`
- `sabotage_deck_count: int`
- `sabotage_pending_count: int`
- `ecaille_deck_count: int`
- `ecaille_pending_count: int`
- `reshuffle_count: int`
- `oiseau_perchoir_card: int` — Code jeton (CARD_NONE ou 1..14) posé face cachée sur le Perchoir de Vigie de O.

**Méthodes :**
- `clone(self) -> GameState` — Copie rapide et strictement indépendante à l'octet près (compatible IS-MCTS / Forks).
- `raw_used_bytes(self) -> bytes` — Extrait immuable des octets alloués (pour assertions de tests et hachage déterministe).
- `get_resonance_pending_count(self) -> int` — Retourne 1 si l'icône 6 (RESONANCE) est allumée pour la vague en cours, sinon 0 (INV-09).
- `light_trigger(self, case_num: int) -> None` — Allume l'icône Gardien `1..6` (drapeau 1 bit par icône, INV-09).
- `is_trigger_lit(self, case_num: int) -> bool`
- `clear_trigger(self, case_num: int) -> None` — Éteint l'icône Gardien `1..6`.
- `get_parcel_arbres(self, r: int, p: int) -> int`
- `get_parcel_souches(self, r: int, p: int) -> int`
- `set_parcel_arbres_souches(self, r: int, p: int, arbres: int, souches: int) -> None`
- `is_route_forestiere(self, r: int, p: int) -> bool` — Une parcelle à 0 Arbre et 0 Souche est une Route Forestière.
- `get_parcel_insectes(self, r: int, p: int) -> int`
- `set_parcel_insectes(self, r: int, p: int, count: int) -> None`
- `get_parcel_piege(self, r: int, p: int) -> int`
- `set_parcel_piege(self, r: int, p: int, state_val: int) -> None`
- `get_parcel_defenseurs(self, r: int, p: int) -> int`
- `set_parcel_defenseurs(self, r: int, p: int, count: int) -> None`
- `get_parcel_nid(self, r: int, p: int) -> tuple[int, bool]` — Retourne (m_num 1..5 ou 0, active_ce_tour).
- `get_parcel_nid_encoded(self, r: int, p: int) -> int` — Retourne 0 ou (id_slot_M | (0x80 si activé ce tour)).
- `set_parcel_nid(self, r: int, p: int, m_num: int, active_ce_tour: bool=False) -> None`
- `clear_nid(self, m_num: int) -> None`
- `set_nid_activated(self, m_num: int, active_ce_tour: bool) -> None`
- `get_nid_position(self, m_num: int) -> tuple[int, int, bool] | None` — Retourne (ray, p, active_ce_tour) si le Nid M{m_num} est en forêt, sinon None.
- `get_nid_ponte(self, m_num: int) -> bool` — Vrai si une Écaille Ponte (G14 Le Téju) est glissée sous le Nid `M{m_num}`.
- `set_nid_ponte(self, m_num: int, has_ponte: bool) -> None` — Pose ou retire une Écaille Ponte (G14 Le Téju) sous le Nid `M{m_num}`.
- `count_nid_pontes(self) -> int` — Nombre total d'Écailles Ponte (G14) actuellement glissées sous des Nids.
- `count_total_insects_on_board(self) -> int` — Total physique d'Insectes en jeu (parcelles + Réglette + Piste Gardiens + passagers).
- `next_non_razed_towards_heart(self, r: int, from_p: int) -> int | None` — Prochaine parcelle non rasée vers le cœur (p > from_p), ou None.
- `next_non_razed_towards_border(self, r: int, from_p: int) -> int | None` — Prochaine parcelle non rasée vers la bordure (p < from_p), ou None.
- `first_non_razed_from_border(self, r: int) -> int | None`
- `last_non_razed_parcel(self, r: int) -> int | None`
- `total_arbres_rayon(self, r: int) -> int`
- `total_arbres_plateau(self) -> int`
- `total_power_tokens_plateau(self) -> int` — Somme totale des jetons Puissance (rouges physiques) portés par les machines actives.
- `lisiere_ray_for_rive(self, lisiere: int, rive: int) -> int`
- `get_furtivite_slot_face(self, lisiere: int, p: int, slot_0_3: int) -> int`
- `set_furtivite_slot_face(self, lisiere: int, p: int, slot_0_3: int, face: int) -> None`
- `get_furtivite_slots(self, lisiere: int, p: int) -> tuple[int, int, int, int]`
- `get_furtivite_nb_def_rive(self, lisiere: int, p: int, rive: int) -> int`
- `get_furtivite_total_defs(self, lisiere: int, p: int) -> int`
- `get_furtivite_insectes(self, lisiere: int, p: int) -> int`
- `set_furtivite_insectes(self, lisiere: int, p: int, count: int) -> None`
- `get_player_def_loc_raw(self, seat: int, def_idx: int) -> int`
- `set_player_def_loc_raw(self, seat: int, def_idx: int, raw_loc: int) -> None`
- `is_player_def2_definitif(self, seat: int) -> bool`
- `set_player_def2_definitif(self, seat: int, is_definitif: bool) -> None`
- `decode_def_loc(self, raw_loc: int) -> tuple[str, int, int, int]` — Décode une localisation brute en (kind, a, b, c).
- `mark_defender_waiting(self, seat: int, def_idx: int) -> None` — Couche le Défenseur (seat, def_idx) « en attente » devant son propriétaire (après construction 3.1, INV-19).
- `list_waiting_defenders(self) -> list[tuple[int, int]]` — Retourne tous les `(seat, def_idx)` actuellement couchés « en attente ».
- `list_available_waiting_defenders(self) -> list[tuple[int, int]]` — Retourne tous les `(seat, def_idx)` « en attente » (bâtisseurs couchés, couchés sur Rêve résolu, ou sur une rive de Furtivité après 4.1).
- `list_defenders_on_reve_case(self, case_1_6: int) -> list[tuple[int, int]]` — Retourne tous les `(seat, def_idx)` (debout + couchés) présents sur le Rêve en `case_1_6`.
- `list_defenders_on_parcel(self, ray: int, p: int) -> list[tuple[int, int]]` — Retourne tous les `(seat, def_idx)` suivis actuellement sur la parcelle `(ray, p)`.
- `remove_player_defender(self, seat: int, def_idx: int) -> None` — Retire proprement le Défenseur (seat, def_idx) de sa position actuelle vers la main.
- `place_defender_foret(self, seat: int, def_idx: int, r: int, p: int, face: int) -> None`
- `place_defender_bourbier(self, seat: int, def_idx: int, r: int, p: int) -> None` — Pose un Chamane en Bourbier sur la Route Forestière `(r, p)` (G7 Le Tapir).
- `place_defender_saisie_harpie(self, seat: int, def_idx: int, ray: int, m_type: int) -> None` — Pose un Défenseur Oiseau en Saisie sur le jeton de la machine mobile `(ray, m_type)` (G11).
- `is_ray_furtivite_open(self, ray: int) -> bool` — Vrai si le rayon `ray` n'est pas intégralement rasé (>= 1 parcelle non-Route et >= 1 machine non retirée).
- `count_rooted_sentinels_on_ray(self, ray: int) -> int` — Nombre de tuiles enracinées en Sentinelle permanente sur la Rive Sabotage de `ray` (0, 1 ou 2).
- `get_furtivite_rive_capacity(self, ray: int, rive: int) -> int` — Nombre max de Défenseurs actifs posables sur `rive` de `ray` (Rive Piège=2, Sabotage=2-Sentinelles).
- `get_furtivite_rive_total_occupancy(self, ray: int, rive: int) -> int` — Occupation totale (Défenseurs actifs + tuiles enracinées en Sentinelle) de `rive` sur `ray` (0..2).
- `count_mobilized_machines_for_ray(self, ray: int) -> int` — Retourne `m(ray)` en 4.1 (`0`, `1` ou `2`) : jetons Machine visibles devant `ray` + Ratissages actifs. Indépendant de toute déviation ±1 et de tout Étouffement ; exclut les jetons retournés face cachée (R2).
- `place_defender_furtivite(self, seat: int, def_idx: int, ray: int, rive: int, face: int, preferred_twin: int=0) -> None` — Pose librement un Défenseur en Furtivité au pied du rayon `ray` (`rive` 0=Piège, 1=Sabotage).
- `flip_defender2_to_definitif_in_place(self, seat: int) -> None` — Retourne sur place le 2e Défenseur réflexion -> définitif (sans aucun tirage).
- `place_defender_lisiere_tile(self, seat: int, def_idx: int, lisiere_slot_idx: int, face: int) -> None`
- `count_gardien_pari_defenders_at_case(self, case_1_6: int) -> int` — Nombre de 2es Défenseurs actifs (non consommés) posés en pari sur la case `1..6`.
- `count_gardien_pari_consumed_at_case(self, case_1_6: int) -> int` — Nombre de 2es Défenseurs déjà consommés par ouverture sur la case `1..6` ce tour.
- `total_gardien_pari_remaining(self) -> int` — Nombre total de 2es Défenseurs encore actifs (non consommés) sur la Piste des Gardiens.
- `total_gardien_pari_consumed(self) -> int` — Nombre total de Défenseurs déjà consommés par ouverture de Gardiens ce tour.
- `total_gardien_pari_engaged(self) -> int` — Nombre total de Défenseurs engagés en 2.2 sur la Piste des Gardiens (actifs + consommés).
- `place_defender_gardien_pari(self, seat: int, case_1_6: int, face: int) -> None` — Engage le Défenseur de `seat` en pari d'activation sur le Gardien en case `1..6` (max 2).
- `consume_one_gardien_pari_defender(self, case_1_6: int) -> bool` — Glisse 1 Défenseur actif sur la case `1..6` dans son encoche latérale jusqu'en 6.2.
- `count_reve_activation_defenders_at_case(self, case_1_6: int) -> int` — Nombre de Défenseurs debout (encore à résoudre) posés sur le Rêve en case `1..6`.
- `count_reve_activation_consumed_at_case(self, case_1_6: int) -> int` — Nombre de Défenseurs couchés (consommés / Rêve résolu) sur le Rêve en case `1..6` ce tour.
- `total_reve_activation_remaining(self) -> int` — Nombre total de Défenseurs encore debout sur des Rêves.
- `total_reve_activation_consumed(self) -> int` — Nombre total de Défenseurs couchés sur des Rêves ce tour.
- `total_reve_activation_engaged(self) -> int` — Nombre total de Défenseurs engagés sur des Rêves (debout + couchés).
- `consume_reve_activation_defenders(self, case_1_6: int, count: int) -> int` — Couche jusqu'à `count` Défenseurs debout sur le Rêve en case `1..6` (2.1 d'abord puis 2.2).
- `lay_down_all_defenders_on_reve(self, case_1_6: int) -> int` — Couche à plat tous les Défenseurs encore debout sur le Rêve `case_1_6` (marqueur résolu, INV-15).
- `place_defender_reve_standing(self, seat: int, def_idx: int, case_1_6: int) -> None` — Pose ou transfère un Défenseur DEBOUT sur le Rêve `case_1_6` afin qu'il se résolve (R1/R2/G11).
- `count_face2_gardiens_on_track(self) -> int` — Nombre de Gardiens actuellement en piste sur leur Face 2 (0..6, Éveil cumulatif INV-10).
- `has_gardien_bet_lost_this_turn(self) -> bool` — Vrai si au moins 1 pari de Gardien a été perdu ce tour (même sauvé par Bouclier de lisière).
- `mark_gardien_bet_lost_this_turn(self) -> None` — Marque qu'au moins 1 pari de Gardien a été perdu à ce tour (INV-10 / INV-18).
- `is_eveil_attempt_eligible(self) -> bool` — Vrai si l'Éveil cumulatif est actif à ce tour (Mode 2+, A >= 1, Tours 1..7, INV-10).
- `is_eveil_gardiens_victory(self) -> bool` — Éveil de la Forêt cumulatif en piste v6.4 (Tours 1..7, A >= 1, INV-10) : au moins `A + 1` Gardiens en piste sur leur Face 2 ET 0 pari de Gardien perdu à ce tour.
- `place_defender_reve_activation(self, seat: int, case_1_6: int, face: int, *, def_idx: int=1) -> None` — Engage un Défenseur (`def_idx` 0 en 2.1 ou 1 en 2.2) de `seat` sur un Rêve en case `1..6`.
- `mark_defender_impasse(self, seat: int, def_idx: int, face: int) -> None` — Consomme le Défenseur sans pose physique lorsque 100 % des cibles légales sont épuisées.
- `get_lisiere_tile_state(self, slot_idx: int) -> tuple[int, int]` — Retourne (status, nb_constructors).
- `set_lisiere_tile_state(self, slot_idx: int, status: int, constructors: int) -> None`
- `find_lisiere_slot_by_tile_id(self, tile_id: str) -> int | None`
- `get_gardien_at_case(self, case_1_6: int) -> tuple[int, int]` — Retourne (g_num 0..15, face 1..2) sur la case 1..6.
- `set_gardien_at_case(self, case_1_6: int, g_num: int, face: int=1) -> None`
- `get_tactique_at_rank(self, rank_0_5: int) -> int`
- `set_tactique_at_rank(self, rank_0_5: int, code: int) -> None`
- `find_tactique_rank(self, code: int) -> int | None`
- `get_bugs_at_case(self, case_1_6: int) -> int`
- `set_bugs_at_case(self, case_1_6: int, count: int) -> None`
- `get_colonie_at_case(self, case_1_6: int) -> int`
- `set_colonie_at_case(self, case_1_6: int, count: int) -> None`
- `get_machine_pos_status(self, ray: int, m_type: int) -> tuple[int, int, bool]` — Retourne (pos 0..P_Max, status, pending_ratissage).
- `set_machine_pos_status(self, ray: int, m_type: int, pos: int, status: int, pending_ratissage: bool=False) -> None`
- `get_machine_tokens(self, ray: int, m_type: int) -> tuple[int, int]` — Retourne (rouges physiques, bleus).
- `get_machine_effective_rouges(self, ray: int, m_type: int) -> int` — Retourne le nombre de jetons rouges physiques (v6.2 INV-12 : 0 bonus imprimé en Ratissage).
- `set_machine_tokens(self, ray: int, m_type: int, rouges: int, bleus: int) -> None`
- `machines_on_parcel(self, ray: int, p: int) -> list[int]` — Retourne la liste des types de machines physiquement présentes sur (ray, p).
- `is_sommeil_victory(self) -> bool` — Vrai si tous les Rêves en jeu (hors R1 enraciné non bloquant) sont en bloc à gauche (INV-22).
- `count_active_cale_ecaille(self) -> int` — Nombre de jetons Écaille actuellement glissés en cale (0 en v6.4 ; conservé pour compatibilité).
- `count_total_ecailles_in_play(self) -> int` — Total physique d'Écailles sorties de la réserve Reptile (sac + attente + pontes G14 + cales <= 4).
- `add_ecaille_to_bag(self, count: int=1) -> int` — Ajoute jusqu'à `count` jetons Écaille depuis la réserve Reptile (plafond physique 4). Retourne le nombre ajouté.
- `add_permanent_sabotage(self, count: int=1, *, light_case_3: bool=True) -> None` — Ajoute définitivement +count jetons Sabotage (rejoignent le sac au ménage 6.3).
- `rebuild_and_shuffle_machine_deck(self, *, increment_reshuffle: bool) -> None` — Reconstitue le sac opaque hors Ratissages/retirées + Sabotages + Écailles et vide le Perchoir.
- `remove_machine_card_from_deck_if_present(self, card_code: int) -> None` — Retire une carte Machine du paquet restant si elle passe en Siège en 1.1.
- `draw_next_machine_card(self) -> int` — Pioche la prochaine carte du paquet Machine (ou CARD_NONE si paquet épuisé).
- `get_player_hand(self, seat: int) -> tuple[int, int, int, int, int]` — Retourne (card_code, d1, d2, lecture_m, bound_tactique) pour seat.
- `set_player_hand(self, seat: int, card: int, d1: int=0, d2: int=0, lecture_m: int=0, bound_tactique: int=0) -> None`
- `get_machine_turn_stats(self, ray: int, m_type: int) -> tuple[int, bool, bool]` — Retourne (damaged_parcels_count 0..3, gained_red, attacked_this_turn).
- `set_machine_turn_stats(self, ray: int, m_type: int, damaged_count: int, gained_red: bool, attacked: bool) -> None`
- `has_reve_opened_this_turn(self, r_num: int) -> bool`
- `mark_reve_opened_this_turn(self, r_num: int) -> None`
- `was_seat_cancelled_by_reve_this_turn(self, seat: int) -> bool` — Vrai si la machine du siège `seat` a déjà été annulée par un Rêve en 3.2 ce tour.
- `mark_seat_cancelled_by_reve_this_turn(self, seat: int) -> None` — Marque le siège `seat` comme ayant eu sa machine annulée par un Rêve en 3.2.
- `get_step2_pass_state(self) -> tuple[int, bool]` — Retourne (pass_idx 0..15, moved_in_pass).
- `set_step2_pass_state(self, pass_idx: int, moved_in_pass: bool) -> None`
- `get_global_mod_seuil_turn(self) -> int` — Modificateur global transitoire de Seuil de Parade pour le tour (-64..+63).
- `add_global_mod_seuil_turn(self, delta: int) -> None` — Ajoute un bonus/malus transitoire global au Seuil de Parade pour le tour.
- `get_machine_seuil_mod_turn(self, ray: int, m_type: int) -> int` — Modificateur transitoire de Seuil porté par une machine pour le tour (-8..+7).
- `add_machine_seuil_mod_turn(self, ray: int, m_type: int, delta: int) -> None` — Ajoute un bonus/malus transitoire de Seuil sur une machine (ex: G1 B Face 1, R10 A).
- `get_parcel_seuil_mod_turn(self, r: int, p: int) -> int` — Modificateur transitoire de Seuil sur la parcelle (r, p) pour le tour (-64..+63).
- `add_parcel_seuil_mod_turn(self, r: int, p: int, delta: int) -> None` — Ajoute un bonus/malus transitoire de Seuil sur la parcelle (r, p) (ex: G4 A, G11 A, R9 A).
- `get_parcel_flags_turn(self, r: int, p: int) -> int` — Retourne le bitmask transitoire de la parcelle (r, p) pour le tour.
- `has_parcel_flag_turn(self, r: int, p: int, flag_mask: int) -> bool` — Vérifie si le drapeau transitoire `flag_mask` est actif sur (r, p) ce tour.
- `set_parcel_flag_turn(self, r: int, p: int, flag_mask: int, active: bool=True) -> None` — Active ou désactive un drapeau transitoire de parcelle (SANCTUAIRE_SOUCHE, MATAMATA, etc.).
- `has_used_once_per_turn(self, lock_idx: int) -> bool` — Vérifie si le verrou 'une fois par tour' `lock_idx` (0..63) a déjà servi ce tour.
- `mark_used_once_per_turn(self, lock_idx: int) -> None` — Verrouille l'index `lock_idx` (0..63) pour le reste du tour.
- `has_slot_used_once_per_turn(self, slot_id: str) -> bool` — Vérifie si l'emplacement `slot_id` (ex: 'G3', 'R4', 'M1') a utilisé son quota 1/tour.
- `mark_slot_used_once_per_turn(self, slot_id: str) -> None` — Marque l'emplacement `slot_id` comme ayant utilisé son effet limité à 1 fois par tour.
- `has_gardien_opened_this_turn(self, case_1_6: int) -> bool` — Vrai si le Gardien de la case `1..6` s'est déjà ouvert au moins une fois ce tour.
- `mark_gardien_opened_this_turn(self, case_1_6: int) -> None` — Marque la case Gardien `1..6` comme ayant déjà été ouverte ce tour.
- `was_seat_deviated_by_bug_this_turn(self, seat: int) -> bool` — Vrai si la carte Machine du siège `seat` a déjà été déviée par un Bug en 3.2 ce tour.
- `mark_seat_deviated_by_bug_this_turn(self, seat: int) -> None` — Marque le siège `seat` comme ayant consommé son déclencheur 3.2 sur 6. Insecte (Bug).
- `get_reve_advance_dest_rank(self, rank_0_5: int) -> int | None` — Retourne l'index `0..5` de la 1re case non-Rêve à gauche de `rank_0_5`, ou None si bloqué au bord.
- `shift_reve_block_left(self, rank_0_5: int) -> int | None` — Glisse le Rêve en `rank_0_5` d'1 rang à gauche en poussant tout bloc contigu et ses Défenseurs (INV-15). Retourne le nouvel index `rank_0_5 - 1` du Rêve poussé, ou None s'il est bloqué contre le rang 1.
- `move_reve_to_free_rank(self, src_rank_0_5: int, dst_rank_0_5: int) -> bool` — Glisse le Rêve de `src_rank_0_5` vers le rang libre (non-Rêve) `dst_rank_0_5` avec ses Défenseurs.
- `slide_reve_1_free_left(self, rank_0_5: int) -> int | None` — Glisse le Rêve en `rank_0_5` vers `rank_0_5 - 1` UNIQUEMENT si ce rang est libre (non-Rêve).
- `swap_tactique_ranks(self, rank_a: int, rank_b: int) -> None` — Échange les tuiles Rêve présentes aux rangs `rank_a` et `rank_b` avec leurs Défenseurs solidaires.
- `get_croc_parcel(self) -> tuple[int, int] | None` — Retourne `(ray, p)` si le Croc Reptile est en forêt, ou None s'il est en réserve.
- `set_croc_parcel(self, ray: int, p: int) -> None` — Pose ou déplace le Croc Reptile sur la parcelle `(ray, p)` (peut cohabiter avec un Piège).
- `clear_croc(self) -> None` — Renvoie le Croc dans la réserve Reptile.
- `get_machine_cale(self, ray: int, m_type: int) -> int` — Retourne CALE_NONE (0) ou CALE_CAIMAN (1) sous la machine (exclusif G9 Le Caïman noir).
- `set_machine_cale(self, ray: int, m_type: int, cale_type: int) -> None` — Pose (ou retire via CALE_NONE) la cale exclusive du Caïman noir (G9) sous une machine mobile.
- `clear_all_cales(self) -> None` — Retire la cale du Caïman noir de toutes les machines (lorsque G9 quitte la Piste des Gardiens).
- `find_machine_with_cale(self) -> tuple[int, int] | None` — Retourne `(ray, m_type)` de la machine portant la cale du Caïman noir, ou None.
- `has_machine_alteration(self, ray: int, m_type: int) -> bool` — Vrai si la machine porte un jeton d'Altération des Entités (max 1 par machine mobile).
- `set_machine_alteration(self, ray: int, m_type: int, active: bool) -> None` — Pose ou retire le jeton d'Altération des Entités sur la machine `(ray, m_type)`.
- `is_machine_etouffee_this_turn(self, ray: int, m_type: int) -> bool` — Vrai si la machine (mobile ou Ratissage) est Étouffée (90°) pour ce tour (INV-08 / INV-12).
- `mark_machine_etouffee_this_turn(self, ray: int, m_type: int) -> None` — Marque la machine `(ray, m_type)` comme Étouffée (90°) pour le reste du tour.
- `is_machine_facedown_this_turn(self, ray: int, m_type: int) -> bool` — Vrai si le jeton Machine est retourné face cachée devant son rayon (0 dans m(r), R2).
- `mark_machine_facedown_this_turn(self, ray: int, m_type: int) -> None` — Retourne le jeton Machine face cachée devant son rayon pour le compte Furtivité 4.1 (R2).
- `was_seat_altered_this_turn(self, seat: int) -> bool` — Vrai si la machine révélée par `seat` en 3.2 a été altérée (recul + Étouffement).
- `mark_seat_altered_this_turn(self, seat: int) -> None` — Marque le siège `seat` comme ayant eu sa machine altérée en 3.2.
- `get_machine_passenger_insects(self, ray: int, m_type: int) -> int` — Nombre d'Insectes passagers (M1) actuellement embarqués sur cette machine.
- `set_machine_passenger_insects(self, ray: int, m_type: int, count: int) -> None` — Définit le nombre d'Insectes passagers (0..15) sur la machine (0 si I absent).
- `get_duel_state(self) -> tuple[int, int, int]` — Retourne `(status, ray, p)` du jeton Duel Mammifère (`(DUEL_NONE, 0, 0)` si en réserve).
- `set_duel_defi(self, ray: int, p: int) -> None` — Pose ou déplace le jeton Duel face `DEFI` sur la parcelle `(ray, p)`.
- `set_duel_state_at(self, ray: int, p: int, face: int, *, allow_route: bool=False) -> None` — Pose ou déplace le jeton Duel avec sa face (`DEFI` ou `TERRITOIRE_TENU`) sur `(ray, p)`.
- `set_duel_bourbier(self, ray: int, p: int, face: int=DUEL_DEFI) -> None` — Pose le jeton Duel (en conservant sa face) sur une Route Forestière en Bourbier (G7 Le Tapir).
- `flip_duel_to_territoire_tenu(self) -> bool` — Bascule le Duel de `DEFI` vers `TERRITOIRE_TENU` en place. Retourne True si basculé.
- `flip_duel_to_defi(self) -> bool` — Bascule le Duel de `TERRITOIRE_TENU` vers `DEFI` en place (G4 Second cri / G7 F2 Bourbier).
- `clear_duel(self) -> None` — Renvoie le jeton Duel dans la réserve Mammifère.
- `is_duel_territoire_tenu_at(self, ray: int, p: int) -> bool` — Vrai si le jeton Duel est sur la parcelle non-Route `(ray, p)` face `TERRITOIRE_TENU`.
- `get_bourbier_at(self, ray: int, p: int) -> tuple[str, int, int] | None` — Retourne `("DUEL", duel_face, 0)` ou `("CHAMAN", seat, def_idx)` si un Bourbier G7 occupe cette Route.
- `clear_all_bourbiers(self) -> None` — Nettoie tous les Bourbiers G7 lorsque Le Tapir quitte la Piste des Gardiens.
- `get_humain_chaman_archetype(self, def_idx: int) -> int` — Retourne l'archétype Chamane (CHAMAN_NONE/TAMBOUR/CHANT) du pion `def_idx` (0 ou 1) de H.
- `set_humain_chaman_archetype(self, def_idx: int, archetype: int) -> None` — Enregistre l'archétype du pion `def_idx` de H et impose automatiquement l'autre au binôme.
- `is_chant_on_reve_case(self, case_1_6: int) -> bool` — Vrai si le pion Chamane `CHANT` des Humains (H) défend (debout ou couché) le Rêve en `case_1_6`.
- `is_tambour_on_reve_case(self, case_1_6: int) -> bool` — Vrai si le pion Chamane `TAMBOUR` des Humains (H) défend (debout ou couché) le Rêve en `case_1_6`.
- `get_humain_tambour_parcel(self) -> tuple[int, int] | None` — Retourne `(ray, p)` si le pion Chamane `TAMBOUR` de H est sur une parcelle forêt, sinon None.
- `is_oiseau_perchoir_revealed(self) -> bool` — Vrai si le jeton du Perchoir de Vigie a été révélé publiquement ce tour.
- `reveal_oiseau_perchoir(self) -> None` — Révèle publiquement le jeton du Perchoir de Vigie pour le reste du tour.
- `get_oiseau_chose_d2(self) -> bool` — Vrai si l'Oiseau (O) a librement choisi de retenir son 2e dé (`d2`) plutôt que `d1` (INV-07).
- `set_oiseau_chose_d2(self, chose_d2: bool) -> None` — Enregistre le choix secret de dé retenu de O (`False`=d1, `True`=d2 ; INV-07).
- `get_player_discarded_die(self, seat: int) -> int` — Retourne le dé écarté (1..6, ou 0 si aucun dé lancé) sous le paravent de `seat` (G12 / INV-07).
- `was_seat_ibijau_moved_f2(self, seat: int) -> bool` — Vrai si G12 Face 2 (L'Ibijau) a déplacé le dé de `seat` ce tour (glissement Rêve si Étouffée).
- `mark_seat_ibijau_moved_f2(self, seat: int) -> None` — Marque le siège `seat` comme déplacé par G12 Face 2 ce tour.
- `get_oiseau_perchoir_signal(self) -> tuple[int, int, int, bool]` — Retourne `(face, kind, idx, locked)` du Perchoir de Vigie orientable (`face=0` si non posé).
- `set_oiseau_perchoir_signal(self, face: int, kind: int, idx: int, *, locked: bool=False) -> None` — Pose ou ajuste le Perchoir de Vigie (`face`: CHAUD/CALME, `kind`: RAY/RANK, `idx`: 0..5).
- `lock_oiseau_perchoir_signal(self) -> None` — Fige le Perchoir de Vigie lorsque O retourne son 2e pion sur Définitif (INV-03 / INV-20).
- `get_oiseau_plume(self) -> tuple[int, int, int, bool]`
- `set_oiseau_plume(self, face: int, kind: int, idx: int, *, locked: bool=False) -> None`
- `lock_oiseau_plume(self) -> None`
- `is_slot_rooted(self, slot_idx: int) -> bool` — Vrai si l'emplacement de lisière `slot_idx` a été enraciné volontairement sur la Rive Sabotage.
- `is_tile_id_rooted(self, tile_id: str) -> bool` — Vrai si la tuile `tile_id` fait partie de la table et est actuellement enracinée.
- `is_slot_rooted_gue_marque(self, slot_idx: int) -> bool` — Vrai si la tuile enracinée `slot_idx` porte la marque 90° Gué marqué (R2 -> 2 Souches).
- `get_slot_rooted_info(self, slot_idx: int) -> tuple[int, int, int, bool] | None` — Retourne `(ray, slot_on_rive 0|1, tier_souches 1|2, blocks_sommeil)` si enraciné, sinon None.
- `root_tile_on_sabotage_bank(self, slot_idx: int, ray: int, *, tier_souches: int=1, gue_marque: bool=False) -> None` — Enracine la tuile construite `slot_idx` sur une place libre de la Rive Sabotage de `ray` (INV-14 / INV-22).
- `list_rooted_tiles(self) -> list[tuple[int, str, int, int, int]]` — Liste toutes les tuiles enracinées : `(slot_idx, tile_id, ray, slot_on_rive, tier_souches)`.
- `has_any_rooted_reve(self) -> bool` — Vrai si au moins un Rêve bloquant le Sommeil a été enraciné (tous Rêves sauf R1, INV-22).
- `was_machine_pushed_heart_this_turn(self, ray: int, m_type: int) -> bool` — Vrai si une création de Route en bordure a déjà poussé cette machine vers le cœur (INV-13).
- `mark_machine_pushed_heart_this_turn(self, ray: int, m_type: int) -> None` — Marque la machine comme déjà poussée d'1 parcelle vers le cœur sur création de Route en bordure.
- `reset_transient_modifiers(self) -> None` — Remet intégralement à zéro la plage dédiée de modificateurs transitoires en 6.2.
- `cleanup_end_of_turn_6_2(self) -> None` — Ménage rapide de fin de tour 6.2 par tranches mémoire contiguës + descente Insectes passagers (INV-21).
- `get_observation(self, seat_id: int) -> PlayerObservation` — Construit une vue immuable strictement isolée sur snapshot 384B assaini en O(1).

## PRNG adressable par événement (`engine.rng`)

*Source : `engine/rng.py`*

> PRNG déterministe adressable par événement (CRN & Forks, 100 % stdlib PyPy 3.11).

### Constantes publiques

- `T = TypeVar('T')`
- `MASK64: int = 18446744073709551615`
- `SRC_DICE: int = 1`
- `SRC_MACHINE_SHUFFLE: int = 2`
- `SRC_TACTICS_SETUP: int = 3`
- `SRC_BOT_TIEBREAK: int = 4`
- `rand_event = rand_u64`

### Fonctions publiques

- `rand_u64(exp_seed: int, rep_id: int, source_type: int, tour: int, entity_id: int, draw_idx: int) -> int` — Génère un entier 64 bits déterministe pur à partir du tuple d'adresse à 6 clés. Conçu sans état global ni hashlib pour tourner à pleine vitesse sous le JIT de PyPy 3.11 tout en garantissant l'indépendance CRN stricte entre sources, tours et entités.
- `rand_below(upper: int, exp_seed: int, rep_id: int, source_type: int, tour: int, entity_id: int, draw_idx: int) -> int` — Retourne un entier uniforme dans [0, upper) par réduction entière 128 bits.
- `roll_d6(exp_seed: int, rep_id: int, source_type: int, tour: int, entity_id: int, draw_idx: int) -> int` — Lance un dé à 6 faces déterministe retournant une valeur dans 1..6.
- `shuffle_deterministic(items: Sequence[T], exp_seed: int, rep_id: int, source_type: int, tour: int, entity_id: int=0) -> list[T]` — Retourne une copie mélangée par Fisher-Yates adressé par idx décroissant.

## Bus des 7 Primitives & Hooks Mode 4 (`engine.primitives`)

*Source : `engine/primitives.py`*

> Bus des 7 Primitives Formelles, 6 Verbes du Cœur v6.4, structures de décision/fin et registre de hooks Mode 4.

### Constantes publiques

- `CAUSE_TOUR_8: str = 'TOUR_8_ATTEINT'`
- `CAUSE_REVE_RANG_1: str = 'REVE_RANG_1'`
- `CAUSE_REVEIL_GARDIENS: str = 'REVEIL_GARDIENS'`
- `DEC_EFFET_TUILE: str = 'EFFET_TUILE'`
- `PRIM_MOD_SEUIL: str = 'MOD_SEUIL'`
- `PRIM_CREATION_ENTITE: str = 'CREATION_ENTITE'`
- `PRIM_DEPLACEMENT: str = 'DEPLACEMENT'`
- `PRIM_MOD_PUISSANCE: str = 'MOD_PUISSANCE'`
- `PRIM_PERMUTATION_PISTE: str = 'PERMUTATION_PISTE'`
- `PRIM_PARTAGE_INFO_ETAT_GARDIEN: str = 'PARTAGE_INFO_ETAT_GARDIEN'`
- `PRIM_MOD_LOI_DU_COEUR: str = 'MOD_LOI_DU_COEUR'`
- `ALL_PRIMITIVES: tuple[str, ...] = ...`
- `HOOK_1_3_LECTURE_DE: str = 'HOOK_1_3_LECTURE_DE'`
- `HOOK_2_1_DEBUT: str = 'HOOK_2_1_DEBUT'`
- `HOOK_2_1_PORTEE_DEF1: str = 'HOOK_2_1_PORTEE_DEF1'`
- `HOOK_3_1_CONSTRUCTION: str = 'HOOK_3_1_CONSTRUCTION'`
- `HOOK_3_2_REVELATION: str = 'HOOK_3_2_REVELATION'`
- `HOOK_3_2_CALE_REVEAL: str = 'HOOK_3_2_CALE_REVEAL'`
- `HOOK_3_2_ECAILLE_REVELEE: str = 'HOOK_3_2_ECAILLE_REVELEE'`
- `HOOK_3_2_APRES_DEVIATION: str = 'HOOK_3_2_APRES_DEVIATION'`
- `HOOK_3_2_OUVERTURE_REVE: str = 'HOOK_3_2_OUVERTURE_REVE'`
- `HOOK_3_2_APRES_REVELATION: str = 'HOOK_3_2_APRES_REVELATION'`
- `HOOK_GARDIEN_OUVERTURE: str = 'HOOK_GARDIEN_OUVERTURE'`
- `HOOK_4_1_FURTIVITE: str = 'HOOK_4_1_FURTIVITE'`
- `HOOK_4_2_NID_AVANT_PROD: str = 'HOOK_4_2_NID_AVANT_PROD'`
- `HOOK_4_2_NID_APRES_PROD: str = 'HOOK_4_2_NID_APRES_PROD'`
- `HOOK_4_3_MIGRATION_DESTS: str = 'HOOK_4_3_MIGRATION_DESTS'`
- `HOOK_5_DEBUT: str = 'HOOK_5_DEBUT'`
- `HOOK_5_ORDRE_RAYON: str = 'HOOK_5_ORDRE_RAYON'`
- `HOOK_5_CIBLAGE_MACHINE: str = 'HOOK_5_CIBLAGE_MACHINE'`
- `HOOK_5_BOURBIER_CHECK: str = 'HOOK_5_BOURBIER_CHECK'`
- `HOOK_5_LAW_QUERY: str = 'HOOK_5_LAW_QUERY'`
- `HOOK_5_PARADE_JAGUAR: str = 'HOOK_5_PARADE_JAGUAR'`
- `HOOK_5_PARADE_HARPIE: str = 'HOOK_5_PARADE_HARPIE'`
- `HOOK_5_PARADE_PONTE: str = 'HOOK_5_PARADE_PONTE'`
- `HOOK_5_PARADE_SOLDATS: str = 'HOOK_5_PARADE_SOLDATS'`
- `HOOK_5_SEUIL_PARADE: str = 'HOOK_5_SEUIL_PARADE'`
- `HOOK_5_DEFENSE_PARCELLE: str = 'HOOK_5_DEFENSE_PARCELLE'`
- `HOOK_5_APRES_PARADE_PIEGE: str = 'HOOK_5_APRES_PARADE_PIEGE'`
- `HOOK_5_PARADE_CLASSIQUE: str = 'HOOK_5_PARADE_CLASSIQUE'`
- `HOOK_5_TERRASSEMENT: str = 'HOOK_5_TERRASSEMENT'`
- `HOOK_5_CONTACT_NID: str = 'HOOK_5_CONTACT_NID'`
- `HOOK_5_FIN_ATTAQUE_MACHINE: str = 'HOOK_5_FIN_ATTAQUE_MACHINE'`
- `HOOK_5_3_PRE_RETRAIT: str = 'HOOK_5_3_PRE_RETRAIT'`
- `HOOK_MACHINE_RECUL: str = 'HOOK_MACHINE_RECUL'`
- `HOOK_ENRACINEMENT: str = 'HOOK_ENRACINEMENT'`
- `HOOK_REPOUSSE_FINALE: str = 'HOOK_REPOUSSE_FINALE'`
- `HOOK_EFFECT_RESUME: str = 'HOOK_EFFECT_RESUME'`
- `EffectHandler = Callable[[GameState, str, dict[str, Any]], Any]`

### Fonctions publiques

- `register_tile(slot_id: str, profile: str, hooks: Sequence[str]=()) -> Callable[[EffectHandler], EffectHandler]` — Décorateur d'enregistrement d'un profil stateless (slot_id, profile).
- `get_tile_registration(slot_id: str, profile: str) -> TileRegistration | None`
- `list_registered_tiles() -> tuple[tuple[str, str], ...]`
- `clear_tile_registry() -> None`
- `has_pending_decision(state: GameState) -> bool` — Retourne True si une DecisionRequest est déjà en tête de la pile de continuation.
- `push_continuation_sequence(state: GameState, frames: Sequence[tuple[Any, ...]]) -> None` — Empile une séquence de frames en tête de continuation dans leur ordre chronologique naturel (C3-02).
- `push_effect_decision(state: GameState, decideur: int, options: Sequence[Any], context: dict[str, Any], *, slot_id: str, profile: str, resume_tag: str='RESUME', resume_payload: tuple[Any, ...]=(), decision_type: str=DEC_EFFET_TUILE) -> DecisionRequest` — Suspend proprement un effet de tuile sur une DecisionRequest gouvernée par `decideur`.
- `dispatch_hook(state: GameState, hook_name: str, ctx: dict[str, Any] | None=None) -> list[Any]` — Exécute le bus de hooks pour les tuiles en jeu ayant un profil actif. En Mode 1 : retourne immédiatement []. En Mode 2 : neutralise les textes de G/R/M (profile_for_slot -> None) tout en laissant passer les hooks structurels et Migration A/A. Si un handler suspend via push_effect_decision, met en file les handlers restants.
- `prim_mod_seuil(state: GameState, delta: int, *, ray: int | None=None, p: int | None=None, m_type: int | None=None) -> None` — Primitive 1 : MOD_SEUIL — modifie le Seuil de Parade (parcelle, rayon, machine ou global).
- `prim_creation_entite(state: GameState, entity_type: str, *, ray: int=0, p: int=1, lisiere: int | None=None, m_type: int=0, cale_type: int=CALE_SABOTAGE, count: int=1, light_trigger: bool=True) -> None` — Primitive 2 : CREATION_ENTITE — crée Insecte, Piège, Croc, Sabotage, Écaille, Altération, Cale ou Arbre.
- `apply_machine_nid_contact(state: GameState, ray: int, p: int) -> bool` — Règle v6.2 (INV-16) : zéro écrasement au contact hors Route Forestière. Nids, Insectes, Pièges, Croc et Duel cohabitent pacifiquement avec toute machine en forêt. Seule la création d'une Route Forestière (0 Arbre, 0 Souche) vide la case.
- `prim_deplacement(state: GameState, entity_type: str, *, src_ray: int=0, src_p: int=1, dst_ray: int=0, dst_p: int=1, src_lisiere: int | None=None, dst_lisiere: int | None=None, src_lisiere_slot: int | None=None, from_waiting: bool=False, src_seat: int | None=None, src_def_idx: int | None=None, dst_furtivite_rive: int | None=None, m_type: int=0, dst_machine_type: int | None=None, global_track: str | None=None, global_case: int=1, count: int=1) -> bool` — Primitive 3 : DEPLACEMENT — déplace Insecte, Machine mobile, Piège ou Défenseur.
- `prim_mod_puissance(state: GameState, ray: int, m_type: int, *, delta_rouges: int=0, delta_bleus: int=0, flip_rouge_to_bleu: int=0) -> None` — Primitive 4 : MOD_PUISSANCE — ajuste les jetons Puissance rouges et bleus Surchauffe.
- `prim_permutation_piste(state: GameState, action: str, *, rank_a: int=0, rank_b: int=0, seat: int=0, seat_a: int=0, seat_b: int=0, delta_m: int=0, rebind_tactique: bool=False) -> bool` — Primitive 5 : PERMUTATION_PISTE — glissement contigu Rêve, échange de rangs ou décalage dé M.
- `prim_partage_info_etat_gardien(state: GameState, action: str, *, case_1_6: int=1, new_face: int=2) -> bool` — Primitive 7 : PARTAGE_INFO_ETAT_GARDIEN — états Gardiens & ouverture paravents.
- `prim_mod_loi_du_coeur(state: GameState, law_id: str, *, active: bool=True) -> bool` — Primitive 8 : MOD_LOI_DU_COEUR — point d'entrée typé des Lois passives/temporaires.
- `verb_refroidir(state: GameState, ray: int, m_type: int, count: int=1) -> int` — Verbe 1 (Refroidir) : retourne jusqu'à `count` jetons Rouges existants en Bleus Surchauffe (−1). Fonctionne sur machine mobile OU en Ratissage ; jamais de Bleu posé à sec depuis la réserve (INV-02).
- `verb_alterer(state: GameState, ray: int, m_type: int) -> bool` — Verbe 2 (Altérer) : pose 1 jeton d'Altération sur une machine mobile sans Altération (jamais Ratissage).
- `verb_reculer(state: GameState, ray: int, m_type: int) -> bool` — Verbe 3 (Reculer) : déplace une machine mobile d'1 parcelle vers la bordure en sautant les Routes. Sans effet sur une machine en Ratissage ou déjà sur la 1re parcelle ; déclenche `HOOK_MACHINE_RECUL` (R7).
- `verb_etouffer(state: GameState, ray: int, m_type: int, *, seat: int | None=None) -> bool` — Verbe 4 (Étouffer) : neutralise toute l'activation restante de la machine à ce tour (90° + dé retiré). Couvre aussi bien une machine mobile (jeton incliné à 90° et dé retiré de 1..6) qu'une machine en Ratissage (tournée à 90° sur place jusqu'au ménage, INV-08 / INV-12).
- `verb_semer_au_sac(state: GameState, token_type: str='SABOTAGE', count: int=1) -> int` — Verbe 5 (Semer au sac) : glisse `count` jetons (SABOTAGE ou ECAILLE) au sac sans allumer d'icône.
- `verb_glisser_reve(state: GameState, rank_0_5: int, *, dst_rank_0_5: int | None=None, push_block: bool=False) -> int | None` — Verbe 6 (Glisser un Rêve) : déplace un Rêve sur la Réglette avec ses Défenseurs (debout/couchés).
- `prim_deplacement_nid(state: GameState, m_num: int, dst_ray: int, dst_p: int) -> bool` — Déménagement unifié d'un Nid (INV-21) : emporte tous ses Insectes, Défenseurs et son éventuelle ponte.
- `prim_insecte_take_with_priming(state: GameState, src: tuple[Any, ...]) -> tuple[bool, int]` — Prélève 1 Insecte depuis `src` (ou réserve si 0 Insecte en jeu — Amorçage natif INV-21). Retourne `(ok, colonie_case_or_0)` où `colonie_case_or_0` vaut `1..6` si prélevé sur une icône Gardien.
- `list_targeted_parcels(state: GameState) -> tuple[tuple[int, int], ...]` — Retourne toutes les « parcelles ciblées » actuelles (hors machines Étouffées, incluant Ratissages, INV-12).
- `list_machines_targeting_parcel(state: GameState, ray: int, p: int, *, mobile_only: bool=False) -> tuple[tuple[int, int], ...]` — Retourne les machines `(ray, m_type)` non Étouffées n'ayant pas encore frappé qui visent `(ray, p)`.

### Classe `DecisionRequest`

Suspension déterministe de la machine à états demandant un choix légal à un siège.

**Champs :**
- `decideur: int`
- `decision_type: str`
- `options: tuple[Any, ...]`
- `context: dict[str, Any]`

### Classe `GameOver`

Résultat final d'une partie après Repousse Finale.

**Champs :**
- `tour_fin: int`
- `cause_fin: str`
- `score_arbres: int`
- `ratio_arbres: float`

### Classe `TileRegistration`

**Champs :**
- `slot_id: str`
- `profile: str`
- `hooks: tuple[str, ...]`
- `handler: EffectHandler`

## Registre stateless des tuiles (`engine.effects.registry`)

*Source : `engine/effects/registry.py`*

> Registre stateless des effets de tuiles (conforme au garde-fou AST verify_lot.py).
