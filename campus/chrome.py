"""Shared chrome for the campus shell and the static pages."""

from __future__ import annotations

import html

CONTACT = "https://cyphermonkeylabs.com/#contact"
LABS_HOME = "https://cyphermonkeylabs.com"
REPO = "https://github.com/cipher0x9/ai-lab-free-university-mesmerizing"
ISSUES = "https://github.com/cipher0x9/ai-lab-free-university-mesmerizing/issues"

LINKS = (
    ("Labs", LABS_HOME),
    ("Links", "https://linktr.ee/cyphermonkey"),
    ("Repo", ISSUES),
    ("dev.to", "https://dev.to/cyphermonkey"),
    ("Hugging Face", "https://huggingface.co/Cypher0x9"),
    ("X", "https://x.com/Cypher0x9"),
)

NEXT_LABS = (
    ("UC Lab", "https://github.com/cipher0x9/uc-lab-free-university-mesmerizing"),
    ("Webex", "https://github.com/cipher0x9/webex-lab-free-university-mesmerizing"),
    ("Five9", "https://github.com/cipher0x9/five9-lab-free-university-mesmerizing"),
    ("NICE CXone", "https://github.com/cipher0x9/nice-cxone-lab-free-university-mesmerizing"),
    ("Genesys", "https://github.com/cipher0x9/genesys-cloud-lab-free-university-mesmerizing"),
    ("Amazon Connect", "https://github.com/cipher0x9/amazon-connect-lab-free-university-mesmerizing"),
    ("Microsoft Voice", "https://github.com/cipher0x9/microsoft-voice-cc-lab-free-university-mesmerizing"),
    ("SIP Universe", "https://github.com/cipher0x9/sip-universe-lab-free-university-mesmerizing"),
    ("Gemini gems", "https://github.com/cipher0x9/gemini-gems-free-gallery"),
)

DISCLAIMER = (
    "Independent educational project, not affiliated with or endorsed by any vendor. "
    "Trademarks belong to their owners. MIT code, CC BY-NC-SA content."
)


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def link_row() -> str:
    parts = []
    for label, href in LINKS:
        hint = "Rate, comment, or help" if label == "Repo" else label
        parts.append(f'<a href="{esc(href)}">{esc(hint if label == "Repo" else label)}</a>')
    return "".join(parts)


def next_strip() -> str:
    items = "".join(f'<a href="{esc(href)}">{esc(name)}</a>' for name, href in NEXT_LABS)
    return f'<nav class="next-labs" aria-label="Other labs"><span>Next lab</span>{items}</nav>'


def topbar() -> str:
    return f"""
<div class="labbar">
  <a class="mascot" href="#home" aria-label="CypherMonkey, home">
    <svg class="monkey" viewBox="0 0 64 64" aria-hidden="true">
      <g class="monkey-face face-a"><circle cx="32" cy="34" r="16" fill="#F6C453"/><circle cx="18" cy="22" r="8" fill="#E7A23A"/><circle cx="46" cy="22" r="8" fill="#E7A23A"/><circle cx="26" cy="32" r="2.2" fill="#1C1408"/><circle cx="38" cy="32" r="2.2" fill="#1C1408"/><path d="M28 40c2 2 6 2 8 0" stroke="#1C1408" stroke-width="1.6" fill="none" stroke-linecap="round"/></g>
      <g class="monkey-face face-b"><circle cx="32" cy="34" r="16" fill="#7CDEFF"/><circle cx="18" cy="22" r="8" fill="#3DB7E8"/><circle cx="46" cy="22" r="8" fill="#3DB7E8"/><circle cx="26" cy="32" r="2.2" fill="#06202A"/><circle cx="38" cy="32" r="2.2" fill="#06202A"/><path d="M27 41h10" stroke="#06202A" stroke-width="1.6" stroke-linecap="round"/></g>
      <g class="monkey-face face-c"><circle cx="32" cy="34" r="16" fill="#F472B6"/><circle cx="18" cy="22" r="8" fill="#FB7185"/><circle cx="46" cy="22" r="8" fill="#FB7185"/><circle cx="26" cy="31" r="2.4" fill="#2A0A18"/><circle cx="38" cy="31" r="2.4" fill="#2A0A18"/><path d="M28 42c2-2 6-2 8 0" stroke="#2A0A18" stroke-width="1.6" fill="none" stroke-linecap="round"/></g>
      <g class="monkey-face face-d"><circle cx="32" cy="34" r="16" fill="#C4F54A"/><circle cx="18" cy="22" r="8" fill="#86EFAC"/><circle cx="46" cy="22" r="8" fill="#86EFAC"/><circle cx="26" cy="32" r="2" fill="#14210A"/><circle cx="38" cy="32" r="2" fill="#14210A"/><path d="M28 39c2.4 3 6 3 8.2 0" stroke="#14210A" stroke-width="1.6" fill="none" stroke-linecap="round"/></g>
    </svg>
    <span>CypherMonkey</span>
  </a>
  <nav class="labbar-links" aria-label="CypherMonkey">{link_row()}</nav>
  <a class="labbar-dl" id="offlineBtn" href="../downloads/ai-lab-university.html.zip">Download offline</a>
</div>
"""


