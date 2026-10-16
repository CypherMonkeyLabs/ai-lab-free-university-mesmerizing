#!/usr/bin/env python3
"""Headless checks for the offline campus: links, navigation, and no network."""

from __future__ import annotations

import json
import re
import sys
import threading
from functools import partial
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "campus" / "ai-lab-university.html"


class Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.dupes: list[str] = []
        self.hrefs: list[str] = []
        self.external_srcs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        if "id" in data and data["id"]:
            if data["id"] in self.ids:
                self.dupes.append(data["id"])
            self.ids.add(data["id"])
        href = data.get("href", "")
        src = data.get("src", "")
        if tag == "a" and href:
            self.hrefs.append(href)
        if tag in {"script", "img", "iframe"} and src and not src.startswith("data:"):
            self.external_srcs.append(src)
        if tag == "link":
            rel = data.get("rel", "")
            if "stylesheet" in rel or (href and not href.startswith("data:") and not href.startswith("#")):
                self.external_srcs.append(href)


ALLOWED_URL_MARKERS = (
    "127.0.0.1",
    "www.w3.org",
    "github.com/cipher0x9/",
    "github.com/CypherMonkeyLabs/",
    "https://cyphermonkeylabs.com/ai-lab-free-university-mesmerizing/",
    "cyphermonkeylabs.com",
    "cipher0x9.github.io/",
    "arxiv.org/",
    "doi.org/",
    "modelcontextprotocol.io/",
    "platform.openai.com/",
    "docs.anthropic.com/",
    "huggingface.co/",
    "linktr.ee/cyphermonkey",
    "dev.to/cyphermonkey",
    "x.com/Cypher0x9",
    "creativecommons.org/licenses/by-nc-sa/4.0/",
    "airc.nist.gov",
)

# Profile buttons have no trailing slash. Match them exactly so the path
# markers above still require github.com/<owner>/.
EXACT_URLS = {
    "https://github.com/cipher0x9",
    "https://github.com/CypherMonkeyLabs",
}


def url_allowed(url: str) -> bool:
    if url in EXACT_URLS:
        return True
    return any(marker in url for marker in ALLOWED_URL_MARKERS)


def catalog() -> dict:
    return json.loads((ROOT / "campus" / "assets" / "curriculum" / "catalog.json").read_text(encoding="utf-8"))


def static_checks() -> list[str]:
    text = HTML.read_text(encoding="utf-8")
    errors: list[str] = []
    parser = Collector()
    parser.feed(text)
    if parser.dupes:
        errors.append("duplicate ids: " + ", ".join(parser.dupes[:8]))
    remote = [src for src in parser.external_srcs if src.startswith(("http://", "https://", "//"))]
    if remote:
        errors.append("external resources: " + ", ".join(remote))
    urls = re.findall(r"https?://[^\s'\"<>)]+", text)
    bad = [url for url in urls if not url_allowed(url)]
    if bad:
        errors.append("external urls: " + ", ".join(bad[:8]))
    data = catalog()
    routable = set(parser.ids)
    routable.update(data["order"])
    routable.update("school-" + school["id"] for school in data["schools"])
    routable.update("play-" + key for key in data["plays"])
    routable.update({"home", "map", "play", "studio", "builds", "view-missing"})
    visible = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", "", text, flags=re.I)
    if len(re.findall(r"<h1\b", visible, flags=re.I)) != 1:
        errors.append("shell does not have a single h1")
    for href in parser.hrefs:
        if href.startswith("https://") and url_allowed(href):
            continue
        if not href.startswith("#") or href == "#":
            errors.append("non-anchor link: " + href)
            continue
        target = href[1:]
        if target not in routable:
            errors.append("unresolved link: " + href)
    needed = ["home", "menuBtn", "themeBtn", "q", "pagerPrev", "pagerNext", "markBtn", "sourcesBtn", "stage"]
    for item in needed:
        if item not in parser.ids:
            errors.append("missing id: " + item)
    if "googleapis" in text or "jsdelivr" in text or "unpkg" in text:
        errors.append("cdn marker found")
    return errors


def _serve() -> tuple[ThreadingHTTPServer, str]:
    handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f"http://127.0.0.1:{server.server_address[1]}/campus/ai-lab-university.html"


