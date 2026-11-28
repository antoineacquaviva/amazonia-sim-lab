"""Devis 5 lignes, alertes automatiques, digest exécutif léger et rapport Markdown v6.4.

100 % stdlib Python (compatible PyPy 3.11 et CPython 3.12, zéro dépendance tierce, zéro appel API LLM).
Produit :
1. `format_campaign_quote_5_lines` : devis auteur clair en 5 lignes avant lancement Cloud Batch Spot.
2. `generate_balancing_alerts` : détection automatique d'anomalies d'équilibrage (lisible nativement par `docs/index.html`).
3. `build_executive_digest` : digest exécutif léger (< 35 Ko) pour `docs/digests/`.
4. `render_campaign_markdown_report` : rapport Markdown complet et lisible pour `docs/rapports/`.
"""

from __future__ import annotations

import json
import math
from typing import Any

__all__ = (
    "build_executive_digest",
    "estimate_campaign_cost_and_duration",
    "format_campaign_quote_5_lines",
    "generate_balancing_alerts",
    "render_campaign_markdown_report",
)

# Débits réels calibrés sur worker PyPy 3.11 (`c3-standard-8`, 8 vCPU Spot)
_GPS_PER_CORE_B2_MACRO: float = 48.0
_GPS_PER_CORE_B0_B1_MACRO: float = 75.0
_GPS_PER_CORE_B3_MCTS: float = 2.8
_GPS_PER_CORE_MICRO_FORKS: float = 8.5

# Tarifs indicatifs GCP Europe-West1 (EUR / vCPU-heure approximatif)
_COST_EUR_PER_VCPU_HOUR_SPOT: float = 0.0115
_COST_EUR_PER_VCPU_HOUR_STD: float = 0.0440


def estimate_campaign_cost_and_duration(
    plan: dict[str, Any],
    *,
    backend: str = "batch",
    tasks: int = 8,
    workers: int = 8,
    is_spot: bool = True,
) -> dict[str, Any]:
    """Estime la durée murale et le coût GCP (en EUR) à partir du plan résolu et des débits PyPy mesurés."""
    units = list(plan.get("units", ()))
    is_forks = bool(plan.get("micro_forks", False))
    total_core_sec = 0.0
    b3_games = 0
    total_games = 0
    for u in units:
        g = int(u.get("n_games", 0))
        total_games += g
        b = str(u.get("bot", "B2")).upper()
        if b == "B3":
            b3_games += g
            b3_cfg = u.get("b3_config") or {}
            det_scale = max(1.0, float(b3_cfg.get("n_determinizations", 2)) / 2.0)
            gps = _GPS_PER_CORE_B3_MCTS / det_scale
        elif is_forks:
            gps = _GPS_PER_CORE_MICRO_FORKS
        elif b in ("B0", "B1"):
            gps = _GPS_PER_CORE_B0_B1_MACRO
        else:
            gps = _GPS_PER_CORE_B2_MACRO
        total_core_sec += float(g) / max(0.2, gps)

    eff_tasks = max(1, min(tasks, max(1, len(units))))
    eff_cores = max(1, eff_tasks * max(1, workers))
    # Surcoût démarrage VM Spot / téléchargement image (~75 s pour Batch, 20 s Cloud Run, 0 s local)
    startup_sec = 0.0 if backend == "local" else (75.0 if backend == "batch" else 25.0)
    compute_wall_sec = (total_core_sec / float(eff_cores)) * 1.25  # +25 % marge déséquilibre de shards
    est_wall_sec = startup_sec + compute_wall_sec

    if backend == "local":
        est_cost_eur = 0.0
    else:
        vcpu_hours = (eff_cores * est_wall_sec) / 3600.0
        rate = _COST_EUR_PER_VCPU_HOUR_SPOT if (backend == "batch" and is_spot) else _COST_EUR_PER_VCPU_HOUR_STD
        est_cost_eur = vcpu_hours * rate

    return {
        "total_games": total_games,
        "b3_games": b3_games,
        "total_units": len(units),
        "effective_tasks": eff_tasks,
        "effective_vcpus": eff_cores,
        "est_wall_sec": round(est_wall_sec, 1),
        "est_wall_min": round(est_wall_sec / 60.0, 1),
        "est_cost_eur": round(est_cost_eur, 3),
        "llm_cost_eur": 0.0,
    }


def _format_duration_fr(seconds: float) -> str:
    if seconds < 90.0:
        return f"~{max(1, round(seconds))} s"
    minutes = seconds / 60.0
    if minutes < 90.0:
        return f"~{minutes:.1f} min"
    hours = minutes / 60.0
    return f"~{hours:.1f} h"


