/* ============================================================
   financing.js — financing.html only
   ============================================================

   A page-local file, on srp.js's precedent, rather than 90 more lines
   in main.js. Two behaviours, both of which degrade to something
   complete when this file does not run:

     - the estimator computes a monthly figure from the four controls;
       with no script the controls are still real inputs and the figure
       reads an em dash, which is what it says before any rate is given
       anyway.
     - the trade form validates on submit, using .field--error and
       .field__error — states main.css has carried since the beginning
       and which nothing on the site used until now. With no script the
       browser's own required/type validation stands.

   The credit application is deliberately absent from both. It is the
   lender's hosted form and this page only frames it.
   ============================================================ */
(function () {
  'use strict';

  /* ---- money ---------------------------------------------------------
     Intl is not asked for a currency symbol: the dollar sign in the
     figure is its own element, set two thirds the size of the digits,
     and a symbol baked into the string would arrive at digit size. */
  var money0 = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 });

  function digits(v) {
    var n = parseFloat(String(v).replace(/[^0-9.]/g, ''));
    return isFinite(n) ? n : 0;
  }

  /* ============================================================
     1 — THE ESTIMATOR
     ============================================================ */
  (function estimator() {
    var form = document.getElementById('fn-calc');
    if (!form) return;

    var price = document.getElementById('fn-price');
    var down  = document.getElementById('fn-down');
    var term  = document.getElementById('fn-term');
    var apr   = document.getElementById('fn-apr');

    var outMonthly  = form.querySelector('[data-fn-out]');
    var outFinanced = form.querySelector('[data-fn-financed]');
    var outTotal    = form.querySelector('[data-fn-total]');
    var outInterest = form.querySelector('[data-fn-interest]');
    if (!price || !down || !term || !apr || !outMonthly) return;

    var DASH = '—';

    function compute() {
      var p = digits(price.value);
      var d = digits(down.value);
      var n = parseInt(term.value, 10) || 0;
      var financed = Math.max(p - d, 0);

      /* The rate field opens empty on purpose — this site does not
         publish a rate — so an empty or unparseable APR is the normal
         state, not an error. The page says so rather than showing a
         number it had to invent. */
      var raw = apr.value.replace(/[^0-9.]/g, '');
      var hasRate = raw !== '' && isFinite(parseFloat(raw));
      var r = hasRate ? parseFloat(raw) / 100 / 12 : null;

      outFinanced.textContent = financed > 0 ? '$' + money0.format(financed) : DASH;

      if (!financed || !n || r === null) {
        outMonthly.textContent = DASH;
        outTotal.textContent = DASH;
        outInterest.textContent = DASH;
        return;
      }

      var monthly = r === 0
        ? financed / n
        : financed * r / (1 - Math.pow(1 + r, -n));

      if (!isFinite(monthly) || monthly <= 0) {
        outMonthly.textContent = DASH;
        outTotal.textContent = DASH;
        outInterest.textContent = DASH;
        return;
      }

      var total = monthly * n;
      outMonthly.textContent  = money0.format(Math.round(monthly));
      outTotal.textContent    = '$' + money0.format(Math.round(total));
      outInterest.textContent = '$' + money0.format(Math.round(total - financed));
    }

    /* Thousands separators as you type. The caret is put back at the
       end only when the edit WAS at the end — reformatting mid-string
       and then jumping the caret is how these fields become unusable
       for anyone correcting a middle digit. */
    function group(el) {
      var atEnd = el.selectionStart === el.value.length;
      var n = digits(el.value);
      var next = el.value === '' ? '' : money0.format(n);
      if (next !== el.value) {
        el.value = next;
        if (atEnd) { try { el.setSelectionRange(next.length, next.length); } catch (e) {} }
      }
    }

    [price, down].forEach(function (el) {
      el.addEventListener('input', function () { group(el); compute(); });
    });
    [term, apr].forEach(function (el) {
      el.addEventListener('input', compute);
      el.addEventListener('change', compute);
    });

    form.addEventListener('submit', function (e) { e.preventDefault(); compute(); });

    compute();
  })();


  /* ============================================================
     2 — VALIDATION, ON THE PROJECT'S OWN ERROR STATE
     ============================================================
     One routine for both forms. It marks the .field wrapper rather
     than the control, because .field--error is what main.css keys the
     red rule off, and it writes the message into a .field__error the
     script creates once and reuses. */
  function wrapperOf(el) {
    var n = el;
    while (n && n !== document.body) {
      if (n.classList && n.classList.contains('field')) return n;
      n = n.parentNode;
    }
    return null;
  }

  function setError(el, message) {
    var w = wrapperOf(el);
    if (!w) return;
    var msg = w.querySelector('.field__error');
    if (message) {
      if (!msg) {
        msg = document.createElement('p');
        msg.className = 'field__error';
        msg.id = el.id + '-err';
        w.appendChild(msg);
      }
      msg.textContent = message;
      w.classList.add('field--error');
      el.setAttribute('aria-invalid', 'true');
      el.setAttribute('aria-describedby', msg.id);
    } else {
      if (msg) msg.remove();
      w.classList.remove('field--error');
      el.removeAttribute('aria-invalid');
      if (el.getAttribute('aria-describedby') === el.id + '-err') {
        el.removeAttribute('aria-describedby');
      }
    }
  }

  function check(el) {
    var v = el.value.trim();
    if (el.hasAttribute('required') && !v) return 'Required.';
    if (v && el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) {
      return 'That address is not complete.';
    }
    if (v && el.type === 'tel' && v.replace(/[^0-9]/g, '').length < 10) {
      return 'Ten digits, please.';
    }
    return '';
  }

  function wire(formId, noteText) {
    var form = document.getElementById(formId);
    if (!form) return;
    var controls = [].slice.call(form.querySelectorAll('input, select'));
    var note = form.querySelector('[data-fn-formnote]');

    /* Errors clear as the field is corrected, and are only RAISED on
       submit or on leaving a field that has already failed once. A
       field that reddens on the third keystroke of a valid address is
       the failure this ordering avoids. */
    controls.forEach(function (el) {
      el.addEventListener('input', function () {
        if (wrapperOf(el) && wrapperOf(el).classList.contains('field--error')) {
          setError(el, check(el));
        }
      });
      el.addEventListener('blur', function () {
        if (el.value.trim()) setError(el, check(el));
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var first = null;
      controls.forEach(function (el) {
        var m = check(el);
        setError(el, m);
        if (m && !first) first = el;
      });
      if (first) {
        first.focus();
        if (note) note.textContent = 'Check the fields marked above.';
        return;
      }
      if (note) note.textContent = noteText;
    });
  }

  /* The trade appraisal only. The credit application is the lender's
     hosted form and this file must not go near it — validating a guest
     iframe is not possible and pretending to is worse than leaving it
     alone. CMC's live trade tool is their own (no vendor host on
     /trade-in-car-chicago-il/, read 2026-08-30), so this one is ours to
     build. */
  wire('fn-trade-form', 'Preview build — the fields are valid and nothing was transmitted.');
})();
