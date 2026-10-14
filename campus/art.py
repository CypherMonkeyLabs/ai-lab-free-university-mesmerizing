"""Original SVG illustrations, plates, and step-through flows."""

from __future__ import annotations

import html
import math

from campus.icons import ICONS

HEROES = {
    "balance", "bits", "columns", "cycle", "desk", "folder", "gate", "layers",
    "library", "machine", "meters", "route", "search", "shield", "speech", "stream",
}
PLATES = {"bars", "compare", "cycle", "funnel", "gates", "layers", "pipeline", "scatter", "split", "stack"}
ACCENT = {
    "balance": "#F5B942",
    "bits": "#0F9B8E",
    "columns": "#38BDF8",
    "cycle": "#A78BFA",
    "desk": "#38BDF8",
    "folder": "#F5B942",
    "gate": "#22C55E",
    "layers": "#6366F1",
    "library": "#0F9B8E",
    "machine": "#0F9B8E",
    "meters": "#22C55E",
    "route": "#38BDF8",
    "search": "#6366F1",
    "shield": "#F5B942",
    "speech": "#A78BFA",
    "stream": "#818CF8",
}


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def _commands(spec: str) -> str:
    parts: list[str] = []
    for raw in spec.split("|"):
        bits = raw.strip().split()
        if not bits:
            continue
        op = bits[0]
        if op in {"C", "F"}:
            x, y, r = bits[1:4]
            cls = "icon-fill" if op == "F" else "icon-ink"
            extra = "" if op == "C" else ""
            if op == "C":
                parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" class="icon-ink"/>')
            else:
                parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" class="icon-fill"/>')
        elif op == "R":
            x, y, w, h = bits[1:5]
            parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" class="icon-ink"/>')
        elif op == "L":
            x1, y1, x2, y2 = bits[1:5]
            parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="icon-ink"/>')
        elif op == "P":
            points = " ".join(bit.replace(",", " ") for bit in bits[1:])
            # rebuild as pairs
            nums = []
            for bit in bits[1:]:
                a, b = bit.split(",")
                nums.append(f"{a},{b}")
            parts.append(f'<polyline points="{" ".join(nums)}" class="icon-ink"/>')
        elif op == "G":
            nums = []
            for bit in bits[1:]:
                a, b = bit.split(",")
                nums.append(f"{a},{b}")
            parts.append(f'<polygon points="{" ".join(nums)}" class="icon-ink"/>')
        else:
            raise SystemExit(f"Bad icon op {op}")
    return "".join(parts)


def icon_svg(name: str, art_id: str, badge: str = "") -> str:
    if name not in ICONS:
        raise SystemExit(f"Missing icon {name}")
    mark = ""
    if badge:
        mark = (
            f'<circle cx="50" cy="50" r="11" class="icon-badge"/>'
            f'<text x="50" y="54" text-anchor="middle" class="icon-badge-t">{esc(badge)}</text>'
        )
    return (
        f'<svg class="lesson-icon" data-art="{esc(art_id)}" viewBox="0 0 64 64" aria-hidden="true">'
        f'<rect x="1.5" y="1.5" width="61" height="61" rx="16" class="icon-bg"/>'
        f"{_commands(ICONS[name])}{mark}</svg>"
    )


def _fit(word: str, limit: int) -> str:
    if len(word) <= limit:
        return word
    return word[: max(1, limit - 1)] + "…"


def _wrap(text: str, limit: int, max_lines: int = 2) -> list[str]:
    limit = max(6, limit)
    words = text.split() or [text]
    lines: list[str] = []
    current = ""
    index = 0
    while index < len(words) and len(lines) < max_lines:
        word = _fit(words[index], limit)
        trial = word if not current else f"{current} {word}"
        if len(trial) <= limit:
            current = trial
            index += 1
            continue
        if current:
            lines.append(current)
            current = ""
            continue
        lines.append(word)
        index += 1
    if current and len(lines) < max_lines:
        lines.append(current)
    if index < len(words) and lines and not lines[-1].endswith("…"):
        last = lines[-1]
        room = limit - 1
        lines[-1] = (last[:room] + "…") if len(last) > room else last + "…"
    return lines or [_fit(text, limit)]


