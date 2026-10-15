/* Arcade, themes, mascot, badges, and the Konami greeting. No network. */
(function () {
  var THEMES = ["neon", "holographic", "cyberpunk", "sunset", "light", "dark"];
  var MASCOT_KEY = "ailab-mascot";
  var face = 0;
  try { face = Number(localStorage.getItem(MASCOT_KEY) || "0") || 0; } catch (err) { face = 0; }

  function paintFace() {
    document.documentElement.setAttribute("data-mascot", String(face % 4));
  }
  paintFace();
  var motion = document.documentElement.getAttribute("data-motion") === "reduce"
    || window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!motion) {
    function nextFace() {
      face = (face + 1) % 4;
      paintFace();
      try { localStorage.setItem(MASCOT_KEY, String(face)); } catch (err) { /* ignore */ }
    }
    window.setInterval(nextFace, 90000);
    document.addEventListener("campus-show", nextFace);
  }

  var themeBtn = document.getElementById("themeBtn");
  if (themeBtn && window.CampusTheme) {
    themeBtn.addEventListener("click", function (event) {
      event.stopImmediatePropagation();
      var current = document.documentElement.getAttribute("data-theme") || "futuristic";
      var index = THEMES.indexOf(current);
      window.CampusTheme(THEMES[(index + 1) % THEMES.length]);
    }, true);
  }

  var keys = [];
  var konami = ["ArrowUp", "ArrowUp", "ArrowDown", "ArrowDown", "ArrowLeft", "ArrowRight", "ArrowLeft", "ArrowRight", "b", "a"];
  document.addEventListener("keydown", function (event) {
    var name = event.key.length === 1 ? event.key.toLowerCase() : event.key;
    keys.push(name);
    if (keys.length > konami.length) keys.shift();
    if (keys.join(",") === konami.join(",")) {
      document.documentElement.setAttribute("data-egg", "1");
      var note = document.getElementById("eggNote");
      if (!note) {
        note = document.createElement("p");
        note.id = "eggNote";
        note.className = "labfoot-note";
        note.textContent = "CypherMonkey waves. The egg is a greeting, not a new lesson. Progress is still the marks in this browser.";
        var foot = document.querySelector(".labfoot");
        if (foot) foot.appendChild(note);
      }
    }
  });

  function studiedCount() {
    try { return JSON.parse(localStorage.getItem("ailab-v3-studied") || "[]").length; } catch (err) { return 0; }
  }

  function wireArcade() {
    var root = document.getElementById("arcade");
    if (!root || root.dataset.wired === "1") return;
    root.dataset.wired = "1";
    var scoreLine = document.getElementById("portScore");
    var choices = root.querySelectorAll("[data-port]");
    var asked = 0;
    var right = 0;
    choices.forEach(function (button) {
      button.addEventListener("click", function () {
        var card = button.closest("[data-port-card]");
        if (!card || card.dataset.done === "1") return;
        card.dataset.done = "1";
        asked += 1;
        var good = button.getAttribute("data-ok") === "1";
        if (good) right += 1;
        card.querySelectorAll("[data-port]").forEach(function (peer) {
          if (peer.getAttribute("data-ok") === "1") peer.classList.add("port-hit");
          if (peer === button && !good) peer.classList.add("port-miss");
        });
        button.setAttribute("aria-pressed", "true");
        var why = card.querySelector(".why");
        if (why) why.hidden = false;
        if (scoreLine) scoreLine.textContent = right + " of " + asked + " ports correct in this sitting";
        if (good && right === 8 && window.CampusCelebrate) window.CampusCelebrate();
        try { localStorage.setItem("ailab-ports-best", String(Math.max(right, Number(localStorage.getItem("ailab-ports-best") || "0")))); } catch (err) { /* ignore */ }
        paintBadges();
      });
    });

    var built = [];
    var target = (document.getElementById("flowTarget") || {}).textContent || "";
    var goal = target.split("|").map(function (part) { return part.trim(); }).filter(Boolean);
    var out = document.getElementById("flowOut");
    function paintFlow() {
      if (!out) return;
      var same = built.length === goal.length && built.every(function (step, index) { return step === goal[index]; });
      if (!built.length) out.textContent = "Nothing clicked yet.";
      else if (same) {
        out.textContent = "That order matches the study path. Emergency still leaves the model.";
        if (window.CampusCelebrate) window.CampusCelebrate();
      }
      else out.textContent = "So far: " + built.join(" → ") + ".";
    }
    root.querySelectorAll("[data-flow]").forEach(function (button) {
      button.addEventListener("click", function () {
        if (button.classList.contains("on")) return;
        built.push(button.getAttribute("data-flow"));
        button.classList.add("on");
        paintFlow();
      });
    });
    var reset = document.getElementById("flowReset");
    if (reset) {
      reset.addEventListener("click", function () {
        built = [];
        root.querySelectorAll("[data-flow]").forEach(function (button) { button.classList.remove("on"); });
        paintFlow();
      });
    }
    var mapOut = document.getElementById("mapOut");
    root.querySelectorAll("[data-map]").forEach(function (node) {
      function showMap() {
        root.querySelectorAll("[data-map]").forEach(function (other) {
          other.classList.toggle("on", other === node);
        });
        if (mapOut) mapOut.textContent = node.getAttribute("data-map") + ": " + (node.getAttribute("data-blurb") || "");
      }
      node.addEventListener("click", showMap);
      node.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          showMap();
        }
      });
    });

    var day = document.getElementById("dailyCard");
    if (day) {
      var cards = day.querySelectorAll("[data-daily]");
      if (cards.length) {
        var index = Math.floor(Date.now() / 86400000) % cards.length;
        cards.forEach(function (card, cardIndex) { card.hidden = cardIndex !== index; });
        var label = document.getElementById("dailyIndex");
        if (label) label.textContent = "Prompt " + (index + 1) + " of " + cards.length;
      }
    }
    paintBadges();
    var share = document.getElementById("shareBtn");
    if (share) share.addEventListener("click", shareCard);
  }

  function paintBadges() {
    var done = studiedCount();
    var ports = 0;
    try { ports = Number(localStorage.getItem("ailab-ports-best") || "0"); } catch (err) { ports = 0; }
    document.querySelectorAll("[data-badge]").forEach(function (badge) {
      var need = Number(badge.getAttribute("data-need") || "0");
      var kind = badge.getAttribute("data-badge");
      var on = kind === "ports" ? ports >= need : done >= need;
      badge.classList.toggle("on", on);
    });
  }

  function shareCard() {
    var done = studiedCount();
    var total = (window.CampusCatalog && window.CampusCatalog.order.length) || done;
    var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="800" height="420" viewBox="0 0 800 420">'
      + '<rect width="800" height="420" fill="#070b16"/>'
      + '<text x="40" y="80" fill="#67e8f9" font-family="system-ui,sans-serif" font-size="18">AI Lab Free University</text>'
      + '<text x="40" y="150" fill="#f8fafc" font-family="system-ui,sans-serif" font-size="42">' + done + ' of ' + total + ' marked</text>'
      + '<text x="40" y="210" fill="#93b4c9" font-family="system-ui,sans-serif" font-size="20">Saved in this browser. Not a certificate.</text>'
      + '<text x="40" y="300" fill="#a5f3fc" font-family="system-ui,sans-serif" font-size="22">cyphermonkeylabs.com</text>'
      + '<text x="40" y="350" fill="#64748b" font-family="system-ui,sans-serif" font-size="16">Independent study project. Trademarks belong to their owners.</text>'
      + '</svg>';
    var blob = new Blob([svg], { type: "image/svg+xml" });
    var url = URL.createObjectURL(blob);
    var link = document.getElementById("shareLink");
    if (link) {
      link.href = url;
      link.hidden = false;
      link.download = "ai-lab-progress.svg";
      link.textContent = "Save the result card (SVG)";
    }
  }

  document.addEventListener("campus-show", wireArcade);
  document.addEventListener("campus-progress", paintBadges);
  var offline = document.getElementById("offlineBtn");
  if (offline) {
    offline.addEventListener("click", function () {
      var status = document.getElementById("offlineStatus");
      if (status) status.textContent = "The zip is the full bundle. After one visit on this site, the service worker keeps the files you opened.";
    });
  }
})();
