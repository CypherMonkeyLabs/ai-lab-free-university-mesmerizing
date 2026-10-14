"""Distinct inline illustrations for each lesson. Text comes from that lesson."""

from __future__ import annotations

import html

PALETTE = ("#6366F1", "#0F9B8E", "#F5B942", "#22C55E", "#FB7185", "#38BDF8", "#A78BFA", "#F8FAFC")


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def _clip(text: str, limit: int) -> str:
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def _svg(art_id: str, width: int, height: int, label: str, body: str) -> str:
    return (
        f'<svg class="illu" data-art="{esc(art_id)}" viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="{esc(label)}"><rect width="{width}" height="{height}" rx="16" fill="#0B1220"/>{body}</svg>'
    )


def _footer(width: int, height: int, text: str) -> str:
    return (
        f'<rect x="12" y="{height - 28}" width="{width - 24}" height="18" rx="6" fill="#0c1324"/>'
        f'<text x="20" y="{height - 15}" fill="#C7D2FE" font-size="11" font-family="system-ui,sans-serif">'
        f"{esc(_clip(text, 64))}</text>"
    )


def prompt_card(art_id: str, lesson: str, role: str, body: str, note: str, accent: str) -> str:
    return _svg(
        art_id, 520, 230, f"{role} card for {lesson}",
        f'<text x="20" y="28" fill="{accent}" font-size="12" font-family="system-ui,sans-serif" font-weight="700">{esc(role)}</text>'
        f'<text x="120" y="28" fill="#A8B3C7" font-size="12" font-family="system-ui,sans-serif">{esc(_clip(lesson, 42))}</text>'
        f'<rect x="16" y="42" width="488" height="78" rx="12" fill="#141c33" stroke="{accent}"/>'
        f'<text x="28" y="70" fill="#F8FAFC" font-size="13" font-family="system-ui,sans-serif">{esc(_clip(body, 70))}</text>'
        f'<text x="28" y="92" fill="#A8B3C7" font-size="12" font-family="system-ui,sans-serif">{esc(_clip(note, 72))}</text>'
        f'<text x="20" y="146" fill="#99F6E4" font-size="11" font-family="system-ui,sans-serif">Annotation</text>'
        f'<text x="20" y="168" fill="#F8FAFC" font-size="12" font-family="system-ui,sans-serif">{esc(_clip(note, 78))}</text>'
        + _footer(520, 230, lesson),
    )


def arch_map(art_id: str, lesson: str, nodes: list[str], accent: str) -> str:
    shown = nodes[:5] or [lesson]
    gap = 16
    width = 560
    node_w = (width - 32 - gap * (len(shown) - 1)) / len(shown)
    parts = [f'<text x="16" y="28" fill="#A8B3C7" font-size="12" font-family="system-ui,sans-serif">Components · {esc(_clip(lesson, 36))}</text>']
    for index, name in enumerate(shown):
        x = 16 + index * (node_w + gap)
        parts.append(
            f'<rect x="{x:.0f}" y="48" width="{node_w:.0f}" height="72" rx="12" fill="#141c33" stroke="{accent}"/>'
            f'<text x="{x + 10:.0f}" y="78" fill="#F8FAFC" font-size="12" font-family="system-ui,sans-serif">{esc(_clip(name, 16))}</text>'
            f'<text x="{x + 10:.0f}" y="98" fill="#A8B3C7" font-size="11" font-family="system-ui,sans-serif">{index + 1}</text>'
        )
        if index:
            parts.append(f'<line x1="{x - gap:.0f}" y1="84" x2="{x:.0f}" y2="84" stroke="{accent}" stroke-width="2"/>')
    parts.append(_footer(width, 180, "Architecture map · " + lesson))
    return _svg(art_id, width, 180, "Architecture map for " + lesson, "".join(parts))


def _chrome(title: str, accent: str) -> str:
    return (
        f'<rect x="16" y="16" width="528" height="28" rx="8" fill="#141c33"/>'
        f'<circle cx="32" cy="30" r="4" fill="#FB7185"/><circle cx="46" cy="30" r="4" fill="#F5B942"/>'
        f'<circle cx="60" cy="30" r="4" fill="#22C55E"/>'
        f'<text x="78" y="34" fill="{accent}" font-size="12" font-family="system-ui,sans-serif">{esc(_clip(title, 48))}</text>'
    )