def _edge(x1: float, y1: float, x2: float, y2: float, dest: str) -> str:
    dx, dy = x2 - x1, y2 - y1
    mag = math.hypot(dx, dy) or 1
    ux, uy = dx / mag, dy / mag
    pad = 10
    sx, sy = x1 + ux * pad, y1 + uy * pad
    ex, ey = x2 - ux * (pad + 2), y2 - uy * (pad + 2)
    px, py = -uy, ux
    base = 7
    p1 = (ex - ux * 9 + px * base, ey - uy * 9 + py * base)
    p2 = (ex - ux * 9 - px * base, ey - uy * 9 - py * base)
    return (
        f'<g class="edge" data-i="{dest}">'
        f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex - ux * 8:.1f}" y2="{ey - uy * 8:.1f}"/>'
        f'<polygon class="head" points="{ex:.1f},{ey:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"/>'
        f"</g>"
    )


def _stage(index: int, x: float, y: float, w: float, h: float, title: str, shape: str = "rect") -> str:
    if shape == "diamond":
        lines = _wrap(title, max(8, int(w / 16)), 3)
        start = y + h / 2 - (len(lines) - 1) * 8
    else:
        lines = _wrap(title, max(8, int(w / 8.4)))
        start = y + (h / 2 if len(lines) == 1 else h / 2 - 8)
    texts = []
    for offset, line in enumerate(lines):
        texts.append(
            f'<text class="nt" x="{x + w / 2:.1f}" y="{start + offset * 16:.1f}" text-anchor="middle">{esc(line)}</text>'
        )
    if shape == "diamond":
        cx, cy = x + w / 2, y + h / 2
        body = (
            f'<polygon class="body" points="{cx:.1f},{y:.1f} {x + w:.1f},{cy:.1f} '
            f'{cx:.1f},{y + h:.1f} {x:.1f},{cy:.1f}"/>'
        )
        bx, by = cx, y + 28
    else:
        body = f'<rect class="body" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="16"/>'
        bx, by = x + 18, y + 18
    return (
        f'<g class="stage" data-i="{index}">'
        f"{body}"
        f'<circle class="badge" cx="{bx:.1f}" cy="{by:.1f}" r="11"/>'
        f'<text class="badge-n" x="{bx:.1f}" y="{by + 4:.1f}" text-anchor="middle">{index + 1}</text>'
        f'{"".join(texts)}</g>'
    )


def flow_svg(art_id: str, layout: str, steps: list[tuple[str, str]]) -> str:
    n = len(steps)
    titles = [step[0] for step in steps]
    if layout == "loop":
        width, height = 760, 460
        body = _layout_loop(titles)
    elif layout == "stack":
        height = 36 + n * 78
        width = 760
        body = _layout_stack(titles)
    elif layout == "split":
        width, height = 960, 300
        body = _layout_split(titles)
    elif layout == "gate":
        width, height, body = _layout_gate(titles)
    elif layout == "funnel":
        height = 28 + n * 72
        width = 760
        body = _layout_funnel(titles)
    elif layout == "rail":
        node_w = 168
        gap = 20
        margin = 18
        width = int(margin * 2 + n * node_w + max(0, n - 1) * gap)
        height = 220
        body = _layout_rail(titles, width)
    else:
        raise SystemExit(f"Unknown flow layout {layout}")
    return (
        f'<svg class="walk-svg" data-art="flow-{esc(art_id)}" style="min-width:{width}px" '
        f'viewBox="0 0 {width} {height}" role="img" aria-hidden="true">{body}</svg>'
    )


def _layout_rail(titles: list[str], width: float = 960) -> str:
    n = len(titles)
    gap = 20
    margin = 18
    node_w = (width - margin * 2 - gap * (n - 1)) / n
    node_h = 108
    y = 48
    chunks = []
    centers = []
    for i, title in enumerate(titles):
        x = margin + i * (node_w + gap)
        centers.append((x + node_w / 2, y + node_h / 2))
        chunks.append(_stage(i, x, y, node_w, node_h, title))
    for i in range(n - 1):
        x1 = margin + i * (node_w + gap) + node_w
        x2 = x1 + gap
        chunks.append(_edge(x1, y + node_h / 2, x2, y + node_h / 2, str(i + 1)))
    return "".join(chunks)


def _layout_stack(titles: list[str]) -> str:
    chunks = []
    y0 = 16
    for i, title in enumerate(titles):
        y = y0 + i * 78
        chunks.append(_stage(i, 170, y, 420, 64, title))
        if i:
            chunks.append(_edge(380, y - 14, 380, y, str(i)))
    return "".join(chunks)


