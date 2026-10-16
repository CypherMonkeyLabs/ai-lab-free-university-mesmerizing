/* Learning guide. Crisp monkey, one centre greeting, then a dock. */
(function () {
  var root = document.documentElement;
  var TOUR_KEY = "ai-omni-tour-v1";
  var GREET_KEY = "ai-omni-greeted";
  var IDLE_KEY = "ai-omni-idle-stop";
  var POS_KEY = "ai-omni-bot-pos";
  var IDLE_MS = 150000;
  var IDLE_MAX = 3;

  function prefix() { return document.body.getAttribute("data-root") || ""; }
  function reduced() {
    return root.dataset.motion === "reduce" || window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }
  function storeGet(key) { try { return localStorage.getItem(key); } catch (err) { return null; } }
  function storeSet(key, value) { try { localStorage.setItem(key, value); } catch (err) { /* storage off */ } }

  var mount = document.getElementById("guide-mount");
  if (!mount) return;

  function face(extra) {
    return '<circle cx="46" cy="78" r="28" fill="#f59e0b" stroke="#9a3412" stroke-width="4"/>' +
      '<circle cx="46" cy="78" r="14" fill="#fb7185"/>' +
      '<circle cx="194" cy="78" r="28" fill="#f59e0b" stroke="#9a3412" stroke-width="4"/>' +
      '<circle cx="194" cy="78" r="14" fill="#fb7185"/>' +
      '<circle cx="120" cy="108" r="70" fill="#fbbf24" stroke="#b45309" stroke-width="4"/>' +
      '<ellipse cx="120" cy="132" rx="38" ry="28" fill="#fde68a" stroke="#d97706" stroke-width="3"/>' +
      '<ellipse cx="96" cy="102" rx="16" ry="18" fill="#ffffff" stroke="#1c1408" stroke-width="3"/>' +
      '<ellipse cx="146" cy="102" rx="16" ry="18" fill="#ffffff" stroke="#1c1408" stroke-width="3"/>' +
      '<circle cx="100" cy="106" r="7" fill="#1c1408"/><circle cx="150" cy="106" r="7" fill="#1c1408"/>' +
      '<circle cx="104" cy="102" r="2.5" fill="#ffffff"/><circle cx="154" cy="102" r="2.5" fill="#ffffff"/>' +
      '<ellipse cx="120" cy="128" rx="8" ry="6" fill="#9a3412"/>' +
      '<path d="M98 146 Q120 164 142 146" fill="none" stroke="#1c1408" stroke-width="4" stroke-linecap="round"/>' +
      '<g fill="none" stroke="#0e7490" stroke-width="4"><circle cx="98" cy="104" r="24"/><circle cx="146" cy="104" r="24"/><path d="M122 104 H126"/></g>' +
      (extra || "");
  }
  function pose(name, arms) {
    return '<g class="monkey-pose pose-' + name + '">' +
      '<circle cx="120" cy="128" r="112" fill="none" stroke="#22d3ee" stroke-width="8"/>' +
      '<circle cx="120" cy="128" r="104" fill="none" stroke="#f472b6" stroke-width="4"/>' +
      arms + face("") +
      '<ellipse cx="120" cy="214" rx="54" ry="34" fill="#f59e0b" stroke="#b45309" stroke-width="4"/>' +
      '<ellipse cx="120" cy="218" rx="28" ry="18" fill="#fde68a"/>' +
      "</g>";
  }
  var svgOpen = '<svg class="monkey-figure" viewBox="0 0 240 260" role="img" aria-label="CypherMonkey guide, a cartoon monkey with glasses">';
  var monkeySvg = svgOpen +
    pose("wave", '<path d="M58 150 q-36 8 -20 36" fill="none" stroke="#f59e0b" stroke-width="14" stroke-linecap="round"/><path d="M176 140 q40 -48 18 -8" fill="none" stroke="#f59e0b" stroke-width="14" stroke-linecap="round"/>') +
    pose("think", '<path d="M64 156 q-20 24 8 28" fill="none" stroke="#f59e0b" stroke-width="14" stroke-linecap="round"/><path d="M170 148 q22 10 8 28" fill="none" stroke="#f59e0b" stroke-width="14" stroke-linecap="round"/>') +
    pose("cheer", '<path d="M62 140 q-30 -40 8 -46" fill="none" stroke="#f59e0b" stroke-width="14" stroke-linecap="round"/><path d="M178 140 q30 -40 -8 -46" fill="none" stroke="#f59e0b" stroke-width="14" stroke-linecap="round"/>') +
    pose("listen", '<path d="M60 150 q-24 10 -8 32" fill="none" stroke="#f59e0b" stroke-width="14" stroke-linecap="round"/><path d="M178 132 q16 -20 8 8" fill="none" stroke="#f59e0b" stroke-width="14" stroke-linecap="round"/>') +
    pose("read", '<path d="M70 160 q16 18 40 8" fill="none" stroke="#f59e0b" stroke-width="14" stroke-linecap="round"/><path d="M170 160 q-16 18 -40 8" fill="none" stroke="#f59e0b" stroke-width="14" stroke-linecap="round"/>') +
    "</svg>";

  var dock = document.createElement("div");
  dock.className = "monkey-dock";
  dock.id = "monkey-dock";
  dock.setAttribute("data-tour", "bot");
  dock.setAttribute("data-pose", "wave");
  dock.innerHTML = monkeySvg + '<div class="idle-chip" id="idle-chip" hidden></div>';
  mount.appendChild(dock);

  var dragState = null;
  var dragged = false;
  function restorePos() {
    if (!window.matchMedia("(min-width: 960px)").matches) return;
    var raw = storeGet(POS_KEY);
    if (!raw) return;
    try {
      var pos = JSON.parse(raw);
      if (typeof pos.left !== "number" || typeof pos.top !== "number") return;
      dock.style.left = Math.max(8, pos.left) + "px";
      dock.style.top = Math.max(8, pos.top) + "px";
      dock.style.right = "auto";
      dock.style.bottom = "auto";
    } catch (err) { /* ignore a bad saved position */ }
  }
  restorePos();
  dock.addEventListener("pointerdown", function (event) {
    if (!window.matchMedia("(min-width: 960px)").matches) return;
    if (event.target.closest && event.target.closest("button")) return;
    var rect = dock.getBoundingClientRect();
    dragState = { x: event.clientX, y: event.clientY, left: rect.left, top: rect.top };
    dragged = false;
    dock.setPointerCapture(event.pointerId);
  });
  dock.addEventListener("pointermove", function (event) {
    if (!dragState) return;
    var dx = event.clientX - dragState.x;
    var dy = event.clientY - dragState.y;
    if (Math.abs(dx) + Math.abs(dy) > 4) dragged = true;
    var left = Math.max(8, Math.min(window.innerWidth - dock.offsetWidth - 8, dragState.left + dx));
    var top = Math.max(8, Math.min(window.innerHeight - 80, dragState.top + dy));
    dock.style.left = left + "px";
    dock.style.top = top + "px";
    dock.style.right = "auto";
    dock.style.bottom = "auto";
  });
  dock.addEventListener("pointerup", function () {
    if (!dragState) return;
    if (dragged) {
      var rect = dock.getBoundingClientRect();
      storeSet(POS_KEY, JSON.stringify({ left: rect.left, top: rect.top }));
    }
    dragState = null;
  });

  var sheet = document.createElement("div");
  sheet.className = "monkey-sheet";
  sheet.id = "monkey-sheet";
  sheet.hidden = true;
  sheet.setAttribute("role", "dialog");
  sheet.setAttribute("aria-label", "Guide");
  mount.appendChild(sheet);

  var modal = document.createElement("div");
  modal.className = "greet-modal";
  modal.hidden = true;
  modal.setAttribute("role", "dialog");
  modal.setAttribute("aria-modal", "true");
  modal.setAttribute("aria-labelledby", "greet-title");
  modal.setAttribute("data-pose", "wave");
  document.body.appendChild(modal);

  function setPose(name) { dock.setAttribute("data-pose", name); }

  var steps = [
    { sel: '[data-tour="home"]', title: "1 · Home", text: "Home is the lifelong-learner front door." },
    { sel: '[data-tour="menu"]', title: "2 · Menu", text: "Menu is the top-left button. Escape or a tap outside closes the drawer." },
    { sel: '[data-tour="learn"]', title: "3 · Learn", text: "Learn is the course, from programming foundations to omni-channel agents." },
    { sel: '[data-tour="diagrams"]', title: "4 · Diagrams", text: "Every drawing downloads as SVG, PNG, and HTML." },
    { sel: ['[data-tour="play"]', '[data-tour="listen"]'], title: "5 · Play and Listen", text: "Play is the quiz and games. Listen is read-along." },
    { sel: ['[data-tour="downloads"]', '[data-tour="bot"]'], title: "6 · Downloads and the guide", text: "Downloads holds the exports. You can reopen this tour from Help." }
  ];
  var tourEl = document.createElement("div");
  tourEl.className = "guide-tour";
  tourEl.hidden = true;
  tourEl.innerHTML = '<div class="guide-tour-back"></div><div class="guide-spot"></div><div class="guide-spot" hidden></div>' +
    '<div class="guide-callout"><p class="tour-title"></p><p class="tour-text"></p>' +
    '<div class="guide-callout-actions"><button type="button" class="themed" data-tour-back>Back</button>' +
    '<button type="button" class="themed" data-tour-next>Next</button><button type="button" class="themed" data-tour-skip>Skip</button></div></div>';
  document.body.appendChild(tourEl);
  var spots = tourEl.querySelectorAll(".guide-spot");
  var callout = tourEl.querySelector(".guide-callout");
  var stepIndex = 0;
  function placeSpot(node, spot) {
    if (!node) { spot.hidden = true; return; }
    var rect = node.getBoundingClientRect();
    if (rect.width < 2) { spot.hidden = true; return; }
    spot.hidden = false;
    spot.style.left = Math.max(4, rect.left - 6) + "px";
    spot.style.top = Math.max(4, rect.top - 6) + "px";
    spot.style.width = Math.min(window.innerWidth - 8, rect.width + 12) + "px";
    spot.style.height = (rect.height + 12) + "px";
  }
  function showStep(index) {
    stepIndex = index;
    var step = steps[index];
    var selectors = Array.isArray(step.sel) ? step.sel : [step.sel];
    selectors.forEach(function (sel, i) { placeSpot(document.querySelector(sel), spots[i]); });
    if (selectors.length < 2) spots[1].hidden = true;
    tourEl.querySelector(".tour-title").textContent = step.title;
    tourEl.querySelector(".tour-text").textContent = step.text;
    var target = document.querySelector(selectors[0]);
    var rect = target ? target.getBoundingClientRect() : { bottom: 80, left: 16, top: 80 };
    var top = rect.bottom + 12;
    if (top > window.innerHeight - 190) top = Math.max(12, rect.top - 180);
    callout.style.top = top + "px";
    callout.style.left = Math.min(window.innerWidth - 300, Math.max(12, rect.left)) + "px";
    tourEl.querySelector("[data-tour-back]").disabled = index === 0;
    tourEl.querySelector("[data-tour-next]").textContent = index === steps.length - 1 ? "Done" : "Next";
  }
  function startTour() { tourEl.hidden = false; setPose("wave"); showStep(0); }
  function endTour() { tourEl.hidden = true; storeSet(TOUR_KEY, "done"); greet(); }
  tourEl.querySelector("[data-tour-next]").addEventListener("click", function () {
    if (stepIndex >= steps.length - 1) endTour(); else showStep(stepIndex + 1);
  });
  tourEl.querySelector("[data-tour-back]").addEventListener("click", function () { if (stepIndex > 0) showStep(stepIndex - 1); });
  tourEl.querySelector("[data-tour-skip]").addEventListener("click", endTour);
  window.addEventListener("resize", function () { if (!tourEl.hidden) showStep(stepIndex); });
  document.querySelectorAll("[data-replay-tour]").forEach(function (btn) {
    btn.addEventListener("click", function () { sheet.hidden = true; modal.hidden = true; startTour(); });
  });

  var voices = [];
  var chosen = "";
  var rate = 0.92;
  var pitch = 1;
  var speaking = false;
  function rankVoice(voice) {
    var name = (voice.name + " " + (voice.lang || "")).toLowerCase();
    var score = 0;
    if ((voice.lang || "").toLowerCase().indexOf("en") === 0) score += 5;
    if (name.indexOf("natural") >= 0) score += 8;
    if (name.indexOf("neural") >= 0) score += 7;
    ["aria", "jenny", "guy"].forEach(function (bit) { if (name.indexOf(bit) >= 0) score += 6; });
    if (name.indexOf("enhanced") >= 0 || name.indexOf("premium") >= 0) score += 4;
    return score;
  }
  function loadVoices() {
    voices = window.speechSynthesis ? window.speechSynthesis.getVoices() : [];
    voices.sort(function (a, b) { return rankVoice(b) - rankVoice(a); });
    if (!chosen && voices[0]) chosen = voices[0].name;
    var select = sheet.querySelector("[data-voice]");
    if (!select) return;
    select.innerHTML = voices.map(function (voice) {
      return '<option value="' + voice.name.replace(/"/g, "") + '">' + voice.name + "</option>";
    }).join("") || '<option value="">Browser default</option>';
    if (chosen) select.value = chosen;
  }
  if (window.speechSynthesis) {
    loadVoices();
    window.speechSynthesis.addEventListener("voiceschanged", loadVoices);
  }
  function stopSpeech() {
    speaking = false;
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    document.querySelectorAll(".is-spoken, .is-reading, .is-readalong").forEach(function (node) {
      node.classList.remove("is-spoken", "is-reading", "is-readalong");
    });
  }
  function say(text, done) {
    if (!window.speechSynthesis) { if (done) done(); return; }
    var utter = new SpeechSynthesisUtterance(text);
    var voice = voices.filter(function (item) { return item.name === chosen; })[0] || voices[0];
    if (voice) utter.voice = voice;
    utter.rate = rate;
    utter.pitch = pitch;
    utter.onend = function () { if (done) done(); };
    utter.onerror = function () { if (done) done(); };
    window.speechSynthesis.speak(utter);
  }
  function sentences(text) {
    return text.replace(/\s+/g, " ").trim().split(/(?<=[.!?])\s+/).filter(Boolean);
  }
  function readNodes(nodes) {
    stopSpeech();
    speaking = true;
    setPose("read");
    var index = 0;
    function pump() {
      if (!speaking || index >= nodes.length) { setPose("wave"); return; }
      var node = nodes[index];
      document.querySelectorAll(".is-reading").forEach(function (el) { el.classList.remove("is-reading"); });
      node.classList.add("is-reading");
      var menuName = node.getAttribute("data-menu");
      document.querySelectorAll(".section-chip").forEach(function (chip) {
        chip.classList.toggle("is-readalong", !!(menuName && chip.getAttribute("data-tour") === menuName));
      });
      node.scrollIntoView({ block: "center", behavior: reduced() ? "auto" : "smooth" });
      var parts = sentences(node.innerText || "");
      var part = 0;
      function nextPart() {
        if (!speaking) return;
        if (part >= parts.length) { index += 1; pump(); return; }
        say(parts[part], function () { part += 1; nextPart(); });
      }
      nextPart();
    }
    pump();
  }

  function go(href) { window.location.href = prefix() + href; }
  function currentExport() {
    var room = document.body.getAttribute("data-room");
    if (!room) return prefix() + "downloads.html";
    return prefix() + "downloads/diagrams/" + room + "-arch.html";
  }
  function navigate(query) {
    var q = query.toLowerCase();
    var routes = [["download", "downloads.html"], ["diagram", "diagrams.html"], ["flow", "flows.html"], ["play", "play.html"], ["listen", "listen.html"], ["help", "help.html"], ["legal", "legal.html"], ["learn", "learn.html"], ["ecosystem", "ecosystem.html"], ["glossar", "glossary.html"], ["cert", "certs.html"], ["home", "index.html"]];
    for (var i = 0; i < routes.length; i++) {
      if (q.indexOf(routes[i][0]) >= 0) { go(routes[i][1]); return true; }
    }
    var pages = window.AI_GUIDE_PAGES || [];
    var hit = null;
    pages.forEach(function (page) { if (q.indexOf(page.title.toLowerCase()) >= 0) hit = page; });
    if (hit) { go(hit.href); return true; }
    return false;
  }
  function log(text) {
    var box = sheet.querySelector(".guide-log");
    if (!box) return;
    var p = document.createElement("p");
    p.className = "guide-bubble";
    p.textContent = text;
    box.appendChild(p);
  }
  function ask(text) {
    var q = (text || "").trim();
    if (!q) return;
    if (navigate(q)) return;
    if (/export|download/.test(q.toLowerCase())) { window.location.href = currentExport(); return; }
    log("I can open Learn, Diagrams, Play, Listen, Downloads, or Help. I do not invent a fact the page does not state.");
    setPose("think");
  }

  function fillSheet() {
    sheet.innerHTML =
      '<button type="button" class="sheet-handle" aria-label="Drag to resize the guide"></button>' +
      '<div class="sheet-offers">' +
      '<button type="button" class="themed" data-go="learn.html#ten">Finish in 10 minutes</button>' +
      '<button type="button" class="themed" data-go="learn.html">Full course</button>' +
      '<button type="button" class="themed" data-go="downloads.html">Just download</button>' +
      '<button type="button" class="themed" data-close-sheet>Close</button></div>' +
      '<details class="sheet-extra"><summary>Voice, read-along, and more</summary>' +
      '<div class="guide-log"></div>' +
      '<button type="button" class="themed" data-read-page>Read this page</button>' +
      '<button type="button" class="themed" data-read-menu>Read the menu</button>' +
      '<button type="button" class="themed" data-offer-export>Export this section</button>' +
      '<label>Voice <select class="themed" data-voice aria-label="Voice"></select></label>' +
      '<label>Rate <input data-rate type="range" min="0.7" max="1.2" step="0.05" value="0.92"></label>' +
      '<label>Pitch <input data-pitch type="range" min="0.8" max="1.2" step="0.05" value="1"></label>' +
      '<button type="button" class="themed" data-speech-stop>Stop speech</button>' +
      '<button type="button" class="themed" data-ambient aria-pressed="false">Ambient sound off</button>' +
      '<form class="guide-form"><input data-ask type="text" aria-label="Ask the guide" placeholder="Ask, or name a section"><button type="submit" class="themed">Send</button><button type="button" class="themed" data-mic>Mic</button></form>' +
      '<p class="mic-note"></p></details>';
    loadVoices();
    sheet.querySelectorAll("[data-go]").forEach(function (btn) {
      btn.addEventListener("click", function () { go(btn.getAttribute("data-go")); });
    });
    sheet.querySelector("[data-close-sheet]").addEventListener("click", closeSheet);
    sheet.querySelector("[data-read-page]").addEventListener("click", function () {
      readNodes(Array.prototype.slice.call(document.querySelectorAll("[data-read]")));
    });
    sheet.querySelector("[data-read-menu]").addEventListener("click", function () {
      var chips = Array.prototype.slice.call(document.querySelectorAll(".section-chip"));
      stopSpeech();
      speaking = true;
      setPose("read");
      var i = 0;
      function next() {
        if (!speaking || i >= chips.length) { setPose("wave"); return; }
        chips.forEach(function (chip) { chip.classList.remove("is-readalong"); });
        chips[i].classList.add("is-readalong");
        say(chips[i].textContent || "", function () { i += 1; next(); });
      }
      next();
    });
    sheet.querySelector("[data-offer-export]").addEventListener("click", function () { window.location.href = currentExport(); });
    sheet.querySelector("[data-voice]").addEventListener("change", function (event) { chosen = event.target.value; });
    sheet.querySelector("[data-rate]").addEventListener("input", function (event) { rate = Number(event.target.value); });
    sheet.querySelector("[data-pitch]").addEventListener("input", function (event) { pitch = Number(event.target.value); });
    sheet.querySelector("[data-speech-stop]").addEventListener("click", stopSpeech);
    sheet.querySelector("[data-ambient]").addEventListener("click", function (event) { toggleAmbient(event.target); });
    sheet.querySelector("form").addEventListener("submit", function (event) {
      event.preventDefault();
      var input = sheet.querySelector("[data-ask]");
      ask(input.value);
      input.value = "";
    });
    sheet.querySelector("[data-mic]").addEventListener("click", function (event) { listen(event.target); });
    var note = sheet.querySelector(".mic-note");
    if (!(window.SpeechRecognition || window.webkitSpeechRecognition)) note.textContent = "This browser has no speech recognition. Type instead.";
    var handle = sheet.querySelector(".sheet-handle");
    var drag = null;
    handle.addEventListener("pointerdown", function (event) {
      drag = { y: event.clientY, height: sheet.getBoundingClientRect().height };
      handle.setPointerCapture(event.pointerId);
    });
    handle.addEventListener("pointermove", function (event) {
      if (!drag) return;
      var dockH = 0;
      var bar = document.querySelector(".phone-dock");
      if (bar && getComputedStyle(bar).display !== "none") dockH = bar.getBoundingClientRect().height;
      var max = Math.min(window.innerHeight * 0.6, window.innerHeight - dockH - 20);
      var next = Math.max(180, Math.min(max, drag.height + (drag.y - event.clientY)));
      sheet.style.maxHeight = next + "px";
    });
    handle.addEventListener("pointerup", function () { drag = null; });
  }
  var audioCtx = null;
  var ambient = null;
  function toggleAmbient(btn) {
    var on = btn.getAttribute("aria-pressed") === "true";
    if (on) {
      if (ambient) ambient.stop();
      ambient = null;
      btn.setAttribute("aria-pressed", "false");
      btn.textContent = "Ambient sound off";
      return;
    }
    var Ctx = window.AudioContext || window.webkitAudioContext;
    if (!Ctx) return;
    if (!audioCtx) audioCtx = new Ctx();
    var osc = audioCtx.createOscillator();
    var gain = audioCtx.createGain();
    osc.frequency.value = 174;
    gain.gain.value = 0.015;
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    ambient = osc;
    btn.setAttribute("aria-pressed", "true");
    btn.textContent = "Ambient sound on";
  }
  function listen(btn) {
    var Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!Rec) {
      var input = sheet.querySelector("[data-ask]");
      if (input) input.focus();
      return;
    }
    var rec = new Rec();
    rec.lang = "en-US";
    setPose("listen");
    rec.onresult = function (event) { ask(event.results[0][0].transcript); };
    rec.onend = function () { if (dock.getAttribute("data-pose") === "listen") setPose("wave"); };
    rec.start();
    btn.setAttribute("aria-pressed", "true");
  }
  function openSheet() {
    if (!sheet.childElementCount) fillSheet();
    sheet.hidden = false;
    dock.classList.add("sheet-open");
    setPose("cheer");
  }
  function closeSheet() {
    sheet.hidden = true;
    dock.classList.remove("sheet-open");
    setPose("wave");
  }
  dock.querySelector(".monkey-figure").addEventListener("click", function () {
    if (dragged) { dragged = false; return; }
    if (sheet.hidden) openSheet(); else closeSheet();
  });
  document.querySelectorAll("[data-open-guide]").forEach(function (btn) {
    btn.addEventListener("click", function () { if (sheet.hidden) openSheet(); else closeSheet(); });
  });

  function greet() {
    dock.classList.add("is-docked");
    if (storeGet(GREET_KEY) === "1") { startIdle(); return; }
    modal.hidden = false;
    modal.innerHTML = '<div class="greet-card"><h2 id="greet-title">Welcome</h2>' + monkeySvg +
      '<p>Welcome to CypherMonkey Labs. I am the learning guide for this AI omni-channel lab. This is study material, not a claim of professional GenAI work.</p>' +
      '<div class="choice-cards"><button type="button" class="themed" data-go="learn.html#ten">Finish in 10 minutes</button>' +
      '<button type="button" class="themed" data-go="learn.html">Full course</button>' +
      '<button type="button" class="themed" data-go="downloads.html">Just download</button>' +
      '<button type="button" class="themed" data-dock-now>Dock the monkey</button></div></div>';
    modal.querySelectorAll("[data-go]").forEach(function (btn) {
      btn.addEventListener("click", function () { storeSet(GREET_KEY, "1"); go(btn.getAttribute("data-go")); });
    });
    modal.querySelector("[data-dock-now]").addEventListener("click", function () {
      storeSet(GREET_KEY, "1");
      modal.hidden = true;
      startIdle();
    });
  }

  var idleCount = 0;
  var idleTimer = 0;
  function startIdle() {
    if (storeGet(IDLE_KEY) === "1") return;
    window.clearTimeout(idleTimer);
    idleTimer = window.setTimeout(offerIdle, IDLE_MS);
  }
  ["pointerdown", "keydown"].forEach(function (type) {
    window.addEventListener(type, function () { if (dock.classList.contains("is-docked")) startIdle(); }, { passive: true });
  });
  function offerIdle() {
    if (storeGet(IDLE_KEY) === "1" || idleCount >= IDLE_MAX || !modal.hidden) return;
    idleCount += 1;
    var chip = document.getElementById("idle-chip");
    if (!chip || window.matchMedia("(max-width: 959px)").matches) {
      openSheet();
      log("Need a hand with this page? Use Not now or Stop offering if you want quiet.");
      return;
    }
    chip.hidden = false;
    chip.innerHTML = '<p>Need a hand?</p><button type="button" class="themed" data-idle-yes>Yes</button><button type="button" class="themed" data-idle-later>Not now</button><button type="button" class="themed" data-idle-stop>Stop offering</button>';
    chip.querySelector("[data-idle-yes]").addEventListener("click", function () { chip.hidden = true; openSheet(); });
    chip.querySelector("[data-idle-later]").addEventListener("click", function () { chip.hidden = true; startIdle(); });
    chip.querySelector("[data-idle-stop]").addEventListener("click", function () { storeSet(IDLE_KEY, "1"); chip.hidden = true; });
  }

  document.addEventListener("ai-quiz", function (event) {
    var detail = event.detail || {};
    setPose(detail.correct === detail.total ? "cheer" : "think");
  });

  var footer = document.querySelector(".site-footer");
  if (footer && "IntersectionObserver" in window) {
    var footerWatch = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var phone = window.matchMedia("(max-width: 959px)").matches;
        dock.classList.toggle("is-clear", phone && entry.isIntersecting);
      });
    }, { threshold: 0.2 });
    footerWatch.observe(footer);
  }

  if (storeGet(TOUR_KEY) === "done") greet();
  else startTour();
  window.AiGuide = { startTour: startTour, openSheet: openSheet };
})();