def console_mock(art_id: str, lesson: str, rows: list[tuple[str, str]], accent: str) -> str:
    parts = [_chrome(lesson, accent)]
    for index, (name, detail) in enumerate(rows[:4]):
        y = 56 + index * 32
        parts.append(
            f'<text x="24" y="{y}" fill="{accent}" font-size="12" font-family="ui-monospace,monospace">{esc(_clip(name, 18))}</text>'
            f'<text x="160" y="{y}" fill="#F8FAFC" font-size="12" font-family="system-ui,sans-serif">{esc(_clip(detail, 48))}</text>'
        )
    parts.append(_footer(560, 230, "Console mock · " + lesson))
    return _svg(art_id, 560, 230, lesson, "".join(parts))


def dashboard_mock(art_id: str, lesson: str, cells: list[tuple[str, str]], accent: str) -> str:
    parts = [_chrome(lesson, accent)]
    for index, (name, value) in enumerate(cells[:4]):
        x = 20 + (index % 4) * 132
        parts.append(
            f'<rect x="{x}" y="58" width="120" height="70" rx="12" fill="#141c33" stroke="{accent}"/>'
            f'<text x="{x + 10}" y="82" fill="#A8B3C7" font-size="11" font-family="system-ui,sans-serif">{esc(_clip(name, 14))}</text>'
            f'<text x="{x + 10}" y="108" fill="#F8FAFC" font-size="16" font-family="system-ui,sans-serif">{esc(_clip(value, 12))}</text>'
        )
    parts.append(
        '<text x="20" y="160" fill="#A8B3C7" font-size="12" font-family="system-ui,sans-serif">'
        "Four numbers. A blank cell is not a pass. Sketch labels, not a live score.</text>"
    )
    parts.append(_footer(560, 210, "Dashboard mock · " + lesson))
    return _svg(art_id, 560, 210, lesson, "".join(parts))


def inspector_mock(art_id: str, lesson: str, rows: list[tuple[str, str]], accent: str) -> str:
    parts = [_chrome(lesson, accent)]
    for index, (name, detail) in enumerate(rows[:4]):
        y = 58 + index * 34
        parts.append(
            f'<rect x="20" y="{y - 16}" width="520" height="28" rx="8" fill="#141c33"/>'
            f'<text x="32" y="{y + 2}" fill="{accent}" font-size="12" font-family="system-ui,sans-serif">{esc(_clip(name, 22))}</text>'
            f'<text x="200" y="{y + 2}" fill="#F8FAFC" font-size="12" font-family="system-ui,sans-serif">{esc(_clip(detail, 42))}</text>'
        )
    parts.append(_footer(560, 230, "Inspector trace · " + lesson))
    return _svg(art_id, 560, 230, lesson, "".join(parts))


def note_card(art_id: str, lesson: str, heading: str, body: str, accent: str) -> str:
    return _svg(
        art_id, 480, 160, heading + " for " + lesson,
        f'<rect x="16" y="16" width="8" height="100" rx="4" fill="{accent}"/>'
        f'<text x="36" y="40" fill="{accent}" font-size="13" font-family="system-ui,sans-serif" font-weight="700">{esc(_clip(heading, 40))}</text>'
        f'<text x="36" y="68" fill="#F8FAFC" font-size="13" font-family="system-ui,sans-serif">{esc(_clip(body, 62))}</text>'
        f'<text x="36" y="90" fill="#A8B3C7" font-size="12" font-family="system-ui,sans-serif">{esc(_clip(lesson, 52))}</text>'
        + _footer(480, 160, heading + " · " + lesson),
    )


def spark_card(art_id: str, lesson: str, label: str, values: list[float], accent: str) -> str:
    peak = max(values) or 1
    parts = [
        f'<text x="16" y="28" fill="#A8B3C7" font-size="12" font-family="system-ui,sans-serif">{esc(_clip(label, 42))}</text>',
        '<text x="16" y="48" fill="#99F6E4" font-size="11" font-family="system-ui,sans-serif">Sketch from this lesson. Not a benchmark.</text>',
    ]
    for index, value in enumerate(values):
        h = 8 + (value / peak) * 70
        x = 24 + index * 36
        parts.append(f'<rect x="{x}" y="{130 - h:.0f}" width="22" height="{h:.0f}" rx="5" fill="{accent}" opacity="{0.45 + 0.1 * (index % 4)}"/>')
    parts.append(_footer(480, 180, label + " · " + lesson))
    return _svg(art_id, 480, 180, label + " for " + lesson, "".join(parts))