def _layout_split(titles: list[str]) -> str:
    n = len(titles)
    top = (n + 1) // 2
    rows = [titles[:top], titles[top:]]
    chunks = []
    positions = []
    for r, row in enumerate(rows):
        if not row:
            continue
        gap = 16
        margin = 16
        node_w = (960 - margin * 2 - gap * (len(row) - 1)) / len(row)
        y = 28 + r * 140
        for i, title in enumerate(row):
            x = margin + i * (node_w + gap)
            index = i if r == 0 else top + i
            positions.append((index, x, y, node_w))
            chunks.append(_stage(index, x, y, node_w, 96, title))
        for i in range(len(row) - 1):
            index = i if r == 0 else top + i
            x1 = margin + i * (node_w + gap) + node_w
            chunks.append(_edge(x1, y + 48, x1 + gap, y + 48, str(index + 1)))
    if len(rows[1]):
        first = positions[top - 1]
        second = positions[top]
        x1 = first[1] + first[3] / 2
        y1 = first[2] + 96
        x2 = second[1] + second[3] / 2
        y2 = second[2]
        mid = (y1 + y2) / 2
        chunks.append(
            f'<g class="edge" data-i="{top}">'
            f'<path d="M {x1:.1f} {y1 + 2:.1f} L {x1:.1f} {mid:.1f} L {x2:.1f} {mid:.1f} L {x2:.1f} {y2 - 8:.1f}" fill="none"/>'
            f'<polygon class="head" points="{x2:.1f},{y2 - 1:.1f} {x2 - 6:.1f},{y2 - 12:.1f} {x2 + 6:.1f},{y2 - 12:.1f}"/>'
            f"</g>"
        )
    return "".join(chunks)


def _layout_gate(titles: list[str]) -> tuple[int, int, str]:
    n = len(titles)
    lead = max(1, n - 1)
    gap = 16
    margin = 20
    node_w = 172
    node_h = 108
    y = 70
    diamond_w, diamond_h = 240, 160
    width = int(margin + lead * (node_w + gap) + diamond_w + 36)
    height = 260
    chunks = []
    for i in range(lead):
        x = margin + i * (node_w + gap)
        chunks.append(_stage(i, x, y, node_w, node_h, titles[i]))
        if i:
            chunks.append(_edge(x - gap, y + node_h / 2, x, y + node_h / 2, str(i)))
    if n == 1:
        return width, height, "".join(chunks)
    x = margin + lead * (node_w + gap) + 8
    dy = y + node_h / 2 - diamond_h / 2
    chunks.append(_stage(n - 1, x, dy, diamond_w, diamond_h, titles[-1], shape="diamond"))
    prev_right = margin + (lead - 1) * (node_w + gap) + node_w
    chunks.append(_edge(prev_right, y + node_h / 2, x, dy + diamond_h / 2, str(n - 1)))
    return width, height, "".join(chunks)


def _layout_funnel(titles: list[str]) -> str:
    chunks = []
    for i, title in enumerate(titles):
        inset = i * 28
        y = 16 + i * 72
        w = 680 - inset * 2
        x = 40 + inset
        chunks.append(_stage(i, x, y, w, 60, title))
        if i:
            chunks.append(_edge(380, y - 12, 380, y, str(i)))
    return "".join(chunks)


def _layout_loop(titles: list[str]) -> str:
    n = len(titles)
    cx, cy, radius = 380, 214, 158
    chunks = []
    points = []
    w, h = (150, 72) if n <= 5 else (132, 68)
    for i, title in enumerate(titles):
        angle = -math.pi / 2 + i * (2 * math.pi / n)
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)
        points.append((px, py))
        chunks.append(_stage(i, px - w / 2, py - h / 2, w, h, title))
    for i in range(n):
        j = (i + 1) % n
        dest = "return" if j == 0 else str(j)
        x1, y1 = points[i]
        x2, y2 = points[j]
        group = _edge(x1, y1, x2, y2, dest)
        if dest == "return":
            group = group.replace('class="edge"', 'class="edge edge-return"', 1)
        chunks.append(group)
    chunks.append(f'<text class="ns" x="{cx}" y="{cy}" text-anchor="middle">repeat</text>')
    return "".join(chunks)


def _svg_text(x: float, y: float, text: str, cls: str, anchor: str = "start") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" class="{cls}">{esc(text)}</text>'