def footer() -> str:
    return f"""
<footer class="labfoot">
  <p><strong>CYPHER0X9</strong></p>
  <p>{esc(DISCLAIMER)}</p>
  <p class="labfoot-links">
    <a href="{esc(CONTACT)}">Report a concern or request a takedown</a>
    <a href="{esc(CONTACT)}">Work with us</a>
    <a href="{esc(REPO)}">This repository</a>
  </p>
  {next_strip()}
  <p class="labfoot-note">The contact links go to the form on cyphermonkeylabs.com. This page does not show an email address.</p>
</footer>
"""


def extra_nav() -> str:
    return (
        '<a class="ll" href="#downloads" data-search="downloads cheat sheets pdf flashcards offline bundle">'
        '<span class="ln">Get</span><span class="nav-ico"></span><span>Cheat codes</span></a>'
        '<a class="ll" href="#arcade" data-search="arcade ports game flow map call flow daily challenge badges">'
        '<span class="ln">Play</span><span class="nav-ico"></span><span>Arcade</span></a>'
        '<a class="ll" href="#school-EX" data-search="ecosystem glossary mind map sister technologies">'
        '<span class="ln">EX</span><span class="nav-ico"></span><span>Ecosystem</span></a>'
    )


CHROME_CSS = r"""
.labbar {
  display: flex; gap: 10px; align-items: center; flex-wrap: wrap;
  padding: 8px 12px; border-bottom: 1px solid var(--line);
  background: color-mix(in srgb, var(--side) 88%, transparent);
  position: sticky; top: 0; z-index: 50;
}
.labbar-links { display: flex; gap: 8px; flex-wrap: wrap; min-width: 0; }
.labbar-links a, .labbar-dl, .labfoot a, .next-labs a {
  color: var(--link); font-size: 13px; font-weight: 700; text-decoration: none;
}
.labbar-dl {
  margin-left: auto; border: 1px solid var(--line); border-radius: 999px;
  padding: 6px 10px; background: var(--card);
}
.mascot { display: inline-flex; align-items: center; gap: 8px; color: var(--ink); text-decoration: none; font-weight: 800; }
.monkey { width: 36px; height: 36px; }
.monkey-face { transform-origin: 32px 34px; }
.face-b, .face-c, .face-d { display: none; }
html[data-mascot="1"] .face-a { display: none; }
html[data-mascot="1"] .face-b { display: block; }
html[data-mascot="2"] .face-a, html[data-mascot="2"] .face-b { display: none; }
html[data-mascot="2"] .face-c { display: block; }
html[data-mascot="3"] .face-a, html[data-mascot="3"] .face-b, html[data-mascot="3"] .face-c { display: none; }
html[data-mascot="3"] .face-d { display: block; }
html[data-motion="full"] .monkey { animation: bob 3.2s ease-in-out infinite; }
@keyframes bob { 50% { transform: translateY(-2px); } }
.labfoot { margin-top: 28px; padding-top: 16px; border-top: 1px solid var(--line); color: var(--muted); font-size: 14px; max-width: 78ch; }
.labfoot-links, .next-labs { display: flex; flex-wrap: wrap; gap: 8px 12px; margin: 8px 0; }
.next-labs span { font-weight: 800; color: var(--ink); }
.origin-diagram { width: 100%; height: auto; border-radius: 16px; }
.cheat-grid, .game-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; }
.cheat-card, .port-choice, .flow-node {
  display: block; border: 1px solid var(--line); border-radius: 16px; padding: 12px;
  background: var(--card); color: inherit; text-decoration: none;
}
.port-choice, .flow-node, .badge { cursor: pointer; font: inherit; text-align: left; }
.port-choice[aria-pressed="true"] { border-color: var(--primary); }
.flow-node.on { outline: 2px solid var(--cyan); }
.port-hit { border-color: var(--green); }
.port-miss { border-color: var(--rose); }
.flow-map-wrap { max-width: 100%; overflow-x: auto; }
.flow-map { width: 100%; max-width: 980px; height: auto; background: var(--card); border: 1px solid var(--line); border-radius: 16px; }
.map-line, .map-node rect, .map-node text { stroke: currentColor; fill: none; }
.map-node text { fill: currentColor; stroke: none; font: 600 14px system-ui, sans-serif; }
.map-line { opacity: 0.55; }
.map-stop { stroke: var(--rose); stroke-dasharray: 5 4; fill: none; }
.map-stop-node rect { stroke: var(--rose); }
.map-node { cursor: pointer; }
.map-node.on rect { stroke: var(--primary); stroke-width: 2; }
.badge-row { display: flex; flex-wrap: wrap; gap: 8px; }
.badge { border: 1px dashed var(--line); border-radius: 999px; padding: 6px 10px; background: transparent; color: var(--muted); }
.badge.on { border-style: solid; color: var(--ink); border-color: var(--green); }
.share-card { border: 1px solid var(--line); border-radius: 16px; padding: 16px; background: var(--card-2); }
html[data-theme="dark"] { color-scheme: dark; }
html[data-theme="futuristic"] {
  --bg: #070b16; --side: #050814; --card: #10182c; --card-2: #17233d;
  --ink: #e7f6ff; --muted: #93b4c9; --line: #1e3a52;
  --primary: #22d3ee; --primary-2: #67e8f9; --link: #a5f3fc; --on-primary: #042028;
  --cyan: #22d3ee; --green: #34d399; --amber: #fbbf24; --rose: #fb7185;
}
html[data-theme="futuristic"] body { background-image: radial-gradient(circle at 10% -10%, rgba(34,211,238,.16), transparent 36%); }
html[data-theme="gaming"] {
  --bg: #14081f; --side: #0d0616; --card: #241033; --card-2: #311848;
  --ink: #f8f1ff; --muted: #d4b4f5; --line: #6d28d9;
  --primary: #e879f9; --primary-2: #f0abfc; --link: #d9f99d; --on-primary: #2e1065;
  --cyan: #22d3ee; --green: #a3e635; --amber: #facc15; --rose: #fb7185;
}
html[data-theme="gaming"] .track-card, html[data-theme="gaming"] .cheat-card { box-shadow: 4px 4px 0 #6d28d9; }
html[data-theme="neon"] {
  --bg: #050505; --side: #000; --card: #111; --card-2: #1a1a1a;
  --ink: #f8fafc; --muted: #a1a1aa; --line: #27272a;
  --primary: #f0abfc; --primary-2: #22d3ee; --link: #67e8f9; --on-primary: #09090b;
  --cyan: #22d3ee; --green: #4ade80; --amber: #fde047; --rose: #fb7185;
}
html[data-theme="neon"] .labbar { box-shadow: inset 0 -1px 0 #22d3ee; }
html[data-egg="1"] .mascot { filter: drop-shadow(0 0 8px var(--primary)); }
@media (max-width: 720px) {
  .labbar-dl { margin-left: 0; }
  .labbar-links { width: 100%; overflow-x: auto; flex-wrap: nowrap; }
  .pager { left: 0; }
  .flow-map { width: 980px; max-width: none; }
}
@media (prefers-reduced-motion: reduce) {
  .monkey { animation: none !important; }
}
"""


def static_page_chrome() -> str:
    """Chrome for the small HTML pages that are not the generated shell."""
    return f"""
<style>
.labbar{{display:flex;gap:8px;flex-wrap:wrap;align-items:center;padding:8px 12px;background:#0b1020;color:#e8eef9;font:14px system-ui,sans-serif}}
.labbar a{{color:#a5f3fc;font-weight:700;text-decoration:none;margin-right:8px}}
.labfoot{{padding:16px 12px 32px;color:#334155;font:14px/1.5 system-ui,sans-serif}}
.labfoot a{{margin-right:10px}}
</style>
{topbar()}
"""
