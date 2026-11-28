"""Agrégateurs analytiques v6.4 : Tuiles à blanc, 2×2, Moteurs, 197 Assises, Audit B3 et Ockham.

100 % stdlib Python (compatible PyPy 3.11 et CPython 3.12, zéro dépendance tierce).
Consomme directement les cellules pré-agrégées par les workers (`cell_table_rows` / DuckDB)
et produit des blocs structurés prêts pour les digests exécutifs et rapports Markdown.
"""

from __future__ import annotations

import json
import math
from typing import Any

from campaigns.modular_studies import (
    CANONICAL_15_EDGES,
    CANONICAL_30_TILES,
    get_disjoint_motors,
)
from campaigns.ockham_and_traces import (
    RemarkableGameBookmark,
    merge_v64_ockham_audits,
    select_top_remarkable_bookmarks,
    summarize_v64_ockham_audit,
)
from campaigns.stats_tools import (
    holm_bonferroni_adjust,
    paired_diff_cluster_ci95,
)

__all__ = (
    "build_assises_197_summary",
    "build_b3_degenerate_audit",
    "build_modular_study_block",
    "build_v64_forks_summary",
    "build_v64_ockham_from_rows",
    "collect_remarkable_bookmarks_from_rows",
)


def _cell_pair_key(row: dict[str, Any]) -> tuple[str, int, str, int, int]:
    """Clé CRN exacte d'appariement par grappe `(bot, n_players, table_id, exp_seed, rep_start)`."""
    return (
        str(row.get("bot", "B2")),
        int(row.get("n_players", 4)),
        str(row.get("table_id", "")),
        int(row.get("exp_seed", 0)),
        int(row.get("rep_start", 0)),
    )


def _extract_row_ratios(row: dict[str, Any]) -> tuple[float, int, list[int] | None]:
    ng = max(1, int(row.get("n_games") or 1))
    mr = float(row.get("sum_ratio_arbres") or 0.0) / float(ng)
    raw_bp = row.get("rep_ratios_bp_json")
    bp: list[int] | None = None
    if raw_bp:
        try:
            parsed = json.loads(str(raw_bp)) if not isinstance(raw_bp, list) else raw_bp
            if isinstance(parsed, list) and parsed:
                bp = [int(x) for x in parsed]
        except (ValueError, TypeError):
            bp = None
    return mr, ng, bp


def _pair_diffs_for_cluster(
    a: tuple[float, int, list[int] | None],
    b: tuple[float, int, list[int] | None],
) -> list[float]:
    ma, na, bpa = a
    mb, nb, bpb = b
    n_pair = min(na, nb)
    if bpa is not None and bpb is not None and len(bpa) >= n_pair > 0 and len(bpb) >= n_pair:
        return [(bpa[i] - bpb[i]) / 10000.0 for i in range(n_pair)]
    return [ma - mb] * max(1, n_pair)


def _format_cluster_ci_stats(stats: dict[str, Any]) -> dict[str, Any]:
    mean_d = stats.get("mean_delta")
    lo = stats.get("ci95_low")
    hi = stats.get("ci95_high")
    pv = stats.get("p_value")
    return {
        "delta": round(float(mean_d), 5) if mean_d is not None else 0.0,
        "ci95": [round(float(lo), 5), round(float(hi), 5)] if (lo is not None and hi is not None) else None,
        "p_value": round(float(pv), 6) if pv is not None else None,
        "estimable": bool(stats.get("estimable", False)),
        "n_paired_tables": int(stats.get("n_tables", 0)),
        "n_paired_games": int(stats.get("n_pairs", 0)),
    }


def _cluster_paired_diff(
    rows_a: dict[tuple[str, int, str, int, int], tuple[float, int, list[int] | None]],
    rows_b: dict[tuple[str, int, str, int, int], tuple[float, int, list[int] | None]],
) -> dict[str, Any] | None:
    """Calcule la différence CRN appariée `A - B` groupée par table avec IC 95 % CR1."""
    common = sorted(set(rows_a) & set(rows_b))
    if not common:
        return None
    diffs_by_cluster: dict[tuple[str, int, str], list[float]] = {}
    for key in common:
        cluster_k = (key[0], key[1], key[2])
        diffs_by_cluster.setdefault(cluster_k, []).extend(_pair_diffs_for_cluster(rows_a[key], rows_b[key]))
    stats = paired_diff_cluster_ci95(diffs_by_cluster)
    return _format_cluster_ci_stats(stats)