def hero_svg(scene: str, art_id: str, title: str, chips: list[str], gid: str) -> str:
    if scene not in HEROES:
        raise SystemExit(f"Unknown hero scene {scene}")
    accent = ACCENT[scene]
    labels = [(chip[:22] + "…") if len(chip) > 22 else chip for chip in chips[:3]]
    while len(labels) < 3:
        labels.append("")
    grid = "".join(
        f'<line x1="{x}" y1="24" x2="{x}" y2="300" class="hero-grid"/>' for x in range(40, 780, 40)
    )
    body = {
        "stream": _hero_stream,
        "library": _hero_library,
        "cycle": _hero_cycle,
        "columns": _hero_columns,
        "layers": _hero_layers,
        "shield": _hero_shield,
        "meters": _hero_meters,
        "desk": _hero_desk,
        "machine": _hero_machine,
        "balance": _hero_balance,
        "speech": _hero_speech,
        "bits": _hero_bits,
        "gate": _hero_gate,
        "folder": _hero_folder,
        "search": _hero_search,
        "route": _hero_route,
    }[scene](labels, accent)
    return (
        f'<svg class="hero-svg" data-art="hero-{esc(art_id)}" viewBox="0 0 800 360" role="img" '
        f'aria-label="{esc(title)}">'
        f"<defs><linearGradient id=\"{gid}\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"1\">"
        f'<stop offset="0%" stop-color="#17233b"/><stop offset="100%" stop-color="#0B1220"/>'
        f'</linearGradient><radialGradient id="{gid}r" cx="88%" cy="0%" r="70%">'
        f'<stop offset="0%" stop-color="{accent}" stop-opacity="0.5"/>'
        f'<stop offset="65%" stop-color="{accent}" stop-opacity="0"/></radialGradient></defs>'
        f'<rect width="800" height="360" rx="22" fill="url(#{gid})"/>'
        f'<rect width="800" height="360" rx="22" fill="url(#{gid}r)"/>'
        f'<g>{grid}</g>{body}'
        f'<rect x="28" y="312" width="744" height="28" rx="8" class="hero-foot"/>'
        f"{_svg_text(40, 331, ' · '.join(labels), 'hero-foot-t')}"
        f"</svg>"
    )


def _card(x, y, w, h, title, accent, sub=""):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#141c33" stroke="{accent}" stroke-width="1.6"/>'
        f"{_svg_text(x + 16, y + 32, title, 'hero-strong')}"
        + (_svg_text(x + 16, y + 54, sub, "hero-soft") if sub else "")
    )


def _hero_stream(labels, accent):
    chips = [("The", 0), ("model", 1), ("predicts", 2), ("next", 3)]
    colors = ["#6366F1", "#0F9B8E", "#F5B942", "#22C55E"]
    tiles = []
    x = 40
    for word, i in chips:
        tiles.append(
            f'<rect x="{x}" y="48" width="{56 + len(word) * 4}" height="36" rx="10" fill="{colors[i]}"/>'
            f"{_svg_text(x + 12, 72, word, 'hero-on')}"
        )
        x += 64 + len(word) * 4
    bars = []
    heights = (92, 64, 40, 24, 14)
    for i, h in enumerate(heights):
        bars.append(f'<rect x="{430 + i * 28}" y="{168 - h}" width="18" height="{h}" rx="5" fill="{accent}" opacity="{1 - i * 0.14}"/>')
    return (
        "".join(tiles)
        + f'<line x1="40" y1="110" x2="250" y2="110" stroke="{accent}" class="hero-flow"/>'
        + _card(40, 132, 250, 110, labels[0], accent, labels[1])
        + "".join(bars)
        + _svg_text(430, 196, labels[2], "hero-soft")
    )


def _hero_library(labels, accent):
    spines = []
    colors = ["#6366F1", "#0F9B8E", "#F5B942", "#A78BFA", "#22C55E"]
    for i, color in enumerate(colors):
        spines.append(f'<rect x="{48 + i * 28}" y="48" width="20" height="120" rx="4" fill="{color}"/>')
    return (
        "".join(spines)
        + _card(230, 48, 280, 130, labels[0], accent, labels[1])
        + f'<rect x="250" y="108" width="180" height="14" rx="4" fill="{accent}" opacity="0.85"/>'
        + _card(540, 70, 210, 150, "Cite", "#22C55E", labels[2])
    )


def _hero_cycle(labels, accent):
    spots = ((400, 70), (620, 180), (500, 280), (220, 280), (140, 160))
    names = [labels[0], labels[1], "Stop", labels[2], "Tool"]
    body = []
    for i, ((x, y), name) in enumerate(zip(spots, names)):
        body.append(f'<circle cx="{x}" cy="{y}" r="36" fill="#141c33" stroke="{accent if i == 0 else "#334155"}" stroke-width="2"/>')
        body.append(_svg_text(x, y + 4, str(i + 1), "hero-strong", "middle"))
        body.append(_svg_text(x, y + 56, name[:18], "hero-soft", "middle"))
    body.append(f'<circle cx="390" cy="180" r="28" fill="none" stroke="{accent}" stroke-dasharray="5 6" class="hero-flow"/>')
    body.append(_svg_text(390, 184, "loop", "hero-soft", "middle"))
    return "".join(body)


