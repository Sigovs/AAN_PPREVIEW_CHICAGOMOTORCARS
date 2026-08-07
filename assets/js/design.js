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

  /* Print the family a specimen is ACTUALLY rendering in. The prose on
     this page was hand-typed and went stale the moment the tokens moved
     — it still said Bodoni long after the display face had become a
     grotesque. A page that measures its own contrast and then lies
     about its own typefaces is worse than one that does neither. */
  document.querySelectorAll('[data-face]').forEach(function (el) {
    var target = el.getAttribute('data-face');
    var node = target ? el.closest('[data-measure-row], .row, .spec')
                          .querySelector(target) : el;
    if (!node) return;
    var cs = getComputedStyle(node);
    var fam = cs.fontFamily.split(',')[0].replace(/["']/g, '');
    var out = document.createElement('span');
    out.textContent = fam + ' ' + cs.fontWeight;
    el.textContent = '';
    el.appendChild(out);
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

  /* Counts printed from the DOM. "Five rules were being broken" was
     typed by hand and was wrong the moment a sixth finding was added —
     the same staleness that let the prose claim Bodoni. Anything the
     sheet counts about itself, it counts at runtime. */
  var WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six',
               'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve'];
  document.querySelectorAll('[data-count]').forEach(function (el) {
    var n = document.querySelectorAll(el.getAttribute('data-count')).length;
    el.textContent = WORDS[n] || String(n);
  });

  /* ---- The sheet audits itself -------------------------------------
     The measurement above only ever looked at elements carrying
     data-measure, so anything nobody thought to tag was never checked.
     .finding__rule sat at 3.43:1 for the whole life of this page for
     exactly that reason. This sweeps EVERY leaf text element on the
     page against its own composited ground and reports the total —
     a sheet that can only find the defects it was pointed at is not
     an audit, it is a demonstration. */
  var checked = 0, failed = [];
  document.querySelectorAll('p, span, li, dd, dt, a, code, em, b, label, button, h1, h2, h3')
    .forEach(function (el) {
      if (el.children.length || !el.textContent.trim()) return;
      if (el.closest('.ratio, .audit')) return;
      var cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none') return;
      var fg = parse(cs.color);
      if (!fg) return;
      var bg = groundOf(el);
      var r = ratio(over(fg, bg), bg);
      checked++;
      if (r < required(el)) {
        failed.push(el.className.split(' ')[0] || el.tagName.toLowerCase());
        el.setAttribute('data-aa-fail', r.toFixed(2));
      }
    });

  document.querySelectorAll('[data-audit]').forEach(function (el) {
    el.textContent = failed.length
      ? checked + ' text elements swept · ' + failed.length + ' below AA: ' +
        failed.filter(function (v, i, a) { return a.indexOf(v) === i; }).join(', ')
      : checked + ' text elements swept on painted grounds · none below AA';
    el.className += failed.length ? ' audit--fail' : ' audit--pass';
  });
})();