def _weighted_mean_of_variant(
    rows_v: dict[tuple[str, int, str, int, int], tuple[float, int, list[int] | None]]
) -> float | None:
    tot_w = sum(w for _, w, _ in rows_v.values())
    if tot_w <= 0:
        return None
    return round(sum(m * w for m, w, _ in rows_v.values()) / float(tot_w), 5)


def build_modular_study_block(
    cell_rows: list[dict[str, Any]],
    plan: dict[str, Any],
    *,
    preferred_bot: str | None = None,
) -> dict[str, Any] | None:
    """Construit le bloc analytique complet d'une étude `tile_study` (Solo, LOO, L_syn, 2×2, Moteurs)."""
    mod_meta = plan.get("modular_study_meta")
    if not isinstance(mod_meta, dict) or not cell_rows:
        return None

    # Si plusieurs bots sont présents, on analyse sur le bot de référence (B2 sinon le 1er)
    bots_present = sorted({str(r.get("bot", "B2")).upper() for r in cell_rows})
    ref_bot = (
        preferred_bot.upper()
        if (preferred_bot and preferred_bot.upper() in bots_present)
        else ("B2" if "B2" in bots_present else bots_present[0])
    )
    filtered_rows = [r for r in cell_rows if str(r.get("bot", "B2")).upper() == ref_bot]

    # Indexer les performances par variant_id ET par active_slots canoniques (gère les alias dédupliqués)
    by_vid: dict[str, dict[tuple[str, int, str, int, int], tuple[float, int, list[int] | None]]] = {}
    for r in filtered_rows:
        vid = str(r["variant_id"])
        ng = int(r["n_games"])
        if ng <= 0:
            continue
        by_vid.setdefault(vid, {})[_cell_pair_key(r)] = _extract_row_ratios(r)

    variants_meta = list(mod_meta.get("variants") or [])
    vid_by_active: dict[tuple[str, ...], str] = {}
    for vm in variants_meta:
        act_t = tuple(str(s) for s in vm.get("active_slots", ()))
        vid_by_active[act_t] = str(vm["variant_id"])

    def _rows_for_active(
        act_slots: tuple[str, ...],
    ) -> dict[tuple[str, int, str, int, int], tuple[float, int, list[int] | None]]:
        canon = tuple(s for s in CANONICAL_30_TILES if s in set(act_slots))
        vid = vid_by_active.get(canon)
        return by_vid.get(vid, {}) if vid is not None else {}

    rows_neutre = _rows_for_active(())
    rows_active = _rows_for_active(CANONICAL_30_TILES)

    # 1. Solo isolé, Leave-One-Out (LOO) et Levier Synergique L_syn = Delta_eco - Delta_solo
    solo_vs_eco: dict[str, dict[str, Any]] = {}
    solo_pvals: list[tuple[str, float | None]] = []
    eco_pvals: list[tuple[str, float | None]] = []

    for slot in CANONICAL_30_TILES:
        r_solo = _rows_for_active((slot,))
        r_loo = _rows_for_active(tuple(s for s in CANONICAL_30_TILES if s != slot))
        has_s = bool(r_solo and rows_neutre)
        has_e = bool(r_loo and rows_active)
        if not (has_s or has_e):
            continue
        entry: dict[str, Any] = {"slot": slot}
        if has_s:
            st_s = _cluster_paired_diff(r_solo, rows_neutre)
            if st_s is not None:
                entry["delta_solo"] = st_s["delta"]
                entry["ci95_solo"] = st_s["ci95"]
                entry["p_solo"] = st_s["p_value"]
                entry["n_paired_tables_solo"] = st_s["n_paired_tables"]
                solo_pvals.append((slot, st_s["p_value"]))
        if has_e:
            # Perte écosystème quand la tuile est retirée = ALL_ACTIVE - LOO(slot)
            st_e = _cluster_paired_diff(rows_active, r_loo)
            if st_e is not None:
                entry["delta_eco"] = st_e["delta"]
                entry["ci95_eco"] = st_e["ci95"]
                entry["p_eco"] = st_e["p_value"]
                entry["n_paired_tables_eco"] = st_e["n_paired_tables"]
                eco_pvals.append((slot, st_e["p_value"]))
        if "delta_solo" in entry and "delta_eco" in entry:
            # Levier synergique L_syn = (ALL_ACTIVE - LOO) - (SOLO - ALL_NEUTRE) sur tables communes
            common_4 = sorted(set(rows_active) & set(r_loo) & set(r_solo) & set(rows_neutre))
            if common_4:
                syn_by_cluster: dict[tuple[str, int, str], list[float]] = {}
                for k in common_4:
                    d_eco = _pair_diffs_for_cluster(rows_active[k], r_loo[k])
                    d_sol = _pair_diffs_for_cluster(r_solo[k], rows_neutre[k])
                    m_len = min(len(d_eco), len(d_sol))
                    syn_by_cluster.setdefault((k[0], k[1], k[2]), []).extend(
                        d_eco[i] - d_sol[i] for i in range(m_len)
                    )
                st_syn = _format_cluster_ci_stats(paired_diff_cluster_ci95(syn_by_cluster))
                entry["levier_synergique"] = st_syn["delta"]
                entry["ci95_levier"] = st_syn["ci95"]
                entry["p_levier"] = st_syn["p_value"]
            else:
                entry["levier_synergique"] = round(float(entry["delta_eco"]) - float(entry["delta_solo"]), 5)
        solo_vs_eco[slot] = entry

    if solo_pvals:
        adj_s = holm_bonferroni_adjust(solo_pvals)
        for s_k, h_info in adj_s.items():
            solo_vs_eco[s_k]["p_holm_solo"] = h_info.get("holm_adjusted_p")
    if eco_pvals:
        adj_e = holm_bonferroni_adjust(eco_pvals)
        for s_k, h_info in adj_e.items():
            solo_vs_eco[s_k]["p_holm_eco"] = h_info.get("holm_adjusted_p")

    # 2. Carrés 2×2 des 15 lisières (détection automatique via active_slots)
    edges_2x2: dict[str, dict[str, Any]] = {}
    edge_pvals: list[tuple[str, float | None]] = []
    bg_mode = str(mod_meta.get("background", "ALL_NEUTRE")).upper()
    is_blank_bg = bg_mode == "ALL_NEUTRE"

    for ek, (sa, sb) in CANONICAL_15_EDGES.items():
        if is_blank_bg:
            r00 = _rows_for_active(())
            r10 = _rows_for_active((sa,))
            r01 = _rows_for_active((sb,))
            r11 = _rows_for_active((sa, sb))
        else:
            r00 = _rows_for_active(tuple(x for x in CANONICAL_30_TILES if x not in (sa, sb)))
            r10 = _rows_for_active(tuple(x for x in CANONICAL_30_TILES if x != sb))
            r01 = _rows_for_active(tuple(x for x in CANONICAL_30_TILES if x != sa))
            r11 = _rows_for_active(CANONICAL_30_TILES)
        if not (r00 and r10 and r01 and r11):
            continue
        common_e = sorted(set(r00) & set(r10) & set(r01) & set(r11))
        if not common_e:
            continue
        inter_by_cluster: dict[tuple[str, int, str], list[float]] = {}
        for k in common_e:
            d11_10 = _pair_diffs_for_cluster(r11[k], r10[k])
            d01_00 = _pair_diffs_for_cluster(r01[k], r00[k])
            m_len = min(len(d11_10), len(d01_00))
            inter_by_cluster.setdefault((k[0], k[1], k[2]), []).extend(
                d11_10[i] - d01_00[i] for i in range(m_len)
            )
        st_i = _format_cluster_ci_stats(paired_diff_cluster_ci95(inter_by_cluster))
        edge_pvals.append((ek, st_i["p_value"]))
        edges_2x2[ek] = {
            "edge": ek,
            "slot_a": sa,
            "slot_b": sb,
            "background": bg_mode,
            "y00": _weighted_mean_of_variant({k: r00[k] for k in common_e}),
            "y10": _weighted_mean_of_variant({k: r10[k] for k in common_e}),
            "y01": _weighted_mean_of_variant({k: r01[k] for k in common_e}),
            "y11": _weighted_mean_of_variant({k: r11[k] for k in common_e}),
            "interaction_2x2": st_i["delta"],
            "ci95_interaction": st_i["ci95"],
            "p_interaction": st_i["p_value"],
            "n_paired_tables": st_i["n_paired_tables"],
        }
    if edge_pvals:
        adj_ed = holm_bonferroni_adjust(edge_pvals)
        for ek, h_info in adj_ed.items():
            edges_2x2[ek]["p_holm_interaction"] = h_info.get("holm_adjusted_p")

    # 3. Moteurs (seuls vs par ablation + synergie holistique si 5 moteurs disjoints présents)
    motors_summary: dict[str, dict[str, Any]] = {}
    motor_ids_seen: dict[str, list[str]] = {}
    for vm in variants_meta:
        role = str(vm.get("study_role", ""))
        if role in ("motor_solo", "motor_ablation"):
            m_id = str(vm.get("group_id", ""))
            m_slots = list((vm.get("extra_meta") or {}).get("motor_slots") or vm.get("target_slots") or [])
            if m_id:
                motor_ids_seen[m_id] = m_slots

    for m_id, m_slots in motor_ids_seen.items():
        r_ms = _rows_for_active(tuple(m_slots))
        r_ma = _rows_for_active(tuple(s for s in CANONICAL_30_TILES if s not in set(m_slots)))
        m_entry: dict[str, Any] = {"motor_id": m_id, "slots": m_slots, "n_slots": len(m_slots)}
        if r_ms and rows_neutre:
            st_ms = _cluster_paired_diff(r_ms, rows_neutre)
            if st_ms is not None:
                m_entry["delta_solo"] = st_ms["delta"]
                m_entry["ci95_solo"] = st_ms["ci95"]
                m_entry["p_solo"] = st_ms["p_value"]
        if r_ma and rows_active:
            st_ma = _cluster_paired_diff(rows_active, r_ma)
            if st_ma is not None:
                m_entry["delta_ablation"] = st_ma["delta"]
                m_entry["ci95_ablation"] = st_ma["ci95"]
                m_entry["p_ablation"] = st_ma["p_value"]
        if "delta_solo" in m_entry and "delta_ablation" in m_entry:
            m_entry["synergy_inter_motors"] = round(
                float(m_entry["delta_ablation"]) - float(m_entry["delta_solo"]), 5
            )
        motors_summary[m_id] = m_entry

    holistic_synergy: dict[str, Any] | None = None
    disjoint_keys = list(get_disjoint_motors().keys())
    if (
        rows_active
        and rows_neutre
        and all(k in motors_summary and "delta_solo" in motors_summary[k] for k in disjoint_keys)
    ):
        st_tot = _cluster_paired_diff(rows_active, rows_neutre)
        if st_tot is not None:
            sum_solos = sum(float(motors_summary[k]["delta_solo"]) for k in disjoint_keys)
            holistic_synergy = {
                "total_ecosystem_gain": st_tot["delta"],
                "sum_5_disjoint_motors_solo": round(sum_solos, 5),
                "holistic_interaction": round(float(st_tot["delta"]) - sum_solos, 5),
            }

    # 4. Sous-ensembles / variantes personnalisées
    subsets_summary: dict[str, dict[str, Any]] = {}
    for vm in variants_meta:
        role = str(vm.get("study_role", ""))
        if role not in ("subset", "custom"):
            continue
        vid = str(vm["variant_id"])
        r_v = by_vid.get(vid, {})
        if not r_v:
            continue
        s_entry: dict[str, Any] = {
            "variant_id": vid,
            "study_role": role,
            "n_active": len(vm.get("active_slots", ())),
            "active_slots": list(vm.get("active_slots", ())),
            "mean_ratio_arbres": _weighted_mean_of_variant(r_v),
        }
        if rows_neutre:
            st_n = _cluster_paired_diff(r_v, rows_neutre)
            if st_n is not None:
                s_entry["delta_vs_all_neutre"] = st_n["delta"]
                s_entry["ci95_vs_all_neutre"] = st_n["ci95"]
        if rows_active:
            st_a = _cluster_paired_diff(r_v, rows_active)
            if st_a is not None:
                s_entry["delta_vs_all_active"] = st_a["delta"]
                s_entry["ci95_vs_all_active"] = st_a["ci95"]
        subsets_summary[vid] = s_entry

    out: dict[str, Any] = {
        "study_type": mod_meta.get("study_type"),
        "reference_bot": ref_bot,
        "baseline_all_neutre_ratio": _weighted_mean_of_variant(rows_neutre) if rows_neutre else None,
        "baseline_all_active_ratio": _weighted_mean_of_variant(rows_active) if rows_active else None,
        "solo_vs_ecosystem": solo_vs_eco,
        "edges_2x2": edges_2x2,
        "motors_summary": motors_summary,
        "subsets_summary": subsets_summary,
    }
    if holistic_synergy is not None:
        out["holistic_synergy"] = holistic_synergy
    return out


