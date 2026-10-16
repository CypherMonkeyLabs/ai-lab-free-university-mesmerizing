"""Printable cheat sheets. HTML, a text PDF, and an SVG poster. No remote hosts."""

from __future__ import annotations

import json
import struct
import zlib
from pathlib import Path

from campus.chrome import CONTACT, COPYRIGHT, DISCLAIMER, ISSUES, REPO, brand_nav, esc

ROOT = Path(__file__).resolve().parents[1]
CAMPUS_OUT = ROOT / "campus" / "assets" / "cheats"
DOWNLOAD_OUT = ROOT / "downloads" / "cheats"

SHEETS = (
    (
        "ports-protocols",
        "Ports and protocols",
        [
            "Study matrix. Confirm every listener on the host you run.",
            "443 TCP — HTTPS to a model API. Confirm the vendor host.",
            "53 UDP/TCP — DNS.",
            "4317 TCP — OTLP gRPC. OpenTelemetry default. Not re-fetched 2026-10-15.",
            "4318 TCP — OTLP HTTP. OpenTelemetry default. Not re-fetched 2026-10-15.",
            "11434 TCP — Ollama's published loopback default. Not re-fetched 2026-10-15.",
            "5060 UDP/TCP — SIP, RFC 3261. Confirm the listener.",
            "5061 TCP — SIP over TLS, commonly assigned. Confirm in the IANA registry.",
            "RTP — a range you configure, not one universal port.",
            "MCP stdio — no port. Remote MCP is HTTP on a port you choose.",
            "Sources: RFC 3261, OpenTelemetry OTLP spec, MCP specification 2025-06-18, Ollama docs, IANA service names.",
        ],
    ),
    (
        "call-flows",
        "Call and data flows",
        [
            "Voice, study order: caller, SIP, media, ASR, turn, retrieval, model, TTS, media, caller.",
            "Emergency leaves that list. The voice platform's emergency path is the path.",
            "Retrieval, study order: documents you may store, chunks, one embedding id, retrieve, rerank, cite or refuse, then the model.",
            "Agent, study order: goal, schema, permission, tool result, trace, stop.",
            "A person sits on send, pay, delete, and cutover.",
        ],
    ),
    (
        "config-checklist",
        "Configuration checklist",
        [
            "Pin the model id and the embedding id.",
            "Keep the key out of the repository.",
            "Bind a local runner to loopback until you mean to share it.",
            "Set a timeout and a retry cap that cannot double-send.",
            "Log ids and counts. Drop the key and the raw private text.",
            "Name the kill switch and the old path.",
        ],
    ),
    (
        "troubleshooting",
        "Troubleshooting tree",
        [
            "No trace: stop and add one.",
            "Wrong fact: was the span in the pack? If not, refuse or fix the index.",
            "Tool error: the model is quoting your handler.",
            "Should have refused: the gate failed, not the tone.",
            "Slow phone turn: time ASR, model, and TTS separately.",
            "Change one thing. Rescore the same tasks.",
        ],
    ),
    (
        "migration",
        "Migration and cutover",
        [
            "Inventory the old bot's answers and their allowed sources.",
            "Write ten tasks, including a refusal.",
            "Shadow mode: users still see the old bot.",
            "Limited audience, kill switch tested, then a wider cut.",
            "Retire the old bot only after its tasks stay in the eval set.",
        ],
    ),
    (
        "security-gates",
        "Security gates",
        [
            "Retrieved text is untrusted.",
            "A debug log is a database.",
            "Card, health, and children's data follow the regime that applies. This sheet is not that regime.",
            "NIST AI RMF and OWASP GenAI are starting readings, not certificates.",
            "This course is not legal advice.",
        ],
    ),
    (
        "eval-card",
        "Eval scorecard",
        [
            "Same tasks. Version the file.",
            "Quality: a pass rule you wrote before the run.",
            "Safety: count failures. More is worse.",
            "Latency and cost on the same card.",
            "Compare to the baseline. A gate a person owns.",
        ],
    ),
    (
        "glossary-card",
        "Glossary card",
        [
            "Token: a chunk the model reads or writes. Not always a word.",
            "Context window: one budget shared by instructions, sources, and the answer.",
            "Retrieval: find a span, then generate. Cite the id.",
            "Tool schema: name, arguments, and your handler.",
            "Eval gate: quality, safety, latency, cost.",
            "The full glossary is the Glossary track in the campus.",
        ],
    ),
    (
        "read-a-ladder",
        "How to read a ladder",
        [
            "Columns are the parties. Time runs downward.",
            "An arrow is one message. The label is the study claim, not a packet capture.",
            "The moving dot is a reading aid. It is not traffic from a live system.",
            "Emergency arrows stop on the voice platform.",
            "The room diagrams are the 38 study-draft files. They were not redrawn from a fresh vendor doc.",
        ],
    ),
    (
        "career-path",
        "Career path",
        [
            "Explain a token, a window, and a sample without a product name.",
            "Build a grounded assistant on notes you may use, with one read-only tool.",
            "Prove ten tasks: retrieval, safety, latency, and cost.",
            "Interview drills ask for the mechanism, the control, and the evidence.",
            "This sheet is not a certificate. Vendor exams are read from that vendor's current page.",
        ],
    ),
)


