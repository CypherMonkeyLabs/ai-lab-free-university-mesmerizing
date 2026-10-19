/* Topic worlds: a CSS 3D strip on the home page. No external library. */
(function () {
  var path = (location.pathname || "").split("/").pop() || "index.html";
  if (path !== "" && path !== "index.html") return;
  var grid = document.querySelector(".track-grid");
  if (!grid || document.getElementById("worlds")) return;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches
    || document.documentElement.dataset.motion === "reduce";
  var worlds = [
    ["Models", "rooms/T2-R1.html", "Tokens, context, sampling."],
    ["Retrieval", "rooms/T4-R1.html", "A passage, then an answer."],
    ["Agents", "rooms/T5-R1.html", "A loop, a schema, a cap."],
    ["MCP", "rooms/T6-R1.html", "Host, client, and server."],
    ["Voice", "rooms/T9-R1.html", "Speech in, speech out."],
    ["Safety", "rooms/T11-R1.html", "Handoff and a guardrail."]
  ];
  var section = document.createElement("section");
  section.className = "worlds" + (reduced ? " is-flat" : "");
  section.id = "worlds";
  section.innerHTML = '<h2>Topic worlds</h2><p class="worlds-note">A map of this lab, drawn in the page. Cypher Monkey, a lifelong student and AI builder, keeps these as study rooms.</p><div class="world-stage" tabindex="0" aria-label="Topic worlds"></div>';
  var stage = section.querySelector(".world-stage");
  worlds.forEach(function (item, index) {
    var card = document.createElement("a");
    card.className = "world-card";
    card.href = item[1];
    card.style.setProperty("--i", String(index));
    card.innerHTML = "<strong></strong><span></span>";
    card.querySelector("strong").textContent = item[0];
    card.querySelector("span").textContent = item[2];
    stage.appendChild(card);
  });
  if (!reduced) {
    stage.addEventListener("pointermove", function (event) {
      var rect = stage.getBoundingClientRect();
      var x = (event.clientX - rect.left) / rect.width - 0.5;
      var y = (event.clientY - rect.top) / rect.height - 0.5;
      stage.style.setProperty("--tilt-x", (y * -8).toFixed(2) + "deg");
      stage.style.setProperty("--tilt-y", (x * 10).toFixed(2) + "deg");
    });
    stage.addEventListener("pointerleave", function () {
      stage.style.removeProperty("--tilt-x");
      stage.style.removeProperty("--tilt-y");
    });
  }
  grid.insertAdjacentElement("beforebegin", section);
  var hero = document.querySelector(".hero");
  if (hero) hero.classList.add("has-aurora");
})();
