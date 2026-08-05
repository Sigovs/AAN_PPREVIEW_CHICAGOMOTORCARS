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
