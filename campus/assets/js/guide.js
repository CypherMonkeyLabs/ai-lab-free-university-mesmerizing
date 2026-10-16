/* Guide Bot. Answers come from assets/guide/kb.json. It does not invent lab facts. */
var ENDPOINT = "";
var kbPromise = null;
var state = { mode: "chat", quiz: 0, score: 0, tour: 0, busy: false };

function motionOff() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches
    || document.documentElement.getAttribute("data-motion") === "reduce";
}

function loadKb() {
  if (kbPromise) return kbPromise;
  kbPromise = fetch("assets/guide/kb.json").then(function (res) {
    if (!res.ok) throw new Error("kb");
    return res.json();
  });
  kbPromise.catch(function () { kbPromise = null; });
  return kbPromise;
}

function tokens(text) {
  return String(text || "").toLowerCase().replace(/[^a-z0-9]+/g, " ").split(/\s+/).filter(function (word) {
    return word.length > 2;
  });
}

function expand(words, synonyms) {
  var out = words.slice();
  words.forEach(function (word) {
    Object.keys(synonyms || {}).forEach(function (key) {
      var group = [key].concat(synonyms[key] || []);
      if (group.indexOf(word) !== -1) out = out.concat(group);
    });
  });
  return out;
}

function scorePage(page, words) {
  var title = String(page.title || "").toLowerCase();
  var summary = String(page.summary || "").toLowerCase();
  var keys = page.keywords || [];
  var hay = {};
  var titleWords = {};
  tokens(title).forEach(function (word) { titleWords[word] = 1; hay[word] = 1; });
  tokens(summary + " " + keys.join(" ")).forEach(function (word) { hay[word] = 1; });
  var score = 0;
  words.forEach(function (word) {
    if (titleWords[word]) score += 4;
    else if (hay[word]) score += 1;
    if (keys.indexOf(word) !== -1) score += page.kind === "section" ? 10 : 2;
  });
  if (page.kind === "section" && score > 0) score += 2;
  return score;
}

function localAnswer(kb, question) {
  var words = expand(tokens(question), kb.synonyms);
  if (!words.length) {
    return { text: kb.fallback, pages: [] };
  }
  var ranked = (kb.pages || []).map(function (page) {
    return { page: page, score: scorePage(page, words) };
  }).filter(function (row) { return row.score > 0; });
  ranked.sort(function (a, b) { return b.score - a.score; });
  var top = ranked.slice(0, 3).filter(function (row) { return row.score >= 3; });
  if (!top.length) return { text: kb.fallback, pages: [] };
  var lines = ["From this lab's pages:"];
  top.forEach(function (row) {
    lines.push(row.page.title + " — " + row.page.summary);
    lines.push(row.page.href);
  });
  return {
    text: lines.join("\n"),
    pages: top.map(function (row) { return row.page; })
  };
}

function askRemote(question) {
  if (!ENDPOINT) return Promise.resolve(null);
  return fetch(ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: question, lab: "ai-lab-free-university" })
  }).then(function (res) {
    if (!res.ok) throw new Error("guide endpoint");
    return res.json();
  }).then(function (data) {
    if (!data || typeof data.answer !== "string" || !data.answer.trim()) return null;
    var sources = Array.isArray(data.sources) ? data.sources : [];
    var note = sources.length
      ? "Connected agent. Sources: " + sources.join(", ")
      : "Connected agent. This widget did not check that reply against the lab pages.";
    return { text: note + "\n" + data.answer.trim(), pages: [] };
  }).catch(function () { return null; });
}

function wants(question, words) {
  var text = String(question || "").toLowerCase();
  return words.some(function (word) { return text.indexOf(word) !== -1; });
}

function pageById(kb, id) {
  var pages = kb.pages || [];
  for (var i = 0; i < pages.length; i += 1) {
    if (pages[i].id === id) return pages[i];
  }
  return null;
}

function quizPrompt(kb) {
  var quiz = kb.quizzes[state.quiz];
  var lines = ["Quiz " + (state.quiz + 1) + " of " + kb.quizzes.length, quiz.prompt];
  quiz.choices.forEach(function (choice, index) {
    lines.push((index + 1) + ". " + choice.label);
  });
  return lines.join("\n");
}

function grade(kb, question) {
  var quiz = kb.quizzes[state.quiz];
  var text = String(question || "").trim().toLowerCase();
  var picked = null;
  quiz.choices.forEach(function (choice, index) {
    if (picked) return;
    if (text === String(index + 1) || text === choice.label.toLowerCase() || text === choice.id.toLowerCase()) {
      picked = choice;
    }
  });
  if (!picked) return { text: "Reply with 1, 2, or 3. " + quizPrompt(kb), pages: [] };
  var correct = picked.id === quiz.answer;
  if (correct) state.score += 1;
  var page = pageById(kb, quiz.answer);
  var cite = page ? page.title + " — " + page.summary : quiz.cite;
  var line = (correct ? "That's the page." : "The matching page is another one.") + "\nThe page says: " + cite;
  state.quiz += 1;
  if (state.quiz >= kb.quizzes.length) {
    var total = kb.quizzes.length;
    var score = state.score;
    state.mode = "chat";
    return { text: line + "\nScore: " + score + " of " + total + ".", pages: page ? [page] : [] };
  }
  return { text: line + "\n" + quizPrompt(kb), pages: page ? [page] : [] };
}

function tourStep(kb) {
  var id = kb.tours[state.tour];
  var page = pageById(kb, id);
  if (!page) {
    state.mode = "chat";
    return { text: "That tour step is not in the lab pages.", pages: [] };
  }
  if (location.hash !== page.href) location.hash = page.href;
  var last = state.tour >= kb.tours.length - 1;
  var tail = last ? "\nThat is the last stop." : "\nSay next for the following stop, or stop to leave the tour.";
  if (last) state.mode = "chat";
  return { text: page.title + " — " + page.summary + tail, pages: [page] };
}

