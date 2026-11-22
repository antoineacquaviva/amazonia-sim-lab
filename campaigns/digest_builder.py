"""Constructeur de bilans de campagnes auto-portants (< 35 Ko) et dossiers Gemini Mobile/PC.

Ce module respecte l'architecture duale stricte : stdlib Python pure uniquement
(compatible PyPy 3.11 et CPython 3.12, Windows 11 et Ubuntu Linux via pathlib).
"""

from __future__ import annotations

import hashlib
import html
import json
import sys
import warnings
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from engine.state import (
    CHASSIS_AXES_OPTIONS,
    NUM_CHASSIS,
    decode_chassis_index,
    encode_chassis_axes,
)

__all__ = (
    "AUTHOR_REPORTING_INSTRUCTIONS",
    "GEMINI_EDITORIAL_HEADER",
    "GEMINI_EDITORIAL_STYLE_INSTRUCTIONS",
    "MAX_DIGEST_BYTES",
    "axes_dict_to_chassis_id",
    "build_active_core_rules",
    "build_mobile_one_tap_html",
    "build_prompt_gemini_markdown",
    "build_self_contained_digest",
    "build_tested_tiles_rules",
    "chassis_id_to_studio_index",
    "chassis_id_to_studio_index_192",
    "chassis_id_to_studio_index_384",
    "decode_chassis_axes",
    "load_spec_bundle",
    "studio_index_192_to_chassis_id",
    "studio_index_384_to_chassis_id",
    "studio_index_to_chassis_id",
    "write_digest_and_prompt_files",
)

ROOT: Path = Path(__file__).resolve().parent.parent
DEFAULT_BUNDLE_PATH: Path = ROOT / "data" / "spec_bundle_v5_5.json"
DEFAULT_DIGESTS_DIR: Path = ROOT / "data" / "digests"
MAX_DIGEST_BYTES: int = 35_000

GEMINI_EDITORIAL_HEADER: str = (
    "Dossier de simulation Amazonia : Dernier Rempart — utilise les règles cœur et "
    "statistiques ci-dessous comme unique vérité terrain."
)

GEMINI_EDITORIAL_STYLE_INSTRUCTIONS: str = (
    "Consignes de restitution pour l'auteur :\n"
    "- Rédige ton rapport en français naturel, clair et fluide, directement adressé à l'auteur du jeu.\n"
    "- Zéro code interne, zéro nom de variable, zéro identifiant de variante, zéro numéro de règle ou d'étape, zéro jargon statistique brut : traduis systématiquement chaque notion en langage concret de jeu de société (par exemple : joueurs débutants / intermédiaires / aguerris plutôt que les noms de bots ; les 20 % pires parties plutôt que le sigle statistique ; description claire de chaque variante testée).\n"
    "- Structure le rapport en 4 temps : 1) Hauteur de vue par rapport aux travaux en cours et aux intentions d'auteur ; 2) Chiffres clés essentiels et parlants ; 3) Constats majeurs (ce qui fonctionne, ce qui coince, sensations à table de 3 à 6 joueurs) ; 4) Préconisations hiérarchisées pour la suite.\n"
    "- Si tu proposes un prompt technique destiné à Antigravity, place-le uniquement à la toute fin dans un encart séparé « Annexe technique (pour Antigravity) »."
)

AUTHOR_REPORTING_INSTRUCTIONS: dict[str, Any] = {
    "public": "Auteur du jeu (restitution éditoriale en français courant)",
    "interdits": (
        "Aucun code interne, nom de variable, identifiant de variante, numéro d'étape/règle "
        "ni sigle statistique brut dans le corps du rapport."
    ),
    "traduction_obligatoire": (
        "Traduire chaque indicateur et variante en langage concret de jeu de société "
        "(ex. joueurs débutants/intermédiaires/aguerris, pires 20 % de parties, description claire des règles testées)."
    ),
    "structure_attendue": [
        "1. Hauteur de vue (lien avec les travaux en cours et les intentions d'auteur)",
        "2. Chiffres clés (essentiels, lisibles et contextualisés)",
        "3. Constats majeurs (forces, fragilités, sensations de 3 à 6 joueurs)",
        "4. Préconisations pour la suite (arbitrages concrets et hiérarchisés)",
    ],
    "annexe_technique": (
        "Si un prompt technique pour Antigravity est utile, l'isoler en toute fin dans un encart séparé."
    ),
}

