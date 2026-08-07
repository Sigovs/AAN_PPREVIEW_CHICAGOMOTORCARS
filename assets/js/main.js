/* Chicago Motor Cars — main
   The page is complete without this file. Everything here adds a
   convenience; nothing here is the only way to reach content.

   The chapter-rail observer and the hero reel were removed with the
   sections they drove. Both are in git at efd7a40 and come back with
   their markup, not before — a guarded IIFE that returns early on a
   page with no matching elements is still dead code asking to be read. */

(function () {
  'use strict';

  var toggle = document.querySelector('.menu-toggle');
  var menu = document.getElementById('site-menu');
  if (!toggle || !menu) return;

  // The menu markup ships `hidden` so a failed script leaves a page
  // with a visible header and a working hero, never a stuck overlay.
  // Script present → the toggle becomes real.
  document.documentElement.classList.add('has-js');

  function setOpen(open) {
    toggle.setAttribute('aria-expanded', String(open));
    menu.hidden = !open;
    // The page scrolls now, so without this the document slides around
    // behind the overlay and the visitor loses their place.
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) {
      var first = menu.querySelector('a');
      if (first) first.focus();
    }
  }

  toggle.addEventListener('click', function () {
    setOpen(toggle.getAttribute('aria-expanded') !== 'true');
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      setOpen(false);
      toggle.focus();
    }
  });

  menu.addEventListener('click', function (e) {
    if (e.target.closest('a')) setOpen(false);
  });

  // Close only if the toggle itself has gone away — it used to close on
  // every resize into desktop, which is now wrong: the condensed header
  // puts a real toggle on desktop too, and closing the panel out from
  // under someone who deliberately opened it is worse than leaving it.
  window.addEventListener('resize', function () {
    if (toggle.getAttribute('aria-expanded') !== 'true') return;
    if (getComputedStyle(toggle).display === 'none') setOpen(false);
  });

  /* The header condenses once it has left the hero. IntersectionObserver
     on a sentinel rather than a scroll listener: the answer changes
     twice in the life of the page, so it should not be recomputed on
     every frame of every scroll. */
  var sentinel = document.querySelector('.scroll-sentinel');
  if (sentinel && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      var past = !entries[0].isIntersecting;
      document.documentElement.classList.toggle('is-condensed', past);
      // A dropdown left open would hang under a bar that no longer
      // shows the word that opened it.
      if (past) {
        document.querySelectorAll('.navmenu__trigger[aria-expanded="true"]')
          .forEach(function (t) {
            t.setAttribute('aria-expanded', 'false');
            var p = document.getElementById(t.getAttribute('aria-controls'));
            if (p) p.hidden = true;
          });
      }
    }, { threshold: 0 }).observe(sentinel);
  }
})();

/* The navigation bar's dropdowns.

   Hover opens them for a pointer, but hover is never the ONLY way in:
   the triggers are real <button>s that open on click and on Enter or
   Space, because a route that cannot be found without a pointer is not
   a route. Escape closes and returns focus to the trigger it came from.

   The panels ship in the markup rather than being built here, so with
   the script gone the mobile breakpoint stands every panel open and all
   four groups stay reachable. */
(function () {
  'use strict';

  var bar = document.querySelector('.navbar');
  if (!bar) return;

  var menus = [].slice.call(bar.querySelectorAll('.navmenu')).map(function (m) {
    return { trigger: m.querySelector('.navmenu__trigger'), panel: m.querySelector('.navmenu__panel') };
  }).filter(function (m) { return m.trigger && m.panel; });
  if (!menus.length) return;

  var closeTimer = null;

  function show(target) {
    menus.forEach(function (m) {
      var on = m === target;
      m.trigger.setAttribute('aria-expanded', String(on));
      m.panel.hidden = !on;
    });
  }
  function closeAll() { show(null); }

  menus.forEach(function (m) {
    m.trigger.addEventListener('click', function () {
      var open = m.trigger.getAttribute('aria-expanded') === 'true';
      open ? closeAll() : show(m);
    });
    // Pointer users get it on hover; the click path above still works.
    m.trigger.addEventListener('mouseenter', function () {
      clearTimeout(closeTimer);
      show(m);
    });
  });

  // A small grace period, or the panel closes while the pointer is
  // crossing the gap between the trigger and the panel below it.
  bar.addEventListener('mouseleave', function () {
    closeTimer = setTimeout(closeAll, 180);
  });
  bar.addEventListener('mouseenter', function () { clearTimeout(closeTimer); });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var open = menus.filter(function (m) { return m.trigger.getAttribute('aria-expanded') === 'true'; })[0];
    if (!open) return;
    closeAll();
    open.trigger.focus();
  });

  // Tabbing out of the bar entirely, or clicking away, closes it.
  document.addEventListener('focusin', function (e) {
    if (!bar.contains(e.target)) closeAll();
  });
  document.addEventListener('click', function (e) {
    if (!bar.contains(e.target)) closeAll();
  });
})();

/* ============================================================
   FEATURED INVENTORY — the index drives the dominant field
   ============================================================
   Hover or focus a record and the field crossfades to that vehicle.
   Enhancement only: without this script the first car stays up and every
   record is still a link to the inventory, so nothing a visitor needs
   depends on it. Pointer AND focus, so the keyboard gets the same
   behaviour rather than a degraded one. No timers, no autoplay, no
   carousel — the visitor drives it and it holds where they leave it.

   Only records carrying data-frame drive the field. The others are real
   inventory with no cut-out asset yet: they light on hover and they link
   out, but they never take the enlarged active state, because that state
   means "this is the car in the field" and awarding it to a vehicle the
   field is not showing would be the interface telling a lie.
   ============================================================ */
(function () {
  var wrap = document.querySelector('.showcase');
  if (!wrap) return;

  var cars = [].slice.call(wrap.querySelectorAll('.stage__car'));
  var recs = [].slice.call(wrap.querySelectorAll('.rec'));
  if (cars.length < 2) return;

  var driving = recs.filter(function (r) {
    return r.getAttribute('data-frame') !== null;
  });
  if (!driving.length) return;

  // The order the arrows step through is the order the INDEX is written in,
  // read off the DOM — not 0..n. If a record is ever removed or reordered,
  // the arrows follow the list the reader can see rather than a count that
  // has quietly stopped matching it.
  var frames = driving.map(function (r) { return Number(r.getAttribute('data-frame')); });
  var at = 0;

  function show(i) {
    var seat = frames.indexOf(i);
    if (seat !== -1) at = seat;
    cars.forEach(function (c, n) {
      c.classList.toggle('is-active', n === i);
    });
    recs.forEach(function (r) {
      r.classList.toggle('is-active', r.getAttribute('data-frame') === String(i));
    });
  }

  driving.forEach(function (rec) {
    var i = Number(rec.getAttribute('data-frame'));
    rec.addEventListener('mouseenter', function () { show(i); });
    rec.addEventListener('focus', function () { show(i); });
  });

  // Arrows wrap rather than disable at the ends. Four vehicles is a ring,
  // not a document — a dead control at either end would be the only piece
  // of this section that can be pressed and do nothing.
  [].slice.call(wrap.querySelectorAll('.stage__arrow')).forEach(function (btn) {
    var step = Number(btn.getAttribute('data-step'));
    btn.addEventListener('click', function () {
      var next = (at + step + frames.length) % frames.length;
      show(frames[next]);
    });
  });
})();
