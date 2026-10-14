"""Assemble the visual scripts the campus renderer draws."""

from __future__ import annotations

from campus.v_back import LESSONS as LESSONS_BACK
from campus.v_front import LESSONS as LESSONS_FRONT
from campus.v_meta import AUDIOS, HOME, STUDIO, TRACKS
from campus.v_ref import LESSONS as LESSONS_REF

LAYOUTS = {"rail", "loop", "stack", "split", "gate", "funnel"}


def scripts() -> dict:
    lessons = {}
    lessons.update(LESSONS_FRONT)
    lessons.update(LESSONS_BACK)
    lessons.update(LESSONS_REF)
    for lid, item in lessons.items():
        if item["layout"] not in LAYOUTS:
            raise SystemExit(f"{lid} has unknown layout {item['layout']}")
        if len(item["facts"]) < 3 or len(item["steps"]) < 4:
            raise SystemExit(f"{lid} is missing facts or steps")
        if not item["plate_rows"]:
            item["plate_rows"] = [title for title, _caption in item["steps"]]
    tracks = {}
    for tid, (layout, steps) in TRACKS.items():
        if layout not in LAYOUTS:
            raise SystemExit(f"track {tid} has unknown layout {layout}")
        tracks[tid] = {"id": tid, "layout": layout, "steps": steps}
    return {
        "lessons": lessons,
        "tracks": tracks,
        "audios": [{"id": ident, "title": title, "transcript": text} for ident, title, text in AUDIOS],
        "home": HOME,
        "studio": STUDIO,
    }
