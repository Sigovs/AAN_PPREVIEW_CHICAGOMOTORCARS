#!/usr/bin/env python3
"""Assemble events.html from index_3.html's head, masthead and footer.

Same principle as tools-build-our-dealership.py: anything shared is COPIED
at build time rather than retyped, so the pages cannot drift. index_3 is
the source because it is the approved variant.

It writes events.html and NOTHING ELSE. The inventory builder once wrote
srp.html as well and deleted 525 lines of hand-maintained head; a script
that can only create the one file it is named after cannot repeat that.

NOTE ON THE FIRST BUILD. Python is not installed on the machine this page
was authored on, so the artefact was produced by a one-off transliteration
of this script and then verified in the browser. If a regeneration here
ever differs from the committed events.html, THIS file is the authority
and the difference is a bug in the transliteration, not in the page.
"""
import re, os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(ROOT, "events.html")
src  = open(os.path.join(ROOT, "index_3.html"), encoding="utf-8").read()

# The Events entries still point at the homepage. They appear in BOTH
# the desktop masthead AND the collapsed mobile menu, and the mobile menu
# sits between </header> and <main> — outside the header slice. Repointing
# only the slice left a dead link on the phone, so the replacement runs
# over the whole assembled document at the end instead.
EVENT_LABELS = [
    # CMC own label for this destination. Their page <title> is
    # "Events - Chicago Motor Cars", so the name is theirs and stays.
    "Events",
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
           "<title>Events &#8212; Chicago Motor Cars</title>", h, flags=re.S)
h = re.sub(r'<meta name="description" content=".*?">',
           '<meta name="description" content="Two films shot inside the Chicago Motor Cars '
           'showrooms, plus the cars that get their own on the channel.">', h, flags=re.S)

# NOTHING IS PRELOADED HERE, AND THE ABSENCE IS THE DECISION. This page
# opens on type, not on a photograph: the first portrait is a lazily loaded
# 380px plate well below the fold. Carrying the homepage's hero preload
# across would fetch a large image nobody sees before the LCP, which is the
# wasted-preload defect financing.html was caught on.
h, n = re.subn(r'\s*<link rel="preload" as="image"[^>]*>', '', h)
if n != 1:
    raise SystemExit("ABORT: expected exactly one image preload to remove, found %d" % n)

h, n = re.subn(r'(<link rel="stylesheet" href="assets/css/v3\.css\?v=\d+">)',
               '\\1\n<!-- events.html only. Last, so it wins on equal specificity. -->\n'
               '<link rel="stylesheet" href="assets/css/events.css?v=1">', h)
if n != 1:
    raise SystemExit("ABORT: could not place events.css after v3.css (%d matches). The head "
                     "changed shape; fix this script rather than shipping a page whose "
                     "stylesheet silently never loads." % n)


# ---- the masthead's own Events links ----------------------------------
nav = header


