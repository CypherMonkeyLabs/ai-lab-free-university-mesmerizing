
(function () {
  const STUDY_KEY = "ailab-v3-studied";
  const THEME_KEY = "ailab-v3-theme";
  const LAST_KEY = "ailab-v3-last";
  const catalog = JSON.parse(document.getElementById("campusCatalog").textContent);
  window.CampusCatalog = catalog;
  const byMeta = Object.fromEntries(catalog.lessons.map((item) => [item.id, item]));
  const schoolById = Object.fromEntries(catalog.schools.map((item) => [item.id, item]));
  const order = catalog.order.slice();
  let studied = new Set();
  try { JSON.parse(localStorage.getItem(STUDY_KEY) || "[]").forEach((id) => studied.add(id)); } catch (err) { studied = new Set(); }

  const menuBtn = document.getElementById("menuBtn");
  const scrim = document.getElementById("scrim");
  const search = document.getElementById("q");
  const themeBtn = document.getElementById("themeBtn");
  const markBtn = document.getElementById("markBtn");
  const crumb = document.getElementById("crumb");
  const ring = document.getElementById("ringValue");
  const studiedLabel = document.getElementById("studiedLabel");
  const homeProg = document.getElementById("homeProg");
  const homeBar = document.getElementById("homeBar");
  const continueLink = document.getElementById("continueLink");
  const continueCard = document.getElementById("continueCard");
  const continueTitle = document.getElementById("continueTitle");
  const continueMeta = document.getElementById("continueMeta");
  const pager = document.getElementById("pager");
  const pagerPrev = document.getElementById("pagerPrev");
  const pagerNext = document.getElementById("pagerNext");

  function closeNav() {
    document.body.classList.remove("nav-open");
    menuBtn.setAttribute("aria-expanded", "false");
  }
  menuBtn.addEventListener("click", () => {
    const open = document.body.classList.toggle("nav-open");
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
  });
  scrim.addEventListener("click", closeNav);

  function applyTheme(theme) {
    const allowed = { dark: true, light: true, contrast: true, dusk: true, futuristic: true, gaming: true, neon: true, holographic: true, cyberpunk: true, sunset: true };
    if (!allowed[theme]) theme = "neon";
    document.documentElement.setAttribute("data-theme", theme);
    document.dispatchEvent(new CustomEvent("campus-theme", { detail: theme }));
    const high = theme === "contrast";
    document.documentElement.setAttribute("data-contrast", high ? "high" : "normal");
    localStorage.setItem(THEME_KEY, theme);
    localStorage.setItem("ailab-v3-contrast", high ? "high" : "normal");
    themeBtn.setAttribute("aria-pressed", theme === "light" ? "false" : "true");
    themeBtn.setAttribute("aria-label", "Theme is " + theme + ". Activate to cycle themes.");
    document.querySelectorAll('input[name="setTheme"]').forEach((input) => {
      input.checked = input.value === theme;
    });
    const contrastBtn = document.getElementById("contrastBtn");
    if (contrastBtn) {
      contrastBtn.setAttribute("aria-pressed", high ? "true" : "false");
      contrastBtn.setAttribute("aria-label", high ? "HC, turn off high contrast" : "HC, turn on high contrast");
    }
  }
  window.CampusTheme = applyTheme;
  themeBtn.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme");
    applyTheme(current === "dark" ? "light" : "dark");
  });
  const contrastBtn = document.getElementById("contrastBtn");
  if (contrastBtn) {
    contrastBtn.addEventListener("click", () => {
      const current = document.documentElement.getAttribute("data-theme");
      if (current === "contrast") applyTheme(localStorage.getItem("ailab-v3-theme-prev") || "dark");
      else {
        if (current) localStorage.setItem("ailab-v3-theme-prev", current);
        applyTheme("contrast");
      }
    });
  }
  applyTheme(document.documentElement.getAttribute("data-theme") || "dark");

  function saveStudy() { localStorage.setItem(STUDY_KEY, JSON.stringify([...studied])); }
  function nextUnstudied() {
    const last = localStorage.getItem(LAST_KEY);
    if (last && byMeta[last] && !studied.has(last)) return last;
    return order.find((id) => !studied.has(id)) || order[order.length - 1];
  }
  function refreshProgress() {
    const done = order.filter((id) => studied.has(id)).length;
    const pct = Math.round((done / order.length) * 100);
    ring.setAttribute("stroke-dasharray", pct + " 100");
    studiedLabel.textContent = done + " of " + order.length + " complete";
    if (homeProg) homeProg.textContent = done + " of " + order.length + " lessons marked complete";
    if (homeBar) homeBar.style.width = pct + "%";
    document.querySelectorAll("a.ll").forEach((link) => {
      link.classList.toggle("done", studied.has(link.dataset.id));
    });
    const nid = nextUnstudied();
    const meta = byMeta[nid];
    if (continueTitle && meta) continueTitle.textContent = meta.title;
    if (continueMeta && meta) continueMeta.textContent = (schoolById[meta.school] ? schoolById[meta.school].name : "Track") + " · " + meta.minutes + " min";
    if (continueLink) continueLink.setAttribute("href", "#" + nid);
    if (continueCard) continueCard.setAttribute("href", "#" + nid);
    if (continueLink) continueLink.textContent = done === 0 ? "Start the course" : (done === order.length ? "Review the course" : "Continue");
    if (document.body.dataset.view === "lesson") updateMark(location.hash.slice(1));
    document.dispatchEvent(new CustomEvent("campus-progress"));
  }
  function updateMark(id) {
    const on = studied.has(id);
    markBtn.classList.toggle("done", on);
    markBtn.textContent = on ? "Completed" : "Mark complete";
    markBtn.dataset.id = id;
  }
  markBtn.addEventListener("click", () => {
    const id = markBtn.dataset.id;
    if (!id) return;
    if (studied.has(id)) studied.delete(id); else studied.add(id);
    saveStudy();
    if (window.CampusSettings) window.CampusSettings.play(studied.has(id) ? "ok" : "no");
    refreshProgress();
    document.dispatchEvent(new CustomEvent("campus-marked", { detail: { id, on: studied.has(id) } }));
  });

  let navPackPromise = null;
  function navPack() {
    if (!navPackPromise) navPackPromise = loadJSON("assets/curriculum/nav.json");
    return navPackPromise;
  }
  function fillSchool(schoolId) {
    const block = document.querySelector('.school-block[data-school="' + schoolId + '"]');
    if (!block || block.dataset.filled === "1") return Promise.resolve();
    return navPack().then((pack) => {
      if (block.dataset.filled === "1") return;
      const host = block.querySelector(".lesson-links");
      host.innerHTML = (pack.schools || {})[schoolId] || "";
      block.dataset.filled = "1";
      host.querySelectorAll("a.ll").forEach((link) => {
        link.classList.toggle("done", studied.has(link.dataset.id));
      });
    });
  }
  function fillNav() {
    return navPack().then((pack) => Promise.all(Object.keys(pack.schools || {}).map((id) => fillSchool(id))));
  }
  function setOpenSchool(schoolId) {
    document.querySelectorAll(".school-block").forEach((block) => {
      const open = block.dataset.school === schoolId;
      block.classList.toggle("open", open);
      const chev = block.querySelector(".chev");
      chev.setAttribute("aria-expanded", open ? "true" : "false");
    });
    if (schoolId) fillSchool(schoolId);
  }
  document.querySelectorAll(".chev").forEach((button) => {
    button.addEventListener("click", () => {
      const block = button.closest(".school-block");
      const open = !block.classList.contains("open");
      block.classList.toggle("open", open);
      button.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) fillSchool(block.dataset.school);
    });
  });

  function pagerLink(anchor, id, label) {
    if (!id || !byMeta[id]) {
      anchor.hidden = true;
      return;
    }
    anchor.hidden = false;
    anchor.href = "#" + id;
    anchor.innerHTML = "<small>" + label + "</small><span></span>";
    anchor.querySelector("span").textContent = byMeta[id].title;
  }
  function showLessonChrome(id) {
    const index = order.indexOf(id);
    pagerLink(pagerPrev, order[index - 1], "Previous");
    pagerLink(pagerNext, order[index + 1], "Next");
    updateMark(id);
    localStorage.setItem(LAST_KEY, id);
  }

  function parseHash() {
    const raw = (location.hash || "#home").replace(/^#/, "");
    if (!raw || raw === "home") return { view: "home" };
    if (raw === "map") return { view: "map" };
    if (raw === "studio") return { view: "studio" };
    if (raw === "builds") return { view: "builds" };
    if (raw === "cheats") return { view: "downloads" };
    if (raw === "downloads" || raw === "arcade" || raw === "atlas" || raw === "flows" || raw === "charts" || raw === "regions") return { view: raw };
    if (raw === "play" || raw.startsWith("play-")) return { view: "play", id: raw };
    if (raw.startsWith("school-")) return { view: "school", id: raw };
    if (byMeta[raw]) return { view: "lesson", id: raw };
    return { view: "missing" };
  }

  const modules = new Map();
  let homeHTML = "";
  let showGen = 0;

  function stage() { return document.getElementById("stage"); }
  function mounted(id) {
    const node = document.getElementById(id);
    return node && stage().contains(node) ? node : null;
  }
  function rememberHome() {
    const home = document.getElementById("home");
    if (home && !homeHTML) homeHTML = home.outerHTML;
  }
  function mount(html) {
    document.querySelectorAll(".walk.is-playing").forEach((walk) => {
      if (walk._timer) window.clearInterval(walk._timer);
    });
    stage().innerHTML = html;
    const panel = stage().querySelector("[data-panel]");
    if (panel) panel.classList.add("active");
    parkLandmarks(stage());
    document.dispatchEvent(new CustomEvent("campus-mount"));
  }
  const parked = new Set();
  function releaseLandmarks() {
    parked.forEach((id) => {
      const node = document.querySelector('#routeLandmarks [data-park="' + id + '"]');
      if (node && !document.getElementById(id)) node.id = id;
    });
    parked.clear();
  }
  function parkLandmarks(root) {
    releaseLandmarks();
    if (!root) return;
    root.querySelectorAll("[id]").forEach((node) => {
      const slot = document.querySelector('#routeLandmarks [id="' + CSS.escape(node.id) + '"]');
      if (!slot || slot === node) return;
      slot.dataset.park = node.id;
      slot.removeAttribute("id");
      parked.add(node.id);
    });
  }
  function ensureTargets() {
    const box = document.getElementById("routeLandmarks");
    if (!box) return;
    document.querySelectorAll('a[href^="#"]').forEach((link) => {
      const id = decodeURIComponent((link.getAttribute("href") || "").slice(1));
      if (!id || document.getElementById(id)) return;
      const node = document.createElement("span");
      node.id = id;
      node.tabIndex = -1;
      box.appendChild(node);
    });
  }
  function missingHTML(message) {
    return '<section id="view-missing" class="missing" data-panel="missing"><h1>That page is not in the course.</h1><p class="lede">' + message + '</p><p><a class="btn primary" href="#home">Back to home</a></p></section>';
  }
  async function loadJSON(url) {
    if (modules.has(url)) return modules.get(url);
    const job = fetch(url).then((res) => {
      if (!res.ok) throw new Error(url);
      return res.json();
    });
    modules.set(url, job);
    job.catch(() => modules.delete(url));
    return job;
  }
  async function ensure(route) {
    rememberHome();
    if (route.view === "home") {
      if (!mounted("home")) mount(homeHTML);
      return;
    }
    if (route.view === "map" || route.view === "studio" || route.view === "builds" || route.view === "play" || route.view === "downloads" || route.view === "arcade" || route.view === "atlas" || route.view === "flows" || route.view === "charts" || route.view === "regions") {
      if (mounted(route.view)) return;
      const data = await loadJSON("assets/curriculum/" + route.view + ".json");
      mount(data.html);
      return;
    }
    if (route.view === "school") {
      if (mounted(route.id)) return;
      const id = route.id.replace(/^school-/, "");
      const data = await loadJSON("assets/curriculum/track-" + id + ".json");
      mount(data.hub);
      return;
    }
    if (route.view === "lesson") {
      const meta = byMeta[route.id];
      if (!meta) throw new Error("unknown lesson");
      const existing = mounted(route.id);
      if (existing && existing.classList.contains("lesson")) return;
      const data = await loadJSON("assets/curriculum/track-" + meta.school + ".json");
      if (!data.lessons[route.id]) throw new Error("missing lesson");
      mount(data.lessons[route.id]);
      return;
    }
    if (!document.getElementById("view-missing")) mount(missingHTML("The link does not match a lesson or a track."));
  }
  function updateDock(route) {
    var key = route.view;
    if (route.view === "school" && route.id === "school-EX") key = "school-EX";
    if (route.view === "lesson" && route.id === "EX-11") key = "careers";
    document.querySelectorAll("[data-dock]").forEach((link) => {
      if (link.getAttribute("data-dock") === key) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
  }
  async function show(route) {
    const gen = ++showGen;
    let failed = false;
    try { await ensure(route); } catch (err) { failed = true; }
    if (gen !== showGen) return;
    if (failed) {
      mount(missingHTML("This view did not load. Open the course from the site once so the files can stay on this device. A local disk path cannot fetch the track files."));
      route = { view: "missing" };
    }
    const keepScroll = document.body.dataset.view === "play" && route.view === "play";
    document.body.dataset.view = route.view;
    document.body.classList.remove("is-enter");
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      requestAnimationFrame(() => document.body.classList.add("is-enter"));
    }
    document.querySelectorAll("[data-panel]").forEach((el) => el.classList.remove("active"));
    document.querySelectorAll("a.ll").forEach((link) => link.classList.remove("on"));
    let crumbText = "Home";
    let schoolId = null;
    if (route.view === "home") {
      mounted("home").classList.add("active");
    } else if (route.view === "map") {
      mounted("map").classList.add("active");
      crumbText = "Track map";
    } else if (route.view === "studio") {
      mounted("studio").classList.add("active");
      crumbText = "Studio";
      const studioLink = document.querySelector("a.studio-link");
      if (studioLink) studioLink.classList.add("on");
    } else if (route.view === "builds") {
      mounted("builds").classList.add("active");
      crumbText = "Builds";
      const buildsLink = document.querySelector("a.builds-link");
      if (buildsLink) buildsLink.classList.add("on");
    } else if (route.view === "play") {
      mounted("play").classList.add("active");
      crumbText = "Playgrounds";
      const playLink = document.querySelector("a.play-link");
      if (playLink) playLink.classList.add("on");
    } else if (route.view === "downloads") {
      mounted("downloads").classList.add("active");
      crumbText = "Cheat codes";
    } else if (route.view === "arcade") {
      mounted("arcade").classList.add("active");
      crumbText = "Arcade";
    } else if (route.view === "atlas" || route.view === "flows" || route.view === "charts" || route.view === "regions") {
      mounted(route.view).classList.add("active");
      crumbText = { atlas: "Diagrams", flows: "Flows", charts: "Charts", regions: "Regions" }[route.view];
    } else if (route.view === "school") {
      const page = mounted(route.id);
      if (!page) { show({ view: "missing" }); return; }
      page.classList.add("active");
      crumbText = page.querySelector("h1").textContent;
      schoolId = page.dataset.school;
    } else if (route.view === "lesson") {
      const page = mounted(route.id);
      if (!page) { show({ view: "missing" }); return; }
      crumbText = page.dataset.title;
      schoolId = page.dataset.school;
      await fillSchool(schoolId);
      page.classList.add("active");
      const link = document.querySelector('a.ll[data-id="' + route.id + '"]');
      if (link) link.classList.add("on");
      showLessonChrome(route.id);
    } else {
      const missing = document.getElementById("view-missing");
      if (missing) missing.classList.add("active");
      crumbText = "Not found";
    }
    crumb.textContent = crumbText;
    document.title = crumbText + " · AI Lab Free University";
    if (schoolId) setOpenSchool(schoolId);
    if (!keepScroll) window.scrollTo(0, 0);
    closeNav();
    updateDock(route);
    document.documentElement.classList.remove("route-pending");
    const h1 = document.querySelector("#stage h1");
    if (h1 && route.view !== "home") {
      h1.tabIndex = -1;
      h1.focus({ preventScroll: true });
    }
    document.dispatchEvent(new CustomEvent("campus-show", { detail: route }));
  }
  window.addEventListener("hashchange", () => show(parseHash()));

  function applySearch() {
    const term = search.value.trim().toLowerCase();
    document.querySelectorAll("a.ll").forEach((link) => {
      const hay = link.dataset.search || "";
      link.hidden = Boolean(term) && !hay.includes(term);
    });
    document.querySelectorAll(".school-block").forEach((block) => {
      const visible = [...block.querySelectorAll("a.ll")].some((link) => !link.hidden);
      block.hidden = Boolean(term) && !visible;
      if (term && visible) {
        block.classList.add("open");
        block.querySelector(".chev").setAttribute("aria-expanded", "true");
      }
    });
  }
  search.addEventListener("input", () => {
    const term = search.value.trim();
    if (!term) { applySearch(); return; }
    fillNav().then(applySearch);
  });
  search.addEventListener("keydown", (event) => {
    if (event.key !== "Enter") return;
    event.preventDefault();
    fillNav().then(() => {
      applySearch();
      const first = document.querySelector("a.ll:not([hidden])");
      if (first) location.hash = first.getAttribute("href");
    });
  });
  document.addEventListener("keydown", (event) => {
    const tag = (event.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea") return;
    if (event.key === "/") { event.preventDefault(); search.focus(); }
    if (document.body.dataset.view !== "lesson") return;
    if (event.key === "[" && !pagerPrev.hidden) pagerPrev.click();
    if (event.key === "]" && !pagerNext.hidden) pagerNext.click();
  });

  const sourcesBtn = document.getElementById("sourcesBtn");
  const sourcesDrawer = document.getElementById("sourcesDrawer");
  if (sourcesBtn && sourcesDrawer && sourcesDrawer.showModal) {
    sourcesBtn.addEventListener("click", () => sourcesDrawer.showModal());
    sourcesDrawer.addEventListener("click", (event) => {
      if (event.target.closest("[data-close]")) sourcesDrawer.close();
    });
  }
  const dockMenu = document.getElementById("dockMenu");
  if (dockMenu) dockMenu.addEventListener("click", () => menuBtn.click());
  if (location.protocol === "http:" || location.protocol === "https:") {
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("sw.js").catch(() => {});
    }
    const warm = ["assets/curriculum/map.json", "assets/curriculum/play.json", "assets/curriculum/studio.json", "assets/curriculum/builds.json", "assets/curriculum/downloads.json", "assets/curriculum/arcade.json", "assets/curriculum/atlas.json", "assets/curriculum/flows.json", "assets/curriculum/charts.json", "assets/curriculum/regions.json"]
      .concat(catalog.schools.map((school) => "assets/curriculum/track-" + school.id + ".json"));
    let warmIndex = 0;
    const warmNext = () => {
      if (warmIndex >= warm.length) return;
      const url = warm[warmIndex];
      warmIndex += 1;
      fetch(url).catch(() => {}).finally(() => {
        if (window.requestIdleCallback) window.requestIdleCallback(warmNext, { timeout: 2500 });
        else window.setTimeout(warmNext, 700);
      });
    };
    window.setTimeout(() => {
      if (window.requestIdleCallback) window.requestIdleCallback(warmNext, { timeout: 4000 });
      else warmNext();
    }, 12000);
  }
  refreshProgress();
  rememberHome();
  ensureTargets();
  window.campusBoot = () => show(parseHash());
})();

