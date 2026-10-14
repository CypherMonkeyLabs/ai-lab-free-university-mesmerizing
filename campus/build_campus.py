#!/usr/bin/env python3
"""Build the single-file offline campus at campus/ai-lab-university.html."""

from __future__ import annotations

import html
import re
from pathlib import Path

from campus.diagrams import FIGURES
from campus.lessons_apply import LESSONS as LESSONS_APPLY
from campus.lessons_core import LESSONS as LESSONS_CORE
from campus.lessons_ref import LESSONS as LESSONS_REF
from campus.schema import PATHS, SCHOOLS
from campus.visuals import (
    VISUAL_CSS,
    VISUAL_JS,
    accent,
    emoji_for,
    home_extra,
    home_poster,
    hub_html,
    lesson_cards,
    lesson_head,
    lesson_tail,
    map_poster,
    measure,
    nav_icon,
    studio_nav,
    studio_page,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "campus" / "ai-lab-university.html"
HERO = ROOT / "docs" / "assets" / "hero.svg"

BANNED = (
    "share freely",
    "builder lens",
    "licc",
    "cis" + "co",
    "linktree",
    "mysticism",
    "without religion",
    "confused builder",
    "760mb",
    "emoji-free",
)


def inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return escaped


def render_blocks(lesson: dict) -> str:
    parts: list[str] = []
    for index, block in enumerate(lesson["blocks"]):
        kind = block["t"]
        if kind == "p":
            parts.append(f"<p>{inline(block['text'])}</p>")
        elif kind == "h":
            parts.append(f"<h3>{inline(block['text'])}</h3>")
        elif kind == "ul":
            items = "".join(f"<li>{inline(item)}</li>" for item in block["items"])
            parts.append(f"<ul>{items}</ul>")
        elif kind == "ol":
            items = "".join(f"<li>{inline(item)}</li>" for item in block["items"])
            parts.append(f"<ol>{items}</ol>")
        elif kind == "table":
            head = "".join(f"<th>{inline(cell)}</th>" for cell in block["headers"])
            rows = []
            for row in block["rows"]:
                cells = "".join(f"<td>{inline(cell)}</td>" for cell in row)
                rows.append(f"<tr>{cells}</tr>")
            parts.append(f"<div class=\"table-wrap\"><table><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>")
        elif kind == "pre":
            parts.append(f"<pre><code>{html.escape(block['text'])}</code></pre>")
        elif kind == "diagram":
            svg = FIGURES[block["id"]]
            parts.append(
                f"<figure class=\"diagram\" id=\"fig-{lesson['id']}-{index}\">{svg}"
                f"<figcaption>{inline(block['caption'])}</figcaption></figure>"
            )
        elif kind == "practice":
            parts.append(f"<aside class=\"callout practice\"><h3>Practice</h3><p>{inline(block['text'])}</p></aside>")
        elif kind == "check":
            parts.append(
                "<aside class=\"callout check\"><h3>Check</h3>"
                f"<p>{inline(block['q'])}</p>"
                f"<details><summary>Show the answer</summary><p>{inline(block['a'])}</p></details></aside>"
            )
        elif kind == "note":
            parts.append(f"<aside class=\"callout note\"><h3>{inline(block['title'])}</h3><p>{inline(block['text'])}</p></aside>")
        elif kind == "warn":
            parts.append(f"<aside class=\"callout warn\"><h3>{inline(block['title'])}</h3><p>{inline(block['text'])}</p></aside>")
        else:
            raise SystemExit(f"Unknown block {kind} in {lesson['id']}")
    return "".join(parts)


def validate(lessons: list[dict]) -> None:
    ids = [item["id"] for item in lessons]
    if len(ids) != len(set(ids)):
        raise SystemExit("Duplicate lesson ids")
    school_ids = {school["id"] for school in SCHOOLS}
    for item in lessons:
        if item["school"] not in school_ids:
            raise SystemExit(f"Unknown school on {item['id']}")
        if not item["title"] or not item["summary"] or not item["blocks"]:
            raise SystemExit(f"Empty lesson {item['id']}")
        blob = " ".join(
            str(value) for block in item["blocks"] for value in block.values()
        ).lower()
        for phrase in BANNED:
            if phrase in blob or phrase in item["title"].lower():
                raise SystemExit(f"Banned phrase {phrase!r} in {item['id']}")
        for block in item["blocks"]:
            if block["t"] == "diagram" and block["id"] not in FIGURES:
                raise SystemExit(f"Missing figure {block['id']} in {item['id']}")
    known = set(ids)
    for path in PATHS:
        for lid in path["lessons"]:
            if lid not in known:
                raise SystemExit(f"Path {path['id']} missing {lid}")
    for school in SCHOOLS:
        if school["kind"] == "track":
            count = sum(1 for item in lessons if item["school"] == school["id"])
            if count < 5:
                raise SystemExit(f"Track {school['id']} is too thin ({count})")


def lesson_search(item: dict) -> str:
    chunks = [item["id"], item["title"], item["summary"]]
    for block in item["blocks"]:
        for value in block.values():
            if isinstance(value, str):
                chunks.append(value)
            elif isinstance(value, list):
                chunks.extend(str(part) for part in value)
    return re.sub(r"\s+", " ", " ".join(chunks)).lower()


def build_lessons(lessons: list[dict]) -> tuple[str, dict[str, list[dict]]]:
    by_school: dict[str, list[dict]] = {school["id"]: [] for school in SCHOOLS}
    parts: list[str] = []
    for item in lessons:
        by_school[item["school"]].append(item)
        index = len(by_school[item["school"]])
        total = None  # filled after; placeholder replaced below
        parts.append((item, index))
    rendered: list[str] = []
    for item, index in parts:
        total = len(by_school[item["school"]])
        school = next(school for school in SCHOOLS if school["id"] == item["school"])
        rendered.append(
            f"<article class=\"lesson\" id=\"{item['id']}\" data-panel=\"lesson\" "
            f"data-school=\"{item['school']}\" data-title=\"{html.escape(item['title'])}\" "
            f"data-search=\"{html.escape(lesson_search(item))}\" style=\"--accent:{accent(item['school'])}\">"
            f"{lesson_head(item, index, total, school)}"
            f"<div class=\"prose\">{render_blocks(item)}</div>"
            f"{lesson_tail(item)}"
            f"</article>"
        )
    return "".join(rendered), by_school


def nav_html(by_school: dict[str, list[dict]]) -> str:
    blocks: list[str] = []
    current_kind = None
    for school in SCHOOLS:
        if school["kind"] != current_kind:
            current_kind = school["kind"]
            label = "Tracks" if current_kind == "track" else "Reference"
            blocks.append(f"<p class=\"nav-label\">{label}</p>")
        items = by_school[school["id"]]
        links = []
        for index, item in enumerate(items, start=1):
            links.append(
                f"<a class=\"ll\" href=\"#{item['id']}\" data-id=\"{item['id']}\" "
                f"data-search=\"{html.escape(lesson_search(item))}\">"
                f"<span class=\"ln\">{index:02d}</span>"
                f"<span class=\"nav-ico\">{nav_icon(item)}</span>"
                f"<span>{html.escape(item['title'])}</span></a>"
            )
        blocks.append(
            f"<div class=\"school-block\" data-school=\"{school['id']}\">"
            f"<div class=\"school-row\">"
            f"<a class=\"school-jump\" href=\"#school-{school['id']}\">"
            f"<span class=\"idx\">{html.escape(school['id'])}</span>"
            f"<span class=\"sname\">{html.escape(school['name'])}</span>"
            f"<span class=\"scount\">{len(items)}</span></a>"
            f"<button type=\"button\" class=\"chev\" aria-expanded=\"false\" "
            f"aria-label=\"Show lessons in {html.escape(school['name'])}\">"
            f"<svg class=\"icon\" viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M6 9l6 6 6-6\"/></svg>"
            f"</button></div>"
            f"<div class=\"lesson-links\">{''.join(links)}</div></div>"
        )
    return "".join(blocks)


def school_pages(by_school: dict[str, list[dict]]) -> str:
    pages: list[str] = []
    for school in SCHOOLS:
        items = by_school[school["id"]]
        kind = "Track" if school["kind"] == "track" else "Reference"
        pages.append(
            f"<article class=\"school-page\" id=\"school-{school['id']}\" data-panel=\"school\" "
            f"data-school=\"{school['id']}\" style=\"--accent:{accent(school['id'])}\">"
            f"<p class=\"kicker\">{kind} {html.escape(school['id'])}</p>"
            f"<h1>{html.escape(school['name'])}</h1>"
            f"<p class=\"lede\">{html.escape(school['outcome'])}</p>"
            f"<p><a class=\"btn primary\" href=\"#{items[0]['id']}\">"
            f"{'Start this track' if school['kind'] == 'track' else 'Open the first entry'}</a></p>"
            f"{hub_html(school, items)}"
            f"{lesson_cards(items)}</article>"
        )
    return "".join(pages)


def home_html(lessons: list[dict], by_school: dict[str, list[dict]]) -> str:
    track_count = sum(1 for school in SCHOOLS if school["kind"] == "track")
    minutes = sum(item["minutes"] for item in lessons)
    cards = []
    for offset, school in enumerate(school for school in SCHOOLS if school["kind"] == "track"):
        stripe = (offset % 6) + 1
        cards.append(
            f"<a class=\"track-card\" data-accent=\"{stripe}\" href=\"#school-{school['id']}\" "
            f"style=\"--accent:{accent(school['id'])};border-top-color:{accent(school['id'])}\">"
            f"<span class=\"idx\">{html.escape(school['id'])} <span class=\"emoji\">{emoji_for(school['id'])}</span></span>"
            f"<strong>{html.escape(school['name'])}</strong>"
            f"<em>{html.escape(school['outcome'])}</em>"
            f"<span class=\"meta\">{len(by_school[school['id']])} lessons</span>"
            f"<span class=\"track-bar\"><b data-school-bar=\"{html.escape(school['id'])}\"></b></span></a>"
        )
    routes = []
    by_id = {item["id"]: item for item in lessons}
    for path in PATHS:
        steps = "".join(
            f"<li><a href=\"#{lid}\">{html.escape(by_id[lid]['title'])}</a></li>"
            for lid in path["lessons"]
        )
        routes.append(
            f"<article class=\"route\"><h3>{html.escape(path['name'])}</h3>"
            f"<p>{html.escape(path['blurb'])}</p><ol>{steps}</ol></article>"
        )
    return f"""
<section id="home" class="active" data-panel="home">
  <div class="hero">
    <div>
    <p class="eyebrow">Offline course · October 2026 · MIT</p>
    <h1>Learn to build AI systems you can test.</h1>
    <p class="lede">A free course in models, prompting, local and hosted APIs, retrieval, agents, MCP, coding agents, evals, fine-tuning, safety, and product judgment. One HTML file. No account. No key required to read it.</p>
    <div class="hero-actions">
      <a class="btn primary" id="continueLink" href="#00-01">Start the course</a>
      <a class="btn" href="#map">View the track map</a>
    </div>
    <dl class="stats">
      <div><dt>Tracks</dt><dd>{track_count}</dd></div>
      <div><dt>Lessons</dt><dd id="statLessons">{len(lessons)}</dd></div>
      <div><dt>Reading time</dt><dd>{round(minutes / 60)} hours</dd></div>
      <div><dt>Network calls</dt><dd>0</dd></div>
    </dl>
    </div>
    {home_poster()}
  </div>
  {home_extra()}
  <section class="block">
    <div class="block-head"><h2>Continue</h2><p id="homeProg">Nothing marked complete yet.</p></div>
    <a class="continue-card" id="continueCard" href="#00-01">
      <span class="eyebrow">Next lesson</span>
      <strong id="continueTitle">How to use this campus</strong>
      <em id="continueMeta">Start here · 8 min</em>
    </a>
    <div class="bar" aria-hidden="true"><i id="homeBar"></i></div>
  </section>
  <section class="block">
    <div class="block-head"><h2>Choose a route</h2><p>Short paths through the same lessons. The track map is the full course.</p></div>
    <div class="routes">{''.join(routes)}</div>
  </section>
  <section class="block">
    <div class="block-head"><h2>Tracks</h2><p>Take them in order the first time. Each one assumes the ideas before it.</p></div>
    <div class="track-grid">{''.join(cards)}</div>
  </section>
</section>
"""


def map_html(by_school: dict[str, list[dict]]) -> str:
    steps = []
    for school in SCHOOLS:
        if school["kind"] != "track":
            continue
        links = "".join(
            f"<li><a href=\"#{item['id']}\">{html.escape(item['title'])}</a></li>"
            for item in by_school[school["id"]]
        )
        steps.append(
            f"<li id=\"map-{school['id']}\"><span class=\"dot\">{html.escape(school['id'])}</span>"
            f"<div><h2><a href=\"#school-{school['id']}\">{html.escape(school['name'])}</a></h2>"
            f"<p>{html.escape(school['outcome'])}</p><ol>{links}</ol></div></li>"
        )
    refs = []
    for school in SCHOOLS:
        if school["kind"] != "reference":
            continue
        refs.append(
            f"<a class=\"track-card\" href=\"#school-{school['id']}\" style=\"border-top-color:{accent(school['id'])}\">"
            f"<span class=\"idx\">{html.escape(school['id'])} <span class=\"emoji\">{emoji_for(school['id'])}</span></span>"
            f"<strong>{html.escape(school['name'])}</strong>"
            f"<em>{html.escape(school['outcome'])}</em></a>"
        )
    return f"""
<section id="map" data-panel="map">
  <p class="eyebrow">Learning path</p>
  <h1>Track map</h1>
  <p class="lede">Start with how a model behaves. Add tools only after you can test a single call. Train only after the score says the cheaper fixes failed.</p>
  {map_poster()}
  <ol class="path">{''.join(steps)}</ol>
  <h2 class="ref-head">Reference</h2>
  <div class="track-grid">{''.join(refs)}</div>
</section>
"""


def write_hero(lesson_count: int, track_count: int) -> None:
    HERO.parent.mkdir(parents=True, exist_ok=True)
    HERO.write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 560" role="img" aria-label="AI Lab Free University">
  <rect width="1200" height="560" fill="#0B1220"/>
  <circle cx="980" cy="80" r="220" fill="#6366F1" opacity="0.18"/>
  <circle cx="140" cy="480" r="180" fill="#22D3EE" opacity="0.08"/>
  <rect x="64" y="56" width="52" height="52" rx="14" fill="#6366F1"/>
  <circle cx="90" cy="82" r="4" fill="#fff"/>
  <circle cx="74" cy="82" r="3" fill="#fff"/>
  <circle cx="106" cy="82" r="3" fill="#fff"/>
  <circle cx="90" cy="66" r="3" fill="#fff"/>
  <circle cx="90" cy="98" r="3" fill="#fff"/>
  <path d="M77 82h8M95 82h8M90 69v8M90 87v8" stroke="#fff" stroke-width="1.6" fill="none" stroke-linecap="round"/>
  <text x="132" y="90" fill="#E7ECF5" font-family="system-ui,Segoe UI,sans-serif" font-size="28" font-weight="650">AI Lab Free University</text>
  <text x="64" y="190" fill="#F8FAFC" font-family="system-ui,Segoe UI,sans-serif" font-size="64" font-weight="650">Learn to build AI systems</text>
  <text x="64" y="262" fill="#F8FAFC" font-family="system-ui,Segoe UI,sans-serif" font-size="64" font-weight="650">you can test.</text>
  <text x="64" y="324" fill="#A8B3C7" font-family="system-ui,Segoe UI,sans-serif" font-size="24">Models, retrieval, agents, MCP, coding agents, evals, and product judgment.</text>
  <text x="64" y="362" fill="#A8B3C7" font-family="system-ui,Segoe UI,sans-serif" font-size="24">One offline HTML file. Free to use, share, and remix.</text>
  <g font-family="system-ui,Segoe UI,sans-serif" font-size="16" font-weight="650">
    <rect x="64" y="420" width="150" height="40" rx="20" fill="#6366F1"/>
    <text x="139" y="446" text-anchor="middle" fill="#fff">{track_count} tracks</text>
    <rect x="230" y="420" width="160" height="40" rx="20" fill="#162033"/>
    <text x="310" y="446" text-anchor="middle" fill="#E7ECF5">{lesson_count} lessons</text>
    <rect x="406" y="420" width="150" height="40" rx="20" fill="#162033"/>
    <text x="481" y="446" text-anchor="middle" fill="#34D399">0 CDN</text>
    <rect x="572" y="420" width="120" height="40" rx="20" fill="#162033"/>
    <text x="632" y="446" text-anchor="middle" fill="#E7ECF5">MIT</text>
  </g>
</svg>
""",
        encoding="utf-8",
    )


CSS = r"""
:root {
  --bg: #0B1220;
  --side: #090f1c;
  --card: #141c2f;
  --card-2: #1b2438;
  --ink: #E8EDF7;
  --muted: #9AA8C3;
  --line: #2A3650;
  --primary: #6366F1;
  --primary-2: #818CF8;
  --link: #C7D2FE;
  --on-primary: #ffffff;
  --cyan: #22D3EE;
  --green: #34D399;
  --amber: #FBBF24;
  --rose: #FB7185;
  --violet: #A78BFA;
  --figure: #10182a;
  --code: #0c1220;
  --shadow: 0 16px 40px rgba(0,0,0,.28);
  --font: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --mono: ui-monospace, "SFMono-Regular", "Cascadia Code", Menlo, Consolas, monospace;
  --side-w: 300px;
  --radius: 16px;
  color-scheme: dark;
}
html[data-theme="light"] {
  --bg: #F4F6FB;
  --side: #FFFFFF;
  --card: #FFFFFF;
  --card-2: #F8FAFC;
  --ink: #0B1220;
  --muted: #52627A;
  --line: #E2E8F4;
  --primary: #6366F1;
  --primary-2: #4F46E5;
  --link: #3730A3;
  --figure: #F8FAFC;
  --code: #0F172A;
  --shadow: 0 10px 30px rgba(11,18,32,.06);
  color-scheme: light;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: var(--font);
  background: var(--bg);
  color: var(--ink);
  font-size: 17px;
  line-height: 1.6;
  min-height: 100vh;
}
::selection { background: #6366F1; color: #fff; }
:focus-visible { outline: 2px solid var(--primary-2); outline-offset: 2px; }
a { color: var(--link); text-decoration-thickness: 1px; text-underline-offset: 3px; }
a:hover { color: var(--primary-2); }
.skip {
  position: absolute; left: 12px; top: -40px; background: var(--primary); color: #fff;
  padding: 8px 12px; border-radius: 8px; z-index: 80;
}
.skip:focus { top: 12px; }
.app { display: grid; grid-template-columns: var(--side-w) 1fr; min-height: 100vh; }
#sidebar {
  position: sticky; top: 0; height: 100vh; overflow: auto;
  background: var(--side); border-right: 1px solid var(--line);
  padding: 18px 14px 28px;
}
.brand { display: flex; gap: 10px; align-items: center; text-decoration: none; color: var(--ink); padding: 4px 6px 12px; }
.brand strong { display: block; font-size: 15px; letter-spacing: -0.02em; }
.brand span { display: block; color: var(--muted); font-size: 12px; font-weight: 600; }
.mark { width: 36px; height: 36px; flex: none; }
.side-progress { display: flex; gap: 10px; align-items: center; padding: 8px 8px 14px; }
.ring { width: 46px; height: 46px; flex: none; }
.ring circle { fill: none; stroke-width: 3.5; }
.ring .track { stroke: var(--line); }
.ring .value { stroke: var(--primary); stroke-linecap: round; transform: rotate(-90deg); transform-origin: 18px 18px; }
.side-progress p { margin: 0; font-size: 13px; color: var(--muted); }
.side-progress strong { color: var(--ink); font-size: 14px; }
.search { position: relative; margin: 0 6px 12px; }
.search input {
  width: 100%; border: 1px solid var(--line); background: var(--card);
  color: var(--ink); border-radius: 10px; padding: 9px 10px 9px 34px;
  font: inherit; font-size: 14px;
}
.search svg { position: absolute; left: 10px; top: 10px; width: 16px; height: 16px; stroke: var(--muted); fill: none; stroke-width: 2; }
.nav-label {
  margin: 16px 8px 6px; font-size: 11px; font-weight: 700; letter-spacing: .08em;
  text-transform: uppercase; color: var(--muted);
}
.school-row { display: flex; align-items: stretch; gap: 2px; }
.school-jump {
  flex: 1; display: grid; grid-template-columns: 36px 1fr auto; gap: 6px; align-items: center;
  text-decoration: none; color: var(--ink); padding: 7px 6px; border-radius: 10px; font-size: 14px; font-weight: 650;
}
.school-jump:hover, .school-block.open > .school-row .school-jump { background: color-mix(in srgb, var(--primary) 12%, transparent); }
.idx { color: var(--primary-2); font-variant-numeric: tabular-nums; font-size: 12px; font-weight: 750; }
.scount { color: var(--muted); font-size: 12px; font-weight: 650; }
.chev {
  width: 32px; border: 0; background: transparent; color: var(--muted); border-radius: 8px; cursor: pointer;
}
.chev svg { width: 16px; height: 16px; stroke: currentColor; fill: none; stroke-width: 2; stroke-linecap: round; }
.school-block.open .chev svg { transform: rotate(180deg); }
.lesson-links { display: none; padding: 0 0 8px 8px; }
.school-block.open .lesson-links { display: block; }
a.ll {
  display: grid; grid-template-columns: 28px 1fr; gap: 6px; align-items: start;
  text-decoration: none; color: var(--muted); font-size: 13px; line-height: 1.35;
  padding: 6px 8px; border-radius: 8px; font-weight: 600;
}
a.ll:hover { color: var(--ink); background: color-mix(in srgb, var(--ink) 5%, transparent); }
a.ll.on { color: var(--ink); background: color-mix(in srgb, var(--primary) 16%, transparent); }
a.ll.done .ln { color: var(--green); }
.ln { font-variant-numeric: tabular-nums; color: var(--muted); font-size: 11px; padding-top: 2px; }
.maincol {
  min-width: 0;
  background:
    radial-gradient(900px 420px at 8% -10%, color-mix(in srgb, var(--primary) 20%, transparent), transparent 60%),
    radial-gradient(640px 320px at 100% 0%, color-mix(in srgb, var(--cyan) 10%, transparent), transparent 50%),
    var(--bg);
}
.top {
  position: sticky; top: 0; z-index: 20; display: flex; align-items: center; gap: 10px;
  padding: 12px 28px; border-bottom: 1px solid transparent;
  background: color-mix(in srgb, var(--bg) 84%, transparent); backdrop-filter: blur(16px);
}
.icon-btn, .btn {
  border: 1px solid var(--line); background: var(--card); color: var(--ink);
  border-radius: 10px; font: inherit; font-size: 14px; font-weight: 650;
  padding: 8px 12px; cursor: pointer; text-decoration: none; display: inline-flex;
  align-items: center; justify-content: center; gap: 8px;
}
.icon-btn { width: 40px; height: 40px; padding: 0; }
.icon-btn svg, .btn svg { width: 18px; height: 18px; stroke: currentColor; fill: none; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
.btn.primary { background: var(--primary); border-color: transparent; color: var(--on-primary); }
.btn.primary:hover { background: #4F46E5; color: #fff; }
.btn:hover, .icon-btn:hover { border-color: var(--primary); }
.only-mobile { display: none; }
#crumb { font-size: 14px; color: var(--muted); font-weight: 650; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.spacer { flex: 1; }
#themeBtn .sun { display: none; }
html[data-theme="light"] #themeBtn .moon { display: none; }
html[data-theme="light"] #themeBtn .sun { display: block; }
#content { padding: 28px 32px 120px; max-width: 1100px; }
html.js [data-panel] { display: none; }
html.js [data-panel].active { display: block; }
.eyebrow, .kicker {
  display: flex; flex-wrap: wrap; gap: 8px 14px; align-items: center;
  color: var(--primary-2); font-size: 12px; font-weight: 750; letter-spacing: .08em;
  text-transform: uppercase; margin: 0 0 10px;
}
.kicker a { color: inherit; text-decoration: none; }
.kicker span { color: var(--muted); letter-spacing: .04em; }
h1 { font-size: clamp(2rem, 4vw, 3.35rem); line-height: 1.08; letter-spacing: -0.035em; margin: 0 0 12px; font-weight: 650; }
.lede { font-size: 1.125rem; color: var(--muted); max-width: 62ch; margin: 0 0 18px; }
.hero-actions, .stats { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
.stats { margin-top: 22px; gap: 18px 28px; padding: 0; }
.stats div { min-width: 90px; }
.stats dt { color: var(--muted); font-size: 12px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; }
.stats dd { margin: 0; font-size: 1.35rem; font-weight: 700; letter-spacing: -0.03em; }
.block { margin-top: 36px; }
.block-head { display: flex; justify-content: space-between; gap: 16px; align-items: baseline; margin-bottom: 12px; }
.block-head h2, .ref-head { font-size: 1.25rem; letter-spacing: -0.02em; margin: 0; }
.block-head p { margin: 0; color: var(--muted); font-size: 14px; }
.continue-card {
  display: block; text-decoration: none; color: inherit; background: var(--card);
  border: 1px solid var(--line); border-radius: var(--radius); padding: 18px 18px 16px;
  box-shadow: var(--shadow);
}
.continue-card strong { display: block; font-size: 1.25rem; letter-spacing: -0.02em; margin: 4px 0; }
.continue-card em { color: var(--muted); font-style: normal; font-size: 14px; }
.bar { height: 6px; background: var(--line); border-radius: 99px; margin-top: 12px; overflow: hidden; }
.bar i { display: block; height: 100%; width: 0; background: linear-gradient(90deg, var(--primary), var(--cyan)); }
.track-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 12px; }
.track-card {
  display: flex; flex-direction: column; gap: 6px; text-decoration: none; color: inherit;
  background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 14px 14px 12px;
  min-height: 150px; border-top: 3px solid var(--primary);
}
.track-card[data-accent="2"] { border-top-color: var(--cyan); }
.track-card[data-accent="3"] { border-top-color: var(--green); }
.track-card[data-accent="4"] { border-top-color: var(--amber); }
.track-card[data-accent="5"] { border-top-color: var(--rose); }
.track-card[data-accent="6"] { border-top-color: var(--violet); }
.track-card strong { letter-spacing: -0.02em; }
.track-card em { color: var(--muted); font-style: normal; font-size: 14px; line-height: 1.45; flex: 1; }
.track-card .meta { color: var(--primary-2); font-size: 12px; font-weight: 750; }
.routes { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px; }
.route { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 14px 16px; }
.route h3 { margin: 0 0 6px; font-size: 1rem; }
.route p { margin: 0 0 8px; color: var(--muted); font-size: 14px; }
.route ol, .path ol { margin: 0; padding-left: 1.1rem; }
.route li { margin: 4px 0; font-size: 14px; }
.lesson, .school-page { max-width: 760px; }
.prose h3 { margin: 1.4rem 0 .4rem; font-size: 1.15rem; letter-spacing: -0.02em; }
.prose p { margin: 0 0 .9rem; }
.prose ul, .prose ol { margin: 0 0 1rem; padding-left: 1.2rem; }
.prose li { margin: .28rem 0; }
.prose code, .lesson-index code { font-family: var(--mono); font-size: .88em; background: color-mix(in srgb, var(--primary) 12%, transparent); padding: .1em .35em; border-radius: 6px; }
pre {
  background: var(--code); color: #E7ECF7; border-radius: 12px; padding: 14px 16px;
  overflow: auto; border: 1px solid var(--line); margin: 0 0 1rem;
}
pre code { background: none; padding: 0; color: inherit; font-size: 13px; line-height: 1.55; }
.table-wrap { overflow: auto; border: 1px solid var(--line); border-radius: 12px; margin: 0 0 1rem; }
table { width: 100%; border-collapse: collapse; font-size: 14.5px; }
th, td { text-align: left; vertical-align: top; padding: 10px 12px; border-bottom: 1px solid var(--line); }
th { font-size: 12px; letter-spacing: .05em; text-transform: uppercase; color: var(--muted); background: var(--card-2); }
tr:last-child td { border-bottom: 0; }
.callout { border: 1px solid var(--line); border-left-width: 4px; border-radius: 12px; padding: 12px 14px; margin: 0 0 1rem; background: var(--card); }
.callout h3 { margin: 0 0 6px; font-size: 13px; letter-spacing: .06em; text-transform: uppercase; }
.callout p { margin: 0; }
.callout.practice { border-left-color: var(--green); }
.callout.check { border-left-color: var(--primary); }
.callout.note { border-left-color: var(--cyan); }
.callout.warn { border-left-color: var(--amber); }
.callout details { margin-top: 8px; }
.callout summary { cursor: pointer; font-weight: 700; }
figure.diagram { margin: 4px 0 1.1rem; padding: 12px; background: var(--figure); border: 1px solid var(--line); border-radius: 14px; }
figure.diagram svg { width: 100%; height: auto; display: block; }
figcaption { color: var(--muted); font-size: 13px; margin-top: 8px; }
.fig .node { fill: var(--card); stroke: var(--line); stroke-width: 1.5; }
.fig .node-hot { fill: color-mix(in srgb, var(--primary) 18%, var(--card)); stroke: var(--primary); }
.fig .node-ok { fill: color-mix(in srgb, var(--green) 16%, var(--card)); stroke: var(--green); }
.fig .frame { fill: transparent; stroke: var(--line); stroke-width: 1.5; }
.fig .gate { fill: color-mix(in srgb, var(--amber) 18%, var(--card)); stroke: var(--amber); }
.fig .edge { stroke: var(--primary-2); stroke-width: 1.7; fill: none; }
.fig .arrowhead { fill: var(--primary-2); }
.fig .nt { fill: var(--ink); font-size: 15px; font-weight: 700; font-family: var(--font); }
.fig .ns, .fig .label { fill: var(--muted); font-size: 12px; font-family: var(--font); }
.fig .kicker { fill: var(--primary-2); font-size: 12px; font-weight: 750; letter-spacing: .06em; font-family: var(--font); }
.fig .gs { fill: var(--ink); font-size: 12px; font-weight: 750; font-family: var(--font); }
.fig .track { fill: var(--line); }
.fig .seg-a { fill: #6366F1; }
.fig .seg-b { fill: #22D3EE; }
.fig .seg-c { fill: #A78BFA; }
.fig .seg-d { fill: #34D399; }
.fig .onseg { fill: #0B1220; font-size: 12px; font-weight: 750; font-family: var(--font); }
.path { list-style: none; margin: 10px 0 0; padding: 0 0 0 8px; border-left: 2px solid var(--line); }
.path > li { position: relative; padding: 0 0 28px 28px; }
.path .dot {
  position: absolute; left: -15px; top: 0; width: 28px; height: 28px; border-radius: 50%;
  background: var(--primary); color: #fff; font-size: 10px; font-weight: 750;
  display: grid; place-items: center;
}
.path h2 { margin: 0 0 4px; font-size: 1.35rem; letter-spacing: -0.02em; }
.path h2 a { color: var(--ink); text-decoration: none; }
.path > li > div > p { margin: 0 0 8px; color: var(--muted); }
.lesson-index { list-style: none; padding: 0; margin: 18px 0 0; }
.lesson-index a, .path ol a { text-decoration: none; }
.lesson-index li a {
  display: grid; grid-template-columns: 36px 1fr; gap: 10px; padding: 12px 0;
  border-bottom: 1px solid var(--line); color: inherit;
}
.lesson-index strong { display: block; color: var(--ink); }
.lesson-index em { display: block; color: var(--muted); font-style: normal; font-size: 14px; }
.ref-head { margin: 28px 0 12px; }
.foot-note { margin-top: 48px; color: var(--muted); font-size: 14px; max-width: 68ch; }
.pager {
  position: fixed; z-index: 25; left: var(--side-w); right: 0; bottom: 0;
  display: grid; grid-template-columns: 1fr auto 1fr; gap: 10px; align-items: center;
  padding: 10px 16px calc(10px + env(safe-area-inset-bottom));
  background: color-mix(in srgb, var(--bg) 92%, transparent);
  border-top: 1px solid var(--line); backdrop-filter: blur(14px);
}
html.js body:not([data-view="lesson"]) .pager { display: none; }
.pager a { color: var(--ink); text-decoration: none; font-size: 14px; font-weight: 650; min-width: 0; }
.pager a small { display: block; color: var(--muted); font-weight: 600; font-size: 11px; letter-spacing: .06em; text-transform: uppercase; }
.pager a span { display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
#pagerNext { text-align: right; }
#markBtn.done { border-color: var(--green); color: var(--green); }
#scrim { display: none; }
.missing { max-width: 640px; }
@media (max-width: 960px) {
  .app { grid-template-columns: 1fr; }
  .only-mobile { display: inline-flex; }
  #sidebar {
    position: fixed; z-index: 40; transform: translateX(-105%); transition: transform .18s ease;
    width: min(340px, 90vw); box-shadow: var(--shadow);
  }
  body.nav-open #sidebar { transform: none; }
  body.nav-open #scrim { display: block; position: fixed; inset: 0; background: rgba(5,8,16,.55); z-index: 35; }
  .top { padding: 10px 12px; }
  #content { padding: 20px 16px 128px; }
  .pager { left: 0; grid-template-columns: 1fr 1fr; }
  #markBtn { grid-column: 1 / -1; order: -1; }
  .block-head { flex-direction: column; align-items: flex-start; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  * { transition: none !important; }
}
@media print {
  #sidebar, .top, .pager, #scrim, .skip { display: none !important; }
  .app { display: block; }
  html.js [data-panel] { display: block !important; }
  .lesson, .school-page { break-inside: avoid; max-width: none; }
  body { background: #fff; color: #000; }
}
"""

JS = r"""
(function () {
  const STUDY_KEY = "ailab-v3-studied";
  const THEME_KEY = "ailab-v3-theme";
  const LAST_KEY = "ailab-v3-last";
  const lessons = [...document.querySelectorAll("article.lesson")];
  const byId = Object.fromEntries(lessons.map((el) => [el.id, el]));
  const order = lessons.map((el) => el.id);
  let studied = new Set();
  try { JSON.parse(localStorage.getItem(STUDY_KEY) || "[]").forEach((id) => studied.add(id)); } catch (err) { studied = new Set(); }

  const menuBtn = document.getElementById("menuBtn");
  const scrim = document.getElementById("scrim");
  const search = document.getElementById("q");
  const themeBtn = document.getElementById("themeBtn");
  const markBtn = document.getElementById("markBtn");
  const crumb = document.getElementById("crumb");
  const ring = document.getElementById("ringValue");
  const studiedLabel = document.getElementById("studiedLabel");
  const homeProg = document.getElementById("homeProg");
  const homeBar = document.getElementById("homeBar");
  const continueLink = document.getElementById("continueLink");
  const continueCard = document.getElementById("continueCard");
  const continueTitle = document.getElementById("continueTitle");
  const continueMeta = document.getElementById("continueMeta");
  const pager = document.getElementById("pager");
  const pagerPrev = document.getElementById("pagerPrev");
  const pagerNext = document.getElementById("pagerNext");

  function closeNav() {
    document.body.classList.remove("nav-open");
    menuBtn.setAttribute("aria-expanded", "false");
  }
  menuBtn.addEventListener("click", () => {
    const open = document.body.classList.toggle("nav-open");
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
  });
  scrim.addEventListener("click", closeNav);

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(THEME_KEY, theme);
    const dark = theme === "dark";
    themeBtn.setAttribute("aria-pressed", dark ? "true" : "false");
    themeBtn.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
  }
  themeBtn.addEventListener("click", () => {
    const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
    applyTheme(next);
  });
  applyTheme(document.documentElement.getAttribute("data-theme") || "dark");

  function saveStudy() { localStorage.setItem(STUDY_KEY, JSON.stringify([...studied])); }
  function nextUnstudied() {
    const last = localStorage.getItem(LAST_KEY);
    if (last && byId[last] && !studied.has(last)) return last;
    return order.find((id) => !studied.has(id)) || order[order.length - 1];
  }
  function refreshProgress() {
    const done = order.filter((id) => studied.has(id)).length;
    const pct = Math.round((done / order.length) * 100);
    ring.setAttribute("stroke-dasharray", pct + " 100");
    studiedLabel.textContent = done + " of " + order.length + " complete";
    homeProg.textContent = done + " of " + order.length + " lessons marked complete";
    homeBar.style.width = pct + "%";
    document.querySelectorAll("a.ll").forEach((link) => {
      link.classList.toggle("done", studied.has(link.dataset.id));
    });
    const nid = nextUnstudied();
    const el = byId[nid];
    const schoolName = el.querySelector(".kicker a").textContent;
    const minutes = el.querySelector(".kicker span:last-child").textContent;
    continueTitle.textContent = el.dataset.title;
    continueMeta.textContent = schoolName + " · " + minutes;
    continueLink.setAttribute("href", "#" + nid);
    continueCard.setAttribute("href", "#" + nid);
    continueLink.textContent = done === 0 ? "Start the course" : (done === order.length ? "Review the course" : "Continue");
    if (document.body.dataset.view === "lesson") updateMark(location.hash.slice(1));
    document.dispatchEvent(new CustomEvent("campus-progress"));
  }
  function updateMark(id) {
    const on = studied.has(id);
    markBtn.classList.toggle("done", on);
    markBtn.textContent = on ? "Completed" : "Mark complete";
    markBtn.dataset.id = id;
  }
  markBtn.addEventListener("click", () => {
    const id = markBtn.dataset.id;
    if (!id) return;
    if (studied.has(id)) studied.delete(id); else studied.add(id);
    saveStudy();
    refreshProgress();
  });

  function setOpenSchool(schoolId) {
    document.querySelectorAll(".school-block").forEach((block) => {
      const open = block.dataset.school === schoolId;
      block.classList.toggle("open", open);
      const chev = block.querySelector(".chev");
      chev.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }
  document.querySelectorAll(".chev").forEach((button) => {
    button.addEventListener("click", () => {
      const block = button.closest(".school-block");
      const open = !block.classList.contains("open");
      block.classList.toggle("open", open);
      button.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });

  function pagerLink(anchor, id, label) {
    if (!id || !byId[id]) {
      anchor.hidden = true;
      return;
    }
    anchor.hidden = false;
    anchor.href = "#" + id;
    anchor.innerHTML = "<small>" + label + "</small><span>" + byId[id].dataset.title + "</span>";
  }
  function showLessonChrome(id) {
    const index = order.indexOf(id);
    pagerLink(pagerPrev, order[index - 1], "Previous");
    pagerLink(pagerNext, order[index + 1], "Next");
    updateMark(id);
    localStorage.setItem(LAST_KEY, id);
  }

  function parseHash() {
    const raw = (location.hash || "#home").replace(/^#/, "");
    if (!raw || raw === "home") return { view: "home" };
    if (raw === "map") return { view: "map" };
    if (raw === "studio") return { view: "studio" };
    if (raw.startsWith("school-")) return { view: "school", id: raw };
    if (byId[raw]) return { view: "lesson", id: raw };
    return { view: "missing" };
  }
  function show(route) {
    document.body.dataset.view = route.view;
    document.querySelectorAll("[data-panel]").forEach((el) => el.classList.remove("active"));
    document.querySelectorAll("a.ll").forEach((link) => link.classList.remove("on"));
    let crumbText = "Home";
    let schoolId = null;
    if (route.view === "home") {
      document.getElementById("home").classList.add("active");
    } else if (route.view === "map") {
      document.getElementById("map").classList.add("active");
      crumbText = "Track map";
    } else if (route.view === "studio") {
      document.getElementById("studio").classList.add("active");
      crumbText = "Studio";
      const studioLink = document.querySelector("a.studio-link");
      if (studioLink) studioLink.classList.add("on");
    } else if (route.view === "school") {
      const page = document.getElementById(route.id);
      if (!page) { show({ view: "missing" }); return; }
      page.classList.add("active");
      crumbText = page.querySelector("h1").textContent;
      schoolId = page.dataset.school;
    } else if (route.view === "lesson") {
      const page = byId[route.id];
      page.classList.add("active");
      crumbText = page.dataset.title;
      schoolId = page.dataset.school;
      const link = document.querySelector('a.ll[data-id="' + route.id + '"]');
      if (link) link.classList.add("on");
      showLessonChrome(route.id);
    } else {
      document.getElementById("view-missing").classList.add("active");
      crumbText = "Not found";
    }
    crumb.textContent = crumbText;
    document.title = crumbText + " · AI Lab Free University";
    if (schoolId) setOpenSchool(schoolId);
    window.scrollTo(0, 0);
    closeNav();
    document.dispatchEvent(new CustomEvent("campus-show", { detail: route }));
  }
  window.addEventListener("hashchange", () => show(parseHash()));

  function applySearch() {
    const term = search.value.trim().toLowerCase();
    document.querySelectorAll("a.ll").forEach((link) => {
      const hay = link.dataset.search || "";
      link.hidden = Boolean(term) && !hay.includes(term);
    });
    document.querySelectorAll(".school-block").forEach((block) => {
      const visible = [...block.querySelectorAll("a.ll")].some((link) => !link.hidden);
      block.hidden = Boolean(term) && !visible;
      if (term && visible) {
        block.classList.add("open");
        block.querySelector(".chev").setAttribute("aria-expanded", "true");
      }
    });
  }
  search.addEventListener("input", applySearch);
  search.addEventListener("keydown", (event) => {
    if (event.key !== "Enter") return;
    const first = document.querySelector("a.ll:not([hidden])");
    if (first) { event.preventDefault(); location.hash = first.getAttribute("href"); }
  });
  document.addEventListener("keydown", (event) => {
    const tag = (event.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea") return;
    if (event.key === "/") { event.preventDefault(); search.focus(); }
    if (document.body.dataset.view !== "lesson") return;
    if (event.key === "[" && !pagerPrev.hidden) pagerPrev.click();
    if (event.key === "]" && !pagerNext.hidden) pagerNext.click();
  });

  refreshProgress();
  show(parseHash());
})();
"""



def assemble(lessons_html: str, nav: str, home: str, tracks: str, schools: str) -> str:
    return (
        """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<meta name="description" content="AI Lab Free University. A free offline course in models, retrieval, agents, MCP, coding agents, evals, and product judgment."/>
<meta name="color-scheme" content="dark light"/>
<title>AI Lab Free University</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%236366F1'/%3E%3Ccircle cx='16' cy='16' r='3' fill='white'/%3E%3C/svg%3E"/>
<script>
try {
  var saved = localStorage.getItem("ailab-v3-theme");
  if (!saved && window.matchMedia("(prefers-color-scheme: light)").matches) saved = "light";
  if (saved) document.documentElement.setAttribute("data-theme", saved);
  var contrast = localStorage.getItem("ailab-v3-contrast");
  if (contrast === "high") document.documentElement.setAttribute("data-contrast", "high");
} catch (err) {}
document.documentElement.classList.add("js");
</script>
<style>
"""
        + CSS
        + "\n"
        + VISUAL_CSS
        + """
</style>
</head>
<body data-view="home">
<a class="skip" href="#content">Skip to content</a>
<div class="app">
<aside id="sidebar">
  <a class="brand" href="#home">
    <svg class="mark" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#6366F1"/><circle cx="16" cy="16" r="2.4" fill="#fff"/><circle cx="8" cy="16" r="1.7" fill="#fff"/><circle cx="24" cy="16" r="1.7" fill="#fff"/><circle cx="16" cy="8" r="1.7" fill="#fff"/><circle cx="16" cy="24" r="1.7" fill="#fff"/><path d="M9.6 16h4.2M18.2 16h4.2M16 9.6v4.2M16 18.2v4.2" stroke="#fff" stroke-width="1.4" fill="none" stroke-linecap="round"/></svg>
    <span><strong>AI Lab</strong><span>Free University</span></span>
  </a>
  <div class="side-progress">
    <svg class="ring" viewBox="0 0 36 36" aria-hidden="true"><circle class="track" cx="18" cy="18" r="15" pathLength="100"/><circle class="value" id="ringValue" cx="18" cy="18" r="15" pathLength="100" stroke-dasharray="0 100"/></svg>
    <p><strong id="studiedLabel">0 complete</strong><br/>Saved in this browser</p>
  </div>
  <label class="search">
    <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
    <input id="q" type="search" placeholder="Search lessons" aria-label="Search lessons"/>
  </label>
  <p id="searchMeta" class="search-meta"></p>
  <a class="school-jump" href="#home"><span class="idx">00</span><span class="sname">Home</span></a>
  <a class="school-jump" href="#map"><span class="idx">—</span><span class="sname">Track map</span></a>
"""
        + studio_nav()
        + """
  <nav aria-label="Course">
"""
        + nav
        + """
  </nav>
</aside>
<div id="scrim"></div>
<div class="maincol">
  <header class="top">
    <button type="button" class="icon-btn only-mobile" id="menuBtn" aria-expanded="false" aria-controls="sidebar" aria-label="Open menu">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
    <div id="crumb">Home</div>
    <div class="spacer"></div>
    <button type="button" class="icon-btn" id="contrastBtn" aria-pressed="false" aria-label="Turn on high contrast">HC</button>
    <button type="button" class="icon-btn" id="themeBtn" aria-pressed="true" aria-label="Switch to light theme">
      <svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 14.5A8.5 8.5 0 1 1 9.5 3 7 7 0 0 0 21 14.5z"/></svg>
      <svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
    </button>
  </header>
  <main id="content">
"""
        + home
        + tracks
        + schools
        + lessons_html
        + studio_page()
        + """
    <section id="view-missing" class="missing" data-panel="missing">
      <h1>That page is not in the course.</h1>
      <p class="lede">The link does not match a lesson or a track.</p>
      <p><a class="btn primary" href="#home">Back to home</a></p>
    </section>
    <p class="foot-note">AI Lab Free University. Educational material under the MIT license. No warranty. Model names change; pin the id you actually call. Do not upload secrets or private data.</p>
  </main>
  <nav class="pager" id="pager" aria-label="Lesson">
    <a id="pagerPrev" href="#home"><small>Previous</small><span>Home</span></a>
    <button type="button" id="markBtn">Mark complete</button>
    <a id="pagerNext" href="#00-01"><small>Next</small><span>Next lesson</span></a>
  </nav>
</div>
</div>
<script>
"""
        + JS
        + "\n"
        + VISUAL_JS
        + """
</script>
</body>
</html>
"""
    )


def main() -> None:
    school_order = {school["id"]: index for index, school in enumerate(SCHOOLS)}
    lessons = LESSONS_CORE + LESSONS_APPLY + LESSONS_REF
    lessons.sort(key=lambda item: (school_order[item["school"]], item["id"]))
    validate(lessons)
    lesson_html, by_school = build_lessons(lessons)
    track_count = sum(1 for school in SCHOOLS if school["kind"] == "track")
    page = assemble(
        lesson_html,
        nav_html(by_school),
        home_html(lessons, by_school),
        map_html(by_school),
        school_pages(by_school),
    )
    urls = re.findall(r"https?://[^\s'\"<>)]+", page)
    bad = [url for url in urls if "127.0.0.1" not in url and "www.w3.org" not in url]
    if bad:
        raise SystemExit("External URL slipped into the campus file: " + ", ".join(bad))
    counts = measure(page)
    OUT.write_text(page, encoding="utf-8")
    write_hero(len(lessons), track_count)
    print(f"lessons {len(lessons)}")
    print(f"tracks {track_count}")
    for key in ("svg", "flows", "audio", "widgets", "heroes", "plates", "icons", "unique_art"):
        print(f"{key} {counts[key]}")
    print(f"bytes {OUT.stat().st_size}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
