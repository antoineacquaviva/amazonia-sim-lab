"""Pont zéro-friction vers le téléphone Android et le PC pour les bilans de campagnes.

Exécuté automatiquement en fin de `run-campaign` (zéro appel API LLM payant) :
1. Google Drive (`Amazonia_Digests/PROMPT_GEMINI_<nom>.md` & `.txt`) pour accès direct dans
   l'application Gemini Android via `+ -> Google Drive -> Récents`.
2. Mini-page Mobile 1-Tap (`last_digest.html` poussée sur `gs://amazonia-sim-runs/mobile/latest.html`)
   avec bouton "📋 Copier tout le dossier pour l'app Gemini", URL signée 7 jours et QR code ASCII.
3. Presse-papiers PC automatique (Windows `Set-Clipboard` / `clip` UTF-8, Ubuntu `wl-copy` / `xclip`).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT: Path = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from campaigns.digest_builder import (
    DEFAULT_DIGESTS_DIR,
    build_mobile_one_tap_html,
    write_digest_and_prompt_files,
)
from scripts_cloud.studio_paths import find_gcloud

__all__ = (
    "DRIVE_FOLDER_NAME",
    "GCLOUD_DRIVE_AUTH_CMD",
    "GCS_MOBILE_LATEST_URI",
    "build_mobile_one_tap_html",
    "copy_to_clipboard",
    "publish_campaign_digest",
    "publish_mobile_one_tap_page",
    "render_ascii_qr",
    "upload_prompt_to_google_drive",
)

DRIVE_FOLDER_NAME: str = "Amazonia_Digests"
GCS_BUCKET: str = "amazonia-sim-runs"
GCS_MOBILE_OBJECT: str = "mobile/latest.html"
GCS_MOBILE_LATEST_URI: str = f"gs://{GCS_BUCKET}/{GCS_MOBILE_OBJECT}"
GCLOUD_DRIVE_AUTH_CMD: str = (
    "gcloud auth application-default login "
    "--scopes=https://www.googleapis.com/auth/cloud-platform,"
    "https://www.googleapis.com/auth/drive.file"
)


# ---------------------------------------------------------------------------
# Mini-générateur QR Code ASCII autonome (Version 1..6, Niveau L, Mode Byte)
# Permet d'afficher un vrai QR scannable dans le terminal sans dépendance tierce.
# ---------------------------------------------------------------------------

_GF_EXP = [0] * 512
_GF_LOG = [0] * 256


def _init_gf() -> None:
    x = 1
    for i in range(255):
        _GF_EXP[i] = x
        _GF_LOG[x] = i
        x <<= 1
        if x & 0x100:
            x ^= 0x11D
    for i in range(255, 512):
        _GF_EXP[i] = _GF_EXP[i - 255]


_init_gf()


def _gf_mul(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return _GF_EXP[_GF_LOG[a] + _GF_LOG[b]]


def _rs_generator_poly(nsym: int) -> list[int]:
    g = [1]
    for i in range(nsym):
        nxt = [0] * (len(g) + 1)
        factor = _GF_EXP[i]
        for j, coeff in enumerate(g):
            nxt[j] ^= coeff
            nxt[j + 1] ^= _gf_mul(coeff, factor)
        g = nxt
    return g


def _rs_encode(data: list[int], nsym: int) -> list[int]:
    gen = _rs_generator_poly(nsym)
    res = [0] * nsym
    for byte in data:
        factor = byte ^ res[0]
        res = res[1:] + [0]
        for i in range(nsym):
            res[i] ^= _gf_mul(gen[i + 1], factor)
    return res


# (version, size, total_data_codewords, ec_codewords_per_block, num_blocks, align_centers)
_QR_VERSIONS_L: tuple[tuple[int, int, int, int, int, tuple[int, ...]], ...] = (
    (1, 21, 19, 7, 1, ()),
    (2, 25, 34, 10, 1, (6, 18)),
    (3, 29, 55, 15, 1, (6, 22)),
    (4, 33, 80, 20, 1, (6, 26)),
    (5, 37, 108, 26, 1, (6, 30)),
    (6, 41, 136, 18, 2, (6, 34)),
)


def _bch_format_bits(ec_level_bits: int, mask: int) -> int:
    data = (ec_level_bits << 3) | mask
    rem = data << 10
    for i in range(4, -1, -1):
        if rem & (1 << (i + 10)):
            rem ^= 0x537 << i
    return ((data << 10) | rem) ^ 0x5412


def _make_qr_matrix(text: str) -> list[list[bool]] | None:
    payload = text.encode("utf-8")
    selected = None
    for spec in _QR_VERSIONS_L:
        if len(payload) + 2 <= spec[2]:
            selected = spec
            break
    if selected is None:
        return None

    _ver, size, total_data, ec_per_blk, num_blocks, align_centers = selected

    bits: list[int] = [0, 1, 0, 0]  # Mode Byte (0100)
    for i in range(7, -1, -1):
        bits.append((len(payload) >> i) & 1)
    for b in payload:
        for i in range(7, -1, -1):
            bits.append((b >> i) & 1)

    max_bits = total_data * 8
    for _ in range(min(4, max_bits - len(bits))):
        bits.append(0)
    while len(bits) % 8 != 0:
        bits.append(0)

    data_bytes = [
        sum(bits[i + k] << (7 - k) for k in range(8)) for i in range(0, len(bits), 8)
    ]
    pad_seq = (0xEC, 0x11)
    p_idx = 0
    while len(data_bytes) < total_data:
        data_bytes.append(pad_seq[p_idx % 2])
        p_idx += 1

    blk_size = total_data // num_blocks
    data_blocks: list[list[int]] = []
    ec_blocks: list[list[int]] = []
    for b_i in range(num_blocks):
        blk = data_bytes[b_i * blk_size : (b_i + 1) * blk_size]
        data_blocks.append(blk)
        ec_blocks.append(_rs_encode(blk, ec_per_blk))

    codewords: list[int] = []
    for i in range(blk_size):
        for b_i in range(num_blocks):
            codewords.append(data_blocks[b_i][i])
    for i in range(ec_per_blk):
        for b_i in range(num_blocks):
            codewords.append(ec_blocks[b_i][i])

    grid: list[list[bool | None]] = [[None] * size for _ in range(size)]
    reserved: list[list[bool]] = [[False] * size for _ in range(size)]

    def _set_func(r: int, c: int, val: bool) -> None:
        if 0 <= r < size and 0 <= c < size:
            grid[r][c] = val
            reserved[r][c] = True

    def _place_finder(top: int, left: int) -> None:
        for dr in range(-1, 8):
            for dc in range(-1, 8):
                r, c = top + dr, left + dc
                if 0 <= r < size and 0 <= c < size:
                    in_outer = 0 <= dr <= 6 and 0 <= dc <= 6
                    on_border = dr in (0, 6) or dc in (0, 6)
                    in_core = 2 <= dr <= 4 and 2 <= dc <= 4
                    _set_func(r, c, bool(in_outer and (on_border or in_core)))

    _place_finder(0, 0)
    _place_finder(0, size - 7)
    _place_finder(size - 7, 0)

    for i in range(8, size - 8):
        _set_func(6, i, i % 2 == 0)
        _set_func(i, 6, i % 2 == 0)

    for ar in align_centers:
        for ac in align_centers:
            if reserved[ar][ac]:
                continue
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    _set_func(ar + dr, ac + dc, max(abs(dr), abs(dc)) != 1)

    _set_func(size - 8, 8, True)
    for i in range(9):
        if i != 6:
            reserved[8][i] = True
            reserved[i][8] = True
    for i in range(8):
        reserved[8][size - 1 - i] = True
        reserved[size - 1 - i][8] = True

    stream_bits: list[int] = []
    for cw in codewords:
        for i in range(7, -1, -1):
            stream_bits.append((cw >> i) & 1)

    bit_idx = 0
    upward = True
    col = size - 1
    while col > 0:
        if col == 6:
            col -= 1
        row_iter = range(size - 1, -1, -1) if upward else range(size)
        for r in row_iter:
            for dc in (0, -1):
                c = col + dc
                if not reserved[r][c]:
                    val = bool(stream_bits[bit_idx]) if bit_idx < len(stream_bits) else False
                    bit_idx += 1
                    if (r + c) % 2 == 0:
                        val = not val
                    grid[r][c] = val
        upward = not upward
        col -= 2

    fmt = _bch_format_bits(0b01, 0)  # Level L (01), Mask 0 (000)
    fmt_Coords_A = [
        (8, 0),
        (8, 1),
        (8, 2),
        (8, 3),
        (8, 4),
        (8, 5),
        (8, 7),
        (8, 8),
        (7, 8),
        (5, 8),
        (4, 8),
        (3, 8),
        (2, 8),
        (1, 8),
        (0, 8),
    ]
    fmt_Coords_B = [
        (size - 1, 8),
        (size - 2, 8),
        (size - 3, 8),
        (size - 4, 8),
        (size - 5, 8),
        (size - 6, 8),
        (size - 7, 8),
        (8, size - 8),
        (8, size - 7),
        (8, size - 6),
        (8, size - 5),
        (8, size - 4),
        (8, size - 3),
        (8, size - 2),
        (8, size - 1),
    ]
    for bit_pos in range(15):
        b_val = bool((fmt >> bit_pos) & 1)
        r_a, c_a = fmt_Coords_A[bit_pos]
        r_b, c_b = fmt_Coords_B[bit_pos]
        grid[r_a][c_a] = b_val
        grid[r_b][c_b] = b_val

    return [[bool(cell) for cell in row] for row in grid]


def render_ascii_qr(url: str) -> str:
    """Rend un QR code compact en demi-blocs Unicode (`▀`, `▄`, `█`, ` `) pour terminal."""
    target = url.strip()
    matrix = _make_qr_matrix(target)
    if matrix is None:
        # Si l'URL signée dépasse la capacité d'un petit QR, on encode l'URL courte GCS console/storage
        short_url = f"https://storage.cloud.google.com/{GCS_BUCKET}/{GCS_MOBILE_OBJECT}"
        matrix = _make_qr_matrix(short_url)
    if matrix is None:
        return f"[QR URL] {target}"

    quiet = 2
    n = len(matrix)
    padded_size = n + 2 * quiet
    padded = [[False] * padded_size for _ in range(padded_size)]
    for r in range(n):
        for c in range(n):
            padded[r + quiet][c + quiet] = matrix[r][c]

    lines: list[str] = []
    for r in range(0, padded_size, 2):
        row_chars: list[str] = []
        for c in range(padded_size):
            top = padded[r][c]
            bot = padded[r + 1][c] if (r + 1) < padded_size else False
            if top and bot:
                row_chars.append("█")
            elif top and not bot:
                row_chars.append("▀")
            elif not top and bot:
                row_chars.append("▄")
            else:
                row_chars.append(" ")
        lines.append("  " + "".join(row_chars))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 1. Google Drive (dossier local synchronisé OU API REST Drive v3 via ADC/gcloud)
# ---------------------------------------------------------------------------


def _detect_local_synced_drive_root() -> Path | None:
    """Détecte un dossier Google Drive synchronisé localement sur Windows 11 ou Ubuntu."""
    env_dir = os.environ.get("AMAZONIA_GDRIVE_LOCAL_DIR", "").strip()
    if env_dir:
        cand = Path(env_dir).expanduser()
        if cand.exists():
            return cand

    home = Path.home()
    candidates = [
        home / "Google Drive" / "My Drive",
        home / "Google Drive" / "Mon Drive",
        home / "Google Drive",
        home / "My Drive",
        home / "Mon Drive",
        Path("G:/My Drive"),
        Path("G:/Mon Drive"),
    ]
    for cand in candidates:
        try:
            if cand.exists() and cand.is_dir():
                return cand
        except OSError:
            continue
    return None


def _get_adc_access_token_with_drive_check() -> tuple[str | None, bool, str]:
    """Récupère un token OAuth2 local via `gcloud auth` et vérifie la présence du scope `drive`."""
    try:
        gcloud = find_gcloud()
    except FileNotFoundError:
        return (
            None,
            False,
            f"Exécutable gcloud non trouvé ou scope `drive.file` non activé. Commande :\n  {GCLOUD_DRIVE_AUTH_CMD}",
        )

    for subcmd in (
        [gcloud, "auth", "application-default", "print-access-token"],
        [gcloud, "auth", "print-access-token"],
    ):
        try:
            proc = subprocess.run(
                subcmd,
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except OSError:
            continue
        token = proc.stdout.strip()
        if proc.returncode != 0 or not token:
            continue

        info_url = (
            "https://oauth2.googleapis.com/tokeninfo?access_token="
            + urllib.parse.quote(token, safe="")
        )
        try:
            with urllib.request.urlopen(info_url, timeout=8) as resp:
                info = json.loads(resp.read().decode("utf-8"))
            scopes = str(info.get("scope", ""))
            if "drive" in scopes:
                return token, True, "OK"
        except (urllib.error.URLError, TimeoutError, ValueError):
            continue

    return (
        None,
        False,
        f"Scope Google Drive `drive.file` non activé. Exécutez une seule fois :\n  {GCLOUD_DRIVE_AUTH_CMD}",
    )


def _drive_rest_find_or_create_folder(token: str, folder_name: str) -> str:
    query = (
        f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' "
        "and trashed = false"
    )
    list_url = (
        "https://www.googleapis.com/drive/v3/files?"
        + urllib.parse.urlencode({"q": query, "fields": "files(id,name)", "pageSize": "5"})
    )
    req = urllib.request.Request(
        list_url,
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    files = payload.get("files", [])
    if files:
        return str(files[0]["id"])

    meta_bytes = json.dumps(
        {"name": folder_name, "mimeType": "application/vnd.google-apps.folder"}
    ).encode("utf-8")
    create_req = urllib.request.Request(
        "https://www.googleapis.com/drive/v3/files?fields=id",
        data=meta_bytes,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        method="POST",
    )
    with urllib.request.urlopen(create_req, timeout=15) as resp:
        created = json.loads(resp.read().decode("utf-8"))
    return str(created["id"])


def _drive_rest_upsert_file(
    token: str,
    *,
    folder_id: str,
    filename: str,
    content_bytes: bytes,
    mime_type: str,
) -> dict[str, Any]:
    q = f"name = '{filename}' and '{folder_id}' in parents and trashed = false"
    search_url = "https://www.googleapis.com/drive/v3/files?" + urllib.parse.urlencode(
        {"q": q, "fields": "files(id,name)", "pageSize": "5"}
    )
    req = urllib.request.Request(
        search_url,
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        found = json.loads(resp.read().decode("utf-8")).get("files", [])

    if found:
        file_id = str(found[0]["id"])
        up_url = (
            f"https://www.googleapis.com/upload/drive/v3/files/{file_id}"
            "?uploadType=media&fields=id,name,webViewLink"
        )
        up_req = urllib.request.Request(
            up_url,
            data=content_bytes,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": f"{mime_type}; charset=UTF-8",
            },
            method="PATCH",
        )
        with urllib.request.urlopen(up_req, timeout=30) as resp:
            return dict(json.loads(resp.read().decode("utf-8")))

    boundary = "===amazonia_sim_lab_drive_boundary==="
    meta_json = json.dumps({"name": filename, "parents": [folder_id]}).encode("utf-8")
    body = (
        f"--{boundary}\r\n"
        "Content-Type: application/json; charset=UTF-8\r\n\r\n"
    ).encode() + meta_json + (
        f"\r\n--{boundary}\r\n"
        f"Content-Type: {mime_type}; charset=UTF-8\r\n\r\n"
    ).encode() + content_bytes + f"\r\n--{boundary}--\r\n".encode()

    create_url = (
        "https://www.googleapis.com/upload/drive/v3/files"
        "?uploadType=multipart&fields=id,name,webViewLink"
    )
    c_req = urllib.request.Request(
        create_url,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/related; boundary={boundary}",
        },
        method="POST",
    )
    with urllib.request.urlopen(c_req, timeout=30) as resp:
        return dict(json.loads(resp.read().decode("utf-8")))


def upload_prompt_to_google_drive(prompt_path: Path) -> dict[str, Any]:
    """Téléverse `PROMPT_GEMINI_<nom>.md` (et `.txt`) dans `Amazonia_Digests` sur Google Drive."""
    content_text = prompt_path.read_text(encoding="utf-8")
    content_bytes = content_text.encode("utf-8")
    md_name = prompt_path.name
    txt_name = prompt_path.with_suffix(".txt").name

    # 1. Priorité au dossier Google Drive synchronisé localement s'il est présent
    local_drive = _detect_local_synced_drive_root()
    if local_drive is not None:
        target_dir = local_drive / DRIVE_FOLDER_NAME
        target_dir.mkdir(parents=True, exist_ok=True)
        md_dest = target_dir / md_name
        txt_dest = target_dir / txt_name
        md_dest.write_text(content_text, encoding="utf-8", newline="\n")
        txt_dest.write_text(content_text, encoding="utf-8", newline="\n")
        return {
            "status": "OK_LOCAL_SYNC",
            "folder": target_dir.as_posix(),
            "files": [md_dest.name, txt_dest.name],
        }

    # 2. API REST Google Drive v3 via identifiants gcloud / ADC (scope drive.file)
    token, has_scope, msg = _get_adc_access_token_with_drive_check()
    if token is not None and has_scope:
        try:
            folder_id = _drive_rest_find_or_create_folder(token, DRIVE_FOLDER_NAME)
            res_md = _drive_rest_upsert_file(
                token,
                folder_id=folder_id,
                filename=md_name,
                content_bytes=content_bytes,
                mime_type="text/markdown",
            )
            res_txt = _drive_rest_upsert_file(
                token,
                folder_id=folder_id,
                filename=txt_name,
                content_bytes=content_bytes,
                mime_type="text/plain",
            )
            return {
                "status": "OK_DRIVE_API",
                "folder": DRIVE_FOLDER_NAME,
                "folder_id": folder_id,
                "files": [res_md.get("name", md_name), res_txt.get("name", txt_name)],
                "webViewLink": res_md.get("webViewLink", ""),
            }
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as exc:
            msg = f"Échec appel REST Google Drive v3 ({exc})."

    return {
        "status": "SKIPPED_NO_DRIVE_SCOPE",
        "message": msg,
        "auth_command": GCLOUD_DRIVE_AUTH_CMD,
    }


# ---------------------------------------------------------------------------
# 2. Mini-page Mobile 1-Tap (last_digest.html -> gs://amazonia-sim-runs/mobile/latest.html)
# ---------------------------------------------------------------------------


def publish_mobile_one_tap_page(
    campaign_slug: str,
    prompt_markdown: str,
    digest: dict[str, Any],
    *,
    digests_dir: Path | None = None,
    push_gcs: bool = True,
) -> dict[str, Any]:
    """Écrit `last_digest.html` localement et le pousse sur `gs://amazonia-sim-runs/mobile/latest.html`."""
    out_dir = digests_dir if digests_dir is not None else DEFAULT_DIGESTS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    html_content = build_mobile_one_tap_html(campaign_slug, prompt_markdown, digest)
    local_html = out_dir / "last_digest.html"
    local_html.write_text(html_content, encoding="utf-8", newline="\n")

    sign_cmd_hint = f"gcloud storage sign-url {GCS_MOBILE_LATEST_URI} --duration=7d"
    fallback_url = f"https://storage.cloud.google.com/{GCS_BUCKET}/{GCS_MOBILE_OBJECT}"
    signed_url: str | None = None
    uploaded = False

    if push_gcs:
        try:
            gcloud = find_gcloud()
            cp_proc = subprocess.run(
                [
                    gcloud,
                    "storage",
                    "cp",
                    local_html.as_posix(),
                    GCS_MOBILE_LATEST_URI,
                    "--content-type=text/html; charset=utf-8",
                    "--cache-control=no-cache,max-age=0",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            uploaded = cp_proc.returncode == 0

            if uploaded:
                sign_proc = subprocess.run(
                    [gcloud, "storage", "sign-url", GCS_MOBILE_LATEST_URI, "--duration=7d"],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    timeout=15,
                    check=False,
                )
                if sign_proc.returncode == 0:
                    for line in sign_proc.stdout.splitlines():
                        stripped = line.strip()
                        if stripped.startswith("https://"):
                            signed_url = stripped
                            break
                        if "signed_url:" in stripped:
                            candidate = stripped.split("signed_url:", 1)[1].strip()
                            if candidate.startswith("https://"):
                                signed_url = candidate
                                break
        except FileNotFoundError:
            uploaded = False

    display_url = signed_url or fallback_url
    qr_ascii = render_ascii_qr(fallback_url)

    return {
        "local_html": local_html.relative_to(ROOT).as_posix()
        if local_html.is_relative_to(ROOT)
        else local_html.as_posix(),
        "gcs_uri": GCS_MOBILE_LATEST_URI,
        "uploaded_to_gcs": uploaded,
        "mobile_url": display_url,
        "sign_url_command": sign_cmd_hint,
        "qr_ascii": qr_ascii,
    }


# ---------------------------------------------------------------------------
# 3. Presse-papiers PC automatique (Windows 11 & Ubuntu Linux)
# ---------------------------------------------------------------------------


def copy_to_clipboard(text: str) -> dict[str, Any]:
    """Copie le dossier en UTF-8 dans le presse-papiers local (Windows 11 / Ubuntu, silencieux sinon)."""
    payload = text.encode("utf-8")

    if os.name == "nt":
        for cmd in (
            [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                ("[Console]::InputEncoding = [System.Text.Encoding]::UTF8; "
                "$inputText = [Console]::In.ReadToEnd(); "
                "Set-Clipboard -Value $inputText"),
            ],
            ["clip.exe"],
        ):
            try:
                proc = subprocess.run(
                    cmd,
                    input=payload,
                    capture_output=True,
                    timeout=8,
                    check=False,
                )
                if proc.returncode == 0:
                    return {"copied": True, "backend": cmd[0]}
            except OSError:
                continue
        return {"copied": False, "backend": "none"}

    # Ubuntu / Linux (Wayland wl-copy ou X11 xclip / xsel)
    posix_candidates: list[list[str]] = []
    if shutil.which("wl-copy"):
        posix_candidates.append(["wl-copy"])
    if shutil.which("xclip"):
        posix_candidates.append(["xclip", "-selection", "clipboard"])
    if shutil.which("xsel"):
        posix_candidates.append(["xsel", "--clipboard", "--input"])

    for cmd in posix_candidates:
        try:
            proc = subprocess.run(
                cmd,
                input=payload,
                capture_output=True,
                timeout=5,
                check=False,
            )
            if proc.returncode == 0:
                return {"copied": True, "backend": cmd[0]}
        except (OSError, subprocess.TimeoutExpired):
            continue

    return {"copied": False, "backend": "none"}


# ---------------------------------------------------------------------------
# Orchestration complète : build + 3 livraisons simultanées
# ---------------------------------------------------------------------------


def publish_campaign_digest(
    campaign_slug: str,
    stats_payload: dict[str, Any] | None = None,
    *,
    chassis_ids: list[int] | tuple[int, ...] | None = None,
    tested_tiles: list[str] | tuple[tuple[str, str], ...] | None = None,
    digests_dir: Path | None = None,
    push_gcs: bool = True,
    upload_drive: bool = True,
    copy_clip: bool = True,
) -> dict[str, Any]:
    """Génère `digest_<nom>.json` + `PROMPT_GEMINI_<nom>.md` et exécute les 3 livraisons."""
    out_dir = digests_dir if digests_dir is not None else DEFAULT_DIGESTS_DIR
    slug = campaign_slug.strip()
    slug = slug.removeprefix("digest_")
    slug = slug.removesuffix(".json")

    if stats_payload is None:
        existing_path = out_dir / f"digest_{slug}.json"
        if not existing_path.exists():
            legacy_path = ROOT / "data" / f"digest_{slug}.json"
            existing_path = legacy_path
        stats_payload = dict(json.loads(existing_path.read_text(encoding="utf-8")))

    digest_path, prompt_path, digest = write_digest_and_prompt_files(
        slug,
        stats_payload,
        chassis_ids=chassis_ids,
        tested_tiles=tested_tiles,
        digests_dir=out_dir,
    )
    prompt_md = prompt_path.read_text(encoding="utf-8")

    drive_info = (
        upload_prompt_to_google_drive(prompt_path)
        if upload_drive
        else {"status": "DISABLED"}
    )
    mobile_info = publish_mobile_one_tap_page(
        slug,
        prompt_md,
        digest,
        digests_dir=out_dir,
        push_gcs=push_gcs,
    )
    clip_info = copy_to_clipboard(prompt_md) if copy_clip else {"copied": False, "backend": "disabled"}

    digest_bytes = len(digest_path.read_bytes())
    print("\n=== PONT GEMINI MOBILE & PC (ZÉRO-API-LLM) ===")
    print(f"• Digest auto-portant : {digest_path.name} ({digest_bytes} octets < 35 Ko)")
    print(f"• Dossier Gemini prêt : {prompt_path.name}")
    if drive_info.get("status") in ("OK_LOCAL_SYNC", "OK_DRIVE_API"):
        print(
            f"• [1/3] Google Drive  : Téléversé dans '{DRIVE_FOLDER_NAME}' "
            f"({', '.join(drive_info.get('files', []))})"
        )
    elif drive_info.get("status") == "SKIPPED_NO_DRIVE_SCOPE":
        print(
            f"• [1/3] Google Drive  : {drive_info.get('message')}\n"
            f"        (Secours mobile 1-Tap actif ci-dessous)"
        )
    print(f"• [2/3] Page Mobile   : {mobile_info['local_html']} -> {mobile_info['gcs_uri']}")
    print(f"        Lien mobile   : {mobile_info['mobile_url']}")
    print(f"        URL signée 7j : {mobile_info['sign_url_command']}")
    print(mobile_info["qr_ascii"])
    if clip_info.get("copied"):
        print(
            f"• [3/3] Presse-papiers: Copié automatiquement ({clip_info.get('backend')}) -> Ctrl+V dans Gemini !"
        )
    else:
        print("• [3/3] Presse-papiers: Aucun utilitaire clipboard détecté (fichier .md prêt).")

    return {
        "digest_path": digest_path,
        "prompt_path": prompt_path,
        "digest_bytes": digest_bytes,
        "drive": drive_info,
        "mobile": mobile_info,
        "clipboard": clip_info,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Génère et publie un bilan de campagne auto-portant vers Gemini Mobile & PC."
    )
    parser.add_argument(
        "--campaign",
        default="palier1_b0",
        help="Nom court du digest (ex: palier1_b0 ou palier2_coeur_muet).",
    )
    parser.add_argument(
        "--no-gcs",
        action="store_true",
        help="Ne pas pousser latest.html sur GCS (mode test hors-ligne).",
    )
    parser.add_argument(
        "--no-drive",
        action="store_true",
        help="Ne pas tenter l'upload Google Drive.",
    )
    args = parser.parse_args(argv)

    publish_campaign_digest(
        args.campaign,
        push_gcs=not args.no_gcs,
        upload_drive=not args.no_drive,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
