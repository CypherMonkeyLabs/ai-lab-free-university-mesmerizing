"""Compose lesson chrome, track hubs, the studio, and the visual stylesheet."""

from __future__ import annotations

import html
import re
from pathlib import Path

from campus.art import hero_svg, icon_svg, plate_svg, walk_figure
from campus.demos import demos_html
from campus.flowbook import scripts
from campus.gallery import gallery_html
from campus.media import wav_bytes
from campus.studio import audio_html, widget_html
from campus.v_meta import TRACK_EMOJI
from campus.variants import extra_flows
from campus.walks import WALKS

HERE = Path(__file__).resolve().parent
VISUAL_CSS = (HERE / "visual.css").read_text(encoding="utf-8")
VISUAL_JS = (HERE / "player.js").read_text(encoding="utf-8") + "\n" + (HERE / "demo.js").read_text(encoding="utf-8")

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
    "14": "#38BDF8",
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


def lesson_head(item: dict, index: int, total: int, school: dict, try_href: str = "", try_name: str = "") -> str:
    spec = _spec(item["id"])
    level = {"core": "Core", "practice": "Practice", "advanced": "Advanced"}[item["level"]]
    icon = icon_svg(spec["icon"], f"icon-{item['id']}", f"{index:02d}")
    hero = hero_svg(spec["hero"], item["id"], item["title"], _chips(spec), gid())
    flow = walk_figure(item["id"], item["title"], spec["layout"], list(spec["steps"]))
    try_row = ""
    if try_href:
        try_row = (
            f'<p class="try-row"><a class="btn try-link" href="{esc(try_href)}">Try it: {esc(try_name)}</a></p>'
        )
    return (
        f'<header class="lesson-top">'
        f"<div>"
        f'<p class="kicker"><a href="#school-{esc(item["school"])}">{esc(school["name"])}</a>'
        f"<span>{index} of {total}</span><span>{level}</span><span>{item['minutes']} min</span></p>"
        f'<div class="lesson-idline">{icon}<span class="lesson-num">Lesson {index:02d}</span></div>'
        f"<h1>{esc(item['title'])}</h1>"
        f'<p class="why-kicker">Why it matters</p>'
        f'<p class="lede">{esc(item["summary"])}</p>'
        f"{try_row}"
        f"{_keys(item, index, total, spec)}"
        f"</div>"
        f'<div class="hero-art">{hero}</div>'
        f"</header>{flow}"
    )


def lesson_tail(item: dict) -> str:
    spec = _spec(item["id"])
    plate = plate_svg(spec["plate"], item["id"], item["title"], spec["plate_rows"], spec["plate_note"])
    widgets = "".join(widget_html(name) for name in spec["widgets"])
    flows = "".join(
        walk_figure(ident, title, layout, steps)
        for ident, title, layout, steps in extra_flows(item["id"], spec)
    )
    return (
        f"{flows}{gallery_html(item, spec)}"
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

    cards = []
    tracks = [school for school in SCHOOLS if school["kind"] == "track"]
    for school in tracks:
        svg = (
            f'<svg class="map-svg" data-art="map-{esc(school["id"])}" viewBox="0 0 200 64" role="img" '
            f'aria-label="{esc(school["name"])}">'
            f'<rect width="200" height="64" rx="12" fill="#0B1220"/>'
            f'<text x="12" y="26" fill="#C7D2FE" font-size="12" font-family="system-ui,sans-serif">{esc(school["id"])}</text>'
            f'<text x="12" y="48" fill="#F8FAFC" font-size="13" font-family="system-ui,sans-serif">{esc(school["name"][:22])}</text>'
            f"</svg>"
        )
        cards.append(
            f'<a class="map-node" href="#school-{esc(school["id"])}" data-map-school="{esc(school["id"])}">'
            f"{svg}<span class=\"map-count\">0 of 0</span>"
            f'<span class="map-meter" aria-hidden="true"><i class="map-fill"></i></span></a>'
        )
    return f'<nav class="track-map" aria-label="Visual track map">{"".join(cards)}</nav>'


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
        f'{_clip("studio")}{flow}{widgets}'
        '<h2>Charts and calculators</h2>'
        '<p class="lede">Charts counted from this course are labeled that way. Every other number is a sketch. None of them call a model.</p>'
        f"{demos_html()}</section>"
    )


def achievements_html() -> str:
    return (
        '<section class="block" id="marks">'
        '<div class="block-head"><h2>Marks</h2>'
        '<p id="markEmpty">Complete a lesson to earn the first mark. Marks stay in this browser.</p></div>'
        '<ul class="badges" id="badgeList"></ul></section>'
    )


def builds_nav() -> str:
    return (
        '<a class="ll builds-link" href="#builds" data-search="builds walkthroughs end to end local harness retrieval '
        'tools adapter memory setup eval gate">'
        '<span class="ln">Lab</span><span class="nav-ico"></span><span>Builds</span></a>'
    )


