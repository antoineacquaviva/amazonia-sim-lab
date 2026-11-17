"""Tests smoke du Palier 0 : garde-fou AST et disponibilité PyPy 3.11."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from verify_lot import check_effect_source


def _find_uv() -> str:
    found = shutil.which("uv")
    if found:
        return found
    candidate = Path.home() / ".local" / "bin" / "uv.exe"
    if candidate.exists():
        return str(candidate)
    raise FileNotFoundError("Impossible de trouver l'exécutable 'uv'.")


def test_ast_rejects_buf_access() -> None:
    src = "def f(state):\n    return state._buf[0]\n"
    errors = check_effect_source(src, "dummy.py")
    assert any("_buf" in err for err in errors)


def test_ast_rejects_random_import() -> None:
    src_imp = "import random\n"
    src_from = "from random import randint\n"
    assert check_effect_source(src_imp, "dummy.py")
    assert check_effect_source(src_from, "dummy.py")


def test_ast_rejects_mutable_globals() -> None:
    src_lower = "cache = 0\n"
    src_list = "ITEMS = [1, 2, 3]\n"
    assert check_effect_source(src_lower, "dummy.py")
    assert check_effect_source(src_list, "dummy.py")


def test_ast_accepts_valid_stateless_effect() -> None:
    src = (
        "BONUS_TREES = 2\n"
        "PAIR = (1, 2)\n"
        "@register_tile('G1', 'A')\n"
        "def effect_g1(api, ctx):\n"
        "    return api.add_trees(BONUS_TREES)\n"
    )
    assert check_effect_source(src, "valid.py") == []


def test_pypy_311_available_via_uv() -> None:
    uv_bin = _find_uv()
    env = os.environ.copy()
    proc = subprocess.run(
        [
            uv_bin,
            "run",
            "--no-project",
            "--python",
            "pypy@3.11",
            "python",
            "-c",
            "import sys; assert 'PyPy' in sys.version; print(sys.version)",
        ],
        capture_output=True,
        text=True,
        env=env,
        check=True,
    )
    assert "PyPy" in proc.stdout
