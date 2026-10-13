#!/usr/bin/env python3
"""Check the campus count, offline rule, privacy sweep, labs, and zip freshness."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAMPUS = ROOT / "campus" / "ai-lab-university.html"
SLICE = ROOT / "campus" / "golden-slice.html"
README = ROOT / "README.md"
EXPECTED_SECTIONS = 259

BANNED = ("link" + "tr.ee", "cypher" + "monkey", "cis" + "co")
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
        if "w3.org/2000/svg" in url or "127.0.0.1" in url:
            continue
        if url.startswith("https://github.com/cipher0x9/"):
            continue
        fail(f"{path.name} has unexpected URL {url}")


def check_campus() -> None:
    text = CAMPUS.read_text(encoding="utf-8")
    ids = re.findall(r'<article class="sec" id="([^"]+)"', text)
    if len(ids) != EXPECTED_SECTIONS or len(set(ids)) != EXPECTED_SECTIONS:
        fail(f"article count is {len(ids)} unique {len(set(ids))}, expected {EXPECTED_SECTIONS}")
    match = re.search(r"window\.AILAB_META = (\{.*?\});", text)
    if not match:
        fail("AILAB_META missing")
    meta = json.loads(match.group(1))
    if meta["stats"]["sections"] != EXPECTED_SECTIONS:
        fail("meta section count drifted")
    if set(meta["section_ids"]) != set(ids):
        fail("meta section_ids do not match articles")
    if sum(meta["stats"]["by_school"].values()) != EXPECTED_SECTIONS:
        fail("by_school does not sum to the section count")
    nav_ids = re.findall(r'<a class="nav" data-id="([^"]+)"', text)
    if set(nav_ids) != set(ids):
        fail("sidebar nav does not match articles")
    if 'value="paper"' not in text:
        fail("Paper theme option missing")
    print(f"OK    campus sections={len(ids)} schools={len(meta['schools'])}")


def check_zips() -> None:
    for source, archive_path in ZIP_PAIRS:
        if not archive_path.is_file():
            fail(f"missing zip {archive_path.name}")
        source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        with zipfile.ZipFile(archive_path) as archive:
            names = archive.namelist()
            if names != [source.name]:
                fail(f"{archive_path.name} contains {names}, expected [{source.name}]")
            info = archive.getinfo(source.name)
            if info.extra:
                fail(f"{archive_path.name} still has zip extra metadata")
            packed_hash = hashlib.sha256(archive.read(source.name)).hexdigest()
        if packed_hash != source_hash:
            fail(f"{archive_path.name} is stale relative to {source.name}")
        print(f"OK    zip {archive_path.name}")


def check_readme_links() -> None:
    text = README.read_text(encoding="utf-8")
    if "Sections-259" not in text or "**259 sections**" not in text:
        fail("README does not state 259 sections")
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
