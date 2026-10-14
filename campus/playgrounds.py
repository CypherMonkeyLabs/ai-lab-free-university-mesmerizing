"""App shell and offline playgrounds for the campus page."""

from __future__ import annotations

import html
import json
from pathlib import Path

from campus.schema import SCHOOLS
from campus.visuals import accent

HERE = Path(__file__).resolve().parent
APP_CSS = (HERE / "app.css").read_text(encoding="utf-8")
APP_JS = (HERE / "play_math.js").read_text(encoding="utf-8") + "\n" + (HERE / "app.js").read_text(encoding="utf-8")

WHY = {
    "00": "Later tracks only work if you can keep proof and follow one safety rule.",
    "01": "Token, context, and sampling mistakes cause more bad product calls than a weak slogan.",
    "02": "A prompt without a done-check cannot be improved, because nobody can say it failed.",
    "03": "A local model is how you keep data off a hosted service and learn the real memory limit.",
    "04": "A leaked key or an unread bill ends a project faster than a clumsy prompt.",
    "05": "An answer is grounded only when it cites a passage you actually retrieved.",
    "06": "A tool loop without a schema and a step cap spends money and takes actions you did not allow.",
    "07": "A shared tool protocol helps only when the server cannot act without the permission you granted.",
    "08": "A repository edit is finished when the diff and the tests agree with the task.",
    "09": "A change that feels better can still lose on quality, safety, latency, or cost.",
    "10": "LoRA is warranted when the same eval says prompting and retrieval already failed.",
    "11": "The actions that need a person have to be written down before a tool can take them.",
    "12": "A feature ships when one spec is measurable by both the product owner and the engineer.",
    "13": "The course ends with a small assistant you can test, not a pile of notes.",
}

ICONS = {
    "compass": "M12 21a9 9 0 1 0-9-9 9 9 0 0 0 9 9 M12 8v4l3 2",
    "layers": "M12 3l9 5-9 5L3 8l9-5 M3 12l9 5 9-5 M3 17l9 5 9-5",
    "prompt": "M5 6h14v8H8l-3 3z",
    "laptop": "M4 6h16v9H4z M3 18h18",
    "receipt": "M7 3h10v18l-2-1.4-2 1.4-2-1.4L9 21l-2-1.4z M9 8h6 M9 12h6",
    "search": "M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14 M20 20l-3.2-3.2",
    "loop": "M5 12a7 7 0 0 1 12-4 M19 12a7 7 0 0 1-12 4 M16 5v3h3 M8 19v-3H5",
    "plug": "M9 3v5 M15 3v5 M7 8h10v4a5 5 0 0 1-10 0z M12 17v4",
    "diff": "M8 4v16 M8 5h6 M14 20h6 M20 10v10",
    "gauge": "M5 16a7 7 0 1 1 14 0 M12 16l3.5-3.5",
    "adapter": "M4 6h16v3H4z M4 11h16v3H4z M4 16h9v3H4z",
    "shield": "M12 3l8 3v6c0 4.5-3.2 7.2-8 9-4.8-1.8-8-4.5-8-9V6z",
    "plan": "M8 3h8v4H8z M6 8h12v13H6z M9 12h6 M9 16h4",
    "flag": "M6 4v16 M6 4h11l-2 4 2 4H6",
    "spark": "M12 3v6 M12 15v6 M3 12h6 M15 12h6 M6 6l3 3 M15 15l3 3 M18 6l-3 3 M9 15l-3 3",
    "cards": "M7 6h12v14H7z M5 8v12h12",
    "check": "M5 12l5 5L20 7",
}

TRACK_ICON = {
    "00": "compass",
    "01": "layers",
    "02": "prompt",
    "03": "laptop",
    "04": "receipt",
    "05": "search",
    "06": "loop",
    "07": "plug",
    "08": "diff",
    "09": "gauge",
    "10": "adapter",
    "11": "shield",
    "12": "plan",
    "13": "flag",
}


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def icon(name: str) -> str:
    path = ICONS.get(name, ICONS["spark"])
    return (
        f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">'
        f'<path d="{path}"/></svg>'
    )