def _hero_columns(labels, accent):
    titles = ("Host", "Client", "Server")
    subs = labels
    colors = ("#6366F1", "#38BDF8", "#0F9B8E")
    body = []
    for i, title in enumerate(titles):
        x = 48 + i * 244
        body.append(
            f'<rect x="{x}" y="40" width="220" height="230" rx="18" fill="#141c33" stroke="{colors[i]}"/>'
            f"{_svg_text(x + 20, 78, title, 'hero-kicker')}"
            f"{_svg_text(x + 20, 120, subs[i], 'hero-strong')}"
        )
    return "".join(body)


def _hero_layers(labels, accent):
    body = []
    names = [labels[0], labels[1], "Attention", labels[2]]
    for i, name in enumerate(names):
        y = 40 + i * 58
        body.append(
            f'<rect x="80" y="{y}" width="420" height="46" rx="12" fill="#141c33" stroke="{accent if i == 2 else "#334155"}"/>'
            f"{_svg_text(100, y + 29, name, 'hero-strong')}"
        )
    body.append(f'<rect x="540" y="98" width="200" height="120" rx="16" fill="#141c33" stroke="#F5B942"/>')
    body.append(_svg_text(560, 150, "Adapter", "hero-kicker"))
    body.append(_svg_text(560, 180, "only if you train", "hero-soft"))
    return "".join(body)


def _hero_shield(labels, accent):
    return (
        f'<path d="M180 48 L300 78 L300 160 Q300 230 180 270 Q60 230 60 160 L60 78 Z" fill="#141c33" stroke="{accent}" stroke-width="2"/>'
        f"{_svg_text(180, 150, "Safe", 'hero-strong', 'middle')}"
        + _card(360, 48, 380, 64, labels[0], accent)
        + _card(360, 128, 380, 64, labels[1], "#22C55E")
        + _card(360, 208, 380, 64, labels[2], "#F5B942")
    )


def _hero_meters(labels, accent):
    heights = (150, 110, 80, 130)
    colors = ("#22C55E", "#6366F1", "#F5B942", "#0F9B8E")
    body = []
    for i, h in enumerate(heights):
        x = 70 + i * 120
        body.append(f'<rect x="{x}" y="{230 - h}" width="64" height="{h}" rx="10" fill="{colors[i]}"/>')
        body.append(_svg_text(x, 258, labels[i % 3][:16], "hero-soft"))
    return "".join(body)


def _hero_desk(labels, accent):
    lines = []
    for i in range(5):
        lines.append(f'<rect x="80" y="{78 + i * 22}" width="{280 - (i % 3) * 40}" height="10" rx="4" fill="#334155"/>')
    return (
        f'<rect x="48" y="40" width="380" height="230" rx="18" fill="#141c33" stroke="{accent}"/>'
        + "".join(lines)
        + _card(460, 56, 280, 190, labels[0], "#22C55E", labels[1])
        + _svg_text(480, 160, labels[2], "hero-soft")
    )


def _hero_machine(labels, accent):
    return (
        f'<rect x="70" y="48" width="360" height="210" rx="18" fill="#141c33" stroke="{accent}"/>'
        f'<rect x="92" y="70" width="316" height="150" rx="8" fill="#0B1220"/>'
        f"{_svg_text(110, 110, labels[0], 'hero-strong')}"
        f"{_svg_text(110, 140, labels[1], 'hero-soft')}"
        f"{_svg_text(110, 170, 'localhost', 'hero-kicker')}"
        f'<rect x="150" y="258" width="200" height="12" rx="6" fill="#334155"/>'
        + _card(480, 80, 260, 160, labels[2], "#F5B942", "weights stay here")
    )


def _hero_balance(labels, accent):
    return (
        _card(40, 50, 340, 210, labels[0], accent, labels[1])
        + f'<rect x="60" y="140" width="200" height="18" rx="8" fill="{accent}"/>'
        + f'<rect x="60" y="170" width="120" height="18" rx="8" fill="#22C55E"/>'
        + _card(420, 50, 340, 210, labels[2], "#6366F1", "same tasks")
        + '<rect x="440" y="150" width="160" height="18" rx="8" fill="#6366F1"/>'
    )


def _hero_speech(labels, accent):
    return (
        f'<rect x="40" y="40" width="300" height="70" rx="16" fill="#6366F1"/>'
        f"{_svg_text(58, 82, 'System · ' + labels[0], 'hero-on')}"
        f'<rect x="180" y="130" width="340" height="70" rx="16" fill="#141c33" stroke="{accent}"/>'
        f"{_svg_text(198, 172, 'User · ' + labels[1], 'hero-strong')}"
        f'<rect x="80" y="220" width="420" height="70" rx="16" fill="#141c33" stroke="#F5B942"/>'
        f"{_svg_text(98, 262, 'Tool · ' + labels[2], 'hero-strong')}"
    )


