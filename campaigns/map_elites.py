"""Optimisation Palier 4 : Sequential Halving final, MAP-Elites 2D, CVaR_20% & Shapley d'ordre 2.

Module 100 % stdlib Python pure (compatible PyPy 3.11 workers Cloud & CPython 3.12 local).
Implémente :
- Phase A : Sequential Halving des 128 châssis sur Mode 3 référence + sets Mode 4 stratifiés.
- Phase B : Archive MAP-Elites 2D (Axe X = complexité cognitive, Axe Y = entropie de Shannon des 3 fins),
  fitness intra-cellule = CVaR_20% inter-tables circulaires (N=3..6), et opérateur de mutation 70/30
  guidé par régression ridge / valeurs marginales de Shapley d'ordre 2 sur `MATRICE_PAIRES`.
- Étape 2 : Validation croisée de profondeur stratégique (`B0 < B1 < B2 <= B3` et `Delta_V_neg > 0`).
"""

from __future__ import annotations

import json
import math
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bots.bot_b0 import play_game_b0
from bots.bot_b3_rh import play_game_b3
from bots.heuristic_engine import play_game_b1, play_game_b2
from campaigns.designs import (
    MANDATORY_6_CIRCLES,
    all_canonical_mirror_pairs,
    mirror_peuples,
    paired_mirror_blocks,
    run_micro_fork_on_config,
    sequential_halving_select,
)
from engine.primitives import CAUSE_REVE_RANG_1, CAUSE_REVEIL_GARDIENS, CAUSE_TOUR_8
from engine.rng import rand_below, rand_u64
from engine.state import MATRICE_PAIRES, PEUPLES_ORDER, GameConfig, GameState
from engine.telemetry import TelemetryTracker

__all__ = (
    "ADJACENT_16_SLOT_PAIRS",
    "CANONICAL_32_SLOTS",
    "CircularTableSpec",
    "Genome32",
    "GenomeEvaluation",
    "MapElitesArchive2D",
    "ShapleySurrogateOrder2",
    "StrategicDepthReport",
    "build_127_circular_tables",
    "build_diverse_seed_genomes",
    "build_screening_mirror_tables",
    "cognitive_complexity_x",
    "decode_genome_key",
    "encode_genome_key",
    "evaluate_genome_on_tables",
    "genome_to_tile_profiles",
    "load_catalog_slot_profiles",
    "load_mode3_reference_genome",
    "mutate_genome_shapley_70_30",
    "run_map_elites_island",
    "run_phase_a_chassis_halving",
    "shannon_entropy_3_ends",
    "tile_profiles_to_genome",
    "validate_strategic_depth",
)

ROOT: Path = Path(__file__).resolve().parent.parent
SPEC_BUNDLE_PATH: Path = ROOT / "data" / "spec_bundle_v5_3_1.json"
MODE3_REF_PATH: Path = ROOT / "engine" / "effects" / "mode3_reference.json"

Genome32 = tuple[str, ...]

CANONICAL_32_SLOTS: tuple[str, ...] = (
    *[f"G{i}" for i in range(1, 16)],
    *[f"R{i}" for i in range(1, 11)],
    *[f"M{i}" for i in range(1, 6)],
    "SLOT_BUG_CERVEAU",
    "SLOT_COLONISATION_GARDIENS",
)
_SLOT_TO_INDEX: dict[str, int] = {s: idx for idx, s in enumerate(CANONICAL_32_SLOTS)}

# Les 15 paires adjacentes de lisière (MATRICE_PAIRES) + la paire des 2 pistes de Migration = 16 paires
def _build_adjacent_16_pairs() -> tuple[tuple[str, str], ...]:
    seen: set[tuple[str, str]] = set()
    ordered: list[tuple[str, str]] = []
    for k in sorted(MATRICE_PAIRES.keys()):
        a, b = MATRICE_PAIRES[k]
        pair = (a, b) if _SLOT_TO_INDEX[a] < _SLOT_TO_INDEX[b] else (b, a)
        if pair not in seen:
            seen.add(pair)
            ordered.append(pair)
    ordered.sort(key=lambda ab: (_SLOT_TO_INDEX[ab[0]], _SLOT_TO_INDEX[ab[1]]))
    ordered.append(("SLOT_BUG_CERVEAU", "SLOT_COLONISATION_GARDIENS"))
    assert len(ordered) == 16
    return tuple(ordered)


ADJACENT_16_SLOT_PAIRS: tuple[tuple[str, str], ...] = _build_adjacent_16_pairs()
_PARTNER_SLOT: dict[str, str] = {}
for _sa, _sb in ADJACENT_16_SLOT_PAIRS:
    _PARTNER_SLOT[_sa] = _sb
    _PARTNER_SLOT[_sb] = _sa

_CATALOG_CACHE: dict[str, tuple[str, ...]] | None = None
_SRC_MAP_ELITES: int = 44


def load_catalog_slot_profiles(bundle_path: Path | None = None) -> dict[str, tuple[str, ...]]:
    """Charge la carte ordonnée `{slot_id: ('A', 'B', ...)}` des 32 emplacements (100 profils)."""
    global _CATALOG_CACHE
    if bundle_path is None and _CATALOG_CACHE is not None:
        return _CATALOG_CACHE

    target = bundle_path if bundle_path is not None else SPEC_BUNDLE_PATH
    raw = json.loads(target.read_text(encoding="utf-8"))
    cat = raw["catalogue_tuiles"]
    out: dict[str, tuple[str, ...]] = {}
    total_profiles = 0
    for slot_id in CANONICAL_32_SLOTS:
        profs = tuple(sorted(str(k) for k in cat[slot_id]["profils"]))
        assert len(profs) >= 2
        out[slot_id] = profs
        total_profiles += len(profs)
    assert len(out) == 32 and total_profiles == 100
    if bundle_path is None:
        _CATALOG_CACHE = out
    return out


def load_mode3_reference_genome(ref_path: Path | None = None) -> Genome32:
    """Charge le génome de référence Mode 3 (32 profils épurés) depuis `mode3_reference.json`."""
    target = ref_path if ref_path is not None else MODE3_REF_PATH
    raw = json.loads(target.read_text(encoding="utf-8"))
    sels = raw["selections"]
    return tuple(str(sels[slot_id]["profile"]) for slot_id in CANONICAL_32_SLOTS)


def genome_to_tile_profiles(genome: Genome32) -> tuple[tuple[str, str], ...]:
    """Convertit un `Genome32` en tuple `((slot_id, profile), ...)` pour `GameConfig`."""
    assert len(genome) == 32
    return tuple(zip(CANONICAL_32_SLOTS, genome, strict=True))


def tile_profiles_to_genome(tile_profiles: Sequence[tuple[str, str]]) -> Genome32:
    """Convertit une séquence `(slot_id, profile)` complète en `Genome32` canonique."""
    mapping = {str(s): str(p) for s, p in tile_profiles}
    return tuple(mapping[slot_id] for slot_id in CANONICAL_32_SLOTS)


def encode_genome_key(genome: Genome32) -> str:
    """Sérialise de façon compacte et bijective un `Genome32` (ex: `'A.A.A.A.B...'`)."""
    assert len(genome) == 32
    return ".".join(genome)


def decode_genome_key(key: str) -> Genome32:
    """Désérialise une clé `encode_genome_key` en `Genome32`."""
    parts = tuple(p.strip() for p in key.split(".") if p.strip())
    assert len(parts) == 32
    return parts


