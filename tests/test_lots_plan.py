"""Vérification automatisée du plan des 11 lots (100/100 profils) et des 4 skills autonomes."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SPEC_BUNDLE_PATH = ROOT / "data" / "spec_bundle_v5_3_1.json"
MODE3_REF_PATH = ROOT / "engine" / "effects" / "mode3_reference.json"
LOTS_PLAN_PATH = ROOT / "contracts" / "LOTS_PLAN.md"
STATUS_PATH = ROOT / "STATUS.md"

SKILL_NAMES: tuple[str, ...] = (
    "palier-2",
    "code-lot",
    "run-campaign",
    "palier-4-canon",
)

SECTION_HEADER_RE = re.compile(r"^###\s+(Socle|Lot\s+\d{2})\b", re.MULTILINE)
PROFILES_LINE_RE = re.compile(r"^-\s+Profils\s*:\s*(.+)$", re.MULTILINE)
TOKEN_RE = re.compile(r"`([A-Z0-9_]+:[A-D])`")


def _parse_lots_from_markdown(md_text: str) -> dict[str, list[tuple[str, str]]]:
    matches = list(SECTION_HEADER_RE.finditer(md_text))
    parsed: dict[str, list[tuple[str, str]]] = {}
    for idx, match in enumerate(matches):
        section_key = match.group(1)
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(md_text)
        body = md_text[start:end]
        prof_match = PROFILES_LINE_RE.search(body)
        if prof_match is None:
            parsed[section_key] = []
            continue
        pairs: list[tuple[str, str]] = []
        for tok in TOKEN_RE.findall(prof_match.group(1)):
            slot_id, prof = tok.split(":", maxsplit=1)
            pairs.append((slot_id, prof))
        parsed[section_key] = pairs
    return parsed


def _load_spec_profiles() -> tuple[set[tuple[str, str]], dict[tuple[str, str], str]]:
    data = json.loads(SPEC_BUNDLE_PATH.read_text(encoding="utf-8"))
    cat = data["catalogue_tuiles"]
    all_pairs: set[tuple[str, str]] = set()
    family_by_pair: dict[tuple[str, str], str] = {}
    for slot_id, slot_obj in cat.items():
        fam = str(slot_obj["famille"])
        for prof in slot_obj["profils"]:
            pair = (str(slot_id), str(prof))
            all_pairs.add(pair)
            family_by_pair[pair] = fam
    return all_pairs, family_by_pair


def test_lots_plan_exact_100_profiles_partition() -> None:
    spec_pairs, family_by_pair = _load_spec_profiles()
    assert len(spec_pairs) == 100

    md_text = LOTS_PLAN_PATH.read_text(encoding="utf-8")
    parsed = _parse_lots_from_markdown(md_text)

    expected_keys = ["Socle", *(f"Lot {i:02d}" for i in range(1, 12))]
    assert list(parsed.keys()) == expected_keys

    assert set(parsed["Socle"]) == {
        ("SLOT_BUG_CERVEAU", "A"),
        ("SLOT_COLONISATION_GARDIENS", "A"),
    }
    assert set(parsed["Lot 01"]) == {
        ("G1", "A"),
        ("G2", "A"),
        ("G4", "A"),
        ("G6", "A"),
        ("G7", "A"),
        ("G10", "A"),
        ("R5", "A"),
        ("G9", "C"),
    }
    assert parsed["Lot 11"] == []

    # Aucun doublon à travers Socle + Lots 01..10, et union == 100 profils exacts
    ordered_all: list[tuple[str, str]] = []
    for key in ["Socle", *(f"Lot {i:02d}" for i in range(1, 11))]:
        lot_items = parsed[key]
        assert len(lot_items) >= 2
        ordered_all.extend(lot_items)

    assert len(ordered_all) == 100, f"Total attendu 100, obtenu {len(ordered_all)}"
    assert len(set(ordered_all)) == 100, "Doublon détecté dans contracts/LOTS_PLAN.md"
    assert set(ordered_all) == spec_pairs

    # Jalons de clôture par famille : G + Migration à Lot 05, R à Lot 08, M à Lot 10
    up_to_lot_05 = {
        p for k in ["Socle", *(f"Lot {i:02d}" for i in range(1, 6))] for p in parsed[k]
    }
    g_and_mig = {p for p, fam in family_by_pair.items() if fam in ("GARDIEN", "MIGRATION")}
    assert len(g_and_mig) == 50
    assert g_and_mig.issubset(up_to_lot_05)

    up_to_lot_08 = {
        p for k in ["Socle", *(f"Lot {i:02d}" for i in range(1, 9))] for p in parsed[k]
    }
    reves = {p for p, fam in family_by_pair.items() if fam == "REVE"}
    assert len(reves) == 31
    assert reves.issubset(up_to_lot_08)

    croissance = {p for p, fam in family_by_pair.items() if fam == "CROISSANCE"}
    assert len(croissance) == 19
    assert croissance.issubset(set(ordered_all))

    # Vérifie aussi que les 32 sélections de mode3_reference.json sont couvertes
    mode3_data = json.loads(MODE3_REF_PATH.read_text(encoding="utf-8"))
    mode3_pairs = {
        (str(s), str(info["profile"])) for s, info in mode3_data["selections"].items()
    }
    assert len(mode3_pairs) == 32
    assert mode3_pairs.issubset(set(ordered_all))


def test_status_checklist_and_autonomous_skills_valid() -> None:
    status_text = STATUS_PATH.read_text(encoding="utf-8")
    for lot_num in range(1, 12):
        assert f"**Lot {lot_num:02d}" in status_text, f"Lot {lot_num:02d} absent de STATUS.md"

    for skill_name in SKILL_NAMES:
        skill_path = ROOT / ".agents" / "skills" / skill_name / "SKILL.md"
        assert skill_path.exists(), f"Skill manquante : {skill_path}"
        content = skill_path.read_text(encoding="utf-8")
        assert content.startswith("---\n"), f"Frontmatter YAML manquant dans {skill_path}"
        end_fm = content.find("\n---\n", 4)
        assert end_fm > 0, f"Fermeture frontmatter YAML manquante dans {skill_path}"
        fm = content[4:end_fm]
        assert f"name: {skill_name}" in fm, f"Champ name invalide dans {skill_path}"
        assert "description:" in fm, f"Champ description manquant dans {skill_path}"


@pytest.mark.parametrize(
    "rel_path",
    [
        "contracts/LOTS_PLAN.md",
        "STATUS.md",
        "tests/test_lots_plan.py",
        ".agents/skills/palier-2/SKILL.md",
        ".agents/skills/code-lot/SKILL.md",
        ".agents/skills/run-campaign/SKILL.md",
        ".agents/skills/palier-4-canon/SKILL.md",
    ],
)
def test_autonomy_kit_utf8_no_bom_and_lf(rel_path: str) -> None:
    raw = (ROOT / rel_path).read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), f"BOM UTF-8 interdit dans {rel_path}"
    assert b"\r\n" not in raw, f"CRLF interdit dans {rel_path} (LF requis)"
    raw.decode("utf-8")