_STEP_ARBITRAGES_MAP: dict[int, tuple[str, ...]] = {
    1: ("A01", "A22"),
    2: ("A03",),
    3: ("A04", "A11", "A21", "A02"),
    4: ("A24", "A18", "A17"),
    5: ("A25", "A19", "A08", "A09", "A16"),
    6: ("A12", "A13"),
}


def load_spec_bundle(bundle_path: Path | None = None) -> dict[str, Any]:
    """Charge dynamiquement le `spec_bundle` actif (UTF-8)."""
    target = bundle_path if bundle_path is not None else DEFAULT_BUNDLE_PATH
    return dict(json.loads(target.read_text(encoding="utf-8")))


def chassis_id_to_studio_index(chassis_id: int) -> int:
    """Convertit un `chassis_id` moteur (0..191, LSB = Profil_Piste) en `config_index_192` Studio (1..192, MSB = Profil_Piste)."""
    if not (0 <= chassis_id < NUM_CHASSIS):
        raise ValueError(f"chassis_id hors plage 0..{NUM_CHASSIS - 1} : {chassis_id}")
    decoded = decode_chassis_index(int(chassis_id))
    studio_zero = 0
    for axis_name, opts in CHASSIS_AXES_OPTIONS:
        studio_zero = studio_zero * len(opts) + opts.index(decoded[axis_name])
    return studio_zero + 1


def studio_index_to_chassis_id(studio_index: int) -> int:
    """Convertit un `config_index_192` Doc Studio (1..192) en `chassis_id` moteur (0..191)."""
    if not (1 <= studio_index <= NUM_CHASSIS):
        raise ValueError(f"studio_index hors plage 1..{NUM_CHASSIS} : {studio_index}")
    rem = int(studio_index) - 1
    digits_rev: list[int] = []
    for _axis_name, opts in reversed(CHASSIS_AXES_OPTIONS):
        radix = len(opts)
        digits_rev.append(rem % radix)
        rem //= radix
    digits = list(reversed(digits_rev))
    chassis_id = 0
    mult = 1
    for ax_idx, (_axis_name, opts) in enumerate(CHASSIS_AXES_OPTIONS):
        chassis_id += digits[ax_idx] * mult
        mult *= len(opts)
    return chassis_id


chassis_id_to_studio_index_192 = chassis_id_to_studio_index
studio_index_192_to_chassis_id = studio_index_to_chassis_id
chassis_id_to_studio_index_384 = chassis_id_to_studio_index
studio_index_384_to_chassis_id = studio_index_to_chassis_id


def axes_dict_to_chassis_id(axes: Mapping[str, Any]) -> int:
    """Encode un dictionnaire d'axes nommés (clés moteur ou Doc Studio, insensible à la casse) en `chassis_id` (0..191)."""
    lowered = {str(k).lower(): v for k, v in axes.items()}
    normalized: dict[str, Any] = {}
    for axis_name, opts in CHASSIS_AXES_OPTIONS:
        raw = lowered.get(axis_name.lower(), opts[0])
        matched = False
        for opt in opts:
            if raw == opt or str(raw).strip().upper() == str(opt).strip().upper():
                normalized[axis_name] = opt
                matched = True
                break
        if not matched:
            raise ValueError(
                f"Valeur invalide pour l'axe {axis_name!r} : {raw!r} (attendu {opts!r})"
            )
    return encode_chassis_axes(normalized)


