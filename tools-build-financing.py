#!/usr/bin/env python3
"""Assemble financing.html from index_3.html's head, masthead and footer.

Same principle as tools-build-our-dealership.py: anything shared is COPIED
at build time rather than retyped, so the pages cannot drift. index_3 is
the source because it is the approved variant.

It writes financing.html and NOTHING ELSE. The inventory builder once wrote
srp.html as well and deleted 525 lines of hand-maintained head; a script
that can only create the one file it is named after cannot repeat that.

NOTE ON THE FIRST BUILD. Python is not installed on the machine this page
was authored on, so the artefact was produced by a one-off transliteration
of this script and then verified in the browser. If a regeneration here
ever differs from the committed financing.html, THIS file is the authority
and the difference is a bug in the transliteration, not in the page.
"""
import re, os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(ROOT, "financing.html")
src  = open(os.path.join(ROOT, "index_3.html"), encoding="utf-8").read()

# The five Financing destinations in the copied masthead still point at the
# homepage. They are repointed HERE rather than in index_3, because this
# script must never write a file it is not named after.
FIN_LABELS = [
    "Online Credit Approval",
    "Calculate Payments",
    "Calculate Your Trade",
    "Purchase with BitPay",
    "Trucks &amp; Equipment Online Credit Approval",
    # the footer sets the same five in sentence case
    "Online credit approval",
    "Calculate payments",
    "Calculate your trade",
    "Trucks &amp; Equipment online credit approval",
]


def cut(start, end):
    """Slice src between two literals, refusing to guess."""
    a = src.find(start)
    b = src.find(end, a + 1) if a != -1 else -1
    if a == -1 or b == -1:
        raise SystemExit("ABORT: could not find %r .. %r in index_3.html" % (start, end))
    return src[a:b + len(end)]


head    = cut("<head>", "</head>")
header  = cut('<span class="scroll-sentinel"', "</header>")
between = src[src.index("</header>") + len("</header>"):src.index("<main>")]
footer  = cut('<footer class="foot">', "</footer>")
m = re.search(r'<script src="assets/js/main\.js\?v=\d+" defer></script>', src)
if not m:
    raise SystemExit("ABORT: main.js script tag not found in index_3.html")
script = m.group(0)


# ---- head -------------------------------------------------------------
h = head
h = re.sub(r"<title>.*?</title>",
           "<title>Financing &#8212; Chicago Motor Cars</title>", h, flags=re.S)
h = re.sub(r'<meta name="description" content=".*?">',
           '<meta name="description" content="Apply for credit, estimate a monthly payment '
           'and value your trade &#8212; online, for any vehicle Chicago Motor Cars sells, '
           'from a coupe to a van.">', h, flags=re.S)

# The LCP element here is this page's own opening frame, not the homepage's
# hero. fin-lineup-1600 is the desktop crop; the phone takes fin-mobile-900
# off the srcset and does not pay for this preload.
h, n = re.subn(r'<link rel="preload" as="image"[^>]*>',
               '<link rel="preload" as="image" '
               'href="assets/img/financing/fin-lineup-1600.jpg" '
               'imagesrcset="assets/img/financing/fin-mobile-900.jpg 900w, assets/img/financing/fin-lineup-1600.jpg 1600w, assets/img/financing/fin-lineup-2473.jpg 2473w" '
               'imagesizes="100vw" fetchpriority="high">', h)
if n != 1:
    raise SystemExit("ABORT: expected exactly one image preload in the head, found %d" % n)

h, n = re.subn(r'(<link rel="stylesheet" href="assets/css/v3\.css\?v=\d+">)',
               '\\1\n<!-- financing.html only. Last, so it wins on equal specificity. -->\n'
               '<link rel="stylesheet" href="assets/css/financing.css?v=7">', h)
if n != 1:
    raise SystemExit("ABORT: could not place financing.css after v3.css (%d matches). The head "
                     "changed shape; fix this script rather than shipping a page whose "
                     "stylesheet silently never loads." % n)


# ---- the masthead's own Financing links -------------------------------
nav = header
for label in FIN_LABELS:
    nav = nav.replace('href="index_3.html">' + label,
                      'href="financing.html">' + label)


