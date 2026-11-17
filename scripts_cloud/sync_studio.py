"""Synchronise les contrats JSON depuis amazonia-doc-studio vers data/ avec verrou SHA-256."""

from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
STUDIO_LOCAL_DATA = Path(r"C:\Dev\Jeu\amazonia-doc-studio\data")
STUDIO_RAW_BASE = "https://raw.githubusercontent.com/antoineacquaviva/amazonia-doc-studio/main/data"
STUDIO_JSON_FILES = ("catalog_v5_3.json", "spec_formelle_v5_3.json")
LOCK_FILE = DATA_DIR / "studio_lock.json"


def _read_source_bytes(filename: str) -> tuple[bytes, str]:
    local_path = STUDIO_LOCAL_DATA / filename
    if local_path.exists():
        return local_path.read_bytes(), str(local_path)
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

    lock_payload: dict[str, object] = {
        "studio_version": "v5.3",
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
