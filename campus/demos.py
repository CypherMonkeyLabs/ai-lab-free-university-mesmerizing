"""Zero-key charts and calculators. Course counts are real. Other numbers are labeled sketches."""

from __future__ import annotations

import html
import json
import math
from collections import Counter

from campus.flagship_lessons import LESSONS as ECO_LESSONS
from campus.lessons_apply import LESSONS as APPLY_LESSONS
from campus.lessons_core import LESSONS as CORE_LESSONS
from campus.lessons_ref import LESSONS as REF_LESSONS
from campus.pool import LESSONS as POOL_LESSONS
from campus.schema import SCHOOLS


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def _lessons() -> list[dict]:
    return CORE_LESSONS + APPLY_LESSONS + REF_LESSONS + POOL_LESSONS + ECO_LESSONS


def _softmax(logits: list[float], temperature: float) -> list[float]:
    scaled = [value / temperature for value in logits]
    peak = max(scaled)
    exps = [math.exp(value - peak) for value in scaled]
    total = sum(exps)
    return [value / total for value in exps]


def _gb(billions: float, bits: float) -> float:
    return round(billions * (bits / 8), 2)


def _lora(rank: int, din: int = 4096, dout: int = 4096, layers: int = 32) -> int:
    return 2 * rank * (din + dout) * layers


def _kv_mb(tokens: int) -> float:
    # Sketch: 2 (K and V) * layers * kv heads * head dim * tokens * 2 bytes.
    layers, heads, dim, width = 32, 8, 128, 2
    return round(2 * layers * heads * dim * tokens * width / (1024 * 1024), 1)


