"""Compose lesson chrome, track hubs, the studio, and the visual stylesheet."""

from __future__ import annotations

import html
from pathlib import Path

from campus.art import hero_svg, icon_svg, plate_svg, walk_figure
from campus.flowbook import scripts
from campus.studio import audio_html, widget_html
from campus.v_meta import TRACK_EMOJI

HERE = Path(__file__).resolve().parent
VISUAL_CSS = (HERE / "visual.css").read_text(encoding="utf-8")
VISUAL_JS = (HERE / "player.js").read_text(encoding="utf-8")

_BOOK = None
_SEQ = 0

ACCENTS = {
    "00": "#6366F1",
    "01": "#A78BFA",
    "02": "#38BDF8",
    "03": "#0F9B8E",
    "04": "#F5B942",
    "05": "#22C55E",
    "06": "#FB7185",
    "07": "#818CF8",
    "08": "#38BDF8",
    "09": "#F5B942",
    "10": "#A78BFA",
    "11": "#FB7185",
    "12": "#0F9B8E",
    "13": "#22C55E",
    "GL": "#94A3B8",
    "IV": "#F5B942",
    "FQ": "#38BDF8",
}
LAYOUT_HERO = {
    "rail": "route",
    "stack": "layers",
    "split": "library",
    "loop": "cycle",
    "gate": "gate",
    "funnel": "library",
}


def book() -> dict:
    global _BOOK
    if _BOOK is None:
        _BOOK = scripts()
    return _BOOK


def gid() -> str:
    global _SEQ
    _SEQ += 1
    return f"gg{_SEQ}"


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def accent(school_id: str) -> str:
    return ACCENTS.get(school_id, "#6366F1")


def _spec(lesson_id: str) -> dict:
    found = book()["lessons"].get(lesson_id)
    if not found:
        raise SystemExit(f"No visual script for {lesson_id}")
    return found


def _chips(spec: dict) -> list[str]:
    chips = []
    for _label, value in spec["facts"][:3]:
        chips.append(value if len(value) <= 22 else value[:21] + "…")
    return chips


def nav_icon(item: dict) -> str:
    spec = _spec(item["id"])
    return icon_svg(spec["icon"], f"nav-{item['id']}")


def _keys(item: dict, index: int, total: int, spec: dict) -> str:
    cells = [
        ("Lesson", f"{index:02d} of {total:02d}"),
        ("Time", f"{item['minutes']} min"),
        ("Level", {"core": "Core", "practice": "Practice", "advanced": "Advanced"}[item["level"]]),
    ]
    for label, value in spec["facts"][:3]:
        cells.append((label, value))
    body = "".join(f"<div><dt>{esc(label)}</dt><dd>{esc(value)}</dd></div>" for label, value in cells)
    return f'<dl class="keys">{body}</dl>'


def _clip(ident: str) -> str:
    clips = book()["audios"]
    for index, clip in enumerate(clips, start=1):
        if clip["id"] == ident:
            return audio_html(index, len(clips), clip["title"], clip["transcript"], clip["id"])
    raise SystemExit(f"No audio clip for {ident}")


def lesson_head(item: dict, index: int, total: int, school: dict) -> str:
    spec = _spec(item["id"])
    level = {"core": "Core", "practice": "Practice", "advanced": "Advanced"}[item["level"]]
    icon = icon_svg(spec["icon"], f"icon-{item['id']}", f"{index:02d}")
    hero = hero_svg(spec["hero"], item["id"], item["title"], _chips(spec), gid())
    flow = walk_figure(item["id"], item["title"], spec["layout"], list(spec["steps"]))
    return (
        f'<header class="lesson-top">'
        f"<div>"
        f'<p class="kicker"><a href="#school-{esc(item["school"])}">{esc(school["name"])}</a>'
        f"<span>{index} of {total}</span><span>{level}</span><span>{item['minutes']} min</span></p>"
        f'<div class="lesson-idline">{icon}<span class="lesson-num">Lesson {index:02d}</span></div>'
        f"<h1>{esc(item['title'])}</h1>"
        f'<p class="lede">{esc(item["summary"])}</p>'
        f"{_keys(item, index, total, spec)}"
        f"</div>"
        f'<div class="hero-art">{hero}</div>'
        f"</header>{flow}"
    )


def lesson_tail(item: dict) -> str:
    spec = _spec(item["id"])
    plate = plate_svg(spec["plate"], item["id"], item["title"], spec["plate_rows"], spec["plate_note"])
    widgets = "".join(widget_html(name) for name in spec["widgets"])
    return (
        f'<figure class="diagram plate"><figcaption>Diagram. {esc(spec["plate_note"] or item["title"])}</figcaption>'
        f"{plate}</figure>{widgets}"
    )


def hub_html(school: dict, items: list[dict]) -> str:
    track = book()["tracks"][school["id"]]
    scene = LAYOUT_HERO[track["layout"]]
    chips = [step[0] for step in track["steps"][:3]]
    poster = hero_svg(scene, f"track-{school['id']}", school["name"], chips, gid())
    flow = walk_figure(f"track-{school['id']}", school["name"], track["layout"], list(track["steps"]))
    return (
        f'<div class="hub-hero">{poster}{_clip(school["id"])}{flow}</div>'
    )