def track_cards(by_school: dict[str, list[dict]]) -> str:
    cards = []
    tracks = [school for school in SCHOOLS if school["kind"] == "track"]
    for offset, school in enumerate(tracks):
        stripe = (offset % 6) + 1
        count = len(by_school[school["id"]])
        cards.append(
            f'<a class="track-card tilt" data-accent="{stripe}" data-school="{esc(school["id"])}" '
            f'href="#school-{esc(school["id"])}" style="--accent:{accent(school["id"])}">'
            f'<span class="tilt-face">'
            f'<span class="card-top"><span class="ico-chip">{icon(TRACK_ICON[school["id"]])}</span>'
            f'<span class="idx">{esc(school["id"])}</span></span>'
            f"<strong>{esc(school['name'])}</strong>"
            f"<em>{esc(school['outcome'])}</em>"
            f'<span class="why"><span>Why it matters.</span> {esc(WHY[school["id"]])}</span>'
            f'<span class="meta">{count} lessons</span>'
            f'<span class="track-bar" aria-hidden="true"><b data-school-bar="{esc(school["id"])}"></b></span>'
            f"</span></a>"
        )
    return "".join(cards)


def launcher_section() -> str:
    labs = (
        ("attn", "spark", "Tokens and attention", "See which earlier token a position is allowed to use.", "#play-attn"),
        ("rag", "search", "Retrieval pipeline", "Step from chunks to vectors to a cited answer, or a refusal.", "#play-rag"),
        ("agent", "plug", "Agent and MCP", "Watch a tool call, then the gate that blocks a send.", "#play-agent"),
        ("eval", "gauge", "Eval gate", "Move quality, safety, latency, and cost until the gate says stop.", "#play-eval"),
        ("lora", "adapter", "LoRA rank", "See how rank changes the count of trainable numbers.", "#play-lora"),
        ("quiz", "check", "Quiz", "Ten questions with the reason each answer matters.", "#play-quiz"),
        ("cards", "cards", "Flashcards", "The check questions from the lessons, stored in this browser.", "#play-cards"),
    )
    cards = []
    for key, glyph, title, why, href in labs:
        cards.append(
            f'<a class="launch-card tilt" href="{href}" data-lab="{key}">'
            f'<span class="tilt-face"><span class="ico-chip">{icon(glyph)}</span>'
            f"<strong>{esc(title)}</strong><em>{esc(why)}</em></span></a>"
        )
    return (
        '<section class="block" id="launchBoard">'
        '<div class="block-head"><h2>Playgrounds</h2>'
        "<p>Zero keys. The numbers are fixed teaching values.</p></div>"
        f'<div class="launch-grid">{"".join(cards)}</div></section>'
    )


def command_palette() -> str:
    return """
<div id="palette" class="palette" hidden>
  <div class="palette-back" data-palette-close="1"></div>
  <div class="palette-dialog" role="dialog" aria-modal="true" aria-labelledby="paletteLabel">
    <div class="palette-search">
      <svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14 M20 20l-3.2-3.2"/></svg>
      <label id="paletteLabel" class="sr-only" for="paletteInput">Search the course</label>
      <input id="paletteInput" type="text" autocomplete="off" spellcheck="false" placeholder="Lessons, tracks, playgrounds" aria-controls="paletteList" aria-autocomplete="list"/>
      <kbd>Esc</kbd>
    </div>
    <div id="paletteList" class="palette-list" role="listbox" aria-label="Results"></div>
    <p class="palette-hint"><kbd>↑</kbd><kbd>↓</kbd> move <kbd>Enter</kbd> open <kbd>Esc</kbd> close</p>
  </div>
</div>
"""


def mini_player() -> str:
    return """
<div id="miniPlayer" class="mini-player" hidden>
  <button type="button" class="icon-btn" id="miniToggle" aria-label="Pause audio">
    <svg class="ico play-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l12-7z"/></svg>
    <svg class="ico pause-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h4v14H7z M13 5h4v14h-4z"/></svg>
  </button>
  <div class="mini-copy">
    <strong id="miniTitle">Audio</strong>
    <span id="miniTime">0:00</span>
  </div>
  <label class="sr-only" for="miniSeek">Seek</label>
  <input id="miniSeek" type="range" min="0" max="1000" value="0" aria-label="Seek in the clip"/>
  <button type="button" class="icon-btn" id="miniClose" aria-label="Hide the player and pause">
    <svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12 M18 6L6 18"/></svg>
  </button>
</div>
"""


def play_nav() -> str:
    return (
        '<a class="ll play-link" href="#play" data-search="playgrounds tokens attention retrieval rag agent mcp '
        'eval scoreboard lora rank quiz flashcards">'
        '<span class="ln">Lab</span><span class="nav-ico"></span><span>Playgrounds</span></a>'
    )


