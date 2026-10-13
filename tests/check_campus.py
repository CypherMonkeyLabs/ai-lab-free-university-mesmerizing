#!/usr/bin/env python3
"""Headless checks for the offline campus: links, navigation, and no network."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "university" / "v2-UNIVERSITY.html"


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


def static_checks() -> list[str]:
    text = HTML.read_text(encoding="utf-8")
    errors: list[str] = []
    parser = Collector()
    parser.feed(text)
    if parser.dupes:
        errors.append("duplicate ids: " + ", ".join(parser.dupes[:8]))
    if parser.external_srcs:
        errors.append("external resources: " + ", ".join(parser.external_srcs))
    urls = re.findall(r"https?://[^\s'\"<>)]+", text)
    bad = [url for url in urls if "127.0.0.1" not in url and "www.w3.org" not in url]
    if bad:
        errors.append("external urls: " + ", ".join(bad))
    for href in parser.hrefs:
        if not href.startswith("#") or href == "#":
            errors.append("non-anchor link: " + href)
            continue
        target = href[1:]
        if target not in parser.ids:
            errors.append("unresolved link: " + href)
    needed = ["home", "map", "menuBtn", "themeBtn", "q", "pagerPrev", "pagerNext", "markBtn", "00-01", "06-01", "07-01"]
    for item in needed:
        if item not in parser.ids:
            errors.append("missing id: " + item)
    if "cdn" in text.lower() or "googleapis" in text or "jsdelivr" in text or "unpkg" in text:
        errors.append("cdn marker found")
    return errors


def browser_checks() -> list[str]:
    errors: list[str] = []
    external: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=True, args=["--disable-gpu", "--no-sandbox"])
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        def on_request(request) -> None:
            url = request.url
            if url.startswith(("file:", "data:", "blob:", "about:")):
                return
            external.append(url)

        page.on("request", on_request)
        page.goto(HTML.as_uri() + "#home", wait_until="load")
        page.evaluate("localStorage.clear()")
        page.goto(HTML.as_uri() + "#home", wait_until="load")

        def visible_title() -> str:
            return page.locator("[data-panel].active h1").inner_text()

        if "Learn to build" not in visible_title():
            errors.append("home title missing: " + visible_title())

        page.click("a[href='#map']")
        page.wait_for_function("() => location.hash === '#map'")
        if page.locator("#map.active").count() != 1:
            errors.append("map did not open")

        schools = page.eval_on_selector_all("a.school-jump[href^='#school-']", "els => els.map(e => e.getAttribute('href'))")
        for href in schools:
            page.goto(HTML.as_uri() + href, wait_until="load")
            if page.locator(href + ".active").count() != 1:
                errors.append("school did not open " + href)

        lessons = page.eval_on_selector_all("article.lesson", "els => els.map(e => e.id)")
        if len(lessons) < 100:
            errors.append("too few lessons: " + str(len(lessons)))
        for lid in lessons:
            page.goto(HTML.as_uri() + "#" + lid, wait_until="load")
            active = page.locator("article.lesson.active")
            if active.count() != 1 or active.get_attribute("id") != lid:
                errors.append("lesson nav failed " + lid)
                break
            if page.locator("a.ll.on").get_attribute("data-id") != lid:
                errors.append("sidebar did not highlight " + lid)
                break

        page.goto(HTML.as_uri() + "#00-01", wait_until="load")
        page.click("#pagerNext")
        page.wait_for_selector("[id='00-02'].active")
        page.click("#pagerPrev")
        page.wait_for_selector("[id='00-01'].active")
        if page.locator("#pagerPrev").is_visible():
            errors.append("previous shown on the first lesson")

        page.fill("#q", "Model Context Protocol")
        page.keyboard.press("Enter")
        page.wait_for_timeout(150)
        if page.locator("article.lesson.active").get_attribute("id") != "07-01":
            errors.append("search did not open MCP lesson, got " + str(page.locator("article.lesson.active").get_attribute("id")))

        before = page.locator("#studiedLabel").inner_text()
        page.click("#markBtn")
        after = page.locator("#studiedLabel").inner_text()
        if before == after or "Completed" not in page.locator("#markBtn").inner_text():
            errors.append("mark complete did not update progress")

        page.click("#themeBtn")
        theme = page.evaluate("() => document.documentElement.getAttribute('data-theme')")
        page.click("#themeBtn")
        theme2 = page.evaluate("() => document.documentElement.getAttribute('data-theme')")
        if theme == theme2 or theme not in {"light", "dark"}:
            errors.append("theme toggle failed: " + str(theme) + " -> " + str(theme2))

        page.fill("#q", "")
        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(HTML.as_uri() + "#home", wait_until="load")
        page.click("#menuBtn")
        if not page.evaluate("() => document.body.classList.contains('nav-open')"):
            errors.append("mobile menu did not open")
        page.locator(".school-block[data-school='06'] .chev").click()
        page.click("a.ll[data-id='06-01']")
        page.wait_for_selector("[id='06-01'].active")
        if page.evaluate("() => document.body.classList.contains('nav-open')"):
            errors.append("mobile menu stayed open")

        page.goto(HTML.as_uri() + "#not-a-lesson", wait_until="load")
        if page.locator("#view-missing.active").count() != 1:
            errors.append("missing hash did not show the fallback")

        browser.close()
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
