"""Imported idea-pool lessons, drills, and practice data."""

from __future__ import annotations

import json
from pathlib import Path

_DIR = Path(__file__).resolve().parent / "pool"


def _load(name: str):
    return json.loads((_DIR / name).read_text(encoding="utf-8"))


LESSONS: list[dict] = _load("lessons.json")
QUIZ: list[dict] = _load("quiz.json")
CARDS: list[dict] = _load("cards.json")
SCENARIOS: list[dict] = _load("scenarios.json")
FOLDS: list[dict] = _load("folds.json")


def apply_folds(lessons: list[dict]) -> None:
    by_id = {item["id"]: item for item in lessons}
    for fold in FOLDS:
        item = by_id.get(fold["id"])
        if not item:
            continue
        if any(block.get("t") == "note" and block.get("text") == fold["text"] for block in item["blocks"]):
            continue
        item["blocks"].append({"t": "note", "title": fold["title"], "text": fold["text"]})