def compare_card(art_id: str, lesson: str, left: str, right: str, accent: str) -> str:
    return _svg(
        art_id, 520, 180, "Compare for " + lesson,
        f'<text x="20" y="28" fill="#A8B3C7" font-size="12" font-family="system-ui,sans-serif">Before and after · {esc(_clip(lesson, 36))}</text>'
        f'<rect x="16" y="42" width="230" height="80" rx="12" fill="#141c33" stroke="#FB7185"/>'
        f'<text x="28" y="74" fill="#F8FAFC" font-size="13" font-family="system-ui,sans-serif">{esc(_clip(left, 28))}</text>'
        f'<rect x="270" y="42" width="230" height="80" rx="12" fill="#141c33" stroke="{accent}"/>'
        f'<text x="282" y="74" fill="#F8FAFC" font-size="13" font-family="system-ui,sans-serif">{esc(_clip(right, 28))}</text>'
        + _footer(520, 180, "Compare · " + lesson),
    )


def data_card(art_id: str, lesson: str, pairs: list[tuple[str, str]], accent: str) -> str:
    parts = [f'<text x="16" y="28" fill="{accent}" font-size="12" font-family="system-ui,sans-serif">Data this lesson keeps</text>']
    for index, (label, value) in enumerate(pairs[:4]):
        y = 54 + index * 24
        parts.append(
            f'<text x="20" y="{y}" fill="#A8B3C7" font-size="12" font-family="system-ui,sans-serif">{esc(_clip(label, 16))}</text>'
            f'<text x="160" y="{y}" fill="#F8FAFC" font-size="12" font-family="system-ui,sans-serif">{esc(_clip(value, 42))}</text>'
        )
    parts.append(_footer(520, 180, "Data card · " + lesson))
    return _svg(art_id, 520, 180, "Data card for " + lesson, "".join(parts))


def timeline_card(art_id: str, lesson: str, steps: list[str], accent: str) -> str:
    parts = [f'<text x="16" y="28" fill="{accent}" font-size="12" font-family="system-ui,sans-serif">Step order · {esc(_clip(lesson, 36))}</text>']
    for index, name in enumerate(steps[:5]):
        y = 52 + index * 28
        parts.append(
            f'<circle cx="32" cy="{y - 4}" r="8" fill="{accent}"/>'
            f'<text x="32" y="{y}" text-anchor="middle" fill="#0B1220" font-size="10" font-family="system-ui,sans-serif">{index + 1}</text>'
            f'<text x="50" y="{y}" fill="#F8FAFC" font-size="12" font-family="system-ui,sans-serif">{esc(_clip(name, 48))}</text>'
        )
    parts.append(_footer(520, 220, "Timeline · " + lesson))
    return _svg(art_id, 520, 220, "Timeline for " + lesson, "".join(parts))


def permit_card(art_id: str, lesson: str, steps: list[str], accent: str) -> str:
    parts = [
        f'<text x="16" y="26" fill="#A8B3C7" font-size="12" font-family="system-ui,sans-serif">Classify before the loop · {esc(_clip(lesson, 28))}</text>',
        '<rect x="16" y="40" width="150" height="100" rx="12" fill="#141c33" stroke="#22C55E"/>',
        '<text x="28" y="64" fill="#22C55E" font-size="12" font-family="system-ui,sans-serif">Allow</text>',
        '<text x="28" y="86" fill="#F8FAFC" font-size="11" font-family="system-ui,sans-serif">Read-only, inside the cap</text>',
        '<rect x="178" y="40" width="160" height="100" rx="12" fill="#141c33" stroke="#F5B942"/>',
        '<text x="190" y="64" fill="#F5B942" font-size="12" font-family="system-ui,sans-serif">Ask</text>',
        '<text x="190" y="86" fill="#F8FAFC" font-size="11" font-family="system-ui,sans-serif">Send, pay, or delete</text>',
        '<rect x="350" y="40" width="150" height="100" rx="12" fill="#141c33" stroke="#FB7185"/>',
        '<text x="362" y="64" fill="#FB7185" font-size="12" font-family="system-ui,sans-serif">Deny</text>',
        '<text x="362" y="86" fill="#F8FAFC" font-size="11" font-family="system-ui,sans-serif">Everything else</text>',
        f'<text x="16" y="162" fill="#A8B3C7" font-size="12" font-family="system-ui,sans-serif">Unsorted steps from this lesson: {esc(_clip(" · ".join(steps[:3]), 70))}</text>',
    ]
    parts.append(_footer(520, 210, "Permissions · " + lesson))
    return _svg(art_id, 520, 210, "Permission card for " + lesson, "".join(parts))