def browser_checks() -> list[str]:
    errors: list[str] = []
    external: list[str] = []
    server, base = _serve()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
            page = browser.new_page(viewport={"width": 1440, "height": 900})

            def on_request(request) -> None:
                url = request.url
                if url.startswith(("data:", "blob:", "about:")):
                    return
                if url.startswith("http://127.0.0.1:"):
                    return
                external.append(url)

            page.on("request", on_request)
            page.goto(base + "#home", wait_until="load")
            page.evaluate("localStorage.clear()")
            page.goto(base + "#home", wait_until="domcontentloaded")
            page.wait_for_selector("#home.active h1")

            def visible_title() -> str:
                return page.locator("[data-panel].active h1").inner_text()

            if "Learn to build" not in visible_title():
                errors.append("home title missing: " + visible_title())
            if page.locator("h1").count() != 1:
                errors.append("home has more than one h1")
            home_nodes = page.evaluate("() => document.getElementsByTagName('*').length")
            if home_nodes > 2000:
                errors.append("home DOM is too large: " + str(home_nodes))

            page.click("a[href='#map']")
            page.wait_for_selector("#map.active")

            schools = page.eval_on_selector_all(
                "a.school-jump[href^='#school-']",
                "els => els.map(e => e.getAttribute('href'))",
            )
            for href in schools:
                page.goto(base + href, wait_until="domcontentloaded")
                page.wait_for_selector(href + ".active")

            lessons = catalog()["order"]
            if len(lessons) < 100:
                errors.append("too few lessons: " + str(len(lessons)))
            for lid in lessons:
                page.goto(base + "#" + lid, wait_until="domcontentloaded")
                page.wait_for_selector("article.lesson.active")
                active = page.locator("article.lesson.active")
                if active.count() != 1 or active.get_attribute("id") != lid:
                    errors.append("lesson nav failed " + lid)
                    break
                if page.locator("a.ll.on").get_attribute("data-id") != lid:
                    errors.append("sidebar did not highlight " + lid)
                    break
                if page.locator("h1").count() != 1:
                    errors.append("lesson view lost the single h1 at " + lid)
                    break

            lesson_nodes = page.evaluate("() => document.getElementsByTagName('*').length")
            if lesson_nodes > 3600:
                errors.append("lesson DOM is too large: " + str(lesson_nodes))

            page.goto(base + "#00-01", wait_until="domcontentloaded")
            page.wait_for_selector("[id='00-01'].active")
            page.click("#pagerNext")
            page.wait_for_selector("[id='00-02'].active")
            page.click("#pagerPrev")
            page.wait_for_selector("[id='00-01'].active")
            if page.locator("#pagerPrev").is_visible():
                errors.append("previous shown on the first lesson")

            page.fill("#q", "Model Context Protocol")
            page.keyboard.press("Enter")
            page.wait_for_selector("[id='07-01'].active")
            if page.locator("article.lesson.active").get_attribute("id") != "07-01":
                errors.append("search did not open MCP lesson, got " + str(page.locator("article.lesson.active").get_attribute("id")))

            before = page.locator("#studiedLabel").inner_text()
            page.click("#markBtn")
            after = page.locator("#studiedLabel").inner_text()
            if before == after or "Completed" not in page.locator("#markBtn").inner_text():
                errors.append("mark complete did not update progress")

            page.goto(base + "#play-guard", wait_until="domcontentloaded")
            page.wait_for_selector("#play-guard:not([hidden])")
            page.goto(base + "#play-embed", wait_until="domcontentloaded")
            page.wait_for_selector("#embedX")
            page.wait_for_selector("#embedY")
            page.locator("#embedMount canvas, #embedCanvas").first.wait_for(state="attached")

            page.click("#themeBtn")
            theme = page.evaluate("() => document.documentElement.getAttribute('data-theme')")
            page.click("#themeBtn")
            theme2 = page.evaluate("() => document.documentElement.getAttribute('data-theme')")
            if theme == theme2 or theme not in {"light", "dark"}:
                errors.append("theme toggle failed: " + str(theme) + " -> " + str(theme2))

            page.fill("#q", "")
            page.set_viewport_size({"width": 390, "height": 844})
            page.goto(base + "#home", wait_until="domcontentloaded")
            page.wait_for_selector("#home.active")
            if not page.locator(".dock").is_visible():
                errors.append("mobile dock is hidden")
            page.click("#menuBtn")
            if not page.evaluate("() => document.body.classList.contains('nav-open')"):
                errors.append("mobile menu did not open")
            page.locator(".school-block[data-school='06'] .chev").click()
            page.click("a.ll[data-id='06-01']")
            page.wait_for_selector("[id='06-01'].active")
            if page.evaluate("() => document.body.classList.contains('nav-open')"):
                errors.append("mobile menu stayed open")

            page.goto(base + "#not-a-lesson", wait_until="domcontentloaded")
            page.wait_for_selector("#view-missing.active")

            browser.close()
    finally:
        server.shutdown()
    if external:
        errors.append("external requests: " + ", ".join(sorted(set(external))[:8]))
    return errors


def main() -> int:
    errors = static_checks() + browser_checks()
    if errors:
        print("FAILED")
        for error in errors:
            print("-", error)
        return 1
    print("PASSED campus checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
