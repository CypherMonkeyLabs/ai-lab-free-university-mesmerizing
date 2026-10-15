#!/usr/bin/env python3
"""Build the offline campus shell at campus/ai-lab-university.html."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from campus.atlas import build_surface, track_strip
from campus.cheats import SHEETS, write_cheats
from campus.chrome import CHROME_CSS, course_links, extra_nav, footer, topbar
from campus.glossary_expand import expand_glossary
from campus.diagrams import FIGURES
from campus.flagship_lessons import LESSONS as LESSONS_ECO
from campus.lessons_apply import LESSONS as LESSONS_APPLY
from campus.lessons_core import LESSONS as LESSONS_CORE
from campus.lessons_ref import LESSONS as LESSONS_REF
from campus.pool import LESSONS as LESSONS_POOL
from campus.pool import apply_folds, attach_diagrams
from campus.schema import PATHS, SCHOOLS
from campus.quiz_bank import bank, cards_for
from campus.surfaces import arcade_page, downloads_page
from campus.tips import TIPS
from campus.playgrounds import (
    APP_CSS,
    APP_JS,
    LABS,
    command_palette,
    lab_for,
    launcher_section,
    mini_player,
    play_nav,
    playgrounds_page,
    track_cards,
)
from campus.visuals import (
    VISUAL_CSS,
    VISUAL_JS,
    accent,
    achievements_html,
    builds_nav,
    builds_page,
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
    write_audio_assets,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "campus" / "ai-lab-university.html"
HERO = ROOT / "docs" / "assets" / "hero.svg"

BANNED = (
    "share freely",
    "builder lens",
    "licc",
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
        elif kind == "svg":
            parts.append(
                f"<figure class=\"diagram origin-figure\">{block['html']}"
                f"<figcaption>{inline(block['caption'])}</figcaption></figure>"
            )
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


def build_lessons(lessons: list[dict]) -> tuple[str, dict[str, list[dict]], dict[str, str]]:
    by_school: dict[str, list[dict]] = {school["id"]: [] for school in SCHOOLS}
    parts: list[str] = []
    for item in lessons:
        by_school[item["school"]].append(item)
        index = len(by_school[item["school"]])
        total = None  # filled after; placeholder replaced below
        parts.append((item, index))
    rendered: list[str] = []
    by_id: dict[str, str] = {}
    for item, index in parts:
        total = len(by_school[item["school"]])
        school = next(school for school in SCHOOLS if school["id"] == item["school"])
        try_href, try_name = lab_for(item["id"], item["school"])
        article = (
            f"<article class=\"lesson\" id=\"{item['id']}\" data-panel=\"lesson\" "
            f"data-school=\"{item['school']}\" data-title=\"{html.escape(item['title'])}\" "
            f"data-search=\"{html.escape(lesson_search(item))}\" style=\"--accent:{accent(item['school'])}\">"
            f"{lesson_head(item, index, total, school, try_href, try_name)}"
            f"<div class=\"prose\">{render_blocks(item)}</div>"
            f"{lesson_tail(item)}"
            f"</article>"
        )
        rendered.append(article)
        by_id[item["id"]] = article
    return "".join(rendered), by_school, by_id


def nav_html(by_school: dict[str, list[dict]], icons: bool = True, embed_links: bool = True) -> tuple[str, dict[str, str]]:
    blocks: list[str] = []
    link_map: dict[str, str] = {}
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
                + (f"<span class=\"nav-ico\">{nav_icon(item)}</span>" if icons else "")
                + f"<span>{html.escape(item['title'])}</span></a>"
            )
        joined = "".join(links)
        link_map[school["id"]] = joined
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
            f"<div class=\"lesson-links\">{joined if embed_links else ''}</div></div>"
        )
    return "".join(blocks), link_map


def school_pages(
    by_school: dict[str, list[dict]],
    lessons: list[dict],
    sheet_count: int,
    diagrams: int,
    flows_n: int,
) -> tuple[str, dict[str, str]]:
    pages: list[str] = []
    by_id: dict[str, str] = {}
    for school in SCHOOLS:
        items = by_school[school["id"]]
        kind = "Track" if school["kind"] == "track" else "Reference"
        page = (
            f"<article class=\"school-page\" id=\"school-{school['id']}\" data-panel=\"school\" "
            f"data-school=\"{school['id']}\" style=\"--accent:{accent(school['id'])}\">"
            f"<p class=\"kicker\">{kind} {html.escape(school['id'])}</p>"
            f"<h1>{html.escape(school['name'])}</h1>"
            f"<p class=\"lede\">{html.escape(school['outcome'])}</p>"
            f"<p><a class=\"btn primary\" href=\"#{items[0]['id']}\">"
            f"{'Start this track' if school['kind'] == 'track' else 'Open the first entry'}</a></p>"
            f"{track_strip(school['id'], lessons, sheet_count, diagrams, flows_n)}"
            f"{hub_html(school, items)}"
            f"{lesson_cards(items)}</article>"
        )
        pages.append(page)
        by_id[school["id"]] = page
    return "".join(pages), by_id


def _mascot_variations() -> str:
    faces = (
        ("#F6C453", "#E7A23A"),
        ("#7CDEFF", "#3DB7E8"),
        ("#F472B6", "#FB7185"),
        ("#C4F54A", "#86EFAC"),
    )
    parts = []
    for fill, ear in faces:
        parts.append(
            f'<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="34" r="16" fill="{fill}"/>'
            f'<circle cx="18" cy="22" r="8" fill="{ear}"/><circle cx="46" cy="22" r="8" fill="{ear}"/>'
            f'<circle cx="26" cy="32" r="2.2" fill="#1c1408"/><circle cx="38" cy="32" r="2.2" fill="#1c1408"/></svg>'
        )
    return f'<div class="mascot-variations" aria-label="Mascot variations">{"".join(parts)}</div>'


def home_html(lessons: list[dict], by_school: dict[str, list[dict]], strip: str) -> str:
    track_count = sum(1 for school in SCHOOLS if school["kind"] == "track")
    minutes = sum(item["minutes"] for item in lessons)
    hours = round(minutes / 60)
    cards = track_cards(by_school)
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
  <div class="hero hero-stage">
    <div class="space-mount hero-world" id="heroMount" data-space="topology" data-label="3D campus topology. Orbit to move around the learner, prompt, model, retriever, tools, and eval gate.">
      <p class="space-fallback">A 3D map of the course: prompt, model, retriever, tools, and an eval gate. This browser has no WebGL, so the map stays flat. Drag does nothing here.</p>
      <div class="fail-toggles" role="group" aria-label="Topology failure scenarios">
        <button type="button" data-fail="retriever" aria-pressed="false">Retriever miss</button>
        <button type="button" data-fail="tools" aria-pressed="false">Tool denied</button>
        <button type="button" data-fail="eval" aria-pressed="false">Eval stop</button>
      </div>
    </div>
    <div class="hero-copy" data-i18n-root>
    <p class="eyebrow" data-i18n="eyebrow">Offline course · October 2026 · MIT code · CC BY-NC-SA content</p>
    <h1 data-i18n="hero-title">Learn to build AI systems you can test.</h1>
    <p class="lede" data-i18n="hero-lede">The glowing map is the path: prompt, model, retrieval, tools, and an eval gate. No account. No key required to read it.</p>
    <div class="hero-actions">
      <a class="btn primary" id="continueLink" href="#00-01" data-i18n="start">Start the course</a>
      <a class="btn" href="#play" data-i18n="play">Open playgrounds</a>
      <a class="btn" href="#atlas" data-i18n="nav-diagrams">Diagrams</a>
      <a class="btn" href="#flows" data-i18n="nav-flows">Flows</a>
      <a class="btn" href="#downloads" data-i18n="nav-cheats">Cheat codes</a>
      <a class="btn" href="#regions" data-i18n="regions">Regions</a>
    </div>
    <dl class="stats">
      <div><dt data-i18n="tracks">Tracks</dt><dd data-count="{track_count}">0</dd></div>
      <div><dt data-i18n="lessons">Lessons</dt><dd id="statLessons" data-count="{len(lessons)}">0</dd></div>
      <div><dt data-i18n="hours">Reading time</dt><dd><span data-count="{hours}">0</span> <span data-i18n="hours-unit">hours</span></dd></div>
      <div><dt data-i18n="network">Network calls</dt><dd data-count="0">0</dd></div>
    </dl>
    </div>
  </div>
  <section class="block" id="homeSurface">
    <div class="block-head"><h2>Diagrams, flows, and charts</h2><p>The same counts are on every track page.</p></div>
    {_mascot_variations()}
    <div class="dash-progress glass">
      <svg class="ring dash-ring" viewBox="0 0 36 36" aria-hidden="true"><circle class="track" cx="18" cy="18" r="15" pathLength="100"/><circle class="value" id="dashRing" cx="18" cy="18" r="15" pathLength="100" stroke-dasharray="0 100"/></svg>
      <div>
        <strong id="dashPct">0%</strong>
        <span id="dashCaption">Nothing marked complete yet.</span>
        <span id="streakLine">Streak <strong id="streakCount">0</strong> <span id="streakUnit">days</span></span>
        <a id="dashContinue" href="#00-01">Start the course</a>
      </div>
    </div>
    {home_poster()}
    {strip}
    <section class="audio-studio" id="architectAudio">
      <h2>Architect conversation</h2>
      <p class="lede">Two short clips about how to view, practise, and share this lab. Two Piper voices, en_GB alba and en_US lessac, over a synthesized chord pad. The words are also in <code>audio/scripts/</code>.</p>
      <div class="audio-row">
        <figure>
          <figcaption>Tour the first screen</figcaption>
          <audio controls preload="none" src="assets/audio/architect-tour.wav"></audio>
        </figure>
        <figure>
          <figcaption>Practise, download, and share</figcaption>
          <audio controls preload="none" src="assets/audio/architect-practise.wav"></audio>
        </figure>
      </div>
      <p class="block-note">Rate, comment, or help from the repository. Share the lab from the Labs link. This audio is a study guide, not a certificate.</p>
      <p><a href="https://github.com/cipher0x9/ai-lab-free-university-mesmerizing/issues">Rate, comment, or help</a> · <a href="https://cyphermonkeylabs.com">Labs</a> · <a href="https://linktr.ee/cyphermonkey">Links</a></p>
    </section>
    <p><a class="btn primary" href="#atlas">Open the diagram atlas</a> <a class="btn" href="#flows">Play the flows</a> <a class="btn" href="#charts">Open the charts</a> <a class="btn" href="#downloads">Cheat codes</a></p>
  </section>
  <section class="block" id="trackBoard">
    <div class="block-head">
      <h2>Tracks</h2>
      <div class="seg" role="group" aria-label="Filter tracks">
        <button type="button" data-track-filter="all" aria-pressed="true">All</button>
        <button type="button" data-track-filter="open">Still open</button>
        <button type="button" data-track-filter="done">Finished</button>
      </div>
    </div>
    <p class="block-note">Take them in order the first time. Each card says why that track matters. The bar is your progress in this browser. The catalog count is every study page, including short glossary entries and interview drills. The 581 figure is 128 course lessons plus 453 imported pages, checked by id before the ecosystem track was added.</p>
    <div class="track-grid">{cards}</div>
    <p id="trackEmpty" class="block-note" hidden>No track is in that state yet.</p>
  </section>
  {launcher_section()}
  <section class="block">
    <div class="block-head"><h2>Continue</h2><p id="homeProg">Nothing marked complete yet.</p></div>
    <a class="continue-card" id="continueCard" href="#00-01">
      <span class="eyebrow">Next lesson</span>
      <strong id="continueTitle">How to use this campus</strong>
      <em id="continueMeta">Start here · 8 min</em>
    </a>
    <div class="bar" aria-hidden="true"><i id="homeBar"></i></div>
  </section>
  {achievements_html()}
  <section class="block">
    <div class="block-head"><h2>Choose a route</h2><p>Short paths through the same lessons. The track map is the full course.</p></div>
    <div class="routes">{''.join(routes)}</div>
  </section>
  {home_extra()}
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
  <text x="64" y="362" fill="#A8B3C7" font-family="system-ui,Segoe UI,sans-serif" font-size="24">Shell page plus track modules. Free to use, share, and remix.</text>
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
  --cc-bg: #0B1120;
  --cc-surface: #131D31;
  --cc-accent-1: #818CF8;
  --cc-accent-2: #2DD4BF;
  --cc-accent-3: #FBBF24;
  --cc-accent-4: #F472B6;
  --bg: var(--cc-bg);
  --side: #090f1c;
  --card: var(--cc-surface);
  --card-2: #1b2740;
  --ink: #E8EDF7;
  --muted: #9AA8C3;
  --line: #2A3650;
  --primary: var(--cc-accent-1);
  --primary-2: #A5B4FC;
  --link: #C7D2FE;
  --on-primary: #0B1120;
  --cyan: var(--cc-accent-2);
  --green: #34D399;
  --amber: var(--cc-accent-3);
  --rose: var(--cc-accent-4);
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
  --cc-bg: #F8FAFC;
  --cc-surface: #FFFFFF;
  --cc-accent-1: #4F46E5;
  --cc-accent-2: #0F766E;
  --cc-accent-3: #B45309;
  --cc-accent-4: #BE185D;
  --bg: var(--cc-bg);
  --side: #FFFFFF;
  --card: var(--cc-surface);
  --card-2: #F8FAFC;
  --ink: #0B1220;
  --muted: #52627A;
  --line: #E2E8F4;
  --primary: var(--cc-accent-1);
  --primary-2: #4F46E5;
  --link: #3730A3;
  --on-primary: #ffffff;
  --figure: #F8FAFC;
  --code: #0F172A;
  --shadow: 0 10px 30px rgba(11,18,32,.06);
  color-scheme: light;
}
html[data-theme="dusk"] {
  --cc-bg: #1A120B;
  --cc-surface: #2A1C12;
  --cc-accent-1: #F6C177;
  --cc-accent-2: #E07A5F;
  --cc-accent-3: #F4A261;
  --cc-accent-4: #E9C46A;
  --bg: var(--cc-bg);
  --side: #140E09;
  --card: var(--cc-surface);
  --card-2: #3A2818;
  --ink: #F8EDE3;
  --muted: #D4C4B0;
  --line: #5C4636;
  --primary: var(--cc-accent-1);
  --primary-2: #FFE0A3;
  --link: #FFE0A3;
  --on-primary: #1A120B;
  --cyan: var(--cc-accent-2);
  --green: #C4D7A4;
  --amber: var(--cc-accent-3);
  --rose: #E8A0A0;
  --violet: #E9C46A;
  --figure: #1A120B;
  --code: #120C08;
  --shadow: 0 16px 40px rgba(0,0,0,.35);
  color-scheme: dark;
}
html[data-theme="contrast"] {
  --cc-bg: #000;
  --cc-surface: #000;
  --cc-accent-1: #FFE14A;
  --cc-accent-2: #9FF7EE;
  --cc-accent-3: #FFE14A;
  --cc-accent-4: #FFD0D8;
  --bg: #000;
  --side: #000;
  --card: #000;
  --card-2: #000;
  --ink: #fff;
  --muted: #fff;
  --line: #fff;
  --primary: #FFE14A;
  --primary-2: #fff;
  --link: #fff;
  --on-primary: #000;
  --cyan: #9FF7EE;
  --green: #B6FFCF;
  --amber: #FFE14A;
  --rose: #FFD0D8;
  --violet: #EFE7FF;
  --figure: #000;
  --code: #000;
  color-scheme: dark;
}
html[data-font="sm"] { --font-size: 15px; }
html[data-font="lg"] { --font-size: 19px; }
html[data-font="xl"] { --font-size: 22px; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: var(--font);
  background: var(--bg);
  color: var(--ink);
  font-size: var(--font-size, 17px);
  line-height: 1.6;
  min-height: 100vh;
}
::selection { background: #6366F1; color: #fff; }
:focus-visible { outline: 2px solid var(--primary-2); outline-offset: 2px; }
a { color: var(--link); text-decoration-thickness: 1px; text-underline-offset: 3px; }
a:hover { color: var(--primary-2); }
#routeLandmarks {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0;
}
.skip {
  position: absolute; left: 12px; top: -40px; background: var(--primary); color: var(--on-primary);
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
.icon-btn.text-btn { width: auto; min-width: 40px; padding: 0 12px; }
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
html.route-pending #stage { visibility: hidden; }
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
  * { transition: none !important; animation: none !important; }
}
html[data-motion="reduce"] { scroll-behavior: auto; }
html[data-motion="reduce"] * { transition: none !important; animation: none !important; }
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
  const catalog = JSON.parse(document.getElementById("campusCatalog").textContent);
  window.CampusCatalog = catalog;
  const byMeta = Object.fromEntries(catalog.lessons.map((item) => [item.id, item]));
  const schoolById = Object.fromEntries(catalog.schools.map((item) => [item.id, item]));
  const order = catalog.order.slice();
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
    const allowed = { dark: true, light: true, contrast: true, dusk: true, futuristic: true, gaming: true, neon: true, holographic: true, cyberpunk: true, sunset: true };
    if (!allowed[theme]) theme = "neon";
    document.documentElement.setAttribute("data-theme", theme);
    document.dispatchEvent(new CustomEvent("campus-theme", { detail: theme }));
    const high = theme === "contrast";
    document.documentElement.setAttribute("data-contrast", high ? "high" : "normal");
    localStorage.setItem(THEME_KEY, theme);
    localStorage.setItem("ailab-v3-contrast", high ? "high" : "normal");
    themeBtn.setAttribute("aria-pressed", theme === "light" ? "false" : "true");
    themeBtn.setAttribute("aria-label", "Theme is " + theme + ". Activate to cycle themes.");
    document.querySelectorAll('input[name="setTheme"]').forEach((input) => {
      input.checked = input.value === theme;
    });
    const contrastBtn = document.getElementById("contrastBtn");
    if (contrastBtn) {
      contrastBtn.setAttribute("aria-pressed", high ? "true" : "false");
      contrastBtn.setAttribute("aria-label", high ? "HC, turn off high contrast" : "HC, turn on high contrast");
    }
  }
  window.CampusTheme = applyTheme;
  themeBtn.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme");
    applyTheme(current === "dark" ? "light" : "dark");
  });
  const contrastBtn = document.getElementById("contrastBtn");
  if (contrastBtn) {
    contrastBtn.addEventListener("click", () => {
      const current = document.documentElement.getAttribute("data-theme");
      if (current === "contrast") applyTheme(localStorage.getItem("ailab-v3-theme-prev") || "dark");
      else {
        if (current) localStorage.setItem("ailab-v3-theme-prev", current);
        applyTheme("contrast");
      }
    });
  }
  applyTheme(document.documentElement.getAttribute("data-theme") || "dark");

  function saveStudy() { localStorage.setItem(STUDY_KEY, JSON.stringify([...studied])); }
  function nextUnstudied() {
    const last = localStorage.getItem(LAST_KEY);
    if (last && byMeta[last] && !studied.has(last)) return last;
    return order.find((id) => !studied.has(id)) || order[order.length - 1];
  }
  function refreshProgress() {
    const done = order.filter((id) => studied.has(id)).length;
    const pct = Math.round((done / order.length) * 100);
    ring.setAttribute("stroke-dasharray", pct + " 100");
    studiedLabel.textContent = done + " of " + order.length + " complete";
    if (homeProg) homeProg.textContent = done + " of " + order.length + " lessons marked complete";
    if (homeBar) homeBar.style.width = pct + "%";
    document.querySelectorAll("a.ll").forEach((link) => {
      link.classList.toggle("done", studied.has(link.dataset.id));
    });
    const nid = nextUnstudied();
    const meta = byMeta[nid];
    if (continueTitle && meta) continueTitle.textContent = meta.title;
    if (continueMeta && meta) continueMeta.textContent = (schoolById[meta.school] ? schoolById[meta.school].name : "Track") + " · " + meta.minutes + " min";
    if (continueLink) continueLink.setAttribute("href", "#" + nid);
    if (continueCard) continueCard.setAttribute("href", "#" + nid);
    if (continueLink) continueLink.textContent = done === 0 ? "Start the course" : (done === order.length ? "Review the course" : "Continue");
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
    if (window.CampusSettings) window.CampusSettings.play(studied.has(id) ? "ok" : "no");
    refreshProgress();
    document.dispatchEvent(new CustomEvent("campus-marked", { detail: { id, on: studied.has(id) } }));
  });

  let navPackPromise = null;
  function navPack() {
    if (!navPackPromise) navPackPromise = loadJSON("assets/curriculum/nav.json");
    return navPackPromise;
  }
  function fillSchool(schoolId) {
    const block = document.querySelector('.school-block[data-school="' + schoolId + '"]');
    if (!block || block.dataset.filled === "1") return Promise.resolve();
    return navPack().then((pack) => {
      if (block.dataset.filled === "1") return;
      const host = block.querySelector(".lesson-links");
      host.innerHTML = (pack.schools || {})[schoolId] || "";
      block.dataset.filled = "1";
      host.querySelectorAll("a.ll").forEach((link) => {
        link.classList.toggle("done", studied.has(link.dataset.id));
      });
    });
  }
  function fillNav() {
    return navPack().then((pack) => Promise.all(Object.keys(pack.schools || {}).map((id) => fillSchool(id))));
  }
  function setOpenSchool(schoolId) {
    document.querySelectorAll(".school-block").forEach((block) => {
      const open = block.dataset.school === schoolId;
      block.classList.toggle("open", open);
      const chev = block.querySelector(".chev");
      chev.setAttribute("aria-expanded", open ? "true" : "false");
    });
    if (schoolId) fillSchool(schoolId);
  }
  document.querySelectorAll(".chev").forEach((button) => {
    button.addEventListener("click", () => {
      const block = button.closest(".school-block");
      const open = !block.classList.contains("open");
      block.classList.toggle("open", open);
      button.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) fillSchool(block.dataset.school);
    });
  });

  function pagerLink(anchor, id, label) {
    if (!id || !byMeta[id]) {
      anchor.hidden = true;
      return;
    }
    anchor.hidden = false;
    anchor.href = "#" + id;
    anchor.innerHTML = "<small>" + label + "</small><span></span>";
    anchor.querySelector("span").textContent = byMeta[id].title;
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
    if (raw === "builds") return { view: "builds" };
    if (raw === "cheats") return { view: "downloads" };
    if (raw === "downloads" || raw === "arcade" || raw === "atlas" || raw === "flows" || raw === "charts" || raw === "regions") return { view: raw };
    if (raw === "play" || raw.startsWith("play-")) return { view: "play", id: raw };
    if (raw.startsWith("school-")) return { view: "school", id: raw };
    if (byMeta[raw]) return { view: "lesson", id: raw };
    return { view: "missing" };
  }

  const modules = new Map();
  let homeHTML = "";
  let showGen = 0;

  function stage() { return document.getElementById("stage"); }
  function mounted(id) {
    const node = document.getElementById(id);
    return node && stage().contains(node) ? node : null;
  }
  function rememberHome() {
    const home = document.getElementById("home");
    if (home && !homeHTML) homeHTML = home.outerHTML;
  }
  function mount(html) {
    document.querySelectorAll(".walk.is-playing").forEach((walk) => {
      if (walk._timer) window.clearInterval(walk._timer);
    });
    stage().innerHTML = html;
    const panel = stage().querySelector("[data-panel]");
    if (panel) panel.classList.add("active");
    parkLandmarks(stage());
    document.dispatchEvent(new CustomEvent("campus-mount"));
  }
  const parked = new Set();
  function releaseLandmarks() {
    parked.forEach((id) => {
      const node = document.querySelector('#routeLandmarks [data-park="' + id + '"]');
      if (node && !document.getElementById(id)) node.id = id;
    });
    parked.clear();
  }
  function parkLandmarks(root) {
    releaseLandmarks();
    if (!root) return;
    root.querySelectorAll("[id]").forEach((node) => {
      const slot = document.querySelector('#routeLandmarks [id="' + CSS.escape(node.id) + '"]');
      if (!slot || slot === node) return;
      slot.dataset.park = node.id;
      slot.removeAttribute("id");
      parked.add(node.id);
    });
  }
  function ensureTargets() {
    const box = document.getElementById("routeLandmarks");
    if (!box) return;
    document.querySelectorAll('a[href^="#"]').forEach((link) => {
      const id = decodeURIComponent((link.getAttribute("href") || "").slice(1));
      if (!id || document.getElementById(id)) return;
      const node = document.createElement("span");
      node.id = id;
      node.tabIndex = -1;
      box.appendChild(node);
    });
  }
  function missingHTML(message) {
    return '<section id="view-missing" class="missing" data-panel="missing"><h1>That page is not in the course.</h1><p class="lede">' + message + '</p><p><a class="btn primary" href="#home">Back to home</a></p></section>';
  }
  async function loadJSON(url) {
    if (modules.has(url)) return modules.get(url);
    const job = fetch(url).then((res) => {
      if (!res.ok) throw new Error(url);
      return res.json();
    });
    modules.set(url, job);
    job.catch(() => modules.delete(url));
    return job;
  }
  async function ensure(route) {
    rememberHome();
    if (route.view === "home") {
      if (!mounted("home")) mount(homeHTML);
      return;
    }
    if (route.view === "map" || route.view === "studio" || route.view === "builds" || route.view === "play" || route.view === "downloads" || route.view === "arcade" || route.view === "atlas" || route.view === "flows" || route.view === "charts" || route.view === "regions") {
      if (mounted(route.view)) return;
      const data = await loadJSON("assets/curriculum/" + route.view + ".json");
      mount(data.html);
      return;
    }
    if (route.view === "school") {
      if (mounted(route.id)) return;
      const id = route.id.replace(/^school-/, "");
      const data = await loadJSON("assets/curriculum/track-" + id + ".json");
      mount(data.hub);
      return;
    }
    if (route.view === "lesson") {
      const meta = byMeta[route.id];
      if (!meta) throw new Error("unknown lesson");
      const existing = mounted(route.id);
      if (existing && existing.classList.contains("lesson")) return;
      const data = await loadJSON("assets/curriculum/track-" + meta.school + ".json");
      if (!data.lessons[route.id]) throw new Error("missing lesson");
      mount(data.lessons[route.id]);
      return;
    }
    if (!document.getElementById("view-missing")) mount(missingHTML("The link does not match a lesson or a track."));
  }
  function updateDock(route) {
    document.querySelectorAll("[data-dock]").forEach((link) => {
      if (link.getAttribute("data-dock") === route.view) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
  }
  async function show(route) {
    const gen = ++showGen;
    let failed = false;
    try { await ensure(route); } catch (err) { failed = true; }
    if (gen !== showGen) return;
    if (failed) {
      mount(missingHTML("This view did not load. Open the course from the site once so the files can stay on this device. A local disk path cannot fetch the track files."));
      route = { view: "missing" };
    }
    const keepScroll = document.body.dataset.view === "play" && route.view === "play";
    document.body.dataset.view = route.view;
    document.body.classList.remove("is-enter");
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      requestAnimationFrame(() => document.body.classList.add("is-enter"));
    }
    document.querySelectorAll("[data-panel]").forEach((el) => el.classList.remove("active"));
    document.querySelectorAll("a.ll").forEach((link) => link.classList.remove("on"));
    let crumbText = "Home";
    let schoolId = null;
    if (route.view === "home") {
      mounted("home").classList.add("active");
    } else if (route.view === "map") {
      mounted("map").classList.add("active");
      crumbText = "Track map";
    } else if (route.view === "studio") {
      mounted("studio").classList.add("active");
      crumbText = "Studio";
      const studioLink = document.querySelector("a.studio-link");
      if (studioLink) studioLink.classList.add("on");
    } else if (route.view === "builds") {
      mounted("builds").classList.add("active");
      crumbText = "Builds";
      const buildsLink = document.querySelector("a.builds-link");
      if (buildsLink) buildsLink.classList.add("on");
    } else if (route.view === "play") {
      mounted("play").classList.add("active");
      crumbText = "Playgrounds";
      const playLink = document.querySelector("a.play-link");
      if (playLink) playLink.classList.add("on");
    } else if (route.view === "downloads") {
      mounted("downloads").classList.add("active");
      crumbText = "Cheat codes";
    } else if (route.view === "arcade") {
      mounted("arcade").classList.add("active");
      crumbText = "Arcade";
    } else if (route.view === "atlas" || route.view === "flows" || route.view === "charts" || route.view === "regions") {
      mounted(route.view).classList.add("active");
      crumbText = { atlas: "Diagrams", flows: "Flows", charts: "Charts", regions: "Regions" }[route.view];
    } else if (route.view === "school") {
      const page = mounted(route.id);
      if (!page) { show({ view: "missing" }); return; }
      page.classList.add("active");
      crumbText = page.querySelector("h1").textContent;
      schoolId = page.dataset.school;
    } else if (route.view === "lesson") {
      const page = mounted(route.id);
      if (!page) { show({ view: "missing" }); return; }
      crumbText = page.dataset.title;
      schoolId = page.dataset.school;
      await fillSchool(schoolId);
      page.classList.add("active");
      const link = document.querySelector('a.ll[data-id="' + route.id + '"]');
      if (link) link.classList.add("on");
      showLessonChrome(route.id);
    } else {
      const missing = document.getElementById("view-missing");
      if (missing) missing.classList.add("active");
      crumbText = "Not found";
    }
    crumb.textContent = crumbText;
    document.title = crumbText + " · AI Lab Free University";
    if (schoolId) setOpenSchool(schoolId);
    if (!keepScroll) window.scrollTo(0, 0);
    closeNav();
    updateDock(route);
    document.documentElement.classList.remove("route-pending");
    const h1 = document.querySelector("#stage h1");
    if (h1 && route.view !== "home") {
      h1.tabIndex = -1;
      h1.focus({ preventScroll: true });
    }
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
  search.addEventListener("input", () => {
    const term = search.value.trim();
    if (!term) { applySearch(); return; }
    fillNav().then(applySearch);
  });
  search.addEventListener("keydown", (event) => {
    if (event.key !== "Enter") return;
    event.preventDefault();
    fillNav().then(() => {
      applySearch();
      const first = document.querySelector("a.ll:not([hidden])");
      if (first) location.hash = first.getAttribute("href");
    });
  });
  document.addEventListener("keydown", (event) => {
    const tag = (event.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea") return;
    if (event.key === "/") { event.preventDefault(); search.focus(); }
    if (document.body.dataset.view !== "lesson") return;
    if (event.key === "[" && !pagerPrev.hidden) pagerPrev.click();
    if (event.key === "]" && !pagerNext.hidden) pagerNext.click();
  });

  const sourcesBtn = document.getElementById("sourcesBtn");
  const sourcesDrawer = document.getElementById("sourcesDrawer");
  if (sourcesBtn && sourcesDrawer && sourcesDrawer.showModal) {
    sourcesBtn.addEventListener("click", () => sourcesDrawer.showModal());
    sourcesDrawer.addEventListener("click", (event) => {
      if (event.target.closest("[data-close]")) sourcesDrawer.close();
    });
  }
  const dockMenu = document.getElementById("dockMenu");
  if (dockMenu) dockMenu.addEventListener("click", () => menuBtn.click());
  if (location.protocol === "http:" || location.protocol === "https:") {
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("sw.js").catch(() => {});
    }
    const warm = ["assets/curriculum/map.json", "assets/curriculum/play.json", "assets/curriculum/studio.json", "assets/curriculum/builds.json", "assets/curriculum/downloads.json", "assets/curriculum/arcade.json", "assets/curriculum/atlas.json", "assets/curriculum/flows.json", "assets/curriculum/charts.json", "assets/curriculum/regions.json"]
      .concat(catalog.schools.map((school) => "assets/curriculum/track-" + school.id + ".json"));
    let warmIndex = 0;
    const warmNext = () => {
      if (warmIndex >= warm.length) return;
      const url = warm[warmIndex];
      warmIndex += 1;
      fetch(url).catch(() => {}).finally(() => {
        if (window.requestIdleCallback) window.requestIdleCallback(warmNext, { timeout: 2500 });
        else window.setTimeout(warmNext, 700);
      });
    };
    window.setTimeout(() => {
      if (window.requestIdleCallback) window.requestIdleCallback(warmNext, { timeout: 4000 });
      else warmNext();
    }, 12000);
  }
  refreshProgress();
  rememberHome();
  ensureTargets();
  window.campusBoot = () => show(parseHash());
})();
"""



