#!/usr/bin/env python3
"""Check the campus count, offline rule, privacy sweep, labs, and zip freshness."""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from campus.citation_hosts import url_allowed
CAMPUS = ROOT / "campus" / "ai-lab-university.html"
SLICE = ROOT / "campus" / "golden-slice.html"
README = ROOT / "README.md"
EXPECTED_LESSONS = 581

BANNED = ("link" + "tr.ee", "cypher" + "monkey")
LABS = (
    "labs/01-local-hello.py",
    "labs/02-tool-call.py",
    "labs/03-golden-eval.py",
    "labs/06-rag-ablation.py",
    "labs/07-agent-loop.py",
    "labs/08-voice-latency-budget.py",
)
ZIP_PAIRS = (
    (CAMPUS, ROOT / "downloads" / "ai-lab-university.html.zip"),
    (SLICE, ROOT / "downloads" / "golden-slice.html.zip"),
)


def fail(message: str) -> None:
    print(f"FAIL  {message}")
    raise SystemExit(1)


def check_privacy(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="replace").lower()
    for banned in BANNED:
        if banned in text:
            fail(f"{path.relative_to(ROOT)} contains {banned}")


def check_offline(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if re.search(r"<script[^>]+src\s*=", text, flags=re.I):
        fail(f"{path.name} loads an external script")
    if re.search(r"<link[^>]+stylesheet[^>]+href\s*=\s*['\"]https?:", text, flags=re.I):
        fail(f"{path.name} loads an external stylesheet")
    for url in re.findall(r"https?://[^\"'\s>]+", text):
        if not url_allowed(url):
            fail(f"{path.name} has unexpected URL {url}")


def check_campus() -> None:
    text = CAMPUS.read_text(encoding="utf-8")
    ids = re.findall(r'<article class="lesson" id="([^"]+)"', text)
    if len(ids) != EXPECTED_LESSONS or len(set(ids)) != EXPECTED_LESSONS:
        fail(f"lesson count is {len(ids)} unique {len(set(ids))}, expected {EXPECTED_LESSONS}")
    if 'id="home"' not in text or 'id="map"' not in text:
        fail("home or track map is missing")
    if 'data-theme="dark"' not in text or 'data-theme="light"' not in text:
        fail("light and dark themes are missing")
    print(f"OK    campus lessons={len(ids)}")


def _member_matches(archive: zipfile.ZipFile, arcname: str, source: Path) -> None:
    info = archive.getinfo(arcname)
    if info.extra:
        fail(f"{arcname} still has zip extra metadata")
    packed_hash = hashlib.sha256(archive.read(arcname)).hexdigest()
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    if packed_hash != source_hash:
        fail(f"{arcname} is stale relative to {source}")


def check_zips() -> None:
    campus_zip = ZIP_PAIRS[0][1]
    if not campus_zip.is_file():
        fail(f"missing zip {campus_zip.name}")
    wavs = sorted((ROOT / "campus" / "assets" / "audio").glob("*.wav"))
    if len(wavs) < 40:
        fail(f"need 40 audio files, found {len(wavs)}")
    expected = [CAMPUS.name] + [f"assets/audio/{path.name}" for path in wavs]
    with zipfile.ZipFile(campus_zip) as archive:
        names = archive.namelist()
        if names != expected:
            fail(f"{campus_zip.name} contains {len(names)} entries, expected the HTML plus {len(wavs)} clips")
        _member_matches(archive, CAMPUS.name, CAMPUS)
        for path in wavs:
            _member_matches(archive, f"assets/audio/{path.name}", path)
    print(f"OK    zip {campus_zip.name} html+{len(wavs)} clips")

    source, archive_path = ZIP_PAIRS[1]
    if not archive_path.is_file():
        fail(f"missing zip {archive_path.name}")
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        if names != [source.name]:
            fail(f"{archive_path.name} contains {names}, expected [{source.name}]")
        _member_matches(archive, source.name, source)
    print(f"OK    zip {archive_path.name}")


def check_readme_links() -> None:
    text = README.read_text(encoding="utf-8")
    if f"{EXPECTED_LESSONS} lessons" not in text:
        fail(f"README does not state {EXPECTED_LESSONS} lessons")
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        path = (ROOT / target.split("#", 1)[0].removeprefix("./")).resolve()
        if not path.exists():
            fail(f"README link missing on disk: {target}")
    print("OK    README relative links")


def check_labs() -> None:
    for relative in LABS:
        completed = subprocess.run(
            [sys.executable, relative],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            fail(f"{relative} exited {completed.returncode}\n{completed.stdout}\n{completed.stderr}")
        print(f"OK    {relative}")


def scan_tree() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".html", ".cff", ".py", ".json", ".yml", ".yaml", ".sh"}:
            continue
        check_privacy(path)
    print("OK    privacy sweep")


def main() -> int:
    if not CAMPUS.is_file() or not SLICE.is_file():
        fail("campus HTML missing")
    check_campus()
    check_offline(CAMPUS)
    check_offline(SLICE)
    check_zips()
    check_readme_links()
    scan_tree()
    check_labs()
    print("PASS  campus verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
