"""Synchronise les contrats JSON depuis amazonia-doc-studio vers data/ avec verrou SHA-256."""

from __future__ import annotations

import hashlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts_cloud.studio_paths import resolve_studio_dir

DATA_DIR = ROOT / "data"
STUDIO_RAW_BASE = "https://raw.githubusercontent.com/antoineacquaviva/amazonia-doc-studio/main/data"
STUDIO_JSON_FILES = ("catalog_v5_5.json", "spec_formelle_v5_5.json")
STUDIO_EXTRA_LOCKED_FILES = ("amazonia_data_v5_5.js", "livret_v5_5.js")
LOCK_FILE = DATA_DIR / "studio_lock.json"


def _portable_source_label(local_path: Path) -> str:
    resolved = local_path.resolve()
    try:
        return resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        pass
    try:
        rel_sibling = resolved.relative_to(ROOT.resolve().parent)
        return f"../{rel_sibling.as_posix()}"
    except ValueError:
        return resolved.as_posix()


def _read_source_bytes(filename: str) -> tuple[bytes, str]:
    studio_data_dir = resolve_studio_dir(ROOT) / "data"
    local_path = studio_data_dir / filename
    if local_path.exists():
        return local_path.read_bytes(), _portable_source_label(local_path)
    url = f"{STUDIO_RAW_BASE}/{filename}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read(), url


def sync_studio() -> dict[str, object]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    lock_entries: dict[str, dict[str, object]] = {}

    for filename in STUDIO_JSON_FILES:
        raw_bytes, source = _read_source_bytes(filename)
        dest = DATA_DIR / filename
        dest.write_bytes(raw_bytes)
        sha256 = hashlib.sha256(raw_bytes).hexdigest()
        lock_entries[filename] = {
            "sha256": sha256,
            "bytes": len(raw_bytes),
            "source": source,
        }
        print(f"Synced {filename} ({len(raw_bytes)} bytes, sha256={sha256[:12]}...)")

    for filename in STUDIO_EXTRA_LOCKED_FILES:
        raw_bytes, source = _read_source_bytes(filename)
        sha256 = hashlib.sha256(raw_bytes).hexdigest()
        lock_entries[filename] = {
            "sha256": sha256,
            "bytes": len(raw_bytes),
            "source": source,
        }
        print(f"Locked {filename} ({len(raw_bytes)} bytes, sha256={sha256[:12]}...)")

    lock_payload: dict[str, object] = {
        "studio_version": "v5.5",
        "files": lock_entries,
    }
    LOCK_FILE.write_text(
        json.dumps(lock_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote {LOCK_FILE.relative_to(ROOT).as_posix()}")
    return lock_payload


if __name__ == "__main__":
    sync_studio()
