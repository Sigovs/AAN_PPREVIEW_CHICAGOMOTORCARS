/* Chicago Motor Cars — design system page
   The page measures its own contrast at runtime. Every swatch and every
   type rank reads its OWN computed colour against its OWN computed
   ground, composites the alpha, and prints the ratio. Nothing here is
   typed in by hand, so the numbers cannot drift away from the tokens. */

(function () {
  'use strict';

  function parse(c) {
    var m = c.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    var p = m[1].split(/[,\s/]+/).filter(Boolean).map(Number);
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  }

  function lin(v) {
    v /= 255;
    return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  }

  function lum(c) {
    return 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b);
  }

  function over(fg, bg) {
    return {
      r: fg.a * fg.r + (1 - fg.a) * bg.r,
      g: fg.a * fg.g + (1 - fg.a) * bg.g,
      b: fg.a * fg.b + (1 - fg.a) * bg.b,
      a: 1
    };
  }

  function ratio(fg, bg) {
    var a = lum(fg), b = lum(bg);
    var hi = Math.max(a, b), lo = Math.min(a, b);
    return (hi + 0.05) / (lo + 0.05);
  }

  /* The nearest ancestor that actually paints a background. */
  function groundOf(el) {
    var node = el;
    while (node && node !== document.documentElement) {
      var bg = parse(getComputedStyle(node).backgroundColor);
      if (bg && bg.a > 0.95) return bg;
      node = node.parentElement;
    }
    return { r: 11, g: 11, b: 12, a: 1 };
  }

  /* AA threshold for the element's own rendered size and weight. */
  function required(el) {
    var cs = getComputedStyle(el);
    var px = parseFloat(cs.fontSize);
    var w = parseInt(cs.fontWeight, 10) || 400;
    var large = px >= 24 || (px >= 18.66 && w >= 700);
    return large ? 3 : 4.5;
  }

  document.querySelectorAll('[data-measure]').forEach(function (el) {
    var fg = parse(getComputedStyle(el).color);
    var bg = groundOf(el);
    if (!fg) return;

    var r = ratio(over(fg, bg), bg);
    var need = required(el);
    var pass = r >= need;

    var tag = document.createElement('span');
    tag.className = 'ratio' + (pass ? '' : ' ratio--fail');
    tag.textContent = r.toFixed(2) + ':1 · ' + (pass ? 'AA' : 'FAILS ' + need);

    var slot = el.closest('[data-measure-row]');
    (slot ? slot.querySelector('[data-ratio-slot]') || slot : el.parentElement)
      .appendChild(tag);
  });

  /* Print the resolved value of every token named on the page, so the
     swatch and the number can never disagree. */
  var root = getComputedStyle(document.documentElement);
  document.querySelectorAll('[data-token]').forEach(function (el) {
    var name = el.getAttribute('data-token');
    var v = root.getPropertyValue(name).trim();
    var out = el.querySelector('[data-token-value]');
    if (out) out.textContent = v || '—';
  });
})();