# ---------------------------------------------------------------------------
# Tables circulaires (suite stratifiée 127 tables & criblage miroir rapide)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class CircularTableSpec:
    """Spécification d'une table circulaire orientée et de son partenaire miroir CRN."""

    table_idx: int
    n_players: int
    table_id: str
    peuples: tuple[str, ...]
    mirror_id: str
    mirror_pair_id: str
    crn_pair_group: int
    is_mandatory: bool


def _canon_rot(peuples: tuple[str, ...]) -> tuple[str, ...]:
    rmap = {code: idx for idx, code in enumerate(PEUPLES_ORDER)}
    best = min(range(len(peuples)), key=lambda i: rmap[peuples[i]])
    return peuples[best:] + peuples[:best]


def build_127_circular_tables() -> tuple[CircularTableSpec, ...]:
    """Construit le référentiel déterministe exact de 127 tables circulaires (N in {3, 4, 5, 6}).

    Répartition équilibrée en paires miroirs :
    - N = 3 : 13 paires = 26 tables
    - N = 4 : 17 paires = 34 tables
    - N = 5 : 17 paires = 34 tables
    - N = 6 : 16 paires + 1 ancre = 33 tables
    Total = 127 tables circulaires, incluant 100 % des 6 cercles obligatoires et leurs miroirs.
    """
    quotas_by_n: dict[int, int] = {3: 26, 4: 34, 5: 34, 6: 33}
    mand_by_n: dict[int, list[tuple[str, ...]]] = {3: [], 4: [], 5: [], 6: []}
    for _, p_tup in MANDATORY_6_CIRCLES:
        mand_by_n[len(p_tup)].append(_canon_rot(p_tup))

    specs: list[CircularTableSpec] = []
    tbl_cursor = 0
    pair_cursor = 0

    for n_pl in (3, 4, 5, 6):
        target_count = quotas_by_n[n_pl]
        all_pairs = list(all_canonical_mirror_pairs(n_pl))
        chosen_pairs: list[tuple[str, tuple[str, ...], str, tuple[str, ...], bool]] = []
        used: set[tuple[str, ...]] = set()

        for m_circle in mand_by_n[n_pl]:
            mir = _canon_rot(mirror_peuples(m_circle))
            chosen_pairs.append(("-".join(m_circle), m_circle, "-".join(mir), mir, True))
            used.add(m_circle)
            used.add(mir)

        needed_pairs = (target_count + 1) // 2
        stride = max(1, len(all_pairs) // max(1, needed_pairs))
        scan = 0
        while len(chosen_pairs) < needed_pairs and scan < len(all_pairs) * 2:
            id_a, c_a, id_b, c_b = all_pairs[(scan * stride) % len(all_pairs)]
            scan += 1
            if c_a in used or c_b in used:
                continue
            chosen_pairs.append((id_a, c_a, id_b, c_b, False))
            used.add(c_a)
            used.add(c_b)

        for id_a, c_a, id_b, c_b in all_pairs:
            if len(chosen_pairs) >= needed_pairs:
                break
            if c_a in used or c_b in used:
                continue
            chosen_pairs.append((id_a, c_a, id_b, c_b, False))
            used.add(c_a)
            used.add(c_b)

        added_for_n = 0
        for id_a, c_a, id_b, c_b, is_mand in chosen_pairs:
            mp_id = f"{id_a}__{id_b}"
            if added_for_n < target_count:
                specs.append(
                    CircularTableSpec(
                        table_idx=tbl_cursor,
                        n_players=n_pl,
                        table_id=id_a,
                        peuples=c_a,
                        mirror_id=id_b,
                        mirror_pair_id=mp_id,
                        crn_pair_group=pair_cursor,
                        is_mandatory=is_mand,
                    )
                )
                tbl_cursor += 1
                added_for_n += 1
            if added_for_n < target_count:
                specs.append(
                    CircularTableSpec(
                        table_idx=tbl_cursor,
                        n_players=n_pl,
                        table_id=id_b,
                        peuples=c_b,
                        mirror_id=id_a,
                        mirror_pair_id=mp_id,
                        crn_pair_group=pair_cursor,
                        is_mandatory=is_mand,
                    )
                )
                tbl_cursor += 1
                added_for_n += 1
            pair_cursor += 1

    assert len(specs) == 127
    return tuple(specs)


def build_screening_mirror_tables(blocks_per_n: int = 2) -> tuple[CircularTableSpec, ...]:
    """Construit une suite rapide en paires miroirs couvrant 100 % des 32 emplacements."""
    blocks = paired_mirror_blocks(blocks_per_n=blocks_per_n, reps_per_side=1, exp_seed=20260404)
    specs: list[CircularTableSpec] = []
    t_idx = 0
    for blk in blocks:
        mp_id = f"{blk.circle_id}__{blk.mirror_id}"
        specs.append(
            CircularTableSpec(
                table_idx=t_idx,
                n_players=blk.n_players,
                table_id=blk.circle_id,
                peuples=blk.peuples,
                mirror_id=blk.mirror_id,
                mirror_pair_id=mp_id,
                crn_pair_group=blk.block_id,
                is_mandatory=blk.is_mandatory_cover,
            )
        )
        t_idx += 1
        specs.append(
            CircularTableSpec(
                table_idx=t_idx,
                n_players=blk.n_players,
                table_id=blk.mirror_id,
                peuples=blk.mirror_peuples,
                mirror_id=blk.circle_id,
                mirror_pair_id=mp_id,
                crn_pair_group=blk.block_id,
                is_mandatory=blk.is_mandatory_cover,
            )
        )
        t_idx += 1
    return tuple(specs)


# ---------------------------------------------------------------------------
# Descripteurs comportementaux 2D & Évaluation CVaR_20%
# ---------------------------------------------------------------------------


def shannon_entropy_3_ends(cnt_t8: int, cnt_reve: int, cnt_reveil: int) -> float:
    """Entropie de Shannon normalisée en base 3 des 3 causes de fin : H in [0, 1]."""
    total = cnt_t8 + cnt_reve + cnt_reveil
    if total <= 0:
        return 0.0
    inv_log3 = 1.0 / math.log(3.0)
    h = 0.0
    for c in (cnt_t8, cnt_reve, cnt_reveil):
        if c > 0:
            p = c / total
            h -= p * math.log(p) * inv_log3
    return max(0.0, min(1.0, h))


def cognitive_complexity_x(
    mem_debt_mean: float,
    law_stack_mean: float,
    fiddliness_mean: float,
    cascade_sweeps_mean: float,
) -> float:
    """Axe X normalisé [0, 1] de complexité cognitive agrégée (engine/telemetry.py)."""
    c_mem = min(1.0, max(0.0, mem_debt_mean / 12.0))
    c_law = min(1.0, max(0.0, law_stack_mean / 2.0))
    c_fid = min(1.0, max(0.0, (fiddliness_mean - 4.5) / 6.0))
    c_cas = min(1.0, max(0.0, cascade_sweeps_mean / 3.0))
    raw = 0.35 * c_mem + 0.35 * c_law + 0.15 * c_fid + 0.15 * c_cas
    return max(0.0, min(1.0, raw))


def _cvar_bottom(sorted_vals: list[float], alpha: float = 0.20) -> float:
    if not sorted_vals:
        return 0.0
    k = max(1, round(len(sorted_vals) * alpha))
    return sum(sorted_vals[:k]) / k


def _median_sorted(sorted_vals: list[float]) -> float:
    n = len(sorted_vals)
    if n == 0:
        return 0.0
    mid = n // 2
    if n % 2 == 1:
        return sorted_vals[mid]
    return 0.5 * (sorted_vals[mid - 1] + sorted_vals[mid])


@dataclass(frozen=True, slots=True)
class GenomeEvaluation:
    """Bilan complet d'évaluation d'un génome 32 tuiles sur une suite de tables circulaires."""

    genome_key: str
    genome: Genome32
    chassis_id: int
    n_tables: int
    n_games: int
    mean_ratio_arbres: float
    median_table_ratio: float
    cvar20_tables: float
    by_n_mean_ratio: dict[int, float]
    by_n_cvar20: dict[int, float]
    mirror_asymmetry_mean: float
    mean_tours: float
    pct_tour_8: float
    pct_reve_rang_1: float
    pct_reveil_gardiens: float
    shannon_entropy: float
    mem_debt_mean: float
    law_stack_mean: float
    law_stack_max: int
    fiddliness_mean: float
    cascade_sweeps_mean: float
    mid_combat_interrupts_mean: float
    x_cognitive: float
    cell_fitness: float
    editorial_score: float
    cpu_sec: float

    def to_record_dict(self, *, record_type: str = "MAP_ELITES_GENOME") -> dict[str, Any]:
        return {
            "record_type": record_type,
            "genome_key": self.genome_key,
            "chassis_id": self.chassis_id,
            "n_tables": self.n_tables,
            "n_games": self.n_games,
            "mean_ratio_arbres": round(self.mean_ratio_arbres, 6),
            "median_table_ratio": round(self.median_table_ratio, 6),
            "cvar20_tables": round(self.cvar20_tables, 6),
            "ratio_n3": round(self.by_n_mean_ratio.get(3, 0.0), 6),
            "ratio_n4": round(self.by_n_mean_ratio.get(4, 0.0), 6),
            "ratio_n5": round(self.by_n_mean_ratio.get(5, 0.0), 6),
            "ratio_n6": round(self.by_n_mean_ratio.get(6, 0.0), 6),
            "cvar20_n3": round(self.by_n_cvar20.get(3, 0.0), 6),
            "cvar20_n4": round(self.by_n_cvar20.get(4, 0.0), 6),
            "cvar20_n5": round(self.by_n_cvar20.get(5, 0.0), 6),
            "cvar20_n6": round(self.by_n_cvar20.get(6, 0.0), 6),
            "mirror_asymmetry_mean": round(self.mirror_asymmetry_mean, 6),
            "mean_tours": round(self.mean_tours, 4),
            "pct_tour_8": round(self.pct_tour_8, 3),
            "pct_reve_rang_1": round(self.pct_reve_rang_1, 3),
            "pct_reveil_gardiens": round(self.pct_reveil_gardiens, 3),
            "shannon_entropy": round(self.shannon_entropy, 6),
            "mem_debt_mean": round(self.mem_debt_mean, 4),
            "law_stack_mean": round(self.law_stack_mean, 5),
            "law_stack_max": self.law_stack_max,
            "fiddliness_mean": round(self.fiddliness_mean, 4),
            "cascade_sweeps_mean": round(self.cascade_sweeps_mean, 4),
            "mid_combat_interrupts_mean": round(self.mid_combat_interrupts_mean, 4),
            "x_cognitive": round(self.x_cognitive, 6),
            "cell_fitness": round(self.cell_fitness, 6),
            "editorial_score": round(self.editorial_score, 6),
            "cell_cpu_sec": round(self.cpu_sec, 4),
        }


def _make_mode4_cfg(
    chassis_id: int,
    *,
    n_players: int,
    peuples: tuple[str, ...],
    tile_profiles: tuple[tuple[str, str], ...],
    exp_seed: int,
    rep_id: int,
    coordonnateur_initial: int,
    max_revision_passes: int,
) -> GameConfig:
    base = GameConfig.from_chassis_index(
        chassis_id,
        n_players=n_players,
        mode=4,
        peuples=peuples,
        exp_seed=exp_seed,
        rep_id=rep_id,
        coordonnateur_initial=coordonnateur_initial,
        max_revision_passes=max_revision_passes,
    )
    return GameConfig(
        n_players=base.n_players,
        mode=4,
        peuples=base.peuples,
        exp_seed=base.exp_seed,
        rep_id=base.rep_id,
        coordonnateur_initial=base.coordonnateur_initial,
        max_revision_passes=base.max_revision_passes,
        p_max=base.p_max,
        regle_ouverture_reve_multiple=base.regle_ouverture_reve_multiple,
        offset_seuil_parade=base.offset_seuil_parade,
        mise_en_place_tactiques=base.mise_en_place_tactiques,
        declenchement_fin_de_piste=base.declenchement_fin_de_piste,
        role_abatteuse_fin_de_piste=base.role_abatteuse_fin_de_piste,
        synergie_binome_machines=base.synergie_binome_machines,
        tile_profiles=tile_profiles,
    )


def evaluate_genome_on_tables(
    chassis_id: int,
    genome: Genome32,
    tables: Sequence[CircularTableSpec],
    *,
    reps_per_table: int = 1,
    exp_seed: int = 20264001,
    k_max_passes: int = 3,
    max_steps: int = 2000,
) -> GenomeEvaluation:
    """Évalue un génome 32 profils avec B2 (K_max=3) sur semences CRN appariées par paire miroir."""
    assert len(tables) >= 1 and reps_per_table >= 1
    t0 = time.perf_counter()
    tile_profiles = genome_to_tile_profiles(genome)

    table_ratios: list[float] = []
    ratios_by_n: dict[int, list[float]] = {3: [], 4: [], 5: [], 6: []}
    ratio_by_table_id: dict[str, float] = {}

    total_games = 0
    sum_ratio_all = 0.0
    sum_tours = 0
    cnt_t8 = 0
    cnt_reve = 0
    cnt_reveil = 0

    sum_mem = 0
    sum_law_m = 0.0
    max_law_mx = 0
    sum_fidd = 0.0
    sum_casc = 0
    sum_mid = 0

    for tbl in tables:
        n_pl = tbl.n_players
        t_sum = 0.0
        # Semence CRN identique pour les 2 orientations d'une paire miroir (crn_pair_group)
        base_rep = tbl.crn_pair_group * max(8, reps_per_table * 2)
        for r_off in range(reps_per_table):
            cfg = _make_mode4_cfg(
                chassis_id,
                n_players=n_pl,
                peuples=tbl.peuples,
                tile_profiles=tile_profiles,
                exp_seed=exp_seed,
                rep_id=base_rep + r_off,
                coordonnateur_initial=r_off % n_pl,
                max_revision_passes=k_max_passes,
            )
            trk = TelemetryTracker()
            res = play_game_b2(
                GameState(cfg),
                k_max_passes=k_max_passes,
                max_steps=max_steps,
                chassis_id=chassis_id,
                telemetry=trk,
            )
            total_games += 1
            rt = res.ratio_arbres
            t_sum += rt
            sum_ratio_all += rt
            sum_tours += res.tour_fin
            if res.cause_fin == CAUSE_TOUR_8:
                cnt_t8 += 1
            elif res.cause_fin == CAUSE_REVE_RANG_1:
                cnt_reve += 1
            elif res.cause_fin == CAUSE_REVEIL_GARDIENS:
                cnt_reveil += 1

            ts = trk.summary()
            sum_mem += ts.mem_debt_score
            sum_law_m += ts.law_stack_mean
            max_law_mx = max(max_law_mx, ts.law_stack_max)
            sum_fidd += ts.fiddliness_ratio
            sum_casc += ts.cascade_sweeps
            sum_mid += ts.mid_combat_interrupts

        t_mean = t_sum / reps_per_table
        table_ratios.append(t_mean)
        ratios_by_n.setdefault(n_pl, []).append(t_mean)
        ratio_by_table_id[tbl.table_id] = t_mean

    sorted_tbl = sorted(table_ratios)
    mean_rt = sum_ratio_all / max(1, total_games)
    med_rt = _median_sorted(sorted_tbl)
    cvar20 = _cvar_bottom(sorted_tbl, 0.20)

    by_n_mean: dict[int, float] = {}
    by_n_cvar: dict[int, float] = {}
    for n_pl, vals in ratios_by_n.items():
        if vals:
            s_v = sorted(vals)
            by_n_mean[n_pl] = sum(s_v) / len(s_v)
            by_n_cvar[n_pl] = _cvar_bottom(s_v, 0.20)

    # Asymétrie entre paires miroirs présentes dans l'échantillon
    seen_mp: set[str] = set()
    mirror_gaps: list[float] = []
    for tbl in tables:
        if tbl.mirror_pair_id in seen_mp:
            continue
        if tbl.mirror_id in ratio_by_table_id:
            seen_mp.add(tbl.mirror_pair_id)
            mirror_gaps.append(
                abs(ratio_by_table_id[tbl.table_id] - ratio_by_table_id[tbl.mirror_id])
            )
    mirror_asym = (sum(mirror_gaps) / len(mirror_gaps)) if mirror_gaps else 0.0

    entropy_h = shannon_entropy_3_ends(cnt_t8, cnt_reve, cnt_reveil)
    mem_m = sum_mem / max(1, total_games)
    law_m = sum_law_m / max(1, total_games)
    fidd_m = sum_fidd / max(1, total_games)
    casc_m = sum_casc / max(1, total_games)
    mid_m = sum_mid / max(1, total_games)
    x_cog = cognitive_complexity_x(mem_m, law_m, fidd_m, casc_m)

    # Fitness intra-cellule MAP-Elites : CVaR_20% pénalisée hors bande cible [0.52, 0.74],
    # écart inter-N excessif et asymétrie miroir excessive
    if mean_rt < 0.52:
        band_pen = 0.80 * (0.52 - mean_rt)
    elif mean_rt > 0.74:
        band_pen = 0.80 * (mean_rt - 0.74)
    else:
        band_pen = 0.0

    n_means_present = list(by_n_mean.values())
    n_spread = (max(n_means_present) - min(n_means_present)) if len(n_means_present) >= 2 else 0.0
    spread_pen = 0.35 * max(0.0, n_spread - 0.22)
    mir_pen = 0.40 * max(0.0, mirror_asym - 0.08)

    cell_fit = cvar20 - band_pen - spread_pen - mir_pen
    # Score éditorial global sur le front de Pareto (robustesse CVaR_20% + richesse H - taxe cognitive)
    ed_score = cell_fit + 0.18 * entropy_h - 0.16 * x_cog

    cpu_s = time.perf_counter() - t0
    g_denom = max(1, total_games)
    return GenomeEvaluation(
        genome_key=encode_genome_key(genome),
        genome=genome,
        chassis_id=chassis_id,
        n_tables=len(tables),
        n_games=total_games,
        mean_ratio_arbres=mean_rt,
        median_table_ratio=med_rt,
        cvar20_tables=cvar20,
        by_n_mean_ratio=by_n_mean,
        by_n_cvar20=by_n_cvar,
        mirror_asymmetry_mean=mirror_asym,
        mean_tours=sum_tours / g_denom,
        pct_tour_8=cnt_t8 * 100.0 / g_denom,
        pct_reve_rang_1=cnt_reve * 100.0 / g_denom,
        pct_reveil_gardiens=cnt_reveil * 100.0 / g_denom,
        shannon_entropy=entropy_h,
        mem_debt_mean=mem_m,
        law_stack_mean=law_m,
        law_stack_max=max_law_mx,
        fiddliness_mean=fidd_m,
        cascade_sweeps_mean=casc_m,
        mid_combat_interrupts_mean=mid_m,
        x_cognitive=x_cog,
        cell_fitness=cell_fit,
        editorial_score=ed_score,
        cpu_sec=cpu_s,
    )


# ---------------------------------------------------------------------------
# Modèle de substitution de Shapley d'ordre 2 (Ridge CG stdlib pure) & Mutation 70/30
# ---------------------------------------------------------------------------


class ShapleySurrogateOrder2:
    """Estimateur de Shapley d'ordre 2 (effets principaux + interactions `MATRICE_PAIRES`).

    Ajuste par moindres carrés régularisés (gradient conjugué creux 100 % stdlib) :
      f(g) = w0 + sum_s phi_i(s, g_s) + sum_{(s1, s2) in ADJACENT_16_SLOT_PAIRS} phi_ij((s1, g_s1), (s2, g_s2))
    avec centrage ANOVA exact par emplacement et par paire adjacente.
    """

    def __init__(self, ridge_lambda: float = 2.5) -> None:
        self.ridge_lambda: float = ridge_lambda
        self.slot_profiles: dict[str, tuple[str, ...]] = load_catalog_slot_profiles()

        self.main_feat_idx: dict[tuple[str, str], int] = {}
        self.pair_feat_idx: dict[tuple[str, str, str, str], int] = {}
        cursor = 0
        for s in CANONICAL_32_SLOTS:
            for p in self.slot_profiles[s]:
                self.main_feat_idx[(s, p)] = cursor
                cursor += 1
        for sa, sb in ADJACENT_16_SLOT_PAIRS:
            for pa in self.slot_profiles[sa]:
                for pb in self.slot_profiles[sb]:
                    self.pair_feat_idx[(sa, pa, sb, pb)] = cursor
                    cursor += 1
        self.n_features: int = cursor

        self.intercept: float = 0.0
        self.phi_main: dict[tuple[str, str], float] = dict.fromkeys(self.main_feat_idx, 0.0)
        self.phi_pair: dict[tuple[str, str, str, str], float] = dict.fromkeys(
            self.pair_feat_idx, 0.0
        )
        self.counts_main: dict[tuple[str, str], int] = dict.fromkeys(self.main_feat_idx, 0)
        self.n_samples: int = 0
        self.is_fitted: bool = False

    def _encode_sparse(self, genome: Genome32) -> tuple[int, ...]:
        idxs: list[int] = []
        for s_i, s in enumerate(CANONICAL_32_SLOTS):
            idxs.append(self.main_feat_idx[(s, genome[s_i])])
        for sa, sb in ADJACENT_16_SLOT_PAIRS:
            pa = genome[_SLOT_TO_INDEX[sa]]
            pb = genome[_SLOT_TO_INDEX[sb]]
            idxs.append(self.pair_feat_idx[(sa, pa, sb, pb)])
        return tuple(idxs)

    def fit(self, genomes: Sequence[Genome32], targets: Sequence[float]) -> None:
        """Ajuste les valeurs marginales de Shapley phi_i et d'interaction phi_ij sur l'historique."""
        m = len(genomes)
        assert m == len(targets)
        self.n_samples = m
        for key in self.counts_main:
            self.counts_main[key] = 0
        for g in genomes:
            for s_i, s in enumerate(CANONICAL_32_SLOTS):
                self.counts_main[(s, g[s_i])] += 1

        if m < 4:
            self.is_fitted = False
            return

        mean_y = sum(targets) / m
        y_centered = [y - mean_y for y in targets]
        rows = [self._encode_sparse(g) for g in genomes]
        n_f = self.n_features
        lam = self.ridge_lambda

        # Résolution de (X^T X + lam * I) w = X^T y_centered par Gradient Conjugué creux
        b = [0.0] * n_f
        for r_idxs, yc in zip(rows, y_centered, strict=True):
            for fi in r_idxs:
                b[fi] += yc

        def _matvec(vec: list[float]) -> list[float]:
            out = [lam * v for v in vec]
            for r_idxs in rows:
                dot = 0.0
                for fi in r_idxs:
                    dot += vec[fi]
                for fi in r_idxs:
                    out[fi] += dot
            return out

        w = [0.0] * n_f
        r = list(b)
        p_vec = list(r)
        rs_old = sum(rv * rv for rv in r)
        if rs_old > 1e-15:
            for _ in range(32):
                ap = _matvec(p_vec)
                p_ap = sum(pv * apv for pv, apv in zip(p_vec, ap, strict=True))
                if p_ap <= 1e-15:
                    break
                alpha = rs_old / p_ap
                for i in range(n_f):
                    w[i] += alpha * p_vec[i]
                    r[i] -= alpha * ap[i]
                rs_new = sum(rv * rv for rv in r)
                if rs_new < 1e-14:
                    break
                beta = rs_new / rs_old
                for i in range(n_f):
                    p_vec[i] = r[i] + beta * p_vec[i]
                rs_old = rs_new

        # Projection ANOVA zéro-centrée exacte -> valeurs marginales de Shapley (référence uniforme)
        w0 = mean_y
        raw_main: dict[tuple[str, str], float] = {
            k: w[idx] for k, idx in self.main_feat_idx.items()
        }
        raw_pair: dict[tuple[str, str, str, str], float] = {
            k: w[idx] for k, idx in self.pair_feat_idx.items()
        }

        # 1. Purger les marges des termes de paires vers les effets principaux
        clean_pair: dict[tuple[str, str, str, str], float] = {}
        for sa, sb in ADJACENT_16_SLOT_PAIRS:
            pa_list = self.slot_profiles[sa]
            pb_list = self.slot_profiles[sb]
            na, nb = len(pa_list), len(pb_list)
            mean_ab = (
                sum(raw_pair[(sa, pa, sb, pb)] for pa in pa_list for pb in pb_list) / (na * nb)
            )
            mean_a = {
                pa: sum(raw_pair[(sa, pa, sb, pb)] for pb in pb_list) / nb for pa in pa_list
            }
            mean_b = {
                pb: sum(raw_pair[(sa, pa, sb, pb)] for pa in pa_list) / na for pb in pb_list
            }
            w0 += mean_ab
            for pa in pa_list:
                raw_main[(sa, pa)] += mean_a[pa] - mean_ab
            for pb in pb_list:
                raw_main[(sb, pb)] += mean_b[pb] - mean_ab
            for pa in pa_list:
                for pb in pb_list:
                    clean_pair[(sa, pa, sb, pb)] = (
                        raw_pair[(sa, pa, sb, pb)] - mean_a[pa] - mean_b[pb] + mean_ab
                    )

        # 2. Centrer chaque emplacement individuel pour obtenir phi_i(s, p)
        clean_main: dict[tuple[str, str], float] = {}
        for s in CANONICAL_32_SLOTS:
            plist = self.slot_profiles[s]
            m_s = sum(raw_main[(s, p)] for p in plist) / len(plist)
            w0 += m_s
            for p in plist:
                clean_main[(s, p)] = raw_main[(s, p)] - m_s

        self.intercept = w0
        self.phi_main = clean_main
        self.phi_pair = clean_pair
        self.is_fitted = True

    def predict(self, genome: Genome32) -> float:
        if not self.is_fitted:
            return 0.0
        val = self.intercept
        for s_i, s in enumerate(CANONICAL_32_SLOTS):
            val += self.phi_main[(s, genome[s_i])]
        for sa, sb in ADJACENT_16_SLOT_PAIRS:
            pa = genome[_SLOT_TO_INDEX[sa]]
            pb = genome[_SLOT_TO_INDEX[sb]]
            val += self.phi_pair[(sa, pa, sb, pb)]
        return val

    def marginal_replacement_gain(
        self, genome: Genome32, slot_id: str, new_profile: str, *, ucb_bonus: float = 0.015
    ) -> float:
        """Gain marginal prédit Delta_f(g; slot_id <- new_profile) + léger bonus d'exploration."""
        s_idx = _SLOT_TO_INDEX[slot_id]
        cur_prof = genome[s_idx]
        if new_profile == cur_prof:
            return -1e6

        delta = self.phi_main[(slot_id, new_profile)] - self.phi_main[(slot_id, cur_prof)]
        partner = _PARTNER_SLOT[slot_id]
        part_prof = genome[_SLOT_TO_INDEX[partner]]
        if _SLOT_TO_INDEX[slot_id] < _SLOT_TO_INDEX[partner]:
            delta += (
                self.phi_pair[(slot_id, new_profile, partner, part_prof)]
                - self.phi_pair[(slot_id, cur_prof, partner, part_prof)]
            )
        else:
            delta += (
                self.phi_pair[(partner, part_prof, slot_id, new_profile)]
                - self.phi_pair[(partner, part_prof, slot_id, cur_prof)]
            )

        cnt = self.counts_main.get((slot_id, new_profile), 0)
        return delta + ucb_bonus / math.sqrt(1.0 + cnt)

    def top_main_effects(self, limit: int = 16) -> list[dict[str, Any]]:
        ranked = sorted(self.phi_main.items(), key=lambda kv: -kv[1])
        return [
            {
                "slot": s,
                "profile": p,
                "shapley_phi": round(val, 5),
                "samples": self.counts_main.get((s, p), 0),
            }
            for (s, p), val in ranked[:limit]
        ]

    def top_pair_interactions(self, limit: int = 12) -> list[dict[str, Any]]:
        ranked = sorted(self.phi_pair.items(), key=lambda kv: -abs(kv[1]))
        return [
            {
                "pair": f"{sa}:{pa}+{sb}:{pb}",
                "shapley_interaction_phi": round(val, 5),
            }
            for (sa, pa, sb, pb), val in ranked[:limit]
        ]


def mutate_genome_shapley_70_30(
    parent: Genome32,
    surrogate: ShapleySurrogateOrder2,
    *,
    seen_keys: set[str] | None = None,
    exp_seed: int = 20264001,
    gen_idx: int = 0,
    mut_idx: int = 0,
    guided_prob: float = 0.70,
) -> tuple[Genome32, bool]:
    """Opérateur de mutation Palier 4 : 70 % guidé par Shapley d'ordre 2, 30 % uniforme sans biais.

    Retourne `(child_genome, was_shapley_guided)`.
    """
    slot_profs = surrogate.slot_profiles
    u_draw = (
        rand_u64(exp_seed, gen_idx, _SRC_MAP_ELITES, mut_idx, 0, 1) & 0xFFFFFFFF
    ) / 4294967296.0
    use_guided = surrogate.is_fitted and (u_draw < guided_prob)

    if use_guided:
        # Évaluer tous les remplacements simples et les remplacements couplés de paires voisines
        single_moves: list[tuple[float, int, str]] = []
        for s_i, s_id in enumerate(CANONICAL_32_SLOTS):
            cur_p = parent[s_i]
            for alt_p in slot_profs[s_id]:
                if alt_p == cur_p:
                    continue
                gain = surrogate.marginal_replacement_gain(parent, s_id, alt_p)
                single_moves.append((gain, s_i, alt_p))
        single_moves.sort(key=lambda x: -x[0])

        pair_moves: list[tuple[float, int, str, int, str]] = []
        for sa, sb in ADJACENT_16_SLOT_PAIRS:
            ia, ib = _SLOT_TO_INDEX[sa], _SLOT_TO_INDEX[sb]
            cur_a, cur_b = parent[ia], parent[ib]
            cur_val = (
                surrogate.phi_main[(sa, cur_a)]
                + surrogate.phi_main[(sb, cur_b)]
                + surrogate.phi_pair[(sa, cur_a, sb, cur_b)]
            )
            for pa in slot_profs[sa]:
                for pb in slot_profs[sb]:
                    if pa == cur_a and pb == cur_b:
                        continue
                    new_val = (
                        surrogate.phi_main[(sa, pa)]
                        + surrogate.phi_main[(sb, pb)]
                        + surrogate.phi_pair[(sa, pa, sb, pb)]
                    )
                    bonus = 0.012 / math.sqrt(
                        1.0 + min(surrogate.counts_main[(sa, pa)], surrogate.counts_main[(sb, pb)])
                    )
                    pair_moves.append((new_val - cur_val + bonus, ia, pa, ib, pb))
        pair_moves.sort(key=lambda x: -x[0])

        # Tester par ordre de rang stochastique dans le Top-10 des meilleures mutations Shapley
        use_pair = (
            rand_below(10, exp_seed, gen_idx, _SRC_MAP_ELITES, mut_idx, 0, 2) < 4
            and len(pair_moves) > 0
        )
        for attempt in range(12):
            work = list(parent)
            if use_pair and attempt < len(pair_moves):
                top_w = min(8, len(pair_moves))
                pick = (
                    rand_below(
                        top_w, exp_seed, gen_idx, _SRC_MAP_ELITES, mut_idx, attempt, 10 + attempt
                    )
                    if attempt == 0
                    else attempt % len(pair_moves)
                )
                _, ia, pa, ib, pb = pair_moves[pick]
                work[ia] = pa
                work[ib] = pb
            else:
                top_s = min(10, len(single_moves))
                pick1 = (
                    rand_below(
                        top_s, exp_seed, gen_idx, _SRC_MAP_ELITES, mut_idx, attempt, 30 + attempt
                    )
                    if attempt < 3
                    else attempt % len(single_moves)
                )
                _, s1, p1 = single_moves[pick1]
                work[s1] = p1
                # 50 % du temps, combiner un 2e remplacement indépendant à fort gain
                if attempt % 2 == 1 and len(single_moves) > 4:
                    pick2 = rand_below(
                        min(12, len(single_moves)),
                        exp_seed,
                        gen_idx,
                        _SRC_MAP_ELITES,
                        mut_idx,
                        attempt,
                        50 + attempt,
                    )
                    _, s2, p2 = single_moves[pick2]
                    if s2 != s1:
                        work[s2] = p2

            cand = tuple(work)
            if seen_keys is None or encode_genome_key(cand) not in seen_keys:
                return cand, True

    # Exploration uniforme sans biais (30 % nominal ou repli anti-doublon)
    cand_u: Genome32 = parent
    for fallback_try in range(16):
        work_u = list(parent)
        n_mut = 1 + rand_below(
            3, exp_seed, gen_idx, _SRC_MAP_ELITES, mut_idx, fallback_try, 100 + fallback_try
        )
        for k in range(n_mut):
            s_idx = rand_below(
                32,
                exp_seed,
                gen_idx,
                _SRC_MAP_ELITES,
                mut_idx,
                fallback_try,
                130 + fallback_try * 4 + k,
            )
            s_id = CANONICAL_32_SLOTS[s_idx]
            alts = [p for p in slot_profs[s_id] if p != work_u[s_idx]]
            p_choice = alts[
                rand_below(
                    len(alts),
                    exp_seed,
                    gen_idx,
                    _SRC_MAP_ELITES,
                    mut_idx,
                    fallback_try,
                    160 + fallback_try * 4 + k,
                )
            ]
            work_u[s_idx] = p_choice
        cand_u = tuple(work_u)
        if seen_keys is None or encode_genome_key(cand_u) not in seen_keys:
            return cand_u, False

    return cand_u, False


# ---------------------------------------------------------------------------
# Grille Archive MAP-Elites 2D & Extraction du Front de Pareto
# ---------------------------------------------------------------------------


class MapElitesArchive2D:
    """Archive MAP-Elites 2D indexée par (bin_x=complexité cognitive, bin_y=entropie des 3 fins)."""

    def __init__(self, n_bins_x: int = 8, n_bins_y: int = 8) -> None:
        assert n_bins_x >= 2 and n_bins_y >= 2
        self.n_bins_x: int = n_bins_x
        self.n_bins_y: int = n_bins_y
        self.cells: dict[tuple[int, int], GenomeEvaluation] = {}

    def coords_for(self, ev: GenomeEvaluation) -> tuple[int, int]:
        bx = min(self.n_bins_x - 1, max(0, int(ev.x_cognitive * self.n_bins_x)))
        by = min(self.n_bins_y - 1, max(0, int(ev.shannon_entropy * self.n_bins_y)))
        return bx, by

    def add(self, ev: GenomeEvaluation) -> bool:
        """Insère `ev` si sa cellule 2D est vide ou s'il améliore strictement `cell_fitness`."""
        cell_xy = self.coords_for(ev)
        incumbent = self.cells.get(cell_xy)
        if incumbent is None or ev.cell_fitness > incumbent.cell_fitness + 1e-9 or (
            abs(ev.cell_fitness - incumbent.cell_fitness) <= 1e-9
            and ev.genome_key < incumbent.genome_key
        ):
            self.cells[cell_xy] = ev
            return True
        return False

    def merge(self, other: MapElitesArchive2D) -> int:
        replaced = 0
        for ev in other.cells.values():
            if self.add(ev):
                replaced += 1
        return replaced

    def all_elites(self) -> list[GenomeEvaluation]:
        return sorted(
            self.cells.values(),
            key=lambda e: (-e.editorial_score, -e.cvar20_tables, e.genome_key),
        )

    def pareto_front(self) -> list[GenomeEvaluation]:
        """Extrait le front de Pareto non dominé maximisant (cell_fitness, shannon_entropy, -x_cognitive)."""
        elites = self.all_elites()
        front: list[GenomeEvaluation] = []
        for cand in elites:
            dominated = False
            for other in elites:
                if other.genome_key == cand.genome_key:
                    continue
                better_or_eq = (
                    other.cell_fitness >= cand.cell_fitness - 1e-9
                    and other.shannon_entropy >= cand.shannon_entropy - 1e-9
                    and other.x_cognitive <= cand.x_cognitive + 1e-9
                )
                strictly_better = (
                    other.cell_fitness > cand.cell_fitness + 1e-9
                    or other.shannon_entropy > cand.shannon_entropy + 1e-9
                    or other.x_cognitive < cand.x_cognitive - 1e-9
                )
                if better_or_eq and strictly_better:
                    dominated = True
                    break
            if not dominated:
                front.append(cand)
        return sorted(
            front,
            key=lambda e: (-e.editorial_score, -e.cvar20_tables, e.genome_key),
        )

    def select_top_finalists(self, top_k: int = 5) -> list[GenomeEvaluation]:
        """Sélectionne jusqu'à `top_k` finalistes issus prioritairement du front de Pareto."""
        front = self.pareto_front()
        chosen: list[GenomeEvaluation] = list(front[:top_k])
        seen = {e.genome_key for e in chosen}
        if len(chosen) < top_k:
            for e in self.all_elites():
                if e.genome_key not in seen:
                    chosen.append(e)
                    seen.add(e.genome_key)
                if len(chosen) >= top_k:
                    break
        return chosen


def build_diverse_seed_genomes(count: int = 8, *, exp_seed: int = 20264001) -> list[Genome32]:
    """Construit une population initiale diversifiée incluant la référence Mode 3 et les profils A/B/C/D."""
    slot_profs = load_catalog_slot_profiles()
    ref = load_mode3_reference_genome()
    seeds: list[Genome32] = [ref]
    seen = {encode_genome_key(ref)}

    # Balayage systématique des lettres B, C, D pour couvrir les 100 profils dès l'amorçage
    for target_letter in ("A", "B", "C", "D"):
        if len(seeds) >= count:
            break
        g = tuple(
            target_letter if target_letter in slot_profs[s] else ref[i]
            for i, s in enumerate(CANONICAL_32_SLOTS)
        )
        gk = encode_genome_key(g)
        if gk not in seen:
            seeds.append(g)
            seen.add(gk)

    idx = 0
    while len(seeds) < count:
        idx += 1
        g_rand = tuple(
            slot_profs[s][
                rand_below(len(slot_profs[s]), exp_seed, idx, _SRC_MAP_ELITES, 0, s_i, 7)
            ]
            for s_i, s in enumerate(CANONICAL_32_SLOTS)
        )
        gk = encode_genome_key(g_rand)
        if gk not in seen:
            seeds.append(g_rand)
            seen.add(gk)
    return seeds


def run_map_elites_island(
    chassis_id: int,
    *,
    island_id: int = 0,
    n_init: int = 8,
    n_generations: int = 8,
    batch_per_gen: int = 4,
    screening_blocks_per_n: int = 2,
    reps_screening: int = 1,
    exp_seed: int = 20264100,
    n_bins_x: int = 8,
    n_bins_y: int = 8,
) -> tuple[MapElitesArchive2D, ShapleySurrogateOrder2, list[GenomeEvaluation], dict[str, int]]:
    """Exécute une île complète MAP-Elites 2D guidée par Shapley d'ordre 2 (70 % / 30 %)."""
    island_seed = exp_seed + island_id * 10_000
    tables = build_screening_mirror_tables(blocks_per_n=screening_blocks_per_n)
    archive = MapElitesArchive2D(n_bins_x=n_bins_x, n_bins_y=n_bins_y)
    surrogate = ShapleySurrogateOrder2(ridge_lambda=2.5)

    history_genomes: list[Genome32] = []
    history_targets: list[float] = []
    all_evals: list[GenomeEvaluation] = []
    seen_keys: set[str] = set()

    guided_count = 0
    uniform_count = 0

    init_genomes = build_diverse_seed_genomes(n_init, exp_seed=island_seed)
    for g in init_genomes:
        gk = encode_genome_key(g)
        seen_keys.add(gk)
        ev = evaluate_genome_on_tables(
            chassis_id,
            g,
            tables,
            reps_per_table=reps_screening,
            exp_seed=island_seed,
        )
        archive.add(ev)
        all_evals.append(ev)
        history_genomes.append(g)
        history_targets.append(ev.cell_fitness)

    surrogate.fit(history_genomes, history_targets)

    for gen in range(1, n_generations + 1):
        elites = archive.all_elites()
        for b_idx in range(batch_per_gen):
            p_idx = rand_below(
                len(elites), island_seed, gen, _SRC_MAP_ELITES, gen, b_idx, 900
            )
            parent = elites[p_idx].genome
            child, was_guided = mutate_genome_shapley_70_30(
                parent,
                surrogate,
                seen_keys=seen_keys,
                exp_seed=island_seed,
                gen_idx=gen,
                mut_idx=b_idx,
                guided_prob=0.70,
            )
            if was_guided:
                guided_count += 1
            else:
                uniform_count += 1
            seen_keys.add(encode_genome_key(child))

            ev = evaluate_genome_on_tables(
                chassis_id,
                child,
                tables,
                reps_per_table=reps_screening,
                exp_seed=island_seed,
            )
            archive.add(ev)
            all_evals.append(ev)
            history_genomes.append(child)
            history_targets.append(ev.cell_fitness)

        surrogate.fit(history_genomes, history_targets)

    stats = {
        "evaluated_genomes": len(all_evals),
        "filled_cells": len(archive.cells),
        "guided_mutations": guided_count,
        "uniform_mutations": uniform_count,
    }
    return archive, surrogate, all_evals, stats


# ---------------------------------------------------------------------------
# Phase A — Sequential Halving final des Châssis (Mode 3 réf + sets Mode 4)
# ---------------------------------------------------------------------------


def run_phase_a_chassis_halving(
    chassis_ids: Sequence[int],
    *,
    keep_final: int = 1,
    base_reps_per_table: int = 1,
    round_offset: int = 0,
    exp_seed: int = 20264010,
) -> tuple[tuple[int, ...], list[dict[str, Any]]]:
    """Élimine par Sequential Halving les châssis hors cible sur Mode 3 réf + Mode 4 stratifié."""
    active = tuple(int(c) for c in chassis_ids)
    assert len(active) >= 1
    tables = build_screening_mirror_tables(blocks_per_n=1)  # 12 tables = 6 cercles obligatoires + miroirs
    genomes_probe = build_diverse_seed_genomes(2, exp_seed=exp_seed)  # Mode 3 réf + set alternatif B

    records: list[dict[str, Any]] = []
    round_idx = round_offset
    cur_reps = max(1, base_reps_per_table)

    while len(active) > keep_final:
        round_idx += 1
        next_k = max(keep_final, len(active) // 2)
        r_seed = exp_seed + round_idx * 40_000
        scores: dict[int, float] = {}
        staged: list[tuple[int, dict[str, Any]]] = []

        for ch_id in active:
            t_c = time.perf_counter()
            evals = [
                evaluate_genome_on_tables(
                    ch_id,
                    g,
                    tables,
                    reps_per_table=cur_reps,
                    exp_seed=r_seed + g_i * 1000,
                )
                for g_i, g in enumerate(genomes_probe)
            ]
            n_g = sum(e.n_games for e in evals)
            mean_rt = sum(e.mean_ratio_arbres for e in evals) / len(evals)
            cvar20 = sum(e.cvar20_tables for e in evals) / len(evals)
            entropy_h = sum(e.shannon_entropy for e in evals) / len(evals)
            r_n3 = sum(e.by_n_mean_ratio.get(3, mean_rt) for e in evals) / len(evals)
            r_n6 = sum(e.by_n_mean_ratio.get(6, mean_rt) for e in evals) / len(evals)

            # Cible éditoriale : survie équilibrée (~0.62), sans effondrement à N=3 ni trivialité à N=6
            collapse_n3_pen = 0.60 * max(0.0, 0.42 - r_n3)
            trivial_n6_pen = 0.60 * max(0.0, r_n6 - 0.85)
            ch_fitness = (
                (1.0 - abs(mean_rt - 0.62))
                + 0.40 * cvar20
                + 0.20 * entropy_h
                - collapse_n3_pen
                - trivial_n6_pen
            )
            scores[ch_id] = ch_fitness

            row = {
                "record_type": "PHASE_A_HALVING",
                "halving_round": round_idx,
                "chassis_id": ch_id,
                "selected_next": False,
                "n_games": n_g,
                "mean_ratio_arbres": round(mean_rt, 6),
                "cvar20_tables": round(cvar20, 6),
                "ratio_n3": round(r_n3, 6),
                "ratio_n6": round(r_n6, 6),
                "shannon_entropy": round(entropy_h, 6),
                "chassis_fitness": round(ch_fitness, 6),
                "cell_cpu_sec": round(time.perf_counter() - t_c, 4),
            }
            staged.append((ch_id, row))

        kept = set(sequential_halving_select(scores, keep_count=next_k))
        for ch_id, row in staged:
            row["selected_next"] = ch_id in kept
            records.append(row)
        active = tuple(sorted(kept, key=lambda c: (-scores[c], c)))
        cur_reps = min(4, cur_reps * 2)

    return active, records


# ---------------------------------------------------------------------------
# Étape 2 — Validation croisée de profondeur stratégique (B0 < B1 < B2 <= B3)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class StrategicDepthReport:
    """Rapport de validation croisée CRN de la hiérarchie B0 < B1 < B2 <= B3 et Delta_V_neg."""

    genome_key: str
    chassis_id: int
    n_games_per_bot: int
    n_games_b3: int
    total_games: int
    mean_b0: float
    mean_b1: float
    mean_b2_k0: float
    mean_b2_k3: float
    mean_b3: float
    delta_v_negociation_crn: float
    micro_fork_delta_v_unbiased: float
    monotone_b0_b1_b2: bool
    positive_negotiation: bool
    b3_non_degenerate: bool
    passed_all_checks: bool
    cpu_sec: float

    def to_record_dict(self) -> dict[str, Any]:
        return {
            "record_type": "PHASE_C_DEPTH_VALIDATION",
            "genome_key": self.genome_key,
            "chassis_id": self.chassis_id,
            "n_games": self.total_games,
            "n_games_per_bot": self.n_games_per_bot,
            "n_games_b3": self.n_games_b3,
            "mean_b0": round(self.mean_b0, 6),
            "mean_b1": round(self.mean_b1, 6),
            "mean_b2_k0": round(self.mean_b2_k0, 6),
            "mean_b2_k3": round(self.mean_b2_k3, 6),
            "mean_b3": round(self.mean_b3, 6),
            "delta_v_negociation_crn": round(self.delta_v_negociation_crn, 6),
            "micro_fork_delta_v_unbiased": round(self.micro_fork_delta_v_unbiased, 6),
            "monotone_b0_b1_b2": self.monotone_b0_b1_b2,
            "positive_negotiation": self.positive_negotiation,
            "b3_non_degenerate": self.b3_non_degenerate,
            "passed_all_checks": self.passed_all_checks,
            "cell_cpu_sec": round(self.cpu_sec, 4),
        }


def validate_strategic_depth(
    chassis_id: int,
    genome: Genome32,
    *,
    reps_per_table: int = 2,
    b3_reps_per_table: int = 1,
    b3_horizon_turns: int = 1,
    exp_seed: int = 20264900,
) -> StrategicDepthReport:
    """Vérifie sur semences CRN appariées B0 < B1 < B2, Delta_V_neg > 0 et stabilité B3."""
    t0 = time.perf_counter()
    tables = build_screening_mirror_tables(blocks_per_n=1)  # 12 tables miroirs couvrant N=3..6
    tile_profiles = genome_to_tile_profiles(genome)

    vals_b0: list[float] = []
    vals_b1: list[float] = []
    vals_b2_k0: list[float] = []
    vals_b2_k3: list[float] = []
    vals_b3: list[float] = []
    b3_causes: set[str] = set()
    fork_dvs: list[float] = []

    total_games_and_rollouts = 0

    for tbl in tables:
        n_pl = tbl.n_players
        base_rep = tbl.crn_pair_group * 16
        for r_off in range(reps_per_table):
            rep_id = base_rep + r_off
            coord = r_off % n_pl

            cfg_k0 = _make_mode4_cfg(
                chassis_id,
                n_players=n_pl,
                peuples=tbl.peuples,
                tile_profiles=tile_profiles,
                exp_seed=exp_seed,
                rep_id=rep_id,
                coordonnateur_initial=coord,
                max_revision_passes=0,
            )
            cfg_k3 = _make_mode4_cfg(
                chassis_id,
                n_players=n_pl,
                peuples=tbl.peuples,
                tile_profiles=tile_profiles,
                exp_seed=exp_seed,
                rep_id=rep_id,
                coordonnateur_initial=coord,
                max_revision_passes=3,
            )

            vals_b0.append(
                play_game_b0(GameState(cfg_k0), max_steps=2000, chassis_id=chassis_id).ratio_arbres
            )
            vals_b1.append(
                play_game_b1(
                    GameState(cfg_k3), k_max_passes=3, max_steps=2000, chassis_id=chassis_id
                ).ratio_arbres
            )
            vals_b2_k0.append(
                play_game_b2(
                    GameState(cfg_k0), k_max_passes=0, max_steps=2000, chassis_id=chassis_id
                ).ratio_arbres
            )
            vals_b2_k3.append(
                play_game_b2(
                    GameState(cfg_k3), k_max_passes=3, max_steps=2000, chassis_id=chassis_id
                ).ratio_arbres
            )
            total_games_and_rollouts += 4

            if r_off < b3_reps_per_table:
                res_b3 = play_game_b3(
                    GameState(cfg_k3),
                    k_max_passes=4,
                    n_determinizations=2,
                    horizon_turns=b3_horizon_turns,
                    max_candidates=3,
                    max_steps=2000,
                    chassis_id=chassis_id,
                )
                vals_b3.append(res_b3.ratio_arbres)
                b3_causes.add(res_b3.cause_fin)
                total_games_and_rollouts += 1

        # 1 ancre micro-fork sans biais par paire miroir principale
        if not tbl.table_id.endswith("_M") and tbl.table_idx % 2 == 0:
            cfg_fk = _make_mode4_cfg(
                chassis_id,
                n_players=n_pl,
                peuples=tbl.peuples,
                tile_profiles=tile_profiles,
                exp_seed=exp_seed + 50_000,
                rep_id=tbl.crn_pair_group,
                coordonnateur_initial=0,
                max_revision_passes=3,
            )
            fk = run_micro_fork_on_config(
                cfg_fk, target_tour=2, is_b2=True, n_selection_rollouts=2, n_eval_rollouts=3
            )
            if fk is not None:
                fork_dvs.append(fk.delta_v_negociation)
                total_games_and_rollouts += 13

    m_b0 = sum(vals_b0) / max(1, len(vals_b0))
    m_b1 = sum(vals_b1) / max(1, len(vals_b1))
    m_b2_0 = sum(vals_b2_k0) / max(1, len(vals_b2_k0))
    m_b2_3 = sum(vals_b2_k3) / max(1, len(vals_b2_k3))
    m_b3 = sum(vals_b3) / max(1, len(vals_b3)) if vals_b3 else m_b2_3

    dv_crn = m_b2_3 - m_b2_0
    dv_fork = sum(fork_dvs) / len(fork_dvs) if fork_dvs else dv_crn

    monotone = m_b0 < m_b1 < m_b2_3
    pos_neg = (dv_crn > 0.0) or (dv_fork > 0.0)
    # B3 non dégénéré : pas d'effondrement face à B2 et pas de martingale 100% auto-win > 0.96
    b3_ok = (m_b3 >= m_b2_3 - 0.04) and (m_b3 < 0.96) and (len(b3_causes) >= 1)

    return StrategicDepthReport(
        genome_key=encode_genome_key(genome),
        chassis_id=chassis_id,
        n_games_per_bot=len(vals_b0),
        n_games_b3=len(vals_b3),
        total_games=total_games_and_rollouts,
        mean_b0=m_b0,
        mean_b1=m_b1,
        mean_b2_k0=m_b2_0,
        mean_b2_k3=m_b2_3,
        mean_b3=m_b3,
        delta_v_negociation_crn=dv_crn,
        micro_fork_delta_v_unbiased=dv_fork,
        monotone_b0_b1_b2=monotone,
        positive_negotiation=pos_neg,
        b3_non_degenerate=b3_ok,
        passed_all_checks=(monotone and pos_neg and b3_ok),
        cpu_sec=time.perf_counter() - t0,
    )
