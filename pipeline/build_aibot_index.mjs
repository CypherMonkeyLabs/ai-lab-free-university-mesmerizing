/* Build the offline AI Lab chat index from this lab's own pages.
   Usage: node pipeline/build_aibot_index.mjs
   Writes js/content/aibot-index.json. Do not edit that file by hand. */
import { readFileSync, writeFileSync, readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { tokens } from "../shared/pybot-chat/engine.js";
import { SEEDS } from "./aibot_seeds.mjs";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const outPath = join(root, "js/content/aibot-index.json");

const SYN = {
  tokens: "token",
  tokenizer: "token",
  tokenizers: "token",
  embeddings: "embedding",
  embeding: "embedding",
  rag: "retrieval",
  retrieve: "retrieval",
  retrieved: "retrieval",
  retrieving: "retrieval",
  chunks: "chunk",
  prompts: "prompt",
  prompting: "prompt",
  agents: "agent",
  tools: "tool",
  schemas: "schema",
  evals: "eval",
  evaluation: "eval",
  evaluations: "eval",
  hallucinate: "hallucination",
  hallucinations: "hallucination",
  guardrails: "guardrail",
  handoffs: "handoff",
  transcript: "transcription",
  transcripts: "transcription",
  stt: "speech",
  tts: "speech",
  omnichannel: "omni",
  webrtc: "webrtc",
  livekit: "livekit",
  pipecat: "pipecat",
  mcp: "mcp",
};

const PAGES = [
  "index.html",
  "learn.html",
  "voice-stack.html",
  "speech-analytics.html",
  "agent-safety.html",
  "play.html",
  "listen.html",
  "downloads.html",
  "help.html",
  "glossary.html",
  "ecosystem.html",
  "labs.html",
  "certs.html",
  "legal.html",
];

function plain(html) {
  return String(html || "")
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&#x27;/g, "'")
    .replace(/&nbsp;/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function clip(text, max = 420) {
  const clean = plain(text);
  if (clean.length <= max) return clean;
  const cut = clean.slice(0, max);
  const stop = Math.max(cut.lastIndexOf(". "), cut.lastIndexOf("? "));
  if (stop > 80) return cut.slice(0, stop + 1);
  return cut.trim();
}

function section(html, id) {
  const re = new RegExp(`<section[^>]*id="${id}"[\\s\\S]*?</section>`, "i");
  const match = html.match(re);
  return match ? match[0] : "";
}

function bits(html) {
  const out = [];
  const re = /<(li|p|dd|dt)(?:\s[^>]*)?>([\s\S]*?)<\/\1>/gi;
  let match;
  while ((match = re.exec(html))) {
    if (/export-row|class="cite|source-kind|source-checked/.test(match[0])) continue;
    const text = plain(match[2]);
    if (text.length > 20) out.push(text);
  }
  return out;
}

function caution(text) {
  if (!/price|\$\d|\blimit\b|\bversion\b|availab|quota|\bfee\b|H100/i.test(text)) return text;
  return `${text} The page's source list is dated there (often 2026-10). Treat a vendor number, limit, or price as unconfirmed until you re-open that source.`;
}

const docs = [];

function add(doc) {
  const bodyText = [doc.ti, doc.body].filter(Boolean).join("\n");
  const ex = caution(clip(doc.ex || doc.body || doc.ti));
  docs.push({
    i: doc.i,
    k: doc.k,
    ti: doc.ti,
    h: doc.h,
    s: doc.s || "",
    ex,
    eg: "",
    w: tokens(bodyText, SYN, 3),
    tw: tokens(doc.ti, SYN, 2),
  });
}

for (const name of readdirSync(join(root, "rooms")).filter((file) => /^T\d+-R\d+\.html$/.test(file)).sort()) {
  const html = readFileSync(join(root, "rooms", name), "utf8");
  const title = plain((html.match(/<h1>([\s\S]*?)<\/h1>/) || [])[1] || name);
  const five = bits(section(html, "five"));
  const example = bits(section(html, "example"));
  const eco = bits(section(html, "ecosystem"));
  const body = [...five, ...example, ...eco].join(" ");
  add({
    i: `lesson:${name.replace(".html", "")}`,
    k: "lesson",
    ti: title,
    h: `rooms/${name}`,
    s: (plain((html.match(/<p class="kicker">([\s\S]*?)<\/p>/) || [])[1] || "").split("·")[0] || "").trim(),
    ex: five.slice(0, 4).join(" ") || title,
    body,
  });
}

for (const name of PAGES) {
  const html = readFileSync(join(root, name), "utf8");
  const main = (html.match(/<main[\s\S]*?<\/main>/i) || [html])[0];
  const title = plain((html.match(/<h1>([\s\S]*?)<\/h1>/) || [])[1] || name);
  const paras = bits(main).slice(0, 12);
  add({
    i: `page:${name}`,
    k: "page",
    ti: title,
    h: name,
    ex: paras.slice(0, 2).join(" ") || title,
    body: paras.join(" "),
  });
}

const byRoom = new Map(docs.filter((doc) => doc.k === "lesson").map((doc) => [doc.i.slice("lesson:".length), doc]));
const seeds = [];
for (const rule of SEEDS) {
  const doc = byRoom.get(rule.room);
  if (!doc) throw new Error(`seed room missing: ${rule.room}`);
  seeds.push({
    i: `seed:${rule.room}:${rule.topic}`,
    h: doc.h,
    ti: doc.ti,
    k: "lesson",
    topic: rule.topic,
    any: rule.any || [],
    all: rule.all || [],
    block: rule.block || [],
    how: false,
    allow: [...new Set([...(rule.any || []), ...(rule.all || [])])],
    rank: rule.rank || 4,
    ex: doc.ex,
    eg: "",
  });
}

const index = { v: 2, syn: SYN, seeds, docs };
writeFileSync(outPath, `${JSON.stringify(index)}\n`);
console.log(`docs ${docs.length} seeds ${seeds.length} bytes ${Buffer.byteLength(JSON.stringify(index))}`);
console.log(`wrote ${outPath}`);