def _hero_bits(labels, accent):
    return (
        f'<rect x="40" y="70" width="220" height="150" rx="16" fill="#141c33" stroke="#94A3B8"/>'
        f"{_svg_text(60, 110, '16-bit', 'hero-soft')}"
        f"{_svg_text(60, 150, labels[0], 'hero-strong')}"
        f'<rect x="290" y="90" width="170" height="120" rx="16" fill="#141c33" stroke="{accent}"/>'
        f"{_svg_text(308, 140, '8-bit', 'hero-kicker')}"
        f"{_svg_text(308, 170, labels[1], 'hero-strong')}"
        f'<rect x="490" y="110" width="250" height="90" rx="16" fill="#141c33" stroke="#F5B942"/>'
        f"{_svg_text(508, 150, '4-bit', 'hero-kicker')}"
        f"{_svg_text(508, 178, labels[2], 'hero-strong')}"
    )


def _hero_gate(labels, accent):
    return (
        f'<polygon points="160,40 280,130 160,230 40,130" fill="#141c33" stroke="{accent}" stroke-width="2"/>'
        f"{_svg_text(160, 136, 'Gate', 'hero-strong', 'middle')}"
        + _card(340, 48, 400, 70, labels[0], "#22C55E")
        + _card(340, 140, 400, 70, labels[1], "#F5B942")
        + _svg_text(360, 250, labels[2], "hero-soft")
    )


def _hero_folder(labels, accent):
    return (
        f'<path d="M40 90 H180 L210 60 H460 V280 H40 Z" fill="#141c33" stroke="{accent}" stroke-width="2"/>'
        f"{_svg_text(70, 140, labels[0], 'hero-strong')}"
        f"{_svg_text(70, 176, labels[1], 'hero-soft')}"
        f"{_svg_text(70, 212, labels[2], 'hero-soft')}"
        f'<circle cx="620" cy="160" r="70" fill="#141c33" stroke="#22C55E" stroke-width="3"/>'
        f'<path d="M586 162 L610 186 L658 134" fill="none" stroke="#22C55E" stroke-width="8" stroke-linecap="round"/>'
    )


def _hero_search(labels, accent):
    dots = [(120, 180), (150, 140), (180, 200), (200, 150), (480, 90), (520, 120), (450, 130), (640, 220), (690, 190), (660, 240)]
    colors = ["#0F9B8E", "#0F9B8E", "#0F9B8E", "#0F9B8E", "#6366F1", "#6366F1", "#6366F1", "#F5B942", "#F5B942", "#F5B942"]
    body = [f'<circle cx="{x}" cy="{y}" r="8" fill="{color}"/>' for (x, y), color in zip(dots, colors)]
    body.append(f'<circle cx="150" cy="170" r="46" fill="none" stroke="{accent}" stroke-width="2"/>')
    body.append(_svg_text(80, 250, labels[0], "hero-soft"))
    body.append(_svg_text(430, 180, labels[1], "hero-soft"))
    body.append(_svg_text(600, 280, labels[2], "hero-soft"))
    return "".join(body)


def _hero_route(labels, accent):
    return (
        f'<path d="M60 250 C 180 250, 180 80, 320 80 S 500 250, 740 120" fill="none" stroke="{accent}" stroke-width="4" class="hero-flow"/>'
        f'<circle cx="60" cy="250" r="12" fill="#6366F1"/>'
        f'<circle cx="320" cy="80" r="12" fill="#0F9B8E"/>'
        f'<circle cx="520" cy="200" r="12" fill="#F5B942"/>'
        f'<circle cx="740" cy="120" r="12" fill="#22C55E"/>'
        f"{_svg_text(40, 280, labels[0], 'hero-soft')}"
        f"{_svg_text(280, 64, labels[1], 'hero-soft')}"
        f"{_svg_text(560, 240, labels[2], 'hero-soft')}"
    )


def plate_svg(kind: str, art_id: str, title: str, rows: list[str], note: str) -> str:
    if kind not in PLATES:
        raise SystemExit(f"Unknown plate {kind}")
    drawer = {
        "pipeline": _plate_pipeline,
        "layers": _plate_layers,
        "compare": _plate_compare,
        "cycle": _plate_cycle,
        "funnel": _plate_funnel,
        "gates": _plate_gates,
        "bars": _plate_bars,
        "scatter": _plate_scatter,
        "split": _plate_split,
        "stack": _plate_stack,
    }[kind]
    height, body = drawer(rows)
    note_y = height - 28
    return (
        f'<svg class="fig plate-svg" data-art="plate-{esc(art_id)}" viewBox="0 0 800 {height}" role="img" '
        f'aria-label="{esc(title)}">{body}'
        f'<text x="24" y="{note_y}" class="label">{esc(note[:180])}</text></svg>'
    )