def _charts() -> list[dict]:
    lessons = _lessons()
    by_school: dict[str, list[dict]] = {}
    for item in lessons:
        by_school.setdefault(item["school"], []).append(item)
    tracks = [school for school in SCHOOLS if school["kind"] == "track"]
    refs = [school for school in SCHOOLS if school["kind"] == "reference"]
    track_lessons = [{"label": school["id"], "value": len(by_school[school["id"]])} for school in tracks]
    track_minutes = [
        {"label": school["id"], "value": sum(item["minutes"] for item in by_school[school["id"]])}
        for school in tracks
    ]
    levels = Counter(item["level"] for item in lessons)
    level_points = [
        {"label": "Core", "value": levels["core"]},
        {"label": "Practice", "value": levels["practice"]},
        {"label": "Advanced", "value": levels["advanced"]},
    ]
    running = 0
    cumulative = []
    for school in tracks:
        running += len(by_school[school["id"]])
        cumulative.append({"label": school["id"], "value": running})
    minute_hist = Counter(item["minutes"] for item in lessons)
    hist = [{"label": str(minutes), "value": count} for minutes, count in sorted(minute_hist.items())]
    ref_points = [{"label": school["id"], "value": len(by_school[school["id"]])} for school in refs]
    logits = [4.2, 3.1, 1.6, 0.7]
    names = ["the", "cat", "sat", "dog"]
    temp_points = []
    for temperature in (0.2, 0.5, 1.0, 1.5):
        mass = _softmax(logits, temperature)[0]
        temp_points.append({"label": str(temperature), "value": round(mass * 100, 1)})
    topk = []
    full = _softmax(logits, 1)
    for keep in (1, 2, 3, 4):
        chosen = sorted(full, reverse=True)[:keep]
        topk.append({"label": "k=" + str(keep), "value": round(100 * sum(chosen), 1)})
    notes = (
        "The shop accepts returns for 30 days after delivery. "
        "Standard shipping takes 5 business days. "
        "Support never asks for a password."
    )
    chunks = []
    for window in (40, 80, 120, 200):
        chunks.append({"label": str(window), "value": math.ceil(len(notes) / window)})
    hybrid = []
    for weight in (0, 0.25, 0.5, 0.75, 1):
        hybrid.append({"label": str(weight), "value": round(0.2 * (1 - weight) + 0.9 * weight, 2)})
    course_note = "Counted from the lessons in this file. Not a quality score."
    sketch = "Sketch. Not a benchmark and not a price."
    specs = [
        ("chart-track-lessons", "bar", "Lessons in each track", course_note, {"points": track_lessons}),
        ("chart-track-minutes", "bar", "Reading minutes in each track", course_note, {"points": track_minutes}),
        ("chart-levels", "bar", "Lessons by level", course_note, {"points": level_points}),
        ("chart-cumulative", "line", "Cumulative lessons along the tracks", course_note, {"points": cumulative}),
        ("chart-minute-hist", "hist", "How many lessons share a length", course_note, {"points": hist}),
        ("chart-track-order", "timeline", "Track order", course_note, {"points": [{"label": school["id"], "value": index + 1} for index, school in enumerate(tracks)]}),
        ("chart-reference", "bar", "Lessons in the reference sections", course_note, {"points": ref_points}),
        ("chart-level-minutes", "stack", "Minutes by level", course_note, {
            "series": ["Core", "Practice", "Advanced"],
            "points": [{
                "label": "Course",
                "values": [
                    sum(item["minutes"] for item in lessons if item["level"] == "core"),
                    sum(item["minutes"] for item in lessons if item["level"] == "practice"),
                    sum(item["minutes"] for item in lessons if item["level"] == "advanced"),
                ],
            }],
        }),
        ("chart-quant-bits", "bar", "Example 7B weight file at a few bit widths", "Weights only. A 7B Q4 file is about 3.5 GB. The 16 GB figure is a machine starting point, because the runner and KV cache are extra. " + sketch, {
            "points": [{"label": str(bits) + " bit", "value": _gb(7, bits)} for bits in (4, 5, 8, 16)],
        }),
        ("chart-quant-size", "line", "Example Q4 weight file by parameter count", "Formula: billions times bits/8. " + sketch, {
            "points": [{"label": str(size) + "B", "value": _gb(size, 4)} for size in (1, 3, 7, 8)],
        }),
        ("chart-lora-rank", "line", "Example LoRA trainable count versus rank", "2 × rank × (4096 + 4096) × 32 layers. Example dimensions, not a model card. " + sketch, {
            "points": [{"label": "r" + str(rank), "value": _lora(rank)} for rank in (4, 8, 16, 32, 64)],
        }),
        ("chart-lora-share", "bar", "Example adapter versus one full matrix stack", "Full count is 4096 × 4096 × 32. " + sketch, {
            "points": [
                {"label": "LoRA r16", "value": _lora(16)},
                {"label": "Full", "value": 4096 * 4096 * 32},
            ],
        }),
        ("chart-context", "stack", "Example context split", "One shared window. These token counts are an example, not a bill. " + sketch, {
            "series": ["Instructions", "Retrieval", "Chat", "Answer"],
            "points": [{"label": "Example", "values": [800, 2400, 1200, 600]}],
        }),
        ("chart-temperature", "line", "Toy mass on the top logit versus temperature", "Fixed logits 4.2, 3.1, 1.6, 0.7. Temperature does not add facts. " + sketch, {"points": temp_points}),
        ("chart-topk", "bar", "Toy probability kept by top-k", "Same logits at temperature 1, before top-p. " + sketch, {"points": topk}),
        ("chart-rerank", "slope", "Hand-set retrieval score versus rerank score", "A reranker cannot score a passage the first stage never fetched. " + sketch, {
            "left": "Retrieve",
            "right": "Rerank",
            "points": [
                {"label": "notes-01", "a": 0.91, "b": 0.62},
                {"label": "notes-05", "a": 0.33, "b": 0.88},
                {"label": "notes-02", "a": 0.44, "b": 0.21},
            ],
        }),
        ("chart-tokens", "waterfall", "Example token lines on one call", "Counts, not prices. Fill prices from your own card. " + sketch, {
            "points": [
                {"label": "Input", "value": 1200},
                {"label": "Output", "value": 300},
                {"label": "Cache", "value": 400},
                {"label": "Tools", "value": 200},
                {"label": "Retry", "value": 200},
            ],
        }),
        ("chart-funnel", "funnel", "Example eval funnel", "Ten tasks, all scored, two regressions, nothing shipped. Not yet is a finished result. " + sketch, {
            "points": [
                {"label": "Written", "value": 10},
                {"label": "Scored", "value": 10},
                {"label": "Regressions", "value": 2},
                {"label": "Shipped", "value": 0},
            ],
        }),
        ("chart-attention", "heat", "Toy causal attention row", "Hand-drawn pattern, the same kind the attention widget labels as a sketch. Not a model that knows geography.", {
            "cols": ["The", "capital", "of", "France"],
            "rows": ["The", "capital", "of", "France"],
            "grid": [
                [1, 0, 0, 0],
                [0.35, 0.65, 0, 0],
                [0.1, 0.15, 0.75, 0],
                [0.05, 0.5, 0.1, 0.35],
            ],
        }),
        ("chart-loss", "area", "Sketch of train and validation loss", "Validation turning up is the memorization picture. Not a training run. " + sketch, {
            "series": ["Train", "Validation"],
            "points": [
                {"label": str(index), "values": [round(1.15 * math.exp(-0.35 * index) + 0.08, 2), round(1.1 * math.exp(-0.22 * index) + 0.12 + 0.02 * index * index, 2)]}
                for index in range(8)
            ],
        }),
        ("chart-gate", "bar", "Studio scorecard starting values", "Different units, so the tall bar is latency in milliseconds, not a better score. Quality 84 is higher-better. Safety failures, latency, and cost are lower-better. This is the studio card that starts at gate fix. " + sketch, {
            "points": [
                {"label": "Quality", "value": 84},
                {"label": "Safety fails", "value": 1},
                {"label": "Latency ms", "value": 1100},
                {"label": "Cost cents", "value": 5},
            ],
        }),
        ("chart-permissions", "bar", "Example tool list", "Allow, ask, and deny are a policy. This bar is an example list, not a recommendation of products. " + sketch, {
            "points": [{"label": "Allow", "value": 3}, {"label": "Ask", "value": 2}, {"label": "Deny", "value": 4}],
        }),
        ("chart-chunks", "line", "Character windows on one short note", "A real splitter should keep the heading with the chunk. This count is ceil(length / window). " + sketch, {"points": chunks}),
        ("chart-hybrid", "line", "Blend of a hand-set keyword score and a hand-set cosine", "0.2 keyword and 0.9 cosine. The slider weight is the cosine share. " + sketch, {"points": hybrid}),
        ("chart-retry", "bar", "Calls if every try is repeated", "A retry can double the bill. Budget them. Counts, not prices. " + sketch, {
            "points": [{"label": "1", "value": 1}, {"label": "2", "value": 2}, {"label": "3", "value": 4}],
        }),
        ("chart-kv", "line", "Sketch KV cache versus tokens", "2 × 32 layers × 8 heads × 128 × tokens × 2 bytes. Not a runner report. " + sketch, {
            "points": [{"label": str(tokens), "value": _kv_mb(tokens)} for tokens in (512, 1024, 2048, 4096)],
        }),
        ("chart-qlora", "bar", "Example adapter as a share of the full matrix stack", "QLoRA keeps a quantized base frozen and trains the adapter. The bar is the rank-16 example as a percent of 4096 × 4096 × 32. It is not a memory chart. " + sketch, {
            "points": [
                {"label": "Frozen base", "value": 100},
                {"label": "Adapter %", "value": round(100 * _lora(16) / (4096 * 4096 * 32), 2)},
            ],
        }),
        ("chart-cap", "bar", "Steps left under an example cap of 6", sketch, {
            "points": [{"label": "Used", "value": 4}, {"label": "Left", "value": 2}],
        }),
        ("chart-cite", "bar", "Example citation coverage", "One required id, one cited id. Empty is not a pass. " + sketch, {
            "points": [{"label": "Required", "value": 1}, {"label": "Cited", "value": 1}, {"label": "Missing", "value": 0}],
        }),
        ("chart-machines", "bar", "Machine starting point versus an example weight file", "8 GB starts smaller. 16 GB is the starting point for a 7B or 8B Q4 or Q5, not the size of the weight file. " + sketch, {
            "points": [{"label": "8 GB machine", "value": 8}, {"label": "16 GB machine", "value": 16}, {"label": "7B Q4 file", "value": _gb(7, 4)}],
        }),
        ("chart-loop", "timeline", "One agent loop", "Propose, validate, observe, stop. A loop without a stop is not a design. " + sketch, {
            "points": [{"label": "Propose", "value": 1}, {"label": "Validate", "value": 2}, {"label": "Observe", "value": 3}, {"label": "Stop", "value": 4}],
        }),
        ("chart-handoff", "bar", "When a second loop is justified", "Most jobs stay one loop. A second loop starts from a file, not a shared chat. " + sketch, {
            "points": [{"label": "One loop", "value": 1}, {"label": "File handoff", "value": 1}],
        }),
        ("chart-roles", "bar", "Example tokens by message role", "System, user, and tool text share one window. " + sketch, {
            "points": [{"label": "System", "value": 400}, {"label": "User", "value": 200}, {"label": "Tool", "value": 900}],
        }),
        ("chart-facts", "bar", "Facts added by sampling", "The bar stays at zero. Temperature, top-p, and top-k do not check facts. " + sketch, {
            "points": [{"label": "Temp", "value": 0}, {"label": "Top-p", "value": 0}, {"label": "Top-k", "value": 0}],
        }),
        ("chart-controls", "bar", "What actually checks a claim", "Sources, tools, and tests. Asking the model if it is sure does not. " + sketch, {
            "points": [{"label": "Sources", "value": 1}, {"label": "Tools", "value": 1}, {"label": "Tests", "value": 1}, {"label": "Are you sure", "value": 0}],
        }),
        ("chart-cheaper", "funnel", "Cheaper fixes before a training run", "Prompt, schema, retrieval, and tools come first. Train only for a gap those did not close. " + sketch, {
            "points": [
                {"label": "Prompt", "value": 4},
                {"label": "Schema", "value": 3},
                {"label": "Retrieval", "value": 2},
                {"label": "Train", "value": 1},
            ],
        }),
        ("chart-verbs", "bar", "Verbs that wait for a person", "Send, pay, and delete. Read can be allow inside the cap. " + sketch, {
            "points": [{"label": "Read", "value": 0}, {"label": "Send", "value": 1}, {"label": "Pay", "value": 1}, {"label": "Delete", "value": 1}],
        }),
        ("chart-states", "bar", "Product states to design", "Empty, slow, wrong, and unsafe start blank until you write them. " + sketch, {
            "points": [{"label": "Empty", "value": 0}, {"label": "Slow", "value": 0}, {"label": "Wrong", "value": 0}, {"label": "Unsafe", "value": 0}],
        }),
        ("chart-not-yet", "bar", "Capstone gate", "Ship and not yet are both finished results. " + sketch, {
            "points": [{"label": "Ship", "value": 0}, {"label": "Not yet", "value": 1}],
        }),
        ("chart-scatter", "scatter", "Sketch of latency against a made-up quality axis", "Same roles as the latency widget. Up is not a measured score. " + sketch, {
            "points": [
                {"label": "Small local", "x": 1, "y": 2},
                {"label": "Fast hosted", "x": 2, "y": 3},
                {"label": "Frontier chat", "x": 3, "y": 4},
                {"label": "Reasoning", "x": 5, "y": 5},
                {"label": "Long window", "x": 4, "y": 2},
            ],
        }),
        ("chart-index-pin", "bar", "What a retrieval run must record", "Prompt, model id, and index version. A missing pin is not zero. " + sketch, {
            "points": [{"label": "Prompt", "value": 1}, {"label": "Model id", "value": 1}, {"label": "Index", "value": 1}],
        }),
    ]
    if len(specs) < 40:
        raise SystemExit(f"Need 40 charts, authored {len(specs)}")
    charts = []
    for ident, kind, title, note, payload in specs:
        charts.append({"id": ident, "kind": kind, "title": title, "note": note, "payload": payload})
    return charts