def format_campaign_quote_5_lines(
    manifest: dict[str, Any],
    plan: dict[str, Any],
    *,
    backend: str = "batch",
    tasks: int = 8,
    workers: int = 8,
    machine_type: str = "c3-standard-8",
    is_spot: bool = True,
    stage_summaries: list[dict[str, Any]] | None = None,
) -> str:
    """Produit un devis auteur clair et sans jargon en exactement 5 lignes avant lancement."""
    desc = str(manifest.get("description") or manifest.get("campaign_name") or "Étude v6.4").strip()
    if len(desc) > 110:
        desc = desc[:107] + "..."

    if stage_summaries:
        total_games = sum(int(s["est"]["total_games"]) for s in stage_summaries)
        total_wall_sec = sum(float(s["est"]["est_wall_sec"]) for s in stage_summaries)
        total_cost = sum(float(s["est"]["est_cost_eur"]) for s in stage_summaries)
        n_stages = len(stage_summaries)
        stage_names = ", ".join(str(s["name"]) for s in stage_summaries[:4])
        if n_stages > 4:
            stage_names += f" (+{n_stages - 4})"
        all_bots = sorted({b for s in stage_summaries for b in s["bots"]})
        all_players = sorted({n for s in stage_summaries for n in s["player_counts"]})
        line1 = f"1. Objectif      : Suite orchestrée ({n_stages} étapes) — {desc}"
        line2 = f"2. Étapes        : {stage_names}"
        line3 = (
            f"3. Tables & bots : {','.join(str(n) + 'J' for n in all_players)} | "
            f"Bots {', '.join(all_bots)}"
        )
        est_wall_str = _format_duration_fr(total_wall_sec)
        line4 = f"4. Volume & durée: {total_games:,} parties simulées ({est_wall_str})".replace(",", " ")
        infra_lbl = (
            "Local multi-cœurs (validation)"
            if backend == "local"
            else (
                f"Cloud Batch Spot ({machine_type}, {tasks}×{workers} vCPU, reprise auto)"
                if backend == "batch" and is_spot
                else f"Cloud {backend} ({tasks}×{workers} vCPU)"
            )
        )
        line5 = f"5. Infra & coût  : {infra_lbl} | Cloud ~{total_cost:.2f} € | API LLM 0,00 €"
        return f"{line1}\n{line2}\n{line3}\n{line4}\n{line5}"

    est = estimate_campaign_cost_and_duration(
        plan, backend=backend, tasks=tasks, workers=workers, is_spot=is_spot
    )
    mod_meta = plan.get("modular_study_meta")
    n_vars = len(plan.get("profile_variants", ()))
    if mod_meta:
        comp_txt = f"Tuiles à blanc `{mod_meta['study_type']}` ({n_vars} variantes CRN appariées)"
    elif plan.get("ab_tile_protocol"):
        comp_txt = f"Protocole A/B `{plan['ab_tile_protocol']}` ({n_vars} variantes CRN)"
    elif n_vars > 1:
        comp_txt = f"{n_vars} variantes de profils CRN"
    else:
        comp_txt = f"Profil unique `{plan.get('base_bundle_id', 'STANDARD_A')}` (Mode {plan.get('mode')})"

    extras: list[str] = []
    if plan.get("micro_forks"):
        extras.append(f"Micro-forks v6.4 ({len(plan.get('fork_families', ()))} familles)")
    if plan.get("include_v64_ockham_audit"):
        extras.append("Audit Ockham")
    if (plan.get("extract_remarkable_traces") or {}).get("enabled"):
        extras.append("Traces remarquables")
    if extras:
        comp_txt += " + " + ", ".join(extras)

    p_str = "/".join(f"{n}J" for n in plan.get("player_counts", ()))
    ts_str = str(plan.get("table_selection", "BALANCED_CIRCLES"))
    if ts_str == "ALL_197_ASSISES":
        tbl_lbl = "197 assises canoniques"
    elif ts_str == "BENCHMARK_ASSISES":
        tbl_lbl = "Assises repères"
    else:
        tbl_lbl = "Cercles miroirs équilibrés"
    bots_str = ", ".join(plan.get("bots", ()))

    infra_lbl = (
        f"Local ({workers} cœurs)"
        if backend == "local"
        else (
            f"Cloud Batch Spot ({machine_type}, {est['effective_tasks']}×{workers} vCPU, reprise Spot)"
            if backend == "batch" and is_spot
            else f"Cloud {backend} ({est['effective_tasks']}×{workers} vCPU)"
        )
    )

    line1 = f"1. Objectif      : {desc}"
    line2 = f"2. Étude         : {comp_txt}"
    line3 = f"3. Tables & bots : {p_str} ({tbl_lbl}) | Bots {bots_str}"
    line4 = (
        f"4. Volume & durée: {est['total_games']:,} parties ({est['total_units']} unités) | "
        f"Durée {_format_duration_fr(est['est_wall_sec'])}"
    ).replace(",", " ")
    line5 = f"5. Infra & coût  : {infra_lbl} | Cloud ~{est['est_cost_eur']:.2f} € | API LLM 0,00 €"
    return f"{line1}\n{line2}\n{line3}\n{line4}\n{line5}"


def _derive_pct_effondrement(row: dict[str, Any]) -> float | None:
    if isinstance(row.get("pct_effondrement"), (int, float)):
        return float(row["pct_effondrement"])
    p8 = row.get("pct_tour_8")
    ps = row.get("pct_reve_rang_1")
    pe = row.get("pct_reveil_gardiens")
    if isinstance(p8, (int, float)) and isinstance(ps, (int, float)) and isinstance(pe, (int, float)):
        return round(max(0.0, 100.0 - float(p8) - float(ps) - float(pe)), 2)
    return None


def _normalize_by_n_map(raw_by_n: Any) -> dict[str, dict[str, Any]]:
    if isinstance(raw_by_n, dict):
        return {str(k): v for k, v in raw_by_n.items() if isinstance(v, dict)}
    if isinstance(raw_by_n, list):
        out: dict[str, dict[str, Any]] = {}
        for item in raw_by_n:
            if isinstance(item, dict) and "n_players" in item:
                out[str(item["n_players"])] = item
        return out
    return {}


