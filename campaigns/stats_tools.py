"""Outils statistiques appariés, bootstrap CVaR, dimensionnement et comparaisons multiples (100 % stdlib PyPy 3.11)."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any

from engine.rng import rand_u64

__all__ = (
    "assess_sign_stability",
    "circle_dispersion_summary",
    "cvar_exact_from_bp_hist",
    "cvar_exact_values",
    "cvar_with_bootstrap_ci95",
    "estimate_required_pairs",
    "holm_bonferroni_adjust",
    "paired_diff_cluster_ci95",
    "sequential_ci_elimination",
    "student_t_two_sided_p",
    "t_critical_95",
)

# Quantiles bilatéraux t_{0.975, df} exacts pour IC 95 % (petits nombres de cercles/tables)
_T_CRIT_95_TABLE: dict[int, float] = {
    1: 12.7062,
    2: 4.3027,
    3: 3.1824,
    4: 2.7764,
    5: 2.5706,
    6: 2.4469,
    7: 2.3646,
    8: 2.3060,
    9: 2.2622,
    10: 2.2281,
    11: 2.2010,
    12: 2.1788,
    13: 2.1604,
    14: 2.1448,
    15: 2.1314,
    16: 2.1199,
    17: 2.1098,
    18: 2.1009,
    19: 2.0930,
    20: 2.0860,
    21: 2.0796,
    22: 2.0739,
    23: 2.0687,
    24: 2.0639,
    25: 2.0595,
    26: 2.0555,
    27: 2.0518,
    28: 2.0484,
    29: 2.0452,
    30: 2.0423,
    40: 2.0211,
    60: 2.0003,
    120: 1.9799,
}
_T_CRIT_KEYS: tuple[int, ...] = tuple(sorted(_T_CRIT_95_TABLE))
_SRC_BOOTSTRAP: int = 9101


def t_critical_95(df: int) -> float:
    """Retourne la valeur critique bilatérale t_{0.975, df} (1.96 au-delà de df=120)."""
    if df <= 0:
        return 1.96
    if df in _T_CRIT_95_TABLE:
        return _T_CRIT_95_TABLE[df]
    if df >= 120:
        return 1.96
    lo_k = 30
    hi_k = 120
    for k in _T_CRIT_KEYS:
        if k < df:
            lo_k = k
        elif k > df:
            hi_k = k
            break
    frac = (df - lo_k) / max(1, hi_k - lo_k)
    return _T_CRIT_95_TABLE[lo_k] * (1.0 - frac) + _T_CRIT_95_TABLE[hi_k] * frac


def _betacf(a: float, b: float, x: float) -> float:
    """Fraction continue de Lentz pour la fonction bêta incomplète régularisée I_x(a, b)."""
    eps = 3.0e-12
    fpmin = 1.0e-300
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, 201):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def _regularized_incomplete_beta(a: float, b: float, x: float) -> float:
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(
        math.lgamma(a + b)
        - math.lgamma(a)
        - math.lgamma(b)
        + a * math.log(x)
        + b * math.log(1.0 - x)
    )
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def student_t_two_sided_p(t_abs: float, df: int) -> float:
    """Calcule la p-valeur bilatérale exacte de la loi de Student(|T| >= t_abs)."""
    val = abs(float(t_abs))
    if val <= 0.0:
        return 1.0
    if df <= 0:
        return 1.0
    if df >= 500:
        return math.erfc(val / math.sqrt(2.0))
    x = df / (df + val * val)
    p = _regularized_incomplete_beta(0.5 * df, 0.5, x)
    return max(0.0, min(1.0, p))


def paired_diff_cluster_ci95(
    diffs_by_cluster: Mapping[Any, Sequence[float]] | Sequence[Sequence[float]],
    *,
    alpha_z: float | None = None,
) -> dict[str, Any]:
    """Calcule la différence appariée moyenne et son IC 95 % avec erreurs-types groupées par table.

    Chaque cluster (table/cercle) contient les différences appariées jeu-à-jeu (CRN)
    `y_variant - y_ref` pour cette table. La moyenne globale pondère chaque jeu à poids égal
    et la variance groupée CR1 (Liang-Zeger avec correction `G / (G - 1)`) est exacte même
    lorsque les tables n'ont pas exactement le même effectif.
    """
    clusters: list[tuple[int, float]] = []
    if isinstance(diffs_by_cluster, Mapping):
        raw_iter = diffs_by_cluster.values()
    else:
        raw_iter = diffs_by_cluster

    for seq in raw_iter:
        vals = [float(v) for v in seq]
        if vals:
            clusters.append((len(vals), sum(vals)))

    n_clusters = len(clusters)
    n_pairs = sum(cnt for cnt, _ in clusters)
    if n_clusters == 0 or n_pairs == 0:
        return {
            "n_tables": 0,
            "n_pairs": 0,
            "mean_delta": None,
            "se_clustered": None,
            "ci95_low": None,
            "ci95_high": None,
            "t_stat": None,
            "p_value": None,
            "estimable": False,
            "status": "empty",
        }

    mean_delta = sum(s for _, s in clusters) / n_pairs
    if n_clusters < 2:
        return {
            "n_tables": n_clusters,
            "n_pairs": n_pairs,
            "mean_delta": round(mean_delta, 5),
            "se_clustered": None,
            "ci95_low": None,
            "ci95_high": None,
            "t_stat": None,
            "p_value": None,
            "estimable": False,
            "status": "non_estimable_single_table",
        }

    df = n_clusters - 1
    # Résidu de somme de cluster e_c = sum_i (d_{c,i} - mean_delta) = sum_c - n_c * mean_delta
    sum_sq_e = 0.0
    for cnt, s_val in clusters:
        e_c = s_val - cnt * mean_delta
        sum_sq_e += e_c * e_c
    var_hat = (n_clusters / df) * (sum_sq_e / (n_pairs * n_pairs))
    se = math.sqrt(max(0.0, var_hat))
    crit = float(alpha_z) if alpha_z is not None else t_critical_95(df)
    half = crit * se

    if se > 1e-12:
        t_stat = mean_delta / se
        p_val = student_t_two_sided_p(t_stat, df)
    else:
        t_stat = 0.0 if abs(mean_delta) <= 1e-12 else (math.copysign(999.0, mean_delta))
        p_val = 1.0 if abs(mean_delta) <= 1e-12 else 0.0

    return {
        "n_tables": n_clusters,
        "n_pairs": n_pairs,
        "mean_delta": round(mean_delta, 5),
        "se_clustered": round(se, 5),
        "ci95_low": round(mean_delta - half, 5),
        "ci95_high": round(mean_delta + half, 5),
        "t_stat": round(t_stat, 4),
        "p_value": round(p_val, 6),
        "estimable": True,
        "status": "estimable",
    }


def circle_dispersion_summary(
    means_by_circle: Sequence[float],
    weights_by_circle: Sequence[int] | None = None,
) -> dict[str, Any]:
    """Synthétise la moyenne pondérée et la dispersion inter-cercles (explicite 'non estimable' si 1 cercle)."""
    n_c = len(means_by_circle)
    if n_c == 0:
        return {
            "n_circles": 0,
            "n_blocks": 0,
            "n_games": 0,
            "mean_ratio_arbres": None,
            "std_inter_circles": None,
            "se_inter_circles": None,
            "ci95_low": None,
            "ci95_high": None,
            "min_circle_mean": None,
            "max_circle_mean": None,
            "spread_circles": None,
            "estimable": False,
            "status": "empty",
        }

    vals = [float(v) for v in means_by_circle]
    if weights_by_circle is None:
        ws = [1] * n_c
    else:
        if len(weights_by_circle) != n_c:
            raise ValueError("weights_by_circle doit avoir la même longueur que means_by_circle")
        ws = [max(0, int(w)) for w in weights_by_circle]

    total_w = sum(ws)
    if total_w <= 0:
        ws = [1] * n_c
        total_w = n_c

    mean_w = sum(v * w for v, w in zip(vals, ws, strict=True)) / total_w

    if n_c == 1:
        m_r = round(mean_w, 4)
        return {
            "n_circles": 1,
            "n_blocks": 1,
            "n_games": total_w,
            "mean_ratio_arbres": m_r,
            "std_inter_circles": None,
            "se_inter_circles": None,
            "ci95_low": None,
            "ci95_high": None,
            "min_circle_mean": m_r,
            "max_circle_mean": m_r,
            "spread_circles": 0.0,
            "estimable": False,
            "status": "non_estimable_single_circle",
            "uncertainty_note": "Incertitude inter-cercles non estimable (1 seul cercle exécuté).",
        }

    # Écart-type pondéré des moyennes par cercle (avec correction degrés de liberté G / (G - 1))
    df = n_c - 1
    weighted_var = (n_c / df) * sum(
        (w / total_w) * ((v - mean_w) ** 2) for v, w in zip(vals, ws, strict=True)
    )
    std_c = math.sqrt(max(0.0, weighted_var))
    # Erreur-type groupée CR1 de la moyenne pondérée par effectifs de jeux
    var_mean = (n_c / df) * sum(
        ((w * (v - mean_w)) ** 2) for v, w in zip(vals, ws, strict=True)
    ) / (total_w * total_w)
    se_c = math.sqrt(max(0.0, var_mean))
    half = t_critical_95(df) * se_c

    min_v = min(vals)
    max_v = max(vals)
    return {
        "n_circles": n_c,
        "n_blocks": n_c,
        "n_games": total_w,
        "mean_ratio_arbres": round(mean_w, 4),
        "std_inter_circles": round(std_c, 4),
        "se_inter_circles": round(se_c, 4),
        "ci95_low": round(max(0.0, mean_w - half), 4),
        "ci95_high": round(min(1.0, mean_w + half), 4),
        "min_circle_mean": round(min_v, 4),
        "max_circle_mean": round(max_v, 4),
        "spread_circles": round(max_v - min_v, 4),
        "estimable": True,
        "status": "estimable",
    }


def cvar_exact_values(values: Sequence[float], alpha: float = 0.20) -> float:
    """CVaR continue exacte à alpha uniforme sur la distribution directe des parties.

    Évite tout biais d'arrondi entier selon la taille d'échantillon :
    intègre exactement la fraction `alpha * N` la plus basse des valeurs triées.
    """
    n = len(values)
    if n == 0:
        return 0.0
    if not (0.0 < alpha <= 1.0):
        raise ValueError(f"alpha CVaR invalide (attendu dans (0, 1]) : {alpha}")
    ordered = sorted(float(v) for v in values)
    mass = alpha * n
    if mass <= 1.0:
        return ordered[0]
    full_k = math.floor(mass)
    frac = mass - full_k
    total = sum(ordered[:full_k])
    if frac > 1e-12 and full_k < n:
        total += frac * ordered[full_k]
    return total / mass


def cvar_exact_from_bp_hist(hist: Mapping[int, int], alpha: float = 0.20) -> float:
    """CVaR continue exacte à alpha uniforme depuis un histogramme de ratios en points de base (bp)."""
    total_n = sum(max(0, int(c)) for c in hist.values())
    if total_n <= 0:
        return 0.0
    if not (0.0 < alpha <= 1.0):
        raise ValueError(f"alpha CVaR invalide (attendu dans (0, 1]) : {alpha}")
    mass = alpha * total_n
    rem = mass
    acc = 0.0
    for bp_val in sorted(hist):
        cnt = max(0, int(hist[bp_val]))
        if cnt <= 0:
            continue
        take = min(rem, float(cnt))
        acc += bp_val * take
        rem -= take
        if rem <= 1e-12:
            break
    return (acc / mass) / 10000.0


def _cvar_from_sorted_bp_pairs(pairs: Sequence[tuple[int, int]], total_n: int, alpha: float) -> float:
    if total_n <= 0:
        return 0.0
    mass = alpha * total_n
    rem = mass
    acc = 0.0
    for bp_val, cnt in pairs:
        if cnt <= 0:
            continue
        take = min(rem, float(cnt))
        acc += bp_val * take
        rem -= take
        if rem <= 1e-12:
            break
    return (acc / mass) / 10000.0


def cvar_with_bootstrap_ci95(
    clusters_bp_hists: Sequence[Mapping[int, int]],
    *,
    alpha: float = 0.20,
    n_boot: int = 400,
    seed: int = 20261201,
) -> dict[str, Any]:
    """Calcule la CVaR exacte directe d'une strate et son IC 95 % par bootstrap déterministe.

    - Si >= 2 tables/clusters sont présentes, rééchantillonne les tables avec remise (cluster bootstrap)
      pour respecter la corrélation intra-table.
    - Si 1 seule table avec >= 2 parties est présente, rééchantillonne les parties de cette table et
      indique `bootstrap_level = "within_single_table"`.
    """
    non_empty: list[dict[int, int]] = []
    pooled: dict[int, int] = {}
    for h in clusters_bp_hists:
        clean = {int(k): int(v) for k, v in h.items() if int(v) > 0}
        if not clean:
            continue
        non_empty.append(clean)
        for k, v in clean.items():
            pooled[k] = pooled.get(k, 0) + v

    total_games = sum(pooled.values())
    n_clusters = len(non_empty)
    if total_games <= 0:
        return {
            "alpha": alpha,
            "n_games": 0,
            "n_tables": 0,
            "cvar": 0.0,
            "ci95_low": None,
            "ci95_high": None,
            "bootstrap_level": "empty",
            "estimable": False,
        }

    point_est = cvar_exact_from_bp_hist(pooled, alpha=alpha)
    if total_games < 2 or n_boot < 20:
        return {
            "alpha": alpha,
            "n_games": total_games,
            "n_tables": n_clusters,
            "cvar": round(point_est, 4),
            "ci95_low": None,
            "ci95_high": None,
            "bootstrap_level": "insufficient_samples",
            "estimable": False,
        }

    boot_vals: list[float] = []
    if n_clusters >= 2:
        bootstrap_level = "cluster_table"
        # Pré-compile chaque cluster comme tuple de (bp, cnt) pour rapidité PyPy/CPython
        compiled = [tuple(sorted(c.items())) for c in non_empty]
        for b in range(n_boot):
            agg: dict[int, int] = {}
            tot_b = 0
            for j in range(n_clusters):
                pick = int(rand_u64(seed, b, _SRC_BOOTSTRAP, j, 0, 0) % n_clusters)
                for bp_v, cnt_v in compiled[pick]:
                    agg[bp_v] = agg.get(bp_v, 0) + cnt_v
                    tot_b += cnt_v
            boot_vals.append(_cvar_from_sorted_bp_pairs(sorted(agg.items()), tot_b, alpha))
    else:
        bootstrap_level = "within_single_table"
        expanded: list[int] = []
        for bp_v, cnt_v in sorted(pooled.items()):
            expanded.extend([bp_v] * cnt_v)
        m = len(expanded)
        for b in range(n_boot):
            sample = [
                expanded[int(rand_u64(seed, b, _SRC_BOOTSTRAP, j, 1, 0) % m)]
                for j in range(m)
            ]
            sample.sort()
            mass = alpha * m
            full_k = math.floor(mass)
            frac = mass - full_k
            tot_bp = float(sum(sample[:full_k]))
            if frac > 1e-12 and full_k < m:
                tot_bp += frac * sample[full_k]
            boot_vals.append((tot_bp / mass) / 10000.0)

    boot_vals.sort()
    lo_idx = max(0, math.floor(0.025 * (len(boot_vals) - 1)))
    hi_idx = min(len(boot_vals) - 1, math.ceil(0.975 * (len(boot_vals) - 1)))
    return {
        "alpha": alpha,
        "n_games": total_games,
        "n_tables": n_clusters,
        "cvar": round(point_est, 4),
        "ci95_low": round(boot_vals[lo_idx], 4),
        "ci95_high": round(boot_vals[hi_idx], 4),
        "bootstrap_level": bootstrap_level,
        "estimable": True,
    }


def estimate_required_pairs(
    pilot_diffs: Sequence[float],
    *,
    target_delta: float,
    z: float = 1.96,
    min_pairs: int = 10,
) -> dict[str, Any]:
    """Estime la taille d'échantillon appariée requise n = ceil((z * sigma / delta)^2) sur un pilote."""
    if target_delta <= 0.0:
        raise ValueError(f"target_delta doit être strictement positif (reçu {target_delta})")
    vals = [float(v) for v in pilot_diffs]
    n_pilot = len(vals)
    if n_pilot < 2:
        raise ValueError(f"Au moins 2 paires pilote sont requises (reçu {n_pilot})")
    mean_d = sum(vals) / n_pilot
    var_d = sum((x - mean_d) ** 2 for x in vals) / (n_pilot - 1)
    sigma = math.sqrt(max(0.0, var_d))
    raw_ci_n = ((z * sigma) / target_delta) ** 2
    req_ci95 = max(min_pairs, math.ceil(raw_ci_n))
    # Référence supplémentaire à puissance 80 % bilatérale (z_{0.975} + z_{0.80} ≈ 2.8016)
    raw_pow80_n = ((2.8016 * sigma) / target_delta) ** 2
    req_pow80 = max(min_pairs, math.ceil(raw_pow80_n))
    return {
        "n_pilot_pairs": n_pilot,
        "pilot_mean_delta": round(mean_d, 5),
        "pilot_std_diff": round(sigma, 5),
        "target_delta": float(target_delta),
        "z_value": float(z),
        "required_pairs_ci95": req_ci95,
        "required_pairs_power80": req_pow80,
    }


