"""Constructeur de bilans de campagnes auto-portants (< 35 Ko) et dossiers Gemini Mobile/PC.

Ce module respecte l'architecture duale stricte : stdlib Python pure uniquement
(compatible PyPy 3.11 et CPython 3.12, Windows 11 et Ubuntu Linux via pathlib).
"""

from __future__ import annotations

import html
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from engine.state import CHASSIS_AXES_OPTIONS

__all__ = (
    "GEMINI_EDITORIAL_HEADER",
    "MAX_DIGEST_BYTES",
    "build_active_core_rules",
    "build_mobile_one_tap_html",
    "build_prompt_gemini_markdown",
    "build_self_contained_digest",
    "build_tested_tiles_rules",
    "decode_chassis_axes",
    "load_spec_bundle",
    "write_digest_and_prompt_files",
)

ROOT: Path = Path(__file__).resolve().parent.parent
DEFAULT_BUNDLE_PATH: Path = ROOT / "data" / "spec_bundle_v5_3_1.json"
DEFAULT_DIGESTS_DIR: Path = ROOT / "data" / "digests"
MAX_DIGEST_BYTES: int = 35_000

GEMINI_EDITORIAL_HEADER: str = (
    "Dossier de simulation Amazonia : Dernier Rempart — utilise les règles cœur et "
    "statistiques ci-dessous comme unique vérité terrain."
)


def load_spec_bundle(bundle_path: Path | None = None) -> dict[str, Any]:
    """Charge dynamiquement le `spec_bundle` actif (UTF-8)."""
    target = bundle_path if bundle_path is not None else DEFAULT_BUNDLE_PATH
    return dict(json.loads(target.read_text(encoding="utf-8")))


def decode_chassis_axes(chassis_id: int) -> dict[str, Any]:
    """Décode les valeurs exactes des 7 axes binaires d'un `chassis_id` (0..127)."""
    if not (0 <= chassis_id < 128):
        raise ValueError(f"chassis_id hors plage 0..127 : {chassis_id}")
    axes: dict[str, Any] = {"chassis_id": int(chassis_id)}
    for bit_pos, (axis_name, opts_pair) in enumerate(CHASSIS_AXES_OPTIONS):
        bit_val = (int(chassis_id) >> bit_pos) & 1
        axes[axis_name] = opts_pair[bit_val]
    return axes


