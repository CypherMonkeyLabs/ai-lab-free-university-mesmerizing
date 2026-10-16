import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const pages = [
  "index.html", "learn.html", "diagrams.html", "flows.html", "play.html", "listen.html",
  "downloads.html", "help.html", "legal.html", "ecosystem.html", "glossary.html", "certs.html", "labs.html",
];
const allowedHosts = [
  "cyphermonkeylabs.com",
  "github.com/CypherMonkeyLabs",
  "linktr.ee/cypherMonkey",
  "arxiv.org",
  "nist.gov",
  "owasp.org",
  "modelcontextprotocol.io",
  "developer.mozilla.org",
  "w3.org",
  "rfc-editor.org",
  "docs.python.org",
  "git-scm.com",
  "nvidia.com",
  "x.ai",
  "anthropic.com",
  "docs.aws.amazon.com",
  "learn.microsoft.com",
  "cloud.google.com",
  "creativecommons.org",
  "opensource.org",
  "apache.org",
  "en.wikipedia.org",
  "webaudio.github.io",
  "github.com/modelcontextprotocol",
  "www.python.org",
  "opentelemetry.io",
  "www.iana.org",
  "github.com/ollama/ollama",
];
let failed = 0;
function fail(message) {
  failed += 1;
  console.error("FAIL", message);
}
const hrefRe = /href="(https?:\/\/[^"]+)"/g;
function walkHtml(dir, found) {
  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name);
    if (fs.statSync(full).isDirectory()) walkHtml(full, found);
    else if (name.endsWith(".html")) found.push(full);
  }
}
const sourced = [];
walkHtml(path.join(root, "rooms"), sourced);
walkHtml(path.join(root, "downloads"), sourced);
sourced.push(path.join(root, "learn.html"), path.join(root, "index.html"), path.join(root, "downloads.html"));
for (const full of sourced) {
  const rel = path.relative(root, full);
  const text = fs.readFileSync(full, "utf8");
  if (!text.includes("Sources and go deeper")) fail(`${rel} missing sources block`);
  if (!text.includes("last checked 2026-10")) fail(`${rel} missing last-checked mark`);
  for (const item of text.matchAll(/<li>([\s\S]*?)<\/li>/g)) {
    const li = item[1];
    if (li.includes(">confirm<") && /href="https?:/.test(li)) fail(`${rel} confirm item still has a URL`);
  }
}
const indexHtml = fs.readFileSync(path.join(root, "index.html"), "utf8");
for (const heading of ["What this lab means by an agent", "A model continues text", "Retrieve, then answer", "A loop is not a workflow", "One way to name tools"]) {
  if (!indexHtml.includes(heading)) fail(`index missing ${heading}`);
}
if (!indexHtml.includes('class="chip-ico"')) fail("index missing 3D chip icons");
for (const rel of pages) {
  const text = fs.readFileSync(path.join(root, rel), "utf8");
  if (!text.includes("learning-only student project")) fail(`${rel} missing disclaimer`);
  if (!text.includes("https://linktr.ee/cypherMonkey")) fail(`${rel} missing Linktree`);
  if (!text.includes('data-tour="menu"') || !text.includes("phone-dock")) fail(`${rel} missing chrome`);
  for (const match of text.matchAll(hrefRe)) {
    const url = match[1];
    if (!allowedHosts.some((host) => url.includes(host))) fail(`${rel} unexpected ${url}`);
    if (/x\.com|twitter\.com|linkedin\.com|mailto:|cipher0x9|huggingface\.co\/(?!docs)/i.test(url)) fail(`${rel} forbidden ${url}`);
  }
}
const diagrams = fs.readdirSync(path.join(root, "downloads/diagrams")).filter((name) => name.endsWith(".svg"));
const flows = diagrams.filter((name) => name.endsWith("-flow.svg"));
if (diagrams.length < 60) fail(`diagrams ${diagrams.length}`);
if (flows.length < 30) fail(`flows ${flows.length}`);
for (const name of diagrams) {
  const png = path.join(root, "downloads/diagrams", name.replace(/\.svg$/, ".png"));
  if (!fs.existsSync(png)) fail(`missing png for ${name}`);
}
const zipPath = path.join(root, "downloads/ai-omni-lab-offline.zip");
if (!fs.existsSync(zipPath)) fail("missing offline zip");
if (failed) {
  console.error(`FAIL ${failed}`);
  process.exit(1);
}
console.log(`OK pages=${pages.length} diagrams=${diagrams.length} flows=${flows.length}`);
