# Contrat API Publique du Noyau Scellé (`core_state_api.md`)

Ce document est généré automatiquement par `scripts_cloud/export_api_doc.py` via inspection AST.
Les modules d'effets stateless dans `engine/effects/*.py` doivent utiliser **exclusivement**
les constantes, structures, accesseurs et primitives listés ci-dessous (zéro accès à `_buf`,
zéro `import random`, zéro état global mutable).

---

## État de jeu (`engine.state`)

*Source : `engine/state.py`*

> État de jeu déterministe scellé sur bytearray(384) et vue isolée PlayerObservation.

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
- `PIEGE_DECLENCHE: int = 2`
- `FACE_VIDE: int = 0`
- `FACE_REFLEXION: int = 1`
- `FACE_DEFINITIF: int = 2`
- `LISIERE_ABSENT: int = 0`
- `LISIERE_UNCONSTRUCTED: int = 1`
- `LISIERE_CONSTRUCTED: int = 2`
- `LISIERE_EJECTED: int = 3`
- `FAMILLE_GARDIEN: str = 'GARDIEN'`
- `FAMILLE_REVE: str = 'REVE'`
- `FAMILLE_CROISSANCE: str = 'CROISSANCE'`
- `CARD_NONE: int = 0`
- `CARD_SABOTAGE: int = 13`
- `TILE_R_BASE: int = 100`
- `STEP_1_1_RATISSAGE: int = 11`
- `STEP_1_2_DEAL: int = 12`
- `STEP_1_3_DICE: int = 13`
- `STEP_2_1_DEF1: int = 21`
- `STEP_2_2_DEF2: int = 22`
- `STEP_3_1_CONSTRUCT: int = 31`
- `STEP_3_2_REVEAL: int = 32`
- `STEP_4_1_FURTIVITE: int = 41`
- `STEP_4_2_NIDS: int = 42`
- `STEP_4_3_MIGRATION: int = 43`
- `STEP_5_1_TACTIQUES: int = 51`
- `STEP_5_2_RATISSAGE: int = 52`
- `STEP_5_3_END_CHECK: int = 53`
- `STEP_6_1_APPRENTISSAGE: int = 61`
- `STEP_6_2_EVOLUTION: int = 62`
- `STEP_6_3_END_TURN: int = 63`
- `STEP_GAME_OVER: int = 99`
- `DOUBLE_FACE_UPGRADE_GARDIENS: frozenset[tuple[str, str]] = ...`
- `PEUPLES_ORDER: tuple[str, ...] = ('M', 'R', 'O', 'H', 'E', 'I')`
- `ANIMAUX_SAUVAGES: frozenset[str] = frozenset(('M', 'R', 'O'))`
- `PEUPLES_ONIRIQUES: frozenset[str] = frozenset(('H', 'E'))`
- `PEUPLE_TO_ID: dict[str, int] = {code: idx for idx, code in enumerate(PEUPLES_ORDER)}`
- `MATRICE_PAIRES: dict[str, tuple[str, str]] = ...`
- `SYNERGY_META: dict[str, tuple[str, str, int]] = ...`
- `TACTIQUES_SPEC: dict[int, TactiqueSpec] = ...`
- `CHASSIS_AXES_OPTIONS: tuple[tuple[str, tuple[Any, ...]], ...] = ...`
- `NUM_CHASSIS: int = 1`
- `TOPOLOGIES_DOTATION: dict[str, tuple[int, ...]] = ...`

### Fonctions publiques

- `decode_chassis_index(chassis_idx: int) -> dict[str, Any]` — Décode un index de châssis 0..191 (base mixte LSB-first) en dictionnaire d'axes.
- `encode_chassis_axes(axes: dict[str, Any]) -> int` — Encode un dictionnaire d'axes en index de châssis 0..191 (base mixte LSB-first).
- `is_tactique_code(code: int) -> bool`
- `is_reve_code(code: int) -> bool`
- `code_to_tile_id(code: int) -> str`
- `tile_id_to_code(tile_id: str) -> int`
- `machine_card_code(ray: int, m_type: int) -> int`
- `unpack_machine_card(card_code: int) -> tuple[int, int]`
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

Configuration immuable d'une partie (Mode 1..4 et 6 axes des 192 châssis v5.4.2).

