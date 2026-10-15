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
    ("UC Lab", "https://cipher0x9.github.io/uc-lab-free-university-mesmerizing/"),
    ("Webex", "https://cipher0x9.github.io/webex-lab-free-university-mesmerizing/"),
    ("Five9", "https://cipher0x9.github.io/five9-lab-free-university-mesmerizing/"),
    ("NICE CXone", "https://cipher0x9.github.io/nice-cxone-lab-free-university-mesmerizing/"),
    ("Genesys", "https://cipher0x9.github.io/genesys-cloud-lab-free-university-mesmerizing/"),
    ("Amazon Connect", "https://cipher0x9.github.io/amazon-connect-lab-free-university-mesmerizing/"),
    ("Microsoft Voice", "https://cipher0x9.github.io/microsoft-voice-cc-lab-free-university-mesmerizing/"),
    ("SIP Universe", "https://cipher0x9.github.io/sip-universe-lab-free-university-mesmerizing/"),
    ("Gemini gems", "https://cipher0x9.github.io/gemini-gems-free-gallery/"),
)

COURSE_MENU = (
    ("Diagrams", "#atlas", "atlas"),
    ("Flows", "#flows", "flows"),
    ("Charts", "#charts", "charts"),
    ("Cheat Codes", "#downloads", "downloads"),
    ("Play", "#play", "play"),
    ("Ecosystem", "#school-EX", "school"),
    ("Downloads", "#downloads", "downloads"),
    ("Careers", "#EX-11", "lesson"),
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
  <nav class="course-menu" aria-label="Course sections">{course_links()}</nav>
  <div class="theme-switch" role="group" aria-label="Theme">
    <button type="button" data-set-theme="neon">Neon</button>
    <button type="button" data-set-theme="holographic">Holographic</button>
    <button type="button" data-set-theme="cyberpunk">Cyberpunk</button>
    <button type="button" data-set-theme="sunset">Sunset</button>
    <button type="button" data-set-theme="light">Light</button>
  </div>
  <label class="lang-switch">Language
    <select id="langSelect" data-lang-select aria-label="Language">
      <option value="en">English</option>
      <option value="es">Español</option>
      <option value="hi">हिन्दी</option>
      <option value="te">తెలుగు</option>
      <option value="fr">Français</option>
      <option value="de">Deutsch</option>
      <option value="ja">日本語</option>
      <option value="ar">العربية</option>
    </select>
  </label>
</div>
"""


def course_links() -> str:
    keys = {
        "Diagrams": "nav-diagrams",
        "Flows": "nav-flows",
        "Charts": "nav-charts",
        "Cheat Codes": "nav-cheats",
        "Play": "nav-play",
        "Ecosystem": "nav-ecosystem",
        "Downloads": "nav-downloads",
        "Careers": "nav-careers",
    }
    return "".join(
        f'<a href="{esc(href)}" data-dock="{esc(dock)}" data-i18n="{keys[label]}">{esc(label)}</a>'
        for label, href, dock in COURSE_MENU
    )


def footer() -> str:
    return f"""
<footer class="labfoot">
  <p><strong>CYPHER0X9</strong></p>
  <p>{esc(DISCLAIMER)} <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a></p>
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
    items = [
        ("#atlas", "Map", "Diagrams", "diagrams atlas svg flows"),
        ("#flows", "Go", "Flows", "animated call signal data flows ladder"),
        ("#charts", "No", "Charts", "charts counts d3"),
        ("#downloads", "Get", "Cheat Codes", "cheat codes sheets pdf png flashcards"),
        ("#play", "Lab", "Play", "playgrounds practice"),
        ("#school-EX", "EX", "Ecosystem", "ecosystem sister technologies"),
        ("#downloads", "Zip", "Downloads", "offline zip bundle download"),
        ("#EX-11", "Job", "Careers", "career certification interview"),
        ("#regions", "Map", "Regions", "regions countries residency flags"),
        ("#arcade", "Arc", "Arcade", "arcade ports game"),
    ]
    return "".join(
        f'<a class="ll feature-link" href="{href}" data-search="{search}">'
        f'<span class="ln">{code}</span><span class="nav-ico"></span><span>{label}</span></a>'
        for href, code, label, search in items
    )


CHROME_CSS = r"""
.labbar {
  display: flex; gap: 8px; align-items: center; flex-wrap: wrap;
  padding: 6px 12px; border-bottom: 1px solid var(--line);
  background: var(--side);
  position: sticky; top: 0; z-index: 70;
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
.course-menu { display: flex; flex-wrap: wrap; gap: 8px; width: 100%; padding-bottom: 2px; }
.course-menu a { color: var(--ink); background: var(--card); border: 1px solid var(--line); border-radius: 999px; padding: 6px 10px; font-weight: 800; white-space: nowrap; }
.theme-switch { display: flex; gap: 6px; flex-wrap: wrap; }
.theme-switch button { font: inherit; color: var(--ink); background: transparent; border: 1px solid var(--line); border-radius: 999px; padding: 4px 8px; cursor: pointer; }
.feature-link { font-weight: 800; }
.fold-menu { display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0; }
.fold-menu a { color: var(--ink); background: var(--card); border: 1px solid var(--primary); border-radius: 12px; padding: 8px 12px; font-weight: 800; text-decoration: none; }
.mascot-variations { display: flex; gap: 8px; align-items: center; margin: 8px 0; }
.mascot-variations svg { width: 36px; height: 36px; }
.parallax-row { display: flex; gap: 12px; overflow-x: auto; perspective: 900px; margin: 12px 0; padding-bottom: 8px; }
.tilt-card { min-width: 120px; border: 1px solid var(--line); border-radius: 16px; padding: 12px; background: var(--card); transform: rotateY(var(--tilt, -6deg)) rotateX(6deg); transform-style: preserve-3d; }
.tilt-card strong { display: block; font-size: 28px; }
.cube { width: 36px; height: 36px; }
.chart-strip, .atlas-grid { display: grid; gap: 12px; }
.real-chart, .atlas-card { border: 1px solid var(--line); border-radius: 16px; padding: 12px; background: var(--card); }
.real-chart svg, .atlas-card svg, .mindmap { width: 100%; height: auto; }
.atlas-card[hidden] { display: none; }
.pkt { fill: #f8fafc; }
.hero-art { animation: hero-float 6s ease-in-out infinite; }
@keyframes hero-float { 50% { transform: translateY(-6px); } }
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
  --cc-bg: #070018; --cc-surface: #14082c; --cc-accent-1: #22d3ee; --cc-accent-2: #e879f9; --cc-accent-3: #facc15; --cc-accent-4: #fb7185;
  --bg: #070018; --side: #050014; --card: #14082c; --card-2: #1d1038;
  --ink: #f5f3ff; --muted: #c4b5fd; --line: #4c1d95;
  --primary: #22d3ee; --primary-2: #e879f9; --link: #a5f3fc; --on-primary: #042028;
  --cyan: #22d3ee; --green: #34d399; --amber: #facc15; --rose: #fb7185; --figure: #0b0418; --code: #070014;
}
html[data-theme="neon"] body { background-image: radial-gradient(circle at 80% 0%, rgba(232,121,249,.28), transparent 32%), radial-gradient(circle at 10% 20%, rgba(34,211,238,.2), transparent 36%); }
html[data-theme="holographic"] {
  --cc-bg: #041418; --cc-surface: #0b242c; --cc-accent-1: #5eead4; --cc-accent-2: #c4b5fd; --cc-accent-3: #f0abfc; --cc-accent-4: #67e8f9;
  --bg: #041418; --side: #021014; --card: rgba(11,36,44,.82); --card-2: #10343d;
  --ink: #ecfeff; --muted: #99f6e4; --line: #155e75;
  --primary: #5eead4; --primary-2: #c4b5fd; --link: #e9d5ff; --on-primary: #042f2e;
  --cyan: #67e8f9; --green: #5eead4; --amber: #f0abfc; --rose: #f9a8d4; --figure: #062026; --code: #021014;
}
html[data-theme="holographic"] body { background-image: linear-gradient(120deg, rgba(94,234,212,.18), rgba(196,181,253,.16) 40%, rgba(244,114,182,.12)); }
html[data-theme="cyberpunk"] {
  --cc-bg: #140014; --cc-surface: #24001c; --cc-accent-1: #f472b6; --cc-accent-2: #facc15; --cc-accent-3: #22d3ee; --cc-accent-4: #e879f9;
  --bg: #120010; --side: #1a0014; --card: #2a001f; --card-2: #3b0428;
  --ink: #fff1f2; --muted: #fda4af; --line: #9d174d;
  --primary: #f472b6; --primary-2: #facc15; --link: #fde68a; --on-primary: #3b0418;
  --cyan: #22d3ee; --green: #bef264; --amber: #facc15; --rose: #fb7185; --figure: #1a0014; --code: #0a0008;
}
html[data-theme="cyberpunk"] body { background-image: repeating-linear-gradient(90deg, rgba(244,114,182,.08) 0 1px, transparent 1px 72px), radial-gradient(circle at 90% 10%, rgba(250,204,21,.2), transparent 28%); }
html[data-theme="sunset"] {
  --cc-bg: #2a0d16; --cc-surface: #3b1420; --cc-accent-1: #fb7185; --cc-accent-2: #fdba74; --cc-accent-3: #fbbf24; --cc-accent-4: #f97316;
  --bg: #2a0d16; --side: #1c0810; --card: #431520; --card-2: #5c1d2a;
  --ink: #fff7ed; --muted: #fdba74; --line: #9a3412;
  --primary: #fb7185; --primary-2: #fdba74; --link: #ffedd5; --on-primary: #431407;
  --cyan: #fdba74; --green: #fde68a; --amber: #fbbf24; --rose: #fb7185; --figure: #2a0d16; --code: #1c0810;
}
html[data-theme="sunset"] body { background-image: linear-gradient(160deg, rgba(251,113,133,.35), rgba(249,115,22,.2) 45%, rgba(253,186,116,.15)); }
html[data-theme="neon"] .labbar, html[data-theme="holographic"] .labbar, html[data-theme="cyberpunk"] .labbar, html[data-theme="sunset"] .labbar { box-shadow: inset 0 -1px 0 var(--primary); }
html:not([data-motion="reduce"]) .monkey { animation: monkey-wave 5.6s ease-in-out infinite; transform-origin: 18px 36px; }
html[data-theme="neon"] .monkey { filter: drop-shadow(0 0 8px #22d3ee); }
html[data-theme="holographic"] .monkey { filter: drop-shadow(0 0 8px #5eead4); }
html[data-theme="cyberpunk"] .monkey { filter: drop-shadow(0 0 8px #facc15); }
html[data-theme="sunset"] .monkey { filter: drop-shadow(0 0 8px #fb7185); }
html[data-theme="light"] .monkey { filter: drop-shadow(0 8px 10px rgba(79,70,229,.35)); }
@keyframes monkey-wave { 0%, 72%, 100% { transform: rotate(0deg); } 82% { transform: rotate(-14deg); } 90% { transform: rotate(10deg); } }
.top { background: var(--bg); backdrop-filter: none; border-bottom: 1px solid var(--line); top: var(--labbar-h, 118px); z-index: 45; }
#content { max-width: none; padding: 0 0 120px; }
#stage > :not(#home) { padding: 22px 28px 0; }
#home > .block { padding-left: 28px; padding-right: 28px; }
.hero-stage { position: relative; min-height: calc(100dvh - var(--labbar-h, 118px) - 64px); display: block; overflow: hidden; }
.hero-world { position: absolute !important; inset: 0; height: auto !important; margin: 0 !important; border: 0 !important; border-radius: 0 !important; background: transparent !important; }
.hero-world .fail-toggles { top: 12px; bottom: auto; left: auto; right: 12px; width: auto; justify-content: flex-end; }
.hero-copy {
  position: absolute; z-index: 2; left: 20px; bottom: 18px; width: min(520px, 46%);
  margin: 0; padding: 16px 16px 12px; border-radius: 22px;
  background: color-mix(in srgb, var(--bg) 72%, transparent);
  border: 1px solid color-mix(in srgb, var(--primary) 70%, transparent);
  box-shadow: 0 0 32px color-mix(in srgb, var(--primary) 28%, transparent);
}
.hero-copy .lede { font-size: 1rem; margin-bottom: 10px; }
.hero-copy h1 { font-size: clamp(1.7rem, 3vw, 2.6rem); }
.iso-icon { width: 72px; height: 72px; filter: drop-shadow(0 12px 10px color-mix(in srgb, var(--primary) 45%, transparent)); }
.track-card, .launch-card, .cheat-card, .atlas-card, .continue-card {
  background: color-mix(in srgb, var(--card) 88%, transparent);
  border: 1px solid color-mix(in srgb, var(--primary) 55%, var(--line));
  box-shadow: 0 10px 28px rgba(0,0,0,.22);
  transition: transform .18s ease, box-shadow .18s ease;
}
.track-card:hover, .launch-card:hover, .atlas-card:hover, .cheat-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 36px color-mix(in srgb, var(--primary) 32%, transparent);
}
.atlas-card svg { min-height: 420px; }
.lightbox-card svg { min-height: 520px; }
.atlas-grid { grid-template-columns: 1fr; }
.lightbox { position: fixed; inset: 0; z-index: 80; background: rgba(2,6,16,.82); display: grid; place-items: center; padding: 24px; }
.lightbox[hidden] { display: none; }
.lightbox-card { width: min(1100px, 100%); max-height: calc(100vh - 48px); overflow: auto; background: var(--card); color: var(--ink); border-radius: 20px; padding: 16px; border: 1px solid var(--primary); }
.lightbox-card svg { width: 100%; height: auto; min-height: 360px; background: #070b16; border-radius: 12px; }
.lang-switch { display: inline-flex; gap: 6px; align-items: center; color: var(--ink); font-size: 13px; font-weight: 800; }
.lang-switch select { font: inherit; color: var(--ink); background: var(--card); border: 1px solid var(--line); border-radius: 999px; padding: 4px 8px; }
.audio-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; }
.audio-studio audio { width: 100%; }
.flag { width: 36px; height: 24px; border-radius: 4px; box-shadow: 0 0 0 1px var(--line); }
.region-table td { vertical-align: middle; }
html[dir="rtl"] .hero-copy, html[dir="rtl"] .labbar { direction: rtl; }
html[data-egg="1"] .mascot { filter: drop-shadow(0 0 8px var(--primary)); }
@media (max-width: 1100px) {
  .hero-copy { width: min(560px, calc(100% - 16px)); left: 8px; max-height: min(420px, 54vh); overflow: auto; }
}
@media (max-width: 800px) {
  .labbar { padding: 4px 8px; gap: 4px; }
  .labbar-dl { margin-left: 0; }
  .labbar-links, .course-menu, .theme-switch { width: 100%; flex-wrap: nowrap; overflow-x: auto; }
  .course-menu a, .theme-switch button { padding: 4px 8px; font-size: 12px; }
  .hero-copy { left: 8px; right: 8px; bottom: 8px; width: auto; max-height: 46vh; overflow: auto; }
  .pager { left: 0; }
  .flow-map { width: 980px; max-width: none; }
}
@media (prefers-reduced-motion: reduce) {
  .monkey, .hero-art, .tilt-card { animation: none !important; }
  .pkt, .atlas-svg animateMotion { display: none; }
  .tilt-card { transform: none; }
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
