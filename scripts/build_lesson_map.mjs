/* Write data/lesson-map.json and data/sources.json from the room files. */
import { readFileSync, writeFileSync, readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");

function plain(html) {
  return String(html || "").replace(/<[^>]+>/g, " ").replace(/&amp;/g, "&").replace(/&#x27;/g, "'").replace(/&#39;/g, "'").replace(/\s+/g, " ").trim();
}

const lessons = [];
const sources = [];
const seen = new Set();
const rooms = readdirSync(join(root, "rooms")).filter((name) => /^T\d+-R\d+\.html$/.test(name)).sort();
for (const name of rooms) {
  const id = name.replace(".html", "");
  const html = readFileSync(join(root, "rooms", name), "utf8");
  const title = plain((html.match(/<h1>([\s\S]*?)<\/h1>/) || [])[1]);
  const kicker = plain((html.match(/<p class="kicker">([\s\S]*?)<\/p>/) || [])[1]);
  const levelMatch = kicker.match(/L(\d+)/);
  const level = levelMatch ? Number(levelMatch[1]) : 1;
  const five = html.match(/<section[^>]*id="five"[\s\S]*?<li>([\s\S]*?)<\/li>/);
  const outcome = plain(five ? five[1] : title);
  const file = JSON.parse(readFileSync(join(root, "rooms/sources", id, "sources.json"), "utf8"));
  const ids = file.sources.map((item) => item.id);
  for (const item of file.sources) {
    if (seen.has(item.id)) continue;
    seen.add(item.id);
    sources.push({
      id: item.id,
      title: item.title,
      url: item.url || "",
      kind: item.kind || "",
      status: item.status || "unconfirmed",
      last_checked: item.last_checked || null,
    });
  }
  lessons.push({
    key: id,
    title,
    level,
    outcomes: [outcome.length >= 8 ? outcome : `${title} is a room in this lab.`],
    sources: ids,
    last_verified: null,
    last_checked: file.last_checked || null,
  });
}
writeFileSync(join(root, "data/lesson-map.json"), `${JSON.stringify({ lessons }, null, 2)}\n`);
writeFileSync(join(root, "data/sources.json"), `${JSON.stringify({ sources }, null, 2)}\n`);
console.log(`lessons ${lessons.length} sources ${sources.length}`);