def holm_bonferroni_adjust(
    p_items: Sequence[tuple[str, float | None]],
    *,
    alpha: float = 0.05,
) -> dict[str, dict[str, Any]]:
    """Correction de Holm-Bonferroni pas à pas pour comparaisons multiples."""
    valid: list[tuple[str, float]] = []
    out: dict[str, dict[str, Any]] = {}
    for key, p_val in p_items:
        if p_val is None:
            out[key] = {
                "raw_p": None,
                "holm_adjusted_p": None,
                "reject_h0": False,
                "rank": None,
            }
        else:
            valid.append((key, max(0.0, min(1.0, float(p_val)))))

    m = len(valid)
    if m == 0:
        return out

    valid.sort(key=lambda kv: (kv[1], kv[0]))
    running_max = 0.0
    for idx, (key, raw_p) in enumerate(valid):
        factor = m - idx
        adj = min(1.0, raw_p * factor)
        running_max = max(running_max, adj)
        out[key] = {
            "raw_p": round(raw_p, 6),
            "holm_adjusted_p": round(running_max, 6),
            "reject_h0": bool(running_max < alpha),
            "rank": idx + 1,
        }
    return out


def sequential_ci_elimination(
    candidates: Sequence[Mapping[str, Any]],
    *,
    maximize: bool = True,
) -> dict[str, Any]:
    """Élimination séquentielle par recouvrement d'IC 95 % entre nombreux châssis ou tuiles."""
    estimable: list[tuple[str, float, float, float]] = []
    non_estimable: list[str] = []
    for cand in candidates:
        cid = str(cand["id"])
        lo = cand.get("ci95_low")
        hi = cand.get("ci95_high")
        mean = cand.get("mean")
        if lo is None or hi is None or mean is None:
            non_estimable.append(cid)
        else:
            estimable.append((cid, float(mean), float(lo), float(hi)))

    if not estimable:
        return {
            "retained_ids": list(non_estimable),
            "eliminated_ids": [],
            "non_estimable_ids": non_estimable,
            "reference_bound": None,
        }

    if maximize:
        ref_bound = max(lo for _, _, lo, _ in estimable)
        retained = [cid for cid, _, _, hi in estimable if hi >= ref_bound]
        eliminated = [cid for cid, _, _, hi in estimable if hi < ref_bound]
    else:
        ref_bound = min(hi for _, _, _, hi in estimable)
        retained = [cid for cid, _, lo, _ in estimable if lo <= ref_bound]
        eliminated = [cid for cid, _, lo, _ in estimable if lo > ref_bound]

    retained.extend(non_estimable)
    return {
        "retained_ids": retained,
        "eliminated_ids": eliminated,
        "non_estimable_ids": non_estimable,
        "reference_bound": round(ref_bound, 5),
    }


