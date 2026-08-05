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
