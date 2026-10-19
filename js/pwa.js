/* Install prompt and a first-run splash. No network. */
(function () {
  var deferred = null;
  var KEY = "ai-lab-splash-v1";

  function splash() {
    var seen = false;
    try { seen = localStorage.getItem(KEY) === "yes"; } catch (err) { seen = true; }
    var greeted = false;
    try { greeted = localStorage.getItem("ai-omni-greeted") === "1"; } catch (err) { greeted = false; }
    if (!greeted || seen || document.getElementById("pwa-splash")) return;
    var node = document.createElement("div");
    node.id = "pwa-splash";
    node.className = "pwa-splash";
    node.setAttribute("role", "dialog");
    node.setAttribute("aria-modal", "true");
    node.setAttribute("aria-labelledby", "pwa-splash-title");
    node.innerHTML = '<div class="pwa-splash-card"><p class="kicker">AI Lab</p><h2 id="pwa-splash-title">Study offline after this visit</h2><p>Cypher Monkey, a lifelong student and AI builder, keeps this lab on your device. No account.</p><button type="button" class="themed" data-splash-ok>Continue</button></div>';
    document.body.appendChild(node);
    var button = node.querySelector("[data-splash-ok]");
    button.focus();
    function close() {
      try { localStorage.setItem(KEY, "yes"); } catch (err) { /* storage off */ }
      node.remove();
    }
    button.addEventListener("click", close);
    node.addEventListener("keydown", function (event) {
      if (event.key === "Escape") close();
    });
  }

  window.addEventListener("beforeinstallprompt", function (event) {
    event.preventDefault();
    deferred = event;
  });

  function installControl() {
    if (document.getElementById("pwa-install")) return;
    var bar = document.querySelector(".phone-dock") || document.body;
    var button = document.createElement("button");
    button.type = "button";
    button.id = "pwa-install";
    button.className = "themed pwa-install";
    button.textContent = "Install";
    button.addEventListener("click", function () {
      if (!deferred) {
        button.textContent = "Use the browser menu to install";
        return;
      }
      deferred.prompt();
      deferred.userChoice.finally(function () { deferred = null; });
    });
    bar.appendChild(button);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { splash(); installControl(); });
  } else {
    splash();
    installControl();
  }
})();