def assess_sign_stability(
    deltas_by_bot: Mapping[str, Mapping[str, Any]],
    *,
    panel_bots: tuple[str, ...] = ("B1", "B2", "B2_OPEN"),
    zero_tol: float = 1e-4,
) -> dict[str, Any]:
    """Évalue la stabilité du signe d'un effet entre B1, B2 et le plafond omniscient B2_OPEN."""
    present: list[str] = []
    signs: dict[str, int] = {}
    sig_signs: dict[str, int] = {}
    for bot in panel_bots:
        entry = deltas_by_bot.get(bot)
        if not entry or entry.get("mean_delta") is None:
            continue
        present.append(bot)
        md = float(entry["mean_delta"])
        if md > zero_tol:
            signs[bot] = 1
        elif md < -zero_tol:
            signs[bot] = -1
        else:
            signs[bot] = 0
        lo = entry.get("ci95_low")
        hi = entry.get("ci95_high")
        if lo is not None and hi is not None:
            if float(lo) > 0.0:
                sig_signs[bot] = 1
            elif float(hi) < 0.0:
                sig_signs[bot] = -1
            else:
                sig_signs[bot] = 0

    all_present = all(b in present for b in panel_bots)
    if len(present) < 2:
        return {
            "panel_bots": list(panel_bots),
            "bots_present": present,
            "all_panel_present": all_present,
            "signs_by_bot": signs,
            "significant_signs_by_bot": sig_signs,
            "sign_stable": None,
            "status": "INSUFFICIENT_BOTS",
        }

    nonzero = {v for v in signs.values() if v != 0}
    if not nonzero:
        status = "NEUTRAL_ZERO"
        stable = True
    elif len(nonzero) == 1 and len(signs) == sum(1 for v in signs.values() if v != 0):
        sign_v = next(iter(nonzero))
        status = "STABLE_POSITIVE" if sign_v > 0 else "STABLE_NEGATIVE"
        stable = True
    elif len(nonzero) == 1:
        status = "PARTIALLY_ZERO_SAME_SIGN"
        stable = True
    else:
        status = "INCONSISTENT_SIGN"
        stable = False

    return {
        "panel_bots": list(panel_bots),
        "bots_present": present,
        "all_panel_present": all_present,
        "signs_by_bot": signs,
        "significant_signs_by_bot": sig_signs,
        "sign_stable": stable,
        "status": status,
    }