def decode_chassis_axes(chassis_id: int) -> dict[str, Any]:
    """Décode les valeurs exactes des 6 axes d'un `chassis_id` (0..191) avec son `studio_config_index_192` (1..192)."""
    if not (0 <= chassis_id < NUM_CHASSIS):
        raise ValueError(f"chassis_id hors plage 0..{NUM_CHASSIS - 1} : {chassis_id}")
    decoded = decode_chassis_index(int(chassis_id))
    axes: dict[str, Any] = {
        "chassis_id": int(chassis_id),
        "studio_config_index_192": chassis_id_to_studio_index(int(chassis_id)),
    }
    for axis_name, _opts in CHASSIS_AXES_OPTIONS:
        axes[axis_name] = decoded[axis_name]
    return axes


def build_active_core_rules(
    chassis_ids: Sequence[int] = (0,),
    *,
    bundle: dict[str, Any] | None = None,
    bundle_path: Path | None = None,
) -> dict[str, Any]:
    """Extrait dynamiquement `active_core_rules` depuis le `spec_bundle` actif.

    Contient :
    - `version`, `source_studio_version` et `spec_bundle_sha256`,
    - `studio_sha256` (empreintes SHA-256 des sources Studio JSON & JS),
    - `chassis_6_axes` (valeurs exactes des 6 axes + `chassis_id` 0..191 + `studio_config_index_192` 1..192),
    - `tactiques` (`T1..T6` imprimées en dur),
    - `machine_damage_rules` et `machine_deck_rules`,
    - `spec_formelle` (Étapes 1 à 6 issues dynamiquement de `etapes_tour`, Furtivité,
      chaîne des Parades / Pièges, Sabotage par dilution, Activation des Rêves, Fins `5.3`).
    """
    target_path = bundle_path if bundle_path is not None else DEFAULT_BUNDLE_PATH
    if bundle is not None:
        spec_bundle = bundle
        bundle_sha256 = hashlib.sha256(
            json.dumps(spec_bundle, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()
    else:
        raw_bundle = target_path.read_bytes()
        bundle_sha256 = hashlib.sha256(raw_bundle).hexdigest()
        spec_bundle = dict(json.loads(raw_bundle.decode("utf-8")))

    meta = spec_bundle.get("meta", {})
    raw_sha = meta.get("studio_sha256", {})
    studio_sha256: dict[str, str] = {}
    for fname, info in raw_sha.items():
        if isinstance(info, dict) and "sha256" in info:
            studio_sha256[str(fname)] = str(info["sha256"])
        else:
            studio_sha256[str(fname)] = str(info)

    unique_chassis = tuple(dict.fromkeys(int(c) for c in (chassis_ids or (0,))))
    chassis_list = [decode_chassis_axes(cid) for cid in unique_chassis]

    sf = spec_bundle.get("spec_formelle_v5_5") or spec_bundle.get("spec_formelle_v5_4") or {}
    av: dict[str, str] = dict(sf.get("arbitrages_valides", {}))
    etapes_raw: list[dict[str, Any]] = sorted(
        sf.get("etapes_tour", []),
        key=lambda e: int(e.get("numero", 0)),
    )

    etapes_1_a_6: dict[str, str] = {}
    for et in etapes_raw:
        num = int(et.get("numero", 0))
        code = str(et.get("code", f"ETAPE_{num}"))
        nom = str(et.get("nom", f"Étape {num}"))
        arb_codes = _STEP_ARBITRAGES_MAP.get(num, ())
        arb_txt = " ".join(av.get(ac, "") for ac in arb_codes if av.get(ac)).strip()
        etapes_1_a_6[f"etape_{num}_{code}"] = f"{nom} : {arb_txt}".strip(" :")

    spec_formelle_summary: dict[str, Any] = {
        "schema_version": str(sf.get("schema_version", meta.get("schema_version", "5.5.0"))),
        "etapes_1_a_6": etapes_1_a_6,
        "furtivite": av.get("A03", ""),
        "chaine_parades_et_pieges": (
            f"{av.get('A20', '')} | {av.get('A06', '')} | "
            f"{av.get('A05', '')} | {av.get('A07', '')}"
        ),
        "sabotage_par_dilution": av.get("A24", ""),
        "piste_tactiques_fixe_et_reves": f"{av.get('A11', '')} | {av.get('A21', '')}",
        "fins_5_3": f"{av.get('A14', '')} | {av.get('A15', '')}",
    }

    return {
        "version": str(meta.get("schema_version", "5.5.0")),
        "source_studio_version": str(meta.get("source_studio_version", "v5.5")),
        "spec_bundle_sha256": bundle_sha256,
        "studio_sha256": studio_sha256,
        "chassis_6_axes": chassis_list,
        "tactiques": list(spec_bundle.get("tactiques", [])),
        "machine_damage_rules": dict(spec_bundle.get("machine_damage_rules", {})),
        "machine_deck_rules": dict(spec_bundle.get("machine_deck_rules", {})),
        "spec_formelle": spec_formelle_summary,
    }


def _parse_tile_pair(item: str | Sequence[str]) -> tuple[str, str]:
    if isinstance(item, str):
        if ":" not in item:
            raise ValueError(f"Profil de tuile invalide (attendu 'SLOT:PROFIL') : {item!r}")
        slot_id, prof_key = item.split(":", 1)
        return slot_id.strip(), prof_key.strip()
    if len(item) != 2:
        raise ValueError(f"Tuple de tuile invalide (attendu (slot, profil)) : {item!r}")
    return str(item[0]).strip(), str(item[1]).strip()


def build_tested_tiles_rules(
    tile_profiles: Sequence[str | Sequence[str]] = (),
    *,
    bundle: dict[str, Any] | None = None,
    bundle_path: Path | None = None,
) -> list[dict[str, str]]:
    """Extrait (`slot`, `profil`, `nom`, `famille`, `texte`) des seules tuiles évaluées."""
    if not tile_profiles:
        return []
    spec_bundle = bundle if bundle is not None else load_spec_bundle(bundle_path)
    catalogue: dict[str, Any] = dict(spec_bundle.get("catalogue_tuiles", {}))

    seen: set[tuple[str, str]] = set()
    out: list[dict[str, str]] = []
    for raw_item in tile_profiles:
        slot_id, prof_key = _parse_tile_pair(raw_item)
        if (slot_id, prof_key) in seen:
            continue
        seen.add((slot_id, prof_key))
        if slot_id not in catalogue:
            raise KeyError(f"Emplacement de tuile inconnu dans spec_bundle : {slot_id!r}")
        slot_obj = catalogue[slot_id]
        profils_map = slot_obj.get("profils", {})
        if prof_key not in profils_map:
            raise KeyError(f"Profil {prof_key!r} inconnu pour l'emplacement {slot_id!r}")
        prof_obj = profils_map[prof_key]
        out.append(
            {
                "slot": slot_id,
                "profil": prof_key,
                "nom": str(prof_obj.get("nom", slot_obj.get("nomBase", slot_id))),
                "famille": str(slot_obj.get("famille", "")),
                "texte": str(prof_obj.get("texte", "")),
            }
        )
    return out


def _infer_chassis_ids_from_payload(payload: dict[str, Any]) -> tuple[int, ...]:
    found: list[int] = []
    for list_key in ("by_mode_and_chassis", "by_chassis"):
        rows = payload.get(list_key)
        if isinstance(rows, list):
            for row in rows:
                if isinstance(row, dict) and "chassis_id" in row:
                    found.append(int(row["chassis_id"]))
        if found:
            break
    if not found:
        found.append(0)
    return tuple(dict.fromkeys(found))


def _infer_tested_tiles_from_payload(payload: dict[str, Any]) -> list[str]:
    totals = payload.get("totals")
    if isinstance(totals, dict):
        for key in ("tested_tiles", "lot_01_profiles", "tile_profiles"):
            val = totals.get(key)
            if isinstance(val, list) and val:
                return [str(x) for x in val]
    tile_metrics = payload.get("tile_metrics")
    if isinstance(tile_metrics, dict) and tile_metrics:
        return [str(k) for k in tile_metrics if ":" in str(k)]
    return []


def _infer_varying_tile_pairs(
    payload: dict[str, Any],
    tested_tiles_rules: Sequence[Mapping[str, Any]],
) -> set[tuple[str, str]]:
    """Identifie les tuiles (slot, profil) qui varient réellement dans la campagne."""
    varying: set[tuple[str, str]] = set()
    tile_metrics = payload.get("tile_metrics")
    if isinstance(tile_metrics, dict):
        for tok in tile_metrics:
            s_tok = str(tok)
            if ":" in s_tok:
                varying.add(_parse_tile_pair(s_tok))

    by_variant = payload.get("by_variant")
    if isinstance(by_variant, list):
        for row in by_variant:
            if not isinstance(row, dict):
                continue
            vid = str(row.get("variant_id", ""))
            for part in vid.split(","):
                part_clean = part.strip()
                if ":" in part_clean:
                    varying.add(_parse_tile_pair(part_clean))

    # Ajoute tout emplacement présent sous >= 2 profils distincts dans tested_tiles_rules
    by_slot: dict[str, list[str]] = {}
    for entry in tested_tiles_rules:
        s_id = str(entry.get("slot", "")).strip()
        p_id = str(entry.get("profil", "")).strip()
        if s_id and p_id:
            by_slot.setdefault(s_id, []).append(p_id)
    for s_id, profs in by_slot.items():
        if len(set(profs)) >= 2:
            for p_id in profs:
                varying.add((s_id, p_id))
    return varying


def build_self_contained_digest(
    stats_payload: dict[str, Any],
    *,
    chassis_ids: Sequence[int] | None = None,
    tested_tiles: Sequence[str | Sequence[str]] | None = None,
    bundle: dict[str, Any] | None = None,
    bundle_path: Path | None = None,
) -> dict[str, Any]:
    """Assemble un digest 100 % auto-portant (`active_core_rules` + `tested_tiles_rules` + stats)."""
    spec_bundle = bundle if bundle is not None else load_spec_bundle(bundle_path)
    resolved_chassis = (
        tuple(int(c) for c in chassis_ids)
        if chassis_ids is not None
        else _infer_chassis_ids_from_payload(stats_payload)
    )
    resolved_tiles = (
        tested_tiles
        if tested_tiles is not None
        else _infer_tested_tiles_from_payload(stats_payload)
    )

    core_rules = build_active_core_rules(
        resolved_chassis, bundle=bundle, bundle_path=bundle_path
    )
    tiles_rules = build_tested_tiles_rules(resolved_tiles, bundle=spec_bundle)

    ordered: dict[str, Any] = {}
    for top_key in ("campaign", "generated_at_utc"):
        if top_key in stats_payload:
            ordered[top_key] = stats_payload[top_key]

    ordered["consignes_restitution_auteur"] = dict(AUTHOR_REPORTING_INSTRUCTIONS)
    ordered["active_core_rules"] = core_rules
    ordered["tested_tiles_rules"] = tiles_rules

    for k, v in stats_payload.items():
        if k in (
            "campaign",
            "generated_at_utc",
            "consignes_restitution_auteur",
            "active_core_rules",
            "tested_tiles_rules",
        ):
            continue
        ordered[k] = v

    return ordered


def build_prompt_gemini_markdown(digest: dict[str, Any]) -> str:
    """Construit le dossier Markdown prêt-à-coller `PROMPT_GEMINI_<nom>.md` (UTF-8 sans BOM, LF)."""
    raw_json = json.dumps(digest, indent=2, ensure_ascii=False)
    if len(raw_json.encode("utf-8")) >= MAX_DIGEST_BYTES:
        raw_json = json.dumps(digest, separators=(",", ":"), ensure_ascii=False)
    lines = [
        GEMINI_EDITORIAL_HEADER,
        "",
        GEMINI_EDITORIAL_STYLE_INSTRUCTIONS,
        "",
        "```json",
        raw_json,
        "```",
        "",
    ]
    return "\n".join(lines)


def build_mobile_one_tap_html(
    campaign_slug: str,
    prompt_markdown: str,
    digest: dict[str, Any],
) -> str:
    """Construit la mini-page HTML mobile-first 1-Tap (`last_digest.html` / `latest.html`)."""
    generated_at = html.escape(str(digest.get("generated_at_utc", "")))
    camp_title = html.escape(str(digest.get("campaign", campaign_slug)))
    core_ver = html.escape(
        str(digest.get("active_core_rules", {}).get("version", "5.3.1"))
    )
    prompt_escaped = html.escape(prompt_markdown)
    md_filename = html.escape(f"PROMPT_GEMINI_{campaign_slug}.md")
    json_filename = html.escape(f"digest_{campaign_slug}.json")

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
  <title>Amazonia Sim Lab — {camp_title}</title>
  <style>
    :root {{
      --bg: #0f1f17;
      --card: #172e23;
      --accent: #34d399;
      --accent-dark: #059669;
      --text: #ecfdf5;
      --muted: #a7f3d0;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 16px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.45;
    }}
    .card {{
      max-width: 640px;
      margin: 0 auto;
      background: var(--card);
      border: 1px solid #264a39;
      border-radius: 16px;
      padding: 18px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.35);
    }}
    h1 {{
      font-size: 1.2rem;
      margin: 0 0 6px 0;
      color: var(--accent);
    }}
    .meta {{
      font-size: 0.85rem;
      color: var(--muted);
      margin-bottom: 16px;
    }}
    .btn-primary {{
      display: block;
      width: 100%;
      padding: 16px 14px;
      font-size: 1.05rem;
      font-weight: 700;
      text-align: center;
      color: #06281b;
      background: var(--accent);
      border: none;
      border-radius: 12px;
      cursor: pointer;
      margin-bottom: 12px;
    }}
    .btn-primary:active {{
      background: var(--accent-dark);
      color: #ffffff;
    }}
    .btn-secondary {{
      display: inline-block;
      width: 100%;
      padding: 12px;
      font-size: 0.92rem;
      font-weight: 600;
      text-align: center;
      color: var(--text);
      background: #214031;
      border: 1px solid #35634d;
      border-radius: 10px;
      text-decoration: none;
      cursor: pointer;
      margin-bottom: 14px;
    }}
    .status {{
      min-height: 22px;
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--accent);
      text-align: center;
      margin-bottom: 10px;
    }}
    textarea {{
      width: 100%;
      height: 240px;
      background: #09140e;
      color: #d1fae5;
      border: 1px solid #2d5440;
      border-radius: 10px;
      padding: 10px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.78rem;
    }}
  </style>
