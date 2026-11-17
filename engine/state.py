"""État de jeu déterministe scellé sur bytearray(384) et vue isolée PlayerObservation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, NamedTuple

from engine.rng import SRC_MACHINE_SHUFFLE, SRC_TACTICS_SETUP, shuffle_deterministic

__all__ = (
    "BUF_CAPACITY",
    "CARD_NONE",
    "CARD_SABOTAGE",
    "CHASSIS_AXES_OPTIONS",
    "DECK_SLOTS_CAPACITY",
    "FACE_DEFINITIF",
    "FACE_REFLEXION",
    "FAMILLE_CROISSANCE",
    "FAMILLE_GARDIEN",
    "FAMILLE_REVE",
    "LISIERE_ABSENT",
    "LISIERE_CONSTRUCTED",
    "LISIERE_EJECTED",
    "LISIERE_UNCONSTRUCTED",
    "MACHINE_ABATTEUSE",
    "MACHINE_BULLDOZER",
    "MACHINE_STATUS_NORMAL",
    "MACHINE_STATUS_RETIRED",
    "MACHINE_STATUS_SIEGE",
    "MATRICE_PAIRES",
    "MAX_N",
    "MAX_P",
    "MIN_FREE_RESERVE_BYTES",
    "PEUPLES_ORDER",
    "PEUPLE_TO_ID",
    "PFLAG_AUTO_PARADE_ONCE",
    "PFLAG_MATAMATA_MARK",
    "PFLAG_SANCTUAIRE_SOUCHE",
    "PIEGE_ACTIF",
    "PIEGE_AUCUN",
    "PIEGE_DECLENCHE",
    "STATE_BUF_SIZE",
    "STEP_1_1_SIEGE",
    "STEP_1_2_DEAL",
    "STEP_1_3_DICE",
    "STEP_2_1_DEF1",
    "STEP_2_2_DEF2",
    "STEP_3_1_CONSTRUCT",
    "STEP_3_2_REVEAL",
    "STEP_4_1_FURTIVITE",
    "STEP_4_2_NIDS",
    "STEP_4_3_MIGRATION",
    "STEP_5_1_TACTIQUES",
    "STEP_5_2_SIEGES",
    "STEP_5_3_END_CHECK",
    "STEP_6_1_APPRENTISSAGE",
    "STEP_6_2_EVOLUTION",
    "STEP_6_3_END_TURN",
    "STEP_GAME_OVER",
    "SYNERGY_META",
    "TACTIQUES_SPEC",
    "TILE_R_BASE",
    "TRACK_LEN",
    "FurtiviteCellObs",
    "GameConfig",
    "GameState",
    "GardienSlotObs",
    "HandObs",
    "LisiereTileObs",
    "MachineObs",
    "ParcelObs",
    "PlayerObservation",
    "TactiqueSlotObs",
    "code_to_tile_id",
    "get_layout_report",
    "is_reve_code",
    "is_tactique_code",
    "machine_card_code",
    "slot_id_to_once_index",
    "tile_id_to_code",
    "unpack_machine_card",
)

STATE_BUF_SIZE: int = 384  # 6 cache lines de 64 octets
BUF_CAPACITY: int = STATE_BUF_SIZE
MIN_FREE_RESERVE_BYTES: int = 32
MAX_N: int = 6
MAX_P: int = 5
NUM_PARCELS: int = MAX_N * MAX_P  # 30
NUM_SYNERGY_SLOTS: int = 2 * MAX_N  # 12
NUM_MACHINES: int = 2 * MAX_N  # 12
NUM_NIDS: int = 5  # M1..M5
TRACK_LEN: int = 6
DECK_SLOTS_CAPACITY: int = 64  # 32 octets * 2 nibbles (supporte N=6 + forte dilution Sabotage)

# Bitmasks transitoires par parcelle (TRANS_PARCEL_FLAGS, RAZ en 6.2)
PFLAG_SANCTUAIRE_SOUCHE: int = 1 << 0  # ex: M5 A (laisse 1 Souche au terrassement Bulldozer)
PFLAG_MATAMATA_MARK: int = 1 << 1  # ex: G5 A (-1 Seuil si >= 1 Souche à la frappe)
PFLAG_AUTO_PARADE_ONCE: int = 1 << 2  # ex: G11 A Face 2 (pare auto 1 frappe si >= 2 Défenseurs)

# Types de machines par rayon
MACHINE_ABATTEUSE: int = 0
MACHINE_BULLDOZER: int = 1

# Statuts machine
MACHINE_STATUS_NORMAL: int = 0
MACHINE_STATUS_SIEGE: int = 1
MACHINE_STATUS_RETIRED: int = 2

# États des pièges sur parcelle Forêt
PIEGE_AUCUN: int = 0
PIEGE_ACTIF: int = 1
PIEGE_DECLENCHE: int = 2

# Faces des Défenseurs (notamment sur les 4 emplacements jumeaux de Furtivité)
FACE_VIDE: int = 0
FACE_REFLEXION: int = 1
FACE_DEFINITIF: int = 2

# États des tuiles de Synergie en lisière
LISIERE_ABSENT: int = 0
LISIERE_UNCONSTRUCTED: int = 1
LISIERE_CONSTRUCTED: int = 2
LISIERE_EJECTED: int = 3

# Familles de tuiles de Synergie
FAMILLE_GARDIEN: str = "GARDIEN"
FAMILLE_REVE: str = "REVE"
FAMILLE_CROISSANCE: str = "CROISSANCE"

# Codes cartes du paquet Machine (4 bits : 0..13)
CARD_NONE: int = 0
# 1..12 = machine (ray * 2 + m_type + 1)
CARD_SABOTAGE: int = 13

# Codes tuiles sur la Piste des Tactiques / Rêves
# 1..6 = T1..T6 ; 101..110 = R1..R10
TILE_R_BASE: int = 100

# Étapes et sous-étapes de la machine à états
STEP_1_1_SIEGE: int = 11
STEP_1_2_DEAL: int = 12
STEP_1_3_DICE: int = 13
STEP_2_1_DEF1: int = 21
STEP_2_2_DEF2: int = 22
STEP_3_1_CONSTRUCT: int = 31
STEP_3_2_REVEAL: int = 32
STEP_4_1_FURTIVITE: int = 41
STEP_4_2_NIDS: int = 42
STEP_4_3_MIGRATION: int = 43
STEP_5_1_TACTIQUES: int = 51
STEP_5_2_SIEGES: int = 52
STEP_5_3_END_CHECK: int = 53
STEP_6_1_APPRENTISSAGE: int = 61
STEP_6_2_EVOLUTION: int = 62
STEP_6_3_END_TURN: int = 63
STEP_GAME_OVER: int = 99

# Bits de FLAGS (octet d'état global)
_FLAG_PARAVENTS_OUVERTS: int = 1 << 0
_FLAG_STEP2_LOCKED: int = 1 << 1

# Peuples canoniques (0..5)
PEUPLES_ORDER: tuple[str, ...] = ("M", "R", "O", "H", "E", "I")
PEUPLE_TO_ID: dict[str, int] = {code: idx for idx, code in enumerate(PEUPLES_ORDER)}

# Matrice canonique des paires adjacentes (v5.3.1)
MATRICE_PAIRES: dict[str, tuple[str, str]] = {
    "M_R": ("G1", "G2"),
    "R_M": ("G2", "G1"),
    "M_O": ("G3", "G4"),
    "O_M": ("G4", "G3"),
    "R_O": ("G5", "G6"),
    "O_R": ("G6", "G5"),
    "M_H": ("G7", "R3"),
    "H_M": ("R3", "G7"),
    "M_E": ("G8", "R7"),
    "E_M": ("R7", "G8"),
    "R_H": ("G9", "R4"),
    "H_R": ("R4", "G9"),
    "R_E": ("G10", "R8"),
    "E_R": ("R8", "G10"),
    "O_H": ("G11", "R5"),
    "H_O": ("R5", "G11"),
    "O_E": ("G12", "R9"),
    "E_O": ("R9", "G12"),
    "M_I": ("G13", "M1"),
    "I_M": ("M1", "G13"),
    "R_I": ("G14", "M2"),
    "I_R": ("M2", "G14"),
    "O_I": ("G15", "M3"),
    "I_O": ("M3", "G15"),
    "H_E": ("R1", "R2"),
    "E_H": ("R2", "R1"),
    "H_I": ("R6", "M4"),
    "I_H": ("M4", "R6"),
    "E_I": ("R10", "M5"),
    "I_E": ("M5", "R10"),
}

# Métadonnées structurelles des 30 emplacements de Synergie : (famille, peuple_origine, num_interne)
SYNERGY_META: dict[str, tuple[str, str, int]] = {
    "G1": (FAMILLE_GARDIEN, "M", 1),
    "G2": (FAMILLE_GARDIEN, "R", 2),
    "G3": (FAMILLE_GARDIEN, "M", 3),
    "G4": (FAMILLE_GARDIEN, "O", 4),
    "G5": (FAMILLE_GARDIEN, "R", 5),
    "G6": (FAMILLE_GARDIEN, "O", 6),
    "G7": (FAMILLE_GARDIEN, "M", 7),
    "G8": (FAMILLE_GARDIEN, "M", 8),
    "G9": (FAMILLE_GARDIEN, "R", 9),
    "G10": (FAMILLE_GARDIEN, "R", 10),
    "G11": (FAMILLE_GARDIEN, "O", 11),
    "G12": (FAMILLE_GARDIEN, "O", 12),
    "G13": (FAMILLE_GARDIEN, "M", 13),
    "G14": (FAMILLE_GARDIEN, "R", 14),
    "G15": (FAMILLE_GARDIEN, "O", 15),
    "R1": (FAMILLE_REVE, "H", 1),
    "R2": (FAMILLE_REVE, "E", 2),
    "R3": (FAMILLE_REVE, "H", 3),
    "R4": (FAMILLE_REVE, "H", 4),
    "R5": (FAMILLE_REVE, "H", 5),
    "R6": (FAMILLE_REVE, "H", 6),
    "R7": (FAMILLE_REVE, "E", 7),
    "R8": (FAMILLE_REVE, "E", 8),
    "R9": (FAMILLE_REVE, "E", 9),
    "R10": (FAMILLE_REVE, "E", 10),
    "M1": (FAMILLE_CROISSANCE, "I", 1),
    "M2": (FAMILLE_CROISSANCE, "I", 2),
    "M3": (FAMILLE_CROISSANCE, "I", 3),
    "M4": (FAMILLE_CROISSANCE, "I", 4),
    "M5": (FAMILLE_CROISSANCE, "I", 5),
}


@dataclass(frozen=True, slots=True)
class TactiqueSpec:
    """Profil structurel immuable d'une tuile Tactique T1..T6."""

    code: int
    tile_id: str
    cibles: tuple[str, ...]
    avancee: int
    gain_rouge: int
    mod_seuil: int
    est_siege_profil: bool


TACTIQUES_SPEC: dict[int, TactiqueSpec] = {
    1: TactiqueSpec(1, "T1", ("SUR_PLACE",), 0, 0, 0, False),
    2: TactiqueSpec(2, "T2", ("DEVANT",), 0, 0, 0, False),
    3: TactiqueSpec(3, "T3", ("SUR_PLACE", "DEVANT"), 1, 0, -1, False),
    4: TactiqueSpec(4, "T4", ("SUR_PLACE",), 0, 1, -1, True),
    5: TactiqueSpec(5, "T5", ("DEVANT",), 0, 1, -1, False),
    6: TactiqueSpec(6, "T6", ("SUR_PLACE", "DEVANT"), 1, 1, -2, False),
}