def _plate_pipeline(rows: list[str]) -> tuple[int, str]:
    shown = rows[:6]
    n = len(shown)
    gap = 12
    w = (760 - gap * (n - 1)) / n
    body = []
    for i, row in enumerate(shown):
        x = 20 + i * (w + gap)
        body.append(f'<rect x="{x:.1f}" y="36" width="{w:.1f}" height="84" rx="12" class="node"/>')
        body.append(f'<text class="nt" x="{x + w / 2:.1f}" y="84" text-anchor="middle">{esc(_wrap(row, 16)[0])}</text>')
        if i:
            body.append(f'<line x1="{x - gap:.1f}" y1="78" x2="{x:.1f}" y2="78" class="edge"/>')
    return 160, "".join(body)


def _plate_layers(rows: list[str]) -> tuple[int, str]:
    body = []
    shown = rows[:6]
    for i, row in enumerate(shown):
        y = 24 + i * 58
        body.append(f'<rect x="80" y="{y}" width="640" height="48" rx="12" class="node {"node-hot" if i == len(shown) - 1 else ""}"/>')
        body.append(f'<text class="nt" x="104" y="{y + 30}">{esc(row[:64])}</text>')
    return 40 + len(shown) * 58 + 50, "".join(body)


def _plate_stack(rows: list[str]) -> tuple[int, str]:
    return _plate_layers(rows)


def _plate_compare(rows: list[str]) -> tuple[int, str]:
    body = ['<rect x="24" y="28" width="360" height="180" rx="14" class="node"/>',
            '<rect x="416" y="28" width="360" height="180" rx="14" class="node node-hot"/>']
    left = rows[0] if rows else ""
    right = rows[1] if len(rows) > 1 else ""
    extra = rows[2] if len(rows) > 2 else ""
    left_lines = _wrap(left, 26)
    right_lines = _wrap(right, 26)
    body.append(f'<text class="nt" x="44" y="78">{esc(left_lines[0])}</text>')
    if len(left_lines) > 1:
        body.append(f'<text class="ns" x="44" y="104">{esc(left_lines[1])}</text>')
    body.append(f'<text class="nt" x="436" y="78">{esc(right_lines[0])}</text>')
    if len(right_lines) > 1:
        body.append(f'<text class="ns" x="436" y="104">{esc(right_lines[1])}</text>')
    body.append(f'<text class="ns" x="44" y="160">{esc(extra[:70])}</text>')
    return 260, "".join(body)


def _plate_cycle(rows: list[str]) -> tuple[int, str]:
    shown = rows[:5]
    cx, cy, radius = 400, 150, 110
    body = []
    for i, row in enumerate(shown):
        angle = -math.pi / 2 + i * (2 * math.pi / len(shown))
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        body.append(f'<rect x="{x - 70:.1f}" y="{y - 24:.1f}" width="140" height="48" rx="12" class="node"/>')
        body.append(f'<text class="nt" x="{x:.1f}" y="{y + 4:.1f}" text-anchor="middle">{esc(_wrap(row, 14)[0])}</text>')
    body.append('<text class="ns" x="400" y="154" text-anchor="middle">repeat with a stop</text>')
    return 300, "".join(body)


def _plate_funnel(rows: list[str]) -> tuple[int, str]:
    body = []
    shown = rows[:5]
    for i, row in enumerate(shown):
        inset = i * 40
        y = 24 + i * 52
        body.append(f'<rect x="{40 + inset}" y="{y}" width="{720 - inset * 2}" height="42" rx="12" class="node"/>')
        body.append(f'<text class="nt" x="400" y="{y + 27}" text-anchor="middle">{esc(row[:48])}</text>')
    return 40 + len(shown) * 52 + 40, "".join(body)


def _plate_gates(rows: list[str]) -> tuple[int, str]:
    body = []
    shown = rows[:4]
    w = 760 / max(1, len(shown))
    for i, row in enumerate(shown):
        x = 16 + i * w
        body.append(f'<rect x="{x:.1f}" y="36" width="{w - 16:.1f}" height="100" rx="14" class="gate"/>')
        for line_i, line in enumerate(_wrap(row, 18)):
            body.append(f'<text class="nt" x="{x + (w - 16) / 2:.1f}" y="{80 + line_i * 20}" text-anchor="middle">{esc(line)}</text>')
    return 200, "".join(body)


