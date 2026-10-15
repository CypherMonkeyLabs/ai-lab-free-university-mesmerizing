/* Settings and tips. Loaded when those buttons open. */

function readPref(key, fallback) {
  try {
    var value = localStorage.getItem(key);
    return value == null ? fallback : value;
  } catch (err) {
    return fallback;
  }
}

function writePref(key, value) {
  try { localStorage.setItem(key, value); } catch (err) { /* ignore */ }
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

var settingsWired = false;
var tipsWired = false;
var tipPacks = null;

function ensureSettings() {
  if (document.getElementById("settingsDrawer")) return;
  var dialog = document.createElement("dialog");
  dialog.id = "settingsDrawer";
  dialog.className = "sheet";
  dialog.setAttribute("aria-labelledby", "settingsTitle");
  dialog.innerHTML = [
    "<h2 id=\"settingsTitle\">Settings</h2>",
    "<p class=\"lede\">Theme, sound, narration, motion, and type size stay in this browser.</p>",
    "<fieldset class=\"theme-pick\"><legend>Theme</legend>",
    "<label><input type=\"radio\" name=\"setTheme\" value=\"dark\"> <span class=\"swatch swatch-dark\" aria-hidden=\"true\"></span> Dark</label>",
    "<label><input type=\"radio\" name=\"setTheme\" value=\"light\"> <span class=\"swatch swatch-light\" aria-hidden=\"true\"></span> Light</label>",
    "<label><input type=\"radio\" name=\"setTheme\" value=\"contrast\"> <span class=\"swatch swatch-contrast\" aria-hidden=\"true\"></span> High contrast</label>",
    "<label><input type=\"radio\" name=\"setTheme\" value=\"futuristic\"> <span class=\"swatch swatch-dusk\" aria-hidden=\"true\"></span> Futuristic</label>",
    "<label><input type=\"radio\" name=\"setTheme\" value=\"gaming\"> <span class=\"swatch swatch-contrast\" aria-hidden=\"true\"></span> Gaming</label>",
    "<label><input type=\"radio\" name=\"setTheme\" value=\"neon\"> <span class=\"swatch swatch-dark\" aria-hidden=\"true\"></span> Neon</label>",
    "<label><input type=\"radio\" name=\"setTheme\" value=\"holographic\"> <span class=\"swatch swatch-dusk\" aria-hidden=\"true\"></span> Holographic</label>",
    "<label><input type=\"radio\" name=\"setTheme\" value=\"cyberpunk\"> <span class=\"swatch swatch-contrast\" aria-hidden=\"true\"></span> Cyberpunk</label>",
    "<label><input type=\"radio\" name=\"setTheme\" value=\"sunset\"> <span class=\"swatch swatch-light\" aria-hidden=\"true\"></span> Sunset</label>",
    "<label><input type=\"radio\" name=\"setTheme\" value=\"dusk\"> <span class=\"swatch swatch-dusk\" aria-hidden=\"true\"></span> Dusk</label>",
    "</fieldset>",
    "<label class=\"set-row\">Language <select id=\"setLang\" aria-label=\"Language\">",
    "<option value=\"en\">English</option><option value=\"es\">Español</option>",
    "<option value=\"hi\">हिन्दी</option><option value=\"te\">తెలుగు</option>",
    "<option value=\"fr\">Français</option><option value=\"de\">Deutsch</option>",
    "<option value=\"ja\">日本語</option><option value=\"ar\">العربية</option>",
    "</select></label>",
    "<label class=\"set-check\"><input type=\"checkbox\" id=\"setSound\"> Sound effects</label>",
    "<label class=\"set-check\"><input type=\"checkbox\" id=\"setNarration\"> Narration</label>",
    "<label class=\"set-row\">Voice <select id=\"setVoice\"><option value=\"\">Automatic, best installed voice</option></select></label>",
    "<p id=\"voiceNote\" class=\"play-note\"></p>",
    "<label class=\"set-row\">Narration speed <input type=\"range\" id=\"setRate\" min=\"0.7\" max=\"1.4\" step=\"0.1\" value=\"1\"> <span id=\"setRateOut\">1.0×</span></label>",
    "<label class=\"set-check\"><input type=\"checkbox\" id=\"setMotion\"> Reduced motion</label>",
    "<label class=\"set-row\">Font size <select id=\"setFont\">",
    "<option value=\"sm\">Small</option><option value=\"md\">Default</option>",
    "<option value=\"lg\">Large</option><option value=\"xl\">Extra large</option>",
    "</select></label>",
    "<p><button type=\"button\" class=\"btn\" data-close>Close</button></p>"
  ].join("");
  document.body.appendChild(dialog);
}

function wireSettings() {
  if (settingsWired) return;
  settingsWired = true;
  var drawer = document.getElementById("settingsDrawer");
  var sound = document.getElementById("setSound");
  var narration = document.getElementById("setNarration");
  var voice = document.getElementById("setVoice");
  var voiceNote = document.getElementById("voiceNote");
  var rate = document.getElementById("setRate");
  var rateOut = document.getElementById("setRateOut");
  var motion = document.getElementById("setMotion");
  var font = document.getElementById("setFont");
  if (sound) {
    sound.checked = readPref("ailab-v3-sound", "off") === "on";
    sound.addEventListener("change", function () {
      writePref("ailab-v3-sound", sound.checked ? "on" : "off");
      if (sound.checked && window.CampusSettings) window.CampusSettings.play("ok");
    });
  }
  if (narration) {
    narration.checked = readPref("ailab-v3-narration", "on") !== "off";
    narration.addEventListener("change", function () {
      writePref("ailab-v3-narration", narration.checked ? "on" : "off");
      if (!narration.checked && window.speechSynthesis) window.speechSynthesis.cancel();
    });
  }
  if (rate) {
    rate.value = readPref("ailab-v3-rate", "1");
    if (rateOut) rateOut.textContent = Number(rate.value).toFixed(1) + "×";
    rate.addEventListener("input", function () {
      writePref("ailab-v3-rate", rate.value);
      if (rateOut) rateOut.textContent = Number(rate.value).toFixed(1) + "×";
    });
  }
  if (motion) {
    motion.checked = readPref("ailab-v3-motion", "") === "reduce";
    motion.addEventListener("change", function () {
      writePref("ailab-v3-motion", motion.checked ? "reduce" : "auto");
      if (motion.checked) document.documentElement.setAttribute("data-motion", "reduce");
      else document.documentElement.removeAttribute("data-motion");
      document.dispatchEvent(new CustomEvent("campus-motion"));
    });
  }
  var setLang = document.getElementById("setLang");
  if (setLang) {
    setLang.value = document.documentElement.lang || "en";
    setLang.addEventListener("change", function () {
      var select = document.getElementById("langSelect");
      if (select) {
        select.value = setLang.value;
        select.dispatchEvent(new Event("change"));
      }
    });
  }
  if (font) {
    font.value = readPref("ailab-v3-font", "md");
    font.addEventListener("change", function () {
      writePref("ailab-v3-font", font.value);
      if (font.value === "md") document.documentElement.removeAttribute("data-font");
      else document.documentElement.setAttribute("data-font", font.value);
    });
  }
  document.querySelectorAll('input[name="setTheme"]').forEach(function (input) {
    input.addEventListener("change", function () {
      if (!input.checked || !window.CampusTheme) return;
      if (input.value !== "contrast") writePref("ailab-v3-theme-prev", input.value);
      window.CampusTheme(input.value);
    });
  });
  function paintVoices() {
    if (!voice || !window.speechSynthesis) {
      if (voiceNote) voiceNote.textContent = "This browser has no speech engine. Read the transcript instead.";
      return;
    }
    var voices = window.speechSynthesis.getVoices() || [];
    var saved = readPref("ailab-v3-voice", "");
    voice.replaceChildren();
    var auto = document.createElement("option");
    auto.value = "";
    auto.textContent = "Automatic, best installed voice";
    voice.appendChild(auto);
    voices.forEach(function (item) {
      var option = document.createElement("option");
      option.value = item.voiceURI;
      option.textContent = item.name + (item.lang ? " (" + item.lang + ")" : "") + (voiceScore(item) < 0 ? " — robotic" : "");
      voice.appendChild(option);
    });
    voice.value = saved && Array.prototype.some.call(voice.options, function (option) { return option.value === saved; }) ? saved : "";
    var picked = chosenVoice(voices);
    if (voiceNote) {
      if (!voices.length) voiceNote.textContent = "Waiting for the voice list.";
      else if (!picked && !saved) voiceNote.textContent = "No high-quality English voice is installed. Narration stays quiet until you pick one. Robotic desktop voices are listed and are not the default.";
      else voiceNote.textContent = "Narration uses " + (saved ? (voice.selectedOptions[0] ? voice.selectedOptions[0].textContent : "your pick") : picked.name) + ".";
    }
  }
  if (window.speechSynthesis) {
    paintVoices();
    window.speechSynthesis.addEventListener("voiceschanged", paintVoices);
    window.setTimeout(paintVoices, 300);
  } else paintVoices();
  if (voice) voice.addEventListener("change", function () {
    writePref("ailab-v3-voice", voice.value);
    paintVoices();
  });
  if (drawer) drawer.addEventListener("click", function (event) {
    if (event.target.closest("[data-close]")) drawer.close();
  });
}

export function openSettings() {
  ensureSettings();
  wireSettings();
  var themeName = document.documentElement.getAttribute("data-theme") || "neon";
  if (window.CampusTheme) window.CampusTheme(themeName);
  document.querySelectorAll('input[name="setTheme"]').forEach(function (input) {
    input.checked = input.value === themeName;
  });
  var setLang = document.getElementById("setLang");
  if (setLang) setLang.value = document.documentElement.lang || "en";
  var drawer = document.getElementById("settingsDrawer");
  if (drawer && drawer.showModal && !drawer.open) drawer.showModal();
}

function paintTips(id) {
  var body = document.getElementById("tipsBody");
  var pack = tipPacks[id] || tipPacks["00"];
  if (!body || !pack) return;
  body.replaceChildren();
  function section(title, items, kind) {
    var wrap = document.createElement("section");
    wrap.className = "tip-block";
    var heading = document.createElement("h3");
    heading.textContent = title;
    wrap.appendChild(heading);
    if (kind === "list") {
      var list = document.createElement("ul");
      items.forEach(function (line) {
        var li = document.createElement("li");
        li.textContent = line;
        list.appendChild(li);
      });
      wrap.appendChild(list);
    } else {
      var dl = document.createElement("dl");
      items.forEach(function (row) {
        var term = document.createElement("dt");
        term.textContent = row[0];
        var detail = document.createElement("dd");
        detail.textContent = row[1];
        dl.appendChild(term);
        dl.appendChild(detail);
      });
      wrap.appendChild(dl);
    }
    body.appendChild(wrap);
  }
  section("Pro tips", pack.tips || [], "list");
  section("Interview traps", pack.traps || [], "list");
  section("Cheat sheet", pack.sheet || [], "sheet");
}

function currentTrack(select) {
  var hash = (location.hash || "").replace(/^#/, "");
  if (!hash || hash === "home") return "00";
  var catalog = window.CampusCatalog;
  if (catalog) {
    var lesson = catalog.lessons.filter(function (item) { return item.id === hash; })[0];
    if (lesson && tipPacks[lesson.school]) return lesson.school;
  }
  if (hash.indexOf("school-") === 0 && tipPacks[hash.slice(7)]) return hash.slice(7);
  return select.value || "00";
}

function ensureTips() {
  if (document.getElementById("tipsDrawer")) return;
  var dialog = document.createElement("dialog");
  dialog.id = "tipsDrawer";
  dialog.className = "sheet";
  dialog.setAttribute("aria-labelledby", "tipsTitle");
  var title = document.createElement("h2");
  title.id = "tipsTitle";
  title.textContent = "Tips and tricks";
  var lede = document.createElement("p");
  lede.className = "lede";
  lede.textContent = "Pro tips, interview traps, and a cheat sheet for the track you are in.";
  var label = document.createElement("label");
  label.className = "set-row";
  label.appendChild(document.createTextNode("Track "));
  var select = document.createElement("select");
  select.id = "tipsTrack";
  Object.keys(tipPacks).forEach(function (key) {
    var option = document.createElement("option");
    option.value = key;
    option.textContent = tipPacks[key].name || key;
    select.appendChild(option);
  });
  label.appendChild(select);
  var body = document.createElement("div");
  body.id = "tipsBody";
  var closeRow = document.createElement("p");
  var close = document.createElement("button");
  close.type = "button";
  close.className = "btn";
  close.setAttribute("data-close", "");
  close.textContent = "Close";
  closeRow.appendChild(close);
  dialog.appendChild(title);
  dialog.appendChild(lede);
  dialog.appendChild(label);
  dialog.appendChild(body);
  dialog.appendChild(closeRow);
  document.body.appendChild(dialog);
}

export function openTips() {
  var pending = tipPacks ? Promise.resolve(tipPacks) : fetch("assets/curriculum/tips.json").then(function (res) {
    if (!res.ok) throw new Error("tips");
    return res.json();
  });
  return pending.then(function (packs) {
    tipPacks = packs;
    ensureTips();
    if (!tipsWired) {
      tipsWired = true;
      var drawer = document.getElementById("tipsDrawer");
      var select = document.getElementById("tipsTrack");
      select.addEventListener("change", function () { paintTips(select.value); });
      drawer.addEventListener("click", function (event) {
        if (event.target.closest("[data-close]")) drawer.close();
      });
    }
    var select = document.getElementById("tipsTrack");
    var track = currentTrack(select);
    if (tipPacks[track]) select.value = track;
    paintTips(select.value);
    var drawer = document.getElementById("tipsDrawer");
    if (drawer.showModal && !drawer.open) drawer.showModal();
  });
}
