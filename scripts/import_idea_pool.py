#!/usr/bin/env python3
"""Turn the idea-pool pilots into campus lesson, quiz, card, and scenario data.

Reads the byte copy under /cursor/stores/bot/idea-pool/cypher-ai-lab and writes
campus/pool/*.json plus campus/citation_hosts.py. Does not invent facts.
"""

from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/cursor/stores/bot/idea-pool/cypher-ai-lab")
OUT = ROOT / "campus" / "pool"

# Room code -> campus track. Contact-center rooms share a new track because
# the numbered tracks do not teach that system.
SCHOOL = {
    "T1-R01": "01",
    "T1-R03": "01",
    "T2-R01": "02",
    "T2-R03": "02",
    "T2-R07": "02",
    "T3-R01": "05",
    "T3-R04": "05",
    "T4-R01": "06",
    "T4-R09": "06",
    "T5-R01": "09",
    "T5-R06": "04",
    "T5-R07": "09",
    "T6-R01": "10",
    "T7-R01": "14",
    "T7-R02": "14",
    "T7-R07": "14",
    "T8-R01": "11",
    "T8-R03": "14",
    "T8-R08": "14",
}

TRACK_OF_T = {
    "T1": "01",
    "T2": "02",
    "T3": "05",
    "T4": "06",
    "T5": "09",
    "T6": "10",
    "T7": "14",
    "T8": "11",
}

HINTS = (
    ("14", ("whisper", "barge", "contact center", "text-to-speech", "speech", "webrtc", "tts", "asr")),
    ("11", ("owasp", "nist", "gdpr", "privacy", "injection", "pci")),
    ("10", ("lora", "qlora", "distill", "dpo", "rlhf", "fine-tun", "finetun")),
    ("09", ("eval", "golden", "rubric", "opentelemetry", "otel")),
    ("07", ("mcp", "model context protocol")),
    ("06", ("tool call", "idempoten", "agent")),
    ("05", ("retriev", "embedding", "pgvector", "chunk", "rag", "vector")),
    ("04", ("rate limit", "pricing", "latency", "token")),
    ("02", ("prompt", "json schema", "instruction", "structured")),
    ("01", ("temperature", "attention", "softmax", "logit", "transformer")),
)

BLOCK_TAGS = {
    "h1", "h2", "h3", "h4", "p", "ul", "ol", "table", "pre", "details",
    "aside", "figure", "blockquote", "section", "article", "div",
}


class Node:
    def __init__(self, tag: str, attrs: list[tuple[str, str | None]]):
        self.tag = tag
        self.attrs = {key: value or "" for key, value in attrs}
        self.children: list[Node | str] = []


