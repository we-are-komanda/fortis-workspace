/* =========================================================================
   FORTIS landing — interactions
   ========================================================================= */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Theme ---------- */
  var root = document.documentElement;
  var toggle = document.getElementById("theme-toggle");
  var sun = toggle && toggle.querySelector(".icon-sun");
  var moon = toggle && toggle.querySelector(".icon-moon");

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    if (sun && moon) {
      sun.style.display = theme === "light" ? "none" : "block";
      moon.style.display = theme === "light" ? "block" : "none";
    }
  }
  var saved = null;
  try { saved = localStorage.getItem("fortis-theme"); } catch (e) {}
  applyTheme(saved || "dark");

  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
      applyTheme(next);
      try { localStorage.setItem("fortis-theme", next); } catch (e) {}
    });
  }

  /* ---------- Sticky nav ---------- */
  var nav = document.getElementById("nav");
  function onScrollNav() {
    if (!nav) return;
    if (window.scrollY > 24) nav.classList.add("is-stuck");
    else nav.classList.remove("is-stuck");
  }
  onScrollNav();
  window.addEventListener("scroll", onScrollNav, { passive: true });

  /* ---------- Count-up ---------- */
  function formatNumber(n, money) {
    var rounded = Math.round(n);
    if (money) {
      return rounded.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    }
    return rounded.toString();
  }

  function runCount(el) {
    var target = parseFloat(el.getAttribute("data-count")) || 0;
    var money = el.hasAttribute("data-money");
    var prefix = el.getAttribute("data-prefix") || "";
    var suffix = el.getAttribute("data-suffix") || "";
    if (reduceMotion) { el.textContent = prefix + formatNumber(target, money) + suffix; return; }

    var dur = money ? 1600 : 1100;
    var start = null;
    function frame(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 4); // ease-out-quart
      el.textContent = prefix + formatNumber(target * eased, money) + suffix;
      if (p < 1) requestAnimationFrame(frame);
      else el.textContent = prefix + formatNumber(target, money) + suffix;
    }
    requestAnimationFrame(frame);
  }

  /* ---------- Reveal + triggered effects via IntersectionObserver ---------- */
  var revealEls = document.querySelectorAll(".reveal");
  var countEls = document.querySelectorAll("[data-count]");
  var budgetBars = document.querySelectorAll(".budget__bar span");
  var cbars = document.querySelectorAll(".cbar");

  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.16, rootMargin: "0px 0px -8% 0px" });
    revealEls.forEach(function (el) { io.observe(el); });

    // counters
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { runCount(entry.target); cio.unobserve(entry.target); }
      });
    }, { threshold: 0.6 });
    countEls.forEach(function (el) { cio.observe(el); });

    // budget bars + calc bars (animate width on enter)
    var bio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          bio.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    cbars.forEach(function (el) { bio.observe(el); });

    // budget bar fill (width set inline already; re-trigger transition)
    var budgetIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var span = entry.target;
          var w = span.style.width;
          span.style.width = "0%";
          requestAnimationFrame(function () {
            requestAnimationFrame(function () { span.style.width = w; });
          });
          budgetIO.unobserve(span);
        }
      });
    }, { threshold: 0.5 });
    budgetBars.forEach(function (el) { budgetIO.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-in"); });
    countEls.forEach(runCount);
    cbars.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- Failsafe: never leave content invisible ----------
     If IntersectionObserver doesn't fire (some embedded/preview contexts),
     reveal anything currently in the viewport on load, and force-reveal
     everything after a short grace period so nothing stays stuck at opacity 0. */
  function revealInView() {
    document.querySelectorAll(".reveal:not(.is-in)").forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight * 1.1 && r.bottom > -40) {
        el.classList.add("is-in");
        if (el.matches("[data-count]")) runCount(el);
      }
    });
  }
  window.addEventListener("load", function () {
    revealInView();
    setTimeout(revealInView, 500);
  });
  setTimeout(revealInView, 300);

  /* ---------- Parallax (pointer + scroll), rAF-throttled ---------- */
  var parallaxEls = document.querySelectorAll(".parallax");
  var px = 0, py = 0, sy = 0, ticking = false;

  function applyParallax() {
    parallaxEls.forEach(function (el) {
      var depth = parseFloat(el.getAttribute("data-depth")) || 0.2;
      var rect = el.getBoundingClientRect();
      var inView = rect.top < window.innerHeight && rect.bottom > 0;
      if (!inView) return;
      var tx = px * depth * 26;
      var ty = py * depth * 26 + (sy * depth * -0.06);
      el.style.transform = "translate3d(" + tx.toFixed(2) + "px," + ty.toFixed(2) + "px,0)";
    });
    ticking = false;
  }
  function requestParallax() { if (!ticking) { ticking = true; requestAnimationFrame(applyParallax); } }

  if (!reduceMotion && parallaxEls.length) {
    window.addEventListener("mousemove", function (e) {
      px = (e.clientX / window.innerWidth) * 2 - 1;
      py = (e.clientY / window.innerHeight) * 2 - 1;
      requestParallax();
    }, { passive: true });
    window.addEventListener("scroll", function () { sy = window.scrollY; requestParallax(); }, { passive: true });
  }

  /* ---------- Active nav link on scroll ---------- */
  var sections = ["product", "echelons", "how", "modules", "compliance"].map(function (id) { return document.getElementById(id); }).filter(Boolean);
  var navLinks = document.querySelectorAll(".nav__links a");
  if ("IntersectionObserver" in window && sections.length) {
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var id = entry.target.id;
          navLinks.forEach(function (a) {
            a.style.color = a.getAttribute("href") === "#" + id ? "var(--ink)" : "";
          });
        }
      });
    }, { threshold: 0.4 });
    sections.forEach(function (s) { sio.observe(s); });
  }
})();
