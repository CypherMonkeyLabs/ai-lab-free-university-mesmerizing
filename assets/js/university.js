/* Page behaviour that is not the guide monkey: quizzes, play, service worker. */
(function () {
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      var prefix = document.body.getAttribute("data-root") || "";
      navigator.serviceWorker.register(prefix + "sw.js").catch(function () { /* offline file open */ });
    });
  }

  document.querySelectorAll("form.quiz").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var correct = 0;
      var total = 0;
      form.querySelectorAll("fieldset").forEach(function (field) {
        total += 1;
        var answer = field.getAttribute("data-answer");
        var picked = field.querySelector("input:checked");
        var ok = picked && picked.value === answer;
        if (ok) correct += 1;
        field.classList.toggle("is-right", !!ok);
        field.classList.toggle("is-wrong", !ok);
      });
      var out = form.querySelector(".quiz-result");
      if (out) out.textContent = correct + " of " + total + " match the cited point in this room.";
      document.dispatchEvent(new CustomEvent("ai-quiz", { detail: { correct: correct, total: total } }));
    });
  });

  document.querySelectorAll("[data-match]").forEach(function (board) {
    var picked = null;
    var status = board.querySelector("[data-match-status]");
    board.querySelectorAll("button[data-pair]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (!picked) {
          picked = btn;
          btn.setAttribute("aria-pressed", "true");
          return;
        }
        if (picked === btn) return;
        var same = picked.getAttribute("data-pair") === btn.getAttribute("data-pair") && picked !== btn;
        if (same && picked.getAttribute("data-side") !== btn.getAttribute("data-side")) {
          picked.disabled = true;
          btn.disabled = true;
          picked.setAttribute("aria-pressed", "false");
          if (status) status.textContent = "Matched.";
        } else if (status) status.textContent = "Those two do not pair. Try again.";
        if (!same) picked.setAttribute("aria-pressed", "false");
        picked = null;
      });
    });
  });

  document.querySelectorAll("[data-sort]").forEach(function (list) {
    list.addEventListener("click", function (event) {
      var btn = event.target.closest("button[data-move]");
      if (!btn) return;
      var item = btn.closest("li");
      if (!item) return;
      if (btn.getAttribute("data-move") === "up" && item.previousElementSibling) list.insertBefore(item, item.previousElementSibling);
      if (btn.getAttribute("data-move") === "down" && item.nextElementSibling) list.insertBefore(item.nextElementSibling, item);
    });
    var check = list.parentElement.querySelector("[data-sort-check]");
    if (check) {
      check.addEventListener("click", function () {
        var ids = Array.prototype.map.call(list.children, function (li) { return li.getAttribute("data-step"); });
        var want = (list.getAttribute("data-order") || "").split(",");
        var ok = ids.join(",") === want.join(",");
        var out = list.parentElement.querySelector("[data-sort-status]");
        if (out) out.textContent = ok ? "That order matches the worked example." : "Not yet. The worked example order is still the target.";
      });
    }
  });

  document.querySelectorAll("form.scenario").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var answer = form.getAttribute("data-answer");
      var picked = form.querySelector("input:checked");
      var out = form.querySelector(".quiz-result");
      if (!out) return;
      out.textContent = picked && picked.value === answer ? "That choice matches the room." : "Read the why-line under the choices and try again.";
    });
  });
})();