BODY = r"""<main>

  <!-- ============================================================
       1 — THE CLAIM, ON THE FRAME THAT ALREADY MAKES THE ARGUMENT
       ============================================================
       The homepage's Financing card opens with "Make it yours." over
       fin-lineup. The page keeps the line rather than inventing a
       second one: this IS that card, opened.

       THE PHOTOGRAPH IS THE ARGUMENT. Four subjects stand in the hall
       — an AMG GT Black Series, a Mercedes van, a Ducati, a '67 Shelby.
       That is four different kinds of purchase in one frame, which is
       the only claim a financing page actually has to make. The lede
       names them and says nothing the picture does not already show.
       No list of products does this work; a list is what the buyer
       skips.

       THE TEXT SITS RIGHT, AND ONLY ON DESKTOP. The right third of
       fin-lineup falls to near-black and holds no subject — it is the
       quietest field in the frame and the one place type can sit
       without a scrim heavy enough to kill the reflections. The mobile
       crop (fin-mobile-900) is tighter: the four subjects fill it edge
       to edge and there is no dark third left. So the phone does not
       inherit the desktop decision — the frame becomes a band and the
       type stands below it on page ground. Two crops, two decisions.
       ============================================================ -->
  <section class="fn-head" data-reveal aria-labelledby="fn-title">

    <div class="fn-head__frame">
      <img class="fn-head__img"
           src="assets/img/financing/fin-lineup-1600.jpg"
           srcset="assets/img/financing/fin-mobile-900.jpg 900w,
                   assets/img/financing/fin-lineup-1600.jpg 1600w,
                   assets/img/financing/fin-lineup-2473.jpg 2473w"
           sizes="100vw"
           alt="A Mercedes-AMG GT Black Series, a Mercedes van, a Ducati superbike and a 1967 Shelby GT350 standing together in a dark showroom hall."
           width="2473" height="1545" fetchpriority="high" decoding="async">
      <span class="fn-head__wash" aria-hidden="true"></span>
    </div>

    <div class="shell fn-head__inner">
      <div class="fn-head__copy">
        <p class="micro fn-eyebrow">Financing</p>
        <h1 class="fn-title" id="fn-title">
          <span class="ttl-line">Make it</span>
          <span class="ttl-line">yours.</span>
        </h1>
        <p class="lede">A coupe, a classic, a superbike, a van. Four kinds of purchase,
          one set of paperwork — and all of it opens online.</p>
        <div class="fn-acts">
          <a class="btn btn--fill" href="#apply">Start your approval</a>
          <a class="fn-jump" href="#estimator">
            <span>Estimate a payment first</span>
            <svg class="fn-jump__arrow" viewBox="0 0 16 16" width="15" height="15" fill="none" aria-hidden="true"><path d="M8 3v10M3.5 8.5 8 13l4.5-4.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </a>
        </div>
      </div>
    </div>

  </section>


  <!-- ============================================================
       2 — THE ESTIMATOR
       ============================================================
       THE FIGURE IS THE SUBJECT, NOT THE FORM. The buyer's first real
       question is what it costs per month, and the page answers it in
       one number at --t-count — the same scale the homepage gives its
       live figures. The four controls that produce it are subordinate:
       a quiet column on the left, no box, no panel, no card.

       That ranking is the whole reason this section exists in this
       shape. The same content with the controls dominant and the answer
       set in a table is a loan portal, and a loan portal is what
       reduced the perceived value of the last concept this client
       rejected. The arithmetic is identical; the hierarchy is not.

       IT IS AN ESTIMATE AND IT SAYS SO. Nothing here is a quoted rate
       or an offer. THE DEFAULTS ARE CMC&rsquo;S OWN, NOT INVENTED. Their live
       calculator at /auto-loan-calculator-chicago-il/ ships APR 5.9 and
       term 72 as its pre-filled values, read 2026-08-30. This page uses
       the same two, so the number that lands here agrees with the
       number their existing tool produces. An empty rate was the first
       build and it was wrong twice over: the buyer does not know their
       own APR, and a section whose dominant is a dash has no subject.

       WHAT THIS PAGE ADDS THAT THEIRS DOES NOT: a disclaimer. Their
       calculator states no terms at all — no mention that the figure is
       an estimate, and no note about tax, title or fees. That is the
       one place this chapter deliberately says MORE than the original.
       ============================================================ -->
  <section class="fn-calc" id="estimator" data-reveal data-bloom="center" aria-labelledby="fn-calc-title">
    <div class="shell">

      <div class="fn-calc__head">
        <p class="micro fn-eyebrow">Payment estimator</p>
        <h2 class="fn-h2" id="fn-calc-title">
          <span class="ttl-line">What it looks like</span>
          <span class="ttl-line">every month.</span>
        </h2>
      </div>

      <form class="fn-calc__grid" id="fn-calc" novalidate>

        <div class="fn-calc__controls">
          <div class="field field--single">
            <label class="micro field__label" for="fn-price">Vehicle price</label>
            <div class="fn-input">
              <span class="fn-input__pre" aria-hidden="true">$</span>
              <input class="field__control fn-input__control" id="fn-price" name="price"
                     type="text" inputmode="numeric" autocomplete="off" value="145,000">
            </div>
          </div>

          <div class="field field--single">
            <label class="micro field__label" for="fn-down">Down payment</label>
            <div class="fn-input">
              <span class="fn-input__pre" aria-hidden="true">$</span>
              <input class="field__control fn-input__control" id="fn-down" name="down"
                     type="text" inputmode="numeric" autocomplete="off" value="25,000">
            </div>
          </div>

          <div class="field field--single">
            <label class="micro field__label" for="fn-term">Term</label>
            <select class="field__control" id="fn-term" name="term">
              <option value="36">36 months</option>
              <option value="48">48 months</option>
              <option value="60">60 months</option>
              <option value="72" selected>72 months</option>
              <option value="84">84 months</option>
            </select>
          </div>

          <div class="field field--single">
            <label class="micro field__label" for="fn-apr">Annual rate</label>
            <div class="fn-input">
              <input class="field__control fn-input__control" id="fn-apr" name="apr"
                     type="text" inputmode="decimal" autocomplete="off"
                     value="5.9" aria-describedby="fn-apr-help">
              <span class="fn-input__post" aria-hidden="true">%</span>
            </div>
            <p class="fn-help" id="fn-apr-help">CMC&rsquo;s own published starting figure. Change it — your approval sets the real one.</p>
          </div>
        </div>

        <div class="fn-calc__out">
          <p class="micro fn-out__label">Estimated monthly</p>
          <p class="fn-fig" id="fn-monthly" aria-live="polite">
            <span class="fn-fig__cur" aria-hidden="true">$</span><span class="fn-fig__n" data-fn-out>&#8212;</span>
          </p>

          <dl class="fn-sum">
            <div class="fn-sum__row">
              <dt class="micro">Amount financed</dt>
              <dd class="fn-sum__v" data-fn-financed>&#8212;</dd>
            </div>
            <div class="fn-sum__row">
              <dt class="micro">Total of payments</dt>
              <dd class="fn-sum__v" data-fn-total>&#8212;</dd>
            </div>
            <div class="fn-sum__row">
              <dt class="micro">Cost of credit</dt>
              <dd class="fn-sum__v" data-fn-interest>&#8212;</dd>
            </div>
          </dl>

          <p class="fn-note">An estimate, not an offer. It assumes a fixed rate and equal
            payments, and it leaves out tax, title, registration and any documentation fee.
            Your approved rate and term decide the real number.</p>
        </div>

      </form>

    </div>
  </section>


  <!-- ============================================================
       3 — THE APPLICATION, WHICH THIS SITE DOES NOT OWN
       ============================================================
       CMC's live page embeds DealerTrack's hosted credit application in
       an iframe (ebusiness.dealertrack.com, accountId 6228975, read
       2026-08-30) and Alex has confirmed it stays third-party. So this
       chapter is NOT a form. An earlier build made it one — six fields
       in the site's own language — and that was designing a thing the
       client cannot ship.

       THE LIGHT GROUND IS THE ANSWER TO AN UNSTYLEABLE GUEST. A vendor
       form arrives pale, dense and generic. Dropped onto deep navy it
       reads as the page breaking; given its own bone chapter it reads
       as an inserted document, which is what it is. `.on-bone` is the
       project's existing light-chapter modifier — the warranty band
       already uses it — so the buttons, wordmark and rules recolour
       themselves and nothing new was written to host the guest.

       It also buys the page its one tonal change. Four dark chapters in
       a row is a document; dark - dark - LIGHT - dark - dark is a
       sequence, and the light one falls exactly where the visitor has
       to stop and work.

       WHAT CMC OWNS HERE IS THE PREPARATION. The vendor form never
       tells anyone what to have ready, and it never says where the
       details go. Those two things are this section's whole content,
       and they are the part of the chapter that is genuinely CMC's.
       ============================================================ -->
  <section class="fn-apply on-bone" id="apply" data-reveal aria-labelledby="fn-apply-title">
    <div class="shell">

      <div class="fn-apply__head">
        <p class="micro fn-eyebrow">Online credit approval</p>
        <h2 class="fn-h2" id="fn-apply-title">
          <span class="ttl-line">Start it here.</span>
          <span class="ttl-line">It goes to the lenders.</span>
        </h2>
        <p class="lede">Chicago Motor Cars finances with some of the biggest names in lending.
          The application below is theirs, not ours &mdash; have these three things beside you
          and it goes in one sitting.</p>
      </div>

      <ol class="fn-need">
        <li class="fn-need__item">
          <span class="micro fn-need__n">01</span>
          <p class="fn-need__t">Your licence</p>
          <p class="fn-need__d">Name, date of birth and current address, exactly as they are
            printed on it.</p>
        </li>
        <li class="fn-need__item">
          <span class="micro fn-need__n">02</span>
          <p class="fn-need__t">Where you work</p>
          <p class="fn-need__d">Employer, position, how long you have been there, and gross
            income before deductions.</p>
        </li>
        <li class="fn-need__item">
          <span class="micro fn-need__n">03</span>
          <p class="fn-need__t">Where you live</p>
          <p class="fn-need__d">The last two years of addresses, if you have moved inside
            that window.</p>
        </li>
      </ol>

      <!-- THE SLOT. In the live build the lender's iframe mounts inside
           .fn-slot__frame and nothing else changes: the caption, the
           rule and the disclosure below it belong to CMC and sit
           outside the guest. The placeholder is the preview standing in
           for it, and it is labelled as one rather than dressed up as a
           form — a fake form in a mockup is the thing a client
           reasonably mistakes for a decision. -->
      <div class="fn-slot">
        <p class="micro fn-slot__cap">Secure credit application</p>
        <div class="fn-slot__frame" role="img"
             aria-label="Placeholder for the lender's secure credit application form.">
          <p class="fn-slot__note">The lender&rsquo;s application mounts here.</p>
          <p class="fn-slot__sub">Preview build &mdash; the live page loads the secure form
            from CMC&rsquo;s finance partner at this position.</p>
        </div>
        <p class="fn-note fn-slot__legal">Your details are submitted to the lender that
          operates this form, not stored by this website. A credit application permits a
          check of your credit.</p>
      </div>

    </div>
  </section>


  <!-- ============================================================
       4 — THE TRADE
       ============================================================
       The other half of the same arithmetic, and deliberately the
       SHORTEST chapter on the page. The estimator asks what it costs;
       this asks what you already have. Four fields, laid in a single
       row at desktop so the section reads as one line rather than a
       second form — a page with two full-height forms stacked is the
       document the last concept became.
       ============================================================ -->
  <section class="fn-trade" id="trade" data-reveal aria-labelledby="fn-trade-title">
    <div class="shell fn-trade__inner">

      <div class="fn-trade__head">
        <p class="micro fn-eyebrow">Trade appraisal</p>
        <h2 class="fn-h2" id="fn-trade-title">
          <span class="ttl-line">What you already own</span>
          <span class="ttl-line">counts toward it.</span>
        </h2>
      </div>

      <form class="fn-trade__form" id="fn-trade-form" novalidate>
        <div class="fn-trade__row">
          <div class="field field--single">
            <label class="micro field__label" for="fn-ty">Year</label>
            <input class="field__control" id="fn-ty" name="year" type="text" inputmode="numeric" autocomplete="off" placeholder="2021">
          </div>
          <div class="field field--single">
            <label class="micro field__label" for="fn-tmk">Make</label>
            <input class="field__control" id="fn-tmk" name="make" type="text" autocomplete="off" placeholder="Porsche">
          </div>
          <div class="field field--single">
            <label class="micro field__label" for="fn-tmd">Model</label>
            <input class="field__control" id="fn-tmd" name="model" type="text" autocomplete="off" placeholder="911 GT3">
          </div>
          <div class="field field--single">
            <label class="micro field__label" for="fn-tmi">Mileage</label>
            <input class="field__control" id="fn-tmi" name="mileage" type="text" inputmode="numeric" autocomplete="off" placeholder="12,400">
          </div>
        </div>
        <div class="fn-acts fn-trade__acts">
          <button class="btn btn--line" type="submit">Value my car</button>
          <p class="fn-note fn-form__note" data-fn-formnote>Preview build &mdash; this form validates but does not transmit.</p>
        </div>
      </form>

    </div>
  </section>


  <!-- ============================================================
       5 — THE OTHER TWO DOORS
       ============================================================
       BitPay and the trucks-and-equipment application are real and
       neither is a headline. They close the page as a pair of quiet
       rows, reusing .fin__row from the homepage card verbatim — same
       icon slot, same label, same hover. This is the chapter most
       likely to grow a bespoke card treatment and it does not get one.
       ============================================================ -->
  <section class="fn-ways" data-reveal aria-labelledby="fn-ways-title">
    <div class="shell fn-ways__inner">

      <h2 class="micro fn-eyebrow" id="fn-ways-title">Two more ways in</h2>

      <div class="fn-ways__rows">
        <a class="fin__row" href="financing.html">
          <span class="fin__ico" aria-hidden="true"><svg viewBox="0 -960 960 960" width="22" height="22" fill="currentColor"><path d="M240-160q-33 0-56.5-23.5T160-240v-480q0-33 23.5-56.5T240-800h480q33 0 56.5 23.5T800-720v480q0 33-23.5 56.5T720-160H240Zm0-80h480v-480H240v480Zm80-80h320v-80H320v80Zm0-120h320v-80H320v80Zm0-120h320v-80H320v80Z"/></svg></span>
          <span class="fin__row-t">Trucks &amp; Equipment credit approval</span>
        </a>
        <a class="fin__row" href="financing.html">
          <span class="fin__ico" aria-hidden="true"><svg viewBox="0 -960 960 960" width="22" height="22" fill="currentColor"><path d="M441-120v-86q-53-12-91.5-46T293-348l74-30q15 48 44.5 73t77.5 25q41 0 69.5-18.5T587-356q0-35-22-55.5T463-458q-86-27-118-64.5T313-614q0-53 34.5-91.5T441-757v-83h80v83q114 15 137 122l-76 26q-8-33-31-53t-63-20q-42 0-64 19t-22 49q0 32 26 50t99 40q79 22 112 63t33 100q0 60-38 97t-113 47v87h-80Z"/></svg></span>
          <span class="fin__row-t">Purchase with BitPay</span>
        </a>
      </div>

    </div>
  </section>

</main>"""


HEADER_COMMENT = """<!DOCTYPE html>
<html lang="en">
<!-- ============================================================
     financing.html &#8212; GENERATED. Do not hand-edit.

     Head, masthead and footer are COPIED from index_3.html at build
     time by tools-build-financing.py. index_3 is the source because it
     is the approved variant; a hand-copied nav is a nav that drifts.

     <body> carries `v2 is-fin`: v2 because every page on this site runs
     the v2 layer, is-fin because assets/css/financing.css is scoped
     entirely to it and may not reach another page.
     ============================================================ -->
"""

out = (HEADER_COMMENT
       + h + '\n<body class="v2 is-fin">\n'
       + nav + "\n" + (between if between.strip() else "\n") + "\n"
       + BODY + "\n" + footer + "\n" + script + "\n"
       + '<script src="assets/js/financing.js?v=2" defer></script>\n'
       + "</body>\n</html>\n")

open(OUT, "w", encoding="utf-8").write(out)
print("written", OUT, len(out), "bytes")
