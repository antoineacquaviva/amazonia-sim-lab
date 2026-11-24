"""Délègue la génération de data/spec_bundle_v6_0.json au compilateur SSOT unique scripts/build_studio_artifacts.py."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_studio_artifacts import (
    RES_VOCAB,
    TRIG_VOCAB,
    build_all_artifacts,
)

__all__ = (
    "RES_VOCAB",
    "TRIG_VOCAB",
    "build_bundle",
)


def build_bundle() -> None:
    """Compile tous les artefacts dérivés Studio + simulateur depuis contracts/ (SSOT v6.2)."""
    summary = build_all_artifacts()
    print(
        f"Wrote data/spec_bundle_v6_0.json via SSOT v{summary['schema_version']} "
        f"({summary['slots']} slots, {summary['profiles']} profils)"
    )


if __name__ == "__main__":
    build_bundle()
