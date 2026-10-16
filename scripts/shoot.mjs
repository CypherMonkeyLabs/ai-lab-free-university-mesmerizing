import fs from "node:fs";
import path from "node:path";
import puppeteer from "puppeteer-core";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const out = path.join(root, "docs/screenshots");
fs.mkdirSync(out, { recursive: true });
const base = process.env.BASE || "http://127.0.0.1:8742";

const browser = await puppeteer.launch({
  executablePath: process.env.CHROME || "/usr/bin/google-chrome",
  headless: true,
  args: ["--no-sandbox", "--disable-dev-shm-usage", "--font-render-hinting=none"],
});

async function shot(name, width, height, url, prepare, mode = "rest") {
  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: 1 });
  await page.evaluateOnNewDocument((openMode) => {
    localStorage.setItem("ai-omni-tour-v1", "done");
    localStorage.setItem("ai-omni-idle-stop", "1");
    if (openMode === "rest") localStorage.setItem("ai-omni-greeted", "1");
    else localStorage.removeItem("ai-omni-greeted");
  }, mode);
  await page.goto(base + url, { waitUntil: "networkidle0", timeout: 30000 });
  if (prepare) await prepare(page);
  await new Promise((resolve) => setTimeout(resolve, 450));
  await page.screenshot({ path: path.join(out, name), fullPage: false });
  await page.close();
  console.log(name);
}

await shot("home-1440.png", 1440, 900, "/index.html");
await shot("room-1440.png", 1440, 900, "/rooms/T7-R1.html");
await shot("downloads-1440.png", 1440, 900, "/downloads.html");
await shot("menu-1440.png", 1440, 900, "/index.html", async (page) => {
  await page.click("#menu-btn");
  await page.waitForSelector("#edge-menu.is-open");
});
await shot("home-390.png", 390, 844, "/index.html");
await shot("room-390.png", 390, 844, "/rooms/T7-R1.html");
await shot("downloads-390.png", 390, 844, "/downloads.html");
await shot("menu-390.png", 390, 844, "/index.html", async (page) => {
  await page.click("#menu-btn");
  await page.waitForSelector("#edge-menu.is-open");
});
await shot("bot-390.png", 390, 844, "/index.html", async (page) => {
  await page.click("[data-open-guide]");
  await page.waitForSelector("#monkey-sheet:not([hidden])");
});
await shot("greet-1440.png", 1440, 900, "/index.html", async (page) => {
  await page.waitForSelector(".greet-modal:not([hidden])");
}, "greet");
await shot("greet-390.png", 390, 844, "/index.html", async (page) => {
  await page.waitForSelector(".greet-modal:not([hidden])");
}, "greet");
await shot("footer-1440.png", 1440, 900, "/index.html", async (page) => {
  await page.evaluate(() => document.querySelector(".disclaimer-panel").scrollIntoView({ block: "center" }));
});
await shot("footer-390.png", 390, 844, "/index.html", async (page) => {
  await page.evaluate(() => document.querySelector(".disclaimer-panel").scrollIntoView({ block: "center" }));
});

await browser.close();
