/* Counters, theme chips, D3, Rough.js, markmap, and confetti. Offline only. */
import { animate } from "../../vendor/anime.esm.min.js";

var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function countUp(node) {
  var target = Number(node.getAttribute("data-count"));
  if (!Number.isFinite(target) || node.dataset.counted === "1") return;
  node.dataset.counted = "1";
  if (reduce) {
    node.textContent = String(target);
    return;
  }
  var state = { n: 0 };
  try {
    animate(state, {
      n: target,
      duration: 800,
      ease: "outQuad",
      onUpdate: function () {
        node.textContent = String(Math.round(state.n));
      },
    });
  } catch (err) {
    node.textContent = String(target);
  }
}

function paintCounts(root) {
  (root || document).querySelectorAll("[data-count]").forEach(countUp);
}

function drawD3(root) {
  if (!window.d3) return;
  (root || document).querySelectorAll("[data-d3-chart]").forEach(function (host) {
    if (host.dataset.drawn === "1") return;
    host.dataset.drawn = "1";
    var labels = (host.getAttribute("data-labels") || "").split(",").filter(Boolean);
    var values = (host.getAttribute("data-values") || "").split(",").map(Number);
    var rows = labels.map(function (label, index) { return { label: label, value: values[index] || 0 }; });
    var width = 640;
    var height = 36 + rows.length * 22;
    var peak = d3.max(rows, function (row) { return row.value; }) || 1;
    var svg = d3.select(host).append("svg").attr("viewBox", "0 0 " + width + " " + height).attr("role", "img");
    svg.append("rect").attr("width", width).attr("height", height).attr("rx", 12).attr("fill", "#070b16");
    var scale = d3.scaleLinear().domain([0, peak]).range([0, 280]);
    svg.selectAll("text.label").data(rows).enter().append("text")
      .attr("x", 12).attr("y", function (_row, index) { return 28 + index * 22; })
      .attr("fill", "#e7f6ff").attr("font-size", 12).attr("font-family", "system-ui,sans-serif")
      .text(function (row) { return row.label; });
    svg.selectAll("rect.bar").data(rows).enter().append("rect")
      .attr("x", 80).attr("y", function (_row, index) { return 16 + index * 22; })
      .attr("height", 14).attr("rx", 4).attr("fill", "#22d3ee")
      .attr("width", function (row) { return scale(row.value); });
  });
}

function drawRough(root) {
  if (!window.rough) return;
  (root || document).querySelectorAll("[data-rough-chart] svg").forEach(function (svg) {
    if (svg.dataset.drawn === "1") return;
    svg.dataset.drawn = "1";
    var rc = window.rough.svg(svg);
    svg.appendChild(rc.rectangle(8, 8, 260, 64, { stroke: "#22d3ee", roughness: 1.4, strokeWidth: 2 }));
  });
}

function normalizeTree(node) {
  if (!node || typeof node !== "object") return;
  if (!Array.isArray(node.children)) node.children = [];
  node.children.forEach(normalizeTree);
}

function drawMindmap() {
  var svg = document.getElementById("mindmap");
  var dataNode = document.getElementById("mindmapData");
  if (!svg || !dataNode || !window.markmap || !window.markmap.Markmap || svg.dataset.drawn === "1") return;
  var tree;
  try {
    tree = JSON.parse(dataNode.textContent);
    normalizeTree(tree);
  } catch (err) {
    return;
  }
  svg.dataset.drawn = "1";
  try {
    var mm = new window.markmap.Markmap(svg, { duration: reduce ? 0 : 400 });
    mm.setData(tree).then(function () {
      return mm.fit();
    }).catch(function () {
      svg.insertAdjacentHTML("afterend", '<p class="block-note">The mind map words are on this page. The drawing library did not finish.</p>');
    });
  } catch (err) {
    svg.dataset.drawn = "0";
  }
}

function wireThemes(root) {
  (root || document).querySelectorAll("[data-set-theme]").forEach(function (button) {
    if (button.dataset.bound === "1") return;
    button.dataset.bound = "1";
    button.addEventListener("click", function () {
      if (window.CampusTheme) window.CampusTheme(button.getAttribute("data-set-theme"));
    });
  });
}

function wireAtlas(root) {
  (root || document).querySelectorAll("[data-atlas-filter]").forEach(function (button) {
    if (button.dataset.bound === "1") return;
    button.dataset.bound = "1";
    button.addEventListener("click", function () {
      var kind = button.getAttribute("data-atlas-filter");
      var scope = button.closest("[data-panel]") || document;
      scope.querySelectorAll("[data-atlas-filter]").forEach(function (peer) {
        peer.setAttribute("aria-pressed", peer === button ? "true" : "false");
      });
      scope.querySelectorAll("[data-atlas-diagram]").forEach(function (card) {
        var animated = card.getAttribute("data-animated") === "1";
        var cardKind = card.getAttribute("data-kind");
        var show = kind === "all" || (kind === "animated" && animated) || cardKind === kind;
        card.hidden = !show;
      });
    });
  });
}

function tilt(root) {
  if (reduce) return;
  (root || document).querySelectorAll("[data-parallax]").forEach(function (row) {
    if (row.dataset.bound === "1") return;
    row.dataset.bound = "1";
    row.addEventListener("pointermove", function (event) {
      var box = row.getBoundingClientRect();
      var dx = (event.clientX - box.left) / box.width - 0.5;
      row.style.setProperty("--lean", (dx * 8).toFixed(2) + "deg");
    });
  });
}

function openSpace() {
  var host = document.getElementById("heroMount");
  if (!host || host.dataset.opened === "1") return;
  host.dataset.opened = "1";
  host.hidden = false;
  var button = document.getElementById("openSpace");
  if (button) button.hidden = true;
  import("./space.js").then(function (mod) {
    mod.mountTopology(host);
  }).catch(function () { /* the fallback sentence stays */ });
}

function boot(root) {
  paintCounts(root);
  drawD3(root);
  drawRough(root);
  drawMindmap();
  wireThemes(root);
  wireAtlas(root);
  tilt(root);
  if (!reduce) {
    try {
      animate(".tilt-card", { rotateY: [-10, 8], duration: 2800, loop: true, alternate: true, ease: "inOutQuad" });
    } catch (err) { /* counters still ran */ }
  }
  if (document.getElementById("heroMount")) openSpace();
}

window.CampusCelebrate = function () {
  if (reduce || typeof window.confetti !== "function") return;
  window.confetti({ particleCount: 80, spread: 65, origin: { y: 0.75 } });
};

document.addEventListener("campus-show", function () { boot(document.getElementById("stage") || document); });
document.addEventListener("campus-mount", function () { boot(document.getElementById("stage") || document); });
boot(document);