def _plate_bars(rows: list[str]) -> tuple[int, str]:
    body = []
    shown = rows[:4]
    for i, row in enumerate(shown):
        if ":" in row:
            label, _, raw = row.rpartition(":")
            try:
                value = max(4, min(100, float(raw)))
            except ValueError:
                label, value = row, 50
        else:
            label, value = row, 50
        y = 28 + i * 36
        body.append(f'<text class="ns" x="20" y="{y + 16}">{esc(label[:28])}</text>')
        body.append(f'<rect x="230" y="{y}" width="420" height="20" rx="6" class="track"/>')
        body.append(f'<rect x="230" y="{y}" width="{4.2 * value:.1f}" height="20" rx="6" class="seg seg-{("a", "b", "c", "d")[i % 4]}"/>')
    return 36 + len(shown) * 36 + 48, "".join(body)


def _plate_scatter(rows: list[str]) -> tuple[int, str]:
    clusters = [
        ((140, 150), (180, 120), (160, 180), (210, 150)),
        ((420, 90), (460, 120), (400, 140)),
        ((560, 200), (620, 180), (600, 230)),
        ((300, 210), (340, 240)),
    ]
    colors = ("#0F9B8E", "#6366F1", "#F5B942", "#22C55E")
    body = ['<rect x="40" y="30" width="620" height="230" rx="12" class="frame"/>']
    for index, points in enumerate(clusters):
        for x, y in points:
            body.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{colors[index]}"/>')
        label = rows[index] if index < len(rows) else ""
        lx, ly = points[0]
        body.append(f'<text class="ns" x="{lx + 12}" y="{ly}">{esc(label[:22])}</text>')
    return 320, "".join(body)


def _plate_split(rows: list[str]) -> tuple[int, str]:
    mid = (len(rows) + 1) // 2
    top, bottom = rows[:mid], rows[mid:]
    body = [
        '<text class="kicker" x="24" y="28">Index once</text>',
        '<text class="kicker" x="24" y="150">Every question</text>',
    ]
    def band(items, y):
        chunks = []
        if not items:
            return chunks
        w = 740 / len(items)
        for i, item in enumerate(items):
            x = 24 + i * w
            chunks.append(f'<rect x="{x:.1f}" y="{y}" width="{w - 12:.1f}" height="64" rx="12" class="node"/>')
            chunks.append(f'<text class="nt" x="{x + (w - 12) / 2:.1f}" y="{y + 38}" text-anchor="middle">{esc(_wrap(item, 14)[0])}</text>')
        return chunks
    body.extend(band(top[:4], 40))
    body.extend(band(bottom[:4], 168))
    return 280, "".join(body)


def walk_figure(art_id: str, heading: str, layout: str, steps: list[tuple[str, str]]) -> str:
    svg = flow_svg(art_id, layout, steps)
    items = []
    for index, (title, caption) in enumerate(steps):
        items.append(
            f'<li><button type="button" data-act="jump" data-i="{index}">'
            f"<strong>{esc(title)}</strong> {esc(caption)}</button></li>"
        )
    total = len(steps) * 4
    return (
        f'<figure class="walk" data-steps="{len(steps)}" data-speed="1" data-step="0" '
        f'aria-label="Animated flow: {esc(heading)}">'
        f'<div class="walk-kicker"><span>Animated flow</span><span>{esc(heading)}</span></div>'
        f'<div class="walk-stage">{svg}</div>'
        f'<div class="walk-bar" role="group" aria-label="Playback">'
        f'<button type="button" class="btn" data-act="prev">Previous step</button>'
        f'<button type="button" class="btn primary" data-act="play"><span class="play-label">Play</span></button>'
        f'<button type="button" class="btn" data-act="next">Next step</button>'
        f'<label class="speed">Speed <select data-act="speed" aria-label="Playback speed">'
        f'<option value="0.5">0.5×</option><option value="1" selected>1×</option>'
        f'<option value="2">2×</option><option value="4">4×</option></select></label>'
        f'<span class="walk-count">Step 1 of {len(steps)}</span>'
        f'<span class="walk-time">0:00 / 0:{total:02d}</span></div>'
        f'<input class="walk-range" data-act="range" type="range" min="0" max="{len(steps) - 1}" value="0" aria-label="Flow timeline"/>'
        f'<p class="walk-caption" aria-live="polite"></p>'
        f'<ol class="walk-script">{"".join(items)}</ol></figure>'
    )
