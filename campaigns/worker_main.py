"""Worker Cloud PyPy 3.11 stdlib pure pour amazonia-sim-lab."""

from __future__ import annotations

import argparse
import gzip
import json
import platform
import sys
import time
import urllib.parse
import urllib.request

METADATA_TOKEN_URL = (
    "http://metadata.google.internal/computeMetadata/v1/"
    "instance/service-accounts/default/token"
)
BUCKET_NAME = "amazonia-sim-runs"
SMOKE_OBJECT_NAME = "smoke/shard_00.jsonl.gz"


def _fetch_gcp_access_token() -> str:
    req = urllib.request.Request(
        METADATA_TOKEN_URL,
        headers={"Metadata-Flavor": "Google"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return str(payload["access_token"])


def _upload_gcs_bytes(bucket: str, object_name: str, data: bytes, token: str) -> dict:
    encoded_name = urllib.parse.quote(object_name, safe="")
    url = (
        f"https://storage.googleapis.com/upload/storage/v1/b/{bucket}/o"
        f"?uploadType=media&name={encoded_name}"
    )
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/gzip",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _run_jit_microloop(iterations: int = 1_000_000) -> tuple[float, int]:
    buf = bytearray(256)
    t0 = time.perf_counter()
    acc = 0
    for i in range(iterations):
        idx = i & 255
        val = (buf[idx] + i) & 255
        buf[idx] = val
        acc = (acc + val) & 0xFFFFFFFF
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return elapsed_ms, acc


def run_smoke_test() -> int:
    elapsed_ms, checksum = _run_jit_microloop(1_000_000)
    record = {
        "status": "SMOKE_OK",
        "python_implementation": platform.python_implementation(),
        "pypy_version": sys.version.replace("\n", " "),
        "iterations": 1_000_000,
        "cpu_ms": round(elapsed_ms, 3),
        "checksum": checksum,
    }
    raw_jsonl = (json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8")
    compressed = gzip.compress(raw_jsonl)

    token = _fetch_gcp_access_token()
    gcs_resp = _upload_gcs_bytes(BUCKET_NAME, SMOKE_OBJECT_NAME, compressed, token)
    print(
        json.dumps(
            {
                "uploaded_to": f"gs://{BUCKET_NAME}/{SMOKE_OBJECT_NAME}",
                "size": gcs_resp.get("size"),
                "record": record,
            },
            ensure_ascii=False,
        )
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Amazonia Sim Lab PyPy Worker")
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Exécute le smoke-test JIT PyPy -> GCS.",
    )
    args = parser.parse_args(argv)
    if args.smoke_test:
        return run_smoke_test()
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