def response_card(art_id: str, lesson: str, claim: str, check: str, accent: str) -> str:
    return _svg(
        art_id, 520, 210, "Response card for " + lesson,
        f'<text x="20" y="28" fill="{accent}" font-size="12" font-family="system-ui,sans-serif">Response</text>'
        f'<rect x="16" y="40" width="488" height="64" rx="12" fill="#141c33" stroke="{accent}"/>'
        f'<text x="28" y="68" fill="#F8FAFC" font-size="13" font-family="system-ui,sans-serif">{esc(_clip(claim, 68))}</text>'
        f'<text x="20" y="128" fill="#99F6E4" font-size="11" font-family="system-ui,sans-serif">Check that does not ask the model</text>'
        f'<text x="20" y="150" fill="#F8FAFC" font-size="12" font-family="system-ui,sans-serif">{esc(_clip(check, 72))}</text>'
        + _footer(520, 210, "Response card · " + lesson),
    )


def failure_card(art_id: str, lesson: str, name: str, detail: str) -> str:
    return _svg(
        art_id, 520, 180, "Failure card for " + lesson,
        '<rect x="16" y="16" width="488" height="36" rx="10" fill="#3f1d2a"/>'
        '<text x="28" y="40" fill="#FECDD3" font-size="13" font-family="system-ui,sans-serif">Failure to name</text>'
        f'<text x="20" y="80" fill="#F8FAFC" font-size="14" font-family="system-ui,sans-serif">{esc(_clip(name, 60))}</text>'
        f'<text x="20" y="106" fill="#A8B3C7" font-size="12" font-family="system-ui,sans-serif">{esc(_clip(detail, 72))}</text>'
        + _footer(520, 180, "Failure · " + lesson),
    )


def debug_card(art_id: str, lesson: str, lines: list[str], accent: str) -> str:
    parts = [
        f'<text x="16" y="26" fill="{accent}" font-size="12" font-family="ui-monospace,monospace">debug print · {esc(_clip(lesson, 36))}</text>',
    ]
    for index, line in enumerate(lines[:4]):
        y = 54 + index * 26
        parts.append(
            f'<rect x="16" y="{y - 16}" width="488" height="22" rx="6" fill="#141c33"/>'
            f'<text x="24" y="{y}" fill="#99F6E4" font-size="12" font-family="ui-monospace,monospace">{esc(_clip(line, 64))}</text>'
        )
    parts.append(_footer(520, 190, "Debug · " + lesson))
    return _svg(art_id, 520, 190, "Debug card for " + lesson, "".join(parts))


def budget_card(art_id: str, lesson: str, minutes: float, steps: int, accent: str) -> str:
    minute_w = max(24, min(220, minutes * 12))
    step_w = max(24, min(220, steps * 28))
    return _svg(
        art_id, 520, 180, "Length card for " + lesson,
        f'<text x="16" y="28" fill="#A8B3C7" font-size="12" font-family="system-ui,sans-serif">This lesson’s length. Not a score.</text>'
        f'<text x="16" y="62" fill="#F8FAFC" font-size="13" font-family="system-ui,sans-serif">{minutes:g} min</text>'
        f'<rect x="120" y="48" width="{minute_w:.0f}" height="16" rx="8" fill="{accent}"/>'
        f'<text x="16" y="100" fill="#F8FAFC" font-size="13" font-family="system-ui,sans-serif">{steps} steps</text>'
        f'<rect x="120" y="86" width="{step_w:.0f}" height="16" rx="8" fill="#38BDF8"/>'
        + _footer(520, 180, "Length · " + lesson),
    )