def _normalize_by_bot_map(digest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw_bb = digest.get("by_bot")
    if isinstance(raw_bb, dict) and raw_bb:
        return {str(k).upper(): v for k, v in raw_bb.items() if isinstance(v, dict)}
    raw_bm = digest.get("by_mode")
    if isinstance(raw_bm, list):
        out: dict[str, dict[str, Any]] = {}
        for item in raw_bm:
            if isinstance(item, dict) and "bot" in item:
                out[str(item["bot"]).upper()] = item
        return out
    return {}


def generate_balancing_alerts(digest: dict[str, Any]) -> list[dict[str, str]]:
    """Détecte automatiquement les anomalies d'équilibrage (format natif `docs/index.html`)."""
    alerts: list[dict[str, str]] = []

    def _add(level: str, code: str, text: str) -> None:
        alerts.append({"level": level, "code": code, "text": text})

    totals = digest.get("totals") or {}
    mean_r = totals.get("mean_ratio_arbres")
    cvar20 = totals.get("cvar20_ratio")
    p_t8 = totals.get("pct_tour_8")
    p_som = totals.get("pct_reve_rang_1")
    p_ev = totals.get("pct_reveil_gardiens")
    p_eff = _derive_pct_effondrement(totals)

    if isinstance(mean_r, (int, float)):
        if mean_r < 0.45:
            _add("danger", "SURVIE_BASSE", f"Survie globale très basse ({mean_r * 100:.1f} % < 45 %).")
        elif mean_r > 0.88:
            _add("warn", "SURVIE_HAUTE", f"Survie globale très élevée ({mean_r * 100:.1f} % > 88 %, jeu trop permissif ?).")

    if isinstance(cvar20, (int, float)):
        if cvar20 < 0.22:
            _add("danger", "CVAR20_CRITIQUE", f"Queue basse critique : CVaR20 = {cvar20 * 100:.1f} % (< 22 %).")
        elif cvar20 < 0.30:
            _add("warn", "CVAR20_FRAGILE", f"Queue basse fragile : CVaR20 = {cvar20 * 100:.1f} % (< 30 %).")

    if isinstance(p_eff, (int, float)):
        if p_eff > 25.0:
            _add("danger", "EFFONDREMENT_ELEVE", f"Taux d'effondrement élevé ({p_eff:.1f} % > 25 %).")
        elif p_eff > 15.0:
            _add("warn", "EFFONDREMENT_MODERE", f"Taux d'effondrement notable ({p_eff:.1f} % > 15 %).")

    # Équilibre des 3 fins (Mode >= 2)
    plan_blk = digest.get("plan") or {}
    mode = int(plan_blk.get("mode", 4))
    if mode >= 2 and isinstance(p_som, (int, float)) and isinstance(p_ev, (int, float)) and isinstance(p_t8, (int, float)):
        if p_som > 55.0:
            _add("warn", "SOMMEIL_DOMINANT", f"Fin par Sommeil dominante ({p_som:.1f} % > 55 %).")
        if p_ev > 65.0:
            _add("warn", "EVEIL_DOMINANT", f"Fin par Éveil dominante ({p_ev:.1f} % > 65 %).")
        if p_som < 3.0 and p_ev < 3.0 and p_t8 > 90.0:
            _add("info", "FIN_T8_EXCLUSIVE", f"Fins anticipées quasi absentes (Sommeil {p_som:.1f} %, Éveil {p_ev:.1f} %).")

    # Écart 3J-6J
    by_n = _normalize_by_n_map(digest.get("by_n_players"))
    if len(by_n) >= 2:
        n_means = [
            (str(k), float(v["mean_ratio_arbres"]))
            for k, v in by_n.items()
            if isinstance(v.get("mean_ratio_arbres"), (int, float))
        ]
        if len(n_means) >= 2:
            n_means.sort(key=lambda x: x[1])
            spread_pts = (n_means[-1][1] - n_means[0][1]) * 100.0
            if spread_pts > 10.0:
                _add(
                    "danger",
                    "ECART_3J_6J",
                    f"Écart inter-tailles fort ({spread_pts:.1f} pts : {n_means[0][0]}J={n_means[0][1]*100:.1f}% vs {n_means[-1][0]}J={n_means[-1][1]*100:.1f}%).",
                )
            elif spread_pts > 6.0:
                _add(
                    "warn",
                    "ECART_3J_6J",
                    f"Écart inter-tailles modéré ({spread_pts:.1f} pts : {n_means[0][0]}J vs {n_means[-1][0]}J).",
                )

    # Échelle bots B0 < B1 < B2 et audit anti-stratégies dégénérées B3
    by_bot = _normalize_by_bot_map(digest)
    if by_bot:
        b_means = {
            str(b).upper(): float(v["mean_ratio_arbres"])
            for b, v in by_bot.items()
            if isinstance(v.get("mean_ratio_arbres"), (int, float))
        }
        if "B0" in b_means and "B1" in b_means and b_means["B1"] < b_means["B0"] - 0.005:
            _add("danger", "BOT_ORDER_B0_B1", f"Inversion d'échelle bots : B1 ({b_means['B1']*100:.1f}%) < B0 ({b_means['B0']*100:.1f}%).")
        if "B1" in b_means and "B2" in b_means and b_means["B2"] < b_means["B1"] - 0.005:
            _add("danger", "BOT_ORDER_B1_B2", f"Inversion d'échelle bots : B2 ({b_means['B2']*100:.1f}%) < B1 ({b_means['B1']*100:.1f}%).")

    b3_audit = digest.get("b3_degenerate_audit") or {}
    if isinstance(b3_audit, dict) and b3_audit.get("enabled"):
        delta_b3_b2 = b3_audit.get("delta_b3_minus_b2_ratio")
        if isinstance(delta_b3_b2, (int, float)):
            pts = delta_b3_b2 * 100.0
            if pts > 12.0:
                _add(
                    "danger",
                    "B3_STRATEGIE_DEGENEREE",
                    f"Stratégie dégénérée potentielle détectée par B3 MCTS : B3 dépasse B2 de +{pts:.1f} pts !",
                )
            elif pts > 8.0:
                _add(
                    "warn",
                    "B3_EXPLOIT_SURVEILLER",
                    f"Écart B3 MCTS vs B2 élevé (+{pts:.1f} pts) — inspecter les traces remarquables B3.",
                )
        for end_k, shift in (b3_audit.get("ending_shifts_pts") or {}).items():
            if isinstance(shift, (int, float)) and abs(shift) >= 15.0:
                _add(
                    "warn",
                    "B3_BASCULE_FIN",
                    f"B3 MCTS décale fortement la fin `{end_k}` ({shift:+.1f} pts vs B2) — exploit possible.",
                )

    # 197 Assises Canoniques
    a197 = digest.get("assises_197_summary") or {}
    if isinstance(a197, dict) and int(a197.get("n_assises_covered", 0)) >= 6:
        worst = (a197.get("worst_assises") or [None])[0]
        best = (a197.get("best_assises") or [None])[0]
        if isinstance(worst, dict) and isinstance(best, dict):
            w_r = float(worst["mean_ratio_arbres"])
            b_r = float(best["mean_ratio_arbres"])
            sp_a = (b_r - w_r) * 100.0
            if w_r < 0.40:
                _add(
                    "danger",
                    "ASSISE_CRITIQUE",
                    f"Assise en souffrance : {worst['assise_key']} à {w_r*100:.1f} % de survie (< 40 %).",
                )
            if sp_a > 22.0:
                _add(
                    "warn",
                    "DISPERSION_197_ASSISES",
                    f"Dispersion forte sur les assises ({sp_a:.1f} pts : {worst['assise_key']}={w_r*100:.1f}% vs {best['assise_key']}={b_r*100:.1f}%).",
                )

    # Charge cognitive (`cognitive_load` ou `telemetry`)
    cog = digest.get("cognitive_load") or digest.get("telemetry") or {}
    if isinstance(cog, dict):
        law_max = float(cog.get("law_stack_max") or cog.get("max_active_laws") or 0)
        if law_max >= 4:
            _add("warn", "EMPILAGE_LOIS", f"Empilement de lois élevé (max={int(law_max)} >= 4).")
        fidd = float(cog.get("mean_fiddliness_ratio") or cog.get("mean_fiddliness_ops") or 0)
        if fidd > 1.8:
            _add("warn", "MANIPULATION_ELEVEE", f"Ratio manipulation/décision élevé ({fidd:.2f} > 1.8).")

    # Étude modulaire Tuiles à blanc (Solo, LOO, Levier Synergique, 2x2, Moteurs)
    mod_study = digest.get("modular_study") or {}
    if isinstance(mod_study, dict):
        for slot, row in (mod_study.get("solo_vs_ecosystem") or {}).items():
            if not isinstance(row, dict):
                continue
            ds = row.get("delta_solo")
            de = row.get("delta_eco")
            ls = row.get("levier_synergique")
            if isinstance(ds, (int, float)) and abs(ds) > 0.08:
                _add("warn", f"SOLO_FORT_{slot}", f"Tuile {slot} très dominante en solo ({ds*100:+.1f} pts vs ALL_NEUTRE).")
            if isinstance(de, (int, float)) and abs(de) > 0.08:
                _add("warn", f"ECO_FORT_{slot}", f"Tuile {slot} à fort impact écosystème ({de*100:+.1f} pts en retrait LOO).")
            if isinstance(ds, (int, float)) and isinstance(de, (int, float)) and abs(ds) < 0.004 and abs(de) < 0.004:
                _add("info", f"TUILE_DISCRETE_{slot}", f"Tuile {slot} quasi neutre en solo ({ds*100:+.2f} pts) et en écosystème ({de*100:+.2f} pts).")
            if isinstance(ls, (int, float)) and ls < -0.04:
                _add("warn", f"ANTISYNERGIE_{slot}", f"Anti-synergie sur {slot} : levier synergique L_syn = {ls*100:+.1f} pts.")

        for ek, erow in (mod_study.get("edges_2x2") or {}).items():
            if isinstance(erow, dict) and isinstance(erow.get("interaction_2x2"), (int, float)):
                inter = float(erow["interaction_2x2"])
                if inter < -0.04:
                    _add("warn", f"EDGE_ANTISYN_{ek}", f"Lisière 2×2 {ek} ({erow.get('slot_a')}+{erow.get('slot_b')}) : anti-synergie I_2x2 = {inter*100:+.1f} pts.")
                elif inter > 0.05:
                    _add("info", f"EDGE_SYNERGIE_{ek}", f"Lisière 2×2 {ek} ({erow.get('slot_a')}+{erow.get('slot_b')}) : forte synergie I_2x2 = {inter*100:+.1f} pts.")

    # Audit Ockham v6.4 (faux dilemmes > 90 %)
    ock = digest.get("ockham_razor") or {}
    v64_ock = ock.get("v64_decision_audit") or {}
    if isinstance(v64_ock, dict):
        flagged = v64_ock.get("flagged_false_dilemmas") or {}
        for k_int in flagged.get("internal") or []:
            info_d = (v64_ock.get("v64_internal_dilemmas") or {}).get(k_int, {})
            _add(
                "warn",
                f"FAUX_DILEMME_{k_int.upper()}",
                f"Faux dilemme v6.4 `{k_int}` : {info_d.get('dominant_choice')} choisi {info_d.get('dominant_pct', 0):.1f} % (n={info_d.get('n_decisions', 0)}).",
            )
        for k_eff in flagged.get("tile_effects") or []:
            info_e = (v64_ock.get("tile_effect_dilemmas") or {}).get(k_eff, {})
            _add(
                "warn",
                f"FAUX_DILEMME_EFFET_{k_eff.upper()}",
                f"Faux dilemme d'effet `{k_eff}` : {info_e.get('dominant_choice')} choisi {info_e.get('dominant_pct', 0):.1f} % (n={info_e.get('n_decisions', 0)}).",
            )

    # Micro-forks causaux v6.4
    forks = digest.get("forks") or {}
    if isinstance(forks, dict) and forks:
        c64 = forks.get("causal_v6_4") or forks
        dv_neg = forks.get("mean_delta_v_negociation_2_2")
        if dv_neg is None:
            dv_neg = (forks.get("step_2_2_negotiation") or {}).get("mean_delta_v_negociation")
        if isinstance(dv_neg, (int, float)) and dv_neg < -0.005:
            _add("danger", "FORK_NEGOCIATION_NEG", f"Négociation 2.2 contre-productive (Delta_V = {dv_neg*100:+.2f} pts).")
        dv_ev = (c64.get("eveil_a_plus_1") or {}).get("mean_delta_v")
        if isinstance(dv_ev, (int, float)) and dv_ev < -0.05:
            _add("warn", "FORK_EVEIL_NEG", f"Pari Éveil A+1 pénalisant en espérance ({dv_ev*100:+.2f} pts).")
        dv_alt = (c64.get("alteration") or {}).get("mean_delta_v")
        if isinstance(dv_alt, (int, float)) and dv_alt <= -0.005:
            _add("warn", "FORK_ALTERATION_NEG", f"Altération négative en fork causal ({dv_alt*100:+.2f} pts).")

    # Alimenter aussi per-tile `alerts` dans `tile_metrics` si présent
    tm = digest.get("tile_metrics")
    if isinstance(tm, dict):
        for tval in tm.values():
            if not isinstance(tval, dict):
                continue
            t_alerts = list(tval.get("alerts") or [])
            act_rate = tval.get("activations_per_game_when_present")
            if isinstance(act_rate, (int, float)) and act_rate < 0.05:
                msg = f"Sous-activée ({act_rate:.2f}/partie présente)"
                if msg not in t_alerts:
                    t_alerts.append(msg)
            if t_alerts:
                tval["alerts"] = t_alerts

    if not alerts:
        _add("info", "EQUILIBRAGE_SAIN", "Aucune anomalie critique d'équilibrage détectée sur les seuils v6.4.")
    return alerts


def _build_executive_summary_block(digest: dict[str, Any], alerts: list[dict[str, str]]) -> dict[str, Any]:
    n_danger = sum(1 for a in alerts if a.get("level") == "danger")
    n_warn = sum(1 for a in alerts if a.get("level") == "warn")
    n_info = sum(1 for a in alerts if a.get("level") == "info")
    totals = digest.get("totals") or {}
    return {
        "campaign": digest.get("campaign"),
        "verdict": (
            "ACTION_REQUISE" if n_danger > 0 else ("A_SURVEILLER" if n_warn > 0 else "SAIN")
        ),
        "alerts_counts": {"danger": n_danger, "warn": n_warn, "info": n_info},
        "total_games": totals.get("total_games", 0),
        "mean_ratio_arbres": totals.get("mean_ratio_arbres"),
        "cvar20_ratio": totals.get("cvar20_ratio"),
        "endings_pct": {
            "tour_8": totals.get("pct_tour_8"),
            "sommeil": totals.get("pct_reve_rang_1"),
            "eveil": totals.get("pct_reveil_gardiens"),
            "effondrement": _derive_pct_effondrement(totals),
        },
        "top_alerts": [a["text"] for a in alerts[:6]],
    }


def build_executive_digest(
    full_digest: dict[str, Any],
    *,
    max_bytes: int = 34_000,
    full_digest_path: str | None = None,
    report_markdown_path: str | None = None,
    traces_jsonl_path: str | None = None,
) -> dict[str, Any]:
    """Produit le digest exécutif léger (< 35 Ko) avec alertes automatiques pour `docs/digests/`."""
    enriched = dict(full_digest)
    alerts = generate_balancing_alerts(enriched)
    enriched["alerts"] = alerts
    enriched["executive_summary"] = _build_executive_summary_block(enriched, alerts)
    if report_markdown_path:
        enriched["report_markdown_path"] = report_markdown_path
    if traces_jsonl_path:
        enriched["traces_jsonl_path"] = traces_jsonl_path

    raw_len = len(json.dumps(enriched, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
    if raw_len <= max_bytes:
        enriched["digest_mode"] = "FULL"
        return enriched

    # Réduction maîtrisée < 35 Ko tout en conservant 100 % des tableaux décisionnels
    exec_d: dict[str, Any] = {}
    keep_keys = (
        "schema_version",
        "campaign",
        "description",
        "generated_at_utc",
        "digest_mode",
        "full_digest_path",
        "report_markdown_path",
        "traces_jsonl_path",
        "executive_summary",
        "alerts",
        "plan",
        "totals",
        "telemetry",
        "by_bot",
        "by_mode",
        "by_n_players",
        "b3_degenerate_audit",
        "cognitive_load",
        "forks",
        "ab_comparisons",
        "modular_study",
        "remarkable_traces",
        "stages_summary",
    )
    for k in keep_keys:
        if k in enriched:
            exec_d[k] = enriched[k]
    exec_d["digest_mode"] = "EXECUTIVE"
    if full_digest_path:
        exec_d["full_digest_path"] = full_digest_path

    if "assises_197_summary" in enriched and isinstance(enriched["assises_197_summary"], dict):
        a197 = dict(enriched["assises_197_summary"])
        a197.pop("all_assises", None)
        a197["worst_assises"] = list(a197.get("worst_assises") or [])[:10]
        a197["best_assises"] = list(a197.get("best_assises") or [])[:10]
        exec_d["assises_197_summary"] = a197

    if "ockham_razor" in enriched and isinstance(enriched["ockham_razor"], dict):
        ock = dict(enriched["ockham_razor"])
        if "v64_decision_audit" in ock and isinstance(ock["v64_decision_audit"], dict):
            va = dict(ock["v64_decision_audit"])
            eff_d = va.get("tile_effect_dilemmas") or {}
            if len(eff_d) > 12:
                ranked_eff = sorted(
                    eff_d.items(),
                    key=lambda kv: (not kv[1].get("is_false_dilemma", False), -kv[1].get("dominant_pct", 0.0)),
                )[:12]
                va["tile_effect_dilemmas"] = dict(ranked_eff)
            ock["v64_decision_audit"] = va
        exec_d["ockham_razor"] = ock

    if "by_variant" in enriched and isinstance(enriched["by_variant"], list) and len(enriched["by_variant"]) <= 20:
        exec_d["by_variant"] = enriched["by_variant"]
    if "active_core_rules" in enriched:
        cand = dict(exec_d)
        cand["active_core_rules"] = enriched["active_core_rules"]
        if len(json.dumps(cand, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) <= max_bytes:
            exec_d["active_core_rules"] = enriched["active_core_rules"]
    if "tested_tiles_rules" in enriched:
        cand = dict(exec_d)
        cand["tested_tiles_rules"] = enriched["tested_tiles_rules"]
        if len(json.dumps(cand, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) <= max_bytes:
            exec_d["tested_tiles_rules"] = enriched["tested_tiles_rules"]

    if len(json.dumps(exec_d, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) > max_bytes:
        ms = exec_d.get("modular_study")
        if isinstance(ms, dict):
            ms_c = dict(ms)
            ms_c.pop("pivot_tiles", None)
            ms_c.pop("disjoint_motors", None)
            ms_c.pop("pivot_motors", None)
            exec_d["modular_study"] = ms_c

    if len(json.dumps(exec_d, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) > max_bytes:
        exec_d.pop("by_variant", None)
        exec_d.pop("ockham_razor", None)
        if "ockham_razor" in enriched and isinstance(enriched["ockham_razor"], dict):
            v64_o = (enriched["ockham_razor"].get("v64_decision_audit") or {})
            exec_d["ockham_razor"] = {
                "flagged_false_dilemmas": v64_o.get("flagged_false_dilemmas", {}),
            }

    return exec_d


def _fmt_pct(val: Any, signed: bool = False) -> str:
    if not isinstance(val, (int, float)) or math.isnan(val):
        return "—"
    v = float(val) * 100.0
    return f"{v:+.2f} pts" if signed else f"{v:.1f} %"


def _fmt_num(val: Any, digits: int = 2) -> str:
    if not isinstance(val, (int, float)) or math.isnan(val):
        return "—"
    return f"{float(val):.{digits}f}"


def render_campaign_markdown_report(
    digest: dict[str, Any],
    *,
    report_title: str | None = None,
) -> str:
    """Génère un rapport Markdown complet, structuré et directement lisible dans `docs/rapports/`."""
    campaign = str(digest.get("campaign", "campagne_v6_4"))
    title = report_title or f"Rapport d'analyse — `{campaign}`"
    gen_at = str(digest.get("generated_at_utc", ""))
    exec_sum = digest.get("executive_summary") or {}
    alerts = digest.get("alerts") or generate_balancing_alerts(digest)
    totals = digest.get("totals") or {}
    plan = digest.get("plan") or {}
    p_eff_tot = _derive_pct_effondrement(totals)

    lines: list[str] = [
        f"# {title}",
        "",
        f"- **Campagne** : `{campaign}` | **Verdict** : `{exec_sum.get('verdict', 'N/A')}`",
        f"- **Généré (UTC)** : `{gen_at}` | **Mode** : `{plan.get('mode', '?')}` | **Parties simulées** : `{totals.get('total_games', 0):,}`".replace(",", " "),
        f"- **Tables** : `{plan.get('table_selection', 'BALANCED_CIRCLES')}` (`{plan.get('player_counts', [])}`) | **Bots** : `{', '.join(plan.get('bots', ())) or plan.get('bot', '?')}`",
    ]
    if digest.get("traces_jsonl_path"):
        lines.append(f"- **Parties remarquables (`human_trace_1.0`)** : `{digest['traces_jsonl_path']}` (ouvrable dans `docs/human_logger.html`)")
    if digest.get("full_digest_path"):
        lines.append(f"- **Digest complet (données brutes)** : `{digest['full_digest_path']}`")
    lines.append("")

    # 1. Alertes automatiques
    lines.append("## 1. Alertes automatiques d'équilibrage")
    lines.append("")
    badge_map = {"danger": "🔴 CRITIQUE", "warn": "🟠 VIGILANCE", "info": "🟢 INFO"}
    for al in alerts:
        lvl = badge_map.get(str(al.get("level", "info")), "ℹ️")
        lines.append(f"- **{lvl}** (`{al.get('code', '')}`) : {al.get('text', '')}")
    lines.append("")

    # 2. Synthèse globale
    lines.append("## 2. Indicateurs globaux")
    lines.append("")
    lines.append("| Métrique | Valeur |")
    lines.append("|---|---:|")
    lines.append(f"| Survie moyenne (ratio arbres) | {_fmt_pct(totals.get('mean_ratio_arbres'))} |")
    lines.append(f"| Queue basse CVaR20 | {_fmt_pct(totals.get('cvar20_ratio'))} |")
    lines.append(f"| Fin Tour 8 | {_fmt_num(totals.get('pct_tour_8'), 1)} % |")
    lines.append(f"| Fin Sommeil (Rêves rang 1) | {_fmt_num(totals.get('pct_reve_rang_1'), 1)} % |")
    lines.append(f"| Fin Éveil (Gardiens A+1) | {_fmt_num(totals.get('pct_reveil_gardiens'), 1)} % |")
    lines.append(f"| Effondrement (0 arbre) | {_fmt_num(p_eff_tot, 1)} % |")
    lines.append(f"| Durée moyenne | {_fmt_num(totals.get('mean_tours'), 2)} tours |")
    lines.append("")

    # 3. Spectre des bots & Audit B3
    by_bot = _normalize_by_bot_map(digest)
    if by_bot:
        lines.append("## 3. Spectre des bots (`B0` → `B3`) et détection de stratégies dégénérées")
        lines.append("")
        lines.append("| Bot | Parties | Survie | CVaR20 | Tour 8 | Sommeil | Éveil | Effondrement |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
        bot_order = ("B0", "B1", "B2", "B2_OPEN", "B3")
        ordered_bots = [b for b in bot_order if b in by_bot] + [b for b in sorted(by_bot) if b not in bot_order]
        for b in ordered_bots:
            row = by_bot[b]
            lines.append(
                f"| `{b}` | {int(row.get('n_games', 0))} | {_fmt_pct(row.get('mean_ratio_arbres'))} | "
                f"{_fmt_pct(row.get('cvar20_ratio'))} | {_fmt_num(row.get('pct_tour_8'), 1)} % | "
                f"{_fmt_num(row.get('pct_reve_rang_1'), 1)} % | {_fmt_num(row.get('pct_reveil_gardiens'), 1)} % | "
                f"{_fmt_num(_derive_pct_effondrement(row), 1)} % |"
            )
        lines.append("")

        b3_audit = digest.get("b3_degenerate_audit") or {}
        if isinstance(b3_audit, dict) and b3_audit.get("enabled"):
            lines.append("### Audit anti-stratégies dégénérées (`B3 MCTS` vs `B2`)")
            lines.append("")
            lines.append(
                f"- **Écart moyen `B3 - B2`** : {_fmt_pct(b3_audit.get('delta_b3_minus_b2_ratio'), signed=True)} "
                f"(sur {b3_audit.get('paired_tables', 0)} tables appariées CRN)"
            )
            shifts = b3_audit.get("ending_shifts_pts") or {}
            if shifts:
                sh_txt = ", ".join(f"{k}: {v:+.1f} pts" for k, v in shifts.items())
                lines.append(f"- **Décalage des fins (`B3 - B2`)** : {sh_txt}")
            if b3_audit.get("top_divergent_assises"):
                lines.append("- **Assises où B3 exploite le plus l'écart** :")
                for item in b3_audit["top_divergent_assises"][:5]:
                    lines.append(
                        f"  - `{item['assise_key']}` : B3={_fmt_pct(item['b3_ratio'])} vs B2={_fmt_pct(item['b2_ratio'])} "
                        f"(`{item['delta_ratio']*100:+.1f} pts`)"
                    )
            lines.append("")

    # 4. Équilibrage 3J–6J & 197 Assises Canoniques
    by_n = _normalize_by_n_map(digest.get("by_n_players"))
    if by_n:
        lines.append("## 4. Équilibrage par nombre de joueurs (3J–6J)")
        lines.append("")
        lines.append("| Table | Parties | Survie | CVaR20 | Tour 8 | Sommeil | Éveil | Effondrement |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
        for n_k in sorted(by_n, key=lambda x: int(x)):
            r = by_n[n_k]
            lines.append(
                f"| {n_k}J | {int(r.get('n_games', 0))} | {_fmt_pct(r.get('mean_ratio_arbres'))} | "
                f"{_fmt_pct(r.get('cvar20_ratio'))} | {_fmt_num(r.get('pct_tour_8'), 1)} % | "
                f"{_fmt_num(r.get('pct_reve_rang_1'), 1)} % | {_fmt_num(r.get('pct_reveil_gardiens'), 1)} % | "
                f"{_fmt_num(_derive_pct_effondrement(r), 1)} % |"
            )
        lines.append("")

    a197 = digest.get("assises_197_summary") or {}
    if isinstance(a197, dict) and int(a197.get("n_assises_covered", 0)) > 0:
        lines.append(
            f"### Couverture des assises canoniques ({a197['n_assises_covered']} assises / "
            f"{a197.get('n_compositions_covered', 0)} compositions)"
        )
        lines.append("")
        worst_a = a197.get("worst_assises") or []
        best_a = a197.get("best_assises") or []
        if worst_a:
            lines.append("**Pires assises (survie la plus basse)** :")
            lines.append("")
            lines.append("| Assise | Composition | Parties | Survie | Sommeil | Éveil | Effondrement |")
            lines.append("|---|---|---:|---:|---:|---:|---:|")
            for w in worst_a[:8]:
                lines.append(
                    f"| `{w['assise_key']}` | `{w.get('composition_key', '')}` | {w['n_games']} | "
                    f"{_fmt_pct(w['mean_ratio_arbres'])} | {_fmt_num(w.get('pct_reve_rang_1'), 1)} % | "
                    f"{_fmt_num(w.get('pct_reveil_gardiens'), 1)} % | {_fmt_num(w.get('pct_effondrement'), 1)} % |"
                )
            lines.append("")
        if best_a:
            lines.append("**Meilleures assises (survie la plus haute)** :")
            lines.append("")
            lines.append("| Assise | Composition | Parties | Survie | Sommeil | Éveil | Effondrement |")
            lines.append("|---|---|---:|---:|---:|---:|---:|")
            for b in best_a[:8]:
                lines.append(
                    f"| `{b['assise_key']}` | `{b.get('composition_key', '')}` | {b['n_games']} | "
                    f"{_fmt_pct(b['mean_ratio_arbres'])} | {_fmt_num(b.get('pct_reve_rang_1'), 1)} % | "
                    f"{_fmt_num(b.get('pct_reveil_gardiens'), 1)} % | {_fmt_num(b.get('pct_effondrement'), 1)} % |"
                )
            lines.append("")

    # 5. Études modulaires « Tuiles à blanc »
    mod_study = digest.get("modular_study") or {}
    if isinstance(mod_study, dict) and mod_study:
        lines.append(f"## 5. Étude modulaire « Tuiles à blanc » (`{mod_study.get('study_type', '')}`)")
        lines.append("")
        sve = mod_study.get("solo_vs_ecosystem") or {}
        if sve:
            lines.append("### Plancher Solo, Retrait Écosystème (LOO) & Levier Synergique (`L_syn = Δ_éco - Δ_solo`)")
            lines.append("")
            lines.append("| Tuile | Δ Solo (vs ALL_NEUTRE) | IC95 Solo | Δ Éco (ALL_ACTIVE - LOO) | IC95 Éco | Levier Synergique `L_syn` | p-Holm |")
            lines.append("|---|---:|---|---:|---|---:|---:|")
            for slot in sorted(sve, key=lambda s: -(abs(sve[s].get("delta_eco") or sve[s].get("delta_solo") or 0.0))):
                r = sve[slot]
                ci_s = r.get("ci95_solo")
                ci_e = r.get("ci95_eco")
                ci_s_str = f"[{ci_s[0]*100:+.1f}, {ci_s[1]*100:+.1f}]" if isinstance(ci_s, list) and len(ci_s) == 2 else "—"
                ci_e_str = f"[{ci_e[0]*100:+.1f}, {ci_e[1]*100:+.1f}]" if isinstance(ci_e, list) and len(ci_e) == 2 else "—"
                p_h = r.get("p_holm_eco") if r.get("p_holm_eco") is not None else r.get("p_holm_solo")
                lines.append(
                    f"| `{slot}` | {_fmt_pct(r.get('delta_solo'), signed=True)} | {ci_s_str} | "
                    f"{_fmt_pct(r.get('delta_eco'), signed=True)} | {ci_e_str} | "
                    f"{_fmt_pct(r.get('levier_synergique'), signed=True)} | {_fmt_num(p_h, 4)} |"
                )
            lines.append("")

        edges = mod_study.get("edges_2x2") or {}
        if edges:
            lines.append("### Carrés factoriels `2×2` des lisières (`I_2x2 = Y11 - Y10 - Y01 + Y00`)")
            lines.append("")
            lines.append("| Lisière | Paire | Fond | Y00 | Y10 (A) | Y01 (B) | Y11 (A+B) | Interaction `I_2x2` | IC95 `I_2x2` |")
            lines.append("|---|---|---|---:|---:|---:|---:|---:|---|")
            for ek in sorted(edges, key=lambda k: -abs(float(edges[k].get("interaction_2x2", 0.0)))):
                er = edges[ek]
                ci_i = er.get("ci95_interaction")
                ci_i_s = f"[{ci_i[0]*100:+.1f}, {ci_i[1]*100:+.1f}]" if isinstance(ci_i, list) and len(ci_i) == 2 else "—"
                lines.append(
                    f"| `{ek}` | `{er.get('slot_a')}`+`{er.get('slot_b')}` | `{er.get('background', 'ALL_NEUTRE')}` | "
                    f"{_fmt_pct(er.get('y00'))} | {_fmt_pct(er.get('y10'))} | {_fmt_pct(er.get('y01'))} | "
                    f"{_fmt_pct(er.get('y11'))} | {_fmt_pct(er.get('interaction_2x2'), signed=True)} | {ci_i_s} |"
                )
            lines.append("")

        motors_res = mod_study.get("motors_summary") or {}
        if motors_res:
            lines.append("### Moteurs du jeu (testés seuls vs par ablation)")
            lines.append("")
            lines.append("| Moteur | Tuiles | Δ Solo (vs ALL_NEUTRE) | Δ Ablation (ALL_ACTIVE - sans moteur) | Synergie inter-moteurs |")
            lines.append("|---|---|---:|---:|---:|")
            for m_id in sorted(motors_res):
                mr = motors_res[m_id]
                sl_txt = ",".join(mr.get("slots", []))
                lines.append(
                    f"| `{m_id}` | `{sl_txt}` | {_fmt_pct(mr.get('delta_solo'), signed=True)} | "
                    f"{_fmt_pct(mr.get('delta_ablation'), signed=True)} | {_fmt_pct(mr.get('synergy_inter_motors'), signed=True)} |"
                )
            lines.append("")

        subsets_res = mod_study.get("subsets_summary") or {}
        if subsets_res:
            lines.append("### Sous-ensembles & variantes personnalisées")
            lines.append("")
            lines.append("| Variante | Rôle | Tuiles actives | Survie | Δ vs ALL_NEUTRE | Δ vs ALL_ACTIVE |")
            lines.append("|---|---|---:|---:|---:|---:|")
            for vid, sr in subsets_res.items():
                lines.append(
                    f"| `{vid}` | `{sr.get('study_role', '')}` | {sr.get('n_active', 0)} | "
                    f"{_fmt_pct(sr.get('mean_ratio_arbres'))} | {_fmt_pct(sr.get('delta_vs_all_neutre'), signed=True)} | "
                    f"{_fmt_pct(sr.get('delta_vs_all_active'), signed=True)} |"
                )
            lines.append("")

    # 6. Micro-forks causaux v6.4
    forks = digest.get("forks") or {}
    if isinstance(forks, dict) and forks:
        lines.append("## 6. Micro-forks causaux `v6.4` (appariés CRN)")
        lines.append("")
        c64 = forks.get("causal_v6_4") or {}
        if c64:
            lines.append("| Mécanique / Décision | Ancres | ΔV moyen (survie) | Écart-type |")
            lines.append("|---|---:|---:|---:|")
            for f_key, f_val in c64.items():
                if isinstance(f_val, dict):
                    lines.append(
                        f"| `{f_key}` | {int(f_val.get('n_anchors', 0))} | "
                        f"{_fmt_pct(f_val.get('mean_delta_v'), signed=True)} | {_fmt_pct(f_val.get('sd_delta_v'))} |"
                    )
            lines.append("")

    # 7. Audit Ockham v6.4 (choix internes & faux dilemmes)
    ock = digest.get("ockham_razor") or {}
    v64_ock = ock.get("v64_decision_audit") or {}
    if isinstance(v64_ock, dict) and (v64_ock.get("v64_internal_dilemmas") or v64_ock.get("tile_effect_dilemmas")):
        lines.append("## 7. Audit Ockham — Choix internes `v6.4` et faux dilemmes (> 90 %)")
        lines.append("")
        lines.append("| Dilemme | Décisions | Choix dominant | Part dominante | Entropie norm. | Verdict |")
        lines.append("|---|---:|---|---:|---:|---|")
        for k_i, v_i in (v64_ock.get("v64_internal_dilemmas") or {}).items():
            verdict = "⚠️ FAUX DILEMME" if v_i.get("is_false_dilemma") else "OK"
            lines.append(
                f"| `{k_i}` | {v_i['n_decisions']} | `{v_i['dominant_choice']}` | "
                f"{v_i['dominant_pct']:.1f} % | {v_i['entropy_norm']:.2f} | {verdict} |"
            )
        for k_e, v_e in (v64_ock.get("tile_effect_dilemmas") or {}).items():
            verdict = "⚠️ FAUX DILEMME" if v_e.get("is_false_dilemma") else "OK"
            lines.append(
                f"| `effet:{k_e}` | {v_e['n_decisions']} | `{v_e['dominant_choice']}` | "
                f"{v_e['dominant_pct']:.1f} % | {v_e['entropy_norm']:.2f} | {verdict} |"
            )
        lines.append("")

    # 8. Parties remarquables exportées
    rem = digest.get("remarkable_traces") or {}
    if isinstance(rem, dict) and rem.get("games"):
        lines.append("## 8. Parties remarquables extraites (`human_trace_1.0`)")
        lines.append("")
        lines.append(f"Fichier exporté : `{rem.get('path', '')}` ({rem.get('n_games', 0)} parties, {rem.get('n_decisions', 0)} décisions).")
        lines.append("")
        lines.append("| Catégorie | Bot | Variante | Assise | Fin | Tour | Survie | Décisions |")
        lines.append("|---|---|---|---|---|---:|---:|---:|")
        for g in rem["games"]:
            lines.append(
                f"| `{g['category']}` | `{g['bot']}` | `{g['variant_id']}` | `{g['assise_key']}` | "
                f"`{g['cause_fin']}` | {g['tour_fin']} | {_fmt_pct(g['ratio_arbres'])} | {g['n_decisions_exported']} |"
            )
        lines.append("")

    # 9. Étapes de suite orchestrée (si campaign_suite)
    stages_sum = digest.get("stages_summary") or []
    if isinstance(stages_sum, list) and stages_sum:
        lines.append("## 9. Récapitulatif de la suite orchestrée")
        lines.append("")
        lines.append("| Étape | Parties | Survie | Alertes critiques | Alertes vigilance | Rapport |")
        lines.append("|---|---:|---:|---:|---:|---|")
        for st in stages_sum:
            lines.append(
                f"| `{st['stage_name']}` | {st.get('total_games', 0)} | {_fmt_pct(st.get('mean_ratio_arbres'))} | "
                f"{st.get('danger_alerts', 0)} | {st.get('warn_alerts', 0)} | `{st.get('report_md', '')}` |"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
