#!/usr/bin/env python3
"""Rebuild the download zips from the current campus HTML. No Unix uid metadata."""

from __future__ import annotations

import time
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = (
    (ROOT / "campus" / "ai-lab-university.html", ROOT / "downloads" / "ai-lab-university.html.zip"),
    (ROOT / "campus" / "golden-slice.html", ROOT / "downloads" / "golden-slice.html.zip"),
)


def write_zip(source: Path, destination: Path) -> None:
    if not source.is_file():
        raise SystemExit(f"missing campus file: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    stamp = time.localtime(source.stat().st_mtime)
    info = zipfile.ZipInfo(filename=source.name)
    info.date_time = stamp[:6]
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    info.extra = b""
    with zipfile.ZipFile(destination, "w") as archive:
        archive.writestr(info, source.read_bytes())
    print(f"{destination.relative_to(ROOT)}  {destination.stat().st_size} bytes  <-  {source.name}")


def main() -> int:
    for source, destination in PAIRS:
        write_zip(source, destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
