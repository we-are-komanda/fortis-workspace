/* =========================================================================
   FORTIS landing v2 — interactions
   ========================================================================= */
(function () {
  "use strict";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Theme toggle ---------- */
  var themeBtn = document.getElementById("themeBtn");
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var cur = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
      var next = cur === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      try { localStorage.setItem("fortis-v2-theme", next); } catch (e) {}
    });
  }

  /* ---------- Sticky nav ---------- */
  var nav = document.getElementById("nav");
  function onScroll() { if (nav) nav.classList.toggle("is-stuck", window.scrollY > 20); }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---------- Count-up ---------- */
  function fmt(n, money) {
    var r = Math.round(n);
    if (money) return r.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    return r.toString();
  }
  function runCount(el) {
    if (el.dataset.done) return;
    el.dataset.done = "1";
    var target = parseFloat(el.getAttribute("data-count")) || 0;
    var money = el.hasAttribute("data-money");
    var prefix = el.getAttribute("data-prefix") || "";
    var suffix = el.getAttribute("data-suffix") || "";
    if (reduceMotion) { el.textContent = prefix + fmt(target, money) + suffix; return; }
    var dur = money ? 1500 : 1050, start = null;
    function frame(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var e = 1 - Math.pow(1 - p, 4);
      el.textContent = prefix + fmt(target * e, money) + suffix;
      if (p < 1) requestAnimationFrame(frame);
      else el.textContent = prefix + fmt(target, money) + suffix;
    }
    requestAnimationFrame(frame);
  }

  var revealEls = document.querySelectorAll(".reveal");
  var budgetBars = document.querySelectorAll(".bbar span");

  function reveal(el) {
    el.classList.add("is-in");
    el.querySelectorAll("[data-count]").forEach(runCount);
    if (el.matches("[data-count]")) runCount(el);
  }

  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { reveal(e.target); io.unobserve(e.target); } });
    }, { threshold: 0.14, rootMargin: "0px 0px -7% 0px" });
    revealEls.forEach(function (el) { io.observe(el); });

    var bio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          var s = e.target, w = s.style.width;
          s.style.width = "0%";
          requestAnimationFrame(function () { requestAnimationFrame(function () { s.style.width = w; }); });
          bio.unobserve(s);
        }
      });
    }, { threshold: 0.5 });
    budgetBars.forEach(function (el) { bio.observe(el); });
  } else {
    revealEls.forEach(reveal);
  }

  /* ---------- Failsafe: never leave content invisible ---------- */
  function revealInView() {
    document.querySelectorAll(".reveal:not(.is-in)").forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight * 1.1 && r.bottom > -40) reveal(el);
    });
  }
  window.addEventListener("load", function () { revealInView(); setTimeout(revealInView, 500); });
  setTimeout(revealInView, 300);

  /* ---------- Active nav link ---------- */
  var ids = ["modules", "how", "modularity", "compliance", "team"];
  var secs = ids.map(function (id) { return document.getElementById(id); }).filter(Boolean);
  var links = document.querySelectorAll(".nav__links a");
  if ("IntersectionObserver" in window && secs.length) {
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          links.forEach(function (a) { a.style.color = a.getAttribute("href") === "#" + e.target.id ? "var(--ink)" : ""; });
        }
      });
    }, { threshold: 0.4 });
    secs.forEach(function (s) { sio.observe(s); });
  }
})();