def gallery_html(item: dict, spec: dict) -> str:
    lid = item["id"]
    title = item["title"] + " · " + lid
    steps = list(spec["steps"])
    facts = list(spec["facts"])
    rows = list(spec.get("plate_rows") or [step[0] for step in steps])
    accent = PALETTE[sum(ord(char) for char in lid) % len(PALETTE)]
    pictures = []
    roles = ("System", "User", "Tool text", "Check")
    for index, (step_title, caption) in enumerate(steps[:4]):
        fact = facts[index % len(facts)][1]
        pictures.append(prompt_card(
            f"card-{lid}-{index}", title, roles[index % 4], step_title, f"{caption} Fact: {fact}.", accent,
        ))
    pictures.append(arch_map(f"arch-{lid}-a", title, rows, accent))
    pictures.append(arch_map(f"arch-{lid}-b", title, [fact[0] for fact in facts] + [rows[-1]], PALETTE[(ord(lid[-1]) + 3) % len(PALETTE)]))
    trace = [(step_title, caption) for step_title, caption in steps[:4]]
    console_title = "Agent console" if lid[:2] in {"06", "08"} else "Step trace"
    pictures.append(console_mock(f"console-{lid}", console_title + " · " + title, trace, accent))
    cells = []
    for index, (label, value) in enumerate(facts[:4]):
        cells.append((label, _clip(value, 12)))
    while len(cells) < 4:
        cells.append(("Step", str(len(cells) + 1)))
    dash_label = "Eval dashboard" if lid[:2] == "09" else "Number card"
    pictures.append(dashboard_mock(f"dash-{lid}", dash_label + " · " + title, cells, accent))
    if lid[:2] == "07":
        inspector_rows = [
            ("tool", steps[0][0]),
            ("resource", steps[1][0] if len(steps) > 1 else title),
            ("prompt", steps[2][0] if len(steps) > 2 else "template"),
            ("decision", "host approves"),
        ]
        inspector_label = "MCP inspector · " + title
    else:
        inspector_rows = [
            ("step", steps[0][0]),
            ("data", steps[1][0] if len(steps) > 1 else title),
            ("check", steps[2][0] if len(steps) > 2 else "done-check"),
            ("stop", "a person approves send, pay, or delete"),
        ]
        inspector_label = "Check trace · " + title
    pictures.append(inspector_mock(f"inspect-{lid}", inspector_label, inspector_rows, accent))
    pictures.append(note_card(f"note-{lid}-a", title, "Failure to name", steps[0][1], "#FB7185"))
    pictures.append(note_card(f"note-{lid}-b", title, "What you save", spec.get("plate_note") or steps[-1][1], "#F5B942"))
    pictures.append(note_card(f"note-{lid}-c", title, "Debug print", "Print the id, the arguments, and the stop for " + steps[0][0], "#22C55E"))
    minutes = float(item.get("minutes") or 8)
    pictures.append(spark_card(f"spark-{lid}-a", title, "Reading minutes, not a score", [minutes, minutes / 2, minutes / 3, max(4, minutes - 2), 6, 8], accent))
    pictures.append(spark_card(f"spark-{lid}-b", title, "Steps in this path", [float(index + 1) for index in range(len(steps))], "#38BDF8"))
    pictures.append(spark_card(
        f"spark-{lid}-c", title, "Facts named in the header",
        [float(10 + len(value)) for _label, value in facts], "#A78BFA",
    ))
    left = steps[0][0]
    right = steps[-1][0]
    pictures.append(compare_card(f"compare-{lid}", title, left, right, accent))
    pictures.append(data_card(f"data-{lid}", title, facts[:4], accent))
    pictures.append(timeline_card(f"time-{lid}", title, [step[0] for step in steps], accent))
    pictures.append(permit_card(f"permit-{lid}", title, [step[0] for step in steps], accent))
    pictures.append(response_card(
        f"reply-{lid}", title, steps[-1][0],
        "A done-check a person can run. Asking the model if it is sure is not a check.",
        accent,
    ))
    pictures.append(failure_card(f"fail-{lid}", title, steps[0][0], steps[0][1]))
    pictures.append(debug_card(
        f"debug-{lid}", title,
        [
            "id " + lid,
            "step " + steps[0][0],
            "arguments printed before the call",
            "stop recorded when the loop ends",
        ],
        accent,
    ))
    pictures.append(budget_card(f"budget-{lid}", title, minutes, len(steps), accent))
    figures = []
    for picture in pictures:
        figures.append(f'<figure class="illu-card">{picture}</figure>')
    return (
        f'<section class="gallery" aria-label="Illustrations for {esc(item["title"])}">'
        f'<p class="gallery-kicker">Pictures for this lesson. Maps, traces, and annotated cards.</p>'
        f'{"".join(figures)}</section>'
    )