def sources_drawer() -> str:
    return """
<dialog id="sourcesDrawer" class="sources-drawer" aria-labelledby="sourcesTitle">
  <h2 id="sourcesTitle">Primary sources</h2>
  <p class="lede">The course is a teaching text. These are the papers and specs behind the mechanisms.</p>
  <ul class="source-list">
    <li>
      <strong>Vaswani et al., 2017. Attention Is All You Need.</strong>
      <p>Transformer attention, the mechanism behind the token playground.</p>
      <div class="badge-row"><a href="https://arxiv.org/abs/1706.03762">arXiv 1706.03762</a><a href="https://doi.org/10.48550/arXiv.1706.03762">DOI</a></div>
    </li>
    <li>
      <strong>Lewis et al., 2020. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.</strong>
      <p>Retrieve a passage, then generate. The retrieval track follows that split.</p>
      <div class="badge-row"><a href="https://arxiv.org/abs/2005.11401">arXiv 2005.11401</a><a href="https://doi.org/10.48550/arXiv.2005.11401">DOI</a></div>
    </li>
    <li>
      <strong>Hu et al., 2021. LoRA: Low-Rank Adaptation of Large Language Models.</strong>
      <p>Low-rank updates instead of full fine-tuning. The rank lab is a picture of that budget.</p>
      <div class="badge-row"><a href="https://arxiv.org/abs/2106.09685">arXiv 2106.09685</a><a href="https://doi.org/10.48550/arXiv.2106.09685">DOI</a></div>
    </li>
    <li>
      <strong>Model Context Protocol specification, revision 2025-06-18.</strong>
      <p>JSON-RPC handshake, tools/list, and tools/call. The inspector plays a teaching trace of that shape.</p>
      <div class="badge-row"><a href="https://modelcontextprotocol.io/specification/2025-06-18">MCP specification</a></div>
    </li>
    <li>
      <strong>Vendor documentation.</strong>
      <p>Pin the page you actually called. Names and parameters move.</p>
      <div class="badge-row"><a href="https://platform.openai.com/docs">OpenAI docs</a><a href="https://docs.anthropic.com/en/docs">Anthropic docs</a><a href="https://huggingface.co/docs">Hugging Face docs</a></div>
    </li>
  </ul>
  <p><button type="button" class="btn" data-close>Close</button></p>
</dialog>
"""


