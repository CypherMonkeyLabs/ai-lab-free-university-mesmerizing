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
EXPECTED_LESSONS = 593

BANNED = ("linked" + "in.com", "mail" + "to:")
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
    text = path.read_text(encoding="utf-8", errors="replace")
    lowered = text.lower()
    for banned in BANNED:
        if banned in lowered:
            fail(f"{path.relative_to(ROOT)} contains {banned}")
    if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text):
        fail(f"{path.relative_to(ROOT)} contains an email address")


ALLOWED_URL_MARKERS = (
    "w3.org/2000/svg",
    "127.0.0.1",
    "https://github.com/cipher0x9/",
    "https://cipher0x9.github.io/ai-lab-free-university-mesmerizing/",
    "arxiv.org/",
    "doi.org/",
    "modelcontextprotocol.io/",
    "platform.openai.com/",
    "docs.anthropic.com/",
    "huggingface.co/",
    "cipher0x9.github.io/",
    "creativecommons.org/licenses/by-nc-sa/4.0/",
    "cyphermonkeylabs.com",
    "linktr.ee/cyphermonkey",
    "dev.to/cyphermonkey",
    "x.com/Cypher0x9",
    "airc.nist.gov",
)


def check_offline(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for match in re.finditer(r"<script[^>]+src\s*=\s*['\"]([^'\"]+)", text, flags=re.I):
        src = match.group(1)
        if src.startswith(("http://", "https://", "//")):
            fail(f"{path.name} loads a remote script {src}")
    if re.search(r"<link[^>]+stylesheet[^>]+href\s*=\s*['\"]https?:", text, flags=re.I):
        fail(f"{path.name} loads an external stylesheet")
    for url in re.findall(r"https?://[^\"'\s>]+", text):
        if any(marker in url for marker in ALLOWED_URL_MARKERS):
            continue
        fail(f"{path.name} has unexpected URL {url}")


def check_campus() -> None:
    text = CAMPUS.read_text(encoding="utf-8")
    visible = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", "", text, flags=re.I)
    h1_count = len(re.findall(r"<h1\b", visible, flags=re.I))
    if h1_count != 1:
        fail(f"shell has {h1_count} h1 elements, expected 1")
    if 'id="home"' not in text or 'id="stage"' not in text or 'id="campusCatalog"' not in text:
        fail("home, stage, or catalog is missing")
    if 'data-theme="dark"' not in text or 'data-theme="light"' not in text:
        fail("light and dark themes are missing")
    if "--cc-bg" not in text or "--cc-accent-4" not in text:
        fail("campus-core tokens are missing")
    curriculum = ROOT / "campus" / "assets" / "curriculum"
    catalog = json.loads((curriculum / "catalog.json").read_text(encoding="utf-8"))
    if len(catalog["order"]) != EXPECTED_LESSONS or len(set(catalog["order"])) != EXPECTED_LESSONS:
        fail(f"catalog lesson count is {len(catalog['order'])}, expected {EXPECTED_LESSONS}")
    found: list[str] = []
    for path in sorted(curriculum.glob("track-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if "hub" not in data or "lessons" not in data:
            fail(f"{path.name} is missing hub or lessons")
        found.extend(data["lessons"].keys())
    if sorted(found) != sorted(catalog["order"]):
        fail("track modules do not match the catalog")
    play = json.loads((curriculum / "play.json").read_text(encoding="utf-8"))["html"]
    for key in catalog["plays"]:
        if f'id="play-{key}"' not in play:
            fail(f"playground is missing #play-{key}")
    if len(catalog["plays"]) != 23:
        fail(f"expected 23 playgrounds, found {len(catalog['plays'])}")
    if "serviceWorker.register" not in text:
        fail("service worker is not registered")
    if not (ROOT / "campus" / "vendor" / "three.module.min.js").is_file():
        fail("Three.js is not vendored")
    print(f"OK    campus lessons={len(found)} shell_h1={h1_count} plays={len(catalog['plays'])}")


def _member_matches(archive: zipfile.ZipFile, arcname: str, source: Path) -> None:
    info = archive.getinfo(arcname)
    if info.extra:
        fail(f"{arcname} still has zip extra metadata")
    packed_hash = hashlib.sha256(archive.read(arcname)).hexdigest()
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    if packed_hash != source_hash:
        fail(f"{arcname} is stale relative to {source}")


def _campus_members() -> list[tuple[str, Path]]:
    campus = ROOT / "campus"
    ordered = [campus / "ai-lab-university.html", campus / "sw.js"]
    ordered += sorted((campus / "assets" / "audio").glob("*.wav"))
    ordered += sorted((campus / "assets" / "curriculum").glob("*.json"))
    ordered += sorted((campus / "assets" / "js").glob("*.js"))
    ordered += sorted((campus / "assets" / "cheats").glob("*"))
    ordered += sorted((campus / "vendor").glob("*.js"))
    return [(str(path.relative_to(campus)).replace("\\", "/"), path) for path in ordered]


def check_zips() -> None:
    campus_zip = ZIP_PAIRS[0][1]
    if not campus_zip.is_file():
        fail(f"missing zip {campus_zip.name}")
    members = _campus_members()
    wavs = [path for _arc, path in members if path.suffix == ".wav"]
    if len(wavs) < 40:
        fail(f"need 40 audio files, found {len(wavs)}")
    expected = [arc for arc, _path in members]
    with zipfile.ZipFile(campus_zip) as archive:
        names = archive.namelist()
        if names != expected:
            fail(f"{campus_zip.name} contains {len(names)} entries, expected {len(expected)}")
        for arc, path in members:
            _member_matches(archive, arc, path)
    print(f"OK    zip {campus_zip.name} {len(members)} files")

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
    if "593 study pages" not in text:
        fail("README does not state 593 study pages")
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "#", "mail" + "to:")):
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


def check_round3() -> None:
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    if "MIT License" not in license_text or "CC BY-NC-SA" not in license_text:
        fail("LICENSE does not state both MIT code and CC BY-NC-SA content")
    curriculum = ROOT / "campus" / "assets" / "curriculum"
    atlas = json.loads((curriculum / "atlas.json").read_text(encoding="utf-8"))["html"]
    flows = json.loads((curriculum / "flows.json").read_text(encoding="utf-8"))["html"]
    diagrams = atlas.count("data-atlas-diagram")
    animated = flows.count('data-animated="1"')
    if diagrams < 25 or animated < 12:
        fail(f"atlas has {diagrams} diagrams and {animated} animated flows")
    shell = CAMPUS.read_text(encoding="utf-8")
    for label in ("Diagrams", "Flows", "Charts", "Cheat Codes", "Play", "Ecosystem", "Downloads", "Careers"):
        if label not in shell:
            fail(f"course menu is missing {label}")
    if shell.count("data-real-chart") < 6 or "data-parallax" not in shell:
        fail("home is missing charts or parallax counters")
    downloads = json.loads((curriculum / "downloads.json").read_text(encoding="utf-8"))["html"]
    if downloads.count('.png"') < 10:
        fail("cheat codes are missing PNG sheets")
    hub = json.loads((curriculum / "track-01.json").read_text(encoding="utf-8"))["hub"]
    if hub.count("data-real-chart") < 6 or "data-parallax" not in hub:
        fail("a track page is missing charts or counters")
    print(f"OK    round3 diagrams={diagrams} animated_flows={animated}")


def main() -> int:
    if not CAMPUS.is_file() or not SLICE.is_file():
        fail("campus HTML missing")
    check_campus()
    check_offline(CAMPUS)
    check_offline(SLICE)
    check_zips()
    check_readme_links()
    scan_tree()
    check_round3()
    check_labs()
    print("PASS  campus verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
