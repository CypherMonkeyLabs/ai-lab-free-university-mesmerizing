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
];
let failed = 0;
function fail(message) {
  failed += 1;
  console.error("FAIL", message);
}
const hrefRe = /href="(https?:\/\/[^"]+)"/g;
for (const rel of pages) {
  const text = fs.readFileSync(path.join(root, rel), "utf8");
  if (!text.includes("learning-only student project")) fail(`${rel} missing disclaimer`);
  if (!text.includes("https://linktr.ee/cypherMonkey")) fail(`${rel} missing Linktree`);
  if (!text.includes('data-tour="menu"') || !text.includes("phone-dock")) fail(`${rel} missing chrome`);
  for (const match of text.matchAll(hrefRe)) {
    const url = match[1];
    if (!allowedHosts.some((host) => url.includes(host))) fail(`${rel} unexpected ${url}`);
    if (/x\.com|twitter\.com|linkedin\.com|mailto:|cipher0x9|huggingface\.co\/Cypher/i.test(url)) fail(`${rel} forbidden ${url}`);
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
