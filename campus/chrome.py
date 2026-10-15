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
""" + phone_chrome()


def phone_chrome() -> str:
    sections = (
        ("#home", "Learn"),
        ("#map", "Track map"),
        ("#atlas", "Diagrams"),
        ("#flows", "Flows"),
        ("#charts", "Charts"),
        ("#downloads", "Cheat Codes"),
        ("#play", "Play"),
        ("#school-EX", "Ecosystem"),
        ("#downloads", "Downloads"),
        ("#EX-11", "Careers"),
        ("#arcade", "Arcade"),
        ("#regions", "Regions"),
        ("#studio", "Studio"),
        ("#builds", "Builds"),
    )
    links = "".join(
        f'<a href="{esc(href)}" data-section="{esc(href)}">{esc(label)}</a>'
        for href, label in sections
    )
    themes = (
        ("neon", "Neon"),
        ("holographic", "Holographic"),
        ("cyberpunk", "Cyberpunk"),
        ("sunset", "Sunset"),
        ("light", "Light"),
    )
    theme_buttons = "".join(
        f'<button type="button" data-set-theme="{esc(name)}">{esc(label)}</button>'
        for name, label in themes
    )
    return f"""
<header class="phone-bar">
  <a class="phone-logo" href="#home" aria-label="AI Lab, home">
    <svg class="mark" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#6366F1"/><circle cx="16" cy="16" r="2.4" fill="#fff"/><circle cx="8" cy="16" r="1.7" fill="#fff"/><circle cx="24" cy="16" r="1.7" fill="#fff"/><circle cx="16" cy="8" r="1.7" fill="#fff"/><circle cx="16" cy="24" r="1.7" fill="#fff"/></svg>
    <span>AI Lab</span>
  </a>
  <button type="button" id="phoneMenuBtn" aria-expanded="false" aria-controls="phoneSheet">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    <span>Menu</span>
  </button>
</header>
<div id="phoneSheet" class="phone-sheet" hidden role="dialog" aria-modal="true" aria-labelledby="phoneSheetTitle">
  <div class="phone-sheet-head">
    <h2 id="phoneSheetTitle">Menu</h2>
    <button type="button" id="phoneClose">Close</button>
  </div>
  <nav class="phone-sections" aria-label="Sections">{links}</nav>
  <h3 class="sheet-label">Tracks</h3>
  <nav id="phoneTracks" class="phone-sections" aria-label="Tracks"></nav>
  <h3 class="sheet-label">Language and theme</h3>
  <label class="sheet-lang">Language
    <select data-lang-select aria-label="Language">
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
  <div class="sheet-themes" role="group" aria-label="Theme">{theme_buttons}</div>
  <button type="button" id="phoneSettingsBtn" data-open-settings>Settings</button>
</div>
<nav class="quickbar" aria-label="Quick">
  <a href="#home" data-quick="home">Learn</a>
  <a href="#atlas" data-quick="atlas">Diagrams</a>
  <a href="#play" data-quick="play">Play</a>
  <button type="button" id="quickMenu">Menu</button>
  <a href="#home" id="quickListen" data-quick="listen">Listen</a>
</nav>
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
    <a href="{esc(ISSUES)}">Rate, comment, or help</a>
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
    links = "".join(
        f'<a class="ll feature-link" href="{href}" data-search="{search}">'
        f'<span class="ln">{code}</span><span class="nav-ico"></span><span>{label}</span></a>'
        for href, code, label, search in items
    )
    return links + (
        '<button type="button" class="settings-link" id="sideSettings" data-open-settings>'
        "Settings</button>"
    )


