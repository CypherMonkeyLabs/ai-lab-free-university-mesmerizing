try {
  var saved = localStorage.getItem("ailab-v3-theme");
  var contrast = localStorage.getItem("ailab-v3-contrast");
  var themeOk = { dark: 1, light: 1, contrast: 1, dusk: 1, futuristic: 1, gaming: 1, neon: 1, holographic: 1, cyberpunk: 1, sunset: 1 };
  if (saved && !themeOk[saved]) saved = "neon";
  if ((!saved || saved === "dark" || saved === "light" || saved === "neon") && contrast === "high") saved = "contrast";
  if (saved) document.documentElement.setAttribute("data-theme", saved);
  if (saved === "contrast" || contrast === "high") document.documentElement.setAttribute("data-contrast", "high");
  var font = localStorage.getItem("ailab-v3-font");
  if (font) document.documentElement.setAttribute("data-font", font);
  var motionPref = localStorage.getItem("ailab-v3-motion");
  if (motionPref === "reduce" || (motionPref !== "full" && window.matchMedia("(prefers-reduced-motion: reduce)").matches)) {
    document.documentElement.setAttribute("data-motion", "reduce");
  }
  if (location.hash && location.hash !== "#" && location.hash !== "#home") document.documentElement.classList.add("route-pending");
} catch (err) {}
document.documentElement.classList.add("js");
