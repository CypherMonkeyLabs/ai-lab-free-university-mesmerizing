/* Phone menu, quick bar, reveal, and hero parallax. */
import { openSettings } from "./prefs.js";

function motionOff() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches
    || document.documentElement.getAttribute("data-motion") === "reduce";
}

function currentHash() {
  var hash = location.hash || "#home";
  return hash === "#" ? "#home" : hash;
}

function schoolHash() {
  var id = currentHash().slice(1);
  var catalog = window.CampusCatalog;
  if (!catalog || !catalog.lessons) return "";
  for (var i = 0; i < catalog.lessons.length; i += 1) {
    if (catalog.lessons[i].id === id) return "#school-" + catalog.lessons[i].school;
  }
  return "";
}

function paintCurrent() {
  var hash = currentHash();
  var school = schoolHash();
  document.querySelectorAll(".menu-item, .phone-sections a").forEach(function (link) {
    var href = link.getAttribute("href");
    var on = href === hash || (school && href === school);
    if (href === "#play" && (hash === "#play" || hash.indexOf("#play-") === 0)) on = true;
    if (href === "#downloads" && (hash === "#downloads" || hash === "#cheats")) on = true;
    if (on) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  });
  document.querySelectorAll(".quickbar a[data-quick]").forEach(function (link) {
    var key = link.getAttribute("data-quick");
    var on = (key === "home" && hash === "#home")
      || (key === "atlas" && hash === "#atlas")
      || (key === "flows" && hash === "#flows")
      || (key === "downloads" && (hash === "#downloads" || hash === "#cheats"))
      || (key === "play" && (hash === "#play" || hash.indexOf("#play-") === 0));
    if (on) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  });
}

function fillTracks() {
  var nav = document.getElementById("phoneTracks");
  var catalog = window.CampusCatalog;
  if (!nav || nav.dataset.filled === "1" || !catalog || !catalog.schools) return;
  nav.dataset.filled = "1";
  catalog.schools.forEach(function (school) {
    if (school.kind && school.kind !== "track" && school.id !== "EX") return;
    var link = document.createElement("a");
    link.href = "#school-" + school.id;
    link.className = "menu-item";
    link.setAttribute("data-section", link.href);
    link.setAttribute("data-menu-item", "");
    link.setAttribute("data-search", (school.name || "") + " " + (school.outcome || ""));
    var label = document.createElement("span");
    label.className = "menu-label";
    label.textContent = school.name || school.id;
    var desc = document.createElement("span");
    desc.className = "menu-desc";
    desc.textContent = school.outcome || "Open this track.";
    var copy = document.createElement("span");
    copy.className = "menu-copy";
    copy.appendChild(label);
    copy.appendChild(desc);
    link.appendChild(copy);
    nav.appendChild(link);
  });
}

function bindSheet() {
  var sheet = document.getElementById("phoneSheet");
  var openBtn = document.getElementById("phoneMenuBtn");
  var quickBtn = document.getElementById("quickMenu");
  var closeBtn = document.getElementById("phoneClose");
  if (!sheet || !openBtn || sheet.dataset.bound === "1") return;
  sheet.dataset.bound = "1";
  var historyMark = false;
  var opener = openBtn;

  function hide(fromPop) {
    sheet.hidden = true;
    document.body.classList.remove("sheet-open");
    openBtn.setAttribute("aria-expanded", "false");
    var settings = document.getElementById("settingsDrawer");
    if (settings && settings.open) settings.close();
    if (historyMark && !fromPop) {
      historyMark = false;
      history.back();
    } else {
      historyMark = false;
    }
    if (opener && typeof opener.focus === "function") opener.focus();
  }

  function show(button) {
    if (!sheet.hidden) return;
    opener = button || openBtn;
    fillTracks();
    paintCurrent();
    sheet.hidden = false;
    document.body.classList.add("sheet-open");
    openBtn.setAttribute("aria-expanded", "true");
    historyMark = true;
    history.pushState({ phoneSheet: 1 }, "");
    if (closeBtn) closeBtn.focus();
  }

  openBtn.addEventListener("click", function () { show(openBtn); });
  if (quickBtn) quickBtn.addEventListener("click", function () { show(quickBtn); });
  if (closeBtn) closeBtn.addEventListener("click", function () { hide(false); });
  sheet.addEventListener("click", function (event) {
    var link = event.target.closest("a[href^='#']");
    if (!link || !sheet.contains(link)) return;
    event.preventDefault();
    var href = link.getAttribute("href");
    historyMark = false;
    sheet.hidden = true;
    document.body.classList.remove("sheet-open");
    openBtn.setAttribute("aria-expanded", "false");
    history.replaceState({}, "");
    if (location.hash === href) paintCurrent();
    else location.hash = href;
  });
  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape" || sheet.hidden) return;
    var settings = document.getElementById("settingsDrawer");
    if (settings && settings.open) return;
    event.preventDefault();
    hide(false);
  });
  window.addEventListener("popstate", function () {
    if (!sheet.hidden && historyMark) hide(true);
  });
  document.querySelectorAll("[data-open-settings]").forEach(function (button) {
    if (button.dataset.bound === "1") return;
    button.dataset.bound = "1";
    button.addEventListener("click", function () { openSettings(); });
  });
  var listen = document.getElementById("quickListen");
  if (listen) {
    listen.addEventListener("click", function (event) {
      event.preventDefault();
      function scrollAudio() {
        var node = document.getElementById("architectAudio");
        if (!node) return;
        node.scrollIntoView({ behavior: motionOff() ? "auto" : "smooth", block: "start" });
      }
      if (currentHash() === "#home") {
        scrollAudio();
        return;
      }
      document.addEventListener("campus-show", function onShow() {
        document.removeEventListener("campus-show", onShow);
        window.setTimeout(scrollAudio, 40);
      });
      location.hash = "#home";
    });
  }
  window.addEventListener("hashchange", paintCurrent);
  document.addEventListener("campus-show", paintCurrent);
}

