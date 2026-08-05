/* Chicago Motor Cars — main
   The page is complete without this file. Everything here adds a
   convenience; nothing here is the only way to reach content. */

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

  // A menu left open across a resize into the desktop layout would
  // cover a page that already shows its navigation.
  var wide = window.matchMedia('(min-width: 901px)');
  wide.addEventListener('change', function (e) {
    if (e.matches) setOpen(false);
  });
})();

/* The chapter rail marks where you are. IntersectionObserver, not a
   scroll listener — no work on every frame, and no hijacking: the user
   keeps the scrollbar. The rail also inverts over the light chapter,
   because a dim rail on bone is invisible. */
(function () {
  'use strict';
  var rail = document.querySelector('.chapters');
  if (!rail || !('IntersectionObserver' in window)) return;

  var links = [].slice.call(rail.querySelectorAll('a'));
  var map = {};
  links.forEach(function (a) {
    var id = a.getAttribute('href').slice(1);
    var el = document.getElementById(id);
    if (el) map[id] = { link: a, el: el };
  });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      var rec = map[e.target.id];
      if (!rec) return;
      if (e.isIntersecting) {
        links.forEach(function (a) { a.classList.remove('is-here'); });
        rec.link.classList.add('is-here');
        rail.classList.toggle('on-light', e.target.classList.contains('record'));
      }
    });
  }, { rootMargin: '-45% 0px -45% 0px' });

  Object.keys(map).forEach(function (id) { io.observe(map[id].el); });
})();

/* The reel. One ambient moment on the page and this is it — the whole
   budget, spent here. It advances on its own so the opening has
   momentum, pauses whenever a person is looking at or touching it, and
   does not exist at all under prefers-reduced-motion: there the first
   slide simply stands, complete on its own. Nothing here is required to
   read the page — with the script gone, slide one is the hero. */
(function () {
  'use strict';
  var reel = document.querySelector('.reel');
  if (!reel) return;

  var slides = [].slice.call(reel.querySelectorAll('.reel__slide'));
  var dots = [].slice.call(reel.querySelectorAll('.reel__dot'));
  if (slides.length < 2) return;

  var calm = matchMedia('(prefers-reduced-motion: reduce)');
  var i = 0, timer = null;
  var HOLD = 7000;

  function show(n) {
    i = (n + slides.length) % slides.length;
    slides.forEach(function (s, k) {
      s.classList.toggle('is-on', k === i);
      s.setAttribute('aria-hidden', String(k !== i));
    });
    dots.forEach(function (d, k) {
      d.classList.toggle('is-on', k === i);
      d.setAttribute('aria-selected', String(k === i));
    });
  }

  function play()  { if (!calm.matches && !timer) timer = setInterval(function () { show(i + 1); }, HOLD); }
  function pause() { clearInterval(timer); timer = null; }

  dots.forEach(function (d, k) {
    d.addEventListener('click', function () { pause(); show(k); play(); });
    d.addEventListener('focus', pause);
  });

  reel.addEventListener('mouseenter', pause);
  reel.addEventListener('mouseleave', play);
  reel.addEventListener('focusin', pause);
  reel.addEventListener('focusout', play);
  document.addEventListener('visibilitychange', function () {
    document.hidden ? pause() : play();
  });
  calm.addEventListener('change', function (e) { e.matches ? pause() : play(); });

  play();
})();