function answerQuestion(question) {
  return loadKb().then(function (kb) {
    if (state.mode === "quiz") return grade(kb, question);
    if (state.mode === "tour") {
      if (wants(question, ["stop", "done", "quit"])) {
        state.mode = "chat";
        return { text: "Tour stopped. Ask about a page title when you want the lab's own wording.", pages: [] };
      }
      if (wants(question, ["next", "continue", "go"])) {
        state.tour += 1;
        if (state.tour >= kb.tours.length) {
          state.mode = "chat";
          return { text: "Tour finished.", pages: [] };
        }
        return tourStep(kb);
      }
    }
    if (wants(question, ["tour"])) {
      state.mode = "tour";
      state.tour = 0;
      return tourStep(kb);
    }
    if (wants(question, ["quiz"])) {
      state.mode = "quiz";
      state.quiz = 0;
      state.score = 0;
      return { text: quizPrompt(kb), pages: [] };
    }
    return askRemote(question).then(function (remote) {
      return remote || localAnswer(kb, question);
    });
  }).catch(function () {
    return { text: "The guide pages did not load from this copy of the lab. Open a lesson from the menu instead.", pages: [] };
  });
}

function typeInto(node, text) {
  node.textContent = "";
  if (motionOff()) {
    node.textContent = text;
    return Promise.resolve();
  }
  return new Promise(function (resolve) {
    var i = 0;
    var timer = window.setInterval(function () {
      i += 2;
      node.textContent = text.slice(0, i);
      if (i >= text.length) {
        window.clearInterval(timer);
        node.textContent = text;
        resolve();
      }
    }, 16);
  });
}

export function wireGuide() {
  if (document.getElementById("guideBot")) return;
  var root = document.createElement("div");
  root.id = "guideBot";
  var launcher = document.createElement("button");
  launcher.type = "button";
  launcher.className = "guide-launcher";
  launcher.setAttribute("aria-expanded", "false");
  launcher.setAttribute("aria-controls", "guidePanel");
  launcher.textContent = "Guide Bot";
  var panel = document.createElement("section");
  panel.id = "guidePanel";
  panel.className = "guide-panel";
  panel.hidden = true;
  panel.setAttribute("aria-label", "Guide Bot");
  var head = document.createElement("div");
  head.className = "guide-head";
  var title = document.createElement("h2");
  title.textContent = "Guide Bot";
  var close = document.createElement("button");
  close.type = "button";
  close.textContent = "Close";
  head.appendChild(title);
  head.appendChild(close);
  var log = document.createElement("div");
  log.className = "guide-log";
  log.setAttribute("aria-live", "polite");
  var chips = document.createElement("div");
  chips.className = "guide-chips";
  ["Where do I start?", "Diagrams", "Tour the lab", "Quiz me", "Ecosystem"].forEach(function (label) {
    var chip = document.createElement("button");
    chip.type = "button";
    chip.textContent = label;
    chip.addEventListener("click", function () { submit(label); });
    chips.appendChild(chip);
  });
  var form = document.createElement("form");
  form.className = "guide-form";
  var input = document.createElement("input");
  input.type = "text";
  input.name = "q";
  input.setAttribute("aria-label", "Ask the Guide Bot");
  input.placeholder = "Ask about a page in this lab";
  input.autocomplete = "off";
  var send = document.createElement("button");
  send.type = "submit";
  send.textContent = "Send";
  form.appendChild(input);
  form.appendChild(send);
  var note = document.createElement("p");
  note.className = "guide-note";
  note.textContent = "Answers use this lab's pages. A future cloud agent can be attached with CampusGuide.setEndpoint. Nothing is sent until that is set.";
  panel.appendChild(head);
  panel.appendChild(log);
  panel.appendChild(chips);
  panel.appendChild(form);
  panel.appendChild(note);
  root.appendChild(panel);
  root.appendChild(launcher);
  document.body.appendChild(root);

  function bubble(text, who) {
    var node = document.createElement("p");
    node.className = "guide-bubble" + (who === "user" ? " user" : "");
    log.appendChild(node);
    log.scrollTop = log.scrollHeight;
    if (who === "user" || motionOff()) {
      node.textContent = text;
      return Promise.resolve();
    }
    return typeInto(node, text).then(function () { log.scrollTop = log.scrollHeight; });
  }

  function submit(question) {
    var text = String(question || "").trim();
    if (!text || state.busy) return;
    state.busy = true;
    input.value = "";
    bubble(text, "user").then(function () { return answerQuestion(text); }).then(function (result) {
      return bubble(result.text, "bot");
    }).catch(function () {
      return bubble("The guide could not read the lab pages just now.", "bot");
    }).then(function () { state.busy = false; });
  }

  launcher.addEventListener("click", function () {
    panel.hidden = !panel.hidden;
    launcher.setAttribute("aria-expanded", panel.hidden ? "false" : "true");
    if (!panel.hidden && !log.dataset.greeted) {
      log.dataset.greeted = "1";
      bubble("I answer from this lab's pages: lessons, diagrams, flows, charts, cheat sheets, and the ecosystem track. I will say when a question is not in those pages.", "bot");
    }
    if (!panel.hidden) input.focus();
  });
  close.addEventListener("click", function () {
    panel.hidden = true;
    launcher.setAttribute("aria-expanded", "false");
    launcher.focus();
  });
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    submit(input.value);
  });
}

window.CampusGuide = {
  setEndpoint: function (url) { ENDPOINT = typeof url === "string" ? url : ""; },
  getEndpoint: function () { return ENDPOINT; },
  ask: answerQuestion
};
