"""Study pages imported from the 2026-10-14 idea pool.

The pool is 453 pages: 19 long rooms, 333 glossary entries, and 101 interview
drills. Sixteen glossary notes fold onto glossary pages that already existed.
Counted against the 128 course lessons on main, the ids do not overlap, so
128 + 453 = 581 before the ecosystem track added in this campus.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

_DIR = Path(__file__).resolve().parent / "pool"
_DIAGRAMS = Path(__file__).resolve().parent / "assets" / "origin-diagrams"

LESSONS: list[dict] = json.loads((_DIR / "lessons.json").read_text(encoding="utf-8"))
QUIZ: list[dict] = json.loads((_DIR / "quiz.json").read_text(encoding="utf-8"))
CARDS: list[dict] = json.loads((_DIR / "cards.json").read_text(encoding="utf-8"))
SCENARIOS: list[dict] = json.loads((_DIR / "scenarios.json").read_text(encoding="utf-8"))
FOLDS: list[dict] = json.loads((_DIR / "folds.json").read_text(encoding="utf-8"))

_CARRIED = (
    "Carried from the 2026-10-14 study draft and not re-fetched for this campus on 2026-10-15. "
    "Open the cited page before you repeat a model id, a price, or a product step."
)


def apply_folds(lessons: list[dict]) -> None:
    by_id = {item["id"]: item for item in lessons}
    for fold in FOLDS:
        item = by_id.get(fold["id"])
        if not item:
            continue
        if any(block.get("t") == "note" and block.get("text") == fold["text"] for block in item["blocks"]):
            continue
        item["blocks"].append({"t": "note", "title": fold["title"], "text": fold["text"]})


def _scope_svg(svg: str, prefix: str) -> str:
    if "<script" in svg.lower():
        raise SystemExit(f"diagram {prefix} contains a script")
    ids = sorted(set(re.findall(r'\bid="([^"]+)"', svg)), key=len, reverse=True)
    for ident in ids:
        svg = re.sub(rf'\bid="{re.escape(ident)}"', f'id="{prefix}-{ident}"', svg)
        svg = re.sub(rf"url\(#{re.escape(ident)}\)", f"url(#{prefix}-{ident})", svg)
        svg = re.sub(rf'href="#{re.escape(ident)}"', f'href="#{prefix}-{ident}"', svg)
    return svg.replace("<svg ", '<svg class="origin-diagram" ', 1)


def attach_diagrams(lessons: list[dict]) -> int:
    """Inline the 38 origin architecture and sequence drawings onto the 19 rooms."""
    attached = 0
    for item in lessons:
        match = re.search(r"t(\d+)r(\d+)$", item["id"])
        if not match:
            continue
        room = f"T{match.group(1)}-R{int(match.group(2)):02d}"
        folder = _DIAGRAMS / room
        if not folder.is_dir():
            continue
        item["blocks"].append({"t": "h", "text": "Diagrams from the study draft"})
        item["blocks"].append({"t": "note", "title": "Not re-fetched", "text": _CARRIED})
        for name, caption in (
            ("arch.svg", "Architecture map for this room. A teaching drawing, not a vendor poster."),
            ("sequence.svg", "Sequence for this room. Who speaks at each step."),
        ):
            path = folder / name
            if not path.is_file():
                continue
            svg = _scope_svg(path.read_text(encoding="utf-8"), f"{item['id']}-{name.split('.')[0]}")
            item["blocks"].append({"t": "svg", "html": svg, "caption": caption})
            attached += 1
    return attached