def build_active_core_rules(
    chassis_ids: Sequence[int] = (0,),
    *,
    bundle: dict[str, Any] | None = None,
    bundle_path: Path | None = None,
) -> dict[str, Any]:
    """Extrait dynamiquement `active_core_rules` depuis le `spec_bundle` actif.

    Contient :
    - `version` et `source_studio_version`,
    - `studio_sha256` (empreintes SHA-256 des sources Studio),
    - `chassis_7_axes` (valeurs exactes des 7 axes de chaque châssis utilisé),
    - `tactiques` (`T1..T6`),
    - `machine_damage_rules` et `machine_deck_rules`,
    - `spec_formelle` (Étapes 1 à 6, Furtivité, chaîne des Parades / Pièges,
      Sabotage par dilution, Apprentissage, Fins `5.3`).
    """
    spec_bundle = bundle if bundle is not None else load_spec_bundle(bundle_path)
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

    sf = spec_bundle.get("spec_formelle_v5_3", {})
    av: dict[str, str] = dict(sf.get("arbitrages_valides", {}))
    etapes_raw: list[dict[str, Any]] = list(sf.get("etapes_tour", []))
    et_by_num: dict[int, dict[str, Any]] = {int(e["numero"]): e for e in etapes_raw}

    def _et_title(num: int) -> str:
        e = et_by_num.get(num, {})
        return str(e.get("nom", f"Étape {num}"))

    spec_formelle_summary: dict[str, Any] = {
        "schema_version": str(sf.get("schema_version", meta.get("schema_version", "5.3.1"))),
        "etapes_1_a_6": {
            "etape_1_PREPARATION_POSE_FURTIVITE": (
                f"{_et_title(1)} : {av.get('A01', '')} {av.get('A22', '')}".strip()
            ),
            "etape_2_REVELATION_DES_REVES_FURTIVITE": (
                f"{_et_title(2)} : {av.get('A02', '')}".strip()
            ),
            "etape_3_CONSTRUCTION_SYNERGIES": (
                f"{_et_title(3)} : {av.get('A04', '')} {av.get('A11', '')} {av.get('A21', '')}".strip()
            ),
            "etape_4_NIDS_ET_MIGRATION": (
                f"{_et_title(4)} : {av.get('A18', '')} {av.get('A17', '')}".strip()
            ),
            "etape_5_ATTAQUES_ET_TEST_FIN": (
                f"{_et_title(5)} : {av.get('A25', '')} {av.get('A19', '')} "
                f"{av.get('A08', '')} {av.get('A09', '')} {av.get('A16', '')}".strip()
            ),
            "etape_6_APPRENTISSAGE_ET_MENAGE": (
                f"{_et_title(6)} : {av.get('A12', '')} {av.get('A13', '')}".strip()
            ),
        },
        "furtivite": av.get("A03", ""),
        "chaine_parades_et_pieges": (
            f"{av.get('A20', '')} | {av.get('A06', '')} | "
            f"{av.get('A05', '')} | {av.get('A07', '')}"
        ),
        "sabotage_par_dilution": av.get("A24", ""),
        "apprentissage": f"{av.get('A23', '')} | {av.get('A10', '')}",
        "fins_5_3": f"{av.get('A14', '')} | {av.get('A15', '')}",
    }

    return {
        "version": str(meta.get("schema_version", "5.3.1")),
        "source_studio_version": str(meta.get("source_studio_version", "v5.3")),
        "studio_sha256": studio_sha256,
        "chassis_7_axes": chassis_list,
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
    by_mc = payload.get("by_mode_and_chassis")
    if isinstance(by_mc, list):
        for row in by_mc:
            if isinstance(row, dict) and "chassis_id" in row:
                found.append(int(row["chassis_id"]))
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
    return []


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

    core_rules = build_active_core_rules(resolved_chassis, bundle=spec_bundle)
    tiles_rules = build_tested_tiles_rules(resolved_tiles, bundle=spec_bundle)

    ordered: dict[str, Any] = {}
    for top_key in ("campaign", "generated_at_utc"):
        if top_key in stats_payload:
            ordered[top_key] = stats_payload[top_key]

    ordered["active_core_rules"] = core_rules
    ordered["tested_tiles_rules"] = tiles_rules

    for k, v in stats_payload.items():
        if k in ("campaign", "generated_at_utc", "active_core_rules", "tested_tiles_rules"):
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
    digests_dir: Path | None = None,
    legacy_data_copy: bool = True,
    max_bytes: int = MAX_DIGEST_BYTES,
    bundle_path: Path | None = None,
) -> tuple[Path, Path, dict[str, Any]]:
    """Écrit `data/digests/digest_<nom>.json` (< 35 Ko) et `data/digests/PROMPT_GEMINI_<nom>.md`."""
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
        # Repli compacté sans perte d'information si une campagne très dense approche 35 Ko
        raw_json = json.dumps(digest, separators=(",", ":"), ensure_ascii=False) + "\n"
        encoded_json = raw_json.encode("utf-8")

    assert len(encoded_json) < max_bytes, (
        f"Digest trop volumineux : {len(encoded_json)} >= {max_bytes} octets"
    )

    digest_path = out_dir / f"digest_{slug}.json"
    prompt_path = out_dir / f"PROMPT_GEMINI_{slug}.md"

    digest_path.write_text(raw_json, encoding="utf-8", newline="\n")
    if legacy_data_copy and out_dir.resolve() == DEFAULT_DIGESTS_DIR.resolve():
        legacy_path = ROOT / "data" / f"digest_{slug}.json"
        legacy_path.write_text(raw_json, encoding="utf-8", newline="\n")

    prompt_md = build_prompt_gemini_markdown(digest)
    prompt_path.write_text(prompt_md, encoding="utf-8", newline="\n")

    return digest_path, prompt_path, digest