def dock_html() -> str:
    return """
<nav class="dock" aria-label="Primary">
  <a href="#home" data-dock="home" aria-current="page">Home</a>
  <a href="#map" data-dock="map">Map</a>
  <a href="#play" data-dock="play">Labs</a>
  <a href="#studio" data-dock="studio">Studio</a>
  <button type="button" id="dockMenu">Tracks</button>
</nav>
"""


def assemble(lessons_html: str, nav: str, home: str, tracks: str, schools: str, lessons: list[dict], *, shell: bool = False, catalog: str = "") -> str:
    if shell:
        main_body = f'<div id="stage">{home}</div>'
    else:
        main_body = home + tracks + schools + lessons_html + builds_page() + studio_page() + playgrounds_page(lessons)
    catalog_tag = f'<script type="application/json" id="campusCatalog">{catalog}</script>' if shell else '<script type="application/json" id="campusCatalog">{"lessons":[],"schools":[],"order":[]}</script>'
    extra_chrome = (sources_drawer() + dock_html()) if shell else ""
    return (
        """<!DOCTYPE html>
<html lang="en" data-theme="neon">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<meta name="description" content="AI Lab Free University. A free offline course in models, retrieval, agents, MCP, coding agents, evals, and product judgment."/>
<meta name="color-scheme" content="dark light"/>
<meta property="og:title" content="AI Lab Free University"/>
<meta property="og:description" content="__LESSON_COUNT__ study pages in __TRACK_COUNT__ tracks. Agents, MCP, retrieval, evals, and the voice bridge. Offline. No key required to study."/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="https://cipher0x9.github.io/ai-lab-free-university-mesmerizing/campus/ai-lab-university.html"/>
<meta property="og:image" content="https://cipher0x9.github.io/ai-lab-free-university-mesmerizing/campus/og-card.png"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta property="og:image:alt" content="AI Lab Free University. Learn to build AI systems you can test."/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="AI Lab Free University"/>
<meta name="twitter:description" content="__LESSON_COUNT__ study pages in __TRACK_COUNT__ tracks. One offline campus. No key required to study."/>
<meta name="twitter:image" content="https://cipher0x9.github.io/ai-lab-free-university-mesmerizing/campus/og-card.png"/>
<meta name="twitter:image:alt" content="AI Lab Free University. Learn to build AI systems you can test."/>
<title>AI Lab Free University</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%236366F1'/%3E%3Ccircle cx='16' cy='16' r='3' fill='white'/%3E%3C/svg%3E"/>
<script>
try {
  var saved = localStorage.getItem("ailab-v3-theme");
  var contrast = localStorage.getItem("ailab-v3-contrast");
  var themeOk = { dark: 1, light: 1, contrast: 1, dusk: 1, futuristic: 1, gaming: 1, neon: 1, holographic: 1, cyberpunk: 1, sunset: 1 };
  if (saved && !themeOk[saved]) saved = "neon";
  if ((!saved || saved === "dark" || saved === "light" || saved === "neon") && contrast === "high") saved = "contrast";
  if (saved) document.documentElement.setAttribute("data-theme", saved);
  if (saved === "contrast" || contrast === "high") document.documentElement.setAttribute("data-contrast", "high");
  var font = localStorage.getItem("ailab-v3-font");
  if (font) document.documentElement.setAttribute("data-font", font);
  if (localStorage.getItem("ailab-v3-motion") === "reduce") document.documentElement.setAttribute("data-motion", "reduce");
  if (location.hash && location.hash !== "#" && location.hash !== "#home") document.documentElement.classList.add("route-pending");
} catch (err) {}
document.documentElement.classList.add("js");
</script>
<style>
"""
        + CSS
        + "\n"
        + VISUAL_CSS
        + "\n"
        + APP_CSS
        + CHROME_CSS
        + """
</style>
</head>
<body data-view="home">
<a class="skip" href="#content">Skip to content</a>
"""
        + topbar()
        + """
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
        + play_nav()
        + extra_nav()
        + studio_nav()
        + builds_nav()
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
    <button type="button" class="cmd-btn" id="cmdBtn" aria-keyshortcuts="Control+K" aria-label="Search the course">
      <svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14 M20 20l-3.2-3.2"/></svg>
      <span class="cmd-label">Search</span>
      <kbd>Ctrl K</kbd>
    </button>
    <button type="button" class="icon-btn text-btn" id="tipsBtn" aria-haspopup="dialog" aria-controls="tipsDrawer">Tips</button>
    <button type="button" class="icon-btn text-btn" id="settingsBtn" aria-haspopup="dialog" aria-controls="settingsDrawer">Settings</button>
    <button type="button" class="icon-btn text-btn" id="sourcesBtn" aria-haspopup="dialog" aria-controls="sourcesDrawer">Sources</button>
    <button type="button" class="icon-btn text-btn" id="contrastBtn" aria-pressed="false" aria-label="HC, turn on high contrast">HC</button>
    <button type="button" class="icon-btn" id="themeBtn" aria-pressed="true" aria-label="Switch to light theme">
      <svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 14.5A8.5 8.5 0 1 1 9.5 3 7 7 0 0 0 21 14.5z"/></svg>
      <svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
    </button>
  </header>
  <main id="content">
"""
        + main_body
        + ("" if shell else """
    <section id="view-missing" class="missing" data-panel="missing">
      <h1>That page is not in the course.</h1>
      <p class="lede">The link does not match a lesson or a track.</p>
      <p><a class="btn primary" href="#home">Back to home</a></p>
    </section>
""")
        + command_palette()
        + mini_player()
        + """
"""
        + footer()
        + """
  </main>
  <nav class="pager" id="pager" aria-label="Lesson">
    <a id="pagerPrev" href="#home"><small>Previous</small><span>Home</span></a>
    <button type="button" id="markBtn">Mark complete</button>
    <a id="pagerNext" href="#00-01"><small>Next</small><span>Next lesson</span></a>
  </nav>
</div>
</div>
"""
        + extra_chrome
        + '<div id="routeLandmarks"></div>\n'
        + catalog_tag
        + """
<script src="vendor/d3.min.js"></script>
<script src="vendor/rough.js"></script>
<script src="vendor/confetti.browser.js"></script>
<script src="vendor/markmap-view.js"></script>
<script>
"""
        + JS
        + "\n"
        + VISUAL_JS
        + "\n"
        + APP_JS
        + "\n"
        + (ROOT / "campus" / "flagship.js").read_text(encoding="utf-8")
        + """
</script>
<script type="module" src="assets/js/effects.js"></script>
</body>
</html>
"""
    )


