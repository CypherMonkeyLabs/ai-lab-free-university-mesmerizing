/* Particles, hero parallax, and a campus read-along bar.
   Motion stops when the page or the operating system asks for less motion. */
(function () {
  var root = document.documentElement;

  function reduced() {
    return root.dataset.motion === "reduce" || window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function mountParticles() {
    if (document.querySelector(".fx-field")) return;
    var canvas = document.createElement("canvas");
    canvas.className = "fx-field";
    canvas.setAttribute("aria-hidden", "true");
    document.body.prepend(canvas);
    var ctx = canvas.getContext("2d");
    if (!ctx) return;
    var dots = [];
    function size() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      var count = Math.min(42, Math.round(window.innerWidth / 36));
      dots = [];
      for (var i = 0; i < count; i += 1) {
        dots.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          r: 1.2 + Math.random() * 2.2,
          vx: -0.25 + Math.random() * 0.5,
          vy: -0.35 + Math.random() * 0.2,
          hue: [187, 262, 330, 45][i % 4]
        });
      }
    }
    size();
    window.addEventListener("resize", size);
    var frame = 0;
    function tick() {
      frame = window.requestAnimationFrame(tick);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      if (reduced() || document.hidden || root.dataset.theme === "contrast") return;
      dots.forEach(function (dot) {
        dot.x += dot.vx;
        dot.y += dot.vy;
        if (dot.x < 0) dot.x = canvas.width;
        if (dot.x > canvas.width) dot.x = 0;
        if (dot.y < 0) dot.y = canvas.height;
        if (dot.y > canvas.height) dot.y = 0;
        ctx.beginPath();
        ctx.fillStyle = "hsla(" + dot.hue + ", 90%, 70%, 0.55)";
        ctx.arc(dot.x, dot.y, dot.r, 0, Math.PI * 2);
        ctx.fill();
      });
    }
    tick();
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) window.cancelAnimationFrame(frame);
      else tick();
    });
  }

  function wireParallax() {
    var hero = document.querySelector(".hero");
    var illu = document.querySelector(".hero .illu");
    if (!hero || !illu || illu.dataset.parallax === "1") return;
    illu.dataset.parallax = "1";
    var px = 0.5;
    var py = 0.4;
    var sy = 0;
    function paint() {
      if (reduced() || window.innerWidth < 960) {
        illu.style.transform = "";
        hero.style.backgroundPosition = "";
        return;
      }
      var tiltX = (px - 0.5) * 10;
      var tiltY = (py - 0.5) * 8;
      var lift = Math.min(16, sy * 0.03);
      illu.style.transform = "perspective(900px) rotateY(" + (-8 + tiltX).toFixed(2) + "deg) rotateX(" + (5 - tiltY).toFixed(2) + "deg) translate3d(0," + (-lift).toFixed(1) + "px,0)";
      hero.style.backgroundPosition = (px * 12).toFixed(1) + "px " + (py * 8 - lift).toFixed(1) + "px";
    }
    window.addEventListener("pointermove", function (event) {
      px = event.clientX / Math.max(1, window.innerWidth);
      py = event.clientY / Math.max(1, window.innerHeight);
      paint();
    }, { passive: true });
    window.addEventListener("scroll", function () {
      sy = window.scrollY || 0;
      paint();
    }, { passive: true });
    paint();
  }

  function sentences(text) {
    return text.replace(/\s+/g, " ").trim().split(/(?<=[.!?])\s+/).filter(Boolean);
  }

  function mountCampusRead() {
    if (!document.body || !document.body.hasAttribute("data-view")) return;
    if (document.querySelector(".campus-read")) return;
    var bar = document.createElement("div");
    bar.className = "campus-read";
    bar.innerHTML = '<button type="button" data-campus-read>Read this section</button>' +
      '<button type="button" data-campus-stop>Stop</button>' +
      '<label>Voice <select data-campus-voice aria-label="Voice"></select></label>';
    document.body.appendChild(bar);
    var select = bar.querySelector("[data-campus-voice]");
    var chosen = "";
    try { chosen = localStorage.getItem("ailab-v3-voice") || ""; } catch (err) { chosen = ""; }
    function loadVoices() {
      var voices = window.speechSynthesis ? window.speechSynthesis.getVoices() : [];
      select.innerHTML = "";
      var auto = document.createElement("option");
      auto.value = "";
      auto.textContent = "Browser default";
      select.appendChild(auto);
      voices.forEach(function (voice) {
        var option = document.createElement("option");
        option.value = voice.voiceURI;
        option.textContent = voice.name;
        select.appendChild(option);
      });
      if (chosen) select.value = chosen;
    }
    if (window.speechSynthesis) {
      loadVoices();
      window.speechSynthesis.addEventListener("voiceschanged", loadVoices);
    } else loadVoices();
    select.addEventListener("change", function () {
      chosen = select.value;
      try { localStorage.setItem("ailab-v3-voice", chosen); } catch (err) { /* storage off */ }
    });
    var speaking = false;
    function clearGlow() {
      document.querySelectorAll(".is-reading").forEach(function (node) { node.classList.remove("is-reading"); });
    }
    function stop() {
      speaking = false;
      if (window.speechSynthesis) window.speechSynthesis.cancel();
      clearGlow();
    }
    function blocks() {
      var hash = (location.hash || "#home").replace(/^#/, "") || "home";
      var rootNode = document.getElementById(hash) || document.getElementById("content") || document.body;
      return Array.prototype.filter.call(rootNode.querySelectorAll("h1, h2, h3, p, li"), function (node) {
        var text = (node.innerText || "").trim();
        return text.length > 24 && node.getClientRects().length > 0 && !node.closest(".campus-read");
      }).slice(0, 16);
    }
    function say(text, done) {
      if (!window.speechSynthesis) { if (done) done(); return; }
      var utter = new SpeechSynthesisUtterance(text);
      var voices = window.speechSynthesis.getVoices();
      var voice = voices.filter(function (item) { return item.voiceURI === chosen; })[0];
      if (voice) utter.voice = voice;
      utter.onend = function () { if (done) done(); };
      utter.onerror = function () { if (done) done(); };
      window.speechSynthesis.speak(utter);
    }
    bar.querySelector("[data-campus-stop]").addEventListener("click", stop);
    bar.querySelector("[data-campus-read]").addEventListener("click", function () {
      stop();
      var nodes = blocks();
      if (!nodes.length) return;
      speaking = true;
      var index = 0;
      function pump() {
        if (!speaking || index >= nodes.length) { clearGlow(); return; }
        clearGlow();
        var node = nodes[index];
        node.classList.add("is-reading");
        node.scrollIntoView({ block: "center", behavior: reduced() ? "auto" : "smooth" });
        var parts = sentences(node.innerText || "");
        var part = 0;
        function next() {
          if (!speaking) return;
          if (part >= parts.length) { index += 1; pump(); return; }
          say(parts[part], function () { part += 1; next(); });
        }
        next();
      }
      pump();
    });
  }

  function boot() {
    mountParticles();
    wireParallax();
    mountCampusRead();
  }
  if (document.body) boot();
  else document.addEventListener("DOMContentLoaded", boot);
})();
