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

  function loadQuiz() {
    if (quizItems.length) return;
    var node = byId("quizData");
    if (!node) return;
    try { quizItems = JSON.parse(node.textContent); } catch (err) { quizItems = []; }
  }

  function quizQueue() {
    loadQuiz();
    if (quizMode === "boss") return quizItems.filter(function (item) { return item.boss; });
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

  function paintQuiz() {
    var card = byId("quizCard");
    if (!card) return;
    loadQuiz();
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
      var passed = correct >= 16;
      progress.textContent = correct + " of " + queue.length + ". " + (passed ? "Pass. Sixteen was the line." : "Not yet. Sixteen of twenty is the line. The reasons are below.");
      queue.forEach(function (item) {
        var block = document.createElement("article");
        block.className = "quiz-review " + (bossPicks[item.id] === item.answer ? "is-right" : "is-wrong");
        var title = document.createElement("strong");
        title.textContent = item.q;
        var body = document.createElement("p");
        body.textContent = item.why;
        block.appendChild(title);
        block.appendChild(body);
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
    progress.textContent = "Question " + (quizCursor + 1) + " of " + queue.length + " · " + item.trackName + (quizMode === "boss" ? " · boss exam" : "");
    var legend = document.createElement("p");
    legend.className = "quiz-q";
    legend.textContent = item.q;
    card.appendChild(legend);
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
    var passed = correct >= 16;
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
      loadQuiz();
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
