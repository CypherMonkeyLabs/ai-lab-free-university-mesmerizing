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
