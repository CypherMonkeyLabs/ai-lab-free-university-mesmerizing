/* Labeled channel simulation. It does not call a vendor, a SIP trunk, or a model. */
(function () {
  var path = (location.pathname || "").split("/").pop() || "";
  if (path !== "play.html") return;
  var main = document.getElementById("main");
  if (!main || document.getElementById("channel-sim")) return;
  var section = document.createElement("section");
  section.className = "section-block channel-sim";
  section.id = "channel-sim";
  section.innerHTML = [
    '<h2>Channel route, simulated</h2>',
    '<p class="sim-flag">Simulation. No vendor system, SIP trunk, or model was called.</p>',
    '<div class="sim-nodes" role="group" aria-label="Choose a channel">',
    '<button type="button" class="themed" data-channel="voice">Voice</button>',
    '<button type="button" class="themed" data-channel="chat">Chat</button>',
    '<button type="button" class="themed" data-channel="message">Message</button>',
    '<button type="button" class="themed" data-channel="handoff">Handoff</button>',
    '</div>',
    '<label class="sim-cap">Step cap <input type="number" min="1" max="8" value="3" data-cap aria-label="Simulated step cap"></label>',
    '<p class="sim-result" data-sim-result aria-live="polite">Pick a channel. The route stays on this page.</p>'
  ].join("");
  var sources = main.querySelector(".go-deeper");
  if (sources) main.insertBefore(section, sources);
  else main.appendChild(section);
  var result = section.querySelector("[data-sim-result]");
  var capInput = section.querySelector("[data-cap]");
  var channel = "";
  function paint() {
    var cap = Math.max(1, Math.min(8, Number(capInput.value) || 3));
    capInput.value = String(cap);
    if (!channel) {
      result.textContent = "Pick a channel. The route stays on this page.";
      return;
    }
    var lines = {
      voice: "Simulated voice route: speech in, one policy check, then speech out. The loop stops after " + cap + " tool steps.",
      chat: "Simulated chat route: the same policy, text in and text out. The loop stops after " + cap + " tool steps.",
      message: "Simulated message route: the same policy on a message. The loop stops after " + cap + " tool steps.",
      handoff: "Simulated handoff: a person continues the turn. The model loop stops. Step cap " + cap + " is not used."
    };
    result.textContent = lines[channel] + " Simulation only.";
  }
  section.querySelectorAll("[data-channel]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      channel = btn.getAttribute("data-channel");
      section.querySelectorAll("[data-channel]").forEach(function (other) {
        other.setAttribute("aria-pressed", other === btn ? "true" : "false");
      });
      paint();
    });
  });
  capInput.addEventListener("input", paint);
})();
