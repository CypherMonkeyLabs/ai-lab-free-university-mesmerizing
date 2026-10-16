#!/usr/bin/env python3
"""Write the Guide Bot knowledge file from the campus catalog. No invented page text."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "campus" / "assets" / "curriculum" / "catalog.json"
OUT = ROOT / "campus" / "assets" / "guide" / "kb.json"

SECTIONS = (
    {
        "id": "home",
        "href": "#home",
        "title": "Learn",
        "kind": "section",
        "summary": "A lifelong student of systems, networking, voice, and the contact center, studying AI omni-channel agents. The map is prompt, model, retrieval, tools, and an eval gate.",
        "keywords": ["home", "start", "where", "learn", "student", "voice", "contact"],
    },
    {
        "id": "atlas",
        "href": "#atlas",
        "title": "Diagrams",
        "kind": "section",
        "summary": "The room drawings are the 38 files from the study folder. The animated flows are ladders, routing, architecture, deployment, cutover, and a troubleshooting tree drawn for this course.",
        "keywords": ["diagram", "diagrams", "atlas", "picture"],
    },
    {
        "id": "flows",
        "href": "#flows",
        "title": "Flows",
        "kind": "section",
        "summary": "14 call, signal, and data flows. Each picture moves a packet along the study path. Emergency stays on the voice platform. Reduced motion hides the packet.",
        "keywords": ["flow", "flows", "ladder", "animated", "packet"],
    },
    {
        "id": "charts",
        "href": "#charts",
        "title": "Charts",
        "kind": "section",
        "summary": "Every bar is a count from the lesson files in this build. Nothing here is a vendor dashboard.",
        "keywords": ["chart", "charts", "count", "counts"],
    },
    {
        "id": "downloads",
        "href": "#downloads",
        "title": "Cheat Codes",
        "kind": "section",
        "summary": "10 topic sheets, each as HTML, PDF, PNG, and SVG, plus a flashcard JSON of 400 cards and a printable flashcard PDF. The zip is the full offline campus.",
        "keywords": ["cheat", "cheats", "sheet", "sheets", "download", "pdf", "png"],
    },
    {
        "id": "play",
        "href": "#play",
        "title": "Play",
        "kind": "section",
        "summary": "Browser labs for prompts, retrieval, tools, and evals. No key is required to read them.",
        "keywords": ["play", "playground", "lab", "labs"],
    },
    {
        "id": "school-EX",
        "href": "#school-EX",
        "title": "Ecosystem",
        "kind": "section",
        "summary": "Map sister systems, ports, cutovers, and the claims this course will not certify.",
        "keywords": ["ecosystem", "sister", "port", "cutover", "voice", "contact"],
    },
    {
        "id": "EX-11",
        "href": "#EX-11",
        "title": "Licensing, certification, and a career path",
        "kind": "section",
        "summary": "This course issues no certificate. Vendor exams change. The portfolio that matters is a trace, a task set, and a written gate.",
        "keywords": ["career", "careers", "certificate", "interview"],
    },
)

QUIZZES = (
    {
        "prompt": "Which page says fluency is not a source of record?",
        "choices": [
            {"id": "01-01", "label": "A model predicts the next token"},
            {"id": "01-05", "label": "Hallucination is fluent text without evidence"},
            {"id": "09-01", "label": "An eval is a versioned test, not a feeling"},
        ],
        "answer": "01-01",
    },
    {
        "prompt": "Which page says to catch fluent text without evidence by using sources, tools, and tests?",
        "choices": [
            {"id": "01-05", "label": "Hallucination is fluent text without evidence"},
            {"id": "00-01", "label": "How to use this campus"},
            {"id": "06-01", "label": "An agent is a loop with a stop rule"},
        ],
        "answer": "01-05",
    },
    {
        "prompt": "Which page says retrieval finds passages first, then asks the model to answer from those passages?",
        "choices": [
            {"id": "05-01", "label": "Retrieve when the answer has to come from a source"},
            {"id": "01-01", "label": "A model predicts the next token"},
            {"id": "09-01", "label": "An eval is a versioned test, not a feeling"},
        ],
        "answer": "05-01",
    },
    {
        "prompt": "Which page says an agent may call a tool, read the result, and repeat until an answer or a cap?",
        "choices": [
            {"id": "06-01", "label": "An agent is a loop with a stop rule"},
            {"id": "05-01", "label": "Retrieve when the answer has to come from a source"},
            {"id": "EX-11", "label": "Licensing, certification, and a career path"},
        ],
        "answer": "06-01",
    },
    {
        "prompt": "Which page says this course issues no certificate?",
        "choices": [
            {"id": "EX-11", "label": "Licensing, certification, and a career path"},
            {"id": "00-01", "label": "How to use this campus"},
            {"id": "09-01", "label": "An eval is a versioned test, not a feeling"},
        ],
        "answer": "EX-11",
    },
)

SYNONYMS = {
    "rag": ["retrieval", "retrieve", "passages"],
    "diagram": ["diagrams", "atlas", "picture"],
    "flow": ["flows", "ladder", "packet"],
    "cheat": ["cheats", "sheet", "sheets"],
    "chart": ["charts", "count", "counts"],
    "ecosystem": ["sister", "cutover"],
    "agent": ["agents", "loop", "tool"],
    "eval": ["evals", "test", "score"],
    "mcp": ["protocol"],
    "voice": ["sip", "contact", "call"],
    "career": ["careers", "certificate", "interview"],
    "omni": ["omnichannel", "channel"],
}


def write_guide_kb() -> Path:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    pages = [dict(item) for item in SECTIONS]
    seen = {item["id"] for item in pages}
    for lesson in catalog["lessons"]:
        if lesson["id"] in seen:
            continue
        keywords = ["start", "where", "campus"] if lesson["id"] == "00-01" else []
        pages.append(
            {
                "id": lesson["id"],
                "href": "#" + lesson["id"],
                "title": lesson["title"],
                "kind": "lesson",
                "summary": lesson["summary"],
                "keywords": keywords,
            }
        )
    payload = {
        "synonyms": SYNONYMS,
        "fallback": "I only answer from this lab's pages, and none of them match that. Try a lesson title, or ask about diagrams, flows, charts, cheat sheets, or the ecosystem track.",
        "tours": ["home", "atlas", "flows", "charts", "downloads", "school-EX"],
        "quizzes": list(QUIZZES),
        "pages": pages,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=True, separators=(",", ":")), encoding="utf-8")
    return OUT


if __name__ == "__main__":
    path = write_guide_kb()
    print(f"wrote {path}")
