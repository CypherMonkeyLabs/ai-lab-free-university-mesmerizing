/* Chrome for the AI omni-channel learning lab.
   Menu drawer, one-row banner arrows, display controls.
   The guide monkey mounts itself in #guide-mount. */
(function () {
  var root = document.documentElement;

  function applyTheme(name) {
    if (name !== "dark" && name !== "contrast") name = "bright";
    root.dataset.theme = name;
    try { localStorage.setItem("ai-theme", name); } catch (err) { /* storage off */ }
    document.querySelectorAll("[data-set-theme]").forEach(function (btn) {
      btn.setAttribute("aria-checked", btn.getAttribute("data-set-theme") === name ? "true" : "false");
    });
  }
  function applyFont(size) {
    if (["sm", "md", "lg", "xl"].indexOf(size) < 0) size = "md";
    root.dataset.font = size;
    try { localStorage.setItem("ai-font", size); } catch (err) { /* storage off */ }
    document.querySelectorAll("[data-font-set]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", btn.getAttribute("data-font-set") === size ? "true" : "false");
    });
  }
  function applyInk(color) {
    if (!/^#[0-9a-f]{6}$/i.test(color || "")) return;
    root.style.setProperty("--ink", color);
    try { localStorage.setItem("ai-ink", color); } catch (err) { /* storage off */ }
    document.querySelectorAll("[data-ink]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", btn.getAttribute("data-ink").toLowerCase() === color.toLowerCase() ? "true" : "false");
    });
  }
  function applyMotion(reduce) {
    root.dataset.motion = reduce ? "reduce" : "full";
    try { localStorage.setItem("ai-motion", reduce ? "reduce" : "full"); } catch (err) { /* storage off */ }
  }

  var menu = document.getElementById("edge-menu");
  var scrim = document.getElementById("edge-scrim");
  var menuBtn = document.getElementById("menu-btn");
  function setMenu(open) {
    if (!menu || !menuBtn) return;
    menu.classList.toggle("is-open", open);
    if (scrim) scrim.classList.toggle("is-open", open);
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.classList.toggle("edge-open", open);
    if (open) {
      var field = menu.querySelector(".edge-search");
      if (field) field.focus();
    }
  }
  if (menuBtn) menuBtn.addEventListener("click", function () { setMenu(!menu.classList.contains("is-open")); });
  document.querySelectorAll("[data-open-menu]").forEach(function (btn) {
    btn.addEventListener("click", function () { setMenu(true); });
  });
  if (scrim) scrim.addEventListener("click", function () { setMenu(false); menuBtn.focus(); });
  var closer = document.querySelector(".edge-close");
  if (closer) closer.addEventListener("click", function () { setMenu(false); menuBtn.focus(); });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && menu && menu.classList.contains("is-open")) {
      setMenu(false);
      menuBtn.focus();
    }
  });
  var search = menu && menu.querySelector(".edge-search");
  if (search) {
    search.addEventListener("input", function () {
      var q = search.value.trim().toLowerCase();
      menu.querySelectorAll(".edge-list a").forEach(function (link) {
        var hay = (link.textContent || "").toLowerCase();
        link.parentElement.hidden = q.length > 0 && hay.indexOf(q) < 0;
      });
    });
  }

  var displayBtn = document.getElementById("display-btn");
  var displayPanel = document.getElementById("display-panel");
  function setDisplay(open) {
    if (!displayBtn || !displayPanel) return;
    displayPanel.hidden = !open;
    displayBtn.setAttribute("aria-expanded", open ? "true" : "false");
  }
  if (displayBtn) {
    displayBtn.addEventListener("click", function (event) {
      event.stopPropagation();
      setDisplay(displayPanel.hidden);
    });
  }
  document.addEventListener("pointerdown", function (event) {
    if (!displayPanel || displayPanel.hidden) return;
    if (displayPanel.contains(event.target) || (displayBtn && displayBtn.contains(event.target))) return;
    setDisplay(false);
  });

  document.addEventListener("click", function (event) {
    var themeBtn = event.target.closest && event.target.closest("[data-set-theme]");
    if (themeBtn) applyTheme(themeBtn.getAttribute("data-set-theme"));
    var fontBtn = event.target.closest && event.target.closest("[data-font-set]");
    if (fontBtn) applyFont(fontBtn.getAttribute("data-font-set"));
    var inkBtn = event.target.closest && event.target.closest("[data-ink]");
    if (inkBtn) applyInk(inkBtn.getAttribute("data-ink"));
    var motionBtn = event.target.closest && event.target.closest("[data-motion-toggle]");
    if (motionBtn) {
      var next = root.dataset.motion !== "reduce";
      applyMotion(next);
      motionBtn.setAttribute("aria-pressed", next ? "true" : "false");
    }
  });
  var inkInput = document.querySelector("[data-ink-input]");
  if (inkInput) inkInput.addEventListener("input", function () { applyInk(inkInput.value); });

  document.querySelectorAll("[data-rail]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var rail = document.querySelector(".section-rail");
      if (!rail) return;
      var dir = Number(btn.getAttribute("data-rail")) || 1;
      rail.scrollBy({ left: dir * Math.max(160, rail.clientWidth * 0.6), behavior: root.dataset.motion === "reduce" ? "auto" : "smooth" });
    });
  });

  var savedTheme = "bright";
  var savedFont = "md";
  var savedInk = "";
  var savedMotion = "";
  try {
    savedTheme = localStorage.getItem("ai-theme") || "bright";
    savedFont = localStorage.getItem("ai-font") || "md";
    savedInk = localStorage.getItem("ai-ink") || "";
    savedMotion = localStorage.getItem("ai-motion") || "";
  } catch (err) { /* storage off */ }
  applyTheme(savedTheme);
  applyFont(savedFont);
  if (savedInk) applyInk(savedInk);
  applyMotion(savedMotion === "reduce");
  var motionBtn = document.querySelector("[data-motion-toggle]");
  if (motionBtn) motionBtn.setAttribute("aria-pressed", savedMotion === "reduce" ? "true" : "false");

  window.AiFrame = { setMenu: setMenu, applyTheme: applyTheme, applyFont: applyFont, applyInk: applyInk };
})();