**Champs :**
- `n_players: int`
- `mode: int`
- `peuples: tuple[str, ...]`
- `exp_seed: int`
- `rep_id: int`
- `coordonnateur_initial: int`
- `max_revision_passes: int`
- `profil_piste: str`
- `regle_ouverture_reve_multiple: str`
- `offset_seuil_parade: int`
- `placement_initial_machines: str`
- `role_abatteuse_fin_de_piste: str`
- `synergie_binome_machines: str`
- `reve_activation_mode: str`
- `gardien_bet_cap_policy: str`
- `reve_advance_mode: str`
- `gardien_4_trigger_mode: str`
- `tile_profiles: tuple[tuple[str, str], ...]`
- `p_max: int`
- `dotation_arbres: tuple[int, ...]`
- `lisiere_slots: tuple[str, ...]`
- `total_gardiens_partie: int`
- `total_reves_partie: int`
- `nb_animaux_sauvages: int`
- `nb_peuples_oniriques: int`

**Méthodes :**
- `from_chassis_index(cls, chassis_idx: int, *, n_players: int=4, mode: int=1, peuples: tuple[str, ...]=(), exp_seed: int=42, rep_id: int=0, coordonnateur_initial: int=0, max_revision_passes: int=4, reve_activation_mode: str='1_DEF_1_MACHINE', gardien_bet_cap_policy: str='UNIFORM_MAX_2', reve_advance_mode: str='CLEAR_RANK_ONLY', gardien_4_trigger_mode: str='DISTINCT_OPEN_1', tile_profiles: tuple[tuple[str, str], ...]=()) -> GameConfig` — Construit l'une des 192 configurations de châssis v5.5 à partir d'un index 0..191.
- `gardien_bet_cap_for_case(self, case_1_6: int) -> int` — Plafond de Défenseurs en pari 2.2 sur la case `1..6` (v5.5 : uniforme max 2).
- `seat_of_peuple(self, peuple_code: str) -> int | None` — Retourne le siège contrôlant ce Peuple, ou None s'il est absent de la table.
- `profile_for_slot(self, slot_id: str) -> str | None` — Retourne le profil actif d'un emplacement (Bug=B, Colonie=B par défaut en Mode 2+ v5.5).

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
- `apprentissage: int`
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
- `gardien_bet_cap_policy: str`
- `reve_advance_mode: str`
- `gardien_4_trigger_mode: str`
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

**Méthodes :**
- `gardien_bet_cap_for_case(self, case_1_6: int) -> int`
- `hand_of(self, seat: int) -> HandObs` — Accès direct O(1) à la main observée d'un siège (masquée si paravent fermé).
- `is_route(self, r: int, p: int) -> bool` — Retourne True si la parcelle (r, p) est une Route Forestière (0 Arbre, 0 Souche).
- `parcel_arbres(self, r: int, p: int) -> int` — Nombre d'Arbres debout sur (r, p) en O(1).
- `parcel_souches(self, r: int, p: int) -> int` — Nombre de Souches sur (r, p) en O(1).
- `parcel_insectes(self, r: int, p: int) -> int` — Nombre d'Insectes sur (r, p) en O(1).
- `parcel_piege(self, r: int, p: int) -> int` — État du Piège (0=aucun, 1=actif, 2=déclenché) sur (r, p) en O(1).
- `parcel_defenseurs(self, r: int, p: int) -> int` — Nombre de Défenseurs en forêt sur (r, p) en O(1).
- `parcel_has_nid(self, r: int, p: int) -> bool` — Retourne True si un Nid est présent sur (r, p) en Mode >= 2.
- `furtivite_defs_and_ins(self, lisiere: int, p: int) -> tuple[int, int]` — Retourne (nb_total_defenseurs, nb_insectes) sur la case Furtivité (lisiere, p) en O(1).
- `lisiere_tile_info(self, slot_idx: int) -> tuple[str, int, int]` — Retourne (tile_id, status, constructors) pour l'emplacement de lisière `slot_idx`.
- `machine_pos_status(self, r: int, m_type: int) -> tuple[int, int]` — Retourne (position, status) de la machine `(r, m_type)` en O(1).
- `machine_effective_rouges(self, r: int, m_type: int) -> int` — Retourne la puissance rouge totale (jetons rouges + 1 imprimé si en Ratissage).
- `is_sommeil_victory(self) -> bool` — Vrai si toutes les tuiles Rêves en jeu (2 * peuples oniriques > 0) sont en bloc à gauche.
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
- `reve_activation_defenders(self, case_1_6: int) -> int` — Nombre de Défenseurs actifs (non consommés) posés sur le Rêve en case `1..6`.
- `reve_activation_consumed(self, case_1_6: int) -> int` — Nombre de Défenseurs déjà consommés sur le Rêve en case `1..6` ce tour.
- `total_reve_activation_defenders(self) -> int` — Nombre total de Défenseurs actifs (non consommés) posés sur des Rêves.
- `total_reve_activation_engaged(self) -> int` — Nombre total de Défenseurs engagés en 2.2 sur des Rêves (actifs + consommés).
- `reve_activation_defenders_split(self, case_1_6: int) -> tuple[int, int]` — Retourne `(nb_reflexion, nb_definitif)` des Défenseurs actifs sur le Rêve en case `1..6`.
- `player_def2_reve_case(self, seat: int) -> int` — Retourne la case `1..6` ciblée en activation Rêve par le Défenseur de `seat`, ou 0.
- `tactique_code_bugs_app(self, rank_0_5: int) -> tuple[int, int, int]` — Retourne (code, bugs, apprentissage) au rang `0..5` de la piste Tactiques.

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
- `reshuffle_count: int`