def build_assises_197_summary(
    cell_rows: list[dict[str, Any]],
    *,
    preferred_bot: str | None = None,
    preferred_variant: str | None = None,
) -> dict[str, Any] | None:
    """Agrège les performances sur les assises canoniques diédrales (jusqu'à 197 assises / 42 compositions)."""
    if not cell_rows or not any(r.get("assise_key") for r in cell_rows):
        return None
    bots_present = sorted({str(r.get("bot", "B2")).upper() for r in cell_rows})
    ref_bot = (
        preferred_bot.upper()
        if (preferred_bot and preferred_bot.upper() in bots_present)
        else ("B2" if "B2" in bots_present else bots_present[0])
    )
    rows_b = [r for r in cell_rows if str(r.get("bot", "B2")).upper() == ref_bot]
    vids_present = sorted({str(r.get("variant_id", "BASE")) for r in rows_b})
    ref_vid = (
        preferred_variant
        if (preferred_variant and preferred_variant in vids_present)
        else ("ALL_ACTIVE" if "ALL_ACTIVE" in vids_present else ("BASE" if "BASE" in vids_present else vids_present[0]))
    )
    rows_f = [r for r in rows_b if str(r.get("variant_id", "BASE")) == ref_vid]
    if not rows_f:
        return None

    acc_assise: dict[str, dict[str, Any]] = {}
    acc_comp: dict[str, dict[str, Any]] = {}
    for r in rows_f:
        ak = str(r.get("assise_key") or "")
        ck = str(r.get("composition_key") or "")
        if not ak:
            continue
        ng = int(r.get("n_games", 0))
        if ng <= 0:
            continue
        for bucket, key in ((acc_assise, ak), (acc_comp, ck or ak)):
            d = bucket.setdefault(
                key,
                {
                    "n_players": int(r["n_players"]),
                    "assise_key": ak,
                    "composition_key": ck,
                    "n_games": 0,
                    "sum_ratio": 0.0,
                    "c_t8": 0,
                    "c_som": 0,
                    "c_ev": 0,
                },
            )
            d["n_games"] += ng
            d["sum_ratio"] += float(r.get("sum_ratio_arbres", 0.0))
            d["c_t8"] += int(r.get("count_tour_8", 0))
            d["c_som"] += int(r.get("count_reve_rang_1", 0))
            d["c_ev"] += int(r.get("count_reveil_gardiens", 0))

    if not acc_assise:
        return None

    def _fmt_item(d: dict[str, Any]) -> dict[str, Any]:
        ng = max(1, int(d["n_games"]))
        p8 = round(d["c_t8"] * 100.0 / ng, 2)
        ps = round(d["c_som"] * 100.0 / ng, 2)
        pe = round(d["c_ev"] * 100.0 / ng, 2)
        return {
            "assise_key": d["assise_key"],
            "composition_key": d["composition_key"],
            "n_players": d["n_players"],
            "n_games": int(d["n_games"]),
            "mean_ratio_arbres": round(d["sum_ratio"] / ng, 4),
            "pct_tour_8": p8,
            "pct_reve_rang_1": ps,
            "pct_reveil_gardiens": pe,
            "pct_effondrement": round(max(0.0, 100.0 - p8 - ps - pe), 2),
        }

    all_assises = [_fmt_item(d) for d in acc_assise.values()]
    all_assises.sort(key=lambda x: (x["mean_ratio_arbres"], x["assise_key"]))
    by_n_spread: dict[str, dict[str, Any]] = {}
    for n_pl in sorted({a["n_players"] for a in all_assises}):
        sub = [a for a in all_assises if a["n_players"] == n_pl]
        by_n_spread[f"{n_pl}J"] = {
            "n_assises": len(sub),
            "min_ratio": sub[0]["mean_ratio_arbres"],
            "max_ratio": sub[-1]["mean_ratio_arbres"],
            "spread_pts": round((sub[-1]["mean_ratio_arbres"] - sub[0]["mean_ratio_arbres"]) * 100.0, 2),
            "worst_assise": sub[0]["assise_key"],
            "best_assise": sub[-1]["assise_key"],
        }

    return {
        "reference_bot": ref_bot,
        "reference_variant": ref_vid,
        "n_assises_covered": len(all_assises),
        "n_compositions_covered": len(acc_comp),
        "by_n_players_spread": by_n_spread,
        "worst_assises": all_assises[:12],
        "best_assises": list(reversed(all_assises[-12:])),
        "all_assises": all_assises,
    }


