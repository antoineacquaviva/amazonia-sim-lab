"""Orchestrateur local du smoke-test Cloud Build -> Cloud Run Jobs -> GCS -> DuckDB."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
REGION = "europe-west9"
IMAGE_URI = "europe-west9-docker.pkg.dev/amazonia-sim/sim-workers/worker-pypy:latest"
JOB_NAME = "amazonia-smoke"
GCS_SHARD = "gs://amazonia-sim-runs/smoke/shard_00.jsonl.gz"
LOCAL_DIR = ROOT / ".tmp_runs" / "smoke"
LOCAL_SHARD = LOCAL_DIR / "shard_00.jsonl.gz"


def _find_gcloud() -> str:
    for candidate_name in ("gcloud.cmd", "gcloud"):
        found = shutil.which(candidate_name)
        if found:
            return found
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    fallback = (
        Path(local_app_data)
        / "Google"
        / "Cloud SDK"
        / "google-cloud-sdk"
        / "bin"
        / "gcloud.cmd"
    )
    if fallback.exists():
        return str(fallback)
    raise FileNotFoundError("Impossible de trouver 'gcloud'.")


def _run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    gcloud = _find_gcloud()

    _run([gcloud, "builds", "submit", "--config", "cloudbuild.yaml", "."])
    _run(
        [
            gcloud,
            "run",
            "jobs",
            "deploy",
            JOB_NAME,
            "--image",
            IMAGE_URI,
            "--region",
            REGION,
            "--tasks",
            "1",
            "--cpu",
            "1",
            "--memory",
            "512Mi",
            "--max-retries",
            "0",
            "--args=--smoke-test",
        ]
    )
    _run([gcloud, "run", "jobs", "execute", JOB_NAME, "--region", REGION, "--wait"])

    LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    _run([gcloud, "storage", "cp", GCS_SHARD, str(LOCAL_SHARD)])

    rel_shard = LOCAL_SHARD.relative_to(ROOT).as_posix()
    print("\n--- Résultat DuckDB ---")
    relation = duckdb.sql(f"SELECT * FROM read_json_auto('{rel_shard}')")
    if relation is None:
        raise RuntimeError(f"Aucune relation retournée par DuckDB pour {rel_shard}")
    relation.show()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
