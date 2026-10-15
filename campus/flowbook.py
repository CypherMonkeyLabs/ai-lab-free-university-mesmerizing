"""Assemble the visual scripts the campus renderer draws."""

from __future__ import annotations

from campus.v_back import LESSONS as LESSONS_BACK
from campus.v_front import LESSONS as LESSONS_FRONT
from campus.v_meta import AUDIOS, HOME, STUDIO, TRACKS
from campus.v_pool import LESSONS as LESSONS_POOL
from campus.v_ref import LESSONS as LESSONS_REF
from campus.walks import walk_audios

LAYOUTS = {"rail", "loop", "stack", "split", "gate", "funnel"}


def scripts() -> dict:
    lessons = {}
    lessons.update(LESSONS_FRONT)
    lessons.update(LESSONS_BACK)
    lessons.update(LESSONS_REF)
    lessons.update(LESSONS_POOL)
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
    audios = [
        {"id": ident, "title": title, "transcript": text}
        for ident, title, text in list(AUDIOS) + walk_audios()
    ]
    audio_ids = [item["id"] for item in audios]
    if len(audio_ids) != len(set(audio_ids)):
        raise SystemExit("duplicate audio id")
    return {
        "lessons": lessons,
        "tracks": tracks,
        "audios": audios,
        "home": HOME,
        "studio": STUDIO,
    }
