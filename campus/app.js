/* App shell: palette, progress mirror, playgrounds, mini player. */
(function () {
  var math = window.LabPlay;
  function reduceMotion() {
    var stored = "";
    try { stored = localStorage.getItem("ailab-v3-motion") || ""; } catch (err) { stored = ""; }
    if (stored === "reduce") return true;
    if (stored === "full") return false;
    return document.documentElement.getAttribute("data-motion") === "reduce"
      || window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }
  var palette = document.getElementById("palette");
  var paletteInput = document.getElementById("paletteInput");
  var paletteList = document.getElementById("paletteList");
  var cmdBtn = document.getElementById("cmdBtn");
  var index = [];
  var active = 0;
  var lastFocus = null;

  function lessons() {
    return Array.prototype.slice.call(document.querySelectorAll("article.lesson"));
  }

  function buildIndex() {
    if (index.length) return;
    var seen = {};
    function add(item) {
      if (seen[item.href || item.title]) return;
      seen[item.href || item.title] = 1;
      index.push(item);
    }
    add({ title: "Home", hint: "Dashboard", href: "#home", kind: "Place" });
    add({ title: "Track map", hint: "Full path", href: "#map", kind: "Place" });
    add({ title: "Playgrounds", hint: "Offline labs", href: "#play", kind: "Lab" });
    add({ title: "Cheat codes", hint: "Sheets, PDFs, flashcards", href: "#downloads", kind: "Place" });
    add({ title: "Arcade", hint: "Ports, flows, daily prompt", href: "#arcade", kind: "Lab" });
    Array.prototype.forEach.call(document.querySelectorAll(".launch-card"), function (card) {
      var title = card.querySelector("strong");
      if (!title) return;
      add({ title: title.textContent, hint: "Playground", href: card.getAttribute("href"), kind: "Lab" });
    });
    add({ title: "Studio", hint: "Charts and calculators", href: "#studio", kind: "Lab" });
    add({ title: "Builds", hint: "Walkthroughs", href: "#builds", kind: "Lab" });
    Array.prototype.forEach.call(document.querySelectorAll("a.school-jump"), function (link) {
      var name = link.querySelector(".sname");
      if (!name) return;
      add({ title: name.textContent, hint: "Track", href: link.getAttribute("href"), kind: "Track" });
    });
    var catalog = window.CampusCatalog;
    if (catalog) {
      var schoolName = {};
      catalog.schools.forEach(function (school) { schoolName[school.id] = school.name; });
      catalog.lessons.forEach(function (item) {
        var link = document.querySelector('a.ll[data-id="' + item.id + '"]');
        add({
          title: item.title,
          hint: schoolName[item.school] || "Lesson",
          href: "#" + item.id,
          kind: "Lesson",
          hay: link ? (link.getAttribute("data-search") || "") : (item.summary || "")
        });
      });
    }
    add({
      title: "Open settings",
      hint: "Theme, voice, motion, type size",
      kind: "Action",
      run: function () { var button = document.getElementById("settingsBtn"); if (button) button.click(); }
    });
    add({
      title: "Tips and tricks",
      hint: "Pro tips, traps, and a cheat sheet",
      kind: "Action",
      run: function () { var button = document.getElementById("tipsBtn"); if (button) button.click(); }
    });
    add({
      title: "Switch theme",
      hint: "Dark or light",
      kind: "Action",
      run: function () { var button = document.getElementById("themeBtn"); if (button) button.click(); }
    });
    add({
      title: "Toggle high contrast",
      hint: "Stronger edges",
      kind: "Action",
      run: function () { var button = document.getElementById("contrastBtn"); if (button) button.click(); }
    });
  }

  function matches(item, query) {
    if (!query) return true;
    var hay = (item.title + " " + item.hint + " " + (item.hay || "") + " " + item.kind).toLowerCase();
    return query.split(/\s+/).every(function (part) { return hay.indexOf(part) !== -1; });
  }

  function resultsFor(query) {
    var q = query.trim().toLowerCase();
    return index.filter(function (item) { return matches(item, q); }).slice(0, 12);
  }

  function paintPalette() {
    var rows = resultsFor(paletteInput.value);
    if (active >= rows.length) active = 0;
    paletteList.replaceChildren();
    if (!rows.length) {
      var empty = document.createElement("p");
      empty.className = "palette-empty";
      empty.textContent = "No lesson matches that.";
      paletteList.appendChild(empty);
      return;
    }
    rows.forEach(function (item, i) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "palette-item";
      button.setAttribute("role", "option");
      button.setAttribute("aria-selected", i === active ? "true" : "false");
      button.innerHTML = "<small>" + item.kind + "</small><strong></strong><em></em>";
      button.querySelector("strong").textContent = item.title;
      button.querySelector("em").textContent = item.hint;
      button.addEventListener("click", function () { choose(item); });
      paletteList.appendChild(button);
    });
  }

  function choose(item) {
    closePalette();
    if (item.run) item.run();
    else if (item.href) location.hash = item.href;
  }

  function openPalette() {
    buildIndex();
    lastFocus = document.activeElement;
    palette.hidden = false;
    paletteInput.value = "";
    active = 0;
    paintPalette();
    paletteInput.focus();
  }

  function closePalette() {
    if (palette.hidden) return;
    palette.hidden = true;
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  if (cmdBtn) cmdBtn.addEventListener("click", openPalette);
  if (palette) {
    palette.addEventListener("click", function (event) {
      if (event.target.closest("[data-palette-close]")) closePalette();
    });
    palette.addEventListener("keydown", function (event) {
      var rows = resultsFor(paletteInput.value);
      if (event.key === "Escape") { event.preventDefault(); closePalette(); return; }
      if (event.key === "ArrowDown") { event.preventDefault(); active = Math.min(rows.length - 1, active + 1); paintPalette(); return; }
      if (event.key === "ArrowUp") { event.preventDefault(); active = Math.max(0, active - 1); paintPalette(); return; }
      if (event.key === "Enter") {
        event.preventDefault();
        if (rows[active]) choose(rows[active]);
        return;
      }
      if (event.key !== "Tab") return;
      var focusable = [paletteInput].concat(Array.prototype.slice.call(paletteList.querySelectorAll("button")));
      if (!focusable.length) return;
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    });
    paletteInput.addEventListener("input", function () { active = 0; paintPalette(); });
  }

  document.addEventListener("keydown", function (event) {
    var key = event.key.toLowerCase();
    if ((event.metaKey || event.ctrlKey) && key === "k") {
      event.preventDefault();
      if (palette.hidden) openPalette();
      else closePalette();
    }
  });

  function mirrorDash() {
    var src = document.getElementById("ringValue");
    var dst = document.getElementById("dashRing");
    if (src && dst) dst.setAttribute("stroke-dasharray", src.getAttribute("stroke-dasharray") || "0 100");
    var label = document.getElementById("studiedLabel");
    var pct = document.getElementById("dashPct");
    var total = (window.CampusCatalog && window.CampusCatalog.order.length) || lessons().length || 1;
    var done = 0;
    if (label) {
      var match = /(\d+)/.exec(label.textContent || "");
      done = match ? Number(match[1]) : 0;
    }
    if (pct) pct.textContent = Math.round((done / total) * 100) + "%";
    var caption = document.getElementById("dashCaption");
    var homeProg = document.getElementById("homeProg");
    if (caption && homeProg) caption.textContent = homeProg.textContent;
    var go = document.getElementById("dashContinue");
    var link = document.getElementById("continueLink");
    if (go && link) {
      go.setAttribute("href", link.getAttribute("href") || "#00-01");
      go.textContent = link.textContent || "Continue";
    }
  }

  function animateCounts() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-count]"), function (el) {
      if (el.dataset.counted) return;
      el.dataset.counted = "1";
      var target = Number(el.dataset.count || "0");
      if (reduceMotion() || target === 0) { el.textContent = String(target); return; }
      var start = performance.now();
      function frame(now) {
        var t = Math.min(1, (now - start) / 700);
        var eased = 1 - Math.pow(1 - t, 3);
        el.textContent = String(Math.round(target * eased));
        if (t < 1) requestAnimationFrame(frame);
      }
      requestAnimationFrame(frame);
    });
  }

  function bootTilt() {
    if (reduceMotion() || window.matchMedia("(hover: none)").matches) return;
    Array.prototype.forEach.call(document.querySelectorAll(".tilt"), function (card) {
      var face = card.querySelector(".tilt-face") || card;
      card.addEventListener("pointermove", function (event) {
        var rect = card.getBoundingClientRect();
        var px = (event.clientX - rect.left) / rect.width;
        var py = (event.clientY - rect.top) / rect.height;
        card.style.setProperty("--mx", (px * 100) + "%");
        card.style.setProperty("--my", (py * 100) + "%");
        face.style.transform = "rotateX(" + ((0.5 - py) * 8).toFixed(2) + "deg) rotateY(" + ((px - 0.5) * 10).toFixed(2) + "deg)";
      });
      card.addEventListener("pointerleave", function () { face.style.transform = ""; });
    });
  }

  function applyTrackFilter(mode) {
    var shown = 0;
    Array.prototype.forEach.call(document.querySelectorAll(".track-card[data-school]"), function (card) {
      var links = Array.prototype.slice.call(document.querySelectorAll('.school-block[data-school="' + card.dataset.school + '"] a.ll'));
      var done = links.length > 0 && links.every(function (link) { return link.classList.contains("done"); });
      var show = mode === "done" ? done : mode === "open" ? !done : true;
      card.hidden = !show;
      if (show) shown += 1;
    });
    var empty = document.getElementById("trackEmpty");
    if (empty) empty.hidden = shown !== 0;
  }

  Array.prototype.forEach.call(document.querySelectorAll("[data-track-filter]"), function (button) {
    button.addEventListener("click", function () {
      Array.prototype.forEach.call(document.querySelectorAll("[data-track-filter]"), function (other) {
        other.setAttribute("aria-pressed", other === button ? "true" : "false");
      });
      applyTrackFilter(button.getAttribute("data-track-filter"));
    });
  });

  function clock(seconds) {
    if (!isFinite(seconds)) seconds = 0;
    var whole = Math.max(0, Math.floor(seconds));
    var mins = Math.floor(whole / 60);
    var rest = whole % 60;
    return mins + ":" + (rest < 10 ? "0" : "") + rest;
  }

  var player = document.getElementById("miniPlayer");
  var miniToggle = document.getElementById("miniToggle");
  var miniSeek = document.getElementById("miniSeek");
  var miniTitle = document.getElementById("miniTitle");
  var miniTime = document.getElementById("miniTime");
  var currentAudio = null;
  var seeking = false;

  var waveCache = {};
  var waveCtx = null;

  function captionWords(text) {
    return (text || "").split(/\s+/).filter(Boolean);
  }

  function paintCaption() {
    var node = document.getElementById("miniCaption");
    if (!node || !currentAudio) return;
    var text = currentAudio.getAttribute("data-caption") || "";
    var words = captionWords(text);
    if (!words.length) {
      node.textContent = "";
      return;
    }
    var duration = currentAudio.duration || 0;
    var index = 0;
    if (duration) index = Math.min(words.length - 1, Math.floor((currentAudio.currentTime / duration) * words.length));
    node.replaceChildren();
    words.forEach(function (word, i) {
      var span = document.createElement("span");
      if (i === index) span.className = "is-now";
      span.textContent = word;
      if (i) node.appendChild(document.createTextNode(" "));
      node.appendChild(span);
    });
  }

  function paintWave() {
    var canvas = document.getElementById("miniWave");
    if (!canvas || !currentAudio) return;
    var ctx = canvas.getContext("2d");
    var width = canvas.width;
    var height = canvas.height;
    ctx.clearRect(0, 0, width, height);
    var peaks = waveCache[currentAudio.src] || [];
    var duration = currentAudio.duration || 0;
    var progress = duration ? currentAudio.currentTime / duration : 0;
    ctx.fillStyle = "#818CF8";
    if (!peaks.length) {
      for (var i = 0; i < 64; i += 1) {
        var h = 8 + ((i * 17) % 28);
        ctx.globalAlpha = i / 64 < progress ? 1 : 0.35;
        ctx.fillRect(8 + i * 10, (height - h) / 2, 6, h);
      }
      ctx.globalAlpha = 1;
      return;
    }
    peaks.forEach(function (peak, i) {
      var h = Math.max(4, peak * (height - 8));
      ctx.globalAlpha = i / peaks.length < progress ? 1 : 0.35;
      ctx.fillRect((i / peaks.length) * width, (height - h) / 2, Math.max(2, width / peaks.length - 2), h);
    });
    ctx.globalAlpha = 1;
  }

  function captureWave(audio) {
    if (!audio.src || waveCache[audio.src] || !window.AudioContext) return;
    if (!waveCtx) {
      try { waveCtx = new window.AudioContext(); } catch (err) { return; }
    }
    fetch(audio.src).then(function (res) { return res.arrayBuffer(); }).then(function (buf) {
      return waveCtx.decodeAudioData(buf);
    }).then(function (buffer) {
      var data = buffer.getChannelData(0);
      var bars = 64;
      var size = Math.floor(data.length / bars) || 1;
      var peaks = [];
      for (var i = 0; i < bars; i += 1) {
        var max = 0;
        for (var j = 0; j < size; j += 1) {
          var sample = Math.abs(data[i * size + j] || 0);
          if (sample > max) max = sample;
        }
        peaks.push(max);
      }
      var top = Math.max.apply(null, peaks.concat([0.01]));
      waveCache[audio.src] = peaks.map(function (peak) { return peak / top; });
      paintWave();
    }).catch(function () { /* tone files still show a placeholder */ });
  }

  function paintPlayer() {
    if (!player || !currentAudio) return;
    var paused = currentAudio.paused;
    player.classList.toggle("is-paused", paused);
    miniToggle.setAttribute("aria-label", paused ? "Play audio" : "Pause audio");
    var duration = currentAudio.duration || 0;
    if (!seeking && duration) miniSeek.value = String(Math.round((currentAudio.currentTime / duration) * 1000));
    miniTime.textContent = clock(currentAudio.currentTime) + " / " + clock(duration);
    paintCaption();
    paintWave();
  }

  function attachAudio(audio) {
    if (currentAudio && currentAudio !== audio) currentAudio.pause();
    currentAudio = audio;
    var figure = audio.closest("figure");
    var caption = figure ? figure.querySelector("figcaption") : null;
    miniTitle.textContent = caption ? caption.textContent.replace(/\s+/g, " ").trim() : "Audio";
    player.hidden = false;
    document.body.classList.add("player-on");
    captureWave(audio);
    paintPlayer();
  }

  document.addEventListener("play", function (event) {
    if (!event.target || event.target.tagName !== "AUDIO") return;
    attachAudio(event.target);
  }, true);
  document.addEventListener("pause", function (event) {
    if (event.target === currentAudio) paintPlayer();
  }, true);
  document.addEventListener("timeupdate", function (event) {
    if (event.target === currentAudio) paintPlayer();
  }, true);
  document.addEventListener("ended", function (event) {
    if (event.target === currentAudio) paintPlayer();
  }, true);
  if (miniToggle) {
    miniToggle.addEventListener("click", function () {
      if (!currentAudio) return;
      if (currentAudio.paused) currentAudio.play();
      else currentAudio.pause();
    });
  }
  if (miniSeek) {
    miniSeek.addEventListener("pointerdown", function () { seeking = true; });
    miniSeek.addEventListener("input", function () {
      if (!currentAudio || !currentAudio.duration) return;
      currentAudio.currentTime = (Number(miniSeek.value) / 1000) * currentAudio.duration;
    });
    miniSeek.addEventListener("change", function () { seeking = false; paintPlayer(); });
  }
  var miniClose = document.getElementById("miniClose");
  if (miniClose) {
    miniClose.addEventListener("click", function () {
      if (currentAudio) currentAudio.pause();
      player.hidden = true;
      document.body.classList.remove("player-on");
    });
  }

  var playReady = false;
  var ragStep = 0;
  var ragTimer = 0;
  var agentStep = 0;
  var agentFrames = [];

  function tabFromHash() {
    var raw = (location.hash || "#play").replace(/^#/, "");
    if (raw.indexOf("play-") === 0) return raw.slice(5);
    return "attn";
  }

  function selectTab(name) {
    var known = {};
    Array.prototype.forEach.call(document.querySelectorAll(".play-tab"), function (tab) {
      known[tab.dataset.tab] = 1;
    });
    if (!known[name]) name = "attn";
    Array.prototype.forEach.call(document.querySelectorAll(".play-tab"), function (tab) {
      var on = tab.dataset.tab === name;
      tab.setAttribute("aria-selected", on ? "true" : "false");
      tab.tabIndex = on ? 0 : -1;
    });
    Array.prototype.forEach.call(document.querySelectorAll(".play-panel"), function (panel) {
      panel.hidden = panel.dataset.tab !== name;
    });
    var activeTab = document.querySelector('.play-tab[data-tab="' + name + '"]');
    if (activeTab) {
      var cat = activeTab.getAttribute("data-cat");
      Array.prototype.forEach.call(document.querySelectorAll(".play-cat"), function (button) {
        button.setAttribute("aria-pressed", button.getAttribute("data-cat") === cat ? "true" : "false");
      });
      if (activeTab.scrollIntoView) {
        activeTab.scrollIntoView({ inline: "center", block: "nearest", behavior: reduceMotion() ? "auto" : "smooth" });
      }
    }
    var activePanel = document.getElementById("play-" + name);
    if (activePanel && activePanel.scrollIntoView) {
      activePanel.scrollIntoView({ behavior: reduceMotion() ? "auto" : "smooth", block: "start" });
    }
    if (name !== "rag") window.clearInterval(ragTimer);
    if (name === "attn") { drawAttention(); drawBpe(); }
    if (name === "embed") {
      window.requestAnimationFrame(function () {
        var mount = document.getElementById("embedMount");
        if (mount) watchSpace(mount, "embed");
      });
    }
    if (name === "cards") bootCards();
    if (name === "rag") drawRag();
    if (name === "agent") drawAgent();
    if (name === "eval") drawEval();
    if (name === "lora") drawLora();
    if (window.LabExtra) window.LabExtra.onTab(name);
  }

  function bootTabs() {
    var tabs = Array.prototype.slice.call(document.querySelectorAll(".play-tab"));
    tabs.forEach(function (tab, index) {
      tab.addEventListener("click", function () { location.hash = "#play-" + tab.dataset.tab; });
      tab.addEventListener("keydown", function (event) {
        var next = index;
        if (event.key === "ArrowRight") next = (index + 1) % tabs.length;
        else if (event.key === "ArrowLeft") next = (index - 1 + tabs.length) % tabs.length;
        else return;
        event.preventDefault();
        tabs[next].focus();
        location.hash = "#play-" + tabs[next].dataset.tab;
      });
    });
    Array.prototype.forEach.call(document.querySelectorAll(".play-cat"), function (button) {
      if (button.dataset.bound) return;
      button.dataset.bound = "1";
      button.addEventListener("click", function () {
        var cat = button.getAttribute("data-cat");
        var first = document.querySelector('.play-tab[data-cat="' + cat + '"]');
        if (first && first.scrollIntoView) first.scrollIntoView({ inline: "start", block: "nearest", behavior: reduceMotion() ? "auto" : "smooth" });
        Array.prototype.forEach.call(document.querySelectorAll(".play-cat"), function (other) {
          other.setAttribute("aria-pressed", other === button ? "true" : "false");
        });
      });
    });
  }

  function fitCanvas(canvas) {
    var width = canvas.clientWidth || 640;
    var height = Number(canvas.getAttribute("height")) || 280;
    var ratio = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * (width / 880) * ratio);
    var ctx = canvas.getContext("2d");
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    return { ctx: ctx, w: width, h: height * (width / 880) };
  }

  function ink() {
    var styles = getComputedStyle(document.documentElement);
    return {
      ink: styles.getPropertyValue("--ink").trim() || "#E8EDF7",
      muted: styles.getPropertyValue("--muted").trim() || "#9AA8C3",
      line: styles.getPropertyValue("--line").trim() || "#2A3650",
      primary: styles.getPropertyValue("--primary").trim() || "#6366F1",
      cyan: styles.getPropertyValue("--cyan").trim() || "#22D3EE",
      green: styles.getPropertyValue("--green").trim() || "#34D399",
      amber: styles.getPropertyValue("--amber").trim() || "#FBBF24"
    };
  }

  function drawAttention() {
    var canvas = document.getElementById("pgCanvas");
    var text = document.getElementById("pgText");
    var slider = document.getElementById("pgQuery");
    var row = document.getElementById("pgTokens");
    var read = document.getElementById("pgRead");
    if (!canvas || !math) return;
    var tokens = math.tokenize(text.value || "");
    if (!tokens.length) tokens = ["…"];
    var weights = math.attention(tokens);
    var query = Math.max(0, Math.min(tokens.length - 1, Number(slider.value) || 0));
    slider.max = String(tokens.length - 1);
    slider.value = String(query);
    row.replaceChildren();
    tokens.forEach(function (token, i) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "token" + (i === query ? " is-on" : "");
      button.textContent = token;
      button.addEventListener("click", function () { slider.value = String(i); drawAttention(); });
      row.appendChild(button);
    });
    var view = fitCanvas(canvas);
    var ctx = view.ctx;
    var colors = ink();
    ctx.clearRect(0, 0, view.w, view.h);
    var n = tokens.length;
    var cell = Math.min(28, (view.w * 0.46) / n);
    var left = 16;
    var top = 36;
    ctx.font = "12px system-ui, sans-serif";
    ctx.fillStyle = colors.muted;
    ctx.fillText("Query down, key across. Future cells stay empty.", left, 18);
    for (var r = 0; r < n; r += 1) {
      for (var c = 0; c < n; c += 1) {
        var weight = weights[r][c];
        ctx.globalAlpha = c > r ? 0.15 : 0.2 + weight * 0.8;
        ctx.fillStyle = r === query ? colors.cyan : colors.primary;
        ctx.fillRect(left + c * (cell + 3), top + r * (cell + 3), cell, cell);
      }
    }
    ctx.globalAlpha = 1;
    var originX = view.w * 0.58;
    var baseY = view.h - 36;
    tokens.forEach(function (token, i) {
      var x = originX + (i * ((view.w - originX - 16) / Math.max(1, n)));
      ctx.fillStyle = i === query ? colors.cyan : colors.ink;
      ctx.font = "12px system-ui, sans-serif";
      ctx.fillText(token.slice(0, 8), x, baseY);
      if (i === query) return;
      var weight = weights[query][i];
      if (!weight) return;
      ctx.strokeStyle = colors.primary;
      ctx.globalAlpha = 0.25 + weight * 0.75;
      ctx.lineWidth = 1 + weight * 6;
      ctx.beginPath();
      ctx.moveTo(originX + (query * ((view.w - originX - 16) / Math.max(1, n))) + 12, baseY - 16);
      ctx.quadraticCurveTo((x + originX) / 2, baseY - 80 - weight * 40, x + 12, baseY - 16);
      ctx.stroke();
      ctx.globalAlpha = 1;
    });
    var best = 0;
    var bestAt = 0;
    weights[query].forEach(function (weight, i) {
      if (weight >= best) { best = weight; bestAt = i; }
    });
    read.textContent = "Query “" + tokens[query] + "” puts the most weight on “" + tokens[bestAt] + "” (" + best.toFixed(2) + "). Later tokens are masked.";
    canvas.setAttribute("aria-label", read.textContent);
  }

  function drawRag() {
    var canvas = document.getElementById("ragCanvas");
    var input = document.getElementById("ragQuestion");
    var hits = document.getElementById("ragHits");
    var answer = document.getElementById("ragAnswer");
    if (!canvas || !math) return;
    var query = input.value || "";
    var ranked = math.retrieve(query);
    var point = math.embed(query);
    var view = fitCanvas(canvas);
    var ctx = view.ctx;
    var colors = ink();
    ctx.clearRect(0, 0, view.w, view.h);
    function xy(x, y) {
      return [40 + ((x + 1) / 2) * (view.w - 80), view.h - 30 - ((y + 1) / 2) * (view.h - 60)];
    }
    ctx.strokeStyle = colors.line;
    ctx.strokeRect(24, 16, view.w - 48, view.h - 32);
    if (ragStep >= 1) {
      ranked.forEach(function (hit) {
        var pos = xy(hit.x, hit.y);
        ctx.fillStyle = hit.accept && ragStep >= 2 ? colors.green : colors.primary;
        ctx.globalAlpha = ragStep >= 2 && !hit.accept ? 0.35 : 1;
        ctx.beginPath();
        ctx.arc(pos[0], pos[1], ragStep >= 2 && hit === ranked[0] ? 8 : 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
        ctx.fillStyle = colors.muted;
        ctx.font = "11px system-ui, sans-serif";
        ctx.fillText(hit.id.split("#")[0].replace("policy-", ""), pos[0] + 8, pos[1] - 8);
      });
    }
    if (ragStep >= 2) {
      var qpos = xy(point[0], point[1]);
      ctx.fillStyle = colors.amber;
      ctx.beginPath();
      ctx.arc(qpos[0], qpos[1], 7, 0, Math.PI * 2);
      ctx.fill();
      var top = ranked[0];
      if (top) {
        var tpos = xy(top.x, top.y);
        ctx.strokeStyle = top.accept ? colors.green : colors.amber;
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.moveTo(qpos[0], qpos[1]);
        ctx.lineTo(tpos[0], tpos[1]);
        ctx.stroke();
        ctx.setLineDash([]);
      }
    }
    Array.prototype.forEach.call(document.querySelectorAll("#ragPipe li"), function (item) {
      var step = Number(item.dataset.step);
      item.classList.toggle("is-now", step === ragStep);
      item.classList.toggle("is-done", step < ragStep);
    });
    hits.replaceChildren();
    if (ragStep >= 2) {
      ranked.slice(0, 3).forEach(function (hit) {
        var card = document.createElement("article");
        card.className = "hit-card" + (hit.accept && hit === ranked[0] ? " is-pick" : "");
        var title = document.createElement("strong");
        title.textContent = hit.score.toFixed(2) + " · " + hit.id;
        var body = document.createElement("p");
        body.textContent = hit.text;
        card.appendChild(title);
        card.appendChild(body);
        hits.appendChild(card);
      });
    } else if (ragStep === 0) {
      math.chunks().forEach(function (chunk) {
        var card = document.createElement("article");
        card.className = "hit-card";
        var title = document.createElement("strong");
        title.textContent = chunk.id;
        var body = document.createElement("p");
        body.textContent = chunk.text;
        card.appendChild(title);
        card.appendChild(body);
        hits.appendChild(card);
      });
    }
    var best = ranked[0];
    if (ragStep < 3) {
      answer.textContent = ["Notes split into passages.", "Each passage is a toy vector. Shared words pull points together.", "The query is the amber point. A hit needs a shared word and a high cosine.", ""][ragStep];
    } else if (best && best.accept) {
      answer.textContent = best.text + " Source: " + best.id + ".";
    } else {
      answer.textContent = "Refuse. No passage shares the question and clears the similarity bar.";
    }
  }

  function drawAgent() {
    var goal = document.getElementById("agentGoal");
    var list = document.getElementById("agentTrace");
    if (!goal || !math) return;
    agentFrames = math.planAgent(goal.value);
    if (agentStep >= agentFrames.length) agentStep = agentFrames.length - 1;
    list.replaceChildren();
    agentFrames.slice(0, agentStep + 1).forEach(function (frame) {
      var item = document.createElement("li");
      if (frame.kind === "gate") item.classList.add("is-gate");
      var title = document.createElement("b");
      title.textContent = frame.title;
      var body = document.createElement("p");
      body.textContent = frame.text;
      item.appendChild(title);
      item.appendChild(body);
      if (frame.envelope) {
        var pre = document.createElement("pre");
        var code = document.createElement("code");
        code.textContent = JSON.stringify(frame.envelope, null, 2);
        pre.appendChild(code);
        item.appendChild(pre);
      }
      list.appendChild(item);
    });
  }

  function bindRange(id, outId, draw) {
    var input = document.getElementById(id);
    var out = document.getElementById(outId);
    if (!input) return;
    function sync() { if (out) out.textContent = input.value; if (draw) draw(); }
    input.addEventListener("input", sync);
    sync();
  }

  function drawEval() {
    if (!math) return;
    var input = {
      quality: Number(document.getElementById("evQual").value),
      qualityBase: Number(document.getElementById("evQualBase").value),
      safety: Number(document.getElementById("evSafe").value),
      safetyBase: Number(document.getElementById("evSafeBase").value),
      latency: Number(document.getElementById("evLat").value),
      latencyBudget: Number(document.getElementById("evLatBudget").value),
      cost: Number(document.getElementById("evCost").value),
      costBudget: Number(document.getElementById("evCostBudget").value)
    };
    var result = math.gate(input);
    var verdict = document.getElementById("evVerdict");
    verdict.classList.toggle("is-pass", result.pass);
    verdict.classList.toggle("is-stop", !result.pass);
    verdict.textContent = result.pass ? "Ship. Quality held, safety did not get worse, and latency and cost stayed inside budget." : "Stop. " + result.reasons.join(" ");
    document.getElementById("meterQual").style.width = input.quality + "%";
    document.getElementById("meterSafe").style.width = (100 - input.safety * 16) + "%";
    document.getElementById("meterLat").style.width = Math.min(100, (input.latency / 2000) * 100) + "%";
    document.getElementById("meterCost").style.width = (input.cost / 12) * 100 + "%";
  }

  function drawLora() {
    var canvas = document.getElementById("loraCanvas");
    var slider = document.getElementById("loraRank");
    var read = document.getElementById("loraRead");
    if (!canvas || !math) return;
    var model = math.lora(Number(slider.value));
    var view = fitCanvas(canvas);
    var ctx = view.ctx;
    var colors = ink();
    ctx.clearRect(0, 0, view.w, view.h);
    var rows = 8;
    var rank = model.rank;
    var cell = 14;
    ctx.fillStyle = colors.muted;
    ctx.font = "13px system-ui, sans-serif";
    ctx.fillText("A  " + model.width + " × " + rank, 16, 22);
    ctx.fillText("B  " + rank + " × " + model.width, view.w * 0.48, 22);
    for (var r = 0; r < rows; r += 1) {
      for (var c = 0; c < Math.min(rank, 18); c += 1) {
        ctx.fillStyle = colors.primary;
        ctx.globalAlpha = 0.35 + ((r + c) % 5) / 8;
        ctx.fillRect(16 + c * (cell + 2), 36 + r * (cell + 2), cell, cell);
      }
    }
    var bCols = 12;
    for (var br = 0; br < Math.min(rank, 10); br += 1) {
      for (var bc = 0; bc < bCols; bc += 1) {
        ctx.fillStyle = colors.cyan;
        ctx.globalAlpha = 0.3 + ((br * 3 + bc) % 6) / 10;
        ctx.fillRect(view.w * 0.48 + bc * (cell + 2), 36 + br * (cell + 2), cell, cell);
      }
    }
    ctx.globalAlpha = 1;
    var percent = Math.round(model.share * 1000) / 10;
    read.textContent = "Rank " + model.rank + " trains " + model.trainable.toLocaleString() + " numbers instead of " + model.full.toLocaleString() + " in this toy layer. That is " + percent + "% of the full matrix.";
    canvas.setAttribute("aria-label", read.textContent);
  }

  var bpeMerges = [
    ["t", "h"], ["i", "n"], ["e", "r"], ["o", "n"], ["a", "n"], ["r", "e"],
    ["th", "e"], ["in", "g"], ["e", "d"], ["a", "t"], ["s", "t"],
    [" ", "t"], [" ", "a"], [" ", "the"], ["t", "ion"], ["a", "nd"], ["n", "ext"]
  ];

  function bpeEncode(text) {
    var symbols = Array.prototype.map.call(new TextEncoder().encode(text), function (byte) {
      return { text: String.fromCharCode(byte), bytes: [byte] };
    });
    bpeMerges.forEach(function (pair) {
      var next = [];
      for (var i = 0; i < symbols.length; i += 1) {
        if (i < symbols.length - 1 && symbols[i].text === pair[0] && symbols[i + 1].text === pair[1]) {
          next.push({
            text: pair[0] + pair[1],
            bytes: symbols[i].bytes.concat(symbols[i + 1].bytes)
          });
          i += 1;
        } else {
          next.push(symbols[i]);
        }
      }
      symbols = next;
    });
    return symbols;
  }

  function drawBpe() {
    var input = document.getElementById("bpeIn");
    var row = document.getElementById("bpeTokens");
    var read = document.getElementById("bpeRead");
    var bytes = document.getElementById("bpeBytes");
    if (!input || !row) return;
    var tokens = bpeEncode(input.value || "");
    row.replaceChildren();
    tokens.forEach(function (token, index) {
      var chip = document.createElement("button");
      chip.type = "button";
      chip.className = "token is-on";
      var id = token.bytes.length === 1 ? token.bytes[0] : 256 + index;
      chip.textContent = JSON.stringify(token.text) + " #" + id;
      chip.addEventListener("click", function () {
        if (read) read.textContent = "Token " + JSON.stringify(token.text) + " is bytes " + token.bytes.join(", ") + ".";
      });
      row.appendChild(chip);
    });
    var raw = Array.prototype.map.call(new TextEncoder().encode(input.value || ""), function (byte) {
      return byte.toString(16).padStart(2, "0");
    }).join(" ");
    if (bytes) bytes.textContent = raw || "(empty)";
    if (read) {
      read.textContent = tokens.length + " tokens from " + (input.value || "").length + " characters. Click a token to read its bytes. Ids under 256 are raw bytes. Later ids are this lab's merges, not a vendor vocab.";
    }
  }

  function watchSpace(host, kind) {
    if (!host || host.dataset.spaceWatch === "1") return;
    host.dataset.spaceWatch = "1";
    function start() { bootSpace(kind); }
    if (typeof IntersectionObserver !== "function") {
      start();
      return;
    }
    var observer = new IntersectionObserver(function (entries) {
      for (var i = 0; i < entries.length; i += 1) {
        if (!entries[i].isIntersecting) continue;
        observer.disconnect();
        start();
        return;
      }
    });
    observer.observe(host);
  }

  function bindSpaceOpen() {
    var button = document.getElementById("openSpace");
    if (!button || button.dataset.bound) return;
    button.dataset.bound = "1";
    button.addEventListener("click", function () {
      var host = document.getElementById("heroMount");
      if (!host) return;
      host.hidden = false;
      button.hidden = true;
      window.requestAnimationFrame(function () { watchSpace(host, "topology"); });
    });
  }

  function bootSpace(kind) {
    if (!window.CampusSpacePromise) {
      window.CampusSpacePromise = import("./assets/js/space.js").then(function (mod) {
        window.CampusSpace = mod;
        return mod;
      }).catch(function () { return null; });
    }
    window.CampusSpacePromise.then(function (mod) {
      if (!mod) return;
      if (kind === "topology") {
        var hero = document.getElementById("heroMount");
        if (hero) mod.mountTopology(hero);
      }
      if (kind === "embed") {
        var mount = document.getElementById("embedMount");
        if (mount) {
          mod.mountEmbed(mount);
          if (window.LabExtra) window.LabExtra.onTab("embed");
        }
      }
    });
  }

  function bootPlay() {
    var root = document.getElementById("play");
    if (!root || !math) return;
    if (root.dataset.bound) {
      selectTab(tabFromHash());
      return;
    }
    root.dataset.bound = "1";
    playReady = true;
    bootTabs();
    var text = document.getElementById("pgText");
    var slider = document.getElementById("pgQuery");
    if (text) text.addEventListener("input", drawAttention);
    if (slider) slider.addEventListener("input", drawAttention);
    var bpeIn = document.getElementById("bpeIn");
    var bpeGo = document.getElementById("bpeGo");
    if (bpeIn) bpeIn.addEventListener("input", drawBpe);
    if (bpeGo) bpeGo.addEventListener("click", drawBpe);
    drawBpe();
    var ragQuestion = document.getElementById("ragQuestion");
    if (ragQuestion) ragQuestion.addEventListener("input", function () { ragStep = 0; drawRag(); });
    Array.prototype.forEach.call(document.querySelectorAll(".rag-preset"), function (button) {
      button.addEventListener("click", function () {
        ragQuestion.value = button.dataset.q;
        ragStep = 0;
        drawRag();
      });
    });
    document.getElementById("ragPrev").addEventListener("click", function () { ragStep = Math.max(0, ragStep - 1); drawRag(); });
    document.getElementById("ragNext").addEventListener("click", function () { ragStep = Math.min(3, ragStep + 1); drawRag(); });
    document.getElementById("ragPlay").addEventListener("click", function () {
      window.clearInterval(ragTimer);
      ragStep = 0;
      drawRag();
      if (reduceMotion()) { ragStep = 3; drawRag(); return; }
      ragTimer = window.setInterval(function () {
        if (ragStep >= 3) { window.clearInterval(ragTimer); return; }
        ragStep += 1;
        drawRag();
      }, 700);
    });
    var agentGoal = document.getElementById("agentGoal");
    if (agentGoal) agentGoal.addEventListener("input", function () { agentStep = 0; drawAgent(); });
    Array.prototype.forEach.call(document.querySelectorAll(".agent-preset"), function (button) {
      button.addEventListener("click", function () {
        agentGoal.value = button.dataset.q;
        agentStep = 0;
        drawAgent();
      });
    });
    document.getElementById("agentPrev").addEventListener("click", function () { agentStep = Math.max(0, agentStep - 1); drawAgent(); });
    document.getElementById("agentNext").addEventListener("click", function () {
      agentFrames = math.planAgent(agentGoal.value);
      agentStep = Math.min(agentFrames.length - 1, agentStep + 1);
      drawAgent();
    });
    document.getElementById("agentRun").addEventListener("click", function () {
      agentFrames = math.planAgent(agentGoal.value);
      agentStep = agentFrames.length - 1;
      drawAgent();
    });
    ["evQual", "evQualBase", "evSafe", "evSafeBase", "evLat", "evLatBudget", "evCost", "evCostBudget"].forEach(function (id) {
      bindRange(id, id + "Out", drawEval);
    });
    bindRange("loraRank", "loraOut", drawLora);
    if (window.LabExtra) window.LabExtra.boot();
    selectTab(tabFromHash());
  }

  var cardIndex = 0;
  var cardKnown = {};
  var cardCache = null;
  var cardLoading = null;

  function cardList() {
    return cardCache || [];
  }

  function loadCards() {
    if (cardCache) return Promise.resolve(cardCache);
    if (cardLoading) return cardLoading;
    var node = document.getElementById("flashData");
    if (node && (node.textContent || "").trim()) {
      try { cardCache = JSON.parse(node.textContent); } catch (err) { cardCache = []; }
      return Promise.resolve(cardCache);
    }
    cardLoading = fetch("assets/curriculum/cards.json").then(function (res) {
      if (!res.ok) throw new Error("cards");
      return res.json();
    }).then(function (data) {
      cardCache = data.cards || [];
      return cardCache;
    }).catch(function () {
      cardLoading = null;
      cardCache = [];
      return cardCache;
    });
    return cardLoading;
  }

  function paintCard() {
    var cards = cardList();
    var front = document.getElementById("cardFront");
    var back = document.getElementById("cardBack");
    var meta = document.getElementById("cardMeta");
    if (!front) return;
    if (!cards.length) {
      if (meta) meta.textContent = "Loading the deck.";
      loadCards().then(function (rows) {
        if (!rows.length && meta) meta.textContent = "The deck did not load.";
        else paintCard();
      });
      return;
    }
    if (cardIndex >= cards.length) cardIndex = 0;
    if (cardIndex < 0) cardIndex = cards.length - 1;
    var card = cards[cardIndex];
    var knownCount = Object.keys(cardKnown).filter(function (id) { return cardKnown[id] === "known"; }).length;
    front.innerHTML = "<small></small><p></p>";
    back.innerHTML = "<small>Answer</small><p></p><p class=\"quiz-cite\"></p>";
    front.querySelector("small").textContent = card.title + " · " + (cardIndex + 1) + " of " + cards.length;
    front.querySelector("p").textContent = card.q;
    back.querySelector("p").textContent = card.a;
    var cite = back.querySelector(".quiz-cite");
    if (card.cite && card.cite.url) {
      cite.textContent = "Source: " + card.cite.title;
    } else {
      cite.textContent = "";
    }
    meta.textContent = knownCount + " marked known in this browser. " + cards.length + " cards in the practice bank.";
    var flip = document.getElementById("cardFlip");
    var button = document.getElementById("cardFlipBtn");
    flip.classList.remove("is-flipped");
    button.setAttribute("aria-pressed", "false");
  }

  function bootCards() {
    try { cardKnown = JSON.parse(localStorage.getItem("ailab-v3-cards") || "{}"); } catch (err) { cardKnown = {}; }
    var button = document.getElementById("cardFlipBtn");
    if (!button) return;
    if (button.dataset.bound === "1") {
      paintCard();
      return;
    }
    button.dataset.bound = "1";
    button.addEventListener("click", function () {
      var flip = document.getElementById("cardFlip");
      var on = flip.classList.toggle("is-flipped");
      button.setAttribute("aria-pressed", on ? "true" : "false");
    });
    button.addEventListener("keydown", function (event) {
      if (event.key !== " ") return;
      event.preventDefault();
      button.click();
    });
    document.getElementById("cardPrev").addEventListener("click", function () { cardIndex -= 1; paintCard(); });
    document.getElementById("cardNext").addEventListener("click", function () { cardIndex += 1; paintCard(); });
    function mark(state) {
      var cards = cardList();
      var card = cards[cardIndex];
      if (!card) return;
      cardKnown[card.id] = state;
      try { localStorage.setItem("ailab-v3-cards", JSON.stringify(cardKnown)); } catch (err) { /* ignore */ }
      cardIndex += 1;
      paintCard();
    }
    document.getElementById("cardKnew").addEventListener("click", function () { mark("known"); });
    document.getElementById("cardAgain").addEventListener("click", function () { mark("again"); });
    loadCards().then(function () { paintCard(); });
  }

  var resizeTimer = 0;
  window.addEventListener("resize", function () {
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(function () {
      if (document.body.dataset.view !== "play") return;
      var current = tabFromHash();
      if (current === "attn") drawAttention();
      if (current === "rag") drawRag();
      if (current === "lora") drawLora();
      if (window.LabExtra) window.LabExtra.onTab(current);
    }, 120);
  });

  function onShow(route) {
    mirrorDash();
    if (!route) return;
    if (route.view === "home") {
      animateCounts();
      bindSpaceOpen();
    }
    if (route.view === "play") {
      bootPlay();
      var name = (route.id || "play").indexOf("play-") === 0 ? route.id.slice(5) : tabFromHash();
      selectTab(name);
    }
  }

  document.addEventListener("campus-progress", function () {
    mirrorDash();
    var pressed = document.querySelector("[data-track-filter][aria-pressed='true']");
    applyTrackFilter(pressed ? pressed.getAttribute("data-track-filter") : "all");
  });
  document.addEventListener("campus-show", function (event) { onShow(event.detail); });
  document.addEventListener("campus-progress", mirrorDash);

  function readPref(key, fallback) {
    try {
      var value = localStorage.getItem(key);
      return value == null ? fallback : value;
    } catch (err) { return fallback; }
  }
  function writePref(key, value) {
    try { localStorage.setItem(key, value); } catch (err) { /* ignore */ }
  }
  var tickCtx = null;
  function playCue(kind) {
    if (readPref("ailab-v3-sound", "off") !== "on") return;
    var Ctx = window.AudioContext || window.webkitAudioContext;
    if (!Ctx) return;
    if (!tickCtx) {
      try { tickCtx = new Ctx(); } catch (err) { return; }
    }
    var osc = tickCtx.createOscillator();
    var gain = tickCtx.createGain();
    osc.type = "sine";
    osc.frequency.value = kind === "no" ? 220 : 660;
    var now = tickCtx.currentTime;
    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.exponentialRampToValueAtTime(0.04, now + 0.01);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.09);
    osc.connect(gain);
    gain.connect(tickCtx.destination);
    osc.start(now);
    osc.stop(now + 0.1);
  }
  function voiceScore(voice) {
    var low = (voice.name || "").toLowerCase();
    var lang = (voice.lang || "").toLowerCase();
    var score = 0;
    if (lang.indexOf("en") === 0) score += 50;
    else score -= 40;
    if (/natural|neural|premium|enhanced/.test(low)) score += 40;
    if (/samantha|daniel|moira|karen|serena|allison|ava|nicky|aaron|nathan/.test(low)) score += 24;
    if (low.indexOf("google") !== -1 && low.indexOf("english") !== -1) score += 8;
    if (/microsoft (david|zira|mark|hazel|george|susan|heera|ravi)/.test(low)) score -= 80;
    if (low.indexOf("microsoft") !== -1 && !/natural|neural/.test(low)) score -= 60;
    if (/espeak|android/.test(low)) score -= 40;
    return score;
  }
  function chosenVoice(voices) {
    var saved = readPref("ailab-v3-voice", "");
    if (saved) {
      for (var i = 0; i < voices.length; i += 1) if (voices[i].voiceURI === saved) return voices[i];
    }
    var best = null;
    var bestScore = 19;
    voices.forEach(function (voice) {
      var score = voiceScore(voice);
      if (score > bestScore) { best = voice; bestScore = score; }
    });
    return best;
  }
  window.CampusSettings = {
    play: playCue,
    narrationOn: function () { return readPref("ailab-v3-narration", "on") !== "off"; },
    voice: function () { return chosenVoice(window.speechSynthesis ? window.speechSynthesis.getVoices() : []); },
    rate: function () { return Number(readPref("ailab-v3-rate", "1")) || 1; },
    motionReduced: reduceMotion
  };
  var prefsPromise = null;
  function loadPrefs() {
    if (!prefsPromise) prefsPromise = import("./assets/js/prefs.js");
    return prefsPromise;
  }
  var settingsBtn = document.getElementById("settingsBtn");
  var tipsBtn = document.getElementById("tipsBtn");
  if (settingsBtn) settingsBtn.addEventListener("click", function () {
    loadPrefs().then(function (mod) { mod.openSettings(); });
  });
  if (tipsBtn) tipsBtn.addEventListener("click", function () {
    loadPrefs().then(function (mod) { mod.openTips(); });
  });
  bootTilt();
  mirrorDash();
  var hash = (location.hash || "#home").replace(/^#/, "");
  var initial = { view: "home" };
  if (hash === "map" || hash === "studio" || hash === "builds") initial = { view: hash };
  else if (hash === "play" || hash.indexOf("play-") === 0) initial = { view: "play", id: hash };
  else if (hash.indexOf("school-") === 0) initial = { view: "school", id: hash };
  else if (window.CampusCatalog && window.CampusCatalog.order.indexOf(hash) !== -1) initial = { view: "lesson", id: hash };
  onShow(initial);
  if (window.campusBoot) window.campusBoot();
})();
