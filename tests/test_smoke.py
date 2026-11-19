"""Tests smoke : garde-fou AST, garde Zéro-API-LLM, portabilité Linux/Windows et PyPy 3.11."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from scripts_cloud.studio_paths import find_uv, resolve_studio_dir
from verify_lot import check_effect_source, check_zero_llm_api_source


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


def test_zero_llm_api_guard_rejects_paid_sdks_and_key() -> None:
    mod_genai = "google." + "genai"
    mod_vertex = "vertex" + "ai"
    key_tok = "GEMINI_" + "API_KEY"

    assert check_zero_llm_api_source(f"import {mod_genai}\n", "bad1.py")
    assert check_zero_llm_api_source("from google import genai\n", "bad2.py")
    assert check_zero_llm_api_source(f"import {mod_vertex}\n", "bad3.py")
    assert check_zero_llm_api_source(f"import os\nk = os.environ.get('{key_tok}')\n", "bad4.py")
    assert check_zero_llm_api_source("import json\nx = 1 + 2\n", "clean.py") == []


def test_portable_studio_dir_resolution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake_repo = tmp_path / "amazonia-sim-lab"
    fake_studio = tmp_path / "amazonia-doc-studio"
    fake_repo.mkdir()
    fake_studio.mkdir()

    monkeypatch.delenv("AMAZONIA_STUDIO_DIR", raising=False)
    assert resolve_studio_dir(fake_repo) == fake_studio.resolve()

    integrated_data = fake_repo / "docs" / "data"
    integrated_data.mkdir(parents=True)
    (integrated_data / "catalog_v5_4.json").write_text("{}", encoding="utf-8")
    assert resolve_studio_dir(fake_repo) == (fake_repo / "docs").resolve()

    custom_studio = tmp_path / "custom-studio"
    custom_studio.mkdir()
    monkeypatch.setenv("AMAZONIA_STUDIO_DIR", str(custom_studio))
    assert resolve_studio_dir(fake_repo) == custom_studio.resolve()


def test_pypy_311_available_via_uv() -> None:
    uv_bin = find_uv()
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
