(function () {
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

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
    if (reduced) return;
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
      if (!window.speechSynthesis) {
        if (note) note.textContent = "This browser has no speech engine. Read the transcript above.";
        return;
      }
      window.speechSynthesis.cancel();
      const utter = new SpeechSynthesisUtterance(text);
      utter.lang = "en";
      window.speechSynthesis.speak(utter);
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
