#!/usr/bin/env python3
"""Strip forbidden brand links from the older campus shell and cheat sheets."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from campus.chrome import brand_nav  # noqa: E402

PANEL = (
    '<aside class="disclaimer-panel"><h2>A note from the student behind this lab</h2>'
    "<p>This is an independent, free, learning-only student project. "
    "It respects every company and vendor, and every trademark belongs to its owner. "
    "It is not affiliated with or endorsed by any of them. "
    'If anyone has a concern, the content will be removed or corrected promptly via '
    '<a href="https://cyphermonkeylabs.com/#contact">the contact page</a>. '
    "Nothing here is sold. The author is happy to volunteer.</p></aside>"
)
NAV_RE = re.compile(r'<nav class="brand-links"[\s\S]*?</nav>')
NEXT_RE = re.compile(r'<nav class="next-labs"[\s\S]*?</nav>')
OLD_DISC = (
    "Independent educational project, not affiliated with or endorsed by any vendor. "
    "Trademarks belong to their owners. MIT code, CC BY-NC-SA content."
)
SISTER = re.compile(
    r"https://cyphermonkeylabs\.com/(?:uc-lab|webex-lab|five9-lab|nice-cxone-lab|"
    r"genesys-cloud-lab|amazon-connect-lab|microsoft-voice-cc-lab|sip-universe-lab)[^\"'\s<]*"
)


def clean(text: str) -> str:
    text = NAV_RE.sub(brand_nav(), text)
    text = NEXT_RE.sub("", text)
    text = text.replace("<strong>CYPHER0X9</strong>", "<strong>CypherMonkey Labs</strong>")
    text = text.replace("Work with us", "Happy to volunteer")
    text = text.replace(OLD_DISC, "See the learning-only note below. MIT code, CC BY-NC-SA content.")
    text = SISTER.sub("https://cyphermonkeylabs.com/", text)
    text = text.replace("https://github.com/cipher0x9", "https://github.com/CypherMonkeyLabs")
    text = text.replace("https://x.com/Cypher0x9", "https://cyphermonkeylabs.com/")
    text = text.replace("https://huggingface.co/Cypher0x9", "https://cyphermonkeylabs.com/")
    text = text.replace("https://cipher0x9.github.io/gemini-gems-free-gallery/", "https://cyphermonkeylabs.com/")
    if "learning-only student project" not in text and "<footer" in text:
        text = text.replace("<footer", PANEL + "<footer", 1)
    elif "learning-only student project" not in text and "</body>" in text:
        text = text.replace("</body>", PANEL + "</body>", 1)
    return text


def main() -> int:
    changed = 0
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        updated = clean(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(path.relative_to(ROOT))
    print(f"updated {changed} html files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