def build_b3_degenerate_audit(
    cell_rows: list[dict[str, Any]],
    *,
    variant_tile_profiles_map: dict[str, tuple[tuple[str, str], ...]] | None = None,
) -> tuple[dict[str, Any], RemarkableGameBookmark | None]:
    """Compare B3 MCTS à B2 en CRN apparié pour détecter toute stratégie dégénérée / exploit."""
    b2_map: dict[tuple[str, int, str, int, int], dict[str, Any]] = {}
    b3_map: dict[tuple[str, int, str, int, int], dict[str, Any]] = {}
    for r in cell_rows:
        b = str(r.get("bot", "")).upper()
        key = (
            str(r.get("variant_id", "BASE")),
            int(r.get("n_players", 4)),
            str(r.get("table_id", "")),
            int(r.get("exp_seed", 0)),
            int(r.get("rep_start", 0)),
        )
        if b == "B2":
            b2_map[key] = r
        elif b == "B3":
            b3_map[key] = r

    common = sorted(set(b2_map) & set(b3_map))
    if not common:
        return {"enabled": False}, None

    diffs_by_cluster: dict[tuple[str, int, str], list[float]] = {}
    b2_end = {"tour_8": 0, "sommeil": 0, "eveil": 0, "n": 0}
    b3_end = {"tour_8": 0, "sommeil": 0, "eveil": 0, "n": 0}
    assise_divs: list[dict[str, Any]] = []
    top_bm: RemarkableGameBookmark | None = None
    top_div_val = -1e9
    tot_paired_games = 0

    for key in common:
        r2 = b2_map[key]
        r3 = b3_map[key]
        e2 = _extract_row_ratios(r2)
        e3 = _extract_row_ratios(r3)
        n2 = e2[1]
        n3 = e3[1]
        n_pair = min(n2, n3)
        tot_paired_games += n_pair
        # Appariement exact sur les n_pair premières répliques via rep_ratios_bp_json si B3 a un cap
        pair_diffs = _pair_diffs_for_cluster(e3, e2)
        cluster_k = (key[0], key[1], key[2])
        diffs_by_cluster.setdefault(cluster_k, []).extend(pair_diffs)
        delta_k = sum(pair_diffs) / float(max(1, len(pair_diffs)))
        m2 = (
            sum(e2[2][:n_pair]) / (10000.0 * n_pair)
            if (e2[2] is not None and len(e2[2]) >= n_pair > 0)
            else e2[0]
        )
        m3 = (
            sum(e3[2][:n_pair]) / (10000.0 * n_pair)
            if (e3[2] is not None and len(e3[2]) >= n_pair > 0)
            else e3[0]
        )

        b2_end["tour_8"] += int(r2.get("count_tour_8", 0))
        b2_end["sommeil"] += int(r2.get("count_reve_rang_1", 0))
        b2_end["eveil"] += int(r2.get("count_reveil_gardiens", 0))
        b2_end["n"] += n2
        b3_end["tour_8"] += int(r3.get("count_tour_8", 0))
        b3_end["sommeil"] += int(r3.get("count_reve_rang_1", 0))
        b3_end["eveil"] += int(r3.get("count_reveil_gardiens", 0))
        b3_end["n"] += n3

        ak = str(r3.get("assise_key") or r3.get("table_id") or "")
        vid_s = str(r3.get("variant_id", "BASE"))
        assise_divs.append(
            {
                "assise_key": ak,
                "variant_id": vid_s,
                "b2_ratio": round(m2, 4),
                "b3_ratio": round(m3, 4),
                "delta_ratio": round(delta_k, 4),
                "n_paired_games": n_pair,
            }
        )
        if delta_k > top_div_val:
            top_div_val = delta_k
            peuples_t = tuple(p for p in str(r3.get("peuples", "")).split("-") if p)
            t_profs = (
                variant_tile_profiles_map.get(vid_s, ())
                if variant_tile_profiles_map
                else ()
            )
            best_idx = 0
            best_game_m3 = m3
            best_game_m2 = m2
            bp3 = e3[2]
            bp2 = e2[2]
            if (
                bp3 is not None
                and bp2 is not None
                and len(bp3) >= n_pair > 0
                and len(bp2) >= n_pair
            ):
                best_diff_bp = bp3[0] - bp2[0]
                for idx_r in range(1, n_pair):
                    d_bp = bp3[idx_r] - bp2[idx_r]
                    if d_bp > best_diff_bp:
                        best_diff_bp = d_bp
                        best_idx = idx_r
                best_game_m3 = bp3[best_idx] / 10000.0
                best_game_m2 = bp2[best_idx] / 10000.0
            best_rep_id = int(r3.get("rep_start", 0)) + best_idx
            n_pl_b3 = int(r3["n_players"])
            top_bm = RemarkableGameBookmark(
                category="b3_vs_b2_outlier",
                metric_value=round(delta_k, 5),
                bot="B3",
                variant_id=vid_s,
                n_players=n_pl_b3,
                mode=int(r3["mode"]),
                peuples=peuples_t,
                exp_seed=int(r3.get("exp_seed", 0)),
                rep_id=best_rep_id,
                chassis_id=int(r3.get("config_id", -1)),
                tile_profiles=t_profs,
                score_arbres=round(best_game_m3 * n_pl_b3 * 10),
                ratio_arbres=round(best_game_m3, 4),
                cause_fin="B3_VS_B2_OUTLIER",
                tour_fin=8,
                assise_key=ak,
                coordonnateur_initial=best_rep_id % n_pl_b3,
                note=(
                    f"assise B3={m3*100:.1f}% vs B2={m2*100:.1f}% ({delta_k*100:+.1f} pts) | "
                    f"partie rep={best_rep_id}: B3={best_game_m3*100:.1f}% vs B2={best_game_m2*100:.1f}%"
                ),
            )

    st_fmt = _format_cluster_ci_stats(paired_diff_cluster_ci95(diffs_by_cluster))
    assise_divs.sort(key=lambda x: -x["delta_ratio"])

    def _pct_end(d: dict[str, int], k: str) -> float:
        return round(d[k] * 100.0 / max(1, d["n"]), 2)

    p2_t8, p2_som, p2_ev = _pct_end(b2_end, "tour_8"), _pct_end(b2_end, "sommeil"), _pct_end(b2_end, "eveil")
    p3_t8, p3_som, p3_ev = _pct_end(b3_end, "tour_8"), _pct_end(b3_end, "sommeil"), _pct_end(b3_end, "eveil")
    p2_eff = max(0.0, 100.0 - p2_t8 - p2_som - p2_ev)
    p3_eff = max(0.0, 100.0 - p3_t8 - p3_som - p3_ev)
    shifts = {
        "tour_8": round(p3_t8 - p2_t8, 2),
        "sommeil": round(p3_som - p2_som, 2),
        "eveil": round(p3_ev - p2_ev, 2),
        "effondrement": round(p3_eff - p2_eff, 2),
    }
    mean_d = float(st_fmt["delta"])
    is_deg = mean_d > 0.08 or any(abs(v) >= 15.0 for v in shifts.values())

    return (
        {
            "enabled": True,
            "paired_tables": int(st_fmt["n_paired_tables"]),
            "paired_games": int(tot_paired_games),
            "delta_b3_minus_b2_ratio": mean_d,
            "ci95": st_fmt["ci95"],
            "p_value": st_fmt["p_value"],
            "ending_shifts_pts": shifts,
            "degenerate_flag": is_deg,
            "top_divergent_assises": assise_divs[:8],
        },
        top_bm,
    )