</head>
<body>
  <div class="card">
    <h1>🌿 Amazonia : Dernier Rempart</h1>
    <div class="meta">
      Campagne : <strong>{camp_title}</strong> · Règles cœur <strong>v{core_ver}</strong><br>
      Généré (UTC) : {generated_at} · Fichier : <code>{json_filename}</code>
    </div>
    <button id="copyBtn" class="btn-primary" type="button" onclick="copyDossier()">
      📋 Copier tout le dossier pour l'app Gemini
    </button>
    <div id="statusMsg" class="status"></div>
    <button class="btn-secondary" type="button" onclick="downloadMarkdown()">
      ⬇️ Télécharger {md_filename}
    </button>
    <textarea id="promptBox" readonly>{prompt_escaped}</textarea>
  </div>
  <script>
    function copyDossier() {{
      const box = document.getElementById('promptBox');
      const status = document.getElementById('statusMsg');
      const text = box.value;
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(text).then(function() {{
          status.textContent = "✅ Dossier copié ! Ouvrez l'app Gemini et collez.";
        }}).catch(function() {{
          fallbackCopy(box, status);
        }});
      }} else {{
        fallbackCopy(box, status);
      }}
    }}
    function fallbackCopy(box, status) {{
      box.focus();
      box.select();
      box.setSelectionRange(0, box.value.length);
      document.execCommand('copy');
      status.textContent = "✅ Dossier copié ! Ouvrez l'app Gemini et collez.";
    }}
    function downloadMarkdown() {{
      const text = document.getElementById('promptBox').value;
      const blob = new Blob([text], {{ type: 'text/markdown;charset=utf-8' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = "{md_filename}";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }}
  </script>
</body>
</html>
"""


def write_digest_and_prompt_files(
    campaign_slug: str,
    stats_payload: dict[str, Any],
    *,
    chassis_ids: Sequence[int] | None = None,
    tested_tiles: Sequence[str | Sequence[str]] | None = None,
    varying_tiles: Sequence[str | Sequence[str]] | None = None,
    digests_dir: Path | None = None,
    legacy_data_copy: bool = True,
    max_bytes: int = MAX_DIGEST_BYTES,
    bundle_path: Path | None = None,
) -> tuple[Path, Path, dict[str, Any]]:
    """Écrit `data/digests/digest_<nom>.json` (cible < 35 Ko, non bloquant) et `PROMPT_GEMINI_<nom>.md`."""
    slug = campaign_slug.strip()
    slug = slug.removeprefix("digest_")
    slug = slug.removesuffix(".json")

    out_dir = digests_dir if digests_dir is not None else DEFAULT_DIGESTS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    digest = build_self_contained_digest(
        stats_payload,
        chassis_ids=chassis_ids,
        tested_tiles=tested_tiles,
        bundle_path=bundle_path,
    )

    raw_json = json.dumps(digest, indent=2, ensure_ascii=False) + "\n"
    encoded_json = raw_json.encode("utf-8")
    if len(encoded_json) >= max_bytes:
        # Repli compacté sans perte d'information si une campagne dense approche 35 Ko
        raw_json = json.dumps(digest, separators=(",", ":"), ensure_ascii=False) + "\n"
        encoded_json = raw_json.encode("utf-8")

    if len(encoded_json) >= max_bytes:
        # Si le budget cible est encore dépassé, privilégier les tuiles qui varient dans tested_tiles_rules
        current_tiles = list(digest.get("tested_tiles_rules", []))
        if current_tiles:
            varying_pairs: set[tuple[str, str]] = (
                {_parse_tile_pair(item) for item in varying_tiles}
                if varying_tiles is not None
                else _infer_varying_tile_pairs(digest, current_tiles)
            )
            if varying_pairs:
                prioritized = [
                    entry
                    for entry in current_tiles
                    if (str(entry.get("slot", "")), str(entry.get("profil", "")))
                    in varying_pairs
                ]
                if prioritized and len(prioritized) < len(current_tiles):
                    digest["tested_tiles_rules"] = prioritized
                    raw_json = (
                        json.dumps(digest, separators=(",", ":"), ensure_ascii=False) + "\n"
                    )
                    encoded_json = raw_json.encode("utf-8")

    if len(encoded_json) >= max_bytes:
        msg = (
            f"Digest '{slug}' dépasse le budget cible ({len(encoded_json)} >= {max_bytes} octets) "
            "— conservé en JSON compact sans blocage."
        )
        warnings.warn(msg, UserWarning, stacklevel=2)
        print(f"[AVERTISSEMENT] {msg}", file=sys.stderr, flush=True)

    digest_path = out_dir / f"digest_{slug}.json"
    prompt_path = out_dir / f"PROMPT_GEMINI_{slug}.md"

    digest_path.write_text(raw_json, encoding="utf-8", newline="\n")
    if legacy_data_copy and out_dir.resolve() == DEFAULT_DIGESTS_DIR.resolve():
        legacy_path = ROOT / "data" / f"digest_{slug}.json"
        legacy_path.write_text(raw_json, encoding="utf-8", newline="\n")

    prompt_md = build_prompt_gemini_markdown(digest)
    prompt_path.write_text(prompt_md, encoding="utf-8", newline="\n")

    return digest_path, prompt_path, digest