def _chart_html(spec: dict) -> str:
    payload = esc(json.dumps(spec["payload"], separators=(",", ":")))
    return (
        f'<section class="demo" data-demo="{esc(spec["id"])}" data-chart="{esc(spec["id"])}" data-kind="{esc(spec["kind"])}" '
        f'data-payload="{payload}">'
        f'<h3>{esc(spec["title"])}</h3>'
        f'<p class="widget-note">{esc(spec["note"])}</p>'
        f'<div class="chart-host"></div>'
        f'<p class="demo-read" aria-live="polite"></p></section>'
    )


def _playgrounds() -> str:
    return "".join([
        (
            '<section class="demo" data-demo="sampling">'
            "<h3>Sampling playground</h3>"
            '<p class="widget-note">Fixed logits. Temperature, then top-k, then top-p. They reshape this list. They do not add facts. '
            "0.05 stands in for greedy. Many APIs treat 0 as argmax. Temperature 0 is not bit-identical across machines.</p>"
            '<label>Temperature <input class="s-temp" type="range" min="5" max="200" value="80"></label>'
            '<label>Top-p <input class="s-p" type="range" min="10" max="100" value="100"></label>'
            '<label>Top-k <input class="s-k" type="range" min="1" max="8" value="8"></label>'
            '<div class="sample-bars"></div><p class="demo-read" aria-live="polite"></p></section>'
        ),
        (
            '<section class="demo" data-demo="chunk">'
            "<h3>Chunking visualizer</h3>"
            '<p class="widget-note">The same short notes as the retrieval widget. This cuts on a character window so you can see a bad split. '
            "A real index splits on headings and keeps the heading with the chunk.</p>"
            '<label>Window <input class="ch-win" type="range" min="40" max="180" value="80"></label>'
            '<div class="chunk-list"></div><p class="demo-read" aria-live="polite"></p></section>'
        ),
        (
            '<section class="demo" data-demo="rerank">'
            "<h3>Reranker comparison</h3>"
            '<p class="widget-note">Hand-set scores. Sort by the first-stage score or the rerank score. '
            "The unfetched row stays out. A reranker cannot cite a passage the first stage never returned.</p>"
            '<p><button type="button" class="btn rk-ret">Sort by retrieval</button> '
            '<button type="button" class="btn rk-rr">Sort by rerank</button></p>'
            '<div class="rk-list"></div><p class="demo-read" aria-live="polite"></p></section>'
        ),
        (
            '<section class="demo" data-demo="trace">'
            "<h3>Agent trace replayer</h3>"
            '<p class="widget-note">A refund draft. The model may propose send. The policy asks a person. Nothing is sent.</p>'
            '<p><button type="button" class="btn tr-prev">Previous</button> '
            '<button type="button" class="btn tr-next">Next</button></p>'
            '<p class="demo-read" aria-live="polite"></p></section>'
        ),
        (
            '<section class="demo" data-demo="lora">'
            "<h3>LoRA rank calculator</h3>"
            '<p class="widget-note">Trainable count is 2 × rank × (d in + d out) × layers. '
            "The defaults are example dimensions, not a model card. The full count is d in × d out × layers.</p>"
            '<label>d in <input class="lora-in" type="number" min="1" value="4096"></label>'
            '<label>d out <input class="lora-out" type="number" min="1" value="4096"></label>'
            '<label>Rank <input class="lora-rank" type="number" min="1" value="16"></label>'
            '<label>Layers <input class="lora-layers" type="number" min="1" value="32"></label>'
            '<p class="demo-read" aria-live="polite"></p></section>'
        ),
        (
            '<section class="demo" data-demo="quant">'
            "<h3>Quantization memory calculator</h3>"
            '<p class="widget-note">Weight gigabytes are billions of parameters times bits/8. '
            "A 7B or 8B model at Q4 or Q5 is the course starting point for a 16 GB machine because the runner and KV cache are extra. "
            "8 GB starts smaller. Quantizing weights is not the same thing as training a LoRA adapter.</p>"
            '<label>Billions of parameters <input class="q-b" type="number" min="0.1" step="0.1" value="7"></label>'
            '<label>Bits <input class="q-bits" type="number" min="2" max="16" value="4"></label>'
            '<p class="demo-read" aria-live="polite"></p></section>'
        ),
        (
            '<section class="demo" data-demo="schema">'
            "<h3>Schema reject</h3>"
            '<p class="widget-note">Required fields are name and query. Missing fields are a reject, not a guess.</p>'
            '<label>Tool call<textarea class="sch-in" rows="3">{"name":"read_notes"}</textarea></label>'
            '<p><button type="button" class="btn sch-go">Validate</button></p>'
            '<p class="demo-read" aria-live="polite"></p></section>'
        ),
        (
            '<section class="demo" data-demo="approval">'
            "<h3>Approval payload</h3>"
            '<p class="widget-note">Allow read-only inside the cap. Ask before send, pay, or delete. Deny a shell. '
            "The person sees the exact arguments.</p>"
            '<label>Verb <select class="ap-verb">'
            '<option>read_notes</option><option>send_email</option><option>pay</option><option>delete</option><option>shell</option>'
            "</select></label>"
            '<label>Arguments <input class="ap-args" type="text" value=\'{"id":"notes-01"}\'></label>'
            '<p class="demo-read" aria-live="polite"></p></section>'
        ),
        (
            '<section class="demo" data-demo="idem">'
            "<h3>Idempotency key</h3>"
            '<p class="widget-note">The same key and the same arguments replay the stored result. '
            "The same key with different arguments is a conflict. A retry must not double-send.</p>"
            '<label>Key <input class="id-key" type="text" value="job-1"></label>'
            '<label>Arguments <input class="id-args" type="text" value="read notes-01"></label>'
            '<p><button type="button" class="btn id-go">Submit</button></p>'
            '<p class="demo-read" aria-live="polite"></p></section>'
        ),
        (
            '<section class="demo" data-demo="fit">'
            "<h3>Context fit</h3>"
            '<p class="widget-note">Instructions, retrieved text, chat, and the answer share one window. '
            "This uses an example window, not a model card.</p>"
            '<label>Instructions <input class="fit-a" type="number" value="800"></label>'
            '<label>Retrieved <input class="fit-b" type="number" value="2400"></label>'
            '<label>Chat <input class="fit-c" type="number" value="1200"></label>'
            '<label>Answer <input class="fit-d" type="number" value="600"></label>'
            '<label>Window <input class="fit-w" type="number" value="8192"></label>'
            '<p class="demo-read" aria-live="polite"></p></section>'
        ),
        (
            '<section class="demo" data-demo="hybrid">'
            "<h3>Hybrid weight</h3>"
            '<p class="widget-note">Hand-set keyword score 0.20 and cosine 0.90. The weight is the cosine share.</p>'
            '<label>Cosine weight <input class="hy-w" type="range" min="0" max="100" value="55"></label>'
            '<p class="demo-read" aria-live="polite"></p></section>'
        ),
        (
            '<section class="demo" data-demo="retry">'
            "<h3>Retry budget</h3>"
            '<p class="widget-note">Each extra try adds a call. This count is not a price. Stop when the budget is spent.</p>'
            '<label>Budget <input class="ry-b" type="number" min="1" value="2"></label>'
            '<label>Attempts <input class="ry-a" type="number" min="1" value="3"></label>'
            '<p class="demo-read" aria-live="polite"></p></section>'
        ),
        (
            '<section class="demo" data-demo="cite">'
            "<h3>Citation coverage</h3>"
            '<p class="widget-note">The required id is notes-01. Check the ids the draft actually cites. A blank list is not a pass.</p>'
            '<label><input class="cite-box" type="checkbox" value="notes-01"> notes-01</label>'
            '<label><input class="cite-box" type="checkbox" value="notes-02"> notes-02</label>'
            '<p class="demo-read" aria-live="polite"></p></section>'
        ),
        (
            '<section class="demo" data-demo="cap">'
            "<h3>Step cap</h3>"
            '<p class="widget-note">The example cap is 6. At the cap the loop stops, even if the model wants another call.</p>'
            '<label>Steps taken <input class="cap-n" type="number" min="0" value="6"></label>'
            '<p class="demo-read" aria-live="polite"></p></section>'
        ),
        (
            '<section class="demo" data-demo="kv">'
            "<h3>KV cache sketch</h3>"
            '<p class="widget-note">Bytes are 2 × 32 layers × 8 heads × 128 × tokens × 2. A sketch, not a runner report. '
            "This is why a 3.5 GB weight file is not the whole memory bill.</p>"
            '<label>Tokens <input class="kv-n" type="number" min="1" value="2048"></label>'
            '<p class="demo-read" aria-live="polite"></p></section>'
        ),
        (
            '<section class="demo" data-demo="pin">'
            "<h3>Index pin</h3>"
            '<p class="widget-note">A retrieval run records the prompt id, the model id, and the index version. Empty is not pinned.</p>'
            '<label>Prompt id <input class="pin-p" type="text" value=""></label>'
            '<label>Model id <input class="pin-m" type="text" value=""></label>'
            '<label>Index version <input class="pin-i" type="text" value=""></label>'
            '<p class="demo-read" aria-live="polite"></p></section>'
        ),
        (
            '<section class="demo" data-demo="refuse">'
            "<h3>Cite or refuse</h3>"
            '<p class="widget-note">Keyword match on the toy notes. If the notes do not contain the question, the answer is a refusal.</p>'
            '<label>Question <input class="rf-q" type="text" value="what is the capital of france"></label>'
            '<p><button type="button" class="btn rf-go">Ask the notes</button></p>'
            '<p class="demo-read" aria-live="polite"></p></section>'
        ),
    ])


def demos_html() -> str:
    charts = _charts()
    body = "".join(_chart_html(spec) for spec in charts) + _playgrounds()
    return '<div class="demo-grid">' + body + "</div>"
