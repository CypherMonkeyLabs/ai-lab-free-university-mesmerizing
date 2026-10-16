/* Counters, theme chips, D3, Rough.js, markmap, and confetti. Offline only. */
import { wirePhone } from "./phone.js";
import { wireGuide } from "./guide.js";

function motionOff() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches
    || document.documentElement.getAttribute("data-motion") === "reduce";
}

function narrowScreen() {
  return window.matchMedia("(max-width: 800px)").matches;
}

var scriptLoads = {};

function loadClassic(src) {
  if (scriptLoads[src]) return scriptLoads[src];
  scriptLoads[src] = new Promise(function (resolve, reject) {
    var existing = document.querySelector('script[data-lazy="' + src + '"]');
    if (existing && existing.dataset.loaded === "1") {
      resolve();
      return;
    }
    var script = existing || document.createElement("script");
    script.src = src;
    script.async = true;
    script.dataset.lazy = src;
    script.addEventListener("load", function () {
      script.dataset.loaded = "1";
      resolve();
    }, { once: true });
    script.addEventListener("error", function () { reject(new Error(src)); }, { once: true });
    if (!existing) document.head.appendChild(script);
  });
  return scriptLoads[src];
}

function whenNear(selector, fn) {
  var nodes = document.querySelectorAll(selector);
  if (!nodes.length) return;
  if (typeof IntersectionObserver !== "function") {
    fn();
    return;
  }
  var seen = false;
  var observer = new IntersectionObserver(function (entries) {
    if (seen || !entries.some(function (entry) { return entry.isIntersecting; })) return;
    seen = true;
    observer.disconnect();
    fn();
  }, { rootMargin: "160px" });
  nodes.forEach(function (node) { observer.observe(node); });
}