def build_v64_forks_summary(fork_row: dict[str, Any]) -> dict[str, Any]:
    """Formate l'ensemble des 12 métriques de micro-forks causaux v6.4 (moyenne, SD, IC95)."""
    specs: tuple[tuple[str, str, str, str], ...] = (
        ("2_1_b2_vs_b0", "fork_2_1_anchors", "sum_delta_v_2_1_b2_vs_b0", "sum_sq_delta_v_2_1_b2_vs_b0"),
        ("2_1_reve", "fork_2_1_reve_anchors", "sum_delta_v_2_1_reve", "sum_sq_delta_v_2_1_reve"),
        ("2_2_negociation", "fork_anchors", "sum_delta_v_neg", "sum_sq_delta_v_neg"),
        ("furt_rive_piege", "fork_furt_rp_anchors", "sum_delta_v_furt_rp", "sum_sq_delta_v_furt_rp"),
        ("furt_rive_sabotage", "fork_furt_rs_anchors", "sum_delta_v_furt_rs", "sum_sq_delta_v_furt_rs"),
        ("furt_sentinelle", "fork_furt_sent_anchors", "sum_delta_v_furt_sent", "sum_sq_delta_v_furt_sent"),
        ("4_1_pose_piege", "fork_4_1_piege_anchors", "sum_delta_v_4_1_piege", "sum_sq_delta_v_4_1_piege"),
        ("6_1_enracinement", "fork_6_1_enrac_anchors", "sum_delta_v_6_1_enrac", "sum_sq_delta_v_6_1_enrac"),
        ("eveil_a_plus_1", "fork_eveil_anchors", "sum_delta_v_eveil_vs_survival", "sum_sq_delta_v_eveil_vs_survival"),
        ("2_2_gardien_pari", "fork_2_2_gpari_anchors", "sum_delta_v_2_2_gpari", "sum_sq_delta_v_2_2_gpari"),
        ("2_1_chaman_chosen_vs_alt", "fork_2_1_chaman_anchors", "sum_delta_v_2_1_chaman_chosen", "sum_sq_delta_v_2_1_chaman_chosen"),
        ("2_1_chaman_tambour_minus_chant", "fork_2_1_chaman_anchors", "sum_delta_v_2_1_chaman_tmc", "sum_sq_delta_v_2_1_chaman_tmc"),
        ("alteration", "fork_alteration_anchors", "sum_delta_v_alteration", "sum_sq_delta_v_alteration"),
        ("3_1_gardien_icone", "fork_3_1_gicon_anchors", "sum_delta_v_3_1_gicon", "sum_sq_delta_v_3_1_gicon"),
    )
    out: dict[str, Any] = {}
    for label, col_n, col_s, col_sq in specs:
        n_a = int(fork_row.get(col_n) or 0)
        if n_a <= 0:
            continue
        s_v = float(fork_row.get(col_s) or 0.0)
        sq_v = float(fork_row.get(col_sq) or 0.0)
        mean_v = s_v / float(n_a)
        var = max(0.0, (sq_v - (s_v * s_v) / n_a) / (n_a - 1)) if n_a >= 2 else 0.0
        sd_v = math.sqrt(var)
        ci_half = round(1.96 * math.sqrt(var / n_a), 5) if n_a >= 2 else None
        out[label] = {
            "n_anchors": n_a,
            "mean_delta_v": round(mean_v, 5),
            "sd_delta_v": round(sd_v, 5),
            "ci95_half": ci_half,
        }
    return out