def _quiz() -> str:
    questions = (
        (
            "q1",
            "b",
            "What does a model do at each step?",
            (("a", "It looks up a fact database"), ("b", "It predicts the next token"), ("c", "It runs your tests")),
            "Fluency is not a source of record. The next token can sound sure and still be wrong.",
        ),
        (
            "q2",
            "a",
            "Who enforces a tool schema?",
            (("a", "Your code"), ("b", "The model"), ("c", "The prompt wording")),
            "The model only proposes the call. Code rejects an unknown name or a bad argument.",
        ),
        (
            "q3",
            "c",
            "When should a retrieval answer refuse?",
            (("a", "When the user is new"), ("b", "When the answer would be long"), ("c", "When the passages do not contain the answer")),
            "A missing passage cannot be repaired by a confident paragraph.",
        ),
        (
            "q4",
            "b",
            "What makes a citation checkable?",
            (("a", "It sounds specific"), ("b", "It names an id you retrieved and a place a person can find"), ("c", "It includes a link the model invented")),
            "A citation you did not retrieve is a guess with a footnote.",
        ),
        (
            "q5",
            "a",
            "What is a real done-check?",
            (("a", "A test a person or a program can apply without asking the model"), ("b", "A request to try harder"), ("c", "A lower temperature")),
            "If you cannot mark the output pass or fail, the task is not specified yet.",
        ),
        (
            "q6",
            "c",
            "When is LoRA the right next step?",
            (("a", "At the start of every project"), ("b", "Whenever the prose feels generic"), ("c", "After prompting and retrieval fail the same eval")),
            "Rank spends capacity. The eval, not the slider, decides whether that spend is earned.",
        ),
        (
            "q7",
            "b",
            "A key lands in a log. What do you do?",
            (("a", "Edit that file and keep the key"), ("b", "Revoke the key, then fix the log"), ("c", "Lower the temperature")),
            "A copied log still holds the secret. Revoke first.",
        ),
        (
            "q8",
            "a",
            "What does temperature change?",
            (("a", "The distribution over the next token"), ("b", "The facts the model knows"), ("c", "Which passage was retrieved")),
            "Sampling reshapes probability. It does not add a source.",
        ),
        (
            "q9",
            "c",
            "What belongs in an agent trace?",
            (("a", "The API key"), ("b", "Only the final paragraph"), ("c", "The tool name, the arguments, and the observation")),
            "Without the observation, you cannot tell a quoted result from a guess.",
        ),
        (
            "q10",
            "b",
            "What does MCP standardize?",
            (("a", "Which actions are safe"), ("b", "How a client talks to a tool server"), ("c", "The model's training data")),
            "The protocol is the envelope. Permission is still your decision.",
        ),
    )
    blocks = []
    for name, answer, legend, options, why in questions:
        labels = []
        for value, text in options:
            labels.append(
                f'<label><input type="radio" name="{esc(name)}" value="{esc(value)}"/> {esc(text)}</label>'
            )
        blocks.append(
            f'<fieldset data-answer="{esc(answer)}"><legend>{esc(legend)}</legend>'
            f'{"".join(labels)}'
            f'<p class="quiz-why" hidden><span>Why it matters.</span> {esc(why)}</p></fieldset>'
        )
    return "".join(blocks)


def flash_cards(lessons: list[dict]) -> list[dict]:
    cards = []
    for item in lessons:
        seen = 0
        for block in item["blocks"]:
            if block.get("t") != "check":
                continue
            seen += 1
            cards.append({
                "id": f"{item['id']}-{seen}",
                "lesson": item["id"],
                "title": item["title"],
                "q": block["q"],
                "a": block["a"],
            })
    return cards


