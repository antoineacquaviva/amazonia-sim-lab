"""Résolution portable des chemins et exécutables entre Windows 11 et Ubuntu Linux."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

__all__ = (
    "find_gcloud",
    "find_uv",
    "resolve_studio_dir",
)


def resolve_studio_dir(repo_root: Path) -> Path:
    """Localise Amazonia Doc Studio de façon portable Windows / Ubuntu.

    Ordre de priorité :
    1. Variable d'environnement `AMAZONIA_STUDIO_DIR` (si définie) ;
    2. `docs/` intégré directement dans ce dépôt (si `docs/data/catalog_v6_0.json` existe) ;
    3. `../amazonia-doc-studio` à côté de ce dépôt ;
    4. `~/dev/amazonia-doc-studio` (convention Ubuntu) ;
    5. `~/Dev/Jeu/amazonia-doc-studio` (convention Windows).
    """
    env_override = os.environ.get("AMAZONIA_STUDIO_DIR", "").strip()
    if env_override:
        return Path(env_override).expanduser().resolve()

    integrated_docs = repo_root.resolve() / "docs"
    if (integrated_docs / "data" / "catalog_v6_0.json").exists():
        return integrated_docs

    home = Path.home()
    candidates = (
        repo_root.resolve().parent / "amazonia-doc-studio",
        home / "dev" / "amazonia-doc-studio",
        home / "Dev" / "Jeu" / "amazonia-doc-studio",
    )
    for cand in candidates:
        if cand.exists():
            return cand
    return integrated_docs


def find_uv() -> str:
    """Localise l'exécutable `uv` sans dépendre d'une extension Windows `.exe`."""
    found = shutil.which("uv")
    if found:
        return found

    bin_names = ("uv.exe", "uv") if os.name == "nt" else ("uv",)
    home = Path.home()
    for folder in (home / ".local" / "bin", home / ".cargo" / "bin"):
        for bname in bin_names:
            cand = folder / bname
            if cand.exists():
                return str(cand)
    raise FileNotFoundError("Impossible de trouver l'exécutable 'uv' dans le PATH ou ~/.local/bin.")


def find_gcloud() -> str:
    """Localise l'exécutable `gcloud` sous Ubuntu Linux comme sous Windows 11."""
    names = ("gcloud.cmd", "gcloud") if os.name == "nt" else ("gcloud",)
    for cname in names:
        found = shutil.which(cname)
        if found:
            return found

    home = Path.home()
    if os.name == "nt":
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        if local_app_data:
            win_sdk = (
                Path(local_app_data)
                / "Google"
                / "Cloud SDK"
                / "google-cloud-sdk"
                / "bin"
                / "gcloud.cmd"
            )
            if win_sdk.exists():
                return str(win_sdk)
    else:
        for posix_cand in (
            Path("/usr/bin/gcloud"),
            Path("/snap/bin/gcloud"),
            home / "google-cloud-sdk" / "bin" / "gcloud",
        ):
            if posix_cand.exists():
                return str(posix_cand)

    raise FileNotFoundError("Impossible de trouver l'exécutable 'gcloud'.")
