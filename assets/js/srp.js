/* Chicago Motor Cars — the results head
   ============================================================
   The Vegas port renamed everything: .filterbar became .srp-filters,
   .fpill became .filter, .fopt became .filter__option. main.js still
   carries the blocks written against the old names; they find nothing
   now and return at their first line. This file is the one that drives
   the ported head, and it lives apart from main.js because only this
   page has a head like it.

   The sheet repeats the row's options under their own names, so the two
   are synced BY VALUE — a checkbox and its twin are one fact stated
   twice, kept identical rather than counted twice.
   ============================================================ */
(function () {
  'use strict';

  var head = document.querySelector('.srp-filters');
  if (!head) return;

  var boxes = [].slice.call(head.querySelectorAll('input[type="checkbox"]'));
  if (!boxes.length) return;

  var chips = document.getElementById('srp-chips');
  var count = document.querySelector('.page-head__count');
  var total = count ? count.textContent.trim().split(/\s+of\s+/).pop() : '';
  var cells = [].slice.call(document.querySelectorAll('.veh-cell'));

  /* The option's own label, with its count subtracted — the count is a
     sibling span inside the same <label>, so textContent carries both. */
  function labelOf(box) {
    var wrap = box.closest('.filter__option');
    if (!wrap) return box.value;
    var c = wrap.querySelector('.filter__option-count');
    var s = wrap.textContent;
    if (c) s = s.replace(c.textContent, '');
    return s.trim();
  }

  /* Each card's facts, read off the DOM once. */
  var data = cells.map(function (c) {
    var txt = function (sel) {
      var e = c.querySelector(sel);
      return e ? e.textContent.trim() : '';
    };
    var name = txt('.veh__name');
    var pe = c.querySelector('.veh__pill--price');
    var pills = [].slice.call(c.querySelectorAll('.veh__pill'));
    return {
      cell: c,
      make: txt('.veh__make'),
      body: pills.length ? pills[pills.length - 1].textContent.trim() : '',
      year: Number((name.match(/^(\d{4})/) || [0, 0])[1]),
      price: pe ? Number(pe.textContent.replace(/[^0-9]/g, '')) : 0
    };
  });

  /* The bands are the ones the panels offer, so a label and its filter
     cannot drift apart. */
  var YEAR = {
    '2024 and newer': function (y) { return y >= 2024; },
    '2020 – 2023': function (y) { return y >= 2020 && y <= 2023; },
    '2015 – 2019': function (y) { return y >= 2015 && y <= 2019; },
    'Before 2015': function (y) { return y > 0 && y < 2015; }
  };
  var PRICE = {
    'Under $250,000': function (v) { return v < 250000; },
    '$250,000 – $500,000': function (v) { return v >= 250000 && v < 500000; },
    '$500,000 – $750,000': function (v) { return v >= 500000 && v < 750000; },
    '$750,000 and above': function (v) { return v >= 750000; }
  };

  function chosen(kind) {
    var seen = {};
    boxes.forEach(function (b) {
      if (b.checked && (b.name || '').indexOf(kind) === 0) seen[labelOf(b)] = 1;
    });
    return Object.keys(seen);
  }

  function apply() {
    var mk = chosen('make');
    var bd = chosen('bodystyle');
    var yr = chosen('year');
    var pr = chosen('price');
    var shown = 0;

    data.forEach(function (d) {
      var ok = (!mk.length || mk.indexOf(d.make) > -1) &&
               (!bd.length || bd.indexOf(d.body) > -1) &&
               (!yr.length || yr.some(function (k) { return YEAR[k] && YEAR[k](d.year); })) &&
               (!pr.length || pr.some(function (k) { return PRICE[k] && PRICE[k](d.price); }));
      d.cell.hidden = !ok;
      if (ok) shown++;
    });

    if (count) count.innerHTML = '<b>' + shown + '</b> of ' + total;
    var showN = head.querySelector('.filter-all__foot .btn b');
    if (showN) showN.textContent = String(shown);
  }

  /* One fact, however many boxes state it. */
  function setAll(label, on) {
    boxes.forEach(function (b) { if (labelOf(b) === label) b.checked = on; });
    sync();
  }

  function renderChips() {
    if (!chips) return;
    var names = [];
    boxes.forEach(function (b) {
      var l = labelOf(b);
      if (b.checked && names.indexOf(l) < 0) names.push(l);
    });

    chips.hidden = names.length === 0;
    chips.textContent = '';

    names.forEach(function (name) {
      var chip = document.createElement('span');
      chip.className = 'chip';
      chip.appendChild(document.createTextNode(name));

      var x = document.createElement('button');
      x.type = 'button';
      x.setAttribute('aria-label', 'Remove filter ' + name);
      x.textContent = '×';
      x.addEventListener('click', function () { setAll(name, false); });

      chip.appendChild(x);
      chips.appendChild(chip);
    });

    if (names.length) {
      var clear = document.createElement('button');
      clear.className = 'chip-clear';
      clear.type = 'button';
      clear.textContent = 'Clear all';
      clear.addEventListener('click', function () {
        boxes.forEach(function (b) { b.checked = false; });
        sync();
      });
      chips.appendChild(clear);
    }
  }

  function syncTiles() {
    [].slice.call(document.querySelectorAll('.popular-makes__item')).forEach(function (t) {
      var m = t.getAttribute('data-make');
      var on = boxes.some(function (b) { return b.checked && labelOf(b) === m; });
      t.setAttribute('aria-pressed', String(on));
    });
  }

  function sync() {
    renderChips();
    apply();
    syncTiles();
  }

  head.addEventListener('change', function (e) {
    if (!e.target || e.target.type !== 'checkbox') return;
    setAll(labelOf(e.target), e.target.checked);
  });

  [].slice.call(head.querySelectorAll('.filter__clear')).forEach(function (btn) {
    btn.addEventListener('click', function () {
      var panel = btn.closest('.filter__panel');
      if (!panel) return;
      [].slice.call(panel.querySelectorAll('input')).forEach(function (b) { b.checked = false; });
      sync();
    });
  });

  var reset = head.querySelector('.filter-all__foot .chip-clear');
  if (reset) {
    reset.addEventListener('click', function () {
      boxes.forEach(function (b) { b.checked = false; });
      sync();
    });
  }

  /* Show N closes the sheet. The filtering already happened on each
     change, so it confirms nothing — it is the way out, and its number
     is the result about to be looked at. */
  var showBtn = head.querySelector('.filter-all__foot .btn');
  var allPanel = document.getElementById('f-all');
  if (showBtn && allPanel) {
    showBtn.addEventListener('click', function () { allPanel.open = false; });
  }

  /* The marque tiles are the Make filter said shorter — same values, same
     counts — so pressing one ticks its checkbox rather than holding a
     second state of its own. */
  [].slice.call(document.querySelectorAll('.popular-makes__item')).forEach(function (t) {
    t.addEventListener('click', function () {
      var m = t.getAttribute('data-make');
      var on = boxes.some(function (b) { return b.checked && labelOf(b) === m; });
      setAll(m, !on);
    });
  });

  /* <details> has no idea its siblings exist, so every panel opened
     stayed open. One at a time; outside click and Escape close. */
  var panels = [].slice.call(head.querySelectorAll('details'));

  panels.forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (!d.open) return;
      panels.forEach(function (o) { if (o !== d) o.open = false; });
    });
  });

  document.addEventListener('click', function (e) {
    if (head.contains(e.target)) return;
    panels.forEach(function (d) { d.open = false; });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var open = panels.filter(function (d) { return d.open; })[0];
    if (!open) return;
    open.open = false;
    var s = open.querySelector('summary');
    if (s) s.focus();
  });

  sync();
})();
