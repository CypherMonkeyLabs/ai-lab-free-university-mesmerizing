"""Diagram atlas, animated flows, and the real-data chart strip.

The 38 room drawings are read from campus/assets/origin-diagrams. The animated
flows are drawn here. Counts are checked at build time.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

from campus.pool import _scope_svg

ROOT = Path(__file__).resolve().parents[1]
DIAGRAMS = ROOT / "campus" / "assets" / "origin-diagrams"

MIN_DIAGRAMS = 25
MIN_FLOWS = 12
MIN_CHARTS = 6


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def _ladder(diagram_id: str, title: str, columns: list[str], messages: list[tuple[int, int, str]]) -> str:
    width = 160 + len(columns) * 180
    height = 90 + len(messages) * 42
    heads = []
    for index, name in enumerate(columns):
        x = 100 + index * 180
        heads.append(
            f'<text x="{x}" y="36" text-anchor="middle" fill="#67e8f9" font-size="14" font-family="system-ui,sans-serif">{esc(name)}</text>'
            f'<line x1="{x}" y1="48" x2="{x}" y2="{height - 16}" stroke="#1e3a52"/>'
        )
    arrows = []
    path_parts: list[str] = []
    for index, (left, right, label) in enumerate(messages):
        y = 78 + index * 42
        x1 = 100 + left * 180
        x2 = 100 + right * 180
        arrows.append(
            f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#34d399" marker-end="url(#{diagram_id}-arr)"/>'
            f'<text x="{(x1 + x2) // 2}" y="{y - 8}" text-anchor="middle" fill="#e7f6ff" font-size="12" font-family="system-ui,sans-serif">{esc(label)}</text>'
        )
        path_parts.append(f"{'M' if index == 0 else 'L'} {x1} {y} L {x2} {y}")
    path = " ".join(path_parts)
    return (
        f'<svg class="atlas-svg" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">'
        f'<rect width="{width}" height="{height}" rx="16" fill="#070b16"/>'
        f'<defs><marker id="{diagram_id}-arr" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
        f'<path d="M0 0 L7 3 L0 6 Z" fill="#34d399"/></marker></defs>'
        + "".join(heads)
        + "".join(arrows)
        + f'<path id="{diagram_id}-route" d="{path}" fill="none" stroke="none"/>'
        f'<circle class="pkt" r="6" fill="#f8fafc"><animateMotion dur="4.5s" repeatCount="indefinite">'
        f'<mpath href="#{diagram_id}-route"/></animateMotion></circle></svg>'
    )


def _boxes(diagram_id: str, title: str, labels: list[str]) -> str:
    width = 80 + len(labels) * 150
    height = 180
    parts = []
    points = []
    for index, label in enumerate(labels):
        x = 30 + index * 150
        parts.append(
            f'<rect x="{x}" y="56" width="120" height="48" rx="12" fill="#10182c" stroke="#22d3ee"/>'
            f'<text x="{x + 60}" y="86" text-anchor="middle" fill="#e7f6ff" font-size="13" font-family="system-ui,sans-serif">{esc(label)}</text>'
        )
        points.append((x + 60, 80))
    lines = []
    path = []
    for index in range(len(points) - 1):
        x1, y1 = points[index]
        x2, y2 = points[index + 1]
        lines.append(f'<line x1="{x1 + 50}" y1="{y1}" x2="{x2 - 50}" y2="{y2}" stroke="#34d399"/>')
        path.append(f"{'M' if index == 0 else 'L'} {x1 + 50} {y1} L {x2 - 50} {y2}")
    return (
        f'<svg class="atlas-svg" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">'
        f'<rect width="{width}" height="{height}" rx="16" fill="#070b16"/>'
        + "".join(parts)
        + "".join(lines)
        + f'<path id="{diagram_id}-route" d="{" ".join(path)}" fill="none"/>'
        f'<circle class="pkt" r="6" fill="#f8fafc"><animateMotion dur="3.5s" repeatCount="indefinite">'
        f'<mpath href="#{diagram_id}-route"/></animateMotion></circle></svg>'
    )


def _tree(diagram_id: str, title: str, rows: list[tuple[str, str]]) -> str:
    height = 70 + len(rows) * 48
    parts = []
    path = []
    for index, (symptom, move) in enumerate(rows):
        y = 48 + index * 48
        parts.append(
            f'<rect x="24" y="{y}" width="250" height="32" rx="8" fill="#10182c" stroke="#fbbf24"/>'
            f'<text x="36" y="{y + 21}" fill="#fde68a" font-size="13" font-family="system-ui,sans-serif">{esc(symptom)}</text>'
            f'<line x1="274" y1="{y + 16}" x2="340" y2="{y + 16}" stroke="#34d399"/>'
            f'<text x="352" y="{y + 21}" fill="#e7f6ff" font-size="13" font-family="system-ui,sans-serif">{esc(move)}</text>'
        )
        path.append(f"{'M' if index == 0 else 'L'} 274 {y + 16} L 340 {y + 16}")
    return (
        f'<svg class="atlas-svg" viewBox="0 0 760 {height}" role="img" aria-label="{esc(title)}">'
        f'<rect width="760" height="{height}" rx="16" fill="#070b16"/>'
        + "".join(parts)
        + f'<path id="{diagram_id}-route" d="{" ".join(path)}" fill="none"/>'
        f'<circle class="pkt" r="5" fill="#f8fafc"><animateMotion dur="5s" repeatCount="indefinite">'
        f'<mpath href="#{diagram_id}-route"/></animateMotion></circle></svg>'
    )


def _authored() -> list[dict]:
    specs = [
        ("flow-completion", "Completion ladder", "ladder", "One HTTPS call. The model returns scores over the next token.",
         _ladder("flow-completion", "Completion ladder", ["App", "API", "Model"], [
             (0, 1, "443, pinned host"),
             (1, 2, "token budget"),
             (2, 1, "next-token scores"),
             (1, 0, "text or timeout"),
         ])),
        ("flow-rag", "Retrieval data flow", "data", "Find a span, cite the id, or refuse. The model does not mint the source.",
         _ladder("flow-rag", "Retrieval data flow", ["Question", "Index", "Pack", "Model"], [
             (0, 1, "query vector, same model id"),
             (1, 2, "chunk ids"),
             (2, 3, "data, not instructions"),
             (3, 0, "cite or refuse"),
         ])),
        ("flow-tool", "Tool-call ladder", "signal", "The host runs the tool. A schema match is not permission.",
         _ladder("flow-tool", "Tool-call ladder", ["Model", "Host", "Tool"], [
             (0, 1, "tool name and arguments"),
             (1, 1, "permission check"),
             (1, 2, "handler, idempotent"),
             (2, 0, "result in the trace"),
         ])),
        ("flow-voice", "Voice ladder", "ladder", "The voice platform owns signaling and media. Emergency never enters this ladder.",
         _ladder("flow-voice", "Voice ladder", ["Caller", "SIP", "ASR", "Model", "TTS"], [
             (0, 1, "signaling"),
             (1, 2, "audio already captured"),
             (2, 3, "transcript"),
             (3, 4, "text to speak"),
             (4, 0, "platform plays audio"),
         ])),
        ("flow-route", "Routing flow", "routing", "Answer, refuse, or hand to a person. The router does not get the side-effect tool.",
         _boxes("flow-route", "Routing flow", ["Turn", "Router", "Answer", "Refuse", "Person"])),
        ("flow-architecture", "Architecture", "architecture", "Policy, retrieval, model, tools, trace, and a gate. A person sits on side effects.",
         _boxes("flow-architecture", "Architecture", ["Input", "Policy", "Retrieve", "Model", "Tools", "Gate"])),
        ("flow-deploy", "Deployment", "deployment", "Pin the ids, keep the key out of the repo, and name the kill switch.",
         _boxes("flow-deploy", "Deployment", ["Config", "Secret", "Timeout", "Log", "Switch"])),
        ("flow-cutover", "Migration cutover", "migration", "Users see the old path until a limited audience holds.",
         _boxes("flow-cutover", "Migration cutover", ["Shadow", "Limited", "Wider", "Retire"])),
        ("flow-trouble", "Troubleshooting tree", "troubleshooting", "Read the trace before you edit the prompt.",
         _tree("flow-trouble", "Troubleshooting tree", [
             ("No trace", "Stop and add one"),
             ("Wrong fact", "Was the span in the pack?"),
             ("Tool error", "The handler, not the tone"),
             ("Should refuse", "The gate failed"),
             ("Slow phone", "Time ASR, model, TTS"),
         ])),
        ("flow-ports", "Ports path", "routing", "A study path, not a firewall rule to paste.",
         _ladder("flow-ports", "Ports path", ["Laptop", "App", "Model API", "Collector"], [
             (0, 1, "loopback only, until you share"),
             (1, 2, "443 to the pinned host"),
             (1, 3, "4318 to your collector"),
             (0, 0, "11434 stays on loopback"),
         ])),
        ("flow-eval", "Eval gate", "data", "Same tasks. Quality, safety, latency, and cost. A person owns the gate.",
         _boxes("flow-eval", "Eval gate", ["Tasks", "Run", "Score", "Compare", "Ship"])),
        ("flow-agent", "Agent loop", "signal", "Schema, permission, result, stop. The queue still owns the person.",
         _boxes("flow-agent", "Agent loop", ["Goal", "Schema", "Tool", "Trace", "Stop"])),
        ("flow-emergency", "Emergency split", "ladder", "An emergency request leaves the model path.",
         _ladder("flow-emergency", "Emergency split", ["Caller", "Voice platform", "Model"], [
             (0, 1, "emergency intent"),
             (1, 1, "platform emergency path"),
             (0, 2, "ordinary turn only"),
         ])),
        ("flow-mcp", "MCP transports", "architecture", "Stdio has no port. Remote MCP is HTTP on a port you choose.",
         _boxes("flow-mcp", "MCP transports", ["Host", "Stdio", "HTTP", "Tool"])),
    ]
    cards = []
    for diagram_id, title, kind, caption, svg in specs:
        cards.append(
            {
                "id": diagram_id,
                "title": title,
                "kind": kind,
                "caption": caption,
                "animated": True,
                "href": "#atlas",
                "svg": svg,
            }
        )
    return cards


def _origin_cards(lessons: list[dict]) -> list[dict]:
    by_room: dict[str, str] = {}
    for item in lessons:
        match = re.search(r"t(\d+)r(\d+)$", item["id"])
        if match:
            by_room[f"T{match.group(1)}-R{int(match.group(2)):02d}"] = item["id"]
    cards = []
    if not DIAGRAMS.is_dir():
        return cards
    for folder in sorted(path for path in DIAGRAMS.iterdir() if path.is_dir()):
        lesson_id = by_room.get(folder.name, "")
        href = f"#{lesson_id}" if lesson_id else "#atlas"
        for name, kind, caption in (
            ("arch.svg", "architecture", f"Architecture map for {folder.name}. Teaching drawing from the study draft."),
            ("sequence.svg", "ladder", f"Sequence for {folder.name}. Who speaks at each step in the study draft."),
        ):
            path = folder / name
            if not path.is_file():
                continue
            svg = _scope_svg(path.read_text(encoding="utf-8"), f"atlas-{folder.name}-{name.split('.')[0]}")
            cards.append(
                {
                    "id": f"{folder.name}-{name.split('.')[0]}",
                    "title": f"{folder.name} {kind}",
                    "kind": kind,
                    "caption": caption + " Not re-fetched on 2026-10-15.",
                    "animated": False,
                    "href": href,
                    "svg": svg,
                }
            )
    return cards


def _card(item: dict) -> str:
    animated = "1" if item["animated"] else "0"
    return (
        f'<article class="atlas-card" data-atlas-diagram="{esc(item["id"])}" data-animated="{animated}" data-kind="{esc(item["kind"])}">'
        f'<h3><a href="{esc(item["href"])}">{esc(item["title"])}</a></h3>'
        f'{item["svg"]}'
        f'<p>{esc(item["caption"])}</p></article>'
    )


def _bar_chart(prefix: str, chart_id: str, title: str, rows: list[tuple[str, int]], note: str) -> str:
    row_h = 26
    height = 48 + len(rows) * row_h
    width = 720
    peak = max((value for _label, value in rows), default=1) or 1
    bars = []
    for index, (label, value) in enumerate(rows):
        y = 36 + index * row_h
        bar = max(2, int(340 * value / peak))
        bars.append(
            f'<text x="12" y="{y + 16}" fill="#e7f6ff" font-size="12" font-family="system-ui,sans-serif">{esc(label[:28])}</text>'
            f'<rect x="220" y="{y}" width="{bar}" height="16" rx="4" fill="#22d3ee"/>'
            f'<text x="{228 + bar}" y="{y + 13}" fill="#93b4c9" font-size="12" font-family="system-ui,sans-serif">{value}</text>'
        )
    return (
        f'<figure class="real-chart" data-real-chart="{esc(chart_id)}">'
        f'<figcaption>{esc(title)}</figcaption>'
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">'
        f'<rect width="{width}" height="{height}" rx="12" fill="#070b16"/>'
        + "".join(bars)
        + f'</svg><p class="block-note">{esc(note)}</p></figure>'
    )


def chart_facts(lessons: list[dict]) -> dict[str, list[tuple[str, int]]]:
    composition = {"Course": 0, "Rooms": 0, "Glossary": 0, "Interview": 0, "Ecosystem": 0}
    levels: dict[str, int] = {}
    per_track: dict[str, int] = {}
    per_minutes: dict[str, int] = {}
    checks: dict[str, int] = {}
    for item in lessons:
        school = item["school"]
        if school == "GL":
            composition["Glossary"] += 1
        elif school == "IV":
            composition["Interview"] += 1
        elif school == "EX":
            composition["Ecosystem"] += 1
        elif "-p-" in item["id"]:
            composition["Rooms"] += 1
        else:
            composition["Course"] += 1
        levels[item["level"]] = levels.get(item["level"], 0) + 1
        if school not in {"GL", "IV", "FQ"}:
            per_track[school] = per_track.get(school, 0) + 1
            per_minutes[school] = per_minutes.get(school, 0) + int(item["minutes"])
            checks[school] = checks.get(school, 0) + sum(1 for block in item["blocks"] if block.get("t") == "check")
    return {
        "composition": list(composition.items()),
        "levels": sorted(levels.items()),
        "tracks": sorted(per_track.items()),
        "minutes": sorted(per_minutes.items()),
        "checks": sorted(checks.items()),
    }


def _charts(prefix: str, lessons: list[dict], flow_count: int, diagram_count: int) -> str:
    facts = chart_facts(lessons)
    figures = [
        _bar_chart(prefix, f"{prefix}-composition", "Pages in the catalog", facts["composition"],
                   "Counted from lesson ids in this build. Rooms are the long imported pages."),
        _bar_chart(prefix, f"{prefix}-tracks", "Lessons on each track", facts["tracks"],
                   "Glossary, interview, and FAQ are reference sections and are not in these bars."),
        _bar_chart(prefix, f"{prefix}-minutes", "Minutes on each track", facts["minutes"],
                   "Minutes are the lesson field in the catalog, including expanded glossary stubs."),
        _bar_chart(prefix, f"{prefix}-levels", "Lessons by level", facts["levels"],
                   "Levels are the course labels core, practice, and advanced."),
        _bar_chart(prefix, f"{prefix}-checks", "Check questions on each track", facts["checks"],
                   "Counted from check blocks on track lessons, not from the quiz bank."),
        _bar_chart(prefix, f"{prefix}-drawings", "Drawings in the atlas",
                   [("Room diagrams", diagram_count - flow_count), ("Animated flows", flow_count)],
                   "Room diagrams are the 38 study-draft files. Animated flows are drawn for this campus."),
    ]
    if len(figures) < MIN_CHARTS:
        raise SystemExit(f"chart strip has {len(figures)} charts")
    values = ",".join(str(value) for _label, value in facts["minutes"])
    labels = ",".join(label for label, _value in facts["minutes"])
    return (
        f'<div class="chart-strip" data-chart-strip="{esc(prefix)}">'
        + "".join(figures)
        + f'<div class="lib-charts">'
        f'<figure class="real-chart" data-real-chart="{esc(prefix)}-d3" data-d3-chart data-labels="{esc(labels)}" data-values="{esc(values)}">'
        f'<figcaption>Minutes again, drawn with D3 when scripts run</figcaption>'
        f'<p class="block-note">The bar chart above is the same minute counts. This frame is filled by the vendored D3 script.</p></figure>'
        f'<figure class="real-chart" data-real-chart="{esc(prefix)}-rough" data-rough-chart>'
        f'<figcaption>Sketch frame</figcaption>'
        f'<svg class="rough-host" viewBox="0 0 280 80" role="img" aria-label="Sketch frame around the chart strip"></svg>'
        f'<p class="block-note">Rough.js draws this frame from the lesson count {len(lessons)}. The number is the catalog.</p></figure>'
        f'</div></div>'
    )


def _parallax(lessons: list[dict], flow_count: int, diagram_count: int, sheet_count: int) -> str:
    minutes = sum(int(item["minutes"]) for item in lessons)
    hours = round(minutes / 60)
    tiles = [
        ("Lessons", len(lessons)),
        ("Diagrams", diagram_count),
        ("Flows", flow_count),
        ("Sheets", sheet_count),
        ("Hours", hours),
    ]
    cards = []
    for index, (label, value) in enumerate(tiles):
        cards.append(
            f'<article class="tilt-card" style="--tilt:{-8 + index * 4}deg">'
            f'<svg class="cube" viewBox="0 0 48 48" aria-hidden="true">'
            f'<polygon points="24,6 42,16 24,26 6,16" fill="#22d3ee" opacity="0.9"/>'
            f'<polygon points="24,26 42,16 42,34 24,44" fill="#0e7490"/>'
            f'<polygon points="24,26 6,16 6,34 24,44" fill="#155e75"/>'
            f'</svg>'
            f'<strong data-count="{value}">{value}</strong><span>{esc(label)}</span></article>'
        )
    return f'<div class="parallax-row" data-parallax>{"".join(cards)}</div>'


def _mindmap() -> str:
    return (
        '<figure class="real-chart" data-real-chart="mindmap">'
        '<figcaption>Ecosystem mind map</figcaption>'
        '<svg id="mindmap" class="mindmap" viewBox="0 0 720 280"></svg>'
        '<script type="application/json" id="mindmapData">'
        '{"content":"System you ship","children":['
        '{"content":"Model","children":[{"content":"Pinned id","children":[]}]},'
        '{"content":"Retrieval","children":[{"content":"Cite or refuse","children":[]}]},'
        '{"content":"Tools","children":[{"content":"Host permission","children":[]}]},'
        '{"content":"Trace","children":[{"content":"Ids and counts","children":[]}]},'
        '{"content":"Voice","children":[{"content":"Platform owns the call","children":[]}]}'
        ']}</script>'
        '<p class="block-note">markmap-view draws this tree. The words are this course, not a vendor map.</p></figure>'
    )


def build_surface(lessons: list[dict], sheet_count: int) -> dict[str, str | int]:
    authored = _authored()
    origin = _origin_cards(lessons)
    cards = authored + origin
    animated = sum(1 for card in cards if card["animated"])
    if len(cards) < MIN_DIAGRAMS or animated < MIN_FLOWS:
        raise SystemExit(f"atlas has {len(cards)} diagrams and {animated} animated flows")
    if len(origin) < 38:
        raise SystemExit(f"expected 38 room diagrams, found {len(origin)}")
    atlas = (
        '<section id="atlas" data-panel="atlas">'
        '<p class="eyebrow">Diagram atlas</p>'
        f'<h1>{len(cards)} diagrams, {animated} animated flows</h1>'
        '<p class="lede">The room drawings are the 38 files from the study folder. The animated flows are ladders, routing, architecture, deployment, cutover, and a troubleshooting tree drawn for this course.</p>'
        '<div class="badge-row" role="group" aria-label="Filter diagrams">'
        '<button type="button" data-atlas-filter="all" aria-pressed="true">All</button>'
        '<button type="button" data-atlas-filter="animated">Animated flows</button>'
        '<button type="button" data-atlas-filter="architecture">Architecture</button>'
        '<button type="button" data-atlas-filter="ladder">Ladders</button>'
        '</div>'
        f'<div class="atlas-grid">{"".join(_card(card) for card in cards)}</div></section>'
    )
    flows = (
        '<section id="flows" data-panel="flows">'
        '<p class="eyebrow">Animated flows</p>'
        f'<h1>{animated} call, signal, and data flows</h1>'
        '<p class="lede">Each picture moves a packet along the study path. Emergency stays on the voice platform. Reduced motion hides the packet.</p>'
        f'<div class="atlas-grid">{"".join(_card(card) for card in cards if card["animated"])}</div></section>'
    )
    charts = (
        '<section id="charts" data-panel="charts">'
        '<p class="eyebrow">Charts from this catalog</p>'
        '<h1>Counts you can recompute</h1>'
        '<p class="lede">Every bar is a count from the lesson files in this build. Nothing here is a vendor dashboard.</p>'
        + _parallax(lessons, animated, len(cards), sheet_count)
        + _charts("charts", lessons, animated, len(cards))
        + _mindmap()
        + '</section>'
    )
    strip = _parallax(lessons, animated, len(cards), sheet_count) + _charts("home", lessons, animated, len(cards))
    return {
        "atlas": atlas,
        "flows": flows,
        "charts": charts,
        "strip": strip,
        "diagrams": len(cards),
        "flows_n": animated,
        "origin": len(origin),
    }


def track_strip(school_id: str, lessons: list[dict], sheet_count: int, diagrams: int, flows_n: int) -> str:
    mine = [item for item in lessons if item["school"] == school_id]
    minutes = sum(int(item["minutes"]) for item in mine)
    head = (
        f'<div class="track-surface">'
        f'<p class="block-note">This section has {len(mine)} pages and {minutes} minutes. '
        f'The charts below are the whole catalog, so the numbers match the home page.</p>'
        + _parallax(lessons, flows_n, diagrams, sheet_count)
        + _charts(f"t{school_id}", lessons, flows_n, diagrams)
        + '</div>'
    )
    if head.count("data-real-chart") < MIN_CHARTS:
        raise SystemExit(f"track {school_id} chart strip is short")
    return head
