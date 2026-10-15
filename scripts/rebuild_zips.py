#!/usr/bin/env python3
"""Rebuild the download zips from the current campus HTML. No Unix uid metadata."""

from __future__ import annotations

import time
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAMPUS_HTML = ROOT / "campus" / "ai-lab-university.html"
CAMPUS_ZIP = ROOT / "downloads" / "ai-lab-university.html.zip"
SLICE_HTML = ROOT / "campus" / "golden-slice.html"
SLICE_ZIP = ROOT / "downloads" / "golden-slice.html.zip"


def write_members(destination: Path, members: list[tuple[str, Path]]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w") as archive:
        for arcname, source in members:
            if not source.is_file():
                raise SystemExit(f"missing campus file: {source}")
            stamp = time.localtime(source.stat().st_mtime)
            info = zipfile.ZipInfo(filename=arcname)
            info.date_time = stamp[:6]
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            info.extra = b""
            archive.writestr(info, source.read_bytes())
    names = ", ".join(arcname for arcname, _path in members[:3])
    extra = "" if len(members) <= 3 else f" +{len(members) - 3} more"
    print(f"{destination.relative_to(ROOT)}  {destination.stat().st_size} bytes  <-  {names}{extra}")


def campus_members() -> list[tuple[str, Path]]:
    campus = ROOT / "campus"
    ordered = [campus / "ai-lab-university.html", campus / "sw.js"]
    ordered += sorted((campus / "assets" / "audio").glob("*.wav"))
    ordered += sorted((campus / "assets" / "curriculum").glob("*.json"))
    ordered += sorted((campus / "assets" / "js").glob("*.js"))
    ordered += sorted((campus / "assets" / "cheats").glob("*"))
    ordered += sorted((campus / "vendor").glob("*.js"))
    return [(str(path.relative_to(campus)).replace("\\", "/"), path) for path in ordered]


def main() -> int:
    members = campus_members()
    wavs = [path for _arc, path in members if path.suffix == ".wav"]
    if len(wavs) < 40:
        raise SystemExit(f"need 40 audio files beside the campus, found {len(wavs)}")
    write_members(CAMPUS_ZIP, members)
    write_members(SLICE_ZIP, [(SLICE_HTML.name, SLICE_HTML)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