def _safe_json_loads(raw: Any) -> Any:
    if not raw:
        return None
    try:
        return json.loads(str(raw))
    except (ValueError, TypeError):
        return None


def build_v64_ockham_from_rows(
    cell_rows: list[dict[str, Any]],
    *,
    false_dilemma_threshold_pct: float = 90.0,
    min_samples: int = 20,
) -> dict[str, Any] | None:
    """Fusionne les colonnes `v64_dilemmas_json` de tous les shards et détecte les faux dilemmes (> 90 %)."""
    audits: list[dict[str, Any]] = []
    for r in cell_rows:
        parsed = _safe_json_loads(r.get("v64_dilemmas_json"))
        if isinstance(parsed, dict):
            audits.append(parsed)
    if not audits:
        return None
    merged = merge_v64_ockham_audits(audits)
    return summarize_v64_ockham_audit(
        merged,
        false_dilemma_threshold_pct=false_dilemma_threshold_pct,
        min_samples=min_samples,
    )


def collect_remarkable_bookmarks_from_rows(
    cell_rows: list[dict[str, Any]],
    *,
    extra_bookmarks: list[RemarkableGameBookmark] | None = None,
    max_games: int = 8,
) -> list[RemarkableGameBookmark]:
    """Collecte et sélectionne les K parties remarquables à rejouer en `human_trace_1.0`."""
    collected: list[dict[str, Any] | RemarkableGameBookmark] = []
    if extra_bookmarks:
        collected.extend(extra_bookmarks)
    for r in cell_rows:
        items = _safe_json_loads(r.get("remarkable_bookmarks_json"))
        if isinstance(items, list):
            collected.extend(items)
    return select_top_remarkable_bookmarks(collected, max_games=max_games)