BODY = r"""<main>

  <!-- ============================================================
       1 — THE CLAIM
       ============================================================
       THE PAGE IS CALLED EVENTS BECAUSE CMC CALL IT EVENTS. Their nav
       item says Events, it points at chicagomotorcars.com/blog/, and
       that page's own <title> is "Events - Chicago Motor Cars". The
       content behind it is ten write-ups about cars they have for sale.

       An earlier pass renamed this page to "Stories" on the grounds
       that the label does not describe the contents. Alex's direction
       is to take what is on chicagomotorcars.com, so the name is
       theirs, the two section headings below are theirs, and the
       observation about the mismatch is a note to them rather than an
       edit to their site.

       The lede is the only sentence on this page that is not CMC's,
       and it describes the contents without contradicting the label.
       ============================================================ -->
  <section class="st-head" data-reveal data-bloom="center">
    <div class="shell">
      <p class="micro st-eyebrow">Events</p>
      <h1 class="st-title">
        <span class="ttl-line">What came</span>
        <span class="ttl-line">through the door.</span>
      </h1>
      <p class="lede">Write-ups from the floor &mdash; the cars worth stopping for, and what
        makes each one worth the trip.</p>
    </div>
  </section>


  <!-- ============================================================
       2 — RECENT STORIES
       ============================================================
       Their heading, their order, their dates. One lead at full width
       rather than ten equal cards: ten equal cards is a blog index, and
       a lead plus a grid also tells the visitor which one is new.
       ============================================================ -->
  <section class="st-lead" data-reveal aria-labelledby="st-lead-t">
    <div class="shell">
      <div class="st-lead__head">
        <p class="micro st-eyebrow">Recent Stories</p>
      </div>
      <article class="st-feature">
        <a class="st-feature__link" href="https://www.chicagomotorcars.com/classic-dodge-viper-convertible-for-sale-near-aurora-il/" target="_blank" rel="noopener">
          <span class="st-feature__fig"><img src="assets/img/stories/classic-dodge-viper-convertible-for-sale-near-aurora-il-1400.jpg"
                 srcset="assets/img/stories/classic-dodge-viper-convertible-for-sale-near-aurora-il-700.jpg 700w,
                         assets/img/stories/classic-dodge-viper-convertible-for-sale-near-aurora-il-1400.jpg 1400w"
                 sizes="(max-width: 900px) 100vw, 58vw"
                 alt="" width="1400" height="788" loading="lazy" decoding="async"></span>
          <span class="st-feature__body">
            <span class="micro st-feature__kicker">Latest <span class="st-dot" aria-hidden="true">&middot;</span> July 1, 2026</span>
            <span class="st-feature__t" id="st-lead-t">Classic Dodge Viper Convertible for Sale near Aurora, IL</span>
            <span class="st-feature__x">Some cars are fast. The Dodge Viper convertible is something else entirely.</span>
            <span class="fn-jump st-jump">
              <span>Read it</span>
              <svg class="fn-jump__arrow" viewBox="0 0 16 16" width="15" height="15" fill="none" aria-hidden="true"><path d="M3 8h10M8.5 3.5 13 8l-4.5 4.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </span>
          </span>
        </a>
      </article>
    </div>
  </section>


  <!-- ============================================================
       3 — THE REST OF RECENT STORIES
       ============================================================
       Nine cards, newest first, each linking to the article on
       chicagomotorcars.com. The articles are not rebuilt here: this is
       a redesign of the index, and ten reconstructed article pages
       would be ten pages of someone else's copy.
       ============================================================ -->
  <section class="st-more" data-reveal aria-labelledby="st-more-t">
    <div class="shell">
      <div class="st-more__head">
        <p class="micro st-eyebrow">Earlier</p>
        <h2 class="st-h2" id="st-more-t">
          <span class="ttl-line">Nine more,</span>
          <span class="ttl-line">newest first.</span>
        </h2>
      </div>
      <ul class="st-grid">
        <li class="st-card">
          <a class="st-card__link" href="https://www.chicagomotorcars.com/track-focused-sports-cars-for-sale-near-hinsdale-il/" target="_blank" rel="noopener">
            <span class="st-card__fig"><img src="assets/img/stories/track-focused-sports-cars-for-sale-near-hinsdale-il-1400.jpg"
                 srcset="assets/img/stories/track-focused-sports-cars-for-sale-near-hinsdale-il-700.jpg 700w,
                         assets/img/stories/track-focused-sports-cars-for-sale-near-hinsdale-il-1400.jpg 1400w"
                 sizes="(max-width: 720px) 100vw, 30vw"
                 alt="" width="1400" height="788" loading="lazy" decoding="async"></span>
            <span class="micro st-card__date">June 10, 2026</span>
            <span class="st-card__t">Track-Focused Sports Cars for Sale near Hinsdale, IL</span>
            <span class="st-card__x">Performance drivers near Hinsdale know the difference between a sports car and a track-focused sports car. One is quick.</span>
          </a>
        </li>
        <li class="st-card">
          <a class="st-card__link" href="https://www.chicagomotorcars.com/porsche-911-gt2-for-sale-in-naperville-il/" target="_blank" rel="noopener">
            <span class="st-card__fig"><img src="assets/img/stories/porsche-911-gt2-for-sale-in-naperville-il-1400.jpg"
                 srcset="assets/img/stories/porsche-911-gt2-for-sale-in-naperville-il-700.jpg 700w,
                         assets/img/stories/porsche-911-gt2-for-sale-in-naperville-il-1400.jpg 1400w"
                 sizes="(max-width: 720px) 100vw, 30vw"
                 alt="" width="1400" height="788" loading="lazy" decoding="async"></span>
            <span class="micro st-card__date">May 8, 2026</span>
            <span class="st-card__t">Porsche 911 GT2 for Sale in Naperville, IL</span>
            <span class="st-card__x">There&rsquo;s a hierarchy within the Porsche 911 family, and the GT2 sits at a place of its own. The GT3 is the analytical track instrument.</span>
          </a>
        </li>
        <li class="st-card">
          <a class="st-card__link" href="https://www.chicagomotorcars.com/pre-owned-jeep-wrangler-for-sale-near-oak-brook-il/" target="_blank" rel="noopener">
            <span class="st-card__fig"><img src="assets/img/stories/pre-owned-jeep-wrangler-for-sale-near-oak-brook-il-1400.jpg"
                 srcset="assets/img/stories/pre-owned-jeep-wrangler-for-sale-near-oak-brook-il-700.jpg 700w,
                         assets/img/stories/pre-owned-jeep-wrangler-for-sale-near-oak-brook-il-1400.jpg 1400w"
                 sizes="(max-width: 720px) 100vw, 30vw"
                 alt="" width="1400" height="788" loading="lazy" decoding="async"></span>
            <span class="micro st-card__date">April 8, 2026</span>
            <span class="st-card__t">Pre-Owned Jeep Wrangler for Sale near Oak Brook, IL</span>
            <span class="st-card__x">If you are searching for a pre-owned Jeep Wrangler for sale near Oak Brook, IL, you are joining a long list of&hellip;</span>
          </a>
        </li>
        <li class="st-card">
          <a class="st-card__link" href="https://www.chicagomotorcars.com/rare-2018-ferrari-gtc4lusso-for-sale-near-glen-ellyn-il/" target="_blank" rel="noopener">
            <span class="st-card__fig"><img src="assets/img/stories/rare-2018-ferrari-gtc4lusso-for-sale-near-glen-ellyn-il-1400.jpg"
                 srcset="assets/img/stories/rare-2018-ferrari-gtc4lusso-for-sale-near-glen-ellyn-il-700.jpg 700w,
                         assets/img/stories/rare-2018-ferrari-gtc4lusso-for-sale-near-glen-ellyn-il-1400.jpg 1400w"
                 sizes="(max-width: 720px) 100vw, 30vw"
                 alt="" width="1400" height="788" loading="lazy" decoding="async"></span>
            <span class="micro st-card__date">March 20, 2026</span>
            <span class="st-card__t">Rare 2018 Ferrari GTC4Lusso for Sale near Glen Ellyn, IL</span>
            <span class="st-card__x">Imagine driving a vehicle that delivers the thrill of a supercar while offering room for passengers and everyday comfort.</span>
          </a>
        </li>
        <li class="st-card">
          <a class="st-card__link" href="https://www.chicagomotorcars.com/luxury-vehicle-inspections-in-chicago/" target="_blank" rel="noopener">
            <span class="st-card__fig"><img src="assets/img/stories/luxury-vehicle-inspections-in-chicago-1400.jpg"
                 srcset="assets/img/stories/luxury-vehicle-inspections-in-chicago-700.jpg 700w,
                         assets/img/stories/luxury-vehicle-inspections-in-chicago-1400.jpg 1400w"
                 sizes="(max-width: 720px) 100vw, 30vw"
                 alt="" width="1400" height="788" loading="lazy" decoding="async"></span>
            <span class="micro st-card__date">February 23, 2026</span>
            <span class="st-card__t">Luxury Vehicle Inspections in Chicago</span>
            <span class="st-card__x">Luxury vehicles are more than simple transportation. They represent comfort, performance, and personal pride. Owners of high-end cars understand the importance of proper care.</span>
          </a>
        </li>
        <li class="st-card">
          <a class="st-card__link" href="https://www.chicagomotorcars.com/mercedes-benz-sprinter-vans-for-sale-in-chicago/" target="_blank" rel="noopener">
            <span class="st-card__fig"><img src="assets/img/stories/mercedes-benz-sprinter-vans-for-sale-in-chicago-1400.jpg"
                 srcset="assets/img/stories/mercedes-benz-sprinter-vans-for-sale-in-chicago-700.jpg 700w,
                         assets/img/stories/mercedes-benz-sprinter-vans-for-sale-in-chicago-1400.jpg 1400w"
                 sizes="(max-width: 720px) 100vw, 30vw"
                 alt="" width="1400" height="788" loading="lazy" decoding="async"></span>
            <span class="micro st-card__date">December 6, 2025</span>
            <span class="st-card__t">Mercedes-Benz Sprinter Vans for Sale in Chicago</span>
            <span class="st-card__x">Service-based businesses in Chicago rely on strong, reliable, and comfortable vehicles.</span>
          </a>
        </li>
        <li class="st-card">
          <a class="st-card__link" href="https://www.chicagomotorcars.com/pre-owned-mclaren-765lt-for-sale-in-chicago/" target="_blank" rel="noopener">
            <span class="st-card__fig"><img src="assets/img/stories/pre-owned-mclaren-765lt-for-sale-in-chicago-1400.jpg"
                 srcset="assets/img/stories/pre-owned-mclaren-765lt-for-sale-in-chicago-700.jpg 700w,
                         assets/img/stories/pre-owned-mclaren-765lt-for-sale-in-chicago-1400.jpg 1400w"
                 sizes="(max-width: 720px) 100vw, 30vw"
                 alt="" width="1400" height="788" loading="lazy" decoding="async"></span>
            <span class="micro st-card__date">November 13, 2025</span>
            <span class="st-card__t">Pre-Owned McLaren 765LT for Sale in Chicago</span>
            <span class="st-card__x">Have you ever dreamed of owning one of the rarest supercars on the market?</span>
          </a>
        </li>
        <li class="st-card">
          <a class="st-card__link" href="https://www.chicagomotorcars.com/great-inventory-of-audi-cars-in-chicago/" target="_blank" rel="noopener">
            <span class="st-card__fig"><img src="assets/img/stories/great-inventory-of-audi-cars-in-chicago-1400.jpg"
                 srcset="assets/img/stories/great-inventory-of-audi-cars-in-chicago-700.jpg 700w,
                         assets/img/stories/great-inventory-of-audi-cars-in-chicago-1400.jpg 1400w"
                 sizes="(max-width: 720px) 100vw, 30vw"
                 alt="" width="1400" height="788" loading="lazy" decoding="async"></span>
            <span class="micro st-card__date">October 13, 2025</span>
            <span class="st-card__t">Great Inventory of Audi Cars in Chicago</span>
            <span class="st-card__x">Are you searching for the perfect Audi that blends luxury, performance, and everyday practicality?</span>
          </a>
        </li>
        <li class="st-card">
          <a class="st-card__link" href="https://www.chicagomotorcars.com/chicagolands-destination-for-lifted-pickup-trucks/" target="_blank" rel="noopener">
            <span class="st-card__fig"><img src="assets/img/stories/chicagolands-destination-for-lifted-pickup-trucks-1400.jpg"
                 srcset="assets/img/stories/chicagolands-destination-for-lifted-pickup-trucks-700.jpg 700w,
                         assets/img/stories/chicagolands-destination-for-lifted-pickup-trucks-1400.jpg 1400w"
                 sizes="(max-width: 720px) 100vw, 30vw"
                 alt="" width="1400" height="788" loading="lazy" decoding="async"></span>
            <span class="micro st-card__date">September 1, 2025</span>
            <span class="st-card__t">Chicagoland&rsquo;s Destination for Lifted Pickup Trucks</span>
            <span class="st-card__x">Are you looking for a powerful lifted pickup truck that stands out on the road and performs off-road with ease?</span>
          </a>
        </li>
      </ul>
    </div>
  </section>


  <!-- ============================================================
       4 — MOST POPULAR STORIES
       ============================================================
       CMC's second section, kept because it is on their page. It holds
       four entries and it carries NO dates and NO excerpts on their
       site — the widget prints titles only — and all four are already
       in Recent Stories above.

       So it is set as a ranked list rather than as four more picture
       cards. Repeating the same four photographs a second time inside
       one page would read as a bug; a numbered index reads as what the
       section actually is, which is a ranking. Their content, their
       order, no invented dates.
       ============================================================ -->
  <section class="st-pop" data-reveal aria-labelledby="st-pop-t">
    <div class="shell">
      <div class="st-pop__head">
        <p class="micro st-eyebrow">Most Popular Stories</p>
        <h2 class="st-h2" id="st-pop-t">
          <span class="ttl-line">The four people</span>
          <span class="ttl-line">read most.</span>
        </h2>
      </div>
      <ol class="st-pop__list">
          <li class="st-pop__item">
            <a class="st-pop__link" href="https://www.chicagomotorcars.com/classic-dodge-viper-convertible-for-sale-near-aurora-il/" target="_blank" rel="noopener">
              <span class="micro st-pop__n">01</span>
              <span class="st-pop__t">Classic Dodge Viper Convertible for Sale near Aurora, IL</span>
              <svg class="st-pop__arrow" viewBox="0 0 16 16" width="15" height="15" fill="none" aria-hidden="true"><path d="M3 8h10M8.5 3.5 13 8l-4.5 4.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
          </li>
          <li class="st-pop__item">
            <a class="st-pop__link" href="https://www.chicagomotorcars.com/track-focused-sports-cars-for-sale-near-hinsdale-il/" target="_blank" rel="noopener">
              <span class="micro st-pop__n">02</span>
              <span class="st-pop__t">Track-Focused Sports Cars for Sale near Hinsdale, IL</span>
              <svg class="st-pop__arrow" viewBox="0 0 16 16" width="15" height="15" fill="none" aria-hidden="true"><path d="M3 8h10M8.5 3.5 13 8l-4.5 4.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
          </li>
          <li class="st-pop__item">
            <a class="st-pop__link" href="https://www.chicagomotorcars.com/porsche-911-gt2-for-sale-in-naperville-il/" target="_blank" rel="noopener">
              <span class="micro st-pop__n">03</span>
              <span class="st-pop__t">Porsche 911 GT2 for Sale in Naperville, IL</span>
              <svg class="st-pop__arrow" viewBox="0 0 16 16" width="15" height="15" fill="none" aria-hidden="true"><path d="M3 8h10M8.5 3.5 13 8l-4.5 4.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
          </li>
          <li class="st-pop__item">
            <a class="st-pop__link" href="https://www.chicagomotorcars.com/pre-owned-jeep-wrangler-for-sale-near-oak-brook-il/" target="_blank" rel="noopener">
              <span class="micro st-pop__n">04</span>
              <span class="st-pop__t">Pre-Owned Jeep Wrangler for Sale near Oak Brook, IL</span>
              <svg class="st-pop__arrow" viewBox="0 0 16 16" width="15" height="15" fill="none" aria-hidden="true"><path d="M3 8h10M8.5 3.5 13 8l-4.5 4.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
          </li>
      </ol>
    </div>
  </section>


  <!-- ============================================================
       5 — THE WAY OUT
       ============================================================ -->
  <section class="st-cta" data-reveal aria-labelledby="st-cta-t">
    <div class="shell">
      <h2 class="st-h2" id="st-cta-t">
        <span class="ttl-line">Most of these</span>
        <span class="ttl-line">are still here.</span>
      </h2>
      <p class="lede">The cars in these write-ups came off the same floor the inventory
        does. What is left of them is on the site.</p>
      <div class="st-acts">
        <a class="btn btn--fill" href="srp.html">Browse the inventory</a>
        <a class="fn-jump st-jump" href="https://www.chicagomotorcars.com/blog/" target="_blank" rel="noopener">
          <span>Every story on the blog</span>
          <svg class="fn-jump__arrow" viewBox="0 0 16 16" width="15" height="15" fill="none" aria-hidden="true"><path d="M3 8h10M8.5 3.5 13 8l-4.5 4.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
      </div>
    </div>
  </section>

</main>"""


HEADER_COMMENT = """<!DOCTYPE html>
<html lang="en">
<!-- ============================================================
     events.html &#8212; GENERATED. Do not hand-edit.

     Head, masthead and footer are COPIED from index_3.html at build
     time by tools-build-events.py. index_3 is the source because it
     is the approved variant; a hand-copied nav is a nav that drifts.

     <body> carries `v2 is-st`: v2 because every page on this site runs
     the v2 layer, is-st because assets/css/events.css is scoped
     entirely to it and may not reach another page.
     ============================================================ -->
"""

out = (HEADER_COMMENT
       + h + '\n<body class="v2 is-st">\n'
       + nav + "\n" + (between if between.strip() else "\n") + "\n"
       + BODY + "\n" + footer + "\n" + script + "\n"
       + "</body>\n</html>\n")

for label in EVENT_LABELS:
    out = out.replace('href="index_3.html">' + label,
                      'href="events.html">' + label)

open(OUT, "w", encoding="utf-8").write(out)
print("written", OUT, len(out), "bytes")
