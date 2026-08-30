"""Download the public U.S. Social Security Administration baby-names dataset.

Source (official):  https://www.ssa.gov/oact/babynames/names.zip
Landing page:       https://www.ssa.gov/oact/babynames/limits.html

The archive contains one plain-text file per year, ``yob1880.txt`` through the most
recent year available. Each line is ``Name,Sex,Count`` with no header row.

The data is public domain and published by SSA. This script only downloads and
extracts it; the raw files are deliberately NOT committed to this repository
(see ``data/README.md`` and ``.gitignore``).

Usage
-----
    python scripts/download_ssa_data.py                          # download from SSA
    python scripts/download_ssa_data.py --archive path/names.zip # use a local copy

Some networks and hosting providers are blocked by ssa.gov's CDN and receive
``HTTP 403``. In that case download ``names.zip`` manually from the landing page
and pass it with ``--archive``; validation, extraction, and provenance recording
are identical either way, and the provenance file records which route was used.

Options
-------
    --dest DIR      where to extract (default: data/raw)
    --archive PATH  use an already-downloaded names.zip instead of fetching
    --keep-zip      keep a copy of the archive alongside the extracted files
    --force         re-extract even if the data is already present

Running it twice is safe: it skips work that is already done unless ``--force``.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

SSA_URL = "https://www.ssa.gov/oact/babynames/names.zip"
SSA_PAGE = "https://www.ssa.gov/oact/babynames/limits.html"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DEST = REPO_ROOT / "data" / "raw"
PROVENANCE = "PROVENANCE.json"


def download(url: str) -> bytes:
    """Fetch the archive, reporting a clear error rather than a stack trace."""
    print(f"Downloading {url}")
    request = urllib.request.Request(url, headers={"User-Agent": "ssa-babynames-downloader/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = response.read()
    except urllib.error.HTTPError as exc:
        raise SystemExit(
            f"\nSSA returned HTTP {exc.code}.\n"
            f"Some networks and hosting providers are blocked by ssa.gov's edge.\n"
            f"Download it manually from {SSA_PAGE} and unzip into {DEFAULT_DEST}\\ instead."
        ) from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"\nCould not reach ssa.gov: {exc.reason}") from exc

    print(f"  received {len(payload):,} bytes")
    return payload


def extract(payload: bytes, dest: Path) -> list[str]:
    """Extract only the yearly data files, ignoring anything unexpected."""
    if not payload.startswith(b"PK"):
        raise SystemExit("Downloaded file is not a ZIP archive - aborting.")

    dest.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        for name in sorted(archive.namelist()):
            # Only take flat yobXXXX.txt entries; never trust paths from an archive.
            if "/" in name or "\\" in name or not name.lower().endswith(".txt"):
                continue
            (dest / Path(name).name).write_bytes(archive.read(name))
            written.append(Path(name).name)
    if not written:
        raise SystemExit("Archive contained no yearly .txt files - aborting.")
    return written


def write_provenance(dest: Path, payload: bytes, files: list[str], acquisition: str) -> None:
    """Record where the data came from, so the analysis is auditable later."""
    years = sorted(f[3:7] for f in files if f.lower().startswith("yob"))
    record = {
        "source_url": SSA_URL,
        "source_page": SSA_PAGE,
        "acquisition_method": acquisition,
        "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "archive_sha256": hashlib.sha256(payload).hexdigest(),
        "archive_bytes": len(payload),
        "file_count": len(files),
        "year_range": [years[0], years[-1]] if years else None,
        "license": "Public domain (U.S. Social Security Administration)",
    }
    (dest / PROVENANCE).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"  provenance written to {dest / PROVENANCE}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    parser.add_argument("--archive", type=Path, default=None,
                        help="use an already-downloaded names.zip instead of fetching")
    parser.add_argument("--keep-zip", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    dest: Path = args.dest
    existing = sorted(dest.glob("yob*.txt")) if dest.exists() else []
    if existing and not args.force:
        print(f"Already present: {len(existing)} yearly files in {dest}")
        print("Nothing to do. Re-run with --force to redo the extraction.")
        return 0

    if args.archive:
        if not args.archive.is_file():
            raise SystemExit(f"Archive not found: {args.archive}")
        print(f"Using local archive {args.archive}")
        payload = args.archive.read_bytes()
        print(f"  read {len(payload):,} bytes")
        acquisition = (
            "Manual browser download from the official SSA landing page, then supplied "
            "locally via --archive (automated access to ssa.gov returned HTTP 403)."
        )
    else:
        payload = download(SSA_URL)
        acquisition = "Automated download from the official SSA URL by this script."

    files = extract(payload, dest)
    write_provenance(dest, payload, files, acquisition)

    if args.keep_zip:
        archive_path = dest / "names.zip"
        archive_path.write_bytes(payload)
        print(f"  archive kept at {archive_path}")

    years = sorted(f[3:7] for f in files if f.lower().startswith("yob"))
    print(f"\nExtracted {len(files)} files to {dest}")
    if years:
        print(f"Years covered: {years[0]}-{years[-1]}")
    print("\nNext: open notebooks/public-ssa-analysis.ipynb and run all cells.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
