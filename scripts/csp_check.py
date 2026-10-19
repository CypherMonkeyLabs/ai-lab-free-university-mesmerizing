#!/usr/bin/env python3
"""Fail if a script, stylesheet, image, font, or fetch loads off this origin.

Citation anchors are not loads. Exit 1 when any off-origin load is found.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATTERNS = [
    (r"<(?:script|img|iframe|source|video|audio)[^>]+?\bsrc=\"(https?://[^\"]+)\"", "html src"),
    (r"<link[^>]+href=\"(https?://[^\"]+)\"", "html link"),
    (r"url\(\s*[\"']?(https?://[^)\"']+)", "css url()"),
    (r"@import\s+[\"'](https?://[^\"']+)", "css @import"),
    (r"\bimport\s*(?:\(|[^;]*from\s*)[\"'](https?://[^\"']+)", "js import"),
    (r"\bfetch\(\s*[\"'`](https?://[^\"'`]+)", "js fetch"),
    (r"new (?:Worker|WebSocket|EventSource)\(\s*[\"'`](https?://[^\"'`]+)", "js net"),
]
SKIP = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".pdf", ".zip", ".pptx", ".woff2", ".mp3", ".wav", ".ico"}
fail = []
files = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix.lower() not in SKIP and ".git" not in p.parts and "node_modules" not in p.parts]
for path in files:
    if path.suffix.lower() not in {".html", ".css", ".js", ".mjs", ".svg"}:
        continue
    text = path.read_text(errors="replace")
    for pattern, kind in PATTERNS:
        for match in re.finditer(pattern, text):
            fail.append(f"{path.relative_to(ROOT)}: off-origin {kind}: {match.group(1)}")
for item in fail:
    print("FAIL", item)
print("csp_check:", len(fail), "off-origin loads")
sys.exit(1 if fail else 0)
