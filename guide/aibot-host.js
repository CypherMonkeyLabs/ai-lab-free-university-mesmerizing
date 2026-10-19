/* Wires the offline chat into the existing guide sheet. No second bot. */
import { createRetriever } from "../shared/pybot-chat/engine.js";
import { chatMarkup, paintChat, chatInput } from "../shared/pybot-chat/ui.js";

const TOPICS = [
  "What is a token?",
  "Why retrieve a passage?",
  "What is an agent?",
  "What is MCP?",
  "What is a handoff?",
  "What can you help with?",
];

const messages = [];
let retriever = null;
let bound = false;

function prefix() {
  return document.body.getAttribute("data-root") || "";
}

function pushBot(answer) {
  messages.push({
    role: "bot",
    text: answer.text,
    href: answer.href ? prefix() + answer.href : "",
    link: answer.link || "",
    example: answer.example || "",
    follow: answer.follow || "",
    followQ: answer.followQ || "",
    closest: (answer.closest || []).map((hit) => ({
      title: hit.title,
      href: prefix() + hit.href,
    })),
  });
}

function paint() {
  const root = document.querySelector("[data-aibot]");
  if (root) paintChat(root, messages, false);
}

function answer(text) {
  const q = String(text || "").trim();
  if (!q) return;
  messages.push({ role: "user", text: q });
  if (!retriever) {
    pushBot({ text: "The page index is still loading. Ask again in a moment." });
    paint();
    return;
  }
  const result = retriever.ask(q, {});
  pushBot(result);
  paint();
  const input = chatInput(document.querySelector("[data-aibot]"));
  if (input) input.value = "";
}

function listen(root) {
  const Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
  const input = chatInput(root);
  if (!Rec) {
    pushBot({ text: "This browser has no speech recognition. Type instead." });
    paint();
    input?.focus();
    return;
  }
  const rec = new Rec();
  rec.lang = "en-US";
  rec.onresult = (event) => {
    const text = event.results?.[0]?.[0]?.transcript || "";
    answer(text);
  };
  rec.onerror = () => {
    pushBot({ text: "I could not hear that. Type the question instead." });
    paint();
  };
  try {
    rec.start();
  } catch (err) {
    pushBot({ text: "The mic did not start. Type the question instead." });
    paint();
  }
}

function mount() {
  const slot = document.querySelector("[data-aibot]");
  if (!slot || slot.dataset.ready === "yes") return;
  slot.dataset.ready = "yes";
  slot.innerHTML = chatMarkup(TOPICS);
  if (!messages.length) {
    messages.push({
      role: "bot",
      text: "Ask about a topic in this lab. I only quote these pages, and I can be wrong.",
      follow: "What can you help with?",
      followQ: "What can you help with?",
    });
  }
  paint();
  if (bound) return;
  bound = true;
  document.addEventListener("submit", (event) => {
    const form = event.target.closest(".py-chat-form");
    if (!form) return;
    event.preventDefault();
    answer(chatInput(form.closest("[data-aibot]"))?.value || "");
  });
  document.addEventListener("click", (event) => {
    const ask = event.target.closest("[data-py-ask]");
    if (ask && ask.closest("[data-aibot]")) {
      event.preventDefault();
      answer(ask.dataset.pyAsk || ask.textContent);
      return;
    }
    const read = event.target.closest("[data-py-read]");
    if (read) {
      event.preventDefault();
      const msg = messages[Number(read.dataset.pyRead)];
      if (!msg || !window.speechSynthesis) return;
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(new SpeechSynthesisUtterance(msg.text));
      return;
    }
    if (event.target.closest("[data-py-clear]")) {
      event.preventDefault();
      messages.splice(0, messages.length);
      retriever?.reset();
      messages.push({
        role: "bot",
        text: "Chat cleared. I only use these pages, and I can be wrong.",
        follow: "Where do I start?",
        followQ: "Where do I start?",
      });
      paint();
      return;
    }
    if (event.target.closest("[data-py-mic]")) {
      event.preventDefault();
      listen(event.target.closest("[data-aibot]"));
    }
  });
}

async function load() {
  try {
    const response = await fetch(new URL("../js/content/aibot-index.json", import.meta.url));
    const data = await response.json();
    retriever = createRetriever(data);
  } catch (err) {
    messages.push({ role: "bot", text: "I could not load the page index on this device." });
    paint();
  }
}

document.addEventListener("aibot-mount", mount);
load();
if (document.querySelector("[data-aibot]")) mount();