def _favicon_links() -> str:
    return (
        '<link rel="icon" href="../../favicon.ico" sizes="any"/>'
        '<link rel="icon" href="../../favicon.svg" type="image/svg+xml"/>'
    )


def _footer() -> str:
    return f"""
<footer class="labfoot">
  <p><strong>CYPHER0X9</strong> · AI Lab Free University</p>
  <p class="copyright">{esc(COPYRIGHT)}</p>
  {brand_nav()}
  <p>{esc(DISCLAIMER)} <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a></p>
  <p><a href="{esc(REPO)}">Repository</a>
     <a href="{esc(ISSUES)}">Rate, comment, or help</a>
     <a href="{esc(CONTACT)}">Report a concern</a>
     <a href="{esc(CONTACT)}">Work with us</a></p>
  <p>No email address is printed on this sheet. Sources are named in the lesson. This is not a copy of a vendor document.</p>
</footer>
"""


def _html(slug: str, title: str, lines: list[str]) -> str:
    items = "".join(f"<li>{esc(line)}</li>" for line in lines)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(title)} · AI Lab cheat sheet</title>
{_favicon_links()}
<style>
body{{font:16px/1.45 system-ui,sans-serif;margin:24px;color:#0f172a;background:#fff}}
h1{{font-size:28px;margin:0 0 8px}}
ol{{max-width:70ch}}
a{{color:#0f766e}}
.brand-links{{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}}
.brand-link{{display:inline-flex;align-items:center;gap:6px;min-height:40px;padding:0 8px;border:1px solid #cbd5e1;border-radius:10px;text-decoration:none;color:#0f172a}}
.brand-link svg{{width:18px;height:18px}}
@media print{{a{{color:#000;text-decoration:none}}}}
</style></head><body>
<h1>{esc(title)}</h1>
<p>One page. Print from the browser if you want paper. The PDF beside this file is the same text.</p>
<ol>{items}</ol>
{_footer()}
</body></html>
"""


def _svg(title: str, lines: list[str]) -> str:
    rows = []
    y = 86
    for line in lines:
        rows.append(
            f'<text x="36" y="{y}" fill="#e7f6ff" font-family="system-ui,sans-serif" font-size="16">{esc(line[:90])}</text>'
        )
        y += 28
    height = y + 80
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" viewBox="0 0 900 {height}">'
        f'<rect width="900" height="{height}" fill="#070b16"/>'
        f'<text x="36" y="48" fill="#67e8f9" font-family="system-ui,sans-serif" font-size="28">{esc(title)}</text>'
        + "".join(rows)
        + f'<text x="36" y="{y + 36}" fill="#93b4c9" font-family="system-ui,sans-serif" font-size="14">'
        "cyphermonkeylabs.com · independent study sheet</text></svg>"
    )


def _pdf_line(line: str) -> str:
    safe = (
        line.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("—", "-")
        .replace("…", "...")
    )
    if len(safe) > 90:
        safe = safe[:89] + "..."
    return safe


def _paginate(lines: list[str], per_page: int = 46) -> list[list[str]]:
    pages: list[list[str]] = []
    chunk: list[str] = []
    for line in lines:
        chunk.append(line)
        if len(chunk) >= per_page:
            pages.append(chunk)
            chunk = []
    if chunk or not pages:
        pages.append(chunk)
    return pages


def _pdf_document(pages: list[list[str]]) -> bytes:
    streams = []
    for page in pages:
        commands = ["BT", "/F1 11 Tf", "14 TL", "50 760 Td"]
        first = True
        for line in page:
            safe = _pdf_line(line)
            if first:
                commands.append(f"({safe}) Tj")
                first = False
            else:
                commands.append("T*")
                commands.append(f"({safe}) Tj")
        commands.append("ET")
        streams.append("\n".join(commands).encode("latin-1", errors="replace"))
    count = len(streams)
    font_id = 3 + count * 2
    page_ids = [3 + index * 2 for index in range(count)]
    objects: list[bytes] = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Count " + str(count).encode("ascii") + b" /Kids ["
        + b" ".join(f"{page_id} 0 R".encode("ascii") for page_id in page_ids)
        + b"] >>",
    ]
    for index, stream in enumerate(streams):
        page_id = page_ids[index]
        content_id = page_id + 1
        objects.append(
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents "
            + str(content_id).encode("ascii")
            + b" 0 R /Resources << /Font << /F1 "
            + str(font_id).encode("ascii")
            + b" 0 R >> >> >>"
        )
        objects.append(b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n".encode("ascii") + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode("ascii")
    out += b"0000000000 65535 f \n"
    for offset in offsets[1:]:
        out += f"{offset:010d} 00000 n \n".encode("ascii")
    out += f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode("ascii")
    return bytes(out)


def _wrap_pdf(lines: list[str], width: int = 88) -> list[str]:
    wrapped: list[str] = []
    for line in lines:
        text = line.replace("—", "-").replace("…", "...")
        while len(text) > width:
            cut = text.rfind(" ", 0, width)
            if cut < 24:
                cut = width
            wrapped.append(text[:cut])
            text = text[cut:].lstrip()
        wrapped.append(text)
    return wrapped


def _pdf(title: str, lines: list[str]) -> bytes:
    body = [title, ""] + lines + ["", DISCLAIMER, "cyphermonkeylabs.com", "No email address is printed on this sheet."]
    return _pdf_document(_paginate(_wrap_pdf(body)))


_GLYPHS = """
A 01110 10001 10001 11111 10001 10001 10001
B 11110 10001 10001 11110 10001 10001 11110
C 01110 10001 10000 10000 10000 10001 01110
D 11110 10001 10001 10001 10001 10001 11110
E 11111 10000 10000 11110 10000 10000 11111
F 11111 10000 10000 11110 10000 10000 10000
G 01110 10001 10000 10111 10001 10001 01110
H 10001 10001 10001 11111 10001 10001 10001
I 01110 00100 00100 00100 00100 00100 01110
J 00111 00010 00010 00010 10010 10010 01100
K 10001 10010 10100 11000 10100 10010 10001
L 10000 10000 10000 10000 10000 10000 11111
M 10001 11011 10101 10101 10001 10001 10001
N 10001 11001 10101 10011 10001 10001 10001
O 01110 10001 10001 10001 10001 10001 01110
P 11110 10001 10001 11110 10000 10000 10000
Q 01110 10001 10001 10001 10101 10010 01101
R 11110 10001 10001 11110 10100 10010 10001
S 01111 10000 10000 01110 00001 00001 11110
T 11111 00100 00100 00100 00100 00100 00100
U 10001 10001 10001 10001 10001 10001 01110
V 10001 10001 10001 10001 10001 01010 00100
W 10001 10001 10001 10101 10101 10101 01010
X 10001 10001 01010 00100 01010 10001 10001
Y 10001 10001 01010 00100 00100 00100 00100
Z 11111 00001 00010 00100 01000 10000 11111
0 01110 10001 10011 10101 11001 10001 01110
1 00100 01100 00100 00100 00100 00100 01110
2 01110 10001 00001 00110 01000 10000 11111
3 11110 00001 00001 01110 00001 00001 11110
4 00010 00110 01010 10010 11111 00010 00010
5 11111 10000 11110 00001 00001 10001 01110
6 00110 01000 10000 11110 10001 10001 01110
7 11111 00001 00010 00100 01000 01000 01000
8 01110 10001 10001 01110 10001 10001 01110
9 01110 10001 10001 01111 00001 00010 11100
. 00000 00000 00000 00000 00000 01100 01100
, 00000 00000 00000 00000 01100 01100 01000
: 00000 01100 01100 00000 01100 01100 00000
; 00000 01100 01100 00000 01100 01100 01000
' 00100 00100 01000 00000 00000 00000 00000
- 00000 00000 00000 11111 00000 00000 00000
/ 00001 00010 00100 01000 10000 00000 00000
( 00110 01000 10000 10000 10000 01000 00110
) 01100 00010 00001 00001 00001 00010 01100
? 01110 10001 00001 00010 00100 00000 00100
"""

FONT = {
    parts[0]: tuple(int(bits, 2) for bits in parts[1:])
    for parts in (line.split() for line in _GLYPHS.strip().splitlines())
}


def _png(title: str, lines: list[str]) -> bytes:
    scale = 2
    cell_w = 6 * scale
    cell_h = 8 * scale
    width = 1100
    margin = 28
    columns = (width - margin * 2) // cell_w

    def wrap(text: str) -> list[str]:
        cleaned = text.upper().replace("—", "-").replace("…", "...")
        words = cleaned.split(" ")
        rows: list[str] = []
        current = ""
        for word in words:
            trial = word if not current else current + " " + word
            if len(trial) <= columns:
                current = trial
            else:
                if current:
                    rows.append(current)
                while len(word) > columns:
                    rows.append(word[:columns])
                    word = word[columns:]
                current = word
        if current:
            rows.append(current)
        return rows or [""]

    body = wrap(title) + [""] + [row for line in lines for row in wrap(line)]
    body += ["", *wrap(DISCLAIMER), "CYPHERMONKEYLABS.COM", "NO EMAIL ADDRESS IS PRINTED ON THIS SHEET."]
    height = margin * 2 + len(body) * cell_h + 8
    bg = (7, 11, 22)
    canvas = bytearray(bytes(bg) * (width * height))
    bar = bytes((34, 211, 238)) * width
    for y in range(6):
        start = y * width * 3
        canvas[start:start + width * 3] = bar

    def pixel(x: int, y: int, color: tuple[int, int, int]) -> None:
        if 0 <= x < width and 0 <= y < height:
            offset = (y * width + x) * 3
            canvas[offset:offset + 3] = bytes(color)

    def blit(text: str, top: int, color: tuple[int, int, int]) -> None:
        for index, char in enumerate(text):
            glyph = FONT.get(char)
            if glyph is None:
                continue
            origin_x = margin + index * cell_w
            for row, bits in enumerate(glyph):
                for col in range(5):
                    if bits & (1 << (4 - col)):
                        for dy in range(scale):
                            for dx in range(scale):
                                pixel(origin_x + col * scale + dx, top + row * scale + dy, color)

    for index, row in enumerate(body):
        color = (103, 232, 249) if index == 0 else (147, 180, 201) if index >= len(body) - 3 else (231, 246, 255)
        blit(row, margin + index * cell_h, color)

    raw = b"".join(b"\x00" + bytes(canvas[y * width * 3:(y + 1) * width * 3]) for y in range(height))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")


def write_cheats(cards: list[dict]) -> int:
    CAMPUS_OUT.mkdir(parents=True, exist_ok=True)
    DOWNLOAD_OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for slug, title, lines in SHEETS:
        html_text = _html(slug, title, lines)
        svg_text = _svg(title, lines)
        pdf = _pdf(title, lines)
        png = _png(title, lines)
        for folder in (CAMPUS_OUT, DOWNLOAD_OUT):
            (folder / f"{slug}.html").write_text(html_text, encoding="utf-8")
            (folder / f"{slug}.svg").write_text(svg_text, encoding="utf-8")
            (folder / f"{slug}.pdf").write_bytes(pdf)
            (folder / f"{slug}.png").write_bytes(png)
        count += 1
    deck = {
        "cards": [
            {"id": card["id"], "q": card["q"], "a": card["a"], "why": card.get("why", "")}
            for card in cards[:400]
        ],
        "note": "A printable subset. The campus deck is larger. Not a certificate.",
    }
    payload = json.dumps(deck, ensure_ascii=True, indent=2)
    card_lines = [f"{card['q']} — {card['a']}" for card in deck["cards"][:40]]
    printable = _html("flashcards", "Printable flashcards", card_lines)
    card_pdf = _pdf("Printable flashcards", card_lines)
    for folder in (CAMPUS_OUT, DOWNLOAD_OUT):
        (folder / "flashcards.json").write_text(payload, encoding="utf-8")
        (folder / "flashcards.html").write_text(printable, encoding="utf-8")
        (folder / "flashcards.pdf").write_bytes(card_pdf)
    index_items = "".join(
        f'<li><a href="{esc(slug)}.html">{esc(title)} HTML</a> · '
        f'<a href="{esc(slug)}.pdf">PDF</a> · <a href="{esc(slug)}.png">PNG</a> · '
        f'<a href="{esc(slug)}.svg">SVG</a></li>'
        for slug, title, _lines in SHEETS
    )
    index = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><title>AI Lab cheat codes</title>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
{_favicon_links()}
<style>body{{font:16px/1.5 system-ui,sans-serif;margin:24px;max-width:70ch}}
.brand-links{{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}}
.brand-link{{display:inline-flex;align-items:center;gap:6px;min-height:40px;padding:0 8px;border:1px solid #cbd5e1;border-radius:10px;text-decoration:none}}
.brand-link svg{{width:18px;height:18px}}</style></head>
<body><h1>Cheat codes</h1>
<p>One sheet per topic. HTML to read, PDF to pass along, SVG to drop into a slide you make yourself.</p>
<ul>{index_items}<li><a href="flashcards.html">Flashcards HTML</a> · <a href="flashcards.pdf">PDF</a> · <a href="flashcards.json">JSON</a></li></ul>
{_footer()}
</body></html>
"""
    for folder in (CAMPUS_OUT, DOWNLOAD_OUT):
        (folder / "index.html").write_text(index, encoding="utf-8")
    return count
