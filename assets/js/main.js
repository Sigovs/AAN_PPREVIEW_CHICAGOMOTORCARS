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

/* ============================================================
   THE HERO SLIDER — two slides: the film, then the frame
   ============================================================
   Not a carousel. There is no timer and nothing advances on a clock:
   the film runs once, and reaching its end is what hands the stage to
   the photograph. After that the hero holds where it is until a visitor
   says otherwise. That is the difference between a sequence with an
   ending and a loop that talks over itself.

   Playback is started HERE rather than by an `autoplay` attribute,
   because the attribute begins downloading and playing before anything
   can ask whether this visitor wants motion.

   Under prefers-reduced-motion the film is not merely paused — it never
   loads, the photograph is the hero from the first paint, and the pager
   is removed rather than left showing a choice that has become a lie.

   The fade waits for `canplaythrough`, not `loadeddata`. At 21 MB that
   is the difference between continuous motion and fading in to a stall.
   ============================================================ */
(function () {
  'use strict';

  var hero   = document.querySelector('.hero');
  if (!hero) return;
  var slides  = [].slice.call(hero.querySelectorAll('.hero__slide'));
  var counter = hero.querySelector('.counter');
  var num     = counter && counter.querySelector('.counter__n');
  var video   = hero.querySelector('.hero__video');
  if (slides.length < 2) return;

  var meter  = hero.querySelector('.hero__meter');
  var title  = hero.querySelector('.hero__slide-title');
  var words  = (meter && meter.getAttribute('data-titles') || '')
                 .split(',').map(function (w) { return w.trim(); }).filter(Boolean);
  var word   = 0;

  var at = 0;
  var calm = window.matchMedia('(prefers-reduced-motion: reduce)');

  function pad(n) { return (n < 10 ? '0' : '') + n; }

  /* The arc is restarted by REPLACING the class, not by toggling a
     property: a CSS animation does not rewind while its element keeps
     the class, so a second visit to the film would have shown an arc
     already full. Remove, force a reflow, add back — the one reliable
     retrigger without a second set of keyframes. */
  var STILL_HOLD = 5;          // seconds a still slide is given
  var arc = counter && counter.querySelector('.counter__arc');
  var onArcEnd = null;

  function arm(seconds, andThen) {
    if (!counter) return;
    counter.classList.remove('is-timing', 'is-static');
    void counter.offsetWidth;
    counter.style.setProperty('--run', seconds + 's');
    counter.style.setProperty('--run-state', 'running');
    counter.classList.add('is-timing');

    /* The ADVANCE is driven by the arc's own animationend, not by a
       parallel setTimeout. One clock: whatever the arc shows is what
       actually happens, and a paused arc is a paused slide for free —
       a separate timer would keep counting behind a stopped instrument
       and the two would drift apart within one cycle. */
    if (arc && onArcEnd) arc.removeEventListener('animationend', onArcEnd);
    onArcEnd = null;
    if (arc && andThen) {
      onArcEnd = function () { onArcEnd = null; andThen(); };
      arc.addEventListener('animationend', onArcEnd, { once: true });
    }
  }
  function settle() {
    if (!counter) return;
    counter.classList.remove('is-timing');
    counter.classList.add('is-static');
  }

  /* The word advances on EVERY change of slide — clicked or automatic —
     and it runs its own, longer cycle. It is deliberately not read off
     the slide: with four words over two frames it would otherwise be
     captioning a picture it does not describe. It is the register the
     house speaks in, turning over.

     Crossfaded rather than cut: it is the only thing on this row whose
     content swaps, and a hard swap beside a smoothly running arc reads
     as a glitch. */
  function stepWord() {
    if (!title || words.length < 2) return;
    word = (word + 1) % words.length;
    title.classList.add('is-swapping');
    setTimeout(function () {
      title.textContent = words[word];
      title.classList.remove('is-swapping');
    }, 200);
  }

  function go(i) {
    at = i;
    slides.forEach(function (s, n) { s.classList.toggle('is-current', n === i); });
    if (num) num.textContent = pad(i + 1);
    // Nothing plays while it is not the thing on screen.
    if (video && i !== 0) video.pause();
    /* A still now has a duration too, so it gets a real arc rather than
       an empty ring — five seconds, then it hands back to the film. The
       film is timed by the film itself; see `ended` below. */
    if (i !== 0) {
      if (calm.matches) settle();
      else arm(STILL_HOLD, function () { go(0); stepWord(); restartFilm(); });
    }
  }

  function restartFilm() {
    if (!video || calm.matches) return;
    video.currentTime = 0;
    if (isFinite(video.duration)) arm(video.duration.toFixed(2));
    video.play().catch(function () {});
  }

  if (counter) {
    counter.addEventListener('click', function () {
      var next = (at + 1) % slides.length;
      go(next);
      stepWord();
      if (next === 0) restartFilm();
    });
  }

  /* ---- reduced motion: the photograph IS the hero ---- */
  function standDown() {
    if (video) { video.pause(); video.removeAttribute('src'); video.load(); }
    go(1);
    if (counter) counter.remove();   // one slide reachable, so no instrument
  }

  if (calm.matches) { standDown(); return; }
  calm.addEventListener('change', function (e) { if (e.matches) standDown(); });

  if (!video) return;

  function reveal() { video.classList.add('is-playing'); }

  video.addEventListener('play',  function () {
    if (counter) counter.style.setProperty('--run-state', 'running');
  });
  video.addEventListener('pause', function () {
    if (counter) counter.style.setProperty('--run-state', 'paused');
  });

  video.addEventListener('canplaythrough', function () {
    if (isFinite(video.duration)) arm(video.duration.toFixed(2));
    var p = video.play();
    if (p && typeof p.catch === 'function') p.then(reveal).catch(function () {});
    else reveal();
  }, { once: true });

  // The end of the film is the transition.
  video.addEventListener('ended', function () { go(1); stepWord(); });

  /* ---- Nothing advances past someone who is looking at it ----
     The hero now moves on its own, so it has to stop when a visitor is
     engaged with it. Pointer over the hero, or keyboard focus inside it,
     holds BOTH the film and the arc — and because the arc is the clock,
     holding the arc holds the slide. This is the same protection the
     earlier reel carried, and it is what separates a sequence from a
     carousel that talks over you. */
  function hold(on) {
    if (counter) counter.style.setProperty('--run-state', on ? 'paused' : 'running');
    if (!video) return;
    if (on) video.pause();
    else if (slides[0].classList.contains('is-current')) video.play().catch(function () {});
  }
  hero.addEventListener('mouseenter', function () { hold(true); });
  hero.addEventListener('mouseleave', function () { hold(false); });
  /* Focus holds it only for a KEYBOARD user. Clicking the counter also
     focuses it, and with a plain focusin handler that click paused the
     hero permanently — the visitor stepped one slide and the sequence
     never started again. :focus-visible is exactly the distinction:
     someone navigating by keyboard needs the hold, someone who just
     pressed a button does not.

     The try/catch is not decoration — :focus-visible throws on engines
     that do not know the selector, and a hero that stops advancing
     because of a matches() call would be a poor trade for a nicety. */
  function focusHolds(el) {
    if (!el || el === document.body) return false;
    try { return el.matches(':focus-visible'); }
    catch (e) { return false; }
  }
  hero.addEventListener('focusin', function (e) {
    if (focusHolds(e.target)) hold(true);
  });
  hero.addEventListener('focusout', function (e) {
    if (!hero.contains(e.relatedTarget)) hold(false);
  });

  document.addEventListener('visibilitychange', function () {
    hold(document.hidden);
  });

  video.load();
})();

/* ============================================================
   HERO SEARCH — a row knows whether it has been answered
   ============================================================
   CSS alone cannot ask this. :placeholder-shown does not apply to
   <select>, and :has() cannot test a select's VALUE — only its
   structure — so the one honest way to tell an empty control from an
   answered one is to read it.

   Two lines of state, and it also runs on load: a browser restoring
   form values after a back-navigation would otherwise show four filled
   selects behind four empty-looking labels.
   ============================================================ */
(function () {
  'use strict';

  var rows = [].slice.call(document.querySelectorAll('.hunt__field'));
  if (!rows.length) return;

  rows.forEach(function (row) {
    var control = row.querySelector('.hunt__control');
    var out     = row.querySelector('.hunt__value');
    if (!control) return;
    function sync() {
      var filled = control.value !== '';
      row.classList.toggle('is-filled', filled);
      /* The visible value is a span, not the select's own text: the
         select is an invisible sheet covering the row, so it has no text
         to show. Writing the chosen option's label here is what keeps
         the row readable — and it reads the OPTION rather than the raw
         value, so what appears is exactly what was picked from the list. */
      if (out) out.textContent = filled ? control.options[control.selectedIndex].text : '';
    }
    control.addEventListener('change', sync);
    sync();
  });
})();
