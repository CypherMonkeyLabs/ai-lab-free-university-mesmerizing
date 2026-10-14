"""Visual scripts for lessons imported from the idea pool."""

from __future__ import annotations

from campus.pool import LESSONS

LESSONS_VISUAL: dict[str, dict] = {}


def _short(text: str, limit: int) -> str:
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


for _item in LESSONS:
    _titles: list[str] = []
    for _block in _item["blocks"]:
        if _block.get("t") != "h":
            continue
        label = _short(_block["text"], 42)
        if label not in _titles:
            _titles.append(label)
        if len(_titles) == 4:
            break
    while len(_titles) < 4:
        _titles.append(_item["title"] if not _titles else f"Point {len(_titles) + 1}")
    _summary = _short(_item["summary"], 160) or _item["title"]
    _steps = tuple((title, _summary) for title in _titles[:4])
    LESSONS_VISUAL[_item["id"]] = {
        "id": _item["id"],
        "layout": "rail",
        "icon": "clipboard",
        "hero": "library",
        "plate": "pipeline",
        "facts": (
            ("Track", _item["school"]),
            ("Source", "Cited notes"),
            ("Check", "Open the citation"),
        ),
        "steps": _steps,
        "plate_rows": [title for title, _caption in _steps],
        "plate_note": _summary,
        "widgets": [],
    }
