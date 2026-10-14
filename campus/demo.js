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
    if (view !== "studio" && view !== "builds") return;
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
})();