# Les 7 axes binaires des 128 châssis (spec_bundle_v5_3_1.json)
CHASSIS_AXES_OPTIONS: tuple[tuple[str, tuple[Any, Any]], ...] = (
    ("p_max", (4, 5)),
    ("regle_ouverture_reve_multiple", ("UNIQUE_PAR_TOUR", "PAR_DE_M_DESIGNE")),
    ("offset_seuil_parade", (0, 1)),
    ("mise_en_place_tactiques", ("ORDRE_FIXE_T1_T6", "ALEATOIRE")),
    ("declenchement_fin_de_piste", ("ARRIVEE_DERNIERE_PARCELLE", "DEPASSEMENT_DERNIERE_PARCELLE")),
    ("role_abatteuse_fin_de_piste", ("STANDARD_COUPE_ARBRE", "ARRACHE_1_SOUCHE_SI_SANS_ARBRE")),
    ("synergie_binome_machines", ("INDIVIDUELLE", "MUTUALISATION_PUISSANCE_MEME_PARCELLE")),
)

TOPOLOGIES_DOTATION: dict[int, tuple[int, ...]] = {
    4: (2, 2, 3, 3),
    5: (2, 2, 2, 3, 3),
}


_GARDIEN_STR_TABLE: tuple[str | None, ...] = (None, *[f"G{i}" for i in range(1, 16)])
_TACTIQUE_STR_TABLE: dict[int, str] = {
    **{i: f"T{i}" for i in range(1, 7)},
    **{TILE_R_BASE + i: f"R{i}" for i in range(1, 11)},
}


def is_tactique_code(code: int) -> bool:
    return 1 <= code <= 6


def is_reve_code(code: int) -> bool:
    return TILE_R_BASE + 1 <= code <= TILE_R_BASE + 10


def code_to_tile_id(code: int) -> str:
    found = _TACTIQUE_STR_TABLE.get(code)
    if found is not None:
        return found
    raise ValueError(f"Code piste inconnu : {code}")


def tile_id_to_code(tile_id: str) -> int:
    if tile_id.startswith("T") and len(tile_id) == 2:
        val = int(tile_id[1])
        assert 1 <= val <= 6
        return val
    if tile_id.startswith("R"):
        val = int(tile_id[1:])
        assert 1 <= val <= 10
        return TILE_R_BASE + val
    raise ValueError(f"Identifiant piste invalide : {tile_id}")


def machine_card_code(ray: int, m_type: int) -> int:
    assert 0 <= ray < MAX_N
    assert m_type in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
    return ray * 2 + m_type + 1


def unpack_machine_card(card_code: int) -> tuple[int, int]:
    assert 1 <= card_code <= NUM_MACHINES
    idx = card_code - 1
    return idx // 2, idx % 2


def slot_id_to_once_index(slot_id: str) -> int:
    """Convertit un identifiant d'emplacement (G1..G15, R1..R10, M1..M5, Migration) en index 0..63."""
    if slot_id == "SLOT_BUG_CERVEAU":
        return 30
    if slot_id == "SLOT_COLONISATION_GARDIENS":
        return 31
    meta = SYNERGY_META.get(slot_id)
    if meta is None:
        raise ValueError(f"Emplacement inconnu pour verrou once-per-turn : {slot_id}")
    fam, _, num = meta
    if fam == FAMILLE_GARDIEN:
        return num - 1  # 0..14
    if fam == FAMILLE_REVE:
        return 15 + (num - 1)  # 15..24
    return 25 + (num - 1)  # 25..29


class _Layout:
    """Allocateur séquentiel sans magic numbers sur bytearray(384)."""

    _cursor: ClassVar[int] = 0
    _blocks: ClassVar[list[tuple[str, int, int]]] = []

    @classmethod
    def alloc(cls, size: int, name: str = "") -> int:
        assert size > 0
        offset = cls._cursor
        cls._cursor += size
        cls._blocks.append((name, offset, size))
        return offset


