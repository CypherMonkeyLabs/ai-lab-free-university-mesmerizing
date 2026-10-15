"""Downloads hub and arcade markup. Counts are filled from the real banks."""

from __future__ import annotations

import html

from campus.pool import SCENARIOS


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


PORTS = (
    ("HTTPS model API", "443", ("80", "443", "8080", "11434"), "TCP. Confirm the vendor host."),
    ("OTLP gRPC", "4317", ("4317", "4318", "443", "9200"), "OpenTelemetry default. Not re-fetched 2026-10-15."),
    ("OTLP HTTP", "4318", ("4317", "4318", "80", "3000"), "OpenTelemetry default. Not re-fetched 2026-10-15."),
    ("Ollama default", "11434", ("3000", "8080", "11434", "5000"), "Published loopback default. Not re-fetched 2026-10-15."),
    ("SIP signaling", "5060", ("5060", "5061", "443", "16384"), "RFC 3261. Confirm the listener."),
    ("SIP over TLS", "5061", ("443", "5060", "5061", "8443"), "Commonly assigned. Confirm in the IANA registry."),
    ("DNS", "53", ("53", "123", "443", "853"), "Name lookup."),
    ("MCP over stdio", "no port", ("443", "no port", "8080", "22"), "A local process. HTTP is a different transport."),
)

DAILY = (
    ("What does one forward pass produce?", "Scores over the next token, not a finished paragraph."),
    ("What is a done-check?", "A test a person can mark without asking the model."),
    ("When do you cite?", "When a retrieved span has an id someone can open."),
    ("What makes a tool call safe enough to run?", "A schema, a permission, and a handler you wrote."),
    ("What belongs in the log?", "Ids and counts. Not the key, and not raw private text."),
    ("Who owns an emergency call?", "The voice platform's emergency path, not the model."),
    ("What is shadow mode?", "The new path answers beside the old one. Users still see the old one."),
    ("Why skip fine-tuning first?", "Prompt, schema, retrieval, and tools are cheaper to undo."),
    ("What is MCP stdio?", "A local process. It has no port."),
    ("What four numbers share a gate?", "Quality, safety, latency, and cost."),
    ("What is a kill switch?", "A flag, a person who may throw it, and the old path you return to."),
    ("When is a fluent answer not evidence?", "When the span was never in the pack."),
    ("What does temperature change?", "Which token is drawn. Not whether it is true."),
    ("What do you show instead of a certificate?", "A trace, a task set, and a gate."),
)

FLOW = ("Caller", "SIP", "ASR", "Retrieve", "Model", "TTS", "Person if needed")

MAP = (
    ("Caller", 36, 118, "The person on the channel. An emergency request leaves this path."),
    ("SIP", 168, 36, "Signaling on the voice platform. RFC 3261. Confirm the listener."),
    ("ASR", 300, 118, "Speech becomes text after the platform already has the audio."),
    ("Retrieve", 432, 36, "A span you are allowed to store. Cite the id or refuse."),
    ("Model", 564, 118, "A pinned id returns next-token scores. It does not own the call."),
    ("TTS", 696, 36, "The platform plays the audio. The model does not open a socket."),
    ("Person", 828, 118, "Send, pay, delete, and cutover stop with a person."),
    ("Emergency", 168, 210, "The voice platform's emergency path. Do not send that turn to a model."),
)


def downloads_page(sheet_count: int, card_count: int) -> str:
    sheets = (
        ("ports-protocols", "Ports and protocols"),
        ("call-flows", "Call and data flows"),
        ("config-checklist", "Configuration checklist"),
        ("troubleshooting", "Troubleshooting tree"),
        ("migration", "Migration and cutover"),
        ("security-gates", "Security gates"),
        ("eval-card", "Eval scorecard"),
        ("glossary-card", "Glossary card"),
        ("read-a-ladder", "How to read a ladder"),
        ("career-path", "Career path"),
    )
    cards = []
    for slug, title in sheets:
        cards.append(
            f'<article class="cheat-card"><h3>{esc(title)}</h3>'
            f'<p><a href="assets/cheats/{esc(slug)}.html">HTML</a> · '
            f'<a href="assets/cheats/{esc(slug)}.pdf">PDF</a> · '
            f'<a href="assets/cheats/{esc(slug)}.png">PNG</a> · '
            f'<a href="assets/cheats/{esc(slug)}.svg">SVG</a></p></article>'
        )
    return f"""
<section id="downloads" data-panel="downloads">
  <p class="eyebrow">Cheat codes · files in this repo</p>
  <h1>Download the sheets</h1>
  <p class="lede">{sheet_count} topic sheets, each as HTML, PDF, PNG, and SVG, plus a flashcard JSON of {card_count} cards and a printable flashcard PDF. The zip is the full offline campus. Nothing on this page is loaded from another host.</p>
  <p id="offlineStatus" class="block-note">Open a sheet, or take the zip. After one visit on this origin, the service worker keeps the files you used.</p>
  <div class="cheat-grid">{''.join(cards)}
    <article class="cheat-card"><h3>Flashcards</h3>
      <p><a href="assets/cheats/flashcards.html">Printable HTML</a> · <a href="assets/cheats/flashcards.pdf">PDF</a> · <a href="assets/cheats/flashcards.json">JSON</a></p>
    </article>
    <article class="cheat-card"><h3>Full offline bundle</h3>
      <p><a href="../downloads/ai-lab-university.html.zip">Campus zip</a> · <a href="assets/cheats/index.html">Sheet index</a></p>
    </article>
  </div>
  <p class="block-note">Every sheet carries the lab footer. They cite the lesson instead of copying a vendor document.</p>
</section>
"""