(function () {
  function reduced() {
    return document.documentElement.getAttribute("data-motion") === "reduce"
      || window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function fmt(seconds) {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return m + ":" + String(s).padStart(2, "0");
  }

  function paint(walk, step) {
    const n = Number(walk.dataset.steps);
    const next = Math.max(0, Math.min(n - 1, step));
    walk.dataset.step = String(next);
    walk.querySelectorAll(".stage").forEach((el) => {
      const i = Number(el.dataset.i);
      el.classList.toggle("is-now", i === next);
      el.classList.toggle("is-done", i < next);
      el.classList.toggle("is-todo", i > next);
    });
    walk.querySelectorAll(".edge").forEach((el) => {
      const dest = el.dataset.i;
      const hot = dest === "return" ? next === n - 1 : Number(dest) === next && next !== 0;
      const done = dest !== "return" && Number(dest) < next && Number(dest) !== 0;
      el.classList.toggle("is-hot", hot);
      el.classList.toggle("is-done", done && !hot);
    });
    const items = [...walk.querySelectorAll(".walk-script li")];
    items.forEach((li, i) => li.classList.toggle("is-now", i === next));
    const button = items[next].querySelector("button");
    const title = button.querySelector("strong").textContent;
    const rest = button.textContent.replace(title, "").replace(/\s+/g, " ").trim();
    walk.querySelector(".walk-caption").textContent = title + ". " + rest;
    walk.querySelector(".walk-count").textContent = "Step " + (next + 1) + " of " + n;
    const range = walk.querySelector("[data-act='range']");
    if (document.activeElement !== range) range.value = String(next);
    walk.querySelector(".walk-time").textContent = fmt(next * 4) + " / " + fmt(n * 4);
  }

  function pause(walk) {
    walk.classList.remove("is-playing");
    if (walk._timer) window.clearInterval(walk._timer);
    walk._timer = 0;
    const label = walk.querySelector(".play-label");
    if (label) label.textContent = "Play";
    const btn = walk.querySelector("[data-act='play']");
    if (btn) btn.setAttribute("aria-label", "Play");
  }

  function play(walk) {
    pause(walk);
    walk.classList.add("is-playing");
    walk.querySelector(".play-label").textContent = "Pause";
    walk.querySelector("[data-act='play']").setAttribute("aria-label", "Pause");
    const speed = Number(walk.dataset.speed || "1");
    const ms = Math.max(350, 3200 / speed);
    walk._timer = window.setInterval(() => {
      const n = Number(walk.dataset.steps);
      const step = Number(walk.dataset.step || "0");
      if (step >= n - 1) {
        pause(walk);
        return;
      }
      paint(walk, step + 1);
    }, ms);
  }

  function inspectStep(walk) {
    const box = walk.querySelector(".walk-inspect");
    const button = walk.querySelector("[data-act='inspect']");
    if (!box || !button) return;
    const open = button.getAttribute("aria-pressed") !== "true";
    button.setAttribute("aria-pressed", open ? "true" : "false");
    if (!open) {
      box.hidden = true;
      box.textContent = "";
      return;
    }
    const step = Number(walk.dataset.step || "0");
    const item = walk.querySelectorAll(".walk-script li")[step];
    const title = item ? item.querySelector("strong").textContent : "";
    const rest = item ? item.textContent.replace(title, "").replace(/\s+/g, " ").trim() : "";
    box.hidden = false;
    box.textContent = "Step " + (step + 1) + "\n" + title + "\n" + rest;
  }

  function bootWalks() {
    document.querySelectorAll(".walk").forEach((walk) => {
      if (walk.dataset.bound) return;
      walk.dataset.bound = "1";
      walk.dataset.speed = "1";
      paint(walk, 0);
      walk.addEventListener("click", (event) => {
        const btn = event.target.closest("[data-act]");
        if (!btn || !walk.contains(btn)) return;
        const act = btn.dataset.act;
        if (act === "range" || act === "speed") return;
        const n = Number(walk.dataset.steps);
        const step = Number(walk.dataset.step || "0");
        if (act === "play") {
          if (walk.classList.contains("is-playing")) pause(walk);
          else {
            if (step >= n - 1) paint(walk, 0);
            play(walk);
          }
        } else if (act === "prev") {
          pause(walk);
          paint(walk, step - 1);
        } else if (act === "next") {
          pause(walk);
          paint(walk, step + 1);
        } else if (act === "jump") {
          pause(walk);
          paint(walk, Number(btn.dataset.i));
        } else if (act === "inspect") {
          inspectStep(walk);
        }
      });
      walk.querySelector("[data-act='speed']").addEventListener("change", (event) => {
        walk.dataset.speed = event.target.value;
        if (walk.classList.contains("is-playing")) play(walk);
      });
      walk.querySelector("[data-act='range']").addEventListener("input", (event) => {
        pause(walk);
        paint(walk, Number(event.target.value));
      });
      walk.querySelectorAll(".stage").forEach((stage) => {
        stage.addEventListener("click", (event) => {
          event.stopPropagation();
          pause(walk);
          paint(walk, Number(stage.dataset.i));
        });
      });
    });
  }

  function startVisible() {
    document.querySelectorAll(".walk.is-playing").forEach(pause);
    if (reduced()) return;
    const view = document.body.dataset.view;
    let root = null;
    if (view === "home") root = document.getElementById("home");
    else if (view === "map") root = document.getElementById("map");
    else if (view === "studio") root = document.getElementById("studio");
    else if (view === "builds") root = document.getElementById("builds");
    else if (view === "lesson" || view === "school") {
      const raw = (location.hash || "").replace(/^#/, "");
      root = document.getElementById(raw);
    }
    const walk = root && root.querySelector(".walk");
    if (walk) play(walk);
  }

  function paintBars() {
    document.querySelectorAll("[data-school-bar]").forEach((bar) => {
      const id = bar.getAttribute("data-school-bar");
      const links = [...document.querySelectorAll('.school-block[data-school="' + id + '"] a.ll')];
      if (!links.length) return;
      const done = links.filter((link) => link.classList.contains("done")).length;
      bar.style.width = Math.round((done / links.length) * 100) + "%";
    });
  }

  function bootContrast() {
    if (document.getElementById("settingsBtn")) return;
    const button = document.getElementById("contrastBtn");
    if (!button) return;
    function apply(on) {
      document.documentElement.setAttribute("data-contrast", on ? "high" : "normal");
      try { localStorage.setItem("ailab-v3-contrast", on ? "high" : "normal"); } catch (err) { /* ignore */ }
      button.setAttribute("aria-pressed", on ? "true" : "false");
      button.setAttribute("aria-label", on ? "HC, turn off high contrast" : "HC, turn on high contrast");
    }
    let saved = "normal";
    try { saved = localStorage.getItem("ailab-v3-contrast") || "normal"; } catch (err) { saved = "normal"; }
    apply(saved === "high");
    button.addEventListener("click", () => {
      apply(document.documentElement.getAttribute("data-contrast") !== "high");
    });
  }

  function bootSearchMeta() {
    const box = document.getElementById("q");
    const meta = document.getElementById("searchMeta");
    if (!box || !meta) return;
    box.addEventListener("input", () => {
      if (!box.value.trim()) {
        meta.textContent = "";
        return;
      }
      const visible = [...document.querySelectorAll("a.ll[data-id]")].filter((link) => !link.hidden).length;
      meta.textContent = visible + (visible === 1 ? " lesson" : " lessons");
    });
  }

  function bootAudio() {
    document.querySelectorAll("audio[data-b64]").forEach((audio) => {
      const payload = (audio.getAttribute("data-b64") || "").replace(/\s+/g, "");
      if (!payload) return;
      audio.src = "data:audio/wav;base64," + payload;
    });
  }

  function bootSpeech() {
    document.addEventListener("click", (event) => {
      const button = event.target.closest(".speak");
      if (!button) return;
      const text = button.getAttribute("data-transcript") || "";
      const note = button.parentElement.nextElementSibling;
      const settings = window.CampusSettings;
      if (settings && !settings.narrationOn()) {
        if (note) note.textContent = "Narration is off. Turn it on in Settings.";
        return;
      }
      if (!window.speechSynthesis) {
        if (note) note.textContent = "This browser has no speech engine. Read the transcript above.";
        return;
      }
      const voice = settings && settings.voice ? settings.voice() : null;
      if (!voice) {
        if (note) note.textContent = "No high-quality English voice is installed. Pick a voice in Settings, or read the transcript. A robotic desktop voice is not the default.";
        return;
      }
      window.speechSynthesis.cancel();
      const utter = new SpeechSynthesisUtterance(text);
      utter.lang = voice.lang || "en";
      utter.voice = voice;
      utter.rate = settings && settings.rate ? settings.rate() : 1;
      window.speechSynthesis.speak(utter);
      if (note) note.textContent = "Speaking with " + voice.name + ".";
    });
  }

  function field(root, className) {
    return root.querySelector("." + className);
  }

  function bootTokenizer(root) {
    const vocab = ["context", "token", "model", "predicts", "the", "ing", "tion", "ent", "and", "ion", " you", " to", " of", " is", " a", "in", "er", "re", "on", "st", "th", "he", "an", " ", ".", ",", ":", ";", "'", "?", "!"].sort((a, b) => b.length - a.length);
    function run() {
      const text = field(root, "tok-in").value;
      const out = [];
      let i = 0;
      while (i < text.length) {
        const lower = text.slice(i).toLowerCase();
        let found = "";
        for (const token of vocab) {
          if (lower.startsWith(token)) {
            found = text.slice(i, i + token.length);
            break;
          }
        }
        if (!found) found = text.slice(i, i + 1);
        out.push(found);
        i += found.length;
      }
      const box = field(root, "tok-out");
      box.replaceChildren();
      out.forEach((token) => {
        const chip = document.createElement("span");
        chip.className = "tok-chip";
        chip.textContent = token === " " ? "␠" : token;
        box.appendChild(chip);
      });
      field(root, "tok-count").textContent = out.length + " toy tokens. A real tokenizer for your model can disagree.";
    }
    field(root, "tok-go").addEventListener("click", run);
    run();
  }

  function cosine(a, b) {
    let dot = 0;
    let na = 0;
    let nb = 0;
    for (let i = 0; i < a.length; i += 1) {
      dot += a[i] * b[i];
      na += a[i] * a[i];
      nb += b[i] * b[i];
    }
    if (na === 0 || nb === 0) return null;
    return dot / Math.sqrt(na * nb);
  }

  function bootCosine(root) {
    const presets = {
      near: { a: [0.92, 0.24, 0.05, 0], b: [0.8, 0.35, 0.08, 0.02], note: "Near neighbors in this toy space." },
      far: { a: [0.92, 0.24, 0.05, 0], b: [0.02, 0, 0.2, 0.95], note: "Different topics. Cosine stays low." },
      same: { a: [0.5, 0.5, 0.5, 0.5], b: [1, 1, 1, 1], note: "Same direction. Cosine is 1 even when the lengths differ." },
    };
    function inputs(holder, values) {
      holder.replaceChildren();
      values.forEach((value) => {
        const input = document.createElement("input");
        input.type = "number";
        input.step = "0.01";
        input.value = String(value);
        input.addEventListener("input", draw);
        holder.appendChild(input);
      });
    }
    function read(holder) {
      return [...holder.querySelectorAll("input")].map((input) => Number(input.value) || 0);
    }
    function draw() {
      const score = cosine(read(field(root, "vec-a")), read(field(root, "vec-b")));
      field(root, "cos-out").textContent = score === null ? "A zero-length vector has no direction." : "Cosine = " + score.toFixed(3) + ". 1 is the same direction, 0 is orthogonal.";
    }
    field(root, "cos-preset").addEventListener("change", (event) => {
      const preset = presets[event.target.value];
      inputs(field(root, "vec-a"), preset.a);
      inputs(field(root, "vec-b"), preset.b);
      field(root, "cos-out").textContent = preset.note;
      draw();
    });
    inputs(field(root, "vec-a"), presets.near.a);
    inputs(field(root, "vec-b"), presets.near.b);
    draw();
  }

  function softmax(row) {
    const max = Math.max(...row);
    const exps = row.map((value) => Math.exp(value - max));
    const sum = exps.reduce((total, value) => total + value, 0);
    return exps.map((value) => value / sum);
  }

  function bootAttention(root) {
    const tokens = ["The", "capital", "of", "France"];
    const embed = [
      [1, 0, 0, 0],
      [0.2, 1, 0, 0.3],
      [0, 0.2, 1, 0],
      [0.8, 0.7, 0, 1],
    ];
    const sketch = [
      [1, 0, 0, 0],
      [0.35, 0.65, 0, 0],
      [0.1, 0.15, 0.75, 0],
      [0.05, 0.5, 0.1, 0.35],
    ];
    function math() {
      const scale = Math.sqrt(4);
      const scores = embed.map((q) => embed.map((k) => q.reduce((sum, qv, i) => sum + qv * k[i], 0) / scale));
      for (let i = 0; i < 4; i += 1) {
        for (let j = i + 1; j < 4; j += 1) scores[i][j] = -1e9;
      }
      return scores.map(softmax);
    }
    function draw() {
      const mode = field(root, "att-mode").value;
      const grid = mode === "math" ? math() : sketch;
      const table = document.createElement("table");
      table.className = "att-table";
      const head = document.createElement("tr");
      head.appendChild(document.createElement("th"));
      tokens.forEach((token) => {
        const cell = document.createElement("th");
        cell.textContent = token;
        head.appendChild(cell);
      });
      table.appendChild(head);
      grid.forEach((row, i) => {
        const tr = document.createElement("tr");
        const label = document.createElement("th");
        label.textContent = tokens[i];
        tr.appendChild(label);
        row.forEach((value) => {
          const cell = document.createElement("td");
          cell.textContent = value < 0.001 ? "0" : value.toFixed(2);
          const mix = Math.round(255 - value * 140);
          cell.style.background = "rgb(" + mix + "," + (mix - 10) + ",255)";
          cell.style.color = value > 0.55 ? "#0B1220" : "inherit";
          tr.appendChild(cell);
        });
        table.appendChild(tr);
      });
      const box = field(root, "att-grid");
      box.replaceChildren(table);
      const note = document.createElement("p");
      note.className = "widget-note";
      note.textContent = mode === "math"
        ? "Rows sum to 1. Future tokens are masked. Bright cells are this toy arithmetic, not a model that knows geography."
        : "Hand-drawn pattern of the kind a trained head can learn. Not the output of a real model.";
      box.appendChild(note);
    }
    field(root, "att-mode").addEventListener("change", draw);
    draw();
  }

  function bootRag(root) {
    const docs = [
      { id: "notes-01", title: "Refund window", text: "The shop accepts returns for 30 days after delivery. After that, store credit needs a manager.", v: [1, 0, 0, 0] },
      { id: "notes-02", title: "Shipping", text: "Standard shipping takes 5 business days. Express takes 2. We do not ship to post office boxes.", v: [0, 1, 0, 0] },
      { id: "notes-03", title: "Passwords", text: "Support never asks for a password. Reset it from the account page.", v: [0, 0, 1, 0] },
      { id: "notes-04", title: "Memory fit", text: "If the weights do not fit, the runner swaps, crashes, or refuses. Start smaller and measure.", v: [0, 0, 0, 1] },
      { id: "notes-05", title: "Eval gate", text: "Ship a prompt change only when the same ten tasks are scored and quality does not fall.", v: [0.2, 0, 0, 0.9] },
      { id: "notes-06", title: "Tool approval", text: "Read-only tools may run inside the step cap. Sending, paying, or deleting waits for a person.", v: [0, 0.2, 0.9, 0] },
    ];
    const presets = {
      "how long do i have to return an item?": [0.95, 0.05, 0, 0],
      "do you ship to a post office box?": [0.05, 0.95, 0, 0],
      "can support ask for my password?": [0, 0.05, 0.95, 0],
      "what if the model does not fit in memory?": [0, 0, 0.05, 0.95],
      "when can i ship a prompt change?": [0.1, 0, 0, 0.9],
      "can the agent send the email itself?": [0, 0.1, 0.9, 0],
    };
    function keywords(query, text) {
      const terms = query.toLowerCase().split(/[^a-z0-9]+/).filter((word) => word.length > 2);
      if (!terms.length) return 0;
      const hay = text.toLowerCase();
      const hits = terms.filter((term) => hay.includes(term)).length;
      return hits / terms.length;
    }
    function run() {
      const query = field(root, "rag-q").value.trim();
      const vector = presets[query.toLowerCase()] || null;
      const ranked = docs.map((doc) => {
        const word = keywords(query, doc.title + " " + doc.text);
        const near = vector ? cosine(vector, doc.v) : null;
        const hybrid = near === null ? word : 0.45 * word + 0.55 * Math.max(0, near);
        return { doc, word, near, hybrid };
      }).sort((a, b) => b.hybrid - a.hybrid);
      const hits = field(root, "rag-hits");
      hits.replaceChildren();
      ranked.slice(0, 3).forEach((row) => {
        const p = document.createElement("p");
        p.className = "hit";
        const near = row.near === null ? "no preset vector" : "cosine " + row.near.toFixed(2);
        p.textContent = row.doc.id + " · " + row.doc.title + " · keyword " + row.word.toFixed(2) + " · " + near + " · hybrid " + row.hybrid.toFixed(2);
        hits.appendChild(p);
      });
      const best = ranked[0];
      const answer = field(root, "rag-answer");
      if (!query || best.hybrid < 0.28) {
        answer.textContent = "Refusal: the notes do not contain an answer to that question.";
      } else {
        answer.textContent = "From " + best.doc.id + ": \"" + best.doc.text + "\"";
      }
    }
    field(root, "rag-go").addEventListener("click", run);
    field(root, "rag-q").addEventListener("keydown", (event) => {
      if (event.key === "Enter") run();
    });
    run();
  }

  function bootLoss(root) {
    const train = field(root, "loss-train");
    const val = field(root, "loss-val");
    function y(value) {
      return 200 - value * 140;
    }
    function draw() {
      const over = Number(field(root, "loss-over").value) / 100;
      let dTrain = "";
      let dVal = "";
      for (let i = 0; i <= 40; i += 1) {
        const x = 48 + i * 13;
        const t = i / 40;
        const trainLoss = 1.15 * Math.exp(-3.1 * t) + 0.08;
        const valLoss = 1.1 * Math.exp(-2.2 * t) + 0.12 + over * t * t * 1.35;
        dTrain += (i === 0 ? "M" : "L") + x + " " + y(trainLoss).toFixed(1) + " ";
        dVal += (i === 0 ? "M" : "L") + x + " " + y(valLoss).toFixed(1) + " ";
      }
      train.setAttribute("d", dTrain);
      val.setAttribute("d", dVal);
      field(root, "loss-read").textContent = over > 0.55
        ? "Validation has turned up. That sketch is memorization, not a better model."
        : "Both curves fall. You would still score the held-out tasks before keeping a run.";
    }
    field(root, "loss-over").addEventListener("input", draw);
    draw();
  }

  function bootSample(root) {
    const tokens = [
      ["the", 4.2], ["cat", 3.1], ["sat", 1.6], ["dog", 0.7],
      ["on", 0.1], ["mat", -0.5], ["car", -1.2], ["code", -1.8],
    ];
    function nucleus(probs, p) {
      const order = probs.map((value, index) => ({ value, index })).sort((a, b) => b.value - a.value);
      const keep = new Set();
      let mass = 0;
      for (const item of order) {
        keep.add(item.index);
        mass += item.value;
        if (mass >= p) break;
      }
      const kept = probs.map((value, index) => (keep.has(index) ? value : 0));
      const sum = kept.reduce((total, value) => total + value, 0);
      return sum === 0 ? probs : kept.map((value) => value / sum);
    }
    function draw() {
      const temperature = Number(field(root, "temp").value) / 100;
      const topP = Number(field(root, "topp").value) / 100;
      const scaled = tokens.map((pair) => pair[1] / temperature);
      const raw = softmax(scaled);
      const cut = nucleus(raw, topP);
      const box = field(root, "sample-bars");
      box.replaceChildren();
      cut.forEach((value, index) => {
        const row = document.createElement("div");
        row.className = "sample-row" + (value === 0 ? " off" : "");
        const name = document.createElement("span");
        name.textContent = tokens[index][0];
        const bar = document.createElement("i");
        bar.style.width = Math.max(2, value * 100) + "%";
        const num = document.createElement("span");
        num.textContent = (value * 100).toFixed(1) + "%";
        row.append(name, bar, num);
        box.appendChild(row);
      });
      const meta = document.createElement("p");
      meta.className = "widget-note";
      meta.textContent = "Temperature " + temperature.toFixed(2) + ", top-p " + topP.toFixed(2) + ". Grey bars were cut by top-p.";
      box.appendChild(meta);
    }
    field(root, "temp").addEventListener("input", draw);
    field(root, "topp").addEventListener("input", draw);
    draw();
  }

  function bootContext(root) {
    function val(name) { return Number(field(root, name).value) || 0; }
    function draw() {
      const sys = val("c-sys");
      const ret = val("c-ret");
      const chat = val("c-chat");
      const out = val("c-out");
      const windowSize = Number(field(root, "c-win").value);
      const used = sys + ret + chat + out;
      const scale = Math.max(used, windowSize);
      field(root, "c-a").style.width = (sys / scale * 100) + "%";
      field(root, "c-b").style.width = (ret / scale * 100) + "%";
      field(root, "c-c").style.width = (chat / scale * 100) + "%";
      field(root, "c-d").style.width = (out / scale * 100) + "%";
      const pin = field(root, "c-pin").value;
      const pout = field(root, "c-pout").value;
      let cost = "Add prices to estimate a bill.";
      if (pin !== "" && pout !== "") {
        const inputCost = (sys + ret + chat) / 1e6 * Number(pin);
        const outputCost = out / 1e6 * Number(pout);
        cost = "Sketch cost $" + (inputCost + outputCost).toFixed(4) + " for this one call, before cache discounts and retries.";
      }
      const fit = used <= windowSize ? "Fits this example window." : "Overflows this example window. The call may error or truncate, and early instructions are a common casualty.";
      field(root, "c-read").textContent = used + " tokens planned against an example window of " + windowSize + ". " + fit + " " + cost;
    }
    root.querySelectorAll("input, select").forEach((el) => {
      el.addEventListener("input", draw);
      el.addEventListener("change", draw);
    });
    field(root, "c-example").addEventListener("click", () => {
      field(root, "c-pin").value = "2.50";
      field(root, "c-pout").value = "10.00";
      draw();
    });
    draw();
  }

  function bootLatency(root) {
    const points = [
      { x: 90, y: 150, name: "Small local", note: "Latency depends on fit and hardware. Accuracy is an eval, not a prize for staying local." },
      { x: 180, y: 120, name: "Fast hosted", note: "A short call. A fair default when ten extraction tasks already pass." },
      { x: 320, y: 90, name: "Frontier chat", note: "More room for hard writing. Pin the id and score the swap." },
      { x: 500, y: 60, name: "Reasoning", note: "Extra compute before the answer. Slower. Worth it when a wrong plan is expensive." },
      { x: 410, y: 140, name: "Long window", note: "A large window can still miss the middle of the prompt." },
    ];
    const svg = field(root, "lat-svg");
    svg.replaceChildren();
    const axis = document.createElementNS("http://www.w3.org/2000/svg", "path");
    axis.setAttribute("d", "M40 40 V280 H600");
    axis.setAttribute("class", "edge");
    svg.appendChild(axis);
    function label(x, y, text) {
      const node = document.createElementNS("http://www.w3.org/2000/svg", "text");
      node.setAttribute("x", String(x));
      node.setAttribute("y", String(y));
      node.setAttribute("class", "ns");
      node.textContent = text;
      svg.appendChild(node);
    }
    label(48, 36, "higher quality (sketch)");
    label(430, 304, "slower");
    points.forEach((point) => {
      const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      dot.setAttribute("cx", String(point.x));
      dot.setAttribute("cy", String(point.y));
      dot.setAttribute("r", "9");
      dot.setAttribute("class", "dot");
      dot.setAttribute("fill", "#6366F1");
      dot.addEventListener("click", () => {
        field(root, "lat-read").textContent = point.name + ". " + point.note;
      });
      svg.appendChild(dot);
      label(point.x + 12, point.y + 4, point.name);
    });
    field(root, "lat-read").textContent = "Click a point. Right is slower. Up is a higher sketched quality, not a measured score.";
  }

  function bootScore(root) {
    const rows = [
      { label: "Quality, higher is better", base: 80, candidate: 84, low: true },
      { label: "Safety failures, lower is better", base: 1, candidate: 1, low: false },
      { label: "Latency ms, lower is better", base: 900, candidate: 1100, low: false },
      { label: "Cost cents, lower is better", base: 4, candidate: 5, low: false },
    ];
    const grid = field(root, "score-grid");
    rows.forEach((row) => {
      const wrap = document.createElement("div");
      wrap.className = "score-row";
      const name = document.createElement("span");
      name.textContent = row.label;
      const base = document.createElement("input");
      base.type = "number";
      base.value = String(row.base);
      base.setAttribute("aria-label", row.label + " baseline");
      const cand = document.createElement("input");
      cand.type = "number";
      cand.value = String(row.candidate);
      cand.setAttribute("aria-label", row.label + " candidate");
      base.addEventListener("input", judge);
      cand.addEventListener("input", judge);
      wrap.append(name, base, cand);
      grid.appendChild(wrap);
      row.baseInput = base;
      row.candInput = cand;
    });
    function judge() {
      const q = Number(rows[0].candInput.value) >= Number(rows[0].baseInput.value);
      const s = Number(rows[1].candInput.value) <= Number(rows[1].baseInput.value);
      const l = Number(rows[2].candInput.value) <= Number(rows[2].baseInput.value);
      const c = Number(rows[3].candInput.value) <= Number(rows[3].baseInput.value);
      const ok = q && s && l && c;
      field(root, "score-gate").textContent = ok
        ? "Gate: ship. Quality held, safety failures did not rise, and latency and cost stayed inside the baseline."
        : "Gate: fix. " + [q ? "" : "Quality fell. ", s ? "" : "Safety failures rose. ", l ? "" : "Latency grew. ", c ? "" : "Cost grew."].join("");
    }
    judge();
  }

  function bootEmbed(root) {
    const points = [
      { x: 120, y: 160, name: "refund policy", group: "shop" },
      { x: 160, y: 130, name: "return window", group: "shop" },
      { x: 150, y: 190, name: "store credit", group: "shop" },
      { x: 360, y: 80, name: "shipping days", group: "ship" },
      { x: 410, y: 120, name: "post office box", group: "ship" },
      { x: 520, y: 210, name: "password reset", group: "account" },
      { x: 570, y: 180, name: "support script", group: "account" },
      { x: 300, y: 240, name: "quantized weights", group: "ops" },
    ];
    const colors = { shop: "#0F9B8E", ship: "#6366F1", account: "#F5B942", ops: "#22C55E" };
    const svg = field(root, "emb-svg");
    svg.replaceChildren();
    function nearest(index) {
      return points
        .map((point, i) => ({ i, d: Math.hypot(point.x - points[index].x, point.y - points[index].y) }))
        .filter((item) => item.i !== index)
        .sort((a, b) => a.d - b.d)
        .slice(0, 2);
    }
    points.forEach((point, index) => {
      const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      dot.setAttribute("cx", String(point.x));
      dot.setAttribute("cy", String(point.y));
      dot.setAttribute("r", "8");
      dot.setAttribute("fill", colors[point.group]);
      dot.setAttribute("class", "dot");
      dot.addEventListener("click", () => {
        const near = nearest(index).map((item) => points[item.i].name).join(" and ");
        field(root, "emb-read").textContent = point.name + " is nearest to " + near + " in this flat drawing.";
      });
      svg.appendChild(dot);
      const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("x", String(point.x + 10));
      text.setAttribute("y", String(point.y - 10));
      text.setAttribute("class", "ns");
      text.textContent = point.name;
      svg.appendChild(text);
    });
    field(root, "emb-read").textContent = "Click a point. Distance here is ordinary 2D distance, a picture of nearest neighbors.";
  }

  const boots = {
    tokenizer: bootTokenizer,
    cosine: bootCosine,
    attention: bootAttention,
    rag: bootRag,
    loss: bootLoss,
    sample: bootSample,
    context: bootContext,
    latency: bootLatency,
    scorecard: bootScore,
    embed: bootEmbed,
  };

  function bootWidgets() {
    document.querySelectorAll(".widget").forEach((root) => {
      if (root.dataset.ready) return;
      const kind = root.dataset.widget;
      const boot = boots[kind];
      if (!boot) return;
      root.dataset.ready = "1";
      boot(root);
    });
  }

  bootWalks();
  bootWidgets();
  bootContrast();
  bootSearchMeta();
  bootAudio();
  bootSpeech();
  paintBars();
  document.addEventListener("campus-progress", paintBars);
  document.addEventListener("campus-show", startVisible);
  document.addEventListener("campus-mount", () => {
    bootWalks();
    bootWidgets();
    bootAudio();
  });
  startVisible();
})();

(function () {
  function field(root, className) {
    return root.querySelector("." + className);
  }

  function readNum(root, className, fallback) {
    const node = field(root, className);
    const value = node ? Number(node.value) : fallback;
    return Number.isFinite(value) ? value : fallback;
  }

  function say(root, text) {
    const node = field(root, "demo-read");
    if (node) node.textContent = text;
  }

  function softmax(row) {
    const max = Math.max(...row);
    const exps = row.map((value) => Math.exp(value - max));
    const sum = exps.reduce((total, value) => total + value, 0);
    return exps.map((value) => value / sum);
  }

  function button(label, onClick) {
    const node = document.createElement("button");
    node.type = "button";
    node.className = "chart-btn";
    node.textContent = label;
    node.addEventListener("click", onClick);
    return node;
  }

  function drawBars(host, points, onPick) {
    const peak = Math.max(...points.map((point) => point.value), 1);
    host.replaceChildren();
    points.forEach((point) => {
      const node = button(point.label + " " + point.value, () => onPick(point.label + ": " + point.value));
      node.style.height = Math.max(18, (point.value / peak) * 96) + "px";
      host.appendChild(node);
    });
  }

  function drawLine(host, points, onPick, area) {
    host.replaceChildren();
    const series = points[0] && points[0].values ? points[0].values.length : 1;
    for (let s = 0; s < (points[0] && points[0].values ? points[0].values.length : 1); s += 1) {
      const values = points.map((point) => (point.values ? point.values[s] : point.value));
      const peak = Math.max(...values, 0.001);
      const row = document.createElement("div");
      row.className = "chart-line" + (area ? " is-area" : "");
      values.forEach((value, index) => {
        const node = button(points[index].label, () => onPick(points[index].label + " series " + (s + 1) + ": " + value));
        node.style.height = Math.max(8, (value / peak) * 72) + "px";
        row.appendChild(node);
      });
      host.appendChild(row);
    }
    if (!series) host.textContent = "";
  }

  function drawWaterfall(host, points, onPick) {
    let running = 0;
    const rows = points.map((point) => {
      running += point.value;
      return point.label + " +" + point.value + " = " + running;
    });
    host.replaceChildren();
    rows.forEach((row, index) => {
      host.appendChild(button(row, () => onPick(row + ". Running total of the example token lines.")));
      void index;
    });
  }

  function drawFunnel(host, points, onPick) {
    const peak = Math.max(...points.map((point) => point.value), 1);
    host.replaceChildren();
    points.forEach((point) => {
      const node = button(point.label + " " + point.value, () => onPick(point.label + ": " + point.value));
      node.style.width = Math.max(28, (point.value / peak) * 100) + "%";
      host.appendChild(node);
    });
  }

  function drawTimeline(host, points, onPick) {
    host.replaceChildren();
    points.forEach((point, index) => {
      host.appendChild(button((index + 1) + ". " + point.label, () => onPick("Step " + (index + 1) + ": " + point.label)));
    });
  }

  function drawStack(host, payload, onPick) {
    host.replaceChildren();
    payload.points.forEach((point) => {
      const row = document.createElement("div");
      row.className = "chart-stack";
      point.values.forEach((value, index) => {
        const name = (payload.series && payload.series[index]) || "part " + (index + 1);
        const node = button(name + " " + value, () => onPick(point.label + " · " + name + ": " + value));
        node.style.flexGrow = String(Math.max(value, 0.2));
        row.appendChild(node);
      });
      host.appendChild(row);
    });
  }

  function drawScatter(host, points, onPick) {
    host.replaceChildren();
    points.forEach((point) => {
      host.appendChild(button(point.label, () => onPick(point.label + " at sketch x " + point.x + ", y " + point.y + ". Up is not a measured score.")));
    });
  }

  function drawHeat(host, payload, onPick) {
    host.replaceChildren();
    const table = document.createElement("table");
    table.className = "att-table";
    const head = document.createElement("tr");
    head.appendChild(document.createElement("th"));
    payload.cols.forEach((col) => {
      const cell = document.createElement("th");
      cell.textContent = col;
      head.appendChild(cell);
    });
    table.appendChild(head);
    payload.grid.forEach((row, r) => {
      const tr = document.createElement("tr");
      const label = document.createElement("th");
      label.textContent = payload.rows[r];
      tr.appendChild(label);
      row.forEach((value, c) => {
        const cell = document.createElement("td");
        const btn = button(value.toFixed(2), () => onPick(payload.rows[r] + " → " + payload.cols[c] + ": " + value));
        cell.appendChild(btn);
        tr.appendChild(cell);
      });
      table.appendChild(tr);
    });
    host.appendChild(table);
  }

  function drawRadar(host, points, onPick) {
    drawBars(host, points, onPick);
  }

  function drawSlope(host, payload, onPick) {
    host.replaceChildren();
    payload.points.forEach((point) => {
      const row = document.createElement("div");
      row.className = "chart-slope";
      row.append(
        button(payload.left + " " + point.a, () => onPick(point.label + " retrieval " + point.a)),
        button(payload.right + " " + point.b, () => onPick(point.label + " rerank " + point.b + ". Unfetched passages are absent.")),
      );
      host.appendChild(row);
    });
  }

  const drawers = {
    bar: (host, payload, onPick) => drawBars(host, payload.points, onPick),
    hist: (host, payload, onPick) => drawBars(host, payload.points, onPick),
    line: (host, payload, onPick) => drawLine(host, payload.points, onPick, false),
    area: (host, payload, onPick) => drawLine(host, payload.points, onPick, true),
    waterfall: (host, payload, onPick) => drawWaterfall(host, payload.points, onPick),
    funnel: (host, payload, onPick) => drawFunnel(host, payload.points, onPick),
    timeline: (host, payload, onPick) => drawTimeline(host, payload.points, onPick),
    stack: (host, payload, onPick) => drawStack(host, payload, onPick),
    scatter: (host, payload, onPick) => drawScatter(host, payload.points, onPick),
    heat: (host, payload, onPick) => drawHeat(host, payload, onPick),
    radar: (host, payload, onPick) => drawRadar(host, payload.points, onPick),
    slope: (host, payload, onPick) => drawSlope(host, payload, onPick),
  };

  function bootChart(root) {
    const kind = root.dataset.kind;
    const draw = drawers[kind];
    const host = field(root, "chart-host");
    if (!draw || !host) {
      say(root, "This chart has no drawer.");
      return;
    }
    const payload = JSON.parse(root.dataset.payload || "{}");
    draw(host, payload, (text) => say(root, text));
    say(root, "Select a mark. " + (field(root, "widget-note") ? field(root, "widget-note").textContent : ""));
  }

  function bootSampling(root) {
    const tokens = [
      ["the", 4.2], ["cat", 3.1], ["sat", 1.6], ["dog", 0.7],
      ["on", 0.1], ["mat", -0.5], ["car", -1.2], ["code", -1.8],
    ];
    function draw() {
      const temperature = readNum(root, "s-temp", 80) / 100;
      const topP = readNum(root, "s-p", 100) / 100;
      const topK = Math.round(readNum(root, "s-k", 8));
      const scaled = tokens.map((pair) => pair[1] / temperature);
      let probs = softmax(scaled);
      const order = probs.map((value, index) => ({ value, index })).sort((a, b) => b.value - a.value);
      const keep = new Set(order.slice(0, topK).map((item) => item.index));
      probs = probs.map((value, index) => (keep.has(index) ? value : 0));
      const cut = probs.map((value, index) => ({ value, index })).sort((a, b) => b.value - a.value);
      const kept = new Set();
      let mass = 0;
      const sum = probs.reduce((total, value) => total + value, 0) || 1;
      const normalized = probs.map((value) => value / sum);
      const ranked = normalized.map((value, index) => ({ value, index })).sort((a, b) => b.value - a.value);
      let covered = 0;
      for (const item of ranked) {
        if (item.value === 0) continue;
        kept.add(item.index);
        covered += item.value;
        if (covered >= topP) break;
      }
      const after = normalized.map((value, index) => (kept.has(index) ? value : 0));
      const again = after.reduce((total, value) => total + value, 0) || 1;
      const finalProbs = after.map((value) => value / again);
      const box = field(root, "sample-bars");
      box.replaceChildren();
      finalProbs.forEach((value, index) => {
        const row = document.createElement("div");
        row.className = "sample-row" + (value === 0 ? " off" : "");
        const name = document.createElement("span");
        name.textContent = tokens[index][0];
        const bar = document.createElement("i");
        bar.style.width = Math.max(2, value * 100) + "%";
        const num = document.createElement("span");
        num.textContent = (value * 100).toFixed(1) + "%";
        row.append(name, bar, num);
        box.appendChild(row);
      });
      say(root, "Temperature " + temperature.toFixed(2) + ", top-k " + topK + ", top-p " + topP.toFixed(2) + ". Grey rows were cut. This list is not a fact check.");
      void cut;
    }
    root.querySelectorAll("input").forEach((input) => input.addEventListener("input", draw));
    draw();
  }

  function bootChunk(root) {
    const text = "Refund window. The shop accepts returns for 30 days after delivery. Shipping. Standard shipping takes 5 business days. Passwords. Support never asks for a password.";
    function draw() {
      const windowSize = Math.round(readNum(root, "ch-win", 80));
      const list = field(root, "chunk-list");
      list.replaceChildren();
      let count = 0;
      for (let cursor = 0; cursor < text.length; cursor += windowSize) {
        const slice = text.slice(cursor, cursor + windowSize);
        const row = document.createElement("p");
        row.className = "hit";
        row.textContent = "c" + count + " · " + slice;
        list.appendChild(row);
        count += 1;
      }
      say(root, count + " chunks at " + windowSize + " characters. A heading split across chunks is a defect this slider is meant to show.");
    }
    field(root, "ch-win").addEventListener("input", draw);
    draw();
  }

  function bootRerank(root) {
    const rows = [
      { id: "notes-01", title: "Refund window", retrieval: 0.91, rerank: 0.62 },
      { id: "notes-05", title: "Eval gate", retrieval: 0.33, rerank: 0.88 },
      { id: "notes-02", title: "Shipping", retrieval: 0.44, rerank: 0.21 },
      { id: "notes-09", title: "Unfetched policy", retrieval: 0, rerank: null },
    ];
    function paint(mode) {
      const fetched = rows.filter((row) => row.retrieval > 0);
      const ranked = fetched.slice().sort((a, b) => (mode === "rerank" ? b.rerank - a.rerank : b.retrieval - a.retrieval));
      const list = field(root, "rk-list");
      list.replaceChildren();
      ranked.forEach((row) => {
        const p = document.createElement("p");
        p.className = "hit";
        p.textContent = row.id + " · " + row.title + " · retrieval " + row.retrieval.toFixed(2) + " · rerank " + row.rerank.toFixed(2);
        list.appendChild(p);
      });
      const missing = rows.find((row) => row.rerank === null);
      const p = document.createElement("p");
      p.className = "hit";
      p.textContent = missing.id + " · " + missing.title + " · not fetched, so it cannot be reranked.";
      list.appendChild(p);
      say(root, "Sorted by " + mode + ". " + ranked[0].id + " is first in this hand-set list.");
    }
    field(root, "rk-ret").addEventListener("click", () => paint("retrieval"));
    field(root, "rk-rr").addEventListener("click", () => paint("rerank"));
    paint("retrieval");
  }

  function bootTrace(root) {
    const steps = [
      ["Goal", "Draft a refund reply from the notes. Done when the draft cites a note id or refuses."],
      ["Propose read_notes", "The model proposes read_notes. It does not run the handler."],
      ["Handler", "Your code returns notes-01. The shop accepts returns for 30 days after delivery."],
      ["Draft", "The draft quotes notes-01. The quote is text a person can open."],
      ["Propose send_email", "The model proposes send_email with a recipient and a body."],
      ["Policy asks", "Send is not allow. The host shows the exact arguments and waits for a person."],
      ["Stop", "The loop stops. Nothing is sent. The trace keeps the proposal and the stop."],
    ];
    let index = 0;
    function paint() {
      say(root, "Step " + (index + 1) + " of " + steps.length + ". " + steps[index][0] + ". " + steps[index][1]);
    }
    field(root, "tr-prev").addEventListener("click", () => {
      index = Math.max(0, index - 1);
      paint();
    });
    field(root, "tr-next").addEventListener("click", () => {
      index = Math.min(steps.length - 1, index + 1);
      paint();
    });
    paint();
  }

  function bootLora(root) {
    function draw() {
      const din = readNum(root, "lora-in", 4096);
      const dout = readNum(root, "lora-out", 4096);
      const rank = readNum(root, "lora-rank", 16);
      const layers = readNum(root, "lora-layers", 32);
      const trainable = 2 * rank * (din + dout) * layers;
      const full = din * dout * layers;
      const share = full === 0 ? 0 : (100 * trainable) / full;
      say(root, "Trainable " + Math.round(trainable).toLocaleString("en-US") + ". Full matrix stack " + Math.round(full).toLocaleString("en-US") + ". Share " + share.toFixed(2) + "%. Example dimensions, not a model card.");
    }
    root.querySelectorAll("input").forEach((input) => input.addEventListener("input", draw));
    draw();
  }

  function bootQuant(root) {
    function draw() {
      const billions = readNum(root, "q-b", 7);
      const bits = readNum(root, "q-bits", 4);
      const gb = billions * (bits / 8);
      say(root, "Weight file about " + gb.toFixed(2) + " GB. That is the weights only. A 16 GB machine is the starting point for a 7B or 8B Q4 or Q5 because the runner and the KV cache are extra. 8 GB starts smaller.");
    }
    root.querySelectorAll("input").forEach((input) => input.addEventListener("input", draw));
    draw();
  }

  function bootSchema(root) {
    function draw() {
      let parsed = null;
      try { parsed = JSON.parse(field(root, "sch-in").value); } catch (err) { parsed = null; }
      if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
        say(root, "Reject. The call is not a JSON object.");
        return;
      }
      const missing = ["name", "query"].filter((key) => parsed[key] === undefined || parsed[key] === "");
      say(root, missing.length ? "Reject. Missing " + missing.join(", ") + "." : "Accept. name and query are present. The handler may run.");
    }
    field(root, "sch-go").addEventListener("click", draw);
    draw();
  }

  function bootApproval(root) {
    function draw() {
      const verb = field(root, "ap-verb").value;
      const args = field(root, "ap-args").value;
      let decision = "Deny. This verb is not on the allowlist.";
      if (verb === "read_notes") decision = "Allow, inside the step cap.";
      if (verb === "send_email" || verb === "pay" || verb === "delete") decision = "Ask. A person confirms these exact arguments before anything happens.";
      say(root, verb + " " + args + ". " + decision);
    }
    field(root, "ap-verb").addEventListener("change", draw);
    field(root, "ap-args").addEventListener("input", draw);
    draw();
  }

  function bootIdem(root) {
    const store = new Map();
    field(root, "id-go").addEventListener("click", () => {
      const key = field(root, "id-key").value;
      const args = field(root, "id-args").value;
      if (store.has(key)) {
        const prior = store.get(key);
        say(root, prior === args ? "Replay the stored result for " + key + ". The handler does not run again." : "Conflict. " + key + " was already used with different arguments. Do not run it.");
        return;
      }
      store.set(key, args);
      say(root, "Stored " + key + ". A later submit with the same arguments replays. A retry must not double-send.");
    });
    say(root, "Submit once, then submit the same key again.");
  }

  function bootFit(root) {
    function draw() {
      const used = readNum(root, "fit-a", 0) + readNum(root, "fit-b", 0) + readNum(root, "fit-c", 0) + readNum(root, "fit-d", 0);
      const windowSize = readNum(root, "fit-w", 8192);
      const fit = used <= windowSize ? "Fits this example window." : "Overflows this example window. Early instructions are a common casualty.";
      say(root, used + " tokens against " + windowSize + ". " + fit);
    }
    root.querySelectorAll("input").forEach((input) => input.addEventListener("input", draw));
    draw();
  }

  function bootHybrid(root) {
    function draw() {
      const weight = readNum(root, "hy-w", 55) / 100;
      const score = 0.2 * (1 - weight) + 0.9 * weight;
      say(root, "Hybrid " + score.toFixed(2) + " with cosine weight " + weight.toFixed(2) + ". Hand-set scores, not an embedding model.");
    }
    field(root, "hy-w").addEventListener("input", draw);
    draw();
  }

  function bootRetry(root) {
    function draw() {
      const budget = readNum(root, "ry-b", 2);
      const attempts = readNum(root, "ry-a", 1);
      const stop = attempts > budget ? "Stop. The budget is spent." : "Inside the budget.";
      say(root, attempts + " calls against a budget of " + budget + ". " + stop + " This count is not a price.");
    }
    root.querySelectorAll("input").forEach((input) => input.addEventListener("input", draw));
    draw();
  }

  function bootCite(root) {
    function draw() {
      const cited = [...root.querySelectorAll(".cite-box:checked")].map((box) => box.value);
      const hit = cited.includes("notes-01");
      say(root, cited.length ? (hit ? "notes-01 is cited. Coverage of the required id is 1." : "Cited " + cited.join(", ") + ". The required id notes-01 is missing.") : "Nothing cited. A blank list is not a pass.");
    }
    root.querySelectorAll(".cite-box").forEach((box) => box.addEventListener("change", draw));
    draw();
  }

  function bootCap(root) {
    function draw() {
      const taken = readNum(root, "cap-n", 0);
      say(root, taken >= 6 ? "Stop. The example cap is 6." : (6 - taken) + " steps left under the example cap of 6.");
    }
    field(root, "cap-n").addEventListener("input", draw);
    draw();
  }

  function bootKv(root) {
    function draw() {
      const tokens = readNum(root, "kv-n", 2048);
      const bytes = 2 * 32 * 8 * 128 * tokens * 2;
      const mb = bytes / (1024 * 1024);
      say(root, mb.toFixed(1) + " MB at " + tokens + " tokens. Sketch formula, not a runner report.");
    }
    field(root, "kv-n").addEventListener("input", draw);
    draw();
  }

  function bootPin(root) {
    function draw() {
      const prompt = field(root, "pin-p").value.trim();
      const model = field(root, "pin-m").value.trim();
      const index = field(root, "pin-i").value.trim();
      const missing = [];
      if (!prompt) missing.push("prompt id");
      if (!model) missing.push("model id");
      if (!index) missing.push("index version");
      say(root, missing.length ? "Not pinned. Missing " + missing.join(", ") + "." : "Pinned. Prompt " + prompt + ", model " + model + ", index " + index + ".");
    }
    root.querySelectorAll("input").forEach((input) => input.addEventListener("input", draw));
    draw();
  }

  function bootRefuse(root) {
    const notes = [
      { id: "notes-01", text: "returns for 30 days after delivery" },
      { id: "notes-02", text: "standard shipping takes 5 business days" },
      { id: "notes-03", text: "support never asks for a password" },
    ];
    function draw() {
      const query = field(root, "rf-q").value.toLowerCase();
      const terms = query.split(/[^a-z0-9]+/).filter((word) => word.length > 3);
      let best = null;
      let bestHits = 0;
      notes.forEach((note) => {
        const hits = terms.filter((term) => note.text.includes(term) || query.includes(note.text.split(" ")[0])).length;
        if (hits > bestHits) {
          bestHits = hits;
          best = note;
        }
      });
      const direct = notes.find((note) => query.includes("return") || query.includes("refund") ? note.id === "notes-01" : false);
      const chosen = direct || (bestHits > 0 ? best : null);
      say(root, chosen ? "From " + chosen.id + ": " + chosen.text + "." : "Refusal. The notes do not contain an answer to that question.");
    }
    field(root, "rf-go").addEventListener("click", draw);
    draw();
  }

  const playgrounds = {
    sampling: bootSampling,
    chunk: bootChunk,
    rerank: bootRerank,
    trace: bootTrace,
    lora: bootLora,
    quant: bootQuant,
    schema: bootSchema,
    approval: bootApproval,
    idem: bootIdem,
    fit: bootFit,
    hybrid: bootHybrid,
    retry: bootRetry,
    cite: bootCite,
    cap: bootCap,
    kv: bootKv,
    pin: bootPin,
    refuse: bootRefuse,
  };

  function bootDemos() {
    document.querySelectorAll(".demo").forEach((root) => {
      if (root.dataset.ready) return;
      root.dataset.ready = "1";
      if (root.dataset.chart) bootChart(root);
      else if (playgrounds[root.dataset.demo]) playgrounds[root.dataset.demo](root);
    });
  }

  function paintMarks() {
    const list = document.getElementById("badgeList");
    const empty = document.getElementById("markEmpty");
    if (!list || !empty) return;
    let studied = [];
    let seen = [];
    try { studied = JSON.parse(localStorage.getItem("ailab-v3-studied") || "[]"); } catch (err) { studied = []; }
    try { seen = JSON.parse(localStorage.getItem("ailab-v3-seen") || "[]"); } catch (err) { seen = []; }
    const done = new Set(studied);
    const marks = [];
    if (done.size >= 1) marks.push("First lesson");
    if (done.size >= 10) marks.push("Ten lessons");
    if (done.size >= 64) marks.push("Halfway");
    if (done.size >= 128) marks.push("Full course");
    document.querySelectorAll(".school-block").forEach((block) => {
      const links = [...block.querySelectorAll("a.ll")];
      if (!links.length) return;
      const finished = links.every((link) => done.has(link.dataset.id));
      if (!finished) return;
      const name = block.querySelector(".sname");
      marks.push((name ? name.textContent : block.dataset.school) + " complete");
    });
    if (seen.includes("studio")) marks.push("Opened the studio");
    if (seen.includes("builds")) marks.push("Opened the builds");
    if (seen.includes("play")) marks.push("Opened the playgrounds");
    let streakDays = [];
    try { streakDays = JSON.parse(localStorage.getItem("ailab-v3-streak") || "[]"); } catch (err) { streakDays = []; }
    const streak = window.LabExtra ? window.LabExtra.streakLength(streakDays) : 0;
    if (streak >= 2) marks.push(streak >= 7 ? "Seven-day streak" : "Two-day streak");
    let quizBest = 0;
    let boss = "";
    try { quizBest = Number(localStorage.getItem("ailab-v3-quiz-best") || "0"); } catch (err) { quizBest = 0; }
    try { boss = localStorage.getItem("ailab-v3-boss") || ""; } catch (err) { boss = ""; }
    if (quizBest >= 20) marks.push("Quiz in progress");
    if (boss === "pass") marks.push("Boss exam");
    list.replaceChildren();
    marks.forEach((mark) => {
      const item = document.createElement("li");
      item.className = "badge-chip is-on";
      item.textContent = mark;
      list.appendChild(item);
    });
    empty.hidden = marks.length > 0;
  }

  function paintMap() {
    document.querySelectorAll("[data-map-school]").forEach((node) => {
      const id = node.getAttribute("data-map-school");
      const links = [...document.querySelectorAll('.school-block[data-school="' + id + '"] a.ll')];
      if (!links.length) return;
      const done = links.filter((link) => link.classList.contains("done")).length;
      const count = node.querySelector(".map-count");
      if (count) count.textContent = done + " of " + links.length;
      const bar = node.querySelector(".map-fill");
      if (bar) bar.style.width = Math.round((done / links.length) * 100) + "%";
      node.classList.toggle("is-started", done > 0);
      node.classList.toggle("is-complete", done === links.length);
    });
  }

  function rememberView() {
    const view = document.body.dataset.view;
    if (view !== "studio" && view !== "builds" && view !== "play") return;
    let seen = [];
    try { seen = JSON.parse(localStorage.getItem("ailab-v3-seen") || "[]"); } catch (err) { seen = []; }
    if (!seen.includes(view)) {
      seen.push(view);
      try { localStorage.setItem("ailab-v3-seen", JSON.stringify(seen)); } catch (err) { /* ignore */ }
    }
    paintMarks();
  }

  document.addEventListener("click", (event) => {
    const jump = event.target.closest(".jump-build");
    if (!jump) return;
    const target = document.getElementById(jump.getAttribute("data-target") || "");
    if (target) target.scrollIntoView({ block: "start" });
  });

  bootDemos();
  paintMarks();
  paintMap();
  rememberView();
  document.addEventListener("campus-progress", () => {
    paintMap();
    paintMarks();
  });
  document.addEventListener("campus-show", () => {
    rememberView();
    paintMap();
  });
  document.addEventListener("campus-mount", () => {
    bootDemos();
    paintMap();
    paintMarks();
  });
})();

/* Offline playground math. Toy numbers, labeled as toy. No network. */
(function (root, factory) {
  var api = factory();
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.LabPlay = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  var STOP = {
    a: 1, an: 1, the: 1, of: 1, to: 1, do: 1, i: 1, is: 1, how: 1, long: 1,
    what: 1, when: 1, where: 1, and: 1, for: 1, in: 1, on: 1, my: 1, me: 1,
    you: 1, your: 1, may: 1, be: 1, it: 1, this: 1, that: 1, with: 1, from: 1
  };
  var AXIS = {
    return: [1, 0.1], refund: [0.95, 0.15], unopened: [0.75, 0], item: [0.45, 0.05],
    within: [0.6, 0.2], days: [0.2, 0.35], after: [0.35, 0.15], sale: [0.3, 0],
    final: [0.25, -0.05], customer: [0.4, 0.1], window: [0.9, 0.25],
    shipping: [-0.1, 1], standard: [0, 0.75], business: [0.05, 0.7],
    country: [-0.05, 0.55], express: [-0.15, 0.95], arrives: [0, 0.5],
    next: [0.05, 0.4], two: [0, 0.45],
    support: [-0.85, -0.15], desk: [-0.7, -0.1], open: [-0.55, 0.05],
    weekdays: [-0.8, 0], hours: [-0.75, -0.05], time: [-0.4, -0.2],
    local: [-0.15, -0.9], model: [-0.05, -0.85], weights: [0.1, -0.8],
    disk: [-0.1, -0.7], notes: [0.15, -0.55], separate: [0.05, -0.5],
    machine: [-0.2, -0.75], runs: [-0.1, -0.6],
    phone: [0.95, -0.95], ceo: [1, -1], number: [0.4, -0.55]
  };
  var NOTES = [
    { id: "policy-refund", title: "Refunds", text: "A customer may return an unopened item within 30 days for a refund. After 30 days the sale is final." },
    { id: "policy-ship", title: "Shipping", text: "Standard shipping takes two business days inside the country. Express shipping arrives the next business day." },
    { id: "policy-hours", title: "Hours", text: "The support desk is open on weekdays from 9 to 17 local time." },
    { id: "lab-local", title: "Local model", text: "The lab machine runs an open-weight model. Weights stay on disk and are separate from the notes." }
  ];

  function round(value) {
    return Math.round(value * 1000) / 1000;
  }

  function words(text) {
    return (String(text).toLowerCase().match(/[a-z0-9]+/g) || []).filter(function (word) {
      return !STOP[word];
    });
  }

  function wordVec(word) {
    if (AXIS[word]) return AXIS[word];
    var hash = 2166136261;
    for (var i = 0; i < word.length; i += 1) {
      hash ^= word.charCodeAt(i);
      hash = Math.imul(hash, 16777619);
    }
    var x = ((hash >>> 0) % 100) / 800;
    var y = (((hash >>> 8) >>> 0) % 100) / 800;
    return [x - 0.06, y - 0.06];
  }

  function embed(text) {
    var acc = [0, 0];
    words(text).forEach(function (word) {
      var vec = wordVec(word);
      acc[0] += vec[0];
      acc[1] += vec[1];
    });
    var norm = Math.hypot(acc[0], acc[1]);
    if (!norm) return [0, 0];
    return [acc[0] / norm, acc[1] / norm];
  }

  function chunks() {
    var out = [];
    NOTES.forEach(function (note) {
      note.text.split(/(?<=\.)\s+/).forEach(function (sentence, index) {
        var point = embed(sentence);
        out.push({
          id: note.id + "#" + (index + 1),
          note: note.id,
          title: note.title,
          text: sentence,
          x: point[0],
          y: point[1]
        });
      });
    });
    return out;
  }

  function cosine(a, b) {
    var dot = a[0] * b[0] + a[1] * b[1];
    var left = Math.hypot(a[0], a[1]) || 1;
    var right = Math.hypot(b[0], b[1]) || 1;
    return dot / (left * right);
  }

  function shares(query, text) {
    var seen = {};
    words(query).forEach(function (word) { seen[word] = 1; });
    return words(text).some(function (word) { return seen[word]; });
  }

  function retrieve(query) {
    var point = embed(query);
    return chunks().map(function (chunk) {
      var score = cosine(point, [chunk.x, chunk.y]);
      var shared = shares(query, chunk.text);
      return {
        id: chunk.id,
        note: chunk.note,
        title: chunk.title,
        text: chunk.text,
        x: chunk.x,
        y: chunk.y,
        score: score,
        shared: shared,
        accept: shared && score >= 0.55
      };
    }).sort(function (a, b) {
      if (a.accept !== b.accept) return a.accept ? -1 : 1;
      return b.score - a.score;
    });
  }

  function tokenize(text) {
    var parts = String(text).match(/[A-Za-z0-9]+|[^\s]/g) || [];
    var out = [];
    parts.forEach(function (part) {
      if (/^[A-Za-z0-9]+$/.test(part) && part.length > 8) {
        for (var i = 0; i < part.length; i += 4) out.push(part.slice(i, i + 4));
      } else {
        out.push(part);
      }
    });
    return out.slice(0, 14);
  }

  function tokenVec(token) {
    var hash = 2166136261;
    var lower = token.toLowerCase();
    var vec = [];
    var i;
    for (i = 0; i < lower.length; i += 1) {
      hash ^= lower.charCodeAt(i);
      hash = Math.imul(hash, 16777619);
    }
    for (i = 0; i < 4; i += 1) {
      hash = Math.imul(hash ^ (hash >>> 16), 2246822519);
      vec.push((((hash >>> 0) % 2000) / 1000) - 1);
    }
    return vec;
  }

  function softmax(row) {
    var max = Math.max.apply(null, row);
    var ex = row.map(function (value) { return Math.exp(value - max); });
    var sum = ex.reduce(function (acc, value) { return acc + value; }, 0) || 1;
    return ex.map(function (value) { return value / sum; });
  }

  function attention(tokens) {
    var dim = 4;
    var scale = Math.sqrt(dim);
    var vectors = tokens.map(tokenVec);
    return tokens.map(function (_token, query) {
      var scores = tokens.map(function (_key, key) {
        if (key > query) return -1e9;
        var dot = 0;
        for (var i = 0; i < dim; i += 1) dot += vectors[query][i] * vectors[key][i];
        return dot / scale;
      });
      return softmax(scores).map(function (value, key) {
        return key > query ? 0 : value;
      });
    });
  }

  function parseCalc(goal) {
    var percent = String(goal).match(/(\d+(?:\.\d+)?)\s*(?:percent|%)\s+of\s+(\d+(?:\.\d+)?)/i);
    if (percent) {
      var value = round((Number(percent[1]) / 100) * Number(percent[2]));
      return { expr: percent[1] + "% of " + percent[2], value: value, shown: percent[1] + "% × " + percent[2] };
    }
    var binary = String(goal).match(/(\d+(?:\.\d+)?)\s*(plus|\+|minus|-|times|\*|divided by|\/)\s*(\d+(?:\.\d+)?)/i);
    if (!binary) return null;
    var left = Number(binary[1]);
    var right = Number(binary[3]);
    var op = binary[2].toLowerCase();
    var symbol = op;
    var answer = 0;
    if (op === "plus" || op === "+") { answer = left + right; symbol = "+"; }
    else if (op === "minus" || op === "-") { answer = left - right; symbol = "−"; }
    else if (op === "times" || op === "*") { answer = left * right; symbol = "×"; }
    else {
      if (right === 0) return null;
      answer = left / right;
      symbol = "÷";
    }
    return { expr: left + " " + symbol + " " + right, value: round(answer), shown: left + " " + symbol + " " + right };
  }

  function callFrame(name, args) {
    return {
      kind: "call",
      title: "Tool call",
      tool: name,
      args: args,
      text: name,
      envelope: { jsonrpc: "2.0", method: "tools/call", params: { name: name, arguments: args } }
    };
  }

  function planAgent(goal) {
    var clean = String(goal || "").trim();
    var frames = [{ kind: "goal", title: "Goal", text: clean || "Write a goal to start the loop." }];
    if (!clean) {
      frames.push({ kind: "answer", title: "Stop", text: "The loop does not invent a goal." });
      return frames;
    }
    var send = /\b(send|email|post|message)\b/i.test(clean);
    var calc = parseCalc(clean);
    var clock = /\b(clock|what time|current time)\b/i.test(clean);
    var best = retrieve(clean)[0];
    var grounded = Boolean(best && best.accept);

    if (calc && !send) {
      frames.push(callFrame("calc", { expr: calc.expr }));
      frames.push({ kind: "observe", title: "Observation", tool: "calc", text: calc.shown + " = " + calc.value });
      frames.push({ kind: "answer", title: "Answer", text: "The calculator returned " + calc.value + ". The answer quotes that result." });
      return frames;
    }
    if (clock && !send && !grounded) {
      frames.push(callFrame("clock", {}));
      frames.push({ kind: "observe", title: "Observation", tool: "clock", text: "09:00 example clock. This is not the time on your machine." });
      frames.push({ kind: "answer", title: "Answer", text: "The example clock says 09:00. A real clock tool would read a clock you chose." });
      return frames;
    }
    if (grounded) {
      frames.push(callFrame("search_notes", { q: clean }));
      frames.push({ kind: "observe", title: "Observation", tool: "search_notes", text: best.id + " — " + best.text });
      if (send) {
        frames.push(callFrame("send_note", { to: "desk", body: best.text }));
        frames.push({
          kind: "gate",
          title: "Permission gate",
          text: "send_note can leave the machine. The simulator blocks it. Nothing is sent. Draft: " + best.text
        });
        frames.push({ kind: "answer", title: "Stop", text: "Draft only. A person sends from their own tool." });
        return frames;
      }
      frames.push({ kind: "answer", title: "Answer", text: best.text + " Source: " + best.id + "." });
      return frames;
    }
    if (send) {
      frames.push(callFrame("send_note", { to: "desk", body: clean }));
      frames.push({
        kind: "gate",
        title: "Permission gate",
        text: "The model asked to send, and no note supports the body. The call is blocked. Nothing is sent."
      });
      frames.push({ kind: "answer", title: "Stop", text: "No send, and no source to draft from." });
      return frames;
    }
    frames.push({
      kind: "answer",
      title: "Refuse",
      text: "No allowlisted tool returned a source. The simulator stops instead of guessing."
    });
    return frames;
  }

  function lora(rank, width) {
    var d = width || 128;
    var r = Math.max(1, Math.min(32, rank));
    var full = d * d;
    var trainable = 2 * d * r;
    return { width: d, rank: r, full: full, trainable: trainable, share: trainable / full };
  }

  function gate(input) {
    var reasons = [];
    if (input.quality < input.qualityBase) reasons.push("Quality is below the baseline.");
    if (input.safety > input.safetyBase) reasons.push("Safety failures are higher than the baseline.");
    if (input.latency > input.latencyBudget) reasons.push("Latency is over the budget.");
    if (input.cost > input.costBudget) reasons.push("Cost is over the budget.");
    return { pass: reasons.length === 0, reasons: reasons };
  }

  return {
    NOTES: NOTES,
    tokenize: tokenize,
    attention: attention,
    embed: embed,
    chunks: chunks,
    retrieve: retrieve,
    planAgent: planAgent,
    lora: lora,
    gate: gate,
    THRESHOLD: 0.55
  };
});

/* Extra offline labs, the quiz, confetti, and the streak. No network. */
(function () {
  function reduceMotion() {
    return document.documentElement.getAttribute("data-motion") === "reduce"
      || window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }
  var booted = false;
  var quizItems = [];
  var quizMode = "practice";
  var quizFilter = "all";
  var quizCursor = 0;
  var quizRevealed = false;
  var bossPicks = {};
  var bossDone = false;

  function byId(id) {
    return document.getElementById(id);
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

  function say(id, text) {
    var node = byId(id);
    if (node) node.textContent = text;
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

  function readStore(key, fallback) {
    try {
      var raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (err) {
      return fallback;
    }
  }

  function writeStore(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (err) { /* ignore */ }
  }

  function dayKey(date) {
    return date.getFullYear() + "-" + String(date.getMonth() + 1).padStart(2, "0") + "-" + String(date.getDate()).padStart(2, "0");
  }

  function streakLength(days) {
    var set = {};
    (days || []).forEach(function (day) { set[day] = 1; });
    var cursor = new Date();
    if (!set[dayKey(cursor)]) {
      cursor.setDate(cursor.getDate() - 1);
      if (!set[dayKey(cursor)]) return 0;
    }
    var count = 0;
    while (set[dayKey(cursor)]) {
      count += 1;
      cursor.setDate(cursor.getDate() - 1);
    }
    return count;
  }

  function paintStreak() {
    var count = streakLength(readStore("ailab-v3-streak", []));
    var node = byId("streakCount");
    var unit = byId("streakUnit");
    if (node) node.textContent = String(count);
    if (unit) unit.textContent = count === 1 ? "day" : "days";
  }

  function noteToday() {
    var days = readStore("ailab-v3-streak", []);
    var today = dayKey(new Date());
    if (days.indexOf(today) === -1) days.push(today);
    writeStore("ailab-v3-streak", days.slice(-60));
    paintStreak();
    document.dispatchEvent(new CustomEvent("campus-progress"));
  }

  function burst() {
    if (reduceMotion()) return;
    var host = byId("confetti");
    if (!host) {
      host = document.createElement("div");
      host.id = "confetti";
      host.className = "confetti";
      host.setAttribute("aria-hidden", "true");
      document.body.appendChild(host);
    }
    host.replaceChildren();
    var colors = ["#6366F1", "#22D3EE", "#34D399", "#FBBF24", "#F8FAFC"];
    for (var i = 0; i < 18; i += 1) {
      var piece = document.createElement("i");
      piece.style.left = (6 + Math.random() * 88) + "%";
      piece.style.background = colors[i % colors.length];
      piece.style.animationDelay = (Math.random() * 0.15) + "s";
      host.appendChild(piece);
    }
    window.setTimeout(function () { host.replaceChildren(); }, 1400);
  }

  function drawProof() {
    var run = byId("proofRun");
    if (!run) return;
    var trace = byId("proofTrace").value.trim();
    var metric = byId("proofMetric").value.trim();
    var artifact = byId("proofArtifact").value.trim();
    var missing = [];
    if (!run.value.trim()) missing.push("a run");
    if (!trace) missing.push("a trace");
    if (!/\d/.test(metric)) missing.push("a metric with a number");
    if (artifact.length < 3) missing.push("an artifact someone can open");
    var out = byId("proofOut");
    out.classList.toggle("is-pass", missing.length === 0);
    out.classList.toggle("is-stop", missing.length > 0);
    out.textContent = missing.length
      ? "Still missing " + missing.join(", ") + "."
      : "The record is complete. Someone else can open the artifact, follow the trace, and read the metric.";
  }

  var TOY = [
    ["the", 2.4],
    ["model", 2.1],
    ["next", 1.6],
    ["token", 1.2],
    ["a", 0.4],
    ["cat", -0.2],
    ["quantum", -1.4]
  ];

  function sampleDist() {
    var temp = Math.max(0.1, Number(byId("sampleTemp").value) || 1);
    var topP = Math.max(0.05, Math.min(1, Number(byId("sampleP").value) || 1));
    var scaled = TOY.map(function (row) { return row[1] / temp; });
    var max = Math.max.apply(null, scaled);
    var exps = scaled.map(function (value) { return Math.exp(value - max); });
    var sum = exps.reduce(function (total, value) { return total + value; }, 0);
    var probs = exps.map(function (value) { return value / sum; });
    var order = probs.map(function (prob, index) { return { index: index, prob: prob }; });
    order.sort(function (a, b) { return b.prob - a.prob; });
    var mass = 0;
    var keep = {};
    order.forEach(function (row) {
      if (mass >= topP && Object.keys(keep).length) return;
      keep[row.index] = 1;
      mass += row.prob;
    });
    var keptMass = probs.reduce(function (total, prob, index) {
      return total + (keep[index] ? prob : 0);
    }, 0);
    return {
      temp: temp,
      topP: topP,
      probs: probs.map(function (prob, index) {
        return { name: TOY[index][0], full: prob, kept: keep[index] ? prob / keptMass : 0, on: Boolean(keep[index]) };
      })
    };
  }

  function drawSample(drawOne) {
    if (!byId("sampleTemp")) return;
    var dist = sampleDist();
    byId("sampleTempOut").textContent = dist.temp.toFixed(1);
    byId("samplePOut").textContent = dist.topP.toFixed(2);
    var bars = byId("sampleBars");
    bars.replaceChildren();
    dist.probs.forEach(function (row) {
      var line = document.createElement("div");
      line.className = "bar-line" + (row.on ? "" : " is-cut");
      var name = document.createElement("span");
      name.textContent = row.name;
      var track = document.createElement("span");
      track.className = "bar-track";
      var fill = document.createElement("i");
      fill.style.width = Math.max(2, row.full * 100) + "%";
      track.appendChild(fill);
      var pct = document.createElement("span");
      pct.textContent = (row.full * 100).toFixed(1) + "%" + (row.on ? "" : " out");
      line.appendChild(name);
      line.appendChild(track);
      line.appendChild(pct);
      bars.appendChild(line);
    });
    var kept = dist.probs.filter(function (row) { return row.on; });
    var greedy = kept.slice().sort(function (a, b) { return b.kept - a.kept; })[0];
    var drawn = greedy;
    if (drawOne && kept.length) {
      var roll = Math.random();
      var cursor = 0;
      for (var i = 0; i < kept.length; i += 1) {
        cursor += kept[i].kept;
        if (roll <= cursor) { drawn = kept[i]; break; }
      }
    }
    say(
      "sampleOut",
      "Temperature " + dist.temp.toFixed(1) + " reshapes the same logits. Top-p " + dist.topP.toFixed(2) +
      " keeps " + kept.length + " of " + dist.probs.length + " tokens. The greedy pick inside that set is “" +
      greedy.name + "”." + (drawOne ? " This draw landed on “" + drawn.name + "”." : " These are toy logits, not a model.")
    );
  }

  var EMBED_POINTS = [
    { id: "refund", x: 0.78, y: 0.68, z: 0.62, text: "Returns are accepted for 30 days." },
    { id: "shipping", x: 0.24, y: 0.74, z: 0.34, text: "Standard shipping takes five days." },
    { id: "hours", x: 0.62, y: 0.22, z: 0.74, text: "The desk is open on weekdays." },
    { id: "invoice", x: 0.26, y: 0.28, z: 0.4, text: "Invoices list the order id." }
  ];
  var queryPoint = { x: 0.7, y: 0.6, z: 0.55 };
  var embedSync = false;

  function cosine(a, b) {
    var dot = 0;
    var na = 0;
    var nb = 0;
    for (var i = 0; i < a.length; i += 1) {
      dot += a[i] * b[i];
      na += a[i] * a[i];
      nb += b[i] * b[i];
    }
    na = Math.sqrt(na);
    nb = Math.sqrt(nb);
    if (na < 0.04 || nb < 0.04) return null;
    return dot / (na * nb);
  }

  function embedScores() {
    var z = queryPoint.z == null ? 0.55 : queryPoint.z;
    var q = [queryPoint.x - 0.5, queryPoint.y - 0.5, z - 0.5];
    return EMBED_POINTS.map(function (point) {
      var score = cosine(q, [point.x - 0.5, point.y - 0.5, (point.z || 0.5) - 0.5]);
      return { id: point.id, text: point.text, x: point.x, y: point.y, score: score };
    }).sort(function (a, b) {
      var left = a.score === null ? -2 : a.score;
      var right = b.score === null ? -2 : b.score;
      return right - left;
    });
  }

  function syncEmbedSliders() {
    embedSync = true;
    [
      ["embedX", queryPoint.x],
      ["embedY", queryPoint.y],
      ["embedZ", queryPoint.z == null ? 0.55 : queryPoint.z]
    ].forEach(function (pair) {
      var node = byId(pair[0]);
      if (!node) return;
      var next = String(Math.round(pair[1] * 100));
      if (node.value !== next) {
        node.value = next;
        node.dispatchEvent(new Event("input", { bubbles: true }));
        node.dispatchEvent(new Event("change", { bubbles: true }));
      }
    });
    embedSync = false;
  }

  function drawEmbed() {
    syncEmbedSliders();
    if (window.CampusSpace && window.CampusSpace.hasEmbed && window.CampusSpace.hasEmbed()) {
      window.CampusSpace.setEmbedQuery(queryPoint.x, queryPoint.y, queryPoint.z == null ? 0.55 : queryPoint.z);
    }
    var canvas = byId("embedCanvas");
    if (!canvas) {
      paintEmbedReadout();
      return;
    }
    var useFlat = !(window.CampusSpace && window.CampusSpace.hasEmbed && window.CampusSpace.hasEmbed());
    canvas.hidden = !useFlat;
    if (!useFlat) {
      paintEmbedReadout();
      return;
    }
    var view = fitCanvas(canvas);
    var ctx = view.ctx;
    var colors = ink();
    ctx.clearRect(0, 0, view.w, view.h);
    ctx.strokeStyle = colors.line;
    ctx.strokeRect(16, 12, view.w - 32, view.h - 24);
    function xy(x, y) {
      return [16 + x * (view.w - 32), 12 + y * (view.h - 24)];
    }
    var ranked = embedScores();
    var best = ranked[0];
    EMBED_POINTS.forEach(function (point) {
      var pos = xy(point.x, point.y);
      ctx.fillStyle = best && point.id === best.id ? colors.green : colors.primary;
      ctx.beginPath();
      ctx.arc(pos[0], pos[1], 7, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = colors.ink;
      ctx.font = "12px system-ui, sans-serif";
      ctx.fillText(point.id, pos[0] + 10, pos[1] - 8);
    });
    var qpos = xy(queryPoint.x, queryPoint.y);
    ctx.fillStyle = colors.amber;
    ctx.beginPath();
    ctx.arc(qpos[0], qpos[1], 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = colors.amber;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(view.w / 2, view.h / 2);
    ctx.lineTo(qpos[0], qpos[1]);
    ctx.stroke();
    ctx.setLineDash([]);
    paintEmbedReadout();
  }

  function paintEmbedReadout() {
    var ranked = embedScores();
    var best = ranked[0];
    var line = ranked.map(function (row) {
      return row.id + " " + (row.score === null ? "—" : row.score.toFixed(2));
    }).join(" · ");
    var verdict = "Move the amber point off the center.";
    if (best && best.score !== null) {
      verdict = "Nearest is " + best.id + " at cosine " + best.score.toFixed(2) + ". " +
        (best.score >= 0.75 ? "Close enough to cite " + best.id + ". " + best.text : "Below 0.75, so this toy index would refuse rather than guess.");
    }
    say("embedOut", verdict + " " + line);
    var canvas = byId("embedCanvas");
    if (canvas) canvas.setAttribute("aria-label", verdict);
    var mount = byId("embedMount");
    if (mount) {
      var live = mount.querySelector("canvas");
      if (live) live.setAttribute("aria-label", verdict);
    }
  }

  function pointFromEvent(canvas, event) {
    var rect = canvas.getBoundingClientRect();
    var x = (event.clientX - rect.left) / rect.width;
    var y = (event.clientY - rect.top) / rect.height;
    queryPoint.x = Math.max(0.02, Math.min(0.98, x));
    queryPoint.y = Math.max(0.02, Math.min(0.98, y));
    drawEmbed();
  }

  function diffWords(a, b) {
    var left = a.trim().split(/\s+/).filter(Boolean).slice(0, 80);
    var right = b.trim().split(/\s+/).filter(Boolean).slice(0, 80);
    var n = left.length;
    var m = right.length;
    var dp = [];
    for (var i = 0; i <= n; i += 1) {
      dp[i] = [];
      for (var j = 0; j <= m; j += 1) dp[i][j] = 0;
    }
    for (i = n - 1; i >= 0; i -= 1) {
      for (j = m - 1; j >= 0; j -= 1) {
        dp[i][j] = left[i] === right[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
      }
    }
    var removed = [];
    var added = [];
    i = 0;
    j = 0;
    while (i < n && j < m) {
      if (left[i] === right[j]) { i += 1; j += 1; }
      else if (dp[i + 1][j] >= dp[i][j + 1]) { removed.push(left[i]); i += 1; }
      else { added.push(right[j]); j += 1; }
    }
    while (i < n) { removed.push(left[i]); i += 1; }
    while (j < m) { added.push(right[j]); j += 1; }
    return { removed: removed, added: added };
  }

  function promptFlags(text) {
    return {
      job: /\bjob\b|\btask\b|answer the/i.test(text),
      input: /\binput\b|policy note|\bsource\b/i.test(text),
      done: /done-check|cites|must state/i.test(text),
      bound: /do not|only/i.test(text)
    };
  }

  function drawPrompt() {
    var a = byId("promptA");
    if (!a) return;
    var b = byId("promptB");
    var diff = diffWords(a.value, b.value);
    var host = byId("promptDiff");
    host.replaceChildren();
    function line(label, words, kind) {
      var row = document.createElement("p");
      var strong = document.createElement("strong");
      strong.textContent = label;
      row.appendChild(strong);
      if (!words.length) {
        row.appendChild(document.createTextNode(" No word-level change."));
      } else {
        words.forEach(function (word) {
          var mark = document.createElement("span");
          mark.className = kind;
          mark.textContent = word;
          row.appendChild(document.createTextNode(" "));
          row.appendChild(mark);
        });
      }
      host.appendChild(row);
    }
    line("Only in A.", diff.removed, "is-del");
    line("Only in B.", diff.added, "is-add");
    var checks = byId("promptChecks");
    checks.replaceChildren();
    var flagsA = promptFlags(a.value);
    var flagsB = promptFlags(b.value);
    [
      ["job", "Names the job"],
      ["input", "Names the input"],
      ["done", "Names a done-check"],
      ["bound", "Names a boundary"]
    ].forEach(function (pair) {
      var item = document.createElement("li");
      var left = flagsA[pair[0]] ? "A yes" : "A no";
      var right = flagsB[pair[0]] ? "B yes" : "B no";
      item.textContent = pair[1] + ": " + left + ", " + right;
      item.className = flagsB[pair[0]] && !flagsA[pair[0]] ? "is-add" : "";
      checks.appendChild(item);
    });
    var gained = ["job", "input", "done", "bound"].filter(function (key) { return flagsB[key] && !flagsA[key]; }).length;
    say("promptOut", gained
      ? "B adds " + gained + " of the four checks A is missing. Change one of those, then score the same tasks again."
      : "The two prompts do not yet differ on job, input, done-check, and boundary. Add one of those to B and compare again.");
  }

  function drawFit() {
    var slider = byId("fitB");
    if (!slider) return;
    var billions = Number(slider.value);
    var bits = Number(byId("fitBits").value);
    byId("fitBOut").textContent = String(billions);
    var gb = billions * bits / 8;
    var room = [8, 16, 24, 48].filter(function (size) { return gb < size * 0.7; });
    say(
      "fitOut",
      billions + " billion parameters at " + bits + " bits is about " + gb.toFixed(1) +
      " GB of weights. Context and the runtime need more than the weight file. " +
      (room.length ? "Weights leave headroom on " + room.join(", ") + " GB." : "Weights alone are tight for 8, 16, 24, and 48 GB. Pick a smaller file or more memory.")
    );
  }

  function money(value) {
    if (value >= 1) return "$" + value.toFixed(2);
    if (value >= 0.01) return "$" + value.toFixed(3);
    return "$" + value.toFixed(4);
  }

  function drawCost() {
    if (!byId("costIn")) return;
    var input = Math.max(0, Number(byId("costIn").value) || 0);
    var output = Math.max(0, Number(byId("costOutTok").value) || 0);
    var pin = Math.max(0, Number(byId("costPin").value) || 0);
    var pout = Math.max(0, Number(byId("costPout").value) || 0);
    var ms = Math.max(0, Number(byId("costMs").value) || 0);
    var calls = Math.max(0, Number(byId("costCalls").value) || 0);
    var cached = byId("costCache").checked;
    var billedIn = cached ? input * 0.28 : input;
    var call = (billedIn / 1e6) * pin + (output / 1e6) * pout;
    var plain = (input / 1e6) * pin + (output / 1e6) * pout;
    var latency = (output / 1000) * ms;
    say(
      "costRead",
      "One call is " + money(cached ? call : plain) + (cached ? " with the toy cache (80% of input at a tenth of the rate). Without it, " + money(plain) + "." : ".") +
      " " + calls + " calls in a day come to " + money((cached ? call : plain) * calls) +
      ". Output latency is about " + Math.round(latency) + " ms. These rates are toys, not a vendor price."
    );
  }

  var PACK = [
    { id: "system", name: "System rules", cost: 18 },
    { id: "user", name: "User question", cost: 12 },
    { id: "policy", name: "Refund policy", cost: 28 },
    { id: "catalog", name: "Unrelated catalog", cost: 36 },
    { id: "history", name: "Old turns", cost: 30 },
    { id: "reserve", name: "Answer reserve", cost: 20 }
  ];
  var packed = { system: 1, user: 1, policy: 1, catalog: 1, history: 1, reserve: 1 };

  function drawPack() {
    var board = byId("contextBoard");
    if (!board) return;
    var total = PACK.reduce(function (sum, piece) { return sum + (packed[piece.id] ? piece.cost : 0); }, 0);
    board.replaceChildren();
    PACK.forEach(function (piece) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "pack" + (packed[piece.id] ? " is-on" : "");
      button.setAttribute("aria-pressed", packed[piece.id] ? "true" : "false");
      button.textContent = piece.name + " · " + piece.cost;
      button.addEventListener("click", function () {
        packed[piece.id] = packed[piece.id] ? 0 : 1;
        drawPack();
      });
      board.appendChild(button);
    });
    var meter = byId("contextMeter");
    meter.style.width = Math.min(100, total) + "%";
    meter.classList.toggle("is-over", total > 100);
    var needed = packed.user && packed.policy && packed.reserve;
    var over = total > 100;
    var out = byId("contextOut");
    out.classList.toggle("is-pass", needed && !over);
    out.classList.toggle("is-stop", !needed || over);
    if (over) out.textContent = total + " of 100. Over budget. Drop the catalog or the old turns before you keep the policy.";
    else if (!needed) out.textContent = total + " of 100 and inside the window, but the question, the policy, or the answer reserve is missing.";
    else out.textContent = total + " of 100. Packed. The question, the policy, and room for the answer fit.";
  }

  var VDB = [
    { id: "refund", x: 0.72, y: 0.7 },
    { id: "policy", x: 0.8, y: 0.58 },
    { id: "shipping", x: 0.22, y: 0.74 },
    { id: "hours", x: 0.7, y: 0.2 },
    { id: "invoice", x: 0.28, y: 0.24 },
    { id: "catalog", x: 0.48, y: 0.48 }
  ];
  var vdbQuery = { x: 0.76, y: 0.64 };
  var vdbMode = "grid";

  function cellOf(value) {
    return Math.max(0, Math.min(3, Math.floor(value * 4)));
  }

  function drawVdb() {
    var canvas = byId("vdbCanvas");
    if (!canvas) return;
    var view = fitCanvas(canvas);
    var ctx = view.ctx;
    var colors = ink();
    ctx.clearRect(0, 0, view.w, view.h);
    var left = 16;
    var top = 12;
    var size = Math.min(view.w - 32, view.h - 24);
    var step = size / 4;
    var qx = cellOf(vdbQuery.x);
    var qy = cellOf(vdbQuery.y);
    for (var gy = 0; gy < 4; gy += 1) {
      for (var gx = 0; gx < 4; gx += 1) {
        var near = Math.max(Math.abs(gx - qx), Math.abs(gy - qy)) <= 1;
        ctx.fillStyle = vdbMode === "grid" && near ? "rgba(34,211,238,0.16)" : "transparent";
        ctx.fillRect(left + gx * step, top + gy * step, step, step);
        ctx.strokeStyle = colors.line;
        ctx.strokeRect(left + gx * step, top + gy * step, step, step);
      }
    }
    function visited(point) {
      if (vdbMode === "flat") return true;
      return Math.max(Math.abs(cellOf(point.x) - qx), Math.abs(cellOf(point.y) - qy)) <= 1;
    }
    var seen = 0;
    VDB.forEach(function (point) {
      var on = visited(point);
      if (on) seen += 1;
      var px = left + point.x * size;
      var py = top + point.y * size;
      ctx.globalAlpha = on ? 1 : 0.28;
      ctx.fillStyle = colors.primary;
      ctx.beginPath();
      ctx.arc(px, py, 6, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = 1;
      ctx.fillStyle = colors.muted;
      ctx.font = "11px system-ui, sans-serif";
      ctx.fillText(point.id, px + 8, py - 6);
    });
    var qpx = left + vdbQuery.x * size;
    var qpy = top + vdbQuery.y * size;
    ctx.fillStyle = colors.amber;
    ctx.beginPath();
    ctx.arc(qpx, qpy, 7, 0, Math.PI * 2);
    ctx.fill();
    if (byId("vdbX")) byId("vdbX").value = String(Math.round(vdbQuery.x * 100));
    if (byId("vdbY")) byId("vdbY").value = String(Math.round(vdbQuery.y * 100));
    var label = vdbMode === "flat"
      ? "Flat scan visits every point (" + seen + " of " + VDB.length + ")."
      : "The grid visits the query cell and its neighbors (" + seen + " of " + VDB.length + ").";
    say("vdbOut", label + " A real index makes the same trade: fewer reads, and a risk of missing a neighbor just outside the cells you opened.");
    canvas.setAttribute("aria-label", label);
  }

  function setVdbFromEvent(canvas, event) {
    var rect = canvas.getBoundingClientRect();
    var viewW = canvas.clientWidth || rect.width;
    var viewH = Number(canvas.getAttribute("height")) || 280;
    var h = viewH * (viewW / 880);
    var left = 16;
    var top = 12;
    var size = Math.min(viewW - 32, h - 24);
    var x = (event.clientX - rect.left) / rect.width * viewW;
    var y = (event.clientY - rect.top) / rect.height * h;
    vdbQuery.x = Math.max(0.02, Math.min(0.98, (x - left) / size));
    vdbQuery.y = Math.max(0.02, Math.min(0.98, (y - top) / size));
    drawVdb();
  }

  var SCHEMA = {
    name: "lookup_note",
    topics: { refund: 1, shipping: 1, hours: 1 }
  };

  function validateCall(text) {
    var parsed;
    try { parsed = JSON.parse(text); }
    catch (err) { return ["The text is not JSON."]; }
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) return ["The value has to be an object."];
    var errors = [];
    if (parsed.name !== SCHEMA.name) errors.push("name has to be lookup_note.");
    var keys = Object.keys(parsed);
    keys.forEach(function (key) {
      if (key !== "name" && key !== "arguments") errors.push("Unexpected key “" + key + "”.");
    });
    var args = parsed.arguments;
    if (!args || typeof args !== "object" || Array.isArray(args)) errors.push("arguments has to be an object.");
    else {
      if (!Object.prototype.hasOwnProperty.call(args, "topic")) errors.push("arguments.topic is required.");
      Object.keys(args).forEach(function (key) {
        if (key !== "topic") errors.push("Unexpected argument “" + key + "”.");
      });
      if (args.topic && !SCHEMA.topics[args.topic]) errors.push("topic has to be refund, shipping, or hours.");
    }
    return errors;
  }

  function drawSchema() {
    var input = byId("schemaInput");
    if (!input) return;
    var errors = validateCall(input.value);
    var out = byId("schemaOut");
    out.classList.toggle("is-pass", errors.length === 0);
    out.classList.toggle("is-stop", errors.length > 0);
    out.textContent = errors.length
      ? "Rejected. " + errors.join(" ")
      : "Accepted. The handler may run lookup_note with that topic. The model does not get to skip this check.";
  }

  function handoffFrames(goal) {
    if (/phone|password|secret/i.test(goal)) {
      return [
        ["Researcher", "No note contains that fact. Artifact: an empty source list."],
        ["Writer", "Handoff rejected. There is no source, so the writer must not invent one."],
        ["Reviewer", "Stop. A handoff without a source is not an answer."]
      ];
    }
    return [
      ["Researcher", "Found policy-refund. Artifact: the note id and the sentence that says 30 days."],
      ["Writer", "Draft cites policy-refund and states 30 days. It adds no new fact."],
      ["Reviewer", "Accept. The citation matches the artifact the researcher passed."]
    ];
  }

  var handStep = 0;

  function drawHandoff() {
    var goal = byId("handoffGoal");
    var list = byId("handoffTrace");
    if (!goal || !list) return;
    var frames = handoffFrames(goal.value);
    if (handStep >= frames.length) handStep = frames.length - 1;
    list.replaceChildren();
    frames.slice(0, handStep + 1).forEach(function (frame) {
      var item = document.createElement("li");
      var title = document.createElement("b");
      title.textContent = frame[0];
      var body = document.createElement("p");
      body.textContent = frame[1];
      item.appendChild(title);
      item.appendChild(body);
      list.appendChild(item);
    });
    say("handoffOut", "Step " + (handStep + 1) + " of " + frames.length + ". " + frames[handStep][0] + ": " + frames[handStep][1]);
  }

  function drawMcp() {
    var picked = document.querySelector("input[name='mcpTool']:checked");
    var approved = byId("mcpApprove") && byId("mcpApprove").checked;
    var out = byId("mcpOut");
    if (!picked || !out) return;
    var map = {
      read_note: ["Allow", "Read is granted. The result comes back as an observation, not as a new instruction."],
      draft_mail: approved
        ? ["Ask", "A person approved the draft. It is still not a send."]
        : ["Ask", "A draft can be prepared. Sending still waits until a person checks this box."],
      send_mail: ["Deny", "Send is not granted. The client refuses before a server runs it."]
    };
    var row = map[picked.value] || ["Deny", "Unknown tool."];
    out.classList.toggle("is-pass", row[0] === "Allow" || (picked.value === "draft_mail" && approved));
    out.classList.toggle("is-stop", row[0] === "Deny" || (picked.value === "draft_mail" && !approved));
    out.textContent = row[0] + ". " + row[1];
  }

  var reviewSecret = true;
  var reviewTest = false;

  function drawReview() {
    var diff = byId("reviewDiff");
    var out = byId("reviewOut");
    if (!diff || !out) return;
    var lines = ["diff -- a task", "+ def refund_days():", "+     return 30"];
    if (reviewSecret) lines.push("+ TOKEN = \"toy-not-real\"");
    lines.push(reviewTest ? "# tests: refund_days checked, result 30" : "# tests: not run");
    diff.textContent = lines.join("\n");
    var ready = !reviewSecret && reviewTest;
    out.classList.toggle("is-pass", ready);
    out.classList.toggle("is-stop", !ready);
    if (ready) out.textContent = "Ready for a person to read. The secret line is gone and the test is named.";
    else out.textContent = "Not ready." + (reviewSecret ? " A secret is still in the diff." : "") + (reviewTest ? "" : " The test has not been run.");
  }

  function drawDecide() {
    if (!byId("decideGap")) return;
    var gap = byId("decideGap").value;
    var source = byId("decideSource").value;
    var failed = byId("decideFailed").value;
    var licensed = byId("decideLicense").value;
    var pick = "Prompt";
    var why = "You have not shown that a cheaper fix failed. Write the job, the shape, and the done-check, then score it.";
    if (gap === "tool") {
      pick = "Prompt plus a tool";
      why = "The gap is an action or a calculation. A tool returns the value. Training does not add a live clock.";
    } else if (gap === "fact" || source === "yes") {
      pick = "Retrieval";
      why = "The answer has to come from a source you can cite. An adapter does not keep that passage current.";
    } else if (gap === "style" && failed === "yes" && licensed === "yes") {
      pick = "Fine-tune";
      why = "Prompting failed a measured eval, the gap is a behavior the prompt cannot hold, and the data is licensed for training.";
    } else if (gap === "style" && failed === "yes") {
      pick = "Prompt";
      why = "The data is not licensed for training. Stay with the prompt and collect a set you are allowed to use.";
    }
    say("decideOut", pick + ". " + why);
  }

  function guardOf(text) {
    var value = text.toLowerCase();
    if (/ignore (the |all |previous )|disregard|reveal the (system|hidden)|print the hidden/.test(value)) {
      return ["Instruction override", "Refused. Untrusted text stays data. The instructions do not change because a passage says so."];
    }
    if (/password|api key|secret|system prompt|hidden key/.test(value)) {
      return ["Secret request", "Refused. The reply does not include a secret, a key, or a hidden instruction."];
    }
    if (/\b(send|delete|wire|pay|charge)\b/.test(value)) {
      return ["Side effect", "Refused. Sending, paying, and deleting wait for a person."];
    }
    return ["None", "No rule fired. The text can be handled as data. The answer still has to come from a source or a tool."];
  }

  function drawGuard() {
    var input = byId("guardInput");
    var out = byId("guardOut");
    if (!input || !out) return;
    var row = guardOf(input.value);
    out.classList.toggle("is-pass", row[0] === "None");
    out.classList.toggle("is-stop", row[0] !== "None");
    out.textContent = "Rule: " + row[0] + ". " + row[1];
  }

  function drawSpec() {
    var metric = (byId("specMetric") && byId("specMetric").value || "").trim();
    var fields = ["specUser", "specJob", "specNon"].map(function (id) { return (byId(id).value || "").trim(); });
    var out = byId("specOut");
    if (!out) return;
    var vibe = /feel|vibe|nice|good|better/i.test(metric) && !/\d|%|percent|test/i.test(metric);
    var missing = [];
    if (!fields[0]) missing.push("the user");
    if (!fields[1]) missing.push("the job");
    if (!metric) missing.push("the metric");
    if (!fields[2]) missing.push("a non-goal");
    out.classList.toggle("is-pass", !missing.length && !vibe);
    out.classList.toggle("is-stop", Boolean(missing.length) || vibe);
    if (missing.length) out.textContent = "Still missing " + missing.join(", ") + ".";
    else if (vibe) out.textContent = "The metric is a vibe. Name a test or a number both sides can apply.";
    else out.textContent = "The spec names a person, a job, a metric, and something this feature will not do.";
  }

  function drawCap() {
    var boxes = Array.prototype.slice.call(document.querySelectorAll(".cap-check"));
    if (!boxes.length) return;
    var done = boxes.filter(function (box) { return box.checked; }).length;
    var out = byId("capOut");
    out.classList.toggle("is-pass", done === boxes.length);
    out.classList.toggle("is-stop", done !== boxes.length);
    out.textContent = done === boxes.length
      ? "Ready to demo. Tests, a build log, a ten-minute script, and a scorecard are all on the list."
      : done + " of " + boxes.length + " are checked. The demo waits on the rest.";
  }

  var quizLoading = null;

  function loadQuiz() {
    if (quizItems.length) return Promise.resolve(quizItems);
    if (quizLoading) return quizLoading;
    var node = byId("quizData");
    if (node && (node.textContent || "").trim()) {
      try { quizItems = JSON.parse(node.textContent); } catch (err) { quizItems = []; }
      return Promise.resolve(quizItems);
    }
    quizLoading = fetch("assets/curriculum/quiz.json").then(function (res) {
      if (!res.ok) throw new Error("quiz");
      return res.json();
    }).then(function (data) {
      quizItems = data.questions || [];
      return quizItems;
    }).catch(function () {
      quizLoading = null;
      quizItems = [];
      return quizItems;
    });
    return quizLoading;
  }

  function quizQueue() {
    if (quizMode === "boss") {
      return quizItems.filter(function (item) { return item.boss; }).slice().sort(function (a, b) {
        if (a.incident === b.incident) return a.step - b.step;
        return a.incident < b.incident ? -1 : 1;
      });
    }
    if (quizFilter === "all") return quizItems.slice();
    return quizItems.filter(function (item) { return item.track === quizFilter; });
  }

  function practiceMarks() {
    return readStore("ailab-v3-quiz-progress", {});
  }

  function paintQuizScores(queue) {
    var host = byId("quizScores");
    if (!host) return;
    var marks = practiceMarks();
    var groups = {};
    var pool = quizMode === "boss" ? queue : quizItems;
    pool.forEach(function (item) {
      if (!groups[item.track]) groups[item.track] = { name: item.trackName, n: 0, hit: 0, seen: 0 };
      var row = groups[item.track];
      row.n += 1;
      if (quizMode === "boss") {
        if (bossDone && Object.prototype.hasOwnProperty.call(bossPicks, item.id)) {
          row.seen += 1;
          if (bossPicks[item.id] === item.answer) row.hit += 1;
        }
      } else if (Object.prototype.hasOwnProperty.call(marks, item.id)) {
        row.seen += 1;
        if (marks[item.id]) row.hit += 1;
      }
    });
    host.replaceChildren();
    Object.keys(groups).sort().forEach(function (track) {
      var row = groups[track];
      var item = document.createElement("li");
      item.textContent = row.name + ": " + row.hit + " correct of " + row.seen + " answered (" + row.n + " in the bank)";
      host.appendChild(item);
    });
  }

  function passLine(total) {
    return Math.ceil(total * 0.8);
  }

  function citeLine(item) {
    if (!item.cite || !item.cite.url) return null;
    var line = document.createElement("p");
    line.className = "quiz-cite";
    var link = document.createElement("a");
    link.href = item.cite.url;
    link.textContent = item.cite.title;
    line.appendChild(document.createTextNode("Source: "));
    line.appendChild(link);
    return line;
  }

  function paintQuiz() {
    var card = byId("quizCard");
    if (!card) return;
    if (!quizItems.length) {
      var progressWait = byId("quizProgress");
      if (progressWait) progressWait.textContent = "Loading the question bank.";
      loadQuiz().then(function (rows) {
        if (!rows.length) {
          if (progressWait) progressWait.textContent = "The question bank did not load.";
          return;
        }
        paintQuiz();
      });
      return;
    }
    var queue = quizQueue();
    if (quizCursor >= queue.length) quizCursor = 0;
    var progress = byId("quizProgress");
    var why = byId("quizWhy");
    var next = byId("quizNext");
    var check = byId("quizCheck");
    var finish = byId("quizFinish");
    card.replaceChildren();
    if (!queue.length) {
      progress.textContent = "No questions in this slice.";
      return;
    }
    if (quizMode === "boss" && bossDone) {
      var correct = queue.filter(function (item) { return bossPicks[item.id] === item.answer; }).length;
      var line = passLine(queue.length);
      var passed = correct >= line;
      progress.textContent = correct + " of " + queue.length + ". " + (passed ? "Pass. " + line + " was the line." : "Not yet. " + line + " of " + queue.length + " is the line. The reasons are below.");
      var seenIncident = "";
      queue.forEach(function (item) {
        if (item.incident && item.incident !== seenIncident) {
          seenIncident = item.incident;
          var heading = document.createElement("h3");
          heading.textContent = item.incidentTitle;
          card.appendChild(heading);
          if (item.case) {
            var situation = document.createElement("p");
            situation.textContent = item.case;
            card.appendChild(situation);
          }
        }
        var block = document.createElement("article");
        block.className = "quiz-review " + (bossPicks[item.id] === item.answer ? "is-right" : "is-wrong");
        var title = document.createElement("strong");
        title.textContent = "Step " + item.step + ". " + item.q;
        var body = document.createElement("p");
        body.textContent = item.why;
        block.appendChild(title);
        block.appendChild(body);
        var cited = citeLine(item);
        if (cited) block.appendChild(cited);
        card.appendChild(block);
      });
      if (why) why.hidden = true;
      if (check) check.hidden = true;
      if (next) next.hidden = true;
      var prevDone = byId("quizPrev");
      if (prevDone) prevDone.hidden = true;
      if (finish) finish.hidden = true;
      paintQuizScores(queue);
      return;
    }
    var item = queue[quizCursor];
    if (quizMode === "boss" && item.incident) {
      var incidents = [];
      queue.forEach(function (row) {
        if (incidents.indexOf(row.incident) === -1) incidents.push(row.incident);
      });
      progress.textContent = "Incident " + (incidents.indexOf(item.incident) + 1) + " of " + incidents.length + " · Step " + item.step + " of " + item.steps + " · " + item.incidentTitle;
      var situation = document.createElement("p");
      situation.className = "quiz-case";
      situation.textContent = item.case;
      card.appendChild(situation);
    } else {
      progress.textContent = "Question " + (quizCursor + 1) + " of " + queue.length + " · " + item.trackName + " · " + item.kind;
    }
    var legend = document.createElement("p");
    legend.className = "quiz-q";
    legend.textContent = item.q;
    card.appendChild(legend);
    var cited = citeLine(item);
    if (cited) card.appendChild(cited);
    item.choices.forEach(function (choice, index) {
      var label = document.createElement("label");
      var input = document.createElement("input");
      input.type = "radio";
      input.name = "quizPick";
      input.value = String(index);
      if (quizMode === "boss" && bossPicks[item.id] === index) input.checked = true;
      label.appendChild(input);
      label.appendChild(document.createTextNode(" " + choice));
      card.appendChild(label);
    });
    var marks = practiceMarks();
    var showWhy = quizMode === "practice" && quizRevealed;
    if (why) {
      why.hidden = !showWhy;
      why.textContent = showWhy ? item.why : "";
    }
    if (showWhy) {
      var picked = marks[item.id] ? item.answer : -1;
      card.classList.toggle("is-right", marks[item.id] === 1);
      card.classList.toggle("is-wrong", marks[item.id] === 0);
    } else {
      card.classList.remove("is-right", "is-wrong");
    }
    if (check) {
      check.hidden = false;
      check.textContent = quizMode === "boss" ? "Save answer" : "Check";
    }
    if (next) next.hidden = false;
    var prevBtn = byId("quizPrev");
    if (prevBtn) prevBtn.hidden = false;
    if (finish) finish.hidden = quizMode !== "boss";
    void picked;
    paintQuizScores(queue);
  }

  function checkQuiz() {
    var queue = quizQueue();
    var item = queue[quizCursor];
    if (!item) return;
    var picked = document.querySelector("#quizCard input:checked");
    if (!picked) {
      say("quizProgress", "Choose an answer first. Question " + (quizCursor + 1) + " of " + queue.length + ".");
      return;
    }
    var index = Number(picked.value);
    if (quizMode === "boss") {
      bossPicks[item.id] = index;
      if (quizCursor < queue.length - 1) quizCursor += 1;
      paintQuiz();
      return;
    }
    var marks = practiceMarks();
    marks[item.id] = index === item.answer ? 1 : 0;
    writeStore("ailab-v3-quiz-progress", marks);
    var best = 0;
    Object.keys(marks).forEach(function (key) { best += marks[key] ? 1 : 0; });
    try { localStorage.setItem("ailab-v3-quiz-best", String(best)); } catch (err) { /* ignore */ }
    quizRevealed = true;
    paintQuiz();
    if (window.CampusSettings) window.CampusSettings.play(index === item.answer ? "ok" : "no");
    document.dispatchEvent(new CustomEvent("campus-progress"));
  }

  function finishBoss() {
    var queue = quizQueue();
    var unanswered = queue.filter(function (item) { return !Object.prototype.hasOwnProperty.call(bossPicks, item.id); }).length;
    if (unanswered) {
      say("quizProgress", unanswered + " boss questions still need an answer. Use Check to record this one, then move through the rest.");
      return;
    }
    var correct = queue.filter(function (item) { return bossPicks[item.id] === item.answer; }).length;
    bossDone = true;
    var passed = correct >= passLine(queue.length);
    try { localStorage.setItem("ailab-v3-boss", passed ? "pass" : "fail"); } catch (err) { /* ignore */ }
    try { localStorage.setItem("ailab-v3-boss-score", String(correct)); } catch (err) { /* ignore */ }
    if (passed) burst();
    paintQuiz();
    document.dispatchEvent(new CustomEvent("campus-progress"));
  }

  function bootQuizChrome() {
    var track = byId("quizTrack");
    if (track && !track.dataset.ready) {
      track.dataset.ready = "1";
      loadQuiz().then(function () {
      var seen = {};
      quizItems.forEach(function (item) {
        if (seen[item.track]) return;
        seen[item.track] = item.trackName;
      });
      Object.keys(seen).sort().forEach(function (id) {
        var option = document.createElement("option");
        option.value = id;
        option.textContent = seen[id];
        track.appendChild(option);
      });
      track.addEventListener("change", function () {
        quizFilter = track.value;
        quizCursor = 0;
        quizRevealed = false;
        paintQuiz();
      });
      });
    }
    Array.prototype.forEach.call(document.querySelectorAll("[data-quiz-mode]"), function (button) {
      if (button.dataset.bound) return;
      button.dataset.bound = "1";
      button.addEventListener("click", function () {
        quizMode = button.getAttribute("data-quiz-mode");
        quizCursor = 0;
        quizRevealed = false;
        bossPicks = {};
        bossDone = false;
        Array.prototype.forEach.call(document.querySelectorAll("[data-quiz-mode]"), function (other) {
          other.setAttribute("aria-pressed", other === button ? "true" : "false");
        });
        if (track) track.disabled = quizMode === "boss";
        paintQuiz();
      });
    });
    var check = byId("quizCheck");
    var next = byId("quizNext");
    var prev = byId("quizPrev");
    var finish = byId("quizFinish");
    if (check && !check.dataset.bound) {
      check.dataset.bound = "1";
      check.addEventListener("click", checkQuiz);
    }
    function stepQuiz(delta) {
      var queue = quizQueue();
      quizCursor = queue.length ? (quizCursor + delta + queue.length) % queue.length : 0;
      var current = queue[quizCursor];
      quizRevealed = quizMode === "practice" && current && Object.prototype.hasOwnProperty.call(practiceMarks(), current.id);
      paintQuiz();
    }
    if (next && !next.dataset.bound) {
      next.dataset.bound = "1";
      next.addEventListener("click", function () { stepQuiz(1); });
    }
    if (prev && !prev.dataset.bound) {
      prev.dataset.bound = "1";
      prev.addEventListener("click", function () { stepQuiz(-1); });
    }
    if (finish && !finish.dataset.bound) {
      finish.dataset.bound = "1";
      finish.addEventListener("click", finishBoss);
    }
  }

  var drawers = {
    proof: function () { drawProof(); },
    sample: function () { drawSample(false); },
    embed: drawEmbed,
    prompt: drawPrompt,
    fit: drawFit,
    cost: drawCost,
    context: drawPack,
    vdb: drawVdb,
    schema: drawSchema,
    handoff: drawHandoff,
    mcp: drawMcp,
    review: drawReview,
    decide: drawDecide,
    guard: drawGuard,
    spec: drawSpec,
    cap: drawCap,
    quiz: paintQuiz
  };

  var rpcStep = 0;
  var rpcTimer = 0;
  var rpcFrames = [
    {
      title: "initialize",
      dir: "client → server",
      body: {
        jsonrpc: "2.0",
        id: 1,
        method: "initialize",
        params: {
          protocolVersion: "2025-06-18",
          capabilities: {},
          clientInfo: { name: "ai-lab", version: "2026.10" }
        }
      }
    },
    {
      title: "initialize result",
      dir: "server → client",
      body: {
        jsonrpc: "2.0",
        id: 1,
        result: {
          protocolVersion: "2025-06-18",
          capabilities: { tools: { listChanged: false } },
          serverInfo: { name: "lab.tools", version: "2026.10" },
          instructions: "Read notes. Drafts need a person. Sending is denied."
        }
      }
    },
    {
      title: "initialized",
      dir: "client → server",
      body: { jsonrpc: "2.0", method: "notifications/initialized" }
    },
    {
      title: "tools/list",
      dir: "client → server",
      body: { jsonrpc: "2.0", id: 2, method: "tools/list", params: {} }
    },
    {
      title: "tools/list result",
      dir: "server → client",
      body: {
        jsonrpc: "2.0",
        id: 2,
        result: {
          tools: [
            { name: "read_note", description: "Read one note by topic.", inputSchema: { type: "object", properties: { topic: { type: "string" } }, required: ["topic"] } },
            { name: "draft_mail", description: "Draft a message. Does not send.", inputSchema: { type: "object", properties: { topic: { type: "string" } }, required: ["topic"] } },
            { name: "send_mail", description: "Send a message. This server refuses.", inputSchema: { type: "object", properties: { topic: { type: "string" } }, required: ["topic"] } }
          ]
        }
      }
    },
    {
      title: "tools/call read_note",
      dir: "client → server",
      body: { jsonrpc: "2.0", id: 3, method: "tools/call", params: { name: "read_note", arguments: { topic: "refund" } } }
    },
    {
      title: "tools/call result",
      dir: "server → client",
      body: { jsonrpc: "2.0", id: 3, result: { content: [{ type: "text", text: "Returns are accepted for 30 days." }], isError: false } }
    },
    {
      title: "tools/call send_mail denied",
      dir: "server → client",
      body: { jsonrpc: "2.0", id: 4, error: { code: -32001, message: "send_mail is denied. The protocol delivered the call. The server still refused it." } }
    }
  ];

  function paintRpc() {
    var list = byId("rpcLadder");
    var frame = byId("rpcFrame");
    var meta = byId("rpcMeta");
    if (!list || !frame) return;
    if (rpcStep >= rpcFrames.length) rpcStep = rpcFrames.length - 1;
    if (rpcStep < 0) rpcStep = 0;
    list.replaceChildren();
    rpcFrames.forEach(function (item, index) {
      var row = document.createElement("li");
      row.className = index === rpcStep ? "is-now" : (index < rpcStep ? "is-done" : "");
      var title = document.createElement("strong");
      title.textContent = item.title;
      var dir = document.createElement("span");
      dir.textContent = " " + item.dir;
      row.appendChild(title);
      row.appendChild(dir);
      list.appendChild(row);
    });
    var current = rpcFrames[rpcStep];
    if (meta) meta.textContent = "Frame " + (rpcStep + 1) + " of " + rpcFrames.length + ". " + current.title + ". " + current.dir + ".";
    frame.textContent = JSON.stringify(current.body, null, 2);
  }

  function bootRpc() {
    var play = byId("rpcPlay");
    if (!play || play.dataset.bound) return;
    play.dataset.bound = "1";
    paintRpc();
    byId("rpcPrev").addEventListener("click", function () {
      window.clearInterval(rpcTimer);
      rpcStep = Math.max(0, rpcStep - 1);
      paintRpc();
    });
    byId("rpcStep").addEventListener("click", function () {
      window.clearInterval(rpcTimer);
      rpcStep = Math.min(rpcFrames.length - 1, rpcStep + 1);
      paintRpc();
    });
    byId("rpcPause").addEventListener("click", function () {
      window.clearInterval(rpcTimer);
      var label = byId("rpcPlayLabel");
      if (label) label.textContent = "Play";
    });
    play.addEventListener("click", function () {
      window.clearInterval(rpcTimer);
      var label = byId("rpcPlayLabel");
      if (reduceMotion()) {
        rpcStep = rpcFrames.length - 1;
        paintRpc();
        return;
      }
      if (label) label.textContent = "Pause";
      rpcTimer = window.setInterval(function () {
        if (rpcStep >= rpcFrames.length - 1) {
          window.clearInterval(rpcTimer);
          if (label) label.textContent = "Play";
          return;
        }
        rpcStep += 1;
        paintRpc();
      }, 900);
    });
    byId("rpcInspect").addEventListener("click", function () {
      var button = byId("rpcInspect");
      var open = button.getAttribute("aria-pressed") !== "true";
      button.setAttribute("aria-pressed", open ? "true" : "false");
      byId("rpcFrame").hidden = !open;
      paintRpc();
    });
  }

  function boot() {
    if (booted) return;
    booted = true;
    var proofGo = byId("proofGo");
    if (proofGo) proofGo.addEventListener("click", drawProof);
    ["sampleTemp", "sampleP"].forEach(function (id) {
      var node = byId(id);
      if (node) node.addEventListener("input", function () { drawSample(false); });
    });
    var sampleDraw = byId("sampleDraw");
    if (sampleDraw) sampleDraw.addEventListener("click", function () { drawSample(true); });
    var embed = byId("embedCanvas");
    if (embed) {
      embed.addEventListener("pointerdown", function (event) {
        embed.setPointerCapture(event.pointerId);
        pointFromEvent(embed, event);
      });
      embed.addEventListener("pointermove", function (event) {
        if (!embed.hasPointerCapture(event.pointerId)) return;
        pointFromEvent(embed, event);
      });
      embed.addEventListener("keydown", function (event) {
        var step = event.shiftKey ? 0.08 : 0.03;
        if (event.key === "ArrowLeft") queryPoint.x -= step;
        else if (event.key === "ArrowRight") queryPoint.x += step;
        else if (event.key === "ArrowUp") queryPoint.y -= step;
        else if (event.key === "ArrowDown") queryPoint.y += step;
        else return;
        event.preventDefault();
        queryPoint.x = Math.max(0.02, Math.min(0.98, queryPoint.x));
        queryPoint.y = Math.max(0.02, Math.min(0.98, queryPoint.y));
        drawEmbed();
      });
    }
    ["embedX", "embedY", "embedZ"].forEach(function (id) {
      var node = byId(id);
      if (!node || node.dataset.bound) return;
      node.dataset.bound = "1";
      node.addEventListener("input", function () {
        if (embedSync) return;
        queryPoint.x = Number(byId("embedX").value) / 100;
        queryPoint.y = Number(byId("embedY").value) / 100;
        if (byId("embedZ")) queryPoint.z = Number(byId("embedZ").value) / 100;
        drawEmbed();
      });
    });
    window.CampusEmbedDrag = function (x, y, z) {
      queryPoint.x = x;
      queryPoint.y = y;
      queryPoint.z = z;
      drawEmbed();
    };
    Array.prototype.forEach.call(document.querySelectorAll("[data-embed-fail]"), function (button) {
      if (button.dataset.bound) return;
      button.dataset.bound = "1";
      button.addEventListener("click", function () {
        var on = button.getAttribute("aria-pressed") !== "true";
        button.setAttribute("aria-pressed", on ? "true" : "false");
        if (window.CampusSpace && window.CampusSpace.setEmbedFailure) {
          window.CampusSpace.setEmbedFailure(button.getAttribute("data-embed-fail"), on);
        }
        drawEmbed();
      });
    });
    bootRpc();
    var promptGo = byId("promptGo");
    if (promptGo) promptGo.addEventListener("click", drawPrompt);
    var fitB = byId("fitB");
    if (fitB) fitB.addEventListener("input", drawFit);
    var fitBits = byId("fitBits");
    if (fitBits) fitBits.addEventListener("change", drawFit);
    ["costIn", "costOutTok", "costPin", "costPout", "costMs", "costCalls"].forEach(function (id) {
      var node = byId(id);
      if (node) node.addEventListener("input", drawCost);
    });
    var costCache = byId("costCache");
    if (costCache) costCache.addEventListener("change", drawCost);
    var vdb = byId("vdbCanvas");
    if (vdb) {
      vdb.addEventListener("pointerdown", function (event) {
        vdb.setPointerCapture(event.pointerId);
        setVdbFromEvent(vdb, event);
      });
      vdb.addEventListener("pointermove", function (event) {
        if (!vdb.hasPointerCapture(event.pointerId)) return;
        setVdbFromEvent(vdb, event);
      });
    }
    Array.prototype.forEach.call(document.querySelectorAll("[data-vdb]"), function (button) {
      button.addEventListener("click", function () {
        vdbMode = button.getAttribute("data-vdb");
        Array.prototype.forEach.call(document.querySelectorAll("[data-vdb]"), function (other) {
          other.setAttribute("aria-pressed", other === button ? "true" : "false");
        });
        drawVdb();
      });
    });
    ["vdbX", "vdbY"].forEach(function (id) {
      var node = byId(id);
      if (!node) return;
      node.addEventListener("input", function () {
        vdbQuery.x = Number(byId("vdbX").value) / 100;
        vdbQuery.y = Number(byId("vdbY").value) / 100;
        drawVdb();
      });
    });
    var schemaGo = byId("schemaGo");
    if (schemaGo) schemaGo.addEventListener("click", drawSchema);
    Array.prototype.forEach.call(document.querySelectorAll("[data-schema]"), function (button) {
      button.addEventListener("click", function () {
        byId("schemaInput").value = button.getAttribute("data-schema");
        drawSchema();
      });
    });
    var handoffGoal = byId("handoffGoal");
    if (handoffGoal) handoffGoal.addEventListener("input", function () { handStep = 0; drawHandoff(); });
    Array.prototype.forEach.call(document.querySelectorAll(".handoff-preset"), function (button) {
      button.addEventListener("click", function () {
        handoffGoal.value = button.getAttribute("data-q");
        handStep = 0;
        drawHandoff();
      });
    });
    var handPrev = byId("handoffPrev");
    var handNext = byId("handoffNext");
    if (handPrev) handPrev.addEventListener("click", function () { handStep = Math.max(0, handStep - 1); drawHandoff(); });
    if (handNext) handNext.addEventListener("click", function () { handStep = Math.min(2, handStep + 1); drawHandoff(); });
    Array.prototype.forEach.call(document.querySelectorAll("input[name='mcpTool']"), function (input) {
      input.addEventListener("change", drawMcp);
    });
    var mcpApprove = byId("mcpApprove");
    if (mcpApprove) mcpApprove.addEventListener("change", drawMcp);
    var reviewStrip = byId("reviewStrip");
    var reviewTestBtn = byId("reviewTest");
    if (reviewStrip) reviewStrip.addEventListener("click", function () { reviewSecret = false; drawReview(); });
    if (reviewTestBtn) reviewTestBtn.addEventListener("click", function () { reviewTest = true; drawReview(); });
    ["decideGap", "decideSource", "decideFailed", "decideLicense"].forEach(function (id) {
      var node = byId(id);
      if (node) node.addEventListener("change", drawDecide);
    });
    var guardInput = byId("guardInput");
    if (guardInput) guardInput.addEventListener("input", drawGuard);
    Array.prototype.forEach.call(document.querySelectorAll(".guard-preset"), function (button) {
      button.addEventListener("click", function () {
        guardInput.value = button.getAttribute("data-q");
        drawGuard();
      });
    });
    var specGo = byId("specGo");
    if (specGo) specGo.addEventListener("click", drawSpec);
    Array.prototype.forEach.call(document.querySelectorAll(".cap-check"), function (box) {
      box.addEventListener("change", drawCap);
    });
    bootQuizChrome();
  }

  function onTab(name) {
    boot();
    if (drawers[name]) drawers[name]();
  }

  document.addEventListener("campus-mount", function () {
    booted = false;
    window.clearInterval(rpcTimer);
  });

  document.addEventListener("campus-marked", function (event) {
    var detail = event.detail || {};
    if (!detail.on) return;
    noteToday();
    burst();
  });

  paintStreak();
  window.LabExtra = { boot: boot, onTab: onTab, streakLength: streakLength };
  document.dispatchEvent(new CustomEvent("campus-progress"));
})();

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
    add({ title: "Diagrams", hint: "Atlas of room drawings and flows", href: "#atlas", kind: "Place" });
    add({ title: "Flows", hint: "Animated ladders and routes", href: "#flows", kind: "Place" });
    add({ title: "Charts", hint: "Counts from this catalog", href: "#charts", kind: "Place" });
    add({ title: "Careers", hint: "What to show instead of a certificate", href: "#EX-11", kind: "Place" });
    add({ title: "Regions", hint: "Residency names and study boundaries", href: "#regions", kind: "Place" });
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
      var finalText = String(target);
      el.style.minWidth = Math.max(finalText.length, 1) + "ch";
      if (reduceMotion() || target === 0 || (el.textContent || "").trim() === finalText) {
        el.textContent = finalText;
        return;
      }
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

