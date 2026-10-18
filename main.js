/* Seraphic Order — ambient behaviours.
   Everything here is decorative; the page is complete without it. */
(() => {
  "use strict";

  const d = document;
  d.documentElement.classList.remove("no-js");

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const finePointer = window.matchMedia("(pointer: fine)");

  /* ---- Header: settle once the reader has begun to scroll ------------ */
  const head = d.querySelector(".site-head");
  if (head) {
    const settle = () => head.classList.toggle("is-scrolled", window.scrollY > 40);
    window.addEventListener("scroll", settle, { passive: true });
    settle();
  }

  /* ---- Reveal on approach ------------------------------------------- */
  const reveals = d.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) {
          e.target.classList.add("is-in");
          io.unobserve(e.target);
        }
      }
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach((el) => io.observe(el));
    // Anything already in view on arrival (deep links, restored scroll) is shown at once.
    const showVisible = () => {
      const vh = window.innerHeight || d.documentElement.clientHeight;
      reveals.forEach((el) => {
        if (el.classList.contains("is-in")) return;
        const r = el.getBoundingClientRect();
        if (r.top < vh && r.bottom > 0) { el.classList.add("is-in"); io.unobserve(el); }
      });
    };
    window.addEventListener("load", showVisible, { once: true });
    window.setTimeout(showVisible, 1200);
  } else {
    reveals.forEach((el) => el.classList.add("is-in"));
  }

  /* ---- Mark the chapter currently being read ------------------------ */
  const navLinks = Array.from(d.querySelectorAll(".site-nav a[href^='#']"));
  if ("IntersectionObserver" in window && navLinks.length) {
    const byId = new Map(navLinks.map((a) => [a.getAttribute("href").slice(1), a]));
    const sections = Array.from(byId.keys()).map((id) => d.getElementById(id)).filter(Boolean);
    const setActive = (id) => {
      navLinks.forEach((a) => {
        const on = a.getAttribute("href") === "#" + id;
        a.classList.toggle("is-active", on);
        if (on) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
      });
    };
    const so = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) setActive(e.target.id); });
    }, { rootMargin: "-35% 0px -55% 0px", threshold: 0 });
    sections.forEach((s) => so.observe(s));
    // Clear the mark while the hero is in view.
    const hero = d.querySelector(".hero");
    if (hero) {
      new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) setActive("");
      }, { rootMargin: "-35% 0px -55% 0px" }).observe(hero);
    }
  }

  /* ---- Hero: parallax and the lamp that follows the hand ----------- */
  const hero = d.querySelector(".hero");
  const celestial = d.querySelector(".hero__celestial");
  const inner = d.querySelector(".hero__inner");

  if (hero && !reduceMotion.matches) {
    let ticking = false;
    const drift = () => {
      const y = window.scrollY;
      const vh = window.innerHeight || 1;
      if (y <= vh) {
        if (celestial) celestial.style.transform = "translateY(" + (y * 0.18).toFixed(1) + "px)";
        if (inner) {
          inner.style.transform = "translateY(" + (y * 0.12).toFixed(1) + "px)";
          inner.style.opacity = String(Math.max(0, 1 - y / (vh * 0.85)));
        }
      }
      ticking = false;
    };
    window.addEventListener("scroll", () => {
      if (!ticking) { window.requestAnimationFrame(drift); ticking = true; }
    }, { passive: true });

    if (finePointer.matches) {
      hero.addEventListener("pointermove", (e) => {
        const r = hero.getBoundingClientRect();
        hero.style.setProperty("--mx", ((e.clientX - r.left) / r.width * 100).toFixed(2) + "%");
        hero.style.setProperty("--my", ((e.clientY - r.top) / r.height * 100).toFixed(2) + "%");
        hero.classList.add("has-pointer");
      }, { passive: true });
      hero.addEventListener("pointerleave", () => hero.classList.remove("has-pointer"));
    }
  }

  /* ---- Rain against the tall windows -------------------------------- */
  const canvas = d.querySelector(".hero__rain");
  if (hero && canvas && !reduceMotion.matches && canvas.getContext) {
    const ctx = canvas.getContext("2d", { alpha: true });
    const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    let w = 0, h = 0, drops = [], raf = 0, running = false, last = 0;

    const make = (fresh) => {
      const z = Math.random();              // depth: 0 far, 1 near
      const speed = 260 + z * 420;
      const wind = 16 + z * 14;
      return {
        x: Math.random() * (w + 120) - 60,
        y: fresh ? -40 - Math.random() * 80 : Math.random() * h,
        len: 9 + z * 18,
        speed, wind,
        lean: wind / speed,
        alpha: 0.045 + z * 0.13,
        width: 0.7 + z * 0.6
      };
    };

    const size = () => {
      w = hero.clientWidth; h = hero.clientHeight;
      canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
      canvas.style.width = w + "px"; canvas.style.height = h + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const n = Math.round(Math.min(150, Math.max(40, (w * h) / 13000)));
      drops = Array.from({ length: n }, () => make(false));
    };

    const frame = (t) => {
      if (!running) return;
      const dt = Math.min(0.05, last ? (t - last) / 1000 : 0.016);
      last = t;
      ctx.clearRect(0, 0, w, h);
      ctx.lineCap = "round";
      for (const dr of drops) {
        dr.y += dr.speed * dt;
        dr.x += dr.wind * dt;
        if (dr.y > h + 40 || dr.x > w + 60) Object.assign(dr, make(true));
        ctx.strokeStyle = "rgba(228, 206, 170," + dr.alpha.toFixed(3) + ")";
        ctx.lineWidth = dr.width;
        ctx.beginPath();
        ctx.moveTo(dr.x, dr.y);
        ctx.lineTo(dr.x - dr.len * dr.lean, dr.y - dr.len);
        ctx.stroke();
      }
      raf = window.requestAnimationFrame(frame);
    };

    const start = () => { if (running) return; running = true; last = 0; raf = window.requestAnimationFrame(frame); };
    const stop = () => { running = false; window.cancelAnimationFrame(raf); };

    size();
    let resizeTimer = 0;
    window.addEventListener("resize", () => {
      window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(size, 150);
    }, { passive: true });

    let heroVisible = true;
    new IntersectionObserver((entries) => {
      heroVisible = entries[0].isIntersecting;
      if (heroVisible && !d.hidden) start(); else stop();
    }, { threshold: 0.02 }).observe(hero);
    d.addEventListener("visibilitychange", () => {
      if (d.hidden) stop(); else if (heroVisible) start();
    });
    reduceMotion.addEventListener?.("change", (e) => { if (e.matches) { stop(); ctx.clearRect(0, 0, w, h); } });
  }

  /* ---- The year, kept current --------------------------------------- */
  const year = d.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());
})();