def playgrounds_page(lessons: list[dict]) -> str:
    cards = flash_cards(lessons)
    blob = json.dumps(cards, ensure_ascii=True).replace("<", "\\u003c")
    tabs = (
        ("attn", "Tokens"),
        ("rag", "Retrieval"),
        ("agent", "Agent"),
        ("eval", "Evals"),
        ("lora", "LoRA"),
        ("quiz", "Quiz"),
        ("cards", "Cards"),
    )
    tab_html = []
    for key, label in tabs:
        selected = "true" if key == "attn" else "false"
        tab_index = "0" if key == "attn" else "-1"
        tab_html.append(
            f'<button type="button" class="play-tab" role="tab" id="tab-{key}" data-tab="{key}" '
            f'aria-selected="{selected}" aria-controls="panel-{key}" tabindex="{tab_index}">{label}</button>'
        )
    return f"""
<section id="play" data-panel="play">
  <p class="eyebrow">Playgrounds · offline · no key</p>
  <h1>Play the mechanism.</h1>
  <p class="lede">These labs use fixed teaching numbers so you can see a step change. They do not call a model. Each one says why the step matters before you move on.</p>
  <div class="play-tabs" role="tablist" aria-label="Playgrounds">{''.join(tab_html)}</div>

  <div class="play-panel" id="panel-attn" role="tabpanel" aria-labelledby="tab-attn" data-tab="attn">
    <h2>Tokens and attention</h2>
    <p class="why"><span>Why it matters.</span> A later token may use earlier tokens. If you cannot see that limit, a wrong answer looks like memory.</p>
    <label>Text <textarea id="pgText" rows="3">The model predicts the next token.</textarea></label>
    <div id="pgTokens" class="token-row" aria-live="polite"></div>
    <label>Query position <input id="pgQuery" type="range" min="0" max="1" value="0"/></label>
    <canvas id="pgCanvas" class="play-canvas" width="880" height="320" aria-label="Attention heatmap and arcs"></canvas>
    <p id="pgRead" class="play-read">Causal attention on a toy vector. Future tokens stay at zero.</p>
  </div>

  <div class="play-panel" id="panel-rag" role="tabpanel" aria-labelledby="tab-rag" data-tab="rag" hidden>
    <h2>Retrieval pipeline</h2>
    <p class="why"><span>Why it matters.</span> Grounding is a pipeline. The answer is allowed to speak only after a chunk clears the bar.</p>
    <div class="preset-row" role="group" aria-label="Example questions">
      <button type="button" class="btn rag-preset" data-q="How long is the return window?">Return window</button>
      <button type="button" class="btn rag-preset" data-q="What is the shipping time?">Shipping</button>
      <button type="button" class="btn rag-preset" data-q="When is the desk open?">Hours</button>
      <button type="button" class="btn rag-preset" data-q="What is the CEO phone number?">Missing fact</button>
    </div>
    <label>Question <input id="ragQuestion" type="text" value="How long is the return window?"/></label>
    <ol class="pipe" id="ragPipe">
      <li data-step="0"><span>1</span> Chunk</li>
      <li data-step="1"><span>2</span> Embed</li>
      <li data-step="2"><span>3</span> Retrieve</li>
      <li data-step="3"><span>4</span> Answer</li>
    </ol>
    <div class="step-bar">
      <button type="button" class="btn" id="ragPrev">Previous step</button>
      <button type="button" class="btn primary" id="ragNext">Next step</button>
      <button type="button" class="btn" id="ragPlay">Play</button>
    </div>
    <canvas id="ragCanvas" class="play-canvas" width="880" height="280" aria-label="Toy embedding map"></canvas>
    <div id="ragHits" class="hit-list"></div>
    <p id="ragAnswer" class="play-read" aria-live="polite"></p>
  </div>

  <div class="play-panel" id="panel-agent" role="tabpanel" aria-labelledby="tab-agent" data-tab="agent" hidden>
    <h2>Agent and MCP simulator</h2>
    <p class="why"><span>Why it matters.</span> The model proposes a call. Your code decides whether it runs. MCP is the envelope, not permission to skip that check.</p>
    <div class="preset-row" role="group" aria-label="Example goals">
      <button type="button" class="btn agent-preset" data-q="What is 15 percent of 80?">Percent</button>
      <button type="button" class="btn agent-preset" data-q="How long is the return window?">Look up a note</button>
      <button type="button" class="btn agent-preset" data-q="What time is it on the clock?">Clock</button>
      <button type="button" class="btn agent-preset" data-q="Send the refund policy to the desk">Send, blocked</button>
    </div>
    <label>Goal <input id="agentGoal" type="text" value="What is 15 percent of 80?"/></label>
    <div class="step-bar">
      <button type="button" class="btn" id="agentPrev">Previous</button>
      <button type="button" class="btn primary" id="agentNext">Next</button>
      <button type="button" class="btn" id="agentRun">Run the loop</button>
    </div>
    <ol id="agentTrace" class="trace" aria-live="polite"></ol>
    <p class="play-note">The server name in this lab is <code>lab.tools</code>. It is a picture of a call, not a connection.</p>
  </div>

  <div class="play-panel" id="panel-eval" role="tabpanel" aria-labelledby="tab-eval" data-tab="eval" hidden>
    <h2>Eval scoreboard</h2>
    <p class="why"><span>Why it matters.</span> A change that reads better can still fail. The gate ships only when all four checks hold.</p>
    <div class="score-lab">
      <label>Candidate quality <output id="evQualOut">82</output><input id="evQual" type="range" min="50" max="100" value="82"/></label>
      <label>Baseline quality <output id="evQualBaseOut">80</output><input id="evQualBase" type="range" min="50" max="100" value="80"/></label>
      <label>Candidate safety failures <output id="evSafeOut">1</output><input id="evSafe" type="range" min="0" max="5" value="1"/></label>
      <label>Baseline safety failures <output id="evSafeBaseOut">1</output><input id="evSafeBase" type="range" min="0" max="5" value="1"/></label>
      <label>Candidate latency, ms <output id="evLatOut">700</output><input id="evLat" type="range" min="200" max="2000" step="50" value="700"/></label>
      <label>Latency budget, ms <output id="evLatBudgetOut">800</output><input id="evLatBudget" type="range" min="200" max="2000" step="50" value="800"/></label>
      <label>Candidate cost, cents <output id="evCostOut">3</output><input id="evCost" type="range" min="1" max="12" value="3"/></label>
      <label>Cost budget, cents <output id="evCostBudgetOut">4</output><input id="evCostBudget" type="range" min="1" max="12" value="4"/></label>
    </div>
    <div class="meters" aria-hidden="true">
      <span><i id="meterQual"></i></span>
      <span><i id="meterSafe"></i></span>
      <span><i id="meterLat"></i></span>
      <span><i id="meterCost"></i></span>
    </div>
    <p id="evVerdict" class="verdict" role="status">Checking the gate.</p>
  </div>

  <div class="play-panel" id="panel-lora" role="tabpanel" aria-labelledby="tab-lora" data-tab="lora" hidden>
    <h2>LoRA rank</h2>
    <p class="why"><span>Why it matters.</span> Rank is a budget of trainable numbers. A higher rank can fit more, and it can also memorize. Compare the adapter to the base model on the same tasks.</p>
    <label>Rank <output id="loraOut">8</output><input id="loraRank" type="range" min="1" max="32" value="8"/></label>
    <canvas id="loraCanvas" class="play-canvas" width="880" height="260" aria-label="Low rank matrices A and B"></canvas>
    <p id="loraRead" class="play-read"></p>
    <p class="play-note">This layer is a toy width of 128. A shipping model is larger. The picture is the shape of the update, not a trained adapter.</p>
  </div>

  <div class="play-panel" id="panel-quiz" role="tabpanel" aria-labelledby="tab-quiz" data-tab="quiz" hidden>
    <h2>Quiz</h2>
    <p class="why"><span>Why it matters.</span> A score without the reason is a trivia night. Each item states why the distinction changes a build.</p>
    <form id="quizForm">{_quiz()}
      <p class="step-bar"><button type="submit" class="btn primary">Score the quiz</button>
      <button type="button" class="btn" id="quizReset">Clear</button></p>
      <p id="quizOut" class="play-read" role="status"></p>
    </form>
  </div>

  <div class="play-panel" id="panel-cards" role="tabpanel" aria-labelledby="tab-cards" data-tab="cards" hidden>
    <h2>Flashcards</h2>
    <p class="why"><span>Why it matters.</span> These are the check questions already in the lessons. The answer is the distinction the lesson asked you to keep.</p>
    <p id="cardMeta" class="play-note"></p>
    <div class="flip" id="cardFlip">
      <button type="button" class="flip-btn" id="cardFlipBtn" aria-pressed="false">
        <span class="flip-inner">
          <span class="face front" id="cardFront"></span>
          <span class="face back" id="cardBack"></span>
        </span>
      </button>
    </div>
    <div class="step-bar">
      <button type="button" class="btn" id="cardPrev">Previous</button>
      <button type="button" class="btn" id="cardAgain">Study again</button>
      <button type="button" class="btn primary" id="cardKnew">Knew it</button>
      <button type="button" class="btn" id="cardNext">Next</button>
    </div>
    <p class="play-note">Space flips the card when it is focused. Marks stay in this browser.</p>
    <script type="application/json" id="flashData">{blob}</script>
  </div>
</section>
"""