class Dom(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("root", [])
        self.stack = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in {"br", "img", "input", "source", "hr", "wbr"}:
            self.stack.append(node)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                self.stack = self.stack[:index]
                return

    def handle_data(self, data: str) -> None:
        if data:
            self.stack[-1].children.append(data)


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", text.lower())).strip()


def scrub(text: str) -> str:
    text = text.replace("Ravi", "the lab engineer")
    text = text.replace("the lab engineer is a fictional lab engineer", "the lab engineer is fictional")
    text = text.replace("Cypher Monkey", "the author")
    text = text.replace("cypher-monkey", "private-source")
    text = re.sub(
        r"https?://(?:drive\.google\.com|docs\.google\.com|cursor\.com/codebase|origin\.cursor\.com)\S*",
        "[private link removed]",
        text,
    )
    text = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[email removed]", text)
    text = re.sub(r"\b(?:\+?1[-.\s])?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[phone removed]", text)
    return re.sub(r"[ \t]+\n", "\n", text).strip()


def clean(text: str) -> str:
    return scrub(re.sub(r"\s+", " ", text).strip())


def lesson_id(code: str) -> str:
    return f"{SCHOOL[code]}-p-{code.lower().replace('-', '')}"


def room_pointer(href: str, inner: str) -> str:
    match = re.search(r"(T\d-R\d+)", href)
    if not match:
        return inner
    code = match.group(1)
    if code in SCHOOL:
        return f"{inner} (lesson {lesson_id(code)})".strip()
    return f"{inner} (catalog title {code} was not a written room)".strip()


def text_of(node: Node) -> str:
    parts: list[str] = []
    for child in node.children:
        if isinstance(child, str):
            parts.append(child)
            continue
        if child.tag in {"svg", "script", "style", "audio", "input"}:
            continue
        if child.tag == "br":
            parts.append(" ")
            continue
        if child.tag == "img":
            alt = child.attrs.get("alt", "").strip()
            if alt:
                parts.append(alt)
            continue
        if child.tag == "a":
            inner = text_of(child).strip()
            href = child.attrs.get("href", "")
            if href.startswith("http"):
                if inner and inner != href:
                    parts.append(f"{inner} ({href})")
                else:
                    parts.append(href or inner)
            elif "rooms/" in href or href.startswith("../rooms"):
                parts.append(room_pointer(href, inner))
            else:
                parts.append(inner)
            continue
        if child.tag == "code":
            inner = text_of(child).strip()
            if inner:
                parts.append(f"`{inner}`")
            continue
        parts.append(text_of(child))
    return "".join(parts)


def raw_text(node: Node) -> str:
    parts: list[str] = []
    for child in node.children:
        if isinstance(child, str):
            parts.append(child)
        else:
            parts.append(raw_text(child))
    return "".join(parts)


def P(text: str) -> dict:
    return {"t": "p", "text": text}


def H(text: str) -> dict:
    return {"t": "h", "text": text}


def UL(items: list[str]) -> dict:
    return {"t": "ul", "items": items}


def OL(items: list[str]) -> dict:
    return {"t": "ol", "items": items}


def TB(headers: list[str], rows: list[list[str]]) -> dict:
    return {"t": "table", "headers": headers, "rows": rows}


def PRE(text: str) -> dict:
    return {"t": "pre", "text": text}


def NT(title: str, text: str) -> dict:
    return {"t": "note", "title": title, "text": text}


def CK(question: str, answer: str) -> dict:
    return {"t": "check", "q": question, "a": answer}


def walk(node: Node, blocks: list[dict]) -> None:
    tag = node.tag
    if tag in {"svg", "script", "style", "audio", "input", "source"}:
        return
    if tag == "img":
        alt = clean(node.attrs.get("alt", ""))
        if alt:
            blocks.append(P(f"Diagram: {alt}"))
        return
    if tag in {"h1", "h2", "h3", "h4"}:
        title = clean(text_of(node))
        if title:
            blocks.append(H(title))
        return
    if tag == "p":
        text = clean(text_of(node))
        if text:
            blocks.append(P(text))
        return
    if tag in {"ul", "ol"}:
        items = []
        for child in node.children:
            if isinstance(child, Node) and child.tag == "li":
                item = clean(text_of(child))
                if item:
                    items.append(item)
        if items:
            blocks.append(UL(items) if tag == "ul" else OL(items))
        return
    if tag == "pre":
        text = scrub(raw_text(node).strip())
        if text:
            blocks.append(PRE(text))
        return
    if tag == "table":
        headers: list[str] = []
        rows: list[list[str]] = []
        for tr in iter_tag(node, "tr"):
            cells = [clean(text_of(cell)) for cell in direct_cells(tr)]
            cells = [cell for cell in cells if cell or cell == ""]
            if not any(cells):
                continue
            kinds = [cell.tag for cell in direct_cells(tr)]
            if not headers and kinds and all(kind == "th" for kind in kinds):
                headers = cells
                continue
            rows.append(cells)
        if rows:
            width = max(len(headers), max(len(row) for row in rows))
            if not headers:
                headers = [f"Column {index + 1}" for index in range(width)]
            headers = (headers + [""] * width)[:width]
            padded = [(row + [""] * width)[:width] for row in rows]
            blocks.append(TB(headers, padded))
        return
    if tag == "figcaption":
        text = clean(text_of(node))
        if text:
            blocks.append(P(text))
        return
    if tag == "details":
        summary = ""
        inner: list[dict] = []
        for child in node.children:
            if isinstance(child, Node) and child.tag == "summary" and not summary:
                summary = clean(text_of(child))
            elif isinstance(child, Node):
                walk(child, inner)
        if summary:
            blocks.append(H(summary))
        blocks.extend(inner)
        return
    if tag == "aside":
        title = ""
        inner = []
        for child in node.children:
            if isinstance(child, Node) and child.tag == "strong" and not title:
                title = clean(text_of(child))
            elif isinstance(child, Node):
                walk(child, inner)
        if title and inner and inner[0]["t"] == "p":
            blocks.append(NT(title, inner[0]["text"]))
            blocks.extend(inner[1:])
        else:
            if title:
                blocks.append(H(title))
            blocks.extend(inner)
        return
    if tag == "section" and node.attrs.get("id") in {"interview", "hdr"}:
        return
    for child in node.children:
        if isinstance(child, Node):
            walk(child, blocks)


def iter_tag(node: Node, tag: str):
    for child in node.children:
        if isinstance(child, Node):
            if child.tag == tag:
                yield child
            yield from iter_tag(child, tag)


def direct_cells(tr: Node) -> list[Node]:
    cells = []
    for child in tr.children:
        if isinstance(child, Node) and child.tag in {"td", "th"}:
            cells.append(child)
    return cells


def find_section(root: Node, sid: str) -> Node | None:
    for node in iter_tag(root, "section"):
        if node.attrs.get("id") == sid:
            return node
    return None


def lede_of(root: Node) -> str:
    header = find_section(root, "hdr")
    if not header:
        return ""
    for node in iter_tag(header, "p"):
        if "lede" in node.attrs.get("class", ""):
            return clean(text_of(node))
    return ""


def collect_drills(section: Node, code: str) -> list[dict]:
    drills = []
    for article in iter_tag(section, "article"):
        title = ""
        chunks: list[tuple[str, str]] = []
        current = ""
        for child in article.children:
            if not isinstance(child, Node):
                continue
            if child.tag == "h3" and not title:
                title = clean(text_of(child))
            elif child.tag == "h4":
                current = clean(text_of(child))
            elif child.tag == "p" and current:
                chunks.append((current, clean(text_of(child))))
                current = ""
        if not title:
            continue
        blocks = []
        short = ""
        for label, text in chunks:
            blocks.append(H(label))
            blocks.append(P(text))
            if not short:
                short = text
        if not short:
            continue
        blocks.append(CK(title, short))
        drills.append({
            "code": code,
            "title": title,
            "summary": short[:280],
            "blocks": blocks,
        })
    for table in iter_tag(section, "table"):
        for tr in iter_tag(table, "tr"):
            cells = [clean(text_of(cell)) for cell in direct_cells(tr)]
            if len(cells) < 2 or cells[0].lower() in {"prompt", "question"}:
                continue
            prompt, answer = cells[0], cells[1]
            miss = cells[2] if len(cells) > 2 else ""
            blocks = [P(answer)]
            if miss:
                blocks.append(P(f"A miss: {miss}"))
            blocks.append(CK(prompt, answer))
            drills.append({
                "code": code,
                "title": prompt,
                "summary": answer[:280],
                "blocks": blocks,
            })
    return drills


def extract_quiz(html: str, code: str) -> tuple[list[dict], int]:
    items = []
    skipped = 0
    for art in re.findall(r'<article class="quiz-card">(.*?)</article>', html, flags=re.S):
        question_match = re.search(r"<h3>(.*?)</h3>", art, flags=re.S)
        if not question_match:
            skipped += 1
            continue
        question = clean(re.sub(r"<[^>]+>", " ", question_match.group(1)))
        choices = [clean(re.sub(r"<[^>]+>", " ", li)) for li in re.findall(r"<li>(.*?)</li>", art, flags=re.S)]
        answer_match = re.search(r'<details class="answer">.*?<p>(.*?)</p>', art, flags=re.S)
        why = clean(re.sub(r"<[^>]+>", " ", answer_match.group(1))) if answer_match else ""
        letter = re.match(r"^([A-D])\b", why)
        if not letter or len(choices) < 4:
            skipped += 1
            continue
        index = ord(letter.group(1)) - ord("A")
        if index >= len(choices):
            skipped += 1
            continue
        correct = choices[index]
        wrongs = [choice for offset, choice in enumerate(choices) if offset != index]
        items.append({
            "id": f"ip-{code.lower()}-q{len(items) + 1}",
            "track": SCHOOL[code],
            "q": question,
            "correct": correct,
            "wrongs": wrongs[:3],
            "why": why,
        })
    return items, skipped


def load_js_array(path: Path, assignment: str) -> list:
    raw = path.read_text(encoding="utf-8")
    raw = raw.split(assignment, 1)[1]
    raw = raw.strip()
    if raw.endswith(";"):
        raw = raw[:-1]
    return json.loads(raw)


def file_track(text: str) -> str:
    folded = text.lower()
    for track, words in HINTS:
        if any(word in folded for word in words):
            return track
    return "01"


def hours_to_minutes(label: str) -> int:
    match = re.search(r"([\d.]+)", label)
    if not match:
        return 45
    return int(round(float(match.group(1)) * 60))


def existing_norms() -> tuple[set[str], set[str], set[str], dict[str, dict]]:
    from campus.lessons_apply import LESSONS as apply_lessons
    from campus.lessons_core import LESSONS as core_lessons
    from campus.lessons_ref import LESSONS as ref_lessons
    from campus.quiz_bank import AUTHORED

    questions = set()
    cards = set()
    terms: dict[str, dict] = {}
    interviews = set()
    for item in core_lessons + apply_lessons + ref_lessons:
        if item["school"] == "GL":
            terms[norm(item["title"])] = item
        if item["school"] == "IV":
            interviews.add(norm(item["title"]))
        for block in item["blocks"]:
            if block.get("t") == "check":
                questions.add(norm(block["q"]))
                cards.add(norm(block["q"]))
    for row in AUTHORED:
        questions.add(norm(row[3]))
    return questions, cards, interviews, terms


def main() -> None:
    catalog = json.loads((SOURCE / "data" / "catalog.json").read_text(encoding="utf-8"))
    meta = {}
    planned = []
    for track in catalog["tracks"]:
        for room in track["rooms"]:
            code, _slug, title, status, level, hours, blurb = room
            if status == "pilot":
                meta[code] = {
                    "title": title,
                    "level": {"L1": "core", "L2": "practice", "L3": "advanced"}.get(level, "practice"),
                    "minutes": hours_to_minutes(hours),
                    "blurb": blurb,
                }
            else:
                planned.append(code)

    questions, card_norms, interview_norms, terms = existing_norms()
    lessons = []
    drills_out = []
    quiz = []
    folds = []
    hosts: set[str] = set()
    skipped_quiz = 0
    drill_index = 0
    drill_by_title: dict[str, dict] = {}
    source_urls: set[str] = set()

    for code in SCHOOL:
        html = (SOURCE / "content" / f"{code}.body.html").read_text(encoding="utf-8")
        html += "\n" + (SOURCE / "content" / f"{code}.tail.html").read_text(encoding="utf-8")
        source_urls.update(re.findall(r"https?://[^\s\"'<>)]+", html))
        parser = Dom()
        parser.feed(f"<div>{html}</div>")
        parser.close()
        blocks: list[dict] = []
        note = (
            "Source note: last-verified was left unmarked until a person checks the cited pages. "
            "The citation list in this lesson keeps the page and the fetch date."
        )
        blocks.append(NT("Verification", note))
        lede = lede_of(parser.root)
        info = meta[code]
        if lede:
            blocks.append(P(lede))
        for child in parser.root.children:
            if isinstance(child, Node):
                walk(child, blocks)
        interview = find_section(parser.root, "interview")
        found = collect_drills(interview, code) if interview else []
        pointers = []
        for drill in found:
            key = norm(drill["title"])
            if key in interview_norms:
                prior = drill_by_title.get(key)
                if prior:
                    check = prior["blocks"].pop()
                    prior["blocks"].append(H(f"Also answered in {code}"))
                    prior["blocks"].extend(block for block in drill["blocks"] if block["t"] != "check")
                    prior["blocks"].append(check)
                    pointers.append(f"{drill['title']} — {prior['id']}")
                continue
            drill_index += 1
            ident = f"IV-p{drill_index:03d}"
            interview_norms.add(key)
            questions.add(norm(drill["blocks"][-1]["q"]))
            record = {
                "id": ident,
                "school": "IV",
                "level": "practice",
                "minutes": 6,
                "title": drill["title"],
                "summary": drill["summary"],
                "blocks": drill["blocks"],
            }
            drills_out.append(record)
            drill_by_title[key] = record
            pointers.append(f"{drill['title']} — {ident}")
        if pointers:
            blocks.append(H("Interview answers"))
            blocks.append(P(
                "The spoken answers for this room are in Interview practice. "
                "Each line names the question and the lesson that holds the answer."
            ))
            blocks.append(UL(pointers))
        room_quiz, missed = extract_quiz(html, code)
        skipped_quiz += missed
        for item in room_quiz:
            if norm(item["q"]) in questions:
                continue
            if len(item["wrongs"]) < 3:
                skipped_quiz += 1
                continue
            questions.add(norm(item["q"]))
            quiz.append(item)
        if not blocks:
            raise SystemExit(f"{code} produced no blocks")
        lessons.append({
            "id": lesson_id(code),
            "school": SCHOOL[code],
            "level": info["level"],
            "minutes": info["minutes"],
            "title": info["title"],
            "summary": lede or info["blurb"],
            "blocks": blocks,
        })

    glossary = json.loads((SOURCE / "data" / "glossary.json").read_text(encoding="utf-8"))
    gloss_added = 0
    gloss_folded = 0
    for index, entry in enumerate(glossary, start=1):
        term = clean(entry["term"])
        blurb = clean(entry["blurb"])
        key = norm(term)
        href = entry.get("href", "")
        pointer = room_pointer(href, "Cited from the written room.") if "rooms/" in href else ""
        if "labs/" in href:
            pointer = "The zero-key playground on this campus is the place to try the mechanism."
        if key in terms:
            existing = terms[key]
            blob = " ".join(
                str(value) for block in existing["blocks"] for value in block.values() if isinstance(value, str)
            )
            if norm(blurb) not in norm(blob):
                extra = blurb if not pointer else f"{blurb} {pointer}"
                folds.append({"id": existing["id"], "title": "Also cited", "text": extra})
                gloss_folded += 1
            continue
        blocks = [P(blurb)]
        if pointer:
            blocks.append(P(pointer))
        blocks.append(CK(f"How does this course use “{term}”?", blurb))
        ident = f"GL-p{index:03d}"
        lessons.append({
            "id": ident,
            "school": "GL",
            "level": "core",
            "minutes": 4,
            "title": term[:1].upper() + term[1:] if term else term,
            "summary": blurb,
            "blocks": blocks,
        })
        terms[key] = lessons[-1]
        gloss_added += 1

    lessons.extend(drills_out)

    bank = load_js_array(SOURCE / "data" / "quiz-bank.js", "window.CYPHER_QUIZ =")
    bank_added = 0
    for offset, item in enumerate(bank):
        question = clean(item["q"])
        if norm(question) in questions:
            continue
        choices = [clean(choice) for choice in item["choices"]]
        answer = int(item["answer"])
        if answer < 0 or answer >= len(choices):
            skipped_quiz += 1
            continue
        correct = choices[answer]
        wrongs = [choice for index, choice in enumerate(choices) if index != answer]
        if len(wrongs) < 3:
            skipped_quiz += 1
            continue
        questions.add(norm(question))
        quiz.append({
            "id": f"ip-bank-{offset + 1}",
            "track": file_track(question + " " + item.get("why", "")),
            "q": question,
            "correct": correct,
            "wrongs": wrongs[:3],
            "why": clean(item.get("why", "")) or correct,
        })
        bank_added += 1

    cards_raw = load_js_array(SOURCE / "data" / "flashcards.js", "window.CYPHER_CARDS =")
    cards = []
    for card in cards_raw:
        front = clean(card["front"])
        back = clean(card["back"])
        if norm(front) in card_norms:
            continue
        card_norms.add(norm(front))
        track = TRACK_OF_T.get(card.get("track", ""), "01")
        cards.append({
            "id": f"pool-{card['id']}",
            "lesson": next(lesson["id"] for lesson in lessons if lesson["school"] == track and lesson["id"].startswith(f"{track}-p-")),
            "title": card.get("track", track),
            "q": front,
            "a": back,
        })

    scenarios = load_js_array(SOURCE / "data" / "scenarios.js", "window.CYPHER_SCENARIOS =")
    scenario_out = []
    for item in scenarios:
        choices = []
        for choice in item["choices"]:
            choices.append({
                "label": clean(choice["label"]),
                "ok": bool(choice["ok"]),
                "why": clean(choice["why"]),
            })
        scenario_out.append({
            "id": item["id"],
            "title": clean(item["title"]),
            "symptom": clean(item["symptom"]),
            "cite": clean(item["cite"]),
            "choices": choices,
        })

    blob = json.dumps({"lessons": lessons, "quiz": quiz, "cards": cards, "scenarios": scenario_out, "folds": folds})
    for url in re.findall(r"https?://[^\s\"'\\]+", blob):
        host = re.sub(r"^https?://", "", url).split("/")[0].split(":")[0].lower()
        if host.startswith("www."):
            host = host[4:]
        if host in {"cursor.com", "drive.google.com", "docs.google.com", "origin.cursor.com"}:
            raise SystemExit(f"private host survived scrub: {host}")
        hosts.add(host)
    if "[email removed]" in blob or "[phone removed]" in blob or "[private link removed]" in blob:
        pass
    if re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", blob):
        raise SystemExit("email survived scrub")
    folded = blob.lower().replace("-", "")
    if "Ravi" in blob or ("cypher" + "monkey") in folded:
        raise SystemExit("personal token survived scrub")

    kept_urls = []
    missing_urls = []
    for url in sorted(source_urls):
        if any(part in url for part in ("cursor.com", "drive.google.com", "docs.google.com")):
            continue
        if url in blob:
            kept_urls.append(url)
        else:
            missing_urls.append(url)

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "lessons.json").write_text(json.dumps(lessons, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "quiz.json").write_text(json.dumps(quiz, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "cards.json").write_text(json.dumps(cards, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "scenarios.json").write_text(json.dumps(scenario_out, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "folds.json").write_text(json.dumps(folds, ensure_ascii=False, indent=1), encoding="utf-8")
    host_lines = "\n".join(f"    {json.dumps(host)}," for host in sorted(hosts))
    (ROOT / "campus" / "citation_hosts.py").write_text(
        '"""Hosts named in imported citations. The page may show these URLs as text."""\n\n'
        "from __future__ import annotations\n\n"
        "import re\n\n"
        "HOSTS = frozenset({\n"
        f"{host_lines}\n"
        "})\n\n\n"
        "def url_allowed(url: str) -> bool:\n"
        "    if \"w3.org\" in url or \"127.0.0.1\" in url:\n"
        "        return True\n"
        "    if url.startswith(\"https://github.com/cipher0x9/\"):\n"
        "        return True\n"
        "    if url.startswith(\"https://cipher0x9.github.io/ai-lab-free-university-mesmerizing/\"):\n"
        "        return True\n"
        "    host = re.sub(r\"^https?://\", \"\", url).split(\"/\")[0].split(\":\")[0].lower()\n"
        "    if host.startswith(\"www.\"):\n"
        "        host = host[4:]\n"
        "    return host in HOSTS\n",
        encoding="utf-8",
    )
    stats = {
        "rooms": len(SCHOOL),
        "planned_skipped": planned,
        "glossary_added": gloss_added,
        "glossary_folded": gloss_folded,
        "glossary_source": len(glossary),
        "drills": len(drills_out),
        "quiz": len(quiz),
        "quiz_bank_added": bank_added,
        "quiz_bank_source": len(bank),
        "quiz_without_choices_or_duplicate": skipped_quiz,
        "cards": len(cards),
        "cards_source": len(cards_raw),
        "scenarios": len(scenario_out),
        "citation_urls_kept": len(kept_urls),
        "citation_urls_missing": missing_urls[:30],
        "citation_urls_missing_count": len(missing_urls),
        "lessons_added": len(lessons),
        "hosts": sorted(hosts),
    }
    (OUT / "stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