def lesson_cards(items: list[dict]) -> str:
    rows = []
    for index, item in enumerate(items, start=1):
        icon = icon_svg(_spec(item["id"])["icon"], f"card-{item['id']}", f"{index:02d}")
        rows.append(
            f'<li><a href="#{item["id"]}"><span class="ln">{index:02d}</span>{icon}'
            f"<span><strong>{esc(item['title'])}</strong><em>{esc(item['summary'])}</em></span>"
            f'<span class="mins">{item["minutes"]} min</span></a></li>'
        )
    return f'<ol class="hub-lessons">{"".join(rows)}</ol>'


def home_poster() -> str:
    home = book()["home"]
    chips = [step[0] for step in home["steps"][:3]]
    poster = hero_svg("route", "home", "From a prompt to a gate", chips, gid())
    return f'<div class="hero-art">{poster}</div>'


def home_extra() -> str:
    home = book()["home"]
    flow = walk_figure("home", "From a prompt to a gate", home["layout"], list(home["steps"]))
    return (
        '<section class="block"><div class="block-head"><h2>How a tested answer is built</h2>'
        "<p>Play the path. Each step is a habit the tracks practice.</p></div>"
        f"{flow}{_clip('home')}</section>"
    )


def map_poster() -> str:
    from campus.schema import SCHOOLS

    body = []
    tracks = [school for school in SCHOOLS if school["kind"] == "track"]
    for index, school in enumerate(tracks):
        col = index % 7
        row = index // 7
        x = 36 + col * 108
        y = 36 + row * 120
        body.append(
            f'<rect x="{x}" y="{y}" width="96" height="78" rx="14" fill="#141c33" stroke="#6366F1"/>'
            f'<text x="{x + 48}" y="{y + 28}" text-anchor="middle" fill="#C7D2FE" font-size="12" font-family="system-ui,sans-serif">{esc(school["id"])}</text>'
            f'<text x="{x + 48}" y="{y + 52}" text-anchor="middle" fill="#F8FAFC" font-size="11" font-family="system-ui,sans-serif">{esc(school["name"][:16])}</text>'
        )
    svg = (
        '<svg class="hero-svg" data-art="map-tracks" viewBox="0 0 800 280" role="img" aria-label="Fourteen tracks">'
        '<rect width="800" height="280" rx="20" fill="#0B1220"/>'
        + "".join(body)
        + "</svg>"
    )
    return f'<div class="hero-art">{svg}</div>'


def studio_page() -> str:
    studio = book()["studio"]
    names = ("tokenizer", "cosine", "attention", "rag", "sample", "context", "loss", "latency", "scorecard", "embed")
    widgets = "".join(widget_html(name) for name in names)
    flow = walk_figure("studio", "What the studio is showing", studio["layout"], list(studio["steps"]))
    return (
        '<section id="studio" data-panel="studio">'
        '<p class="eyebrow">Zero keys · runs in this page</p>'
        "<h1>Studio</h1>"
        '<p class="lede">Toy instruments for tokens, similarity, attention, retrieval, sampling, cost, and evals. '
        "They use fixed numbers so you can see the mechanism. They do not call a model.</p>"
        f'{_clip("studio")}{flow}{widgets}</section>'
    )


def studio_nav() -> str:
    return (
        '<a class="ll studio-link" href="#studio" data-search="studio tokenizer cosine attention retrieval heatmap '
        'temperature top-p loss chart embedding latency scorecard demo">'
        '<span class="ln">Lab</span><span class="nav-ico"></span><span>Studio</span></a>'
    )


def emoji_for(school_id: str) -> str:
    return TRACK_EMOJI.get(school_id, "•")


def measure(page: str) -> dict:
    lessons = book()["lessons"]
    counts = {
        "svg": page.count("<svg"),
        "flows": page.count('class="walk"'),
        "audio": page.count("<audio "),
        "widgets": page.count('data-widget="'),
        "heroes": page.count('data-art="hero-'),
        "plates": page.count('data-art="plate-'),
        "icons": page.count('data-art="icon-'),
        "unique_art": len({item for item in _art_ids(page)}),
    }
    if counts["svg"] < 500:
        raise SystemExit(f"Need 500 SVG illustrations, found {counts['svg']}")
    if counts["flows"] < 100:
        raise SystemExit(f"Need 100 flows, found {counts['flows']}")
    if not 10 <= counts["audio"] <= 20:
        raise SystemExit(f"Audio clips must be between 10 and 20, found {counts['audio']}")
    if counts["heroes"] < len(lessons):
        raise SystemExit("A lesson is missing a hero")
    if counts["plates"] < len(lessons):
        raise SystemExit("A lesson is missing a plate")
    if "cdn" in page.lower():
        raise SystemExit("Generated page contains a forbidden marker")
    return counts


def _art_ids(page: str):
    marker = 'data-art="'
    start = 0
    while True:
        found = page.find(marker, start)
        if found < 0:
            return
        found += len(marker)
        end = page.find('"', found)
        yield page[found:end]
        start = end + 1