CHROME_CSS = r"""
.labbar {
  display: flex; gap: 8px; align-items: center; flex-wrap: nowrap;
  height: 46px; max-height: 46px; overflow-x: auto; overflow-y: hidden;
  padding: 0 12px; border-bottom: 1px solid var(--line);
  background: var(--side);
  position: sticky; top: 0; z-index: 70;
}
.labbar > * { flex: 0 0 auto; }
.labbar-links { display: flex; gap: 8px; flex-wrap: nowrap; min-width: 0; }
.labbar-links a, .labbar-dl, .labfoot a, .next-labs a {
  color: var(--link); font-size: 13px; font-weight: 700; text-decoration: none;
}
.labbar-dl {
  margin-left: auto; border: 1px solid var(--line); border-radius: 999px;
  padding: 6px 10px; background: var(--card);
}
.mascot { display: inline-flex; align-items: center; gap: 8px; color: var(--ink); text-decoration: none; font-weight: 800; }
.monkey { width: 28px; height: 28px; }
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
.course-menu { display: flex; flex-wrap: nowrap; gap: 8px; width: auto; order: -1; padding-bottom: 0; }
.course-menu a { color: var(--ink); background: var(--card); border: 1px solid var(--line); border-radius: 999px; padding: 4px 8px; font-size: 13px; font-weight: 800; white-space: nowrap; }
.theme-switch { display: flex; gap: 6px; flex-wrap: nowrap; }
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
html[data-theme="light"] .monkey { filter: drop-shadow(0 0 8px #ec4899); }
html[data-theme="light"] {
  --cc-bg: #f6e4ff; --cc-surface: #fff5fb; --cc-accent-1: #e879f9; --cc-accent-2: #22d3ee; --cc-accent-3: #fbbf24; --cc-accent-4: #fb7185;
  --bg: #f7e8ff; --side: #f3d9ff; --card: #fff7fd; --card-2: #e7fbff;
  --ink: #3b0764; --muted: #7e22ce; --line: #f0abfc;
  --primary: #d946ef; --primary-2: #0891b2; --link: #6d28d9; --on-primary: #fff7fb;
  --cyan: #06b6d4; --green: #059669; --amber: #d97706; --rose: #e11d48; --violet: #7c3aed;
  --figure: #fde7ff; --code: #2e1064; --shadow: 0 16px 36px rgba(217,70,239,.18);
  color-scheme: light;
}
html[data-theme="light"] body, html[data-theme="light"] .maincol {
  background-image:
    radial-gradient(circle at 8% -10%, rgba(232,121,249,.55), transparent 34%),
    radial-gradient(circle at 92% 0%, rgba(34,211,238,.48), transparent 32%),
    radial-gradient(circle at 70% 100%, rgba(251,113,133,.38), transparent 36%);
  background-color: #f7e8ff;
}
html[data-theme="light"] .labbar, html[data-theme="light"] .top { background: #fbe7ff; }
@keyframes monkey-wave { 0%, 72%, 100% { transform: rotate(0deg); } 82% { transform: rotate(-14deg); } 90% { transform: rotate(10deg); } }
.top { background: var(--bg); backdrop-filter: none; border-bottom: 1px solid var(--line); top: var(--labbar-h, 46px); z-index: 45; height: 44px; max-height: 44px; padding: 0 16px; overflow: hidden; }
.top .icon-btn { width: 34px; height: 34px; }
.top .icon-btn.text-btn { height: 34px; padding: 0 10px; }
#content { max-width: none; padding: 0 0 120px; }
#stage > :not(#home) { padding: 22px 28px 0; }
#home > .block { padding-left: 28px; padding-right: 28px; }
.hero-stage { position: relative; min-height: calc(100dvh - var(--labbar-h, 46px) - 44px); display: block; overflow: hidden; }
.hero-world { position: absolute !important; inset: 0; height: auto !important; margin: 0 !important; border: 0 !important; border-radius: 0 !important; background: transparent !important; }
.hero-world .fail-toggles { top: 12px; bottom: auto; left: auto; right: 12px; width: auto; justify-content: flex-end; }
.hero-copy {
  position: absolute; z-index: 2; left: 28px; bottom: 28px; width: min(640px, 58%);
  margin: 0; padding: 0; border: 0; border-radius: 0;
  background: transparent; box-shadow: none;
}
.hero-copy .eyebrow, .hero-copy .lede, .hero-copy .stats { display: none; }
.hero-copy .hero-actions a:nth-child(n+3) { display: none; }
.hero-copy .lede { font-size: 1rem; margin-bottom: 8px; max-width: 34ch; text-shadow: 0 2px 16px rgba(0,0,0,.85); }
.hero-copy h1 {
  font-size: clamp(2rem, 4.2vw, 3.5rem); margin-bottom: 6px;
  text-shadow: 0 0 28px color-mix(in srgb, var(--primary) 85%, transparent), 0 10px 28px rgba(0,0,0,.8);
}
.hero-copy .eyebrow, .hero-copy .stats dt, .hero-copy .stats dd { text-shadow: 0 2px 12px rgba(0,0,0,.8); }
.hero-copy .btn, .hero-copy .btn.primary {
  background: transparent; border-color: transparent; box-shadow: none;
  color: var(--cyan); padding: 0 10px 0 0;
  text-shadow: 0 0 14px color-mix(in srgb, var(--cyan) 80%, transparent);
}
.hero-world .fail-toggles button {
  background: transparent; border-color: transparent; color: var(--cyan);
  text-shadow: 0 0 10px var(--cyan);
}
.iso-icon { width: 72px; height: 72px; filter: drop-shadow(0 12px 10px color-mix(in srgb, var(--primary) 45%, transparent)); }
.gem-host { position: relative; display: grid; place-items: center; width: 72px; height: 72px; flex: 0 0 72px; filter: drop-shadow(0 0 12px color-mix(in srgb, var(--primary) 75%, transparent)); }
.gem-canvas { width: 72px; height: 72px; display: block; }
html.gems-on .iso-icon { display: none; }
.track-grid, .launch-grid { perspective: 900px; }
.track-card, .launch-card { transform-style: preserve-3d; }
.track-card .idx, .track-card .meta, .stats dd { font-variant-numeric: tabular-nums; }
.track-card, .launch-card, .cheat-card, .atlas-card, .continue-card {
  background: color-mix(in srgb, var(--card) 88%, transparent);
  border: 1px solid color-mix(in srgb, var(--primary) 55%, var(--line));
  box-shadow: 0 10px 28px rgba(0,0,0,.22);
  transition: transform .18s ease, box-shadow .18s ease;
}
.track-card:hover, .launch-card:hover, .atlas-card:hover, .cheat-card:hover {
  transform: translateY(-6px) rotateX(6deg) rotateY(-8deg);
  box-shadow: 0 16px 36px color-mix(in srgb, var(--primary) 55%, transparent), 0 0 24px color-mix(in srgb, var(--cyan) 35%, transparent);
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
  .app { grid-template-columns: 1fr; }
  .only-mobile { display: inline-flex; }
  #sidebar {
    position: fixed; z-index: 40; top: 0; height: 100vh; transform: translateX(-105%);
    width: min(340px, 90vw); box-shadow: var(--shadow);
  }
  body.nav-open #sidebar { transform: none; }
  body.nav-open #scrim { display: block; position: fixed; inset: 0; background: rgba(5,8,16,.55); z-index: 35; }
  .pager { left: 0; }
  .hero-copy { width: min(420px, 62%); left: 16px; bottom: 16px; max-height: 28vh; overflow: hidden; padding: 0; }
  .hero-copy .lede { display: none; }
  .hero-copy .hero-actions a:nth-child(n+3) { display: none; }
  .hero-copy h1 { font-size: clamp(1.7rem, 4vw, 2.4rem); margin-bottom: 8px; }
  .stats { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 6px 8px; margin-top: 8px; }
  .stats div { min-width: 0; }
  .stats dd { font-size: 1.05rem; }
  .track-grid, .launch-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .gem-host, .iso-icon { width: 72px; height: 72px; }
}
.rail-btn {
  display: none; width: 36px; height: 36px; margin: 0 auto 8px; padding: 0;
  border: 1px solid var(--line); border-radius: 10px; background: transparent; color: var(--ink); cursor: pointer;
}
.rail-btn svg { width: 18px; height: 18px; stroke: currentColor; fill: none; stroke-width: 1.8; stroke-linecap: round; }
@media (min-width: 1101px) {
  .rail-btn { display: inline-flex; align-items: center; justify-content: center; }
  html:not([data-rail="open"]) { --side-w: 72px; }
  html:not([data-rail="open"]) #sidebar { padding: 10px 6px 24px; }
  html:not([data-rail="open"]) #sidebar .brand > span,
  html:not([data-rail="open"]) #sidebar .side-progress p,
  html:not([data-rail="open"]) #sidebar .search,
  html:not([data-rail="open"]) #sidebar .search-meta,
  html:not([data-rail="open"]) #sidebar .sname,
  html:not([data-rail="open"]) #sidebar .scount,
  html:not([data-rail="open"]) #sidebar .chev,
  html:not([data-rail="open"]) #sidebar .lesson-links,
  html:not([data-rail="open"]) #sidebar a.ll > span:last-child { display: none; }
  html:not([data-rail="open"]) #sidebar .school-jump {
    grid-template-columns: 1fr; justify-items: center; padding: 6px 0;
  }
  html:not([data-rail="open"]) #sidebar .brand,
  html:not([data-rail="open"]) #sidebar .side-progress { justify-content: center; }
  html:not([data-rail="open"]) #sidebar a.ll { display: flex; justify-content: center; }
}
@media (max-width: 800px) {
  html { --labbar-h: 34px; }
  .labbar {
    flex-wrap: nowrap; align-items: center; height: 34px; max-height: 34px;
    overflow-x: auto; overflow-y: hidden; padding: 0 8px; gap: 6px;
  }
  .labbar > * { flex: 0 0 auto; }
  .labbar-dl { margin-left: 0; padding: 2px 8px; font-size: 12px; white-space: nowrap; }
  .labbar-links, .course-menu, .theme-switch { width: auto; flex-wrap: nowrap; }
  .course-menu { order: -1; }
  .mascot span, .lang-switch { font-size: 0; }
  .lang-switch select { font-size: 12px; }
  .monkey { width: 22px; height: 22px; }
  .course-menu a, .theme-switch button { padding: 1px 6px; font-size: 11px; }
  .top {
    top: 34px; height: 32px; max-height: 32px; overflow: hidden; flex-wrap: nowrap;
    padding: 0 8px; gap: 4px;
  }
  .top .text-btn, .top .cmd-label, .top kbd { display: none; }
  .top .icon-btn { width: 26px; height: 26px; }
  .hero-stage { min-height: calc(100dvh - 66px); }
  .hero-copy {
    left: 10px; right: auto; bottom: 10px; width: min(250px, 68%);
    max-height: 26vh; overflow: hidden; padding: 10px 12px;
  }
  .hero-copy .eyebrow, .hero-copy .lede, .hero-copy .stats { display: none; }
  .hero-copy .hero-actions a:nth-child(n+3) { display: none; }
  .hero-copy h1 { font-size: 1.2rem; line-height: 1.15; margin: 0 0 8px; }
  .hero-world .fail-toggles button { padding: 2px 6px; font-size: 11px; }
  .pager { left: 0; }
  .flow-map { width: 980px; max-width: none; }
  .track-grid, .launch-grid { grid-template-columns: 1fr; }
  #sidebar a.ll, #sidebar .school-jump, #sidebar .settings-link { min-height: 48px; }
}
.phone-bar, .phone-sheet, .quickbar { display: none; }
.settings-link {
  display: flex; align-items: center; width: calc(100% - 8px); margin: 10px 4px 0;
  min-height: 48px; padding: 8px 12px; border: 1px solid var(--line); border-radius: 12px;
  background: transparent; color: var(--ink); font: inherit; font-weight: 750; cursor: pointer; text-align: start;
}
.phone-bar {
  align-items: center; justify-content: space-between; gap: 12px;
  height: calc(56px + env(safe-area-inset-top)); max-height: calc(64px + env(safe-area-inset-top));
  padding: env(safe-area-inset-top) 12px 0;
  background: var(--bg); border-bottom: 1px solid var(--line); color: var(--ink);
}
.phone-logo { display: inline-flex; align-items: center; gap: 8px; color: var(--ink); text-decoration: none; font-weight: 800; min-height: 48px; }
.phone-logo .mark { width: 28px; height: 28px; }
#phoneMenuBtn, #phoneClose, #phoneSettingsBtn, .quickbar a, .quickbar button, .sheet-themes button {
  min-height: 48px; min-width: 48px;
}
#phoneMenuBtn, #quickMenu {
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  border: 1px solid var(--line); border-radius: 12px; background: transparent; color: var(--ink);
  font: inherit; font-weight: 800; padding: 0 14px; cursor: pointer;
}
#phoneMenuBtn svg, #quickMenu svg { width: 22px; height: 22px; stroke: currentColor; fill: none; stroke-width: 1.8; stroke-linecap: round; }
.phone-sheet {
  position: fixed; inset: 0; z-index: 80; flex-direction: column; gap: 8px;
  background: var(--bg); color: var(--ink); overflow-x: hidden; overflow-y: auto;
  padding: calc(12px + env(safe-area-inset-top)) 16px calc(16px + env(safe-area-inset-bottom));
  overscroll-behavior: contain;
}
.phone-sheet[hidden] { display: none !important; }
.phone-sheet-head { display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; background: var(--bg); z-index: 1; padding-bottom: 8px; }
.phone-sheet-head h2 { margin: 0; font-size: 1.3rem; }
#phoneClose, #phoneSettingsBtn {
  border: 1px solid var(--line); border-radius: 12px; background: transparent; color: var(--ink);
  font: inherit; font-weight: 800; padding: 0 16px; cursor: pointer;
}
.phone-sections { display: flex; flex-direction: column; gap: 6px; }
.phone-sections a {
  display: flex; align-items: center; min-height: 48px; padding: 0 14px; border-radius: 12px;
  color: var(--ink); text-decoration: none; font-weight: 750; border: 1px solid transparent;
}
.phone-sections a[aria-current="page"] {
  background: color-mix(in srgb, var(--primary) 24%, transparent);
  border-color: var(--primary); color: var(--ink);
}
.sheet-label { margin: 12px 0 0; font-size: 0.8rem; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
.sheet-lang { display: flex; flex-direction: column; gap: 6px; font-weight: 750; }
.sheet-lang select, .sheet-themes { width: 100%; }
.sheet-lang select { min-height: 48px; font: inherit; color: var(--ink); background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 0 12px; }
.sheet-themes { display: flex; flex-wrap: wrap; gap: 8px; }
.sheet-themes button {
  border: 1px solid var(--line); border-radius: 999px; background: transparent; color: var(--ink);
  font: inherit; font-weight: 750; padding: 0 14px; cursor: pointer;
}
#phoneSettingsBtn { width: 100%; margin-top: 8px; }
.quickbar {
  position: fixed; z-index: 55; left: 0; right: 0; bottom: 0;
  grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 2px;
  padding: 4px 6px calc(4px + env(safe-area-inset-bottom));
  background: var(--bg); border-top: 1px solid var(--line);
}
.quickbar a, .quickbar button {
  display: flex; align-items: center; justify-content: center; border: 0; background: transparent;
  color: var(--muted); font: inherit; font-size: 12px; font-weight: 800; text-decoration: none; cursor: pointer;
  border-radius: 10px;
}
.quickbar a[aria-current="page"] { color: var(--cyan); background: color-mix(in srgb, var(--primary) 18%, transparent); }
.reveal { opacity: 0; transform: translateY(18px); transition: opacity .5s ease, transform .5s ease; }
.reveal.is-revealed { opacity: 1; transform: none; }
@media (max-width: 720px) {
  html, body { overflow-x: clip; }
  html { scroll-padding-top: 64px; scroll-padding-bottom: 80px; }
  .labbar, .top, .dock { display: none !important; }
  .phone-bar { display: flex; position: fixed; top: 0; left: 0; right: 0; z-index: 60; }
  .phone-sheet:not([hidden]) { display: flex; }
  .quickbar { display: grid; }
  .app { padding-top: calc(56px + env(safe-area-inset-top)); }
  .hero-stage { min-height: calc(100dvh - 56px - 64px - env(safe-area-inset-top) - env(safe-area-inset-bottom)); }
  #content { padding-bottom: calc(88px + env(safe-area-inset-bottom)); }
  .pager { bottom: calc(64px + env(safe-area-inset-bottom)); }
  .hero-copy {
    left: 12px; right: 12px; bottom: 8px; width: auto; max-height: none; overflow: visible;
    padding: 28px 14px 12px; border-radius: 18px;
    background: linear-gradient(180deg, rgba(5,2,16,0) 0px, rgba(5,2,16,0.96) 20px, rgba(6,3,18,0.98) 100%);
  }
  .hero-copy h1 {
    color: #f8f7ff; text-shadow: none; font-size: 1.35rem; line-height: 1.2; margin: 0 0 12px;
  }
  .hero-copy .hero-actions { display: flex; flex-wrap: wrap; gap: 8px; }
  .hero-copy .btn, .hero-copy .btn.primary {
    display: inline-flex; align-items: center; justify-content: center;
    min-height: 48px; padding: 0 16px; border-radius: 12px; text-shadow: none;
    text-decoration: none; font-weight: 750;
  }
  .hero-copy .btn.primary { background: #4f46e5; color: #ffffff; border: 1px solid #4f46e5; }
  .hero-copy .btn { background: #100d1c; color: #f8fafc; border: 1px solid #c7d2fe; }
  .hero-world .fail-toggles {
    top: 10px; left: 8px; right: auto; width: max-content; max-width: calc(100% - 16px);
    justify-content: flex-start; padding: 4px; border-radius: 12px;
    background: rgba(6, 3, 18, 0.92);
  }
  .hero-world .fail-toggles button {
    background: rgba(6, 3, 18, 0.92); color: #e8edf7; border: 1px solid rgba(199, 210, 254, 0.55);
    text-shadow: none; padding: 6px 10px; font-size: 12px;
  }
  body.sheet-open { overflow: hidden; }
}
@media (prefers-reduced-motion: reduce) {
  .reveal { opacity: 1; transform: none; transition: none; }
}
html[data-motion="reduce"] .reveal { opacity: 1; transform: none; transition: none; }
html[data-motion="reduce"] { scroll-behavior: auto; }
@media (prefers-reduced-motion: reduce) {
  .monkey, .hero-art, .tilt-card { animation: none !important; }
  .pkt, .atlas-svg animateMotion { display: none; }
  .tilt-card, .track-card:hover, .launch-card:hover { transform: none; }
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
