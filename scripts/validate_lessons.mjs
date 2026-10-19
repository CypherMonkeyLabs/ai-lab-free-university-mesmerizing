// Validates data/lesson-map.json against rooms/*.html and rooms/sources.
// Exit 1 on any problem.
import { readFileSync, readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const map = JSON.parse(readFileSync(join(root, "data/lesson-map.json"), "utf8"));
const schema = JSON.parse(readFileSync(join(root, "data/lesson-schema.json"), "utf8"));
const catalog = JSON.parse(readFileSync(join(root, "data/sources.json"), "utf8"));
const sourceIds = new Set(catalog.sources.map((item) => item.id));
const problems = [];
const rooms = readdirSync(join(root, "rooms")).filter((name) => /^T\d+-R\d+\.html$/.test(name));
const mapped = new Map(map.lessons.map((lesson) => [lesson.key, lesson]));
const seen = new Set();

function plain(html) {
  return String(html || "").replace(/<[^>]+>/g, " ").replace(/&amp;/g, "&").replace(/&#x27;/g, "'").replace(/&#39;/g, "'").replace(/\s+/g, " ").trim();
}

for (const name of rooms) {
  const key = name.replace(".html", "");
  seen.add(key);
  const lesson = mapped.get(key);
  if (!lesson) {
    problems.push(`${key}: not in lesson-map.json`);
    continue;
  }
  for (const field of schema.required) {
    if (!(field in lesson)) problems.push(`${key}: missing field ${field}`);
  }
  const html = readFileSync(join(root, "rooms", name), "utf8");
  const title = plain((html.match(/<h1>([\s\S]*?)<\/h1>/) || [])[1]);
  if (lesson.title !== title) problems.push(`${key}: title differs from the room file`);
  if (!Number.isInteger(lesson.level) || lesson.level < 0 || lesson.level > 10) problems.push(`${key}: level must be 0-10`);
  if (!Array.isArray(lesson.outcomes) || lesson.outcomes.length < 1 || lesson.outcomes.some((item) => typeof item !== "string" || item.length < 8)) {
    problems.push(`${key}: needs at least one outcome`);
  }
  if (!Array.isArray(lesson.sources) || lesson.sources.length < 1) problems.push(`${key}: needs at least one source`);
  const file = JSON.parse(readFileSync(join(root, "rooms/sources", key, "sources.json"), "utf8"));
  const ids = file.sources.map((item) => item.id);
  if (JSON.stringify(lesson.sources) !== JSON.stringify(ids)) problems.push(`${key}: sources differ from the room sources file`);
  for (const id of lesson.sources || []) {
    if (!sourceIds.has(id)) problems.push(`${key}: unknown source id ${id}`);
  }
  if (lesson.last_verified !== null && !/^\d{4}-\d{2}-\d{2}$/.test(lesson.last_verified)) {
    problems.push(`${key}: last_verified must be null or YYYY-MM-DD`);
  }
}
for (const key of mapped.keys()) if (!seen.has(key)) problems.push(`${key}: in lesson-map.json but no such room`);

for (const problem of problems) console.log("FAIL", problem);
console.log("lessons:", seen.size, "mapped:", mapped.size);
console.log("validate_lessons:", problems.length, "problems");
process.exit(problems.length ? 1 : 0);
