#!/usr/bin/env python3
"""Check THIRD_PARTY_MANIFEST.json hashes and notices.

  python3 scripts/licence_manifest.py
  python3 scripts/licence_manifest.py --write
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAN = ROOT / "THIRD_PARTY_MANIFEST.json"
SCAN = ["campus/vendor"]


def sha(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    data = json.loads(MAN.read_text())
    files = {item["path"]: item for component in data["components"] for item in component["files"]}
    problems = []
    if "--write" in sys.argv:
        for path, item in files.items():
            item["sha256"] = sha(ROOT / path)
        MAN.write_text(json.dumps(data, indent=2) + "\n")
        print("rewrote", MAN)
        return 0
    for path, item in files.items():
        target = ROOT / path
        if not target.is_file():
            problems.append(f"listed but missing: {path}")
        elif sha(target) != item["sha256"]:
            problems.append(f"hash mismatch: {path}")
    for folder in SCAN:
        for path in sorted((ROOT / folder).rglob("*")):
            if path.is_file() and path.suffix != ".md" and path.relative_to(ROOT).as_posix() not in files:
                problems.append(f"vendored file not in manifest: {path.relative_to(ROOT)}")
    notices = (ROOT / "THIRD_PARTY_NOTICES.md").read_text()
    if re.search(r"\bverify\b", notices, re.I):
        problems.append("THIRD_PARTY_NOTICES.md still contains 'verify'")
    for problem in problems:
        print("FAIL", problem)
    print("manifest:", len(files), "files,", len(data["components"]), "components,", len(problems), "problems")
    return 1 if problems else 0


sys.exit(main())