def arcade_page() -> str:
    port_cards = []
    for index, (name, answer, options, why) in enumerate(PORTS, start=1):
        buttons = []
        for option in options:
            ok = "1" if option == answer else "0"
            buttons.append(
                f'<button type="button" class="port-choice" data-port="{index}" data-ok="{ok}">{esc(option)}</button>'
            )
        port_cards.append(
            f'<article class="cheat-card" data-port-card="{index}"><h3>{index}. {esc(name)}</h3>'
            f'<div class="badge-row">{"".join(buttons)}</div>'
            f'<p class="why" hidden>{esc(why)}</p></article>'
        )
    nodes = "".join(
        f'<button type="button" class="flow-node" data-flow="{esc(step)}">{esc(step)}</button>'
        for step in ("Model", "ASR", "Caller", "TTS", "Retrieve", "SIP", "Person if needed")
    )
    daily = []
    for index, (question, answer) in enumerate(DAILY):
        daily.append(
            f'<article data-daily="{index}"><h3>{esc(question)}</h3><p>{esc(answer)}</p></article>'
        )
    scenarios = []
    for item in SCENARIOS:
        good = next((choice for choice in item["choices"] if choice.get("ok")), None)
        label = good["label"] if good else "See the room."
        scenarios.append(
            f'<article class="cheat-card"><h3>{esc(item["title"])}</h3>'
            f'<p>{esc(item["symptom"])}</p>'
            f'<p class="why"><span>A fix that matches the cited failure.</span> {esc(label)}</p></article>'
        )
    badges = (
        ("lessons", 1, "First mark"),
        ("lessons", 10, "Ten pages"),
        ("lessons", 50, "Fifty pages"),
        ("lessons", 128, "Original course"),
        ("ports", 4, "Four ports"),
        ("ports", 8, "Port board clear"),
    )
    badge_html = "".join(
        f'<span class="badge" data-badge="{kind}" data-need="{need}">{esc(name)}</span>'
        for kind, need, name in badges
    )
    return f"""
<section id="arcade" data-panel="arcade">
  <p class="eyebrow">Arcade · {len(PORTS)} ports · {len(DAILY)} daily prompts · {len(SCENARIOS)} scenarios</p>
  <h1>Practice with the same facts</h1>
  <p class="lede">The counters are the size of the banks on this page. A mark still lives only in this browser.</p>
  <h2>Ports and protocols</h2>
  <p id="portScore" class="block-note">0 of {len(PORTS)} ports correct in this sitting.</p>
  <div class="game-grid">{''.join(port_cards)}</div>
  <h2>Flow map</h2>
  <p>Select a node. The picture is a study map. It is not a dial plan, and emergency stays off the model.</p>
  <div class="flow-map-wrap">
  <svg class="flow-map" viewBox="0 0 980 280" role="img" aria-label="Study map from the caller to a person, with emergency kept on the voice platform">
    <line class="map-line" x1="156" y1="140" x2="168" y2="58"/>
    <line class="map-line" x1="288" y1="58" x2="300" y2="140"/>
    <line class="map-line" x1="420" y1="140" x2="432" y2="58"/>
    <line class="map-line" x1="552" y1="58" x2="564" y2="140"/>
    <line class="map-line" x1="684" y1="140" x2="696" y2="58"/>
    <line class="map-line" x1="816" y1="58" x2="828" y2="140"/>
    <line class="map-stop" x1="96" y1="162" x2="228" y2="210"/>
    {''.join(
        f'<g class="map-node{" map-stop-node" if name == "Emergency" else ""}" data-map="{esc(name)}" data-blurb="{esc(blurb)}" tabindex="0" role="button" aria-label="{esc(name)}">'
        f'<rect x="{x}" y="{y}" width="120" height="44" rx="12"/>'
        f'<text x="{x + 60}" y="{y + 28}" text-anchor="middle">{esc(name)}</text></g>'
        for name, x, y, blurb in MAP
    )}
  </svg>
  </div>
  <p id="mapOut" class="block-note">No node selected yet. {len(MAP)} nodes are on the map.</p>
  <h2>Build the study order</h2>
  <p>Click the stages in study order. The target is in the next line so a checker can read it.</p>
  <p id="flowTarget" class="sr-only">{esc("|".join(FLOW))}</p>
  <div class="badge-row">{nodes}<button type="button" class="flow-node" id="flowReset">Start over</button></div>
  <p id="flowOut" class="block-note">Nothing clicked yet.</p>
  <h2>Daily challenge</h2>
  <p id="dailyIndex" class="block-note">Prompt 1 of {len(DAILY)}</p>
  <div id="dailyCard">{''.join(daily)}</div>
  <h2>Badges</h2>
  <div class="badge-row">{badge_html}</div>
  <h2>Share a result card</h2>
  <div class="share-card">
    <p>The card shows how many pages you marked and links the reader to cyphermonkeylabs.com. It is not a certificate.</p>
    <button type="button" class="btn primary" id="shareBtn">Build the card</button>
    <a id="shareLink" hidden href="#arcade">Save the result card</a>
  </div>
  <h2>Incident scenarios</h2>
  <p class="block-note">{len(SCENARIOS)} cited failures from the study draft. Choosing the matching fix is described here. The page does not run the action.</p>
  <div class="game-grid">{''.join(scenarios)}</div>
</section>
"""