**Méthodes :**
- `clone(self) -> GameState` — Copie rapide et strictement indépendante à l'octet près (compatible IS-MCTS / Forks).
- `raw_used_bytes(self) -> bytes` — Extrait immuable des octets alloués (pour assertions de tests et hachage déterministe).
- `light_trigger(self, case_num: int) -> None` — Allume le signal binaire d'une case 1..6 sur la Piste des Gardiens.
- `is_trigger_lit(self, case_num: int) -> bool`
- `clear_trigger(self, case_num: int) -> None`
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
- `next_non_razed_towards_heart(self, r: int, from_p: int) -> int | None` — Prochaine parcelle non rasée vers le cœur (p > from_p), ou None.
- `next_non_razed_towards_border(self, r: int, from_p: int) -> int | None` — Prochaine parcelle non rasée vers la bordure (p < from_p), ou None.
- `first_non_razed_from_border(self, r: int) -> int | None`
- `last_non_razed_parcel(self, r: int) -> int | None`
- `total_arbres_rayon(self, r: int) -> int`
- `total_arbres_plateau(self) -> int`
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
- `remove_player_defender(self, seat: int, def_idx: int) -> None` — Retire proprement le Défenseur (seat, def_idx) de sa position actuelle vers la main.
- `place_defender_foret(self, seat: int, def_idx: int, r: int, p: int, face: int) -> None`
- `enter_furtivite(self, seat: int, def_idx: int, lisiere: int, p: int, rive: int, face: int, preferred_twin: int=0) -> None` — Fait ENTRER un Défenseur en Furtivité (tire l'éventuel autre pion sur le jumeau).
- `flip_defender2_to_definitif_in_place(self, seat: int) -> None` — Retourne sur place le 2e Défenseur réflexion -> définitif (sans aucun tirage).
- `place_defender_lisiere_tile(self, seat: int, def_idx: int, lisiere_slot_idx: int, face: int) -> None`
- `count_gardien_pari_defenders_at_case(self, case_1_6: int) -> int` — Nombre de 2es Défenseurs actifs (non consommés) posés en pari sur la case `1..6`.
- `count_gardien_pari_consumed_at_case(self, case_1_6: int) -> int` — Nombre de 2es Défenseurs déjà consommés par ouverture sur la case `1..6` ce tour.
- `total_gardien_pari_remaining(self) -> int` — Nombre total de 2es Défenseurs encore actifs (non consommés) sur la Piste des Gardiens.
- `total_gardien_pari_consumed(self) -> int` — Nombre total de Défenseurs déjà consommés par ouverture de Gardiens ce tour.
- `total_gardien_pari_engaged(self) -> int` — Nombre total de Défenseurs engagés en 2.2 sur la Piste des Gardiens (actifs + consommés).
- `place_defender_gardien_pari(self, seat: int, case_1_6: int, face: int) -> None` — Engage le Défenseur de `seat` en pari d'activation sur le Gardien en case `1..6` (plafond v5.4.5).
- `consume_one_gardien_pari_defender(self, case_1_6: int) -> bool` — Retire 1 Défenseur actif sur la case `1..6` (mis de côté jusqu'en 6.2).
- `count_reve_activation_defenders_at_case(self, case_1_6: int) -> int` — Nombre de Défenseurs actifs (non consommés) posés sur le Rêve en case `1..6`.
- `count_reve_activation_consumed_at_case(self, case_1_6: int) -> int` — Nombre de Défenseurs déjà consommés sur le Rêve en case `1..6` ce tour.
- `total_reve_activation_remaining(self) -> int` — Nombre total de Défenseurs encore actifs (non consommés) sur des Rêves.
- `total_reve_activation_consumed(self) -> int` — Nombre total de Défenseurs consommés par annulation de machines sur des Rêves ce tour.
- `total_reve_activation_engaged(self) -> int` — Nombre total de Défenseurs engagés en 2.2 sur des Rêves (actifs + consommés).
- `consume_reve_activation_defenders(self, case_1_6: int, count: int) -> int` — Consomme jusqu'à `count` Défenseurs actifs sur le Rêve en case `1..6` (pari gagné).
- `is_eveil_attempt_eligible(self) -> bool` — Vrai si les N Défenseurs de la table ont tous été engagés en 2.2 sur la Piste des Gardiens (Éveil de la Forêt 100 % Gardiens, Tours 1..7, A >= 1).
- `is_eveil_gardiens_victory(self) -> bool` — Éveil de la Forêt 100 % Piste des Gardiens (Tours 1..7, A >= 1) : les N Défenseurs de la table engagés en 2.2 sur la Piste des Gardiens et 0 pari perdu (0 restant en 5.3).
- `place_defender_reve_activation(self, seat: int, case_1_6: int, face: int) -> None` — Engage le Défenseur de `seat` sur un Rêve en case `1..6` pour l'activation en 3.2.
- `mark_defender_impasse(self, seat: int, def_idx: int, face: int) -> None` — Consomme le Défenseur sans pose physique lorsque 100 % des cibles légales sont épuisées.
- `get_lisiere_tile_state(self, slot_idx: int) -> tuple[int, int]` — Retourne (status, nb_constructors).
- `set_lisiere_tile_state(self, slot_idx: int, status: int, constructors: int) -> None`
- `find_lisiere_slot_by_tile_id(self, tile_id: str) -> int | None`
- `get_gardien_at_case(self, case_1_6: int) -> tuple[int, int]` — Retourne (g_num 0..15, face 1..2) sur la case 1..6.
- `set_gardien_at_case(self, case_1_6: int, g_num: int, face: int=1) -> None`
- `get_tactique_at_rank(self, rank_0_5: int) -> int`
- `set_tactique_at_rank(self, rank_0_5: int, code: int) -> None`
- `find_tactique_rank(self, code: int) -> int | None`
- `get_apprentissage_at_rank(self, rank_0_5: int) -> int`
- `set_apprentissage_at_rank(self, rank_0_5: int, val: int) -> None`
- `get_bugs_at_case(self, case_1_6: int) -> int`
- `set_bugs_at_case(self, case_1_6: int, count: int) -> None`
- `get_colonie_at_case(self, case_1_6: int) -> int`
- `set_colonie_at_case(self, case_1_6: int, count: int) -> None`
- `get_machine_pos_status(self, ray: int, m_type: int) -> tuple[int, int, bool]` — Retourne (pos 0..P_Max, status, pending_ratissage).
- `set_machine_pos_status(self, ray: int, m_type: int, pos: int, status: int, pending_ratissage: bool=False) -> None`
- `get_machine_tokens(self, ray: int, m_type: int) -> tuple[int, int]` — Retourne (rouges physiques, bleus).
- `get_machine_effective_rouges(self, ray: int, m_type: int) -> int` — Retourne la puissance rouge totale (jetons rouges + 1 imprimé si face Ratissage).
- `set_machine_tokens(self, ray: int, m_type: int, rouges: int, bleus: int) -> None`
- `machines_on_parcel(self, ray: int, p: int) -> list[int]` — Retourne la liste des types de machines physiquement présentes sur (ray, p).
- `is_sommeil_victory(self) -> bool` — Vrai si toutes les tuiles Rêves en jeu (2 * peuples oniriques > 0) sont en bloc à gauche.
- `add_permanent_sabotage(self, count: int=1, *, light_case_3: bool=True) -> None` — Ajoute définitivement +count cartes Sabotage (mises de côté pour le remélange 6.3).
- `rebuild_and_shuffle_machine_deck(self, *, increment_reshuffle: bool) -> None` — Reconstitue le paquet Machine hors Sièges/retirées + Sabotages et le mélange.
- `remove_machine_card_from_deck_if_present(self, card_code: int) -> None` — Retire une carte Machine du paquet restant si elle passe en Siège en 1.1.
- `draw_next_machine_card(self) -> int` — Pioche la prochaine carte du paquet Machine (ou CARD_NONE si paquet épuisé).
- `get_player_hand(self, seat: int) -> tuple[int, int, int, int, int]` — Retourne (card_code, d1, d2, lecture_m, bound_tactique) pour seat.
- `set_player_hand(self, seat: int, card: int, d1: int=0, d2: int=0, lecture_m: int=0, bound_tactique: int=0) -> None`
- `get_machine_turn_stats(self, ray: int, m_type: int) -> tuple[int, bool, bool]` — Retourne (damaged_parcels_count 0..3, gained_red, attacked_this_turn).
- `set_machine_turn_stats(self, ray: int, m_type: int, damaged_count: int, gained_red: bool, attacked: bool) -> None`
- `has_reve_opened_this_turn(self, r_num: int) -> bool`
- `mark_reve_opened_this_turn(self, r_num: int) -> None`
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
- `has_gardien_won_this_turn(self, case_1_6: int) -> bool` — Vrai si le Gardien de la case `1..6` a déjà achevé son pari ce tour (0 Défenseur restant).
- `mark_gardien_won_this_turn(self, case_1_6: int) -> None` — Marque la case Gardien `1..6` comme ayant achevé son pari ce tour.
- `count_other_gardiens_won_this_turn(self) -> int` — Nombre de Gardiens distincts hors case 4 ayant achevé leur pari ce tour.
- `was_seat_deviated_by_bug_this_turn(self, seat: int) -> bool` — Vrai si la carte Machine du siège `seat` a déjà été déviée par un Bug en 3.2 ce tour.
- `mark_seat_deviated_by_bug_this_turn(self, seat: int) -> None` — Marque le siège `seat` comme ayant consommé son déclencheur 3.2 sur 6. Insecte (Bug).
- `get_pending_apprentissage_at_rank(self, rank_0_5: int) -> int` — Obsolète (Apprentissage 6.1 supprimé en v5.4.2) — retourne toujours 0.
- `add_pending_apprentissage_at_rank(self, rank_0_5: int, delta: int) -> None` — Obsolète (Apprentissage 6.1 supprimé en v5.4.2) — sans effet.
- `get_pending_voluntary_app_reduction(self) -> tuple[int, int]` — Retourne (nb_retraits_volontaires_restants, seat_decideur) mémorisés pour 6.1.
- `add_pending_voluntary_app_reduction(self, count: int, decideur_seat: int) -> None` — Mémorise +count retraits volontaires d'Apprentissage en 6.1 avant Bug (ex: G10 A, R2 A).
- `clear_pending_voluntary_app_reduction(self, remaining: int=0, seat: int=0) -> None` — Met à jour le compteur résiduel de retraits volontaires d'Apprentissage en 6.1.
- `reset_transient_modifiers(self) -> None` — Remet intégralement à zéro la plage dédiée de modificateurs transitoires en 6.2.
- `cleanup_end_of_turn_6_2(self) -> None` — Ménage rapide de fin de tour 6.2 par tranches mémoire contiguës.
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

## Bus des 8 Primitives & Hooks (`engine.primitives`)

*Source : `engine/primitives.py`*

> Bus des 8 Primitives Formelles, structures de décision/fin et registre de hooks.

### Constantes publiques

- `CAUSE_TOUR_8: str = 'TOUR_8_ATTEINT'`
- `CAUSE_REVE_RANG_1: str = 'REVE_RANG_1'`
- `CAUSE_REVEIL_GARDIENS: str = 'REVEIL_GARDIENS'`
- `DEC_EFFET_TUILE: str = 'EFFET_TUILE'`
- `PRIM_MOD_SEUIL: str = 'MOD_SEUIL'`
- `PRIM_CREATION_ENTITE: str = 'CREATION_ENTITE'`
- `PRIM_DEPLACEMENT: str = 'DEPLACEMENT'`
- `PRIM_MOD_PUISSANCE: str = 'MOD_PUISSANCE'`
- `PRIM_MOD_APPRENTISSAGE: str = 'MOD_APPRENTISSAGE'`
- `PRIM_PERMUTATION_PISTE: str = 'PERMUTATION_PISTE'`
- `PRIM_PARTAGE_INFO_ETAT_GARDIEN: str = 'PARTAGE_INFO_ETAT_GARDIEN'`
- `PRIM_MOD_LOI_DU_COEUR: str = 'MOD_LOI_DU_COEUR'`
- `ALL_PRIMITIVES: tuple[str, ...] = ...`
- `HOOK_1_3_LECTURE_DE: str = 'HOOK_1_3_LECTURE_DE'`
- `HOOK_2_1_DEBUT: str = 'HOOK_2_1_DEBUT'`
- `HOOK_2_1_PORTEE_DEF1: str = 'HOOK_2_1_PORTEE_DEF1'`
- `HOOK_3_1_CONSTRUCTION: str = 'HOOK_3_1_CONSTRUCTION'`
- `HOOK_3_2_REVELATION: str = 'HOOK_3_2_REVELATION'`
- `HOOK_3_2_OUVERTURE_REVE: str = 'HOOK_3_2_OUVERTURE_REVE'`
- `HOOK_3_2_APRES_REVELATION: str = 'HOOK_3_2_APRES_REVELATION'`
- `HOOK_GARDIEN_OUVERTURE: str = 'HOOK_GARDIEN_OUVERTURE'`
- `HOOK_4_1_FURTIVITE: str = 'HOOK_4_1_FURTIVITE'`
- `HOOK_4_2_NID_APRES_PROD: str = 'HOOK_4_2_NID_APRES_PROD'`
- `HOOK_4_3_COLONIE_FIN: str = 'HOOK_4_3_COLONIE_FIN'`
- `HOOK_4_3_MIGRATION_DESTS: str = 'HOOK_4_3_MIGRATION_DESTS'`
- `HOOK_5_DEBUT: str = 'HOOK_5_DEBUT'`
- `HOOK_5_ORDRE_RAYON: str = 'HOOK_5_ORDRE_RAYON'`
- `HOOK_5_CIBLAGE_MACHINE: str = 'HOOK_5_CIBLAGE_MACHINE'`
- `HOOK_5_LAW_QUERY: str = 'HOOK_5_LAW_QUERY'`
- `HOOK_5_PARADE_JAGUAR: str = 'HOOK_5_PARADE_JAGUAR'`
- `HOOK_5_PARADE_HARPIE: str = 'HOOK_5_PARADE_HARPIE'`
- `HOOK_5_SEUIL_PARADE: str = 'HOOK_5_SEUIL_PARADE'`
- `HOOK_5_DEFENSE_PARCELLE: str = 'HOOK_5_DEFENSE_PARCELLE'`
- `HOOK_5_APRES_PARADE_PIEGE: str = 'HOOK_5_APRES_PARADE_PIEGE'`
- `HOOK_5_PARADE_CLASSIQUE: str = 'HOOK_5_PARADE_CLASSIQUE'`
- `HOOK_5_TERRASSEMENT: str = 'HOOK_5_TERRASSEMENT'`
- `HOOK_5_CONTACT_NID: str = 'HOOK_5_CONTACT_NID'`
- `HOOK_5_FIN_ATTAQUE_MACHINE: str = 'HOOK_5_FIN_ATTAQUE_MACHINE'`
- `HOOK_5_3_PRE_RETRAIT: str = 'HOOK_5_3_PRE_RETRAIT'`
- `HOOK_6_1_REDUCTION_VOLONTAIRE: str = 'HOOK_6_1_REDUCTION_VOLONTAIRE'`
- `HOOK_6_1_BUG: str = 'HOOK_6_1_BUG'`
- `HOOK_6_2_AVANCEMENT: str = 'HOOK_6_2_AVANCEMENT'`
- `HOOK_REPOUSSE_FINALE: str = 'HOOK_REPOUSSE_FINALE'`
- `HOOK_EFFECT_RESUME: str = 'HOOK_EFFECT_RESUME'`
- `EffectHandler = Callable[[GameState, str, dict[str, Any]], Any]`

### Fonctions publiques

- `register_tile(slot_id: str, profile: str, hooks: Sequence[str]=()) -> Callable[[EffectHandler], EffectHandler]` — Décorateur d'enregistrement d'un profil stateless (slot_id, profile).
- `get_tile_registration(slot_id: str, profile: str) -> TileRegistration | None`
- `list_registered_tiles() -> tuple[tuple[str, str], ...]`
- `clear_tile_registry() -> None`
- `has_pending_decision(state: GameState) -> bool` — Retourne True si une DecisionRequest est déjà en tête de la pile de continuation.
- `push_effect_decision(state: GameState, decideur: int, options: Sequence[Any], context: dict[str, Any], *, slot_id: str, profile: str, resume_tag: str='RESUME', resume_payload: tuple[Any, ...]=(), decision_type: str=DEC_EFFET_TUILE) -> DecisionRequest` — Suspend proprement un effet de tuile sur une DecisionRequest gouvernée par `decideur`.
- `dispatch_hook(state: GameState, hook_name: str, ctx: dict[str, Any] | None=None) -> list[Any]` — Exécute le bus de hooks pour les tuiles en jeu ayant un profil actif. En Mode 1 : retourne immédiatement []. En Mode 2 : neutralise les textes de G/R/M (profile_for_slot -> None) tout en laissant passer les hooks structurels et Migration A/A. Si un handler suspend via push_effect_decision, met en file les handlers restants.
- `prim_mod_seuil(state: GameState, delta: int, *, ray: int | None=None, p: int | None=None, m_type: int | None=None) -> None` — Primitive 1 : MOD_SEUIL — modifie le Seuil de Parade (parcelle, rayon, machine ou global).
- `prim_creation_entite(state: GameState, entity_type: str, *, ray: int=0, p: int=1, lisiere: int | None=None, count: int=1, light_trigger: bool=True) -> None` — Primitive 2 : CREATION_ENTITE — crée Insecte, Piège, Sabotage ou Arbre (Repousse).
- `apply_machine_nid_contact(state: GameState, ray: int, p: int) -> bool` — Règle A16 : tout mouvement entrant d'une machine sur un Nid non protégé le renvoie en lisière (reconstructible) et défausse tous les Insectes locaux.
- `prim_deplacement(state: GameState, entity_type: str, *, src_ray: int=0, src_p: int=1, dst_ray: int=0, dst_p: int=1, src_lisiere: int | None=None, dst_lisiere: int | None=None, src_lisiere_slot: int | None=None, m_type: int=0, global_track: str | None=None, global_case: int=1, count: int=1) -> bool` — Primitive 3 : DEPLACEMENT — déplace Insecte, Machine ou Défenseur.
- `prim_mod_puissance(state: GameState, ray: int, m_type: int, *, delta_rouges: int=0, delta_bleus: int=0, flip_rouge_to_bleu: int=0) -> None` — Primitive 4 : MOD_PUISSANCE — ajuste les jetons Puissance rouges et bleus Surchauffe.
- `prim_mod_apprentissage(state: GameState, rank_0_5: int, delta: int) -> None` — Primitive 5 : MOD_APPRENTISSAGE — neutralisée (Apprentissage supprimé en v5.4.2).
- `prim_permutation_piste(state: GameState, action: str, *, rank_a: int=0, rank_b: int=0, seat: int=0, delta_m: int=0, rebind_tactique: bool=False) -> bool` — Primitive 6 : PERMUTATION_PISTE — avancée Rêve (saut/poussée) ou lecture M sur piste fixe T1..T6.
- `prim_partage_info_etat_gardien(state: GameState, action: str, *, case_1_6: int=1, new_face: int=2) -> bool` — Primitive 7 : PARTAGE_INFO_ETAT_GARDIEN — états Gardiens & ouverture paravents.
- `prim_mod_loi_du_coeur(state: GameState, law_id: str, *, active: bool=True) -> bool` — Primitive 8 : MOD_LOI_DU_COEUR — point d'entrée typé des Lois passives/temporaires.

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
