/* Write sw.js from the shell, the rooms, and the chat files. Budget 3.5 MB. */
import { readFileSync, writeFileSync, statSync, readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const budget = 3_500_000;
const required = [
  "index.html",
  "learn.html",
  "voice-stack.html",
  "speech-analytics.html",
  "agent-safety.html",
  "play.html",
  "listen.html",
  "help.html",
  "legal.html",
  "ecosystem.html",
  "glossary.html",
  "certs.html",
  "labs.html",
  "offline.html",
  "favicon.svg",
  "manifest.webmanifest",
  "icon-192.png",
  "icon-512.png",
  "icon-maskable-512.png",
  "assets/css/frame.css",
  "assets/css/wow.css",
  "assets/css/footer.css",
  "assets/css/lab.css",
  "assets/css/float.css",
  "assets/css/studio.css",
  "assets/js/frame.js",
  "assets/js/float.js",
  "assets/js/university.js",
  "assets/js/pages.js",
  "assets/js/theme-boot.js",
  "assets/js/worlds.js",
  "assets/js/channel-sim.js",
  "guide/guide.css",
  "guide/guide.js",
  "guide/dragbot.js",
  "guide/aibot-host.js",
  "shared/pybot-chat/engine.js",
  "shared/pybot-chat/ui.js",
  "shared/pybot-chat/chat.css",
  "js/content/aibot-index.json",
  "js/pwa.js",
];
const rooms = readdirSync(join(root, "rooms")).filter((name) => name.endsWith(".html")).sort().map((name) => `rooms/${name}`);
const optional = ["downloads.html", "diagrams.html", "flows.html"];

function size(rel) {
  return statSync(join(root, rel)).size;
}

const files = [];
let total = 0;
for (const rel of [...required, ...rooms]) {
  const bytes = size(rel);
  files.push(rel);
  total += bytes;
}
for (const rel of optional) {
  const bytes = size(rel);
  if (total + bytes <= budget) {
    files.push(rel);
    total += bytes;
  } else {
    console.log("skip over budget", rel, bytes);
  }
}
if (total > budget) {
  console.error(`precache ${total} exceeds ${budget}`);
  process.exit(1);
}
const body = `/* Scope is the directory of this file. Cache ${files.length} files, ${total} bytes, under ${budget}. */
const CACHE = "ai-omni-v10";
const FILES = ${JSON.stringify(files, null, 2)};
self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (event) => {
  event.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  event.respondWith(caches.match(event.request).then((hit) => hit || fetch(event.request).catch(() => (
    event.request.mode === "navigate" ? caches.match("./offline.html") : Promise.reject(new Error("offline"))
  ))));
});
`;
writeFileSync(join(root, "sw.js"), body);
console.log(`precache ${files.length} files ${total} bytes`);
