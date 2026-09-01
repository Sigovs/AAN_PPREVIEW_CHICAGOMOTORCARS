/* ============================================================
   videos.js — videos.html only
   ============================================================

   One behaviour: the YouTube facade.

   A YouTube <iframe> loads Google's player and its cookies for every
   visitor on page load, whether or not anyone presses play. Two of them
   is roughly a megabyte of third-party script spent on nothing, and it
   reports the visit to Google either way. So the page ships a poster
   served from this site, and the iframe is created on click.

   WITHOUT THIS FILE the markup is already correct and complete: each
   facade is an <a> to the video on youtube.com, which is where a click
   was going anyway. Nothing is hidden, nothing is broken, and no state
   is written that a missing script would leave dangling.
   ============================================================ */
(function () {
  'use strict';

  var facades = [].slice.call(document.querySelectorAll('.vd-embed[data-yt]'));
  if (!facades.length) return;

  facades.forEach(function (a) {
    var id = a.getAttribute('data-yt');
    if (!id || !/^[A-Za-z0-9_-]{6,20}$/.test(id)) return;

    a.addEventListener('click', function (e) {
      /* Let the browser do its normal thing for a new-tab click, a
         middle click, or a right click — hijacking those is how a
         facade stops behaving like the link it claims to be. */
      if (e.defaultPrevented || e.button !== 0 ||
          e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

      var frame = a.querySelector('.vd-embed__frame');
      if (!frame || frame.querySelector('iframe')) return;

      e.preventDefault();

      var iframe = document.createElement('iframe');
      /* youtube-nocookie, and autoplay because the visitor has already
         pressed play once — asking them to press it twice is the tax
         every badly built facade charges. */
      iframe.src = 'https://www.youtube-nocookie.com/embed/' + id +
                   '?autoplay=1&rel=0&modestbranding=1';
      iframe.title = (a.querySelector('.vd-item__t') || {}).textContent || 'YouTube video';
      iframe.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
      iframe.setAttribute('allowfullscreen', '');
      iframe.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');

      frame.appendChild(iframe);

      /* The anchor has become a player. It must stop being a link, or a
         click on the video's own controls navigates away to YouTube. */
      a.removeAttribute('href');
      a.removeAttribute('target');
      a.setAttribute('aria-hidden', 'false');

      var play = a.querySelector('.vd-play');
      if (play) play.remove();
      var img = frame.querySelector('img');
      if (img) img.remove();
    });
  });
})();
