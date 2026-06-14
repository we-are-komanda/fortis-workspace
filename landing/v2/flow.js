/* =========================================================================
   FORTIS — flow narrative interactions (shared)
   In-view reveals + looping demo animations. Self-contained IIFE.
   ========================================================================= */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-color-scheme: reduce)").matches ||
               window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function fmtMoney(n) { return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " "); }

  /* ---------- In-view: add .fl-in, toggle demo loops ---------- */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      var el = e.target;
      if (e.isIntersecting) {
        el.classList.add("fl-in");
        if (el.__demo) el.__demo.start();
      } else if (el.__demo) {
        el.__demo.stop();
      }
    });
  }, { threshold: 0.18, rootMargin: "0px 0px -6% 0px" });

  document.querySelectorAll(".fl-section, .fl-reveal, [data-fl-demo]").forEach(function (el) { io.observe(el); });

  /* Failsafe: if IntersectionObserver doesn't fire (some embed/preview contexts),
     reveal anything in the viewport on load so content never stays hidden. */
  function flRevealInView() {
    document.querySelectorAll(".fl-section:not(.fl-in), .fl-reveal:not(.fl-in)").forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight * 1.12 && r.bottom > -40) {
        el.classList.add("fl-in");
        if (el.__demo) el.__demo.start();
      }
    });
    document.querySelectorAll("[data-fl-demo]").forEach(function (el) {
      if (!el.__demo || el.__started) return;
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight * 1.12 && r.bottom > -40) { el.__started = true; el.__demo.start(); }
    });
  }
  window.addEventListener("load", function () { flRevealInView(); setTimeout(flRevealInView, 450); });
  setTimeout(flRevealInView, 300);

  /* ---------- Number ticker (loops while in view) ---------- */
  function makeTicker(el, opts) {
    var values = opts.values, idx = 0, raf = null, timer = null, running = false;
    function animateTo(from, to, dur, money) {
      var start = null;
      function step(ts) {
        if (!running) return;
        if (start === null) start = ts;
        var p = Math.min((ts - start) / dur, 1);
        var e = 1 - Math.pow(1 - p, 3);
        var v = from + (to - from) * e;
        el.firstChild ? (el.childNodes[0].nodeValue = money ? fmtMoney(v) : v.toFixed(opts.dp || 0))
                      : (el.textContent = money ? fmtMoney(v) : v.toFixed(opts.dp || 0));
        if (p < 1) raf = requestAnimationFrame(step);
      }
      raf = requestAnimationFrame(step);
    }
    function cycle() {
      if (!running) return;
      var from = values[idx];
      idx = (idx + 1) % values.length;
      var to = values[idx];
      animateTo(from, to, 900, opts.money);
      timer = setTimeout(cycle, 2200);
    }
    return {
      start: function () {
        if (running) return; running = true;
        // set initial
        var v0 = values[idx];
        if (el.childNodes[0]) el.childNodes[0].nodeValue = opts.money ? fmtMoney(v0) : v0.toFixed(opts.dp || 0);
        else el.textContent = opts.money ? fmtMoney(v0) : v0.toFixed(opts.dp || 0);
        if (reduce) { return; }
        timer = setTimeout(cycle, 1100);
      },
      stop: function () { running = false; if (raf) cancelAnimationFrame(raf); if (timer) clearTimeout(timer); }
    };
  }

  /* ---------- Demo 1: live map + calc ---------- */
  document.querySelectorAll('[data-fl-demo="live"]').forEach(function (root) {
    var numEl = root.querySelector(".fl-d-calc__num");      // holds "12,74" textnode + <small>
    var bar = root.querySelector(".fl-d-bar span");
    var map = root.querySelector(".fl-d-map");
    var seq = [10.2, 12.74, 9.6, 14.1, 11.3];                // млн ₽
    var bars = [56, 72, 48, 84, 64];
    var i = 0, t = null, running = false;
    function setNum(v) {
      // first child node is the number text; keep the <small> intact
      if (numEl.firstChild && numEl.firstChild.nodeType === 3) numEl.firstChild.nodeValue = v.toFixed(2).replace(".", ",") + " ";
    }
    function tick() {
      if (!running) return;
      i = (i + 1) % seq.length;
      setNum(seq[i]); if (bar) bar.style.width = bars[i] + "%";
      t = setTimeout(tick, 2400);
    }
    root.__demo = {
      start: function () {
        if (running) return; running = true;
        if (map) map.classList.add("go");
        setNum(seq[i]); if (bar) bar.style.width = bars[i] + "%";
        if (!reduce) t = setTimeout(tick, 1600);
      },
      stop: function () { running = false; if (t) clearTimeout(t); if (map) map.classList.remove("go"); }
    };
    io.observe(root);
  });

  /* ---------- Demo 2: budget fit (staged auto-pick) ---------- */
  document.querySelectorAll('[data-fl-demo="budget"]').forEach(function (root) {
    var picks = [].slice.call(root.querySelectorAll(".fl-pick"));
    var sumEl = root.querySelector(".fl-d2__sum b");
    var wrap = root.querySelector(".fl-d2");
    var prices = picks.map(function (p) { return parseInt(p.getAttribute("data-price"), 10) || 0; });
    var fitCount = parseInt(root.getAttribute("data-fit") || picks.length, 10);
    var t = null, running = false, step = 0;
    function reset() {
      picks.forEach(function (p) { p.classList.remove("on", "skip"); });
      if (wrap) wrap.classList.remove("fit");
      if (sumEl) sumEl.textContent = "0";
      step = 0;
    }
    function advance() {
      if (!running) return;
      if (step < picks.length) {
        var p = picks[step];
        if (step < fitCount) {
          p.classList.add("on");
          var sum = prices.slice(0, step + 1).reduce(function (a, b) { return a + b; }, 0);
          if (sumEl) sumEl.textContent = (sum / 1000000).toFixed(2).replace(".", ",") + " млн";
        } else {
          p.classList.add("skip");
        }
        step++;
        t = setTimeout(advance, step === fitCount ? 760 : 620);
      } else {
        if (wrap) wrap.classList.add("fit");
        t = setTimeout(function () { reset(); t = setTimeout(advance, 700); }, 2600);
      }
    }
    root.__demo = {
      start: function () {
        if (running) return; running = true; reset();
        if (reduce) {
          picks.forEach(function (p, k) { p.classList.add(k < fitCount ? "on" : "skip"); });
          var sum = prices.slice(0, fitCount).reduce(function (a, b) { return a + b; }, 0);
          if (sumEl) sumEl.textContent = (sum / 1000000).toFixed(2).replace(".", ",") + " млн";
          if (wrap) wrap.classList.add("fit");
          return;
        }
        t = setTimeout(advance, 800);
      },
      stop: function () { running = false; if (t) clearTimeout(t); }
    };
    io.observe(root);
  });

  /* ---------- Demo 3: compare A/B counter ---------- */
  document.querySelectorAll('[data-fl-demo="compare"]').forEach(function (root) {
    var nums = [].slice.call(root.querySelectorAll(".fl-cc__num [data-val]"));
    root.__demo = {
      start: function () {
        nums.forEach(function (el) {
          var to = parseFloat(el.getAttribute("data-val"));
          if (reduce) { el.textContent = to.toFixed(2).replace(".", ","); return; }
          var start = null;
          function step(ts) {
            if (start === null) start = ts;
            var p = Math.min((ts - start) / 1000, 1), e = 1 - Math.pow(1 - p, 3);
            el.textContent = (to * e).toFixed(2).replace(".", ",");
            if (p < 1) requestAnimationFrame(step);
          }
          requestAnimationFrame(step);
        });
      },
      stop: function () {}
    };
    io.observe(root);
  });

  /* ---------- Demo 4: collab map cursors ---------- */
  document.querySelectorAll('[data-fl-demo="collab"]').forEach(function (root) {
    var map = root.querySelector(".fl-d4__map");
    root.__demo = {
      start: function () { if (map && !reduce) map.classList.add("go"); },
      stop: function () { if (map) map.classList.remove("go"); }
    };
    io.observe(root);
  });
})();