function bindCourseMenu() {
  var panel = document.getElementById("courseMenu");
  var button = document.getElementById("courseMenuBtn");
  var closeBtn = document.getElementById("courseMenuClose");
  if (!panel || !button || panel.dataset.bound === "1") return;
  panel.dataset.bound = "1";
  function hide() {
    panel.hidden = true;
    button.setAttribute("aria-expanded", "false");
  }
  button.addEventListener("click", function () {
    var open = panel.hidden;
    panel.hidden = !open;
    button.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) {
      var input = document.getElementById("courseSearch");
      if (input) input.focus();
    }
  });
  if (closeBtn) closeBtn.addEventListener("click", hide);
  panel.addEventListener("click", function (event) {
    if (event.target.closest("a[href^='#']")) hide();
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !panel.hidden) hide();
  });
}

function bindMenuSearch(input) {
  if (!input || input.dataset.bound === "1") return;
  input.dataset.bound = "1";
  input.addEventListener("input", function () {
    var query = input.value.trim().toLowerCase();
    var root = input.closest(".course-panel, .phone-sheet, .side-menu-wrap") || document;
    var items = root.querySelectorAll("[data-menu-item]");
    if (root.classList && root.classList.contains("side-menu-wrap")) {
      items = root.querySelectorAll("[data-menu-item]");
    }
    items.forEach(function (item) {
      var hay = ((item.getAttribute("data-search") || "") + " " + item.textContent).toLowerCase();
      item.hidden = !!query && hay.indexOf(query) === -1;
    });
    if (input.id === "phoneSearch") {
      document.querySelectorAll("#phoneTracks a").forEach(function (item) {
        var hay = ((item.getAttribute("data-search") || "") + " " + item.textContent).toLowerCase();
        item.hidden = !!query && hay.indexOf(query) === -1;
      });
    }
  });
}

export function wirePhone() {
  bindSheet();
  bindCourseMenu();
  fillTracks();
  paintCurrent();
  bindMenuSearch(document.getElementById("courseSearch"));
  bindMenuSearch(document.getElementById("phoneSearch"));
  bindMenuSearch(document.getElementById("sideMenuSearch"));
  wireReveal();
  wireParallax();
}

function wireReveal() {
  var nodes = document.querySelectorAll(".block, .track-card, .parallax-row");
  if (motionOff()) {
    nodes.forEach(function (node) { node.classList.add("is-revealed"); });
    return;
  }
  if (!("IntersectionObserver" in window)) {
    nodes.forEach(function (node) { node.classList.add("is-revealed"); });
    return;
  }
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-revealed");
      observer.unobserve(entry.target);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
  nodes.forEach(function (node) {
    if (node.closest(".hero-stage") || node.dataset.revealBound === "1") return;
    node.dataset.revealBound = "1";
    node.classList.add("reveal");
    observer.observe(node);
  });
  document.addEventListener("campus-motion", function () {
    if (!motionOff()) return;
    nodes.forEach(function (node) {
      node.classList.add("is-revealed");
      node.classList.remove("reveal");
    });
    observer.disconnect();
  });
}

function wireParallax() {
  var copy = document.querySelector(".hero-copy");
  if (!copy || copy.dataset.parallaxBound === "1") return;
  copy.dataset.parallaxBound = "1";
  function paint() {
    if (motionOff()) {
      copy.style.transform = "";
      return;
    }
    var shift = Math.min(36, window.scrollY * 0.12);
    copy.style.transform = shift ? "translate3d(0," + shift.toFixed(1) + "px,0)" : "";
  }
  window.addEventListener("scroll", paint, { passive: true });
  document.addEventListener("campus-motion", paint);
  paint();
}