def _reel(ident: str, title: str, layout: str, steps: list) -> str:
    figure = walk_figure(ident, title, layout, steps)
    figure = figure.replace('class="walk"', 'class="walk reel"', 1)
    return figure.replace(">Animated flow<", ">Walkthrough<", 1)


def builds_page() -> str:
    jumps = []
    parts = []
    for ident, title, layout, steps, narration in WALKS:
        jumps.append(
            f'<button type="button" class="btn jump-build" data-target="{esc(ident)}">{esc(title)}</button>'
        )
        parts.append(
            f'<article class="build" id="{esc(ident)}"><h2>{esc(title)}</h2>'
            f"<p>{esc(narration)}</p>{_clip(ident)}{_reel(ident, title, layout, list(steps))}</article>"
        )
    return (
        '<section id="builds" data-panel="builds">'
        '<p class="eyebrow">End to end · still in this page</p>'
        "<h1>Builds</h1>"
        '<p class="lede">Walk through a whole build. Each sequence is one the tracks already teach. '
        "Play, pause, step, and speed work the same way as a lesson flow.</p>"
        f'<div class="build-index">{"".join(jumps)}</div>{"".join(parts)}</section>'
    )


def write_audio_assets() -> int:
    folder = HERE / "assets" / "audio"
    folder.mkdir(parents=True, exist_ok=True)
    keep = set()
    for clip in book()["audios"]:
        name = clip["id"] + ".wav"
        if "/" in name or "\\" in name or name.startswith("."):
            raise SystemExit(f"bad audio name {name}")
        keep.add(name)
        (folder / name).write_bytes(wav_bytes(clip["id"]))
    for old in folder.glob("*.wav"):
        if old.name not in keep:
            old.unlink()
    return len(keep)


def studio_nav() -> str:
    return (
        '<a class="ll studio-link" href="#studio" data-search="studio tokenizer cosine attention retrieval heatmap '
        'temperature top-p loss chart embedding latency scorecard demo">'
        '<span class="ln">Lab</span><span class="nav-ico"></span><span>Studio</span></a>'
    )


def emoji_for(school_id: str) -> str:
    return TRACK_EMOJI.get(school_id, "•")


def _unique_svg_bodies(page: str) -> int:
    seen = set()
    start = 0
    while True:
        found = page.find("<svg", start)
        if found < 0:
            break
        end = page.find("</svg>", found)
        if end < 0:
            break
        body = re.sub(r'\sdata-art="[^"]*"', "", page[found : end + 6])
        seen.add(body)
        start = end + 6
    return len(seen)


def _attr_values(page: str, name: str) -> set[str]:
    return set(re.findall(rf'{name}="([^"]+)"', page))


def measure(page: str) -> dict:
    lessons = book()["lessons"]
    lesson_flows = []
    for article in re.findall(r'<article class="lesson"[\s\S]*?</article>', page):
        lesson_flows.append(article.count('class="walk"'))
    counts = {
        "svg": page.count("<svg"),
        "unique_svg": _unique_svg_bodies(page),
        "flows": page.count('class="walk"') + page.count('class="walk reel"'),
        "reels": page.count('class="walk reel"'),
        "audio": page.count("<audio "),
        "widgets": page.count('data-widget="'),
        "heroes": page.count('data-art="hero-'),
        "plates": page.count('data-art="plate-'),
        "icons": page.count('data-art="icon-'),
        "unique_art": len({item for item in _art_ids(page)}),
        "charts": len(_attr_values(page, "data-chart")),
        "demos": len(_attr_values(page, "data-demo")),
        "min_lesson_flows": min(lesson_flows) if lesson_flows else 0,
    }
    if counts["svg"] < 3000:
        raise SystemExit(f"Need 3000 SVG illustrations, found {counts['svg']}")
    if counts["unique_svg"] < 3000:
        raise SystemExit(f"Need 3000 distinct SVG bodies, found {counts['unique_svg']}")
    if counts["flows"] < 400:
        raise SystemExit(f"Need 400 flows, found {counts['flows']}")
    if counts["min_lesson_flows"] < 3:
        raise SystemExit(f"A lesson has fewer than 3 flows ({counts['min_lesson_flows']})")
    if counts["reels"] < 20:
        raise SystemExit(f"Need 20 walkthroughs, found {counts['reels']}")
    if counts["audio"] < 40:
        raise SystemExit(f"Need 40 audio clips, found {counts['audio']}")
    if counts["charts"] < 40:
        raise SystemExit(f"Need 40 charts, found {counts['charts']}")
    if counts["demos"] < 50:
        raise SystemExit(f"Need 50 demos, found {counts['demos']}")
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