function countUp(node) {
  var target = Number(node.getAttribute("data-count"));
  if (!Number.isFinite(target) || node.dataset.counted === "1") return;
  node.dataset.counted = "1";
  var finalText = String(target);
  node.style.minWidth = Math.max(finalText.length, 1) + "ch";
  if (motionOff() || node.textContent.trim() === finalText) {
    node.textContent = finalText;
    return;
  }
  var start = performance.now();
  function tick(now) {
    var progress = Math.min(1, (now - start) / 900);
    var eased = 1 - Math.pow(1 - progress, 3);
    node.textContent = String(Math.round(target * eased));
    if (progress < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

function paintCounts(root) {
  (root || document).querySelectorAll("[data-count]").forEach(countUp);
}

function drawD3(root) {
  if (!window.d3) return;
  (root || document).querySelectorAll("[data-d3-chart]").forEach(function (host) {
    if (host.dataset.drawn === "1") return;
    host.dataset.drawn = "1";
    var labels = (host.getAttribute("data-labels") || "").split(",").filter(Boolean);
    var values = (host.getAttribute("data-values") || "").split(",").map(Number);
    var rows = labels.map(function (label, index) { return { label: label, value: values[index] || 0 }; });
    var width = 640;
    var height = 36 + rows.length * 22;
    var peak = d3.max(rows, function (row) { return row.value; }) || 1;
    var svg = d3.select(host).append("svg").attr("viewBox", "0 0 " + width + " " + height).attr("role", "img");
    svg.append("rect").attr("width", width).attr("height", height).attr("rx", 12).attr("fill", "#070b16");
    var scale = d3.scaleLinear().domain([0, peak]).range([0, 280]);
    svg.selectAll("text.label").data(rows).enter().append("text")
      .attr("x", 12).attr("y", function (_row, index) { return 28 + index * 22; })
      .attr("fill", "#e7f6ff").attr("font-size", 12).attr("font-family", "system-ui,sans-serif")
      .text(function (row) { return row.label; });
    svg.selectAll("rect.bar").data(rows).enter().append("rect")
      .attr("x", 80).attr("y", function (_row, index) { return 16 + index * 22; })
      .attr("height", 14).attr("rx", 4).attr("fill", "#22d3ee")
      .attr("width", function (row) { return scale(row.value); })
      .append("title").text(function (row) { return row.label + ": " + row.value; });
  });
}

function drawRough(root) {
  if (!window.rough) return;
  (root || document).querySelectorAll("[data-rough-chart] svg").forEach(function (svg) {
    if (svg.dataset.drawn === "1") return;
    svg.dataset.drawn = "1";
    var rc = window.rough.svg(svg);
    svg.appendChild(rc.rectangle(8, 8, 260, 64, { stroke: "#22d3ee", roughness: 1.4, strokeWidth: 2 }));
  });
}

function normalizeTree(node) {
  if (!node || typeof node !== "object") return;
  if (!Array.isArray(node.children)) node.children = [];
  node.children.forEach(normalizeTree);
}

function drawMindmap() {
  var svg = document.getElementById("mindmap");
  var dataNode = document.getElementById("mindmapData");
  if (!svg || !dataNode || !window.markmap || !window.markmap.Markmap || svg.dataset.drawn === "1") return;
  var tree;
  try {
    tree = JSON.parse(dataNode.textContent);
    normalizeTree(tree);
  } catch (err) {
    return;
  }
  svg.dataset.drawn = "1";
  try {
    var mm = new window.markmap.Markmap(svg, { duration: motionOff() ? 0 : 400 });
    mm.setData(tree).then(function () {
      return mm.fit();
    }).catch(function () {
      svg.insertAdjacentHTML("afterend", '<p class="block-note">The mind map words are on this page. The drawing library did not finish.</p>');
    });
  } catch (err) {
    svg.dataset.drawn = "0";
  }
}

function wireThemes(root) {
  (root || document).querySelectorAll("[data-set-theme]").forEach(function (button) {
    if (button.dataset.bound === "1") return;
    button.dataset.bound = "1";
    button.addEventListener("click", function () {
      if (window.CampusTheme) window.CampusTheme(button.getAttribute("data-set-theme"));
    });
  });
}

function wireAtlas(root) {
  (root || document).querySelectorAll("[data-atlas-filter]").forEach(function (button) {
    if (button.dataset.bound === "1") return;
    button.dataset.bound = "1";
    button.addEventListener("click", function () {
      var kind = button.getAttribute("data-atlas-filter");
      var scope = button.closest("[data-panel]") || document;
      scope.querySelectorAll("[data-atlas-filter]").forEach(function (peer) {
        peer.setAttribute("aria-pressed", peer === button ? "true" : "false");
      });
      scope.querySelectorAll("[data-atlas-diagram]").forEach(function (card) {
        var animated = card.getAttribute("data-animated") === "1";
        var cardKind = card.getAttribute("data-kind");
        var show = kind === "all" || (kind === "animated" && animated) || cardKind === kind;
        card.hidden = !show;
      });
    });
  });
}

function tilt(root) {
  if (motionOff()) return;
  (root || document).querySelectorAll("[data-parallax]").forEach(function (row) {
    if (row.dataset.bound === "1") return;
    row.dataset.bound = "1";
    row.addEventListener("pointermove", function (event) {
      var box = row.getBoundingClientRect();
      var dx = (event.clientX - box.left) / box.width - 0.5;
      row.style.setProperty("--lean", (dx * 8).toFixed(2) + "deg");
    });
  });
}

function openSpace() {
  var host = document.getElementById("heroMount");
  if (motionOff()) return;
  import("./space.js").then(function (mod) {
    if (host && host.dataset.opened !== "1") {
      host.dataset.opened = "1";
      host.hidden = false;
      var button = document.getElementById("openSpace");
      if (button) button.hidden = true;
      mod.mountTopology(host);
    }
    if (mod.mountCardIcons && !narrowScreen()) mod.mountCardIcons();
  }).catch(function () { /* the fallback sentence stays */ });
}

function scheduleSpace() {
  var host = document.getElementById("heroMount");
  var button = document.getElementById("openSpace");
  if (!host) return;
  if (motionOff()) {
    if (button) button.hidden = true;
    return;
  }
  var started = false;
  function start() {
    if (started || motionOff()) return;
    started = true;
    openSpace();
  }
  if (button) button.addEventListener("click", start);
  if (narrowScreen()) {
    host.addEventListener("pointerdown", function (event) {
      if (event.target.closest && event.target.closest("[data-fail], #openSpace")) return;
      start();
    }, { once: true });
    return;
  }
  function kick() {
    if (window.requestIdleCallback) window.requestIdleCallback(start, { timeout: 1500 });
    else window.setTimeout(start, 400);
  }
  if (document.readyState === "complete") kick();
  else window.addEventListener("load", kick, { once: true });
}

function scheduleLibraries() {
  whenNear("[data-d3-chart]", function () {
    loadClassic("vendor/d3.min.js").then(function () { drawD3(document); }).catch(function () {});
  });
  whenNear("[data-rough-chart]", function () {
    loadClassic("vendor/rough.js").then(function () { drawRough(document); }).catch(function () {});
  });
  whenNear("#mindmap", function () {
    loadClassic("vendor/markmap-view.js").then(function () { drawMindmap(); }).catch(function () {});
  });
}

var COPY = {
  en: { "hero-title": "Learn to build AI systems you can test.", "hero-lede": "A lifelong student of systems, networking, voice, and the contact center, studying AI omni-channel agents. The map is prompt, model, retrieval, tools, and an eval gate. No account. No key required to read it.", eyebrow: "Offline course · MIT code · CC BY-NC-SA content", start: "Start the course", play: "Open playgrounds", regions: "Regions", tracks: "Tracks", lessons: "Lessons", hours: "Reading time", "hours-unit": "hours", network: "Network calls", "nav-diagrams": "Diagrams", "nav-flows": "Flows", "nav-charts": "Charts", "nav-cheats": "Cheat Codes", "nav-play": "Play", "nav-ecosystem": "Ecosystem", "nav-downloads": "Downloads", "nav-careers": "Careers" },
  es: { "hero-title": "Aprende a construir sistemas de IA que puedes probar.", "hero-lede": "Estudiante de sistemas, redes, voz y contact center, aprendiendo agentes de IA omnicanal. Un curso gratis y sin red. El mapa que brilla es el camino: prompt, modelo, recuperación, herramientas y una puerta de evaluación.", eyebrow: "Curso sin red · código MIT · contenido CC BY-NC-SA", start: "Empezar el curso", play: "Abrir laboratorios", regions: "Regiones", tracks: "Rutas", lessons: "Lecciones", hours: "Tiempo de lectura", "hours-unit": "horas", network: "Llamadas de red", "nav-diagrams": "Diagramas", "nav-flows": "Flujos", "nav-charts": "Gráficos", "nav-cheats": "Chuletas", "nav-play": "Jugar", "nav-ecosystem": "Ecosistema", "nav-downloads": "Descargas", "nav-careers": "Carreras" },
  hi: { "hero-title": "ऐसे एआई सिस्टम बनाएँ जिन्हें आप जाँच सकें।", "hero-lede": "सिस्टम, नेटवर्किंग, वॉइस और कॉन्टैक्ट सेंटर का छात्र, जो एआई ऑम्नी-चैनल एजेंट सीख रहा है। एक मुफ़्त ऑफ़लाइन पाठ्यक्रम। चमकता नक्शा रास्ता है: प्रॉम्प्ट, मॉडल, पुनर्प्राप्ति, उपकरण, और जाँच द्वार।", eyebrow: "ऑफ़लाइन पाठ्यक्रम · MIT कोड · CC BY-NC-SA", start: "पाठ्यक्रम शुरू करें", play: "प्रयोगशाला खोलें", regions: "क्षेत्र", tracks: "पथ", lessons: "पाठ", hours: "पढ़ने का समय", "hours-unit": "घंटे", network: "नेटवर्क कॉल", "nav-diagrams": "आरेख", "nav-flows": "प्रवाह", "nav-charts": "चार्ट", "nav-cheats": "चीट कोड", "nav-play": "खेल", "nav-ecosystem": "पारिस्थितिकी", "nav-downloads": "डाउनलोड", "nav-careers": "करियर" },
  te: { "hero-title": "మీరు పరీక్షించగల ఏఐ వ్యవస్థలను నిర్మించండి.", "hero-lede": "సిస్టమ్స్, నెట్‌వర్కింగ్, వాయిస్, కాంటాక్ట్ సెంటర్ విద్యార్థి. ఏఐ ఓమ్నీ-ఛానల్ ఏజెంట్లు నేర్చుకుంటున్నాను. ఉచిత ఆఫ్‌లైన్ కోర్సు. మెరుస్తున్న పటం మార్గం: ప్రాంప్ట్, మోడల్, రిట్రీవల్, టూల్స్, మరియు మూల్యాంకన ద్వారం.", eyebrow: "ఆఫ్‌లైన్ కోర్సు · MIT కోడ్ · CC BY-NC-SA", start: "కోర్సు మొదలు", play: "ల్యాబ్‌లు", regions: "ప్రాంతాలు", tracks: "మార్గాలు", lessons: "పాఠాలు", hours: "చదివే సమయం", "hours-unit": "గంటలు", network: "నెట్‌వర్క్ కాల్స్", "nav-diagrams": "చిత్రాలు", "nav-flows": "ప్రవాహాలు", "nav-charts": "చార్టులు", "nav-cheats": "చీట్ కోడ్స్", "nav-play": "ఆట", "nav-ecosystem": "పర్యావరణం", "nav-downloads": "డౌన్‌లోడ్స్", "nav-careers": "వృత్తులు" },
  fr: { "hero-title": "Apprenez à construire des systèmes d’IA que vous pouvez tester.", "hero-lede": "Étudiant des systèmes, du réseau, de la voix et du centre de contact, en route vers les agents IA omnicanaux. Un cours gratuit hors ligne. La carte lumineuse est le chemin : invite, modèle, recherche, outils et porte d’évaluation.", eyebrow: "Cours hors ligne · code MIT · contenu CC BY-NC-SA", start: "Commencer", play: "Ouvrir les labs", regions: "Régions", tracks: "Parcours", lessons: "Leçons", hours: "Temps de lecture", "hours-unit": "heures", network: "Appels réseau", "nav-diagrams": "Schémas", "nav-flows": "Flux", "nav-charts": "Graphiques", "nav-cheats": "Antisèches", "nav-play": "Jouer", "nav-ecosystem": "Écosystème", "nav-downloads": "Téléchargements", "nav-careers": "Carrières" },
  de: { "hero-title": "Lerne, KI-Systeme zu bauen, die du prüfen kannst.", "hero-lede": "Student für Systeme, Netze, Voice und Contact Center, auf dem Weg zu KI-Omnichannel-Agenten. Ein kostenloser Offline-Kurs. Die leuchtende Karte ist der Weg: Prompt, Modell, Suche, Werkzeuge und ein Prüf-Tor.", eyebrow: "Offline-Kurs · MIT-Code · CC BY-NC-SA", start: "Kurs starten", play: "Labore öffnen", regions: "Regionen", tracks: "Pfade", lessons: "Lektionen", hours: "Lesezeit", "hours-unit": "Stunden", network: "Netzaufrufe", "nav-diagrams": "Diagramme", "nav-flows": "Flüsse", "nav-charts": "Charts", "nav-cheats": "Spickzettel", "nav-play": "Spielen", "nav-ecosystem": "Ökosystem", "nav-downloads": "Downloads", "nav-careers": "Laufbahn" },
  ja: { "hero-title": "試せるAIシステムを作る。", "hero-lede": "システム、ネットワーク、音声、コンタクトセンターを学ぶ学生。今はAIオムニチャネルエージェントを勉強中。無料のオフライン講座。光る地図が道です。プロンプト、モデル、検索、ツール、評価の門。", eyebrow: "オフライン講座 · MITコード · CC BY-NC-SA", start: "講座を始める", play: "実習を開く", regions: "地域", tracks: "コース", lessons: "レッスン", hours: "読む時間", "hours-unit": "時間", network: "ネットワーク呼び出し", "nav-diagrams": "図", "nav-flows": "フロー", "nav-charts": "チャート", "nav-cheats": "早見表", "nav-play": "実習", "nav-ecosystem": "周辺", "nav-downloads": "ダウンロード", "nav-careers": "進路" },
  ar: { "hero-title": "تعلّم بناء أنظمة ذكاء يمكن اختبارها.", "hero-lede": "طالب أنظمة وشبكات وصوت ومركز اتصال، يدرس وكلاء الذكاء الاصطناعي عبر القنوات. دورة مجانية بلا شبكة. الخريطة المضيئة هي المسار: الأمر، النموذج، الاسترجاع، الأدوات، وبوابة التقييم.", eyebrow: "دورة بلا شبكة · رخصة MIT · محتوى CC BY-NC-SA", start: "ابدأ الدورة", play: "افتح المختبرات", regions: "المناطق", tracks: "المسارات", lessons: "الدروس", hours: "وقت القراءة", "hours-unit": "ساعات", network: "نداءات الشبكة", "nav-diagrams": "مخططات", "nav-flows": "تدفقات", "nav-charts": "رسوم", "nav-cheats": "أوراق مساعدة", "nav-play": "تدريب", "nav-ecosystem": "المنظومة", "nav-downloads": "تنزيلات", "nav-careers": "مسارات مهنية" }
};

function applyLanguage(code) {
  var table = COPY[code] || COPY.en;
  document.querySelectorAll("[data-i18n]").forEach(function (node) {
    var key = node.getAttribute("data-i18n");
    if (table[key]) node.textContent = table[key];
  });
  document.documentElement.lang = code;
  document.documentElement.dir = code === "ar" ? "rtl" : "ltr";
  try { localStorage.setItem("ailab-lang", code); } catch (err) { /* ignore */ }
  var chosen = COPY[code] ? code : "en";
  document.querySelectorAll("[data-lang-select]").forEach(function (select) { select.value = chosen; });
  var setLang = document.getElementById("setLang");
  if (setLang) setLang.value = chosen;
}

function wireLanguage() {
  document.querySelectorAll("[data-lang-select]").forEach(function (select) {
    if (select.dataset.bound === "1") return;
    select.dataset.bound = "1";
    select.addEventListener("change", function () { applyLanguage(select.value); });
  });
  var saved = "en";
  try { saved = localStorage.getItem("ailab-lang") || "en"; } catch (err) { saved = "en"; }
  applyLanguage(saved);
}

function pinChrome() {
  var bar = document.querySelector(".labbar");
  if (!bar) return;
  document.documentElement.style.setProperty("--labbar-h", bar.offsetHeight + "px");
}

function ensureLightbox() {
  var box = document.getElementById("diagramLightbox");
  if (box) return box;
  box = document.createElement("div");
  box.id = "diagramLightbox";
  box.className = "lightbox";
  box.hidden = true;
  box.innerHTML = '<div class="lightbox-card" role="dialog" aria-modal="true" aria-labelledby="lightboxTitle">'
    + '<h2 id="lightboxTitle">Diagram</h2>'
    + '<div class="badge-row">'
    + '<button type="button" class="btn" data-flow="play">Play</button>'
    + '<button type="button" class="btn" data-flow="pause">Pause</button>'
    + '<button type="button" class="btn" data-flow="step">Step</button>'
    + '<button type="button" class="btn" data-flow="close">Close</button>'
    + '</div><div data-flow-stage></div><p data-flow-why></p>'
    + '<p class="block-note">The moving dot is the packet on this study path. Emergency stays on the voice platform.</p></div>';
  document.body.appendChild(box);
  box.addEventListener("click", function (event) {
    var action = event.target.getAttribute && event.target.getAttribute("data-flow");
    if (event.target === box || action === "close") {
      box.hidden = true;
      return;
    }
    var svg = box.querySelector("svg");
    if (!svg || !action) return;
    if (action === "pause" && svg.pauseAnimations) svg.pauseAnimations();
    if (action === "play" && svg.unpauseAnimations) svg.unpauseAnimations();
    if (action === "step" && svg.setCurrentTime) {
      if (svg.pauseAnimations) svg.pauseAnimations();
      var now = svg.getCurrentTime ? svg.getCurrentTime() : 0;
      svg.setCurrentTime(now + 0.35);
    }
  });
  return box;
}

function openDiagram(card) {
  var source = card.querySelector("svg");
  if (!source) return;
  var box = ensureLightbox();
  var stage = box.querySelector("[data-flow-stage]");
  var title = card.querySelector("h3");
  box.querySelector("#lightboxTitle").textContent = title ? title.textContent : "Diagram";
  var why = card.querySelector("p");
  box.querySelector("[data-flow-why]").textContent = why ? why.textContent : "";
  stage.innerHTML = "";
  var clone = source.cloneNode(true);
  clone.removeAttribute("id");
  stage.appendChild(clone);
  box.hidden = false;
  if (clone.unpauseAnimations) clone.unpauseAnimations();
}

function wireLightbox() {
  if (document.body.dataset.lightbox === "1") return;
  document.body.dataset.lightbox = "1";
  document.addEventListener("click", function (event) {
    var button = event.target.closest && event.target.closest("[data-enlarge]");
    if (!button) return;
    var card = button.closest("[data-atlas-diagram]");
    if (card) openDiagram(card);
  });
}

function wireRail() {
  var button = document.getElementById("railBtn");
  var root = document.documentElement;
  function apply(open) {
    if (open) root.setAttribute("data-rail", "open");
    else root.removeAttribute("data-rail");
    if (button) button.setAttribute("aria-pressed", open ? "true" : "false");
    try { localStorage.setItem("ailab-rail", open ? "open" : "slim"); } catch (err) { /* ignore */ }
    window.dispatchEvent(new Event("resize"));
  }
  if (button && button.dataset.bound !== "1") {
    button.dataset.bound = "1";
    button.addEventListener("click", function () {
      apply(root.getAttribute("data-rail") !== "open");
    });
  }
  var saved = "slim";
  try { saved = localStorage.getItem("ailab-rail") || "slim"; } catch (err) { saved = "slim"; }
  apply(saved === "open");
}

function boot(root) {
  pinChrome();
  wireRail();
  wireLanguage();
  wireLightbox();
  paintCounts(root);
  wireThemes(root);
  wireAtlas(root);
  tilt(root);
  if (!motionOff() && !narrowScreen() && document.querySelector(".tilt-card")) {
    import("../../vendor/anime.esm.min.js").then(function (mod) {
      try {
        mod.animate(".tilt-card", { rotateY: [-10, 8], duration: 2800, loop: true, alternate: true, ease: "inOutQuad" });
      } catch (err) { /* counters still ran */ }
    }).catch(function () {});
  }
  wirePhone();
  wireGuide();
}

window.CampusCelebrate = function () {
  if (motionOff()) return;
  loadClassic("vendor/confetti.browser.js").then(function () {
    if (typeof window.confetti === "function") {
      window.confetti({ particleCount: 40, spread: 50, origin: { y: 0.75 } });
    }
  }).catch(function () {});
};

window.addEventListener("resize", pinChrome);
document.addEventListener("campus-show", function () {
  boot(document.getElementById("stage") || document);
  scheduleLibraries();
});
document.addEventListener("campus-mount", function () {
  boot(document.getElementById("stage") || document);
  scheduleLibraries();
});
boot(document);
scheduleLibraries();
scheduleSpace();