class _Mem:
    """Table complète des offsets alloués séquentiellement via _Layout.alloc()."""

    # 1. En-tête global (6 octets)
    TOUR: int = _Layout.alloc(1, "TOUR")
    STEP: int = _Layout.alloc(1, "STEP")
    COORDONNATEUR: int = _Layout.alloc(1, "COORDONNATEUR")
    FLAGS: int = _Layout.alloc(1, "FLAGS")
    SEUIL_REVEIL: int = _Layout.alloc(1, "SEUIL_REVEIL")
    TRIGGERS_LIT: int = _Layout.alloc(1, "TRIGGERS_LIT")

    # 2. Parcelles Forêt : MAX_N=6 * MAX_P=5 = 30 parcelles (88 octets)
    FORET_ARBRES_SOUCHES: int = _Layout.alloc(NUM_PARCELS, "FORET_ARBRES_SOUCHES")
    FORET_INSECTES: int = _Layout.alloc(NUM_PARCELS, "FORET_INSECTES")
    FORET_PIEGES: int = _Layout.alloc((NUM_PARCELS + 3) // 4, "FORET_PIEGES")  # 8 octets (2 bits/parcelle)
    FORET_DEFENSEURS: int = _Layout.alloc((NUM_PARCELS + 1) // 2, "FORET_DEFENSEURS")  # 15 octets (4 bits/parcelle)
    NIDS_STATE: int = _Layout.alloc(NUM_NIDS, "NIDS_STATE")  # 5 octets M1..M5 (parcelle + bit activé)

    # 3. Furtivité : 6 lisières * 5 prof = 30 cases à 4 emplacements jumeaux (45 octets)
    FURTIVITE_SLOTS: int = _Layout.alloc(NUM_PARCELS, "FURTIVITE_SLOTS")  # 4 slots * 2 bits/case
    FURTIVITE_INSECTES: int = _Layout.alloc((NUM_PARCELS + 1) // 2, "FURTIVITE_INSECTES")  # 15 octets

    # 4. Suivi des pions Défenseurs des joueurs : 6 sièges * 2 pions (13 octets)
    PLAYER_DEF_LOC: int = _Layout.alloc(MAX_N * 2, "PLAYER_DEF_LOC")
    PLAYER_DEF2_DEF_MASK: int = _Layout.alloc(1, "PLAYER_DEF2_DEF_MASK")

    # 5. Tuiles de Synergie en lisière : 2N = 12 emplacements (6 octets, 4 bits/tuile)
    LISIERE_TILES: int = _Layout.alloc(NUM_SYNERGY_SLOTS // 2, "LISIERE_TILES")

    # 6. Pistes globales 1..6 (30 octets)
    GARDIENS_PISTE: int = _Layout.alloc(TRACK_LEN, "GARDIENS_PISTE")
    TACTIQUES_PISTE_ID: int = _Layout.alloc(TRACK_LEN, "TACTIQUES_PISTE_ID")
    TACTIQUES_APPRENTISSAGE: int = _Layout.alloc(TRACK_LEN, "TACTIQUES_APPRENTISSAGE")
    PISTE_BUGS: int = _Layout.alloc(TRACK_LEN, "PISTE_BUGS")
    PISTE_COLONIE: int = _Layout.alloc(TRACK_LEN, "PISTE_COLONIE")

    # 7. Machines : 6 rayons * 2 types = 12 machines (24 octets)
    MACHINE_POS_STATUS: int = _Layout.alloc(NUM_MACHINES, "MACHINE_POS_STATUS")
    MACHINE_ROUGES_BLEUS: int = _Layout.alloc(NUM_MACHINES, "MACHINE_ROUGES_BLEUS")

    # 8. Paquet Machine (64 slots), dilution Sabotage & mains secrètes sous paravent (49 octets)
    DECK_LEN: int = _Layout.alloc(1, "DECK_LEN")
    DECK_CURSOR: int = _Layout.alloc(1, "DECK_CURSOR")
    SABOTAGE_DECK_COUNT: int = _Layout.alloc(1, "SABOTAGE_DECK_COUNT")
    SABOTAGE_PENDING_COUNT: int = _Layout.alloc(1, "SABOTAGE_PENDING_COUNT")
    RESHUFFLE_COUNT: int = _Layout.alloc(1, "RESHUFFLE_COUNT")
    DECK_CARDS: int = _Layout.alloc(DECK_SLOTS_CAPACITY // 2, "DECK_CARDS")  # 32 octets (64 cartes)
    PLAYER_HANDS: int = _Layout.alloc(MAX_N * 2, "PLAYER_HANDS")  # 12 octets (2 octets/joueur)

    # 9. Plage dédiée de modificateurs transitoires de tour, RAZ systématique en 6.2 (91 octets)
    TRANSIENT_START: int = _Layout._cursor
    TRANS_MACHINE_STATS: int = _Layout.alloc(NUM_MACHINES // 2, "TRANS_MACHINE_STATS")  # 6 octets
    TRANS_MACHINE_SEUIL_MOD: int = _Layout.alloc(NUM_MACHINES // 2, "TRANS_MACHINE_SEUIL_MOD")  # 6 octets
    TRANS_REVE_OPENED_MASK: int = _Layout.alloc(2, "TRANS_REVE_OPENED_MASK")  # 2 octets (R1..R10)
    TRANS_STEP2_STATE: int = _Layout.alloc(1, "TRANS_STEP2_STATE")  # passe 2.2 + flag mouvement
    TRANS_GLOBAL_SEUIL_MOD: int = _Layout.alloc(1, "TRANS_GLOBAL_SEUIL_MOD")  # 1 octet signé
    TRANS_PARCEL_SEUIL_MOD: int = _Layout.alloc(NUM_PARCELS, "TRANS_PARCEL_SEUIL_MOD")  # 30 octets signés
    TRANS_PARCEL_FLAGS: int = _Layout.alloc(NUM_PARCELS, "TRANS_PARCEL_FLAGS")  # 30 octets bitmask
    TRANS_ONCE_PER_TURN: int = _Layout.alloc(8, "TRANS_ONCE_PER_TURN")  # 8 octets = 64 bits
    TRANS_PENDING_APPRENTISSAGE: int = _Layout.alloc(TRACK_LEN, "TRANS_PENDING_APPRENTISSAGE")  # 6 octets
    TRANS_VOLUNTARY_APP_COUNTER: int = _Layout.alloc(1, "TRANS_VOLUNTARY_APP_COUNTER")  # 1 octet
    TRANSIENT_END: int = _Layout._cursor

    USED_BYTES: int = _Layout._cursor


assert _Layout._cursor <= STATE_BUF_SIZE - MIN_FREE_RESERVE_BYTES, (
    f"Réserve libre insuffisante : {_Layout._cursor} octets utilisés sur {STATE_BUF_SIZE} "
    f"(réserve < {MIN_FREE_RESERVE_BYTES})"
)


def get_layout_report() -> dict[str, Any]:
    """Retourne le bilan détaillé d'allocation mémoire sur les 384 octets (6 cache lines)."""
    return {
        "capacity_bytes": STATE_BUF_SIZE,
        "used_bytes": _Mem.USED_BYTES,
        "free_bytes": STATE_BUF_SIZE - _Mem.USED_BYTES,
        "transient_range": (_Mem.TRANSIENT_START, _Mem.TRANSIENT_END),
        "blocks": list(_Layout._blocks),
    }


@dataclass(frozen=True, slots=True)
class GameConfig:
    """Configuration immuable d'une partie (Mode 1..4 et 7 axes des 128 châssis)."""

    n_players: int = 4
    mode: int = 1
    peuples: tuple[str, ...] = ()
    exp_seed: int = 42
    rep_id: int = 0
    coordonnateur_initial: int = 0
    max_revision_passes: int = 4

    # 7 axes du châssis v5.3.1
    p_max: int = 4
    regle_ouverture_reve_multiple: str = "UNIQUE_PAR_TOUR"
    offset_seuil_parade: int = 0
    mise_en_place_tactiques: str = "ORDRE_FIXE_T1_T6"
    declenchement_fin_de_piste: str = "ARRIVEE_DERNIERE_PARCELLE"
    role_abatteuse_fin_de_piste: str = "STANDARD_COUPE_ARBRE"
    synergie_binome_machines: str = "INDIVIDUELLE"

    # Sélections de profils optionnelles (Mode 3/4) : ((slot_id, profile_key), ...)
    tile_profiles: tuple[tuple[str, str], ...] = ()

    # Champs dérivés immuables calculés à l'initialisation
    dotation_arbres: tuple[int, ...] = ()
    lisiere_slots: tuple[str, ...] = ()
    total_gardiens_partie: int = 0

    def __post_init__(self) -> None:
        assert 3 <= self.n_players <= MAX_N, f"n_players invalide : {self.n_players}"
        assert self.mode in (1, 2, 3, 4), f"mode invalide : {self.mode}"
        assert self.p_max in TOPOLOGIES_DOTATION, f"p_max invalide : {self.p_max}"
        assert self.regle_ouverture_reve_multiple in ("UNIQUE_PAR_TOUR", "PAR_DE_M_DESIGNE")
        assert self.offset_seuil_parade in (0, 1)
        assert self.mise_en_place_tactiques in ("ORDRE_FIXE_T1_T6", "ALEATOIRE")
        assert self.declenchement_fin_de_piste in (
            "ARRIVEE_DERNIERE_PARCELLE",
            "DEPASSEMENT_DERNIERE_PARCELLE",
        )
        assert self.role_abatteuse_fin_de_piste in (
            "STANDARD_COUPE_ARBRE",
            "ARRACHE_1_SOUCHE_SI_SANS_ARBRE",
        )
        assert self.synergie_binome_machines in (
            "INDIVIDUELLE",
            "MUTUALISATION_PUISSANCE_MEME_PARCELLE",
        )
        assert 0 <= self.coordonnateur_initial < self.n_players

        peuples = self.peuples if self.peuples else PEUPLES_ORDER[: self.n_players]
        assert len(peuples) == self.n_players
        assert len(set(peuples)) == self.n_players
        for p in peuples:
            assert p in PEUPLE_TO_ID, f"Peuple inconnu : {p}"
        object.__setattr__(self, "peuples", tuple(peuples))

        dotation = TOPOLOGIES_DOTATION[self.p_max]
        object.__setattr__(self, "dotation_arbres", dotation)

        if self.mode == 1:
            object.__setattr__(self, "lisiere_slots", ())
            object.__setattr__(self, "total_gardiens_partie", 0)
        else:
            slots: list[str] = []
            g_count = 0
            for s in range(self.n_players):
                p_left = peuples[s]
                p_right = peuples[(s + 1) % self.n_players]
                t0, t1 = MATRICE_PAIRES[f"{p_left}_{p_right}"]
                slots.extend((t0, t1))
                if SYNERGY_META[t0][0] == FAMILLE_GARDIEN:
                    g_count += 1
                if SYNERGY_META[t1][0] == FAMILLE_GARDIEN:
                    g_count += 1
            object.__setattr__(self, "lisiere_slots", tuple(slots))
            object.__setattr__(self, "total_gardiens_partie", g_count)

    @classmethod
    def from_chassis_index(
        cls,
        chassis_idx: int,
        *,
        n_players: int = 4,
        mode: int = 1,
        peuples: tuple[str, ...] = (),
        exp_seed: int = 42,
        rep_id: int = 0,
        coordonnateur_initial: int = 0,
        max_revision_passes: int = 4,
    ) -> GameConfig:
        """Construit l'une des 128 configurations de châssis à partir d'un index 0..127."""
        assert 0 <= chassis_idx < 128
        kwargs: dict[str, Any] = {
            "n_players": n_players,
            "mode": mode,
            "peuples": peuples,
            "exp_seed": exp_seed,
            "rep_id": rep_id,
            "coordonnateur_initial": coordonnateur_initial,
            "max_revision_passes": max_revision_passes,
        }
        for bit_pos, (field_name, options) in enumerate(CHASSIS_AXES_OPTIONS):
            kwargs[field_name] = options[(chassis_idx >> bit_pos) & 1]
        return cls(**kwargs)

    def seat_of_peuple(self, peuple_code: str) -> int | None:
        """Retourne le siège contrôlant ce Peuple, ou None s'il est absent de la table."""
        for idx, code in enumerate(self.peuples):
            if code == peuple_code:
                return idx
        return None

    def profile_for_slot(self, slot_id: str) -> str | None:
        """Retourne le profil actif d'un emplacement (A/A en Mode 2 uniquement pour Migration)."""
        if self.mode == 1:
            return None
        if self.mode == 2:
            if slot_id in ("SLOT_BUG_CERVEAU", "SLOT_COLONISATION_GARDIENS"):
                return "A"
            return None
        for s_id, prof in self.tile_profiles:
            if s_id == slot_id:
                return prof
        if slot_id in ("SLOT_BUG_CERVEAU", "SLOT_COLONISATION_GARDIENS"):
            return "A"
        return "A"


# --- Structures immuables d'observation publique/privée ---


class ParcelObs(NamedTuple):
    arbres: int
    souches: int
    insectes: int
    piege: int
    defenseurs: int
    nid_id: int
    nid_active_ce_tour: bool
    est_route: bool


class FurtiviteCellObs(NamedTuple):
    slots_faces: tuple[int, int, int, int]
    nb_def_rive_0: int
    nb_def_rive_1: int
    insectes: int


class LisiereTileObs(NamedTuple):
    tile_id: str
    status: int
    constructors: int


class GardienSlotObs(NamedTuple):
    gardien_num: int
    tile_id: str | None
    face: int
    used_this_turn: bool


class TactiqueSlotObs(NamedTuple):
    code: int
    tile_id: str
    apprentissage: int
    bugs: int


class MachineObs(NamedTuple):
    ray: int
    m_type: int
    position: int
    status: int
    rouges: int
    bleus: int


class HandObs(NamedTuple):
    """Main observée d'un siège : None sur les champs secrets si paravents fermés pour autrui."""

    has_card: bool
    card: int | None
    d1: int | None
    d2: int | None
    lecture_m: int | None
    bound_tactique: int | None


_MASKED_HAS_CARD_SENTINEL: int = 0x0F
_ZERO_DECK_BYTES: bytes = b"\x00" * (DECK_SLOTS_CAPACITY // 2)
_ZERO_TRANSIENT_BYTES: bytes = b"\x00" * (_Mem.TRANSIENT_END - _Mem.TRANSIENT_START)
_ZERO_6_BYTES: bytes = b"\x00" * 6
_ZERO_12_BYTES: bytes = b"\x00" * 12
_ZERO_15_BYTES: bytes = b"\x00" * 15
_ZERO_30_BYTES: bytes = b"\x00" * 30


class PlayerObservation:
    """Vue immuable strictement isolée sur snapshot 384 octets assaini (zéro fuite paquet/mains)."""

    __slots__ = ("_cfg", "_snap", "observer_seat")

    def __init__(self, observer_seat: int, cfg: GameConfig, sanitized_snap: bytes) -> None:
        self.observer_seat: int = observer_seat
        self._cfg: GameConfig = cfg
        self._snap: bytes = sanitized_snap

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlayerObservation):
            return NotImplemented
        return (
            self.observer_seat == other.observer_seat
            and self._snap == other._snap
            and self._cfg == other._cfg
        )

    def __hash__(self) -> int:
        return hash((self.observer_seat, self._snap))

    @property
    def n_players(self) -> int:
        return self._cfg.n_players

    @property
    def mode(self) -> int:
        return self._cfg.mode

    @property
    def tour(self) -> int:
        return self._snap[_Mem.TOUR]

    @property
    def step(self) -> int:
        return self._snap[_Mem.STEP]

    @property
    def coordonnateur(self) -> int:
        return self._snap[_Mem.COORDONNATEUR]

    @property
    def paravents_ouverts(self) -> bool:
        return bool(self._snap[_Mem.FLAGS] & _FLAG_PARAVENTS_OUVERTS)

    @property
    def seuil_reveil(self) -> int:
        return self._snap[_Mem.SEUIL_REVEIL]

    @property
    def triggers_lit(self) -> int:
        return self._snap[_Mem.TRIGGERS_LIT]

    @property
    def deck_remaining_count(self) -> int:
        rem = self._snap[_Mem.DECK_LEN] - self._snap[_Mem.DECK_CURSOR]
        return max(0, rem)

    @property
    def sabotage_deck_count(self) -> int:
        return self._snap[_Mem.SABOTAGE_DECK_COUNT]

    @property
    def sabotage_pending_count(self) -> int:
        return self._snap[_Mem.SABOTAGE_PENDING_COUNT]

    @property
    def reshuffle_count(self) -> int:
        return self._snap[_Mem.RESHUFFLE_COUNT]

    def hand_of(self, seat: int) -> HandObs:
        """Accès direct O(1) à la main observée d'un siège (masquée si paravent fermé)."""
        hp = _Mem.PLAYER_HANDS + seat * 2
        u16 = self._snap[hp] | (self._snap[hp + 1] << 8)
        card = u16 & 0x0F
        if card == _MASKED_HAS_CARD_SENTINEL:
            return HandObs(True, None, None, None, None, None)
        if not self.paravents_ouverts and seat != self.observer_seat:
            return HandObs(False, None, None, None, None, None)
        return HandObs(
            card != CARD_NONE,
            card,
            (u16 >> 4) & 0x07,
            (u16 >> 7) & 0x07,
            (u16 >> 10) & 0x07,
            (u16 >> 13) & 0x07,
        )

    @property
    def hands(self) -> tuple[HandObs, ...]:
        return tuple(self.hand_of(s) for s in range(self._cfg.n_players))

    @property
    def foret(self) -> tuple[tuple[ParcelObs, ...], ...]:
        buf = self._snap
        n = self._cfg.n_players
        p_max = self._cfg.p_max
        nid_by_loc: dict[int, tuple[int, bool]] = {}
        if self._cfg.mode >= 2:
            for m_idx in range(NUM_NIDS):
                raw_n = buf[_Mem.NIDS_STATE + m_idx]
                loc_n = raw_n & 0x7F
                if loc_n != 0:
                    nid_by_loc[loc_n - 1] = (m_idx + 1, bool(raw_n & 0x80))
        rows: list[tuple[ParcelObs, ...]] = []
        for r in range(n):
            row: list[ParcelObs] = []
            r_base = r * MAX_P
            for p_off in range(p_max):
                idx = r_base + p_off
                as_byte = buf[_Mem.FORET_ARBRES_SOUCHES + idx]
                piege = (buf[_Mem.FORET_PIEGES + (idx >> 2)] >> ((idx & 3) * 2)) & 0x03
                def_b = buf[_Mem.FORET_DEFENSEURS + (idx >> 1)]
                defs = ((def_b >> 4) & 0x0F) if (idx & 1) else (def_b & 0x0F)
                nid_pair = nid_by_loc.get(idx)
                nid_id, nid_act = (0, False) if nid_pair is None else nid_pair
                row.append(
                    ParcelObs(
                        (as_byte >> 4) & 0x0F,
                        as_byte & 0x0F,
                        buf[_Mem.FORET_INSECTES + idx],
                        piege,
                        defs,
                        nid_id,
                        nid_act,
                        as_byte == 0,
                    )
                )
            rows.append(tuple(row))
        return tuple(rows)

    @property
    def furtivite(self) -> tuple[tuple[FurtiviteCellObs, ...], ...]:
        buf = self._snap
        n = self._cfg.n_players
        p_max = self._cfg.p_max
        rows: list[tuple[FurtiviteCellObs, ...]] = []
        for l_idx in range(n):
            row: list[FurtiviteCellObs] = []
            l_base = l_idx * MAX_P
            for p_off in range(p_max):
                idx = l_base + p_off
                sb = buf[_Mem.FURTIVITE_SLOTS + idx]
                s0, s1, s2, s3 = sb & 3, (sb >> 2) & 3, (sb >> 4) & 3, (sb >> 6) & 3
                fb = buf[_Mem.FURTIVITE_INSECTES + (idx >> 1)]
                f_ins = ((fb >> 4) & 0x0F) if (idx & 1) else (fb & 0x0F)
                row.append(
                    FurtiviteCellObs(
                        (s0, s1, s2, s3),
                        (1 if s0 else 0) + (1 if s1 else 0),
                        (1 if s2 else 0) + (1 if s3 else 0),
                        f_ins,
                    )
                )
            rows.append(tuple(row))
        return tuple(rows)

    @property
    def lisieres(self) -> tuple[LisiereTileObs, ...]:
        if self._cfg.mode == 1:
            return ()
        buf = self._snap
        l_slots = self._cfg.lisiere_slots
        out: list[LisiereTileObs] = []
        for idx in range(2 * self._cfg.n_players):
            lb = buf[_Mem.LISIERE_TILES + (idx >> 1)]
            nib = ((lb >> 4) & 0x0F) if (idx & 1) else (lb & 0x0F)
            out.append(LisiereTileObs(l_slots[idx], nib & 0x03, (nib >> 2) & 0x03))
        return tuple(out)

    @property
    def piste_gardiens(self) -> tuple[GardienSlotObs, ...]:
        buf = self._snap
        out: list[GardienSlotObs] = []
        for c_off in range(TRACK_LEN):
            gb = buf[_Mem.GARDIENS_PISTE + c_off]
            g_num = gb & 0x0F
            if g_num == 0:
                out.append(GardienSlotObs(0, None, 1, False))
            else:
                out.append(
                    GardienSlotObs(
                        g_num, _GARDIEN_STR_TABLE[g_num], 2 if (gb & 0x10) else 1, bool(gb & 0x20)
                    )
                )
        return tuple(out)

    @property
    def piste_tactiques(self) -> tuple[TactiqueSlotObs, ...]:
        buf = self._snap
        return tuple(
            TactiqueSlotObs(
                buf[_Mem.TACTIQUES_PISTE_ID + i],
                _TACTIQUE_STR_TABLE[buf[_Mem.TACTIQUES_PISTE_ID + i]],
                buf[_Mem.TACTIQUES_APPRENTISSAGE + i],
                buf[_Mem.PISTE_BUGS + i],
            )
            for i in range(TRACK_LEN)
        )

    @property
    def piste_colonie(self) -> tuple[int, ...]:
        buf = self._snap
        return tuple(buf[_Mem.PISTE_COLONIE + i] for i in range(TRACK_LEN))

    @property
    def machines(self) -> tuple[MachineObs, ...]:
        buf = self._snap
        out: list[MachineObs] = []
        for r in range(self._cfg.n_players):
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                m_idx = r * 2 + mt
                ps = buf[_Mem.MACHINE_POS_STATUS + m_idx]
                rb = buf[_Mem.MACHINE_ROUGES_BLEUS + m_idx]
                out.append(MachineObs(r, mt, ps & 0x07, (ps >> 3) & 0x03, (rb >> 4) & 0x0F, rb & 0x0F))
        return tuple(out)

    # --- Accesseurs scalaires O(1) zéro-allocation pour les bots sous JIT PyPy ---
    def is_route(self, r: int, p: int) -> bool:
        """Retourne True si la parcelle (r, p) est une Route Forestière (0 Arbre, 0 Souche)."""
        return self._snap[_Mem.FORET_ARBRES_SOUCHES + r * MAX_P + (p - 1)] == 0

    def parcel_arbres(self, r: int, p: int) -> int:
        """Nombre d'Arbres debout sur (r, p) en O(1)."""
        return (self._snap[_Mem.FORET_ARBRES_SOUCHES + r * MAX_P + (p - 1)] >> 4) & 0x0F

    def parcel_souches(self, r: int, p: int) -> int:
        """Nombre de Souches sur (r, p) en O(1)."""
        return self._snap[_Mem.FORET_ARBRES_SOUCHES + r * MAX_P + (p - 1)] & 0x0F

    def parcel_insectes(self, r: int, p: int) -> int:
        """Nombre d'Insectes sur (r, p) en O(1)."""
        return self._snap[_Mem.FORET_INSECTES + r * MAX_P + (p - 1)]

    def parcel_piege(self, r: int, p: int) -> int:
        """État du Piège (0=aucun, 1=actif, 2=déclenché) sur (r, p) en O(1)."""
        idx = r * MAX_P + (p - 1)
        return (self._snap[_Mem.FORET_PIEGES + (idx >> 2)] >> ((idx & 3) * 2)) & 0x03

    def parcel_defenseurs(self, r: int, p: int) -> int:
        """Nombre de Défenseurs en forêt sur (r, p) en O(1)."""
        idx = r * MAX_P + (p - 1)
        b = self._snap[_Mem.FORET_DEFENSEURS + (idx >> 1)]
        return ((b >> 4) & 0x0F) if (idx & 1) else (b & 0x0F)

    def parcel_has_nid(self, r: int, p: int) -> bool:
        """Retourne True si un Nid est présent sur (r, p) en Mode >= 2."""
        if self._cfg.mode < 2:
            return False
        target_loc = r * MAX_P + p
        buf = self._snap
        for m_idx in range(NUM_NIDS):
            if (buf[_Mem.NIDS_STATE + m_idx] & 0x7F) == target_loc:
                return True
        return False

    def furtivite_defs_and_ins(self, lisiere: int, p: int) -> tuple[int, int]:
        """Retourne (nb_total_defenseurs, nb_insectes) sur la case Furtivité (lisiere, p) en O(1)."""
        idx = lisiere * MAX_P + (p - 1)
        sb = self._snap[_Mem.FURTIVITE_SLOTS + idx]
        nb_d = (
            (1 if (sb & 3) else 0)
            + (1 if ((sb >> 2) & 3) else 0)
            + (1 if ((sb >> 4) & 3) else 0)
            + (1 if ((sb >> 6) & 3) else 0)
        )
        fb = self._snap[_Mem.FURTIVITE_INSECTES + (idx >> 1)]
        ins = ((fb >> 4) & 0x0F) if (idx & 1) else (fb & 0x0F)
        return nb_d, ins

    def lisiere_tile_info(self, slot_idx: int) -> tuple[str, int, int]:
        """Retourne (tile_id, status, constructors) pour l'emplacement de lisière `slot_idx`."""
        lb = self._snap[_Mem.LISIERE_TILES + (slot_idx >> 1)]
        nib = ((lb >> 4) & 0x0F) if (slot_idx & 1) else (lb & 0x0F)
        return self._cfg.lisiere_slots[slot_idx], nib & 0x03, (nib >> 2) & 0x03

    def machine_pos_status(self, r: int, m_type: int) -> tuple[int, int]:
        """Retourne (position, status) de la machine `(r, m_type)` en O(1)."""
        ps = self._snap[_Mem.MACHINE_POS_STATUS + r * 2 + m_type]
        return ps & 0x07, (ps >> 3) & 0x03

    def gardien_available_at_case(self, case_1_6: int) -> bool:
        """Retourne True si un Gardien non encore utilisé ce tour occupe la case `1..6`."""
        gb = self._snap[_Mem.GARDIENS_PISTE + (case_1_6 - 1)]
        return (gb & 0x0F) > 0 and not (gb & 0x20)

    def tactique_code_bugs_app(self, rank_0_5: int) -> tuple[int, int, int]:
        """Retourne (code, bugs, apprentissage) au rang `0..5` de la piste Tactiques."""
        buf = self._snap
        return (
            buf[_Mem.TACTIQUES_PISTE_ID + rank_0_5],
            buf[_Mem.PISTE_BUGS + rank_0_5],
            buf[_Mem.TACTIQUES_APPRENTISSAGE + rank_0_5],
        )


# --- Encodage compact des localisations de pions Défenseurs (0..162, 255) ---
# 0 : en main
# 1..30 : parcelle Forêt (1 + r * MAX_P + (p - 1))
# 31..150 : slot jumeau Furtivité (31 + (l * MAX_P + (p - 1)) * 4 + slot_0_3)
# 151..162 : tuile Synergie en lisière (151 + lisiere_slot_idx)
# 255 : impasse (aucune case légale disponible ce tour, pion consommé hors plateau jusqu'en 6.2)
_LOC_HAND: int = 0
_LOC_FORET_BASE: int = 1
_LOC_FURT_BASE: int = _LOC_FORET_BASE + NUM_PARCELS  # 31
_LOC_LISIERE_BASE: int = _LOC_FURT_BASE + NUM_PARCELS * 4  # 151
_LOC_IMPASSE: int = 255


class GameState:
    """État complet d'une partie, intégralement contenu dans bytearray(384) + _continuation légère."""

    __slots__ = ("_buf", "_continuation", "cfg")

    def __init__(
        self,
        cfg: GameConfig,
        *,
        _raw_buf: bytearray | None = None,
        _continuation: list[tuple[Any, ...]] | None = None,
    ) -> None:
        self.cfg: GameConfig = cfg
        if _raw_buf is not None:
            assert len(_raw_buf) == STATE_BUF_SIZE
            self._buf: bytearray = _raw_buf
            self._continuation: list[tuple[Any, ...]] = (
                list(_continuation) if _continuation else []
            )
            return

        self._buf = bytearray(STATE_BUF_SIZE)
        self._continuation = []
        self._init_board()

    def clone(self) -> GameState:
        """Copie rapide et strictement indépendante à l'octet près (compatible IS-MCTS / Forks)."""
        cont_copy = [
            tuple(item) if isinstance(item, list) else item for item in self._continuation
        ]
        return GameState(self.cfg, _raw_buf=bytearray(self._buf), _continuation=cont_copy)

    def raw_used_bytes(self) -> bytes:
        """Extrait immuable des octets alloués (pour assertions de tests et hachage déterministe)."""
        return bytes(self._buf[: _Mem.USED_BYTES])

    # ------------------------------------------------------------------
    # Initialisation d'une nouvelle partie
    # ------------------------------------------------------------------
    def _init_board(self) -> None:
        cfg = self.cfg
        n = cfg.n_players
        p_max = cfg.p_max

        self.tour = 1
        self.step = STEP_1_1_SIEGE
        self.coordonnateur = cfg.coordonnateur_initial
        self.paravents_ouverts = False

        # Seuil fixe de Réveil des Gardiens (calculé une fois pour toutes à la mise en place)
        g0 = cfg.total_gardiens_partie
        self.seuil_reveil = min(n, g0, 5) if (cfg.mode >= 2 and g0 >= 3) else 0
        self.triggers_lit = 0

        # Parcelles Forêt (dotation initiale d'Arbres, 0 Souche)
        for r in range(n):
            for p in range(1, p_max + 1):
                self.set_parcel_arbres_souches(r, p, cfg.dotation_arbres[p - 1], 0)

        # Tuiles de Synergie en lisière (Mode 2+)
        if cfg.mode >= 2:
            for slot_idx in range(2 * n):
                self.set_lisiere_tile_state(slot_idx, LISIERE_UNCONSTRUCTED, 0)

        # Piste des Tactiques T1..T6
        tactiques_init = [1, 2, 3, 4, 5, 6]
        if cfg.mise_en_place_tactiques == "ALEATOIRE":
            tactiques_init = shuffle_deterministic(
                tactiques_init,
                cfg.exp_seed,
                cfg.rep_id,
                SRC_TACTICS_SETUP,
                0,
                0,
            )
        for rank_idx, t_code in enumerate(tactiques_init):
            self.set_tactique_at_rank(rank_idx, t_code)

        # Machines : 1 Abatteuse + 1 Bulldozer par rayon sur p = 1
        for r in range(n):
            self.set_machine_pos_status(r, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
            self.set_machine_pos_status(r, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)

        # Paquet Machine initial (2N cartes Machine, 0 Sabotage, mélange initial reshuffle_count=0)
        self.sabotage_deck_count = 0
        self.sabotage_pending_count = 0
        self.reshuffle_count = 0
        self.rebuild_and_shuffle_machine_deck(increment_reshuffle=False)

    # ------------------------------------------------------------------
    # Utilitaires internes nibble / 2-bit
    # ------------------------------------------------------------------
    @staticmethod
    def _parcel_idx(r: int, p: int) -> int:
        assert 0 <= r < MAX_N, f"rayon hors bornes : {r}"
        assert 1 <= p <= MAX_P, f"profondeur hors bornes : {p}"
        return r * MAX_P + (p - 1)

    def _get_nibble(self, base: int, idx: int) -> int:
        b = self._buf[base + (idx >> 1)]
        return (b >> 4) & 0x0F if (idx & 1) else (b & 0x0F)

    def _set_nibble(self, base: int, idx: int, val: int) -> None:
        assert 0 <= val <= 0x0F, f"valeur nibble hors bornes : {val}"
        pos = base + (idx >> 1)
        b = self._buf[pos]
        if idx & 1:
            self._buf[pos] = (b & 0x0F) | (val << 4)
        else:
            self._buf[pos] = (b & 0xF0) | val

    def _get_crumb(self, base: int, idx: int) -> int:
        b = self._buf[base + (idx >> 2)]
        shift = (idx & 3) * 2
        return (b >> shift) & 0x03

    def _set_crumb(self, base: int, idx: int, val: int) -> None:
        assert 0 <= val <= 0x03, f"valeur 2-bit hors bornes : {val}"
        pos = base + (idx >> 2)
        shift = (idx & 3) * 2
        self._buf[pos] = (self._buf[pos] & ~(0x03 << shift)) | (val << shift)

    # ------------------------------------------------------------------
    # Accesseurs globaux de tour et contrôle
    # ------------------------------------------------------------------
    @property
    def tour(self) -> int:
        return self._buf[_Mem.TOUR]

    @tour.setter
    def tour(self, val: int) -> None:
        assert 1 <= val <= 16
        self._buf[_Mem.TOUR] = val

    @property
    def step(self) -> int:
        return self._buf[_Mem.STEP]

    @step.setter
    def step(self, val: int) -> None:
        assert 0 <= val <= 255
        self._buf[_Mem.STEP] = val

    @property
    def coordonnateur(self) -> int:
        return self._buf[_Mem.COORDONNATEUR]

    @coordonnateur.setter
    def coordonnateur(self, seat: int) -> None:
        assert 0 <= seat < self.cfg.n_players
        self._buf[_Mem.COORDONNATEUR] = seat

    @property
    def paravents_ouverts(self) -> bool:
        return bool(self._buf[_Mem.FLAGS] & _FLAG_PARAVENTS_OUVERTS)

    @paravents_ouverts.setter
    def paravents_ouverts(self, opened: bool) -> None:
        if opened:
            self._buf[_Mem.FLAGS] |= _FLAG_PARAVENTS_OUVERTS
        else:
            self._buf[_Mem.FLAGS] &= ~_FLAG_PARAVENTS_OUVERTS

    @property
    def step2_locked(self) -> bool:
        return bool(self._buf[_Mem.FLAGS] & _FLAG_STEP2_LOCKED)

    @step2_locked.setter
    def step2_locked(self, locked: bool) -> None:
        if locked:
            self._buf[_Mem.FLAGS] |= _FLAG_STEP2_LOCKED
        else:
            self._buf[_Mem.FLAGS] &= ~_FLAG_STEP2_LOCKED

    @property
    def seuil_reveil(self) -> int:
        return self._buf[_Mem.SEUIL_REVEIL]

    @seuil_reveil.setter
    def seuil_reveil(self, val: int) -> None:
        assert 0 <= val <= 6
        self._buf[_Mem.SEUIL_REVEIL] = val

    @property
    def triggers_lit(self) -> int:
        return self._buf[_Mem.TRIGGERS_LIT]

    @triggers_lit.setter
    def triggers_lit(self, mask: int) -> None:
        assert 0 <= mask <= 0x3F
        self._buf[_Mem.TRIGGERS_LIT] = mask

    def light_trigger(self, case_num: int) -> None:
        """Allume le signal binaire d'une case 1..6 sur la Piste des Gardiens."""
        assert 1 <= case_num <= 6
        if self.cfg.mode >= 2:
            self._buf[_Mem.TRIGGERS_LIT] |= 1 << (case_num - 1)

    def is_trigger_lit(self, case_num: int) -> bool:
        assert 1 <= case_num <= 6
        return bool(self._buf[_Mem.TRIGGERS_LIT] & (1 << (case_num - 1)))

    def clear_trigger(self, case_num: int) -> None:
        assert 1 <= case_num <= 6
        self._buf[_Mem.TRIGGERS_LIT] &= ~(1 << (case_num - 1))

    # ------------------------------------------------------------------
    # Accesseurs Parcelles Forêt & Routes Forestières
    # ------------------------------------------------------------------
    def _assert_active_parcel(self, r: int, p: int) -> int:
        assert 0 <= r < self.cfg.n_players, f"rayon invalide {r}"
        assert 1 <= p <= self.cfg.p_max, f"parcelle invalide {p}"
        return r * MAX_P + (p - 1)

    def get_parcel_arbres(self, r: int, p: int) -> int:
        idx = self._assert_active_parcel(r, p)
        return (self._buf[_Mem.FORET_ARBRES_SOUCHES + idx] >> 4) & 0x0F

    def get_parcel_souches(self, r: int, p: int) -> int:
        idx = self._assert_active_parcel(r, p)
        return self._buf[_Mem.FORET_ARBRES_SOUCHES + idx] & 0x0F

    def set_parcel_arbres_souches(self, r: int, p: int, arbres: int, souches: int) -> None:
        idx = self._assert_active_parcel(r, p)
        assert 0 <= arbres <= 15 and 0 <= souches <= 15
        self._buf[_Mem.FORET_ARBRES_SOUCHES + idx] = (arbres << 4) | souches

    def is_route_forestiere(self, r: int, p: int) -> bool:
        """Une parcelle à 0 Arbre et 0 Souche est une Route Forestière."""
        idx = self._assert_active_parcel(r, p)
        return self._buf[_Mem.FORET_ARBRES_SOUCHES + idx] == 0

    def get_parcel_insectes(self, r: int, p: int) -> int:
        idx = self._assert_active_parcel(r, p)
        return self._buf[_Mem.FORET_INSECTES + idx]

    def set_parcel_insectes(self, r: int, p: int, count: int) -> None:
        idx = self._assert_active_parcel(r, p)
        assert 0 <= count <= 255
        self._buf[_Mem.FORET_INSECTES + idx] = count

    def get_parcel_piege(self, r: int, p: int) -> int:
        idx = self._assert_active_parcel(r, p)
        return self._get_crumb(_Mem.FORET_PIEGES, idx)

    def set_parcel_piege(self, r: int, p: int, state_val: int) -> None:
        idx = self._assert_active_parcel(r, p)
        assert state_val in (PIEGE_AUCUN, PIEGE_ACTIF, PIEGE_DECLENCHE)
        self._set_crumb(_Mem.FORET_PIEGES, idx, state_val)

    def get_parcel_defenseurs(self, r: int, p: int) -> int:
        idx = self._assert_active_parcel(r, p)
        return self._get_nibble(_Mem.FORET_DEFENSEURS, idx)

    def set_parcel_defenseurs(self, r: int, p: int, count: int) -> None:
        idx = self._assert_active_parcel(r, p)
        assert 0 <= count <= 15
        self._set_nibble(_Mem.FORET_DEFENSEURS, idx, count)

    def get_parcel_nid(self, r: int, p: int) -> tuple[int, bool]:
        """Retourne (m_num 1..5 ou 0, active_ce_tour)."""
        idx = self._assert_active_parcel(r, p)
        target_loc = idx + 1
        for m_idx in range(NUM_NIDS):
            raw = self._buf[_Mem.NIDS_STATE + m_idx]
            if (raw & 0x7F) == target_loc:
                return m_idx + 1, bool(raw & 0x80)
        return 0, False

    def get_parcel_nid_encoded(self, r: int, p: int) -> int:
        """Retourne 0 ou (id_slot_M | (0x80 si activé ce tour))."""
        m_num, active = self.get_parcel_nid(r, p)
        if m_num == 0:
            return 0
        return m_num | (0x80 if active else 0)

    def set_parcel_nid(self, r: int, p: int, m_num: int, active_ce_tour: bool = False) -> None:
        idx = self._assert_active_parcel(r, p)
        assert 1 <= m_num <= NUM_NIDS
        existing, _ = self.get_parcel_nid(r, p)
        assert existing in (0, m_num), "1 seul Nid maximum par parcelle"
        self._buf[_Mem.NIDS_STATE + (m_num - 1)] = (idx + 1) | (0x80 if active_ce_tour else 0)

    def clear_nid(self, m_num: int) -> None:
        assert 1 <= m_num <= NUM_NIDS
        self._buf[_Mem.NIDS_STATE + (m_num - 1)] = 0

    def set_nid_activated(self, m_num: int, active_ce_tour: bool) -> None:
        assert 1 <= m_num <= NUM_NIDS
        raw = self._buf[_Mem.NIDS_STATE + (m_num - 1)]
        assert (raw & 0x7F) != 0, "Nid absent du plateau"
        self._buf[_Mem.NIDS_STATE + (m_num - 1)] = (raw & 0x7F) | (0x80 if active_ce_tour else 0)

    def get_nid_position(self, m_num: int) -> tuple[int, int, bool] | None:
        """Retourne (ray, p, active_ce_tour) si le Nid M{m_num} est en forêt, sinon None."""
        assert 1 <= m_num <= NUM_NIDS
        raw = self._buf[_Mem.NIDS_STATE + (m_num - 1)]
        loc = raw & 0x7F
        if loc == 0:
            return None
        p_idx = loc - 1
        return p_idx // MAX_P, (p_idx % MAX_P) + 1, bool(raw & 0x80)

    # Navigation sur rayon en sautant les Routes Forestières
    def next_non_razed_towards_heart(self, r: int, from_p: int) -> int | None:
        """Prochaine parcelle non rasée vers le cœur (p > from_p), ou None."""
        assert 0 <= r < self.cfg.n_players
        assert 0 <= from_p <= self.cfg.p_max
        for cand in range(from_p + 1, self.cfg.p_max + 1):
            if not self.is_route_forestiere(r, cand):
                return cand
        return None

    def next_non_razed_towards_border(self, r: int, from_p: int) -> int | None:
        """Prochaine parcelle non rasée vers la bordure (p < from_p), ou None."""
        assert 0 <= r < self.cfg.n_players
        assert 1 <= from_p <= self.cfg.p_max + 1
        for cand in range(from_p - 1, 0, -1):
            if not self.is_route_forestiere(r, cand):
                return cand
        return None

    def first_non_razed_from_border(self, r: int) -> int | None:
        return self.next_non_razed_towards_heart(r, 0)

    def last_non_razed_parcel(self, r: int) -> int | None:
        return self.next_non_razed_towards_border(r, self.cfg.p_max + 1)

    def total_arbres_rayon(self, r: int) -> int:
        return sum(self.get_parcel_arbres(r, p) for p in range(1, self.cfg.p_max + 1))

    def total_arbres_plateau(self) -> int:
        return sum(self.total_arbres_rayon(r) for r in range(self.cfg.n_players))

    # ------------------------------------------------------------------
    # Accesseurs Furtivité à 4 emplacements jumeaux (slots 0,1 = rive 0 ; 2,3 = rive 1)
    # ------------------------------------------------------------------
    def _assert_active_furtivite(self, lisiere: int, p: int) -> int:
        assert 0 <= lisiere < self.cfg.n_players
        assert 1 <= p <= self.cfg.p_max
        return lisiere * MAX_P + (p - 1)

    def lisiere_ray_for_rive(self, lisiere: int, rive: int) -> int:
        assert 0 <= lisiere < self.cfg.n_players
        assert rive in (0, 1)
        return lisiere if rive == 0 else (lisiere + 1) % self.cfg.n_players

    def get_furtivite_slot_face(self, lisiere: int, p: int, slot_0_3: int) -> int:
        idx = self._assert_active_furtivite(lisiere, p)
        assert 0 <= slot_0_3 <= 3
        b = self._buf[_Mem.FURTIVITE_SLOTS + idx]
        return (b >> (slot_0_3 * 2)) & 0x03

    def set_furtivite_slot_face(self, lisiere: int, p: int, slot_0_3: int, face: int) -> None:
        idx = self._assert_active_furtivite(lisiere, p)
        assert 0 <= slot_0_3 <= 3
        assert face in (FACE_VIDE, FACE_REFLEXION, FACE_DEFINITIF)
        shift = slot_0_3 * 2
        b = self._buf[_Mem.FURTIVITE_SLOTS + idx]
        self._buf[_Mem.FURTIVITE_SLOTS + idx] = (b & ~(0x03 << shift)) | (face << shift)

    def get_furtivite_slots(self, lisiere: int, p: int) -> tuple[int, int, int, int]:
        idx = self._assert_active_furtivite(lisiere, p)
        b = self._buf[_Mem.FURTIVITE_SLOTS + idx]
        return (b & 0x03, (b >> 2) & 0x03, (b >> 4) & 0x03, (b >> 6) & 0x03)

    def get_furtivite_nb_def_rive(self, lisiere: int, p: int, rive: int) -> int:
        assert rive in (0, 1)
        s0, s1, s2, s3 = self.get_furtivite_slots(lisiere, p)
        if rive == 0:
            return int(s0 != FACE_VIDE) + int(s1 != FACE_VIDE)
        return int(s2 != FACE_VIDE) + int(s3 != FACE_VIDE)

    def get_furtivite_total_defs(self, lisiere: int, p: int) -> int:
        s0, s1, s2, s3 = self.get_furtivite_slots(lisiere, p)
        return (
            int(s0 != FACE_VIDE)
            + int(s1 != FACE_VIDE)
            + int(s2 != FACE_VIDE)
            + int(s3 != FACE_VIDE)
        )

    def get_furtivite_insectes(self, lisiere: int, p: int) -> int:
        idx = self._assert_active_furtivite(lisiere, p)
        return self._get_nibble(_Mem.FURTIVITE_INSECTES, idx)

    def set_furtivite_insectes(self, lisiere: int, p: int, count: int) -> None:
        idx = self._assert_active_furtivite(lisiere, p)
        assert 0 <= count <= 15
        self._set_nibble(_Mem.FURTIVITE_INSECTES, idx, count)

    # ------------------------------------------------------------------
    # Suivi individuel des Défenseurs 1 & 2 par joueur + primitives de pose
    # ------------------------------------------------------------------
    def get_player_def_loc_raw(self, seat: int, def_idx: int) -> int:
        assert 0 <= seat < self.cfg.n_players
        assert def_idx in (0, 1)
        return self._buf[_Mem.PLAYER_DEF_LOC + seat * 2 + def_idx]

    def set_player_def_loc_raw(self, seat: int, def_idx: int, raw_loc: int) -> None:
        assert 0 <= seat < self.cfg.n_players
        assert def_idx in (0, 1)
        assert 0 <= raw_loc <= 255
        self._buf[_Mem.PLAYER_DEF_LOC + seat * 2 + def_idx] = raw_loc

    def is_player_def2_definitif(self, seat: int) -> bool:
        assert 0 <= seat < self.cfg.n_players
        return bool(self._buf[_Mem.PLAYER_DEF2_DEF_MASK] & (1 << seat))

    def set_player_def2_definitif(self, seat: int, is_definitif: bool) -> None:
        assert 0 <= seat < self.cfg.n_players
        if is_definitif:
            self._buf[_Mem.PLAYER_DEF2_DEF_MASK] |= 1 << seat
        else:
            self._buf[_Mem.PLAYER_DEF2_DEF_MASK] &= ~(1 << seat)

    def decode_def_loc(self, raw_loc: int) -> tuple[str, int, int, int]:
        """Décode une localisation brute en (kind, a, b, c)."""
        if raw_loc == _LOC_HAND:
            return ("HAND", 0, 0, 0)
        if raw_loc == _LOC_IMPASSE:
            return ("IMPASSE", 0, 0, 0)
        if _LOC_FORET_BASE <= raw_loc < _LOC_FURT_BASE:
            p_idx = raw_loc - _LOC_FORET_BASE
            return ("FORET", p_idx // MAX_P, (p_idx % MAX_P) + 1, 0)
        if _LOC_FURT_BASE <= raw_loc < _LOC_LISIERE_BASE:
            rel = raw_loc - _LOC_FURT_BASE
            cell_idx, slot_0_3 = rel // 4, rel % 4
            return ("FURTIVITE", cell_idx // MAX_P, (cell_idx % MAX_P) + 1, slot_0_3)
        slot_idx = raw_loc - _LOC_LISIERE_BASE
        return ("LISIERE", slot_idx, 0, 0)

    def remove_player_defender(self, seat: int, def_idx: int) -> None:
        """Retire proprement le Défenseur (seat, def_idx) de sa position actuelle vers la main."""
        raw = self.get_player_def_loc_raw(seat, def_idx)
        if raw == _LOC_HAND:
            return
        kind, a, b, c = self.decode_def_loc(raw)
        if kind == "FORET":
            cur = self.get_parcel_defenseurs(a, b)
            assert cur >= 1
            self.set_parcel_defenseurs(a, b, cur - 1)
        elif kind == "FURTIVITE":
            self.set_furtivite_slot_face(a, b, c, FACE_VIDE)
        elif kind == "LISIERE":
            st, nb = self.get_lisiere_tile_state(a)
            if nb >= 1:
                self.set_lisiere_tile_state(a, st, nb - 1)
        self.set_player_def_loc_raw(seat, def_idx, _LOC_HAND)
        if def_idx == 1:
            self.set_player_def2_definitif(seat, False)

    def place_defender_foret(self, seat: int, def_idx: int, r: int, p: int, face: int) -> None:
        assert not self.is_route_forestiere(r, p), "Pose interdite sur une Route Forestière"
        assert face in (FACE_REFLEXION, FACE_DEFINITIF)
        self.remove_player_defender(seat, def_idx)
        self.set_parcel_defenseurs(r, p, self.get_parcel_defenseurs(r, p) + 1)
        raw = _LOC_FORET_BASE + self._parcel_idx(r, p)
        self.set_player_def_loc_raw(seat, def_idx, raw)
        if def_idx == 1:
            self.set_player_def2_definitif(seat, face == FACE_DEFINITIF)

    def enter_furtivite(
        self,
        seat: int,
        def_idx: int,
        lisiere: int,
        p: int,
        rive: int,
        face: int,
        preferred_twin: int = 0,
    ) -> None:
        """Fait ENTRER un Défenseur en Furtivité (tire l'éventuel autre pion sur le jumeau)."""
        assert rive in (0, 1)
        assert preferred_twin in (0, 1)
        assert face in (FACE_REFLEXION, FACE_DEFINITIF)
        facing_ray = self.lisiere_ray_for_rive(lisiere, rive)
        assert not self.is_route_forestiere(facing_ray, p), (
            "Pose interdite sur une rive Furtivité face à une Route Forestière"
        )

        # Retrait préalable si ce même pion était déjà sur le plateau (révision 2.2)
        self.remove_player_defender(seat, def_idx)

        assert self.get_furtivite_total_defs(lisiere, p) < 2, "Case Furtivité déjà pleine (2 Déf)"

        # Recherche d'un éventuel autre Défenseur déjà présent sur la case (l, p)
        other_found: tuple[int, int, int, int] | None = None  # (o_seat, o_def_idx, old_slot, o_face)
        cell_idx = self._parcel_idx(lisiere, p)
        base_raw = _LOC_FURT_BASE + cell_idx * 4
        for o_seat in range(self.cfg.n_players):
            for o_d in (0, 1):
                o_raw = self.get_player_def_loc_raw(o_seat, o_d)
                if base_raw <= o_raw < base_raw + 4:
                    old_slot = o_raw - base_raw
                    o_face = self.get_furtivite_slot_face(lisiere, p, old_slot)
                    other_found = (o_seat, o_d, old_slot, o_face)
                    break
            if other_found is not None:
                break

        target_slot = rive * 2 + preferred_twin
        twin_slot = rive * 2 + (1 - preferred_twin)

        if other_found is not None:
            o_seat, o_d, old_slot, o_face = other_found
            # Vider l'ancien slot puis tirer ce partenaire sur l'emplacement jumeau du bord choisi
            self.set_furtivite_slot_face(lisiere, p, old_slot, FACE_VIDE)
            self.set_furtivite_slot_face(lisiere, p, twin_slot, o_face)
            self.set_player_def_loc_raw(o_seat, o_d, base_raw + twin_slot)

        self.set_furtivite_slot_face(lisiere, p, target_slot, face)
        self.set_player_def_loc_raw(seat, def_idx, base_raw + target_slot)
        if def_idx == 1:
            self.set_player_def2_definitif(seat, face == FACE_DEFINITIF)

    def flip_defender2_to_definitif_in_place(self, seat: int) -> None:
        """Retourne sur place le 2e Défenseur réflexion -> définitif (sans aucun tirage)."""
        raw = self.get_player_def_loc_raw(seat, 1)
        assert raw != _LOC_HAND, "2e Défenseur non posé"
        kind, a, b, c = self.decode_def_loc(raw)
        if kind == "FURTIVITE":
            self.set_furtivite_slot_face(a, b, c, FACE_DEFINITIF)
        self.set_player_def2_definitif(seat, True)

    def place_defender_lisiere_tile(
        self, seat: int, def_idx: int, lisiere_slot_idx: int, face: int
    ) -> None:
        assert self.cfg.mode >= 2, "Tuiles G/R/M interdites en Mode 1"
        assert 0 <= lisiere_slot_idx < 2 * self.cfg.n_players
        assert face in (FACE_REFLEXION, FACE_DEFINITIF)
        self.remove_player_defender(seat, def_idx)
        st, nb = self.get_lisiere_tile_state(lisiere_slot_idx)
        assert st == LISIERE_UNCONSTRUCTED, "Tuile déjà construite ou indisponible"
        assert nb < 2, "Tuile déjà pleine (2 constructeurs)"
        self.set_lisiere_tile_state(lisiere_slot_idx, st, nb + 1)
        self.set_player_def_loc_raw(seat, def_idx, _LOC_LISIERE_BASE + lisiere_slot_idx)
        if def_idx == 1:
            self.set_player_def2_definitif(seat, face == FACE_DEFINITIF)

    def mark_defender_impasse(self, seat: int, def_idx: int, face: int) -> None:
        """Consomme le Défenseur sans pose physique lorsque 100 % des cibles légales sont épuisées."""
        assert face in (FACE_REFLEXION, FACE_DEFINITIF)
        self.remove_player_defender(seat, def_idx)
        self.set_player_def_loc_raw(seat, def_idx, _LOC_IMPASSE)
        if def_idx == 1:
            self.set_player_def2_definitif(seat, face == FACE_DEFINITIF)

    # ------------------------------------------------------------------
    # Tuiles de Synergie en lisière (2N emplacements)
    # ------------------------------------------------------------------
    def get_lisiere_tile_state(self, slot_idx: int) -> tuple[int, int]:
        """Retourne (status, nb_constructors)."""
        assert 0 <= slot_idx < NUM_SYNERGY_SLOTS
        nib = self._get_nibble(_Mem.LISIERE_TILES, slot_idx)
        return nib & 0x03, (nib >> 2) & 0x03

    def set_lisiere_tile_state(self, slot_idx: int, status: int, constructors: int) -> None:
        assert 0 <= slot_idx < NUM_SYNERGY_SLOTS
        assert 0 <= status <= 3 and 0 <= constructors <= 3
        self._set_nibble(_Mem.LISIERE_TILES, slot_idx, (constructors << 2) | status)

    def find_lisiere_slot_by_tile_id(self, tile_id: str) -> int | None:
        for idx, tid in enumerate(self.cfg.lisiere_slots):
            if tid == tile_id:
                return idx
        return None

    # ------------------------------------------------------------------
    # Piste des Gardiens 1..6 (index 0..5)
    # ------------------------------------------------------------------
    def get_gardien_at_case(self, case_1_6: int) -> tuple[int, int, bool]:
        """Retourne (g_num 0..15, face 1..2, used_this_turn) sur la case 1..6."""
        assert 1 <= case_1_6 <= TRACK_LEN
        b = self._buf[_Mem.GARDIENS_PISTE + (case_1_6 - 1)]
        g_num = b & 0x0F
        if g_num == 0:
            return 0, 1, False
        face = 2 if (b & 0x10) else 1
        used = bool(b & 0x20)
        return g_num, face, used

    def set_gardien_at_case(
        self, case_1_6: int, g_num: int, face: int = 1, used: bool = False
    ) -> None:
        assert 1 <= case_1_6 <= TRACK_LEN
        assert 0 <= g_num <= 15
        if g_num == 0:
            self._buf[_Mem.GARDIENS_PISTE + (case_1_6 - 1)] = 0
            return
        assert face in (1, 2)
        val = g_num | (0x10 if face == 2 else 0) | (0x20 if used else 0)
        self._buf[_Mem.GARDIENS_PISTE + (case_1_6 - 1)] = val

    def count_used_gardiens_on_track(self) -> int:
        total = 0
        for c in range(1, TRACK_LEN + 1):
            g_num, _, used = self.get_gardien_at_case(c)
            if g_num > 0 and used:
                total += 1
        return total

    # ------------------------------------------------------------------
    # Piste des Tactiques / Rêves 1..6 & pistes Migration Bug / Colonie
    # ------------------------------------------------------------------
    def get_tactique_at_rank(self, rank_0_5: int) -> int:
        assert 0 <= rank_0_5 < TRACK_LEN
        return self._buf[_Mem.TACTIQUES_PISTE_ID + rank_0_5]

    def set_tactique_at_rank(self, rank_0_5: int, code: int) -> None:
        assert 0 <= rank_0_5 < TRACK_LEN
        assert is_tactique_code(code) or is_reve_code(code)
        self._buf[_Mem.TACTIQUES_PISTE_ID + rank_0_5] = code

    def find_tactique_rank(self, code: int) -> int | None:
        for idx in range(TRACK_LEN):
            if self._buf[_Mem.TACTIQUES_PISTE_ID + idx] == code:
                return idx
        return None

    def get_apprentissage_at_rank(self, rank_0_5: int) -> int:
        assert 0 <= rank_0_5 < TRACK_LEN
        return self._buf[_Mem.TACTIQUES_APPRENTISSAGE + rank_0_5]

    def set_apprentissage_at_rank(self, rank_0_5: int, val: int) -> None:
        assert 0 <= rank_0_5 < TRACK_LEN
        assert 0 <= val <= 255
        self._buf[_Mem.TACTIQUES_APPRENTISSAGE + rank_0_5] = val

    def get_bugs_at_case(self, case_1_6: int) -> int:
        assert 1 <= case_1_6 <= TRACK_LEN
        return self._buf[_Mem.PISTE_BUGS + (case_1_6 - 1)]

    def set_bugs_at_case(self, case_1_6: int, count: int) -> None:
        assert 1 <= case_1_6 <= TRACK_LEN
        assert 0 <= count <= 255
        self._buf[_Mem.PISTE_BUGS + (case_1_6 - 1)] = count

    def get_colonie_at_case(self, case_1_6: int) -> int:
        assert 1 <= case_1_6 <= TRACK_LEN
        return self._buf[_Mem.PISTE_COLONIE + (case_1_6 - 1)]

    def set_colonie_at_case(self, case_1_6: int, count: int) -> None:
        assert 1 <= case_1_6 <= TRACK_LEN
        assert 0 <= count <= 255
        self._buf[_Mem.PISTE_COLONIE + (case_1_6 - 1)] = count

    # ------------------------------------------------------------------
    # Machines (ray 0..N-1, m_type 0=Abatteuse / 1=Bulldozer)
    # ------------------------------------------------------------------
    def _machine_idx(self, ray: int, m_type: int) -> int:
        assert 0 <= ray < self.cfg.n_players
        assert m_type in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
        return ray * 2 + m_type

    def get_machine_pos_status(self, ray: int, m_type: int) -> tuple[int, int, bool]:
        """Retourne (pos 0..P_Max, status, pending_siege)."""
        idx = self._machine_idx(ray, m_type)
        b = self._buf[_Mem.MACHINE_POS_STATUS + idx]
        return b & 0x07, (b >> 3) & 0x03, bool(b & 0x20)

    def set_machine_pos_status(
        self, ray: int, m_type: int, pos: int, status: int, pending_siege: bool = False
    ) -> None:
        idx = self._machine_idx(ray, m_type)
        assert 0 <= pos <= self.cfg.p_max
        assert status in (MACHINE_STATUS_NORMAL, MACHINE_STATUS_SIEGE, MACHINE_STATUS_RETIRED)
        val = pos | (status << 3) | (0x20 if pending_siege else 0)
        self._buf[_Mem.MACHINE_POS_STATUS + idx] = val

    def get_machine_tokens(self, ray: int, m_type: int) -> tuple[int, int]:
        """Retourne (rouges, bleus)."""
        idx = self._machine_idx(ray, m_type)
        b = self._buf[_Mem.MACHINE_ROUGES_BLEUS + idx]
        return (b >> 4) & 0x0F, b & 0x0F

    def set_machine_tokens(self, ray: int, m_type: int, rouges: int, bleus: int) -> None:
        idx = self._machine_idx(ray, m_type)
        assert 0 <= rouges <= 15 and 0 <= bleus <= 15
        self._buf[_Mem.MACHINE_ROUGES_BLEUS + idx] = (rouges << 4) | bleus

    def machines_on_parcel(self, ray: int, p: int) -> list[int]:
        """Retourne la liste des types de machines physiquement présentes sur (ray, p)."""
        out: list[int] = []
        for m_type in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = self.get_machine_pos_status(ray, m_type)
            if st != MACHINE_STATUS_RETIRED and pos == p:
                out.append(m_type)
        return out

    # ------------------------------------------------------------------
    # Paquet Machine, Sabotages par dilution & Mains secrètes
    # ------------------------------------------------------------------
    @property
    def deck_len(self) -> int:
        return self._buf[_Mem.DECK_LEN]

    @deck_len.setter
    def deck_len(self, val: int) -> None:
        assert 0 <= val <= 255
        self._buf[_Mem.DECK_LEN] = val

    @property
    def deck_cursor(self) -> int:
        return self._buf[_Mem.DECK_CURSOR]

    @deck_cursor.setter
    def deck_cursor(self, val: int) -> None:
        assert 0 <= val <= 255
        self._buf[_Mem.DECK_CURSOR] = val

    @property
    def sabotage_deck_count(self) -> int:
        return self._buf[_Mem.SABOTAGE_DECK_COUNT]

    @sabotage_deck_count.setter
    def sabotage_deck_count(self, val: int) -> None:
        assert 0 <= val <= 255
        self._buf[_Mem.SABOTAGE_DECK_COUNT] = val

    @property
    def sabotage_pending_count(self) -> int:
        return self._buf[_Mem.SABOTAGE_PENDING_COUNT]

    @sabotage_pending_count.setter
    def sabotage_pending_count(self, val: int) -> None:
        assert 0 <= val <= 255
        self._buf[_Mem.SABOTAGE_PENDING_COUNT] = val

    @property
    def reshuffle_count(self) -> int:
        return self._buf[_Mem.RESHUFFLE_COUNT]

    @reshuffle_count.setter
    def reshuffle_count(self, val: int) -> None:
        assert 0 <= val <= 255
        self._buf[_Mem.RESHUFFLE_COUNT] = val

    def add_permanent_sabotage(self, count: int = 1, *, light_case_3: bool = True) -> None:
        """Ajoute définitivement +count cartes Sabotage (mises de côté pour le remélange 6.3)."""
        assert count >= 1
        self.sabotage_pending_count += count
        if light_case_3:
            self.light_trigger(3)

    def rebuild_and_shuffle_machine_deck(self, *, increment_reshuffle: bool) -> None:
        """Reconstitue le paquet Machine hors Sièges/retirées + Sabotages et le mélange."""
        if increment_reshuffle:
            self.reshuffle_count += 1
        # Intégrer définitivement les Sabotages acquis durant le tour
        total_sabotages = self.sabotage_deck_count + self.sabotage_pending_count
        self.sabotage_deck_count = total_sabotages
        self.sabotage_pending_count = 0

        cards: list[int] = []
        for r in range(self.cfg.n_players):
            for m_type in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                _, st, _ = self.get_machine_pos_status(r, m_type)
                if st == MACHINE_STATUS_NORMAL:
                    cards.append(machine_card_code(r, m_type))
        cards.extend([CARD_SABOTAGE] * total_sabotages)

        shuffled = shuffle_deterministic(
            cards,
            self.cfg.exp_seed,
            self.cfg.rep_id,
            SRC_MACHINE_SHUFFLE,
            self.reshuffle_count,
            0,
        )
        self._store_deck_cards(shuffled)

    def _store_deck_cards(self, cards: list[int]) -> None:
        self.deck_len = len(cards)
        self.deck_cursor = 0
        for i in range(DECK_SLOTS_CAPACITY):
            code = cards[i] if i < len(cards) else CARD_NONE
            self._set_nibble(_Mem.DECK_CARDS, i, code)

    def remove_machine_card_from_deck_if_present(self, card_code: int) -> None:
        """Retire une carte Machine du paquet restant si elle passe en Siège en 1.1."""
        remaining: list[int] = []
        stored_count = min(self.deck_len, DECK_SLOTS_CAPACITY)
        removed = False
        for i in range(self.deck_cursor, stored_count):
            c = self._get_nibble(_Mem.DECK_CARDS, i)
            if not removed and c == card_code:
                removed = True
                continue
            remaining.append(c)
        if removed:
            self._store_deck_cards(remaining)

    def draw_next_machine_card(self) -> int:
        """Pioche la prochaine carte du paquet Machine (ou CARD_NONE si paquet épuisé)."""
        if self.deck_cursor >= self.deck_len:
            return CARD_NONE
        assert self.deck_cursor < DECK_SLOTS_CAPACITY
        c = self._get_nibble(_Mem.DECK_CARDS, self.deck_cursor)
        self.deck_cursor += 1
        return c

    def get_player_hand(self, seat: int) -> tuple[int, int, int, int, int]:
        """Retourne (card_code, d1, d2, lecture_m, bound_tactique) pour seat."""
        assert 0 <= seat < self.cfg.n_players
        pos = _Mem.PLAYER_HANDS + seat * 2
        u16 = self._buf[pos] | (self._buf[pos + 1] << 8)
        card = u16 & 0x0F
        d1 = (u16 >> 4) & 0x07
        d2 = (u16 >> 7) & 0x07
        lecture_m = (u16 >> 10) & 0x07
        bound_t = (u16 >> 13) & 0x07
        return card, d1, d2, lecture_m, bound_t

    def set_player_hand(
        self,
        seat: int,
        card: int,
        d1: int = 0,
        d2: int = 0,
        lecture_m: int = 0,
        bound_tactique: int = 0,
    ) -> None:
        assert 0 <= seat < self.cfg.n_players
        assert 0 <= card <= 15
        assert 0 <= d1 <= 6 and 0 <= d2 <= 6 and 0 <= lecture_m <= 6
        assert 0 <= bound_tactique <= 6
        u16 = (
            card
            | (d1 << 4)
            | (d2 << 7)
            | (lecture_m << 10)
            | (bound_tactique << 13)
        )
        pos = _Mem.PLAYER_HANDS + seat * 2
        self._buf[pos] = u16 & 0xFF
        self._buf[pos + 1] = (u16 >> 8) & 0xFF

    # ------------------------------------------------------------------
    # Modificateurs transitoires de tour (remis à zéro systématiquement en 6.2)
    # ------------------------------------------------------------------
    def get_machine_turn_stats(self, ray: int, m_type: int) -> tuple[int, bool, bool]:
        """Retourne (damaged_parcels_count 0..3, gained_red, attacked_this_turn)."""
        idx = self._machine_idx(ray, m_type)
        nib = self._get_nibble(_Mem.TRANS_MACHINE_STATS, idx)
        return nib & 0x03, bool(nib & 0x04), bool(nib & 0x08)

    def set_machine_turn_stats(
        self, ray: int, m_type: int, damaged_count: int, gained_red: bool, attacked: bool
    ) -> None:
        idx = self._machine_idx(ray, m_type)
        capped_dmg = min(3, max(0, damaged_count))
        nib = capped_dmg | (0x04 if gained_red else 0) | (0x08 if attacked else 0)
        self._set_nibble(_Mem.TRANS_MACHINE_STATS, idx, nib)

    def has_reve_opened_this_turn(self, r_num: int) -> bool:
        assert 1 <= r_num <= 10
        mask = self._buf[_Mem.TRANS_REVE_OPENED_MASK] | (
            self._buf[_Mem.TRANS_REVE_OPENED_MASK + 1] << 8
        )
        return bool(mask & (1 << (r_num - 1)))

    def mark_reve_opened_this_turn(self, r_num: int) -> None:
        assert 1 <= r_num <= 10
        mask = self._buf[_Mem.TRANS_REVE_OPENED_MASK] | (
            self._buf[_Mem.TRANS_REVE_OPENED_MASK + 1] << 8
        )
        mask |= 1 << (r_num - 1)
        self._buf[_Mem.TRANS_REVE_OPENED_MASK] = mask & 0xFF
        self._buf[_Mem.TRANS_REVE_OPENED_MASK + 1] = (mask >> 8) & 0xFF

    def get_step2_pass_state(self) -> tuple[int, bool]:
        """Retourne (pass_idx 0..15, moved_in_pass)."""
        b = self._buf[_Mem.TRANS_STEP2_STATE]
        return b & 0x0F, bool(b & 0x10)

    def set_step2_pass_state(self, pass_idx: int, moved_in_pass: bool) -> None:
        assert 0 <= pass_idx <= 15
        self._buf[_Mem.TRANS_STEP2_STATE] = pass_idx | (0x10 if moved_in_pass else 0)

    def get_global_mod_seuil_turn(self) -> int:
        """Modificateur global transitoire de Seuil de Parade pour le tour (-64..+63)."""
        raw = self._buf[_Mem.TRANS_GLOBAL_SEUIL_MOD]
        return raw - 256 if raw >= 128 else raw

    def add_global_mod_seuil_turn(self, delta: int) -> None:
        """Ajoute un bonus/malus transitoire global au Seuil de Parade pour le tour."""
        cur = self.get_global_mod_seuil_turn() + delta
        assert -64 <= cur <= 63
        self._buf[_Mem.TRANS_GLOBAL_SEUIL_MOD] = cur & 0xFF

    def get_machine_seuil_mod_turn(self, ray: int, m_type: int) -> int:
        """Modificateur transitoire de Seuil porté par une machine pour le tour (-8..+7)."""
        idx = self._machine_idx(ray, m_type)
        nib = self._get_nibble(_Mem.TRANS_MACHINE_SEUIL_MOD, idx)
        return nib - 16 if nib >= 8 else nib

    def add_machine_seuil_mod_turn(self, ray: int, m_type: int, delta: int) -> None:
        """Ajoute un bonus/malus transitoire de Seuil sur une machine (ex: G1 B Face 1, R10 A)."""
        idx = self._machine_idx(ray, m_type)
        cur = max(-8, min(7, self.get_machine_seuil_mod_turn(ray, m_type) + delta))
        self._set_nibble(_Mem.TRANS_MACHINE_SEUIL_MOD, idx, cur & 0x0F)

    def get_parcel_seuil_mod_turn(self, r: int, p: int) -> int:
        """Modificateur transitoire de Seuil sur la parcelle (r, p) pour le tour (-64..+63)."""
        idx = self._assert_active_parcel(r, p)
        raw = self._buf[_Mem.TRANS_PARCEL_SEUIL_MOD + idx]
        return raw - 256 if raw >= 128 else raw

    def add_parcel_seuil_mod_turn(self, r: int, p: int, delta: int) -> None:
        """Ajoute un bonus/malus transitoire de Seuil sur la parcelle (r, p) (ex: G4 A, G11 A, R9 A)."""
        idx = self._assert_active_parcel(r, p)
        cur = max(-64, min(63, self.get_parcel_seuil_mod_turn(r, p) + delta))
        self._buf[_Mem.TRANS_PARCEL_SEUIL_MOD + idx] = cur & 0xFF

    def get_parcel_flags_turn(self, r: int, p: int) -> int:
        """Retourne le bitmask transitoire de la parcelle (r, p) pour le tour."""
        idx = self._assert_active_parcel(r, p)
        return self._buf[_Mem.TRANS_PARCEL_FLAGS + idx]

    def has_parcel_flag_turn(self, r: int, p: int, flag_mask: int) -> bool:
        """Vérifie si le drapeau transitoire `flag_mask` est actif sur (r, p) ce tour."""
        return bool(self.get_parcel_flags_turn(r, p) & flag_mask)

    def set_parcel_flag_turn(self, r: int, p: int, flag_mask: int, active: bool = True) -> None:
        """Active ou désactive un drapeau transitoire de parcelle (SANCTUAIRE_SOUCHE, MATAMATA, etc.)."""
        idx = self._assert_active_parcel(r, p)
        assert 0 <= flag_mask <= 0xFF
        cur = self._buf[_Mem.TRANS_PARCEL_FLAGS + idx]
        self._buf[_Mem.TRANS_PARCEL_FLAGS + idx] = (
            (cur | flag_mask) if active else (cur & ~flag_mask)
        )

    def has_used_once_per_turn(self, lock_idx: int) -> bool:
        """Vérifie si le verrou 'une fois par tour' `lock_idx` (0..63) a déjà servi ce tour."""
        assert 0 <= lock_idx < 64
        byte_pos = _Mem.TRANS_ONCE_PER_TURN + (lock_idx >> 3)
        return bool(self._buf[byte_pos] & (1 << (lock_idx & 7)))

    def mark_used_once_per_turn(self, lock_idx: int) -> None:
        """Verrouille l'index `lock_idx` (0..63) pour le reste du tour."""
        assert 0 <= lock_idx < 64
        byte_pos = _Mem.TRANS_ONCE_PER_TURN + (lock_idx >> 3)
        self._buf[byte_pos] |= 1 << (lock_idx & 7)

    def has_slot_used_once_per_turn(self, slot_id: str) -> bool:
        """Vérifie si l'emplacement `slot_id` (ex: 'G3', 'R4', 'M1') a utilisé son quota 1/tour."""
        return self.has_used_once_per_turn(slot_id_to_once_index(slot_id))

    def mark_slot_used_once_per_turn(self, slot_id: str) -> None:
        """Marque l'emplacement `slot_id` comme ayant utilisé son effet limité à 1 fois par tour."""
        self.mark_used_once_per_turn(slot_id_to_once_index(slot_id))

    def get_pending_apprentissage_at_rank(self, rank_0_5: int) -> int:
        """Delta d'Apprentissage mémorisé sur le rang `rank_0_5` pour application en 6.1."""
        assert 0 <= rank_0_5 < TRACK_LEN
        raw = self._buf[_Mem.TRANS_PENDING_APPRENTISSAGE + rank_0_5]
        return raw - 256 if raw >= 128 else raw

    def add_pending_apprentissage_at_rank(self, rank_0_5: int, delta: int) -> None:
        """Mémorise un ajustement d'Apprentissage sur `rank_0_5` appliqué en 6.1 avant Bug."""
        assert 0 <= rank_0_5 < TRACK_LEN
        cur = max(-64, min(63, self.get_pending_apprentissage_at_rank(rank_0_5) + delta))
        self._buf[_Mem.TRANS_PENDING_APPRENTISSAGE + rank_0_5] = cur & 0xFF

    def get_pending_voluntary_app_reduction(self) -> tuple[int, int]:
        """Retourne (nb_retraits_volontaires_restants, seat_decideur) mémorisés pour 6.1."""
        b = self._buf[_Mem.TRANS_VOLUNTARY_APP_COUNTER]
        return b & 0x1F, (b >> 5) & 0x07

    def add_pending_voluntary_app_reduction(self, count: int, decideur_seat: int) -> None:
        """Mémorise +count retraits volontaires d'Apprentissage en 6.1 avant Bug (ex: G10 A, R2 A)."""
        assert count >= 0 and 0 <= decideur_seat < self.cfg.n_players
        cur_cnt, _ = self.get_pending_voluntary_app_reduction()
        new_cnt = min(31, cur_cnt + count)
        self._buf[_Mem.TRANS_VOLUNTARY_APP_COUNTER] = new_cnt | (decideur_seat << 5)

    def clear_pending_voluntary_app_reduction(self, remaining: int = 0, seat: int = 0) -> None:
        """Met à jour le compteur résiduel de retraits volontaires d'Apprentissage en 6.1."""
        assert 0 <= remaining <= 31 and 0 <= seat < MAX_N
        self._buf[_Mem.TRANS_VOLUNTARY_APP_COUNTER] = remaining | (seat << 5)

    def reset_transient_modifiers(self) -> None:
        """Remet intégralement à zéro la plage dédiée de modificateurs transitoires en 6.2."""
        self._buf[_Mem.TRANSIENT_START : _Mem.TRANSIENT_END] = _ZERO_TRANSIENT_BYTES

    def cleanup_end_of_turn_6_2(self) -> None:
        """Ménage rapide de fin de tour 6.2 par tranches mémoire contiguës."""
        buf = self._buf
        buf[_Mem.TACTIQUES_APPRENTISSAGE : _Mem.TACTIQUES_APPRENTISSAGE + TRACK_LEN] = _ZERO_6_BYTES
        for c_off in range(TRACK_LEN):
            buf[_Mem.GARDIENS_PISTE + c_off] &= ~0x20  # Effacer bit utilisé
        buf[_Mem.TRIGGERS_LIT] = 0
        for m_off in range(NUM_NIDS):
            buf[_Mem.NIDS_STATE + m_off] &= 0x7F  # Effacer bit activé ce tour
        buf[_Mem.FORET_DEFENSEURS : _Mem.FORET_DEFENSEURS + 15] = _ZERO_15_BYTES
        buf[_Mem.FURTIVITE_SLOTS : _Mem.FURTIVITE_SLOTS + NUM_PARCELS] = _ZERO_30_BYTES
        buf[_Mem.PLAYER_DEF_LOC : _Mem.PLAYER_DEF_LOC + MAX_N * 2] = _ZERO_12_BYTES
        buf[_Mem.PLAYER_DEF2_DEF_MASK] = 0
        buf[_Mem.PLAYER_HANDS : _Mem.PLAYER_HANDS + MAX_N * 2] = _ZERO_12_BYTES
        if self.cfg.mode >= 2:
            for b_off in range(NUM_SYNERGY_SLOTS // 2):
                buf[_Mem.LISIERE_TILES + b_off] &= 0x33  # Conserver statuts (bits 0..1 et 4..5), RAZ constructeurs
        buf[_Mem.FLAGS] &= ~(_FLAG_PARAVENTS_OUVERTS | _FLAG_STEP2_LOCKED)
        buf[_Mem.TRANSIENT_START : _Mem.TRANSIENT_END] = _ZERO_TRANSIENT_BYTES

    # ------------------------------------------------------------------
    # Isolation stricte Public / Privé : get_observation(seat_id)
    # ------------------------------------------------------------------
    def get_observation(self, seat_id: int) -> PlayerObservation:
        """Construit une vue immuable strictement isolée sur snapshot 384B assaini en O(1)."""
        n = self.cfg.n_players
        assert 0 <= seat_id < n
        masked = bytearray(self._buf)
        # Purge totale de l'ordre futur du paquet Machine
        masked[_Mem.DECK_CARDS : _Mem.DECK_CARDS + (DECK_SLOTS_CAPACITY // 2)] = _ZERO_DECK_BYTES
        # Purge stricte des mains et dés adverses tant que les paravents sont fermés
        if not (masked[_Mem.FLAGS] & _FLAG_PARAVENTS_OUVERTS):
            for s in range(MAX_N):
                if s == seat_id:
                    continue
                hp = _Mem.PLAYER_HANDS + s * 2
                has_c = (masked[hp] & 0x0F) != CARD_NONE and s < n
                masked[hp] = _MASKED_HAS_CARD_SENTINEL if has_c else 0
                masked[hp + 1] = 0
        return PlayerObservation(seat_id, self.cfg, bytes(masked))