def _dump_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, separators=(",", ":")), encoding="utf-8")


def _write_worker(files: list[str]) -> None:
    core = json.dumps(files, ensure_ascii=True)
    (ROOT / "campus" / "sw.js").write_text(
        f"""/* Offline cache for the campus. Generated with the page. */
const CACHE = "ailab-campus-v10";
const CORE = {core};
self.addEventListener("install", (event) => {{
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(CORE.map((name) => new URL(name, self.location)))));
  self.skipWaiting();
}});
self.addEventListener("activate", (event) => {{
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key)))).then(() => self.clients.claim())
  );
}});
self.addEventListener("fetch", (event) => {{
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin || event.request.method !== "GET") return;
  event.respondWith(
    caches.match(event.request).then((cached) => {{
      const network = fetch(event.request).then((response) => {{
        if (response && response.ok) {{
          const copy = response.clone();
          caches.open(CACHE).then((cache) => cache.put(event.request, copy));
        }}
        return response;
      }}).catch(() => cached);
      return cached || network;
    }})
  );
}});
""",
        encoding="utf-8",
    )


def main() -> None:
    school_order = {school["id"]: index for index, school in enumerate(SCHOOLS)}
    lessons = LESSONS_CORE + LESSONS_APPLY + LESSONS_REF + LESSONS_POOL + LESSONS_ECO
    apply_folds(lessons)
    expanded = expand_glossary(lessons)
    diagrams = attach_diagrams(lessons)
    lessons.sort(key=lambda item: (school_order[item["school"]], item["id"]))
    validate(lessons)
    lesson_html, by_school, lesson_by_id = build_lessons(lessons)
    surface = build_surface(lessons, len(SHEETS))
    school_html, school_by_id = school_pages(
        by_school, lessons, len(SHEETS), int(surface["diagrams"]), int(surface["flows_n"])
    )
    home = home_html(lessons, by_school, str(surface["strip"]))
    track_map = map_html(by_school)
    track_count = sum(1 for school in SCHOOLS if school["kind"] == "track")
    full_nav, _link_map = nav_html(by_school, embed_links=True)
    full = assemble(lesson_html, full_nav, home, track_map, school_html, lessons, shell=False)
    counts = measure(full)
    catalog = {
        "order": [item["id"] for item in lessons],
        "lessons": [
            {
                "id": item["id"],
                "school": item["school"],
                "title": item["title"],
                "minutes": item["minutes"],
                "summary": item["summary"],
            }
            for item in lessons
        ],
        "schools": [
            {"id": school["id"], "name": school["name"], "kind": school["kind"], "outcome": school["outcome"]}
            for school in SCHOOLS
        ],
        "plays": [lab[0] for lab in LABS],
    }
    catalog_json = json.dumps(catalog, ensure_ascii=True).replace("<", "\\u003c")
    shell_nav, link_map = nav_html(by_school, embed_links=False)
    page = assemble(
        lesson_html,
        shell_nav,
        home,
        "",
        "",
        lessons,
        shell=True,
        catalog=catalog_json,
    )
    allowed = (
        "127.0.0.1",
        "www.w3.org",
        "arxiv.org",
        "doi.org",
        "modelcontextprotocol.io",
        "platform.openai.com",
        "docs.anthropic.com",
        "huggingface.co",
        "https://cipher0x9.github.io/ai-lab-free-university-mesmerizing/",
        "cyphermonkeylabs.com",
        "linktr.ee/cyphermonkey",
        "dev.to/cyphermonkey",
        "x.com/Cypher0x9",
        "github.com/cipher0x9/",
        "cipher0x9.github.io/",
        "creativecommons.org/licenses/by-nc-sa/4.0/",
        "airc.nist.gov",
    )
    page = page.replace("__LESSON_COUNT__", str(len(lessons))).replace("__TRACK_COUNT__", str(track_count))
    urls = re.findall(r"https?://[^\s'\"<>)]+", page)
    bad = [url for url in urls if not any(piece in url for piece in allowed)]
    if bad:
        raise SystemExit("External URL slipped into the campus file: " + ", ".join(bad))
    visible = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", "", page, flags=re.I)
    h1_count = len(re.findall(r"<h1\b", visible, flags=re.I))
    if h1_count != 1:
        raise SystemExit(f"The shell must contain one h1, found {h1_count}")
    curriculum = ROOT / "campus" / "assets" / "curriculum"
    curriculum.mkdir(parents=True, exist_ok=True)
    for old in curriculum.glob("*.json"):
        old.unlink()
    questions = bank(lessons)
    deck = cards_for(questions)
    _dump_json(curriculum / "catalog.json", catalog)
    _dump_json(curriculum / "nav.json", {"schools": link_map})
    _dump_json(curriculum / "tips.json", TIPS)
    _dump_json(curriculum / "quiz.json", {"questions": questions})
    _dump_json(curriculum / "cards.json", {"cards": deck})
    _dump_json(curriculum / "map.json", {"html": track_map})
    _dump_json(curriculum / "play.json", {"html": playgrounds_page(lessons)})
    _dump_json(curriculum / "studio.json", {"html": studio_page()})
    _dump_json(curriculum / "builds.json", {"html": builds_page()})
    sheet_count = write_cheats(deck)
    if sheet_count < 10:
        raise SystemExit(f"need 10 cheat sheets, wrote {sheet_count}")
    _dump_json(curriculum / "downloads.json", {"html": downloads_page(sheet_count, min(400, len(deck)))})
    _dump_json(curriculum / "arcade.json", {"html": arcade_page()})
    _dump_json(curriculum / "atlas.json", {"html": surface["atlas"]})
    _dump_json(curriculum / "flows.json", {"html": surface["flows"]})
    _dump_json(curriculum / "charts.json", {"html": surface["charts"]})
    _dump_json(curriculum / "regions.json", {"html": surface["regions"]})
    if str(surface["atlas"]).count("data-atlas-diagram") < 25:
        raise SystemExit("diagram atlas is below 25")
    if str(surface["flows"]).count('data-animated="1"') < 12:
        raise SystemExit("animated flows are below 12")
    if home.count("data-real-chart") < 6 or "data-parallax" not in home:
        raise SystemExit("home is missing charts or the parallax counters")
    for school_id, hub in school_by_id.items():
        if hub.count("data-real-chart") < 6 or "data-parallax" not in hub:
            raise SystemExit(f"track {school_id} is missing charts or counters")
    for school in SCHOOLS:
        name = f"track-{school['id']}.json"
        lessons_for = {item["id"]: lesson_by_id[item["id"]] for item in by_school[school["id"]]}
        _dump_json(curriculum / name, {"id": school["id"], "hub": school_by_id[school["id"]], "lessons": lessons_for})
    _write_worker(["ai-lab-university.html", "assets/curriculum/catalog.json"])
    OUT.write_text(page, encoding="utf-8")
    clips = write_audio_assets()
    write_hero(len(lessons), track_count)
    pool_n = sum(1 for item in lessons if "-p-" in item["id"])
    eco_n = sum(1 for item in lessons if item["school"] == "EX")
    print(f"glossary_expanded {expanded}")
    print(f"atlas {surface['diagrams']} flows {surface['flows_n']} origin {surface['origin']} sheets {sheet_count}")
    print(f"lessons {len(lessons)}")
    print(f"pool {pool_n}")
    print(f"ecosystem {eco_n}")
    print(f"base {len(lessons) - pool_n - eco_n}")
    print(f"diagrams {diagrams}")
    print(f"minutes {sum(item['minutes'] for item in lessons)}")
    print(f"tracks {track_count}")
    print(f"audio_files {clips}")
    for key in (
        "svg", "unique_svg", "flows", "reels", "audio", "widgets", "heroes",
        "plates", "icons", "unique_art", "charts", "demos", "min_lesson_flows",
    ):
        print(f"{key} {counts[key]}")
    print(f"bytes {OUT.stat().st_size}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
