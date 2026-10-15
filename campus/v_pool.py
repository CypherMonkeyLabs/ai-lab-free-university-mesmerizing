"""Visual scripts for imported pages and the ecosystem track."""

from __future__ import annotations

from campus.flagship_lessons import LESSONS as ECO
from campus.pool import LESSONS as POOL

LESSONS: dict[str, dict] = {}

_ICONS = ("shield", "map", "pipes", "ladder", "voice", "clipboard", "gate", "compass", "trace", "metrics")
_HEROES = ("route", "layers", "library", "cycle", "gate", "shield", "speech", "stream")
_PLATES = ("pipeline", "stack", "layers", "gates", "bars", "split")
_LAYOUTS = ("rail", "loop", "stack", "split", "gate", "funnel")


def _clip(text: str, limit: int) -> str:
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def _add(item: dict, index: int) -> None:
    title = _clip(item["title"], 80)
    summary = _clip(item["summary"], 140)
    steps = (
        ("Name it", title),
        ("The point", summary),
        ("Check", "A person can mark this pass or fail without asking the model."),
        ("Stop", "Side effects wait. A missing source is a refusal."),
    )
    facts = (
        ("Page", item["id"]),
        ("Track", item["school"]),
        ("Use", summary or title),
    )
    LESSONS[item["id"]] = {
        "id": item["id"],
        "layout": _LAYOUTS[index % len(_LAYOUTS)],
        "icon": _ICONS[index % len(_ICONS)],
        "hero": _HEROES[index % len(_HEROES)],
        "plate": _PLATES[index % len(_PLATES)],
        "facts": facts,
        "steps": steps,
        "plate_rows": [step[0] for step in steps],
        "plate_note": summary or title,
        "widgets": [],
    }


for index, item in enumerate(POOL + ECO):
    _add(item, index)
