#!/usr/bin/env python3
"""Assemble srp.html and vdp.html from index_2.html's own head, header and
footer, so the three pages cannot drift apart. Anything shared is COPIED
from index_2 at build time rather than retyped — a hand-copied nav is a nav
that is wrong the first time someone edits the real one."""
import json, re, os, html

ROOT = "/Users/alex/Desktop/WORK/Chicago Motor Cars"
SCR  = os.path.dirname(os.path.abspath(__file__))
src  = open(os.path.join(ROOT, "index_2.html")).read()

head   = src[src.index("<head>"):src.index("</head>")+len("</head>")]
header = src[src.index('<span class="scroll-sentinel"'):src.index("</header>")+len("</header>")]
between= src[src.index("</header>")+len("</header>"):src.index("<main>")]
footer = src[src.index('<footer class="foot">'):src.index("</footer>")+len("</footer>")]
script = re.search(r'<script src="assets/js/main\.js\?v=\d+" defer></script>', src).group(0)

# ---- head, adjusted -------------------------------------------------
def make_head(title, desc, preload):
    h = head
    h = re.sub(r"<title>.*?</title>", "<title>%s</title>" % html.escape(title), h, flags=re.S)
    h = re.sub(r'<meta name="description" content=".*?">',
               '<meta name="description" content="%s">' % html.escape(desc, quote=True), h, flags=re.S)
    # the homepage preloads its hero frame; these pages have a different LCP
    h = re.sub(r'<!-- The frame is the whole page.*?fetchpriority="high">', preload, h, flags=re.S)
    # inventory.css goes last, after v2.css
    h = h.replace('<link rel="stylesheet" href="assets/css/v2.css?v=58">',
                  '<link rel="stylesheet" href="assets/css/v2.css?v=58">\n'
                  '<!-- Last again. srp.html and vdp.html load this; index_2.html does\n'
                  '     not, and index.html loads neither. -->\n'
                  '<link rel="stylesheet" href="assets/css/inventory.css?v=1">')
    return h

# ---- the nav's current page ----------------------------------------
def mark_current(frag, label):
    """Give the INVENTORY item aria-current so the nav says where you are.
    The homepage never needed this because it had nothing to point at."""
    return frag.replace('>%s</a>' % label, ' aria-current="page">%s</a>' % label, 1)

# ---- data ------------------------------------------------------------
cars = json.load(open(os.path.join(SCR, "inventory.json")))
money = lambda n: "${:,}".format(n)
miles = lambda n: "{:,} mi".format(n)

def slug_of(c):
    return re.sub(r"[^a-z0-9]+", "-", ("%d-%s-%s" % (c["year"], c["make"], c["model"])).lower()).strip("-")

# ---- the SRP ---------------------------------------------------------
def card(c, i):
    facts = '<span class="veh__pill veh__pill--price">%s</span>' % money(c["price"])
    facts += '<span class="veh__pill">%s</span>' % miles(c["miles"])
    if c.get("body"):
        facts += '<span class="veh__pill">%s</span>' % c["body"]
    href = "vdp.html" if c.get("vdp") else c["url"]
    ext  = "" if c.get("vdp") else ' rel="noopener"'
    load = "eager" if i < 3 else "lazy"
    name = "%s %s" % (c["year"], c["model"])
    trim = c["trim"] + ((" — " + c["note"]) if c.get("note") else "")
    return f'''        <a class="veh" href="{href}"{ext} aria-label="{html.escape(name)}, {money(c["price"])}">
          <span class="veh__stock">#{html.escape(c["stock"])}</span>
          <span class="veh__media">
            <img src="assets/img/inventory-live/{c["slug"]}.jpg" alt="{html.escape(name)}"
                 width="900" height="598" loading="{load}" decoding="async">
          </span>
          <span class="veh__body">
            <span class="micro veh__make">{html.escape(c["make"])}</span>
            <span class="veh__name">{html.escape(name)}</span>
            <span class="veh__trim">{html.escape(trim)}</span>
            <span class="veh__facts">{facts}</span>
          </span>
        </a>'''

SORTS = ["Price: high to low", "Price: low to high", "Year: newest first", "Year: oldest first",
         "Mileage: low to high", "Mileage: high to low", "Recently added"]
MAKES = sorted({c["make"] for c in cars})
BODIES = ["Convertible", "Coupe", "Hatchback", "Sedan", "SUV", "Wagon", "Pickup Truck", "Sprinter Van", "Motorcycle", "Boat"]
YEARS = ["2026", "2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "Before 2018"]
PRICES = ["Under $50,000", "$50,000 – $100,000", "$100,000 – $250,000", "$250,000 – $500,000", "$500,000 and above"]

def sel(id_, label, options, name):
    opts = "".join("<option>%s</option>" % html.escape(o) for o in options)
    return f'''          <p class="hunt__field">
            <label class="micro hunt__label" for="{id_}">{label}</label>
            <select class="hunt__control" id="{id_}" name="{name}">
              <option value="">{label}</option>{opts}
            </select>
            <span class="hunt__value" aria-hidden="true"></span>
          </p>'''

srp_head = make_head(
    "Inventory — Chicago Motor Cars",
    "Browse the Chicago Motor Cars collection: exotic, performance and collector vehicles, "
    "delivered nationwide from four showrooms.",
    '<!-- The LCP here is the first row of the grid, not one frame. Three cards\n'
    '     load eagerly and the rest are lazy; preloading one of twenty-four\n'
    '     would just pick a winner among equals. -->')

srp = f"""<!DOCTYPE html>
<!-- ============================================================
     srp.html — THE SEARCH RESULTS PAGE
     ============================================================
     Built 2026-08-17 for the index_2 preview. Head, masthead and footer
     are COPIED FROM index_2.html at build time by the script in the
     session scratchpad, not retyped, so the three pages cannot drift.

     REAL INVENTORY. Every vehicle below is a live listing pulled from
     chicagomotorcars.com/used-cars-chicago-il on 2026-08-17: real year,
     make, model, trim, price, mileage, stock number and photograph, and
     every card that is not the demo VDP links to that vehicle's own page
     on the live site. Nothing here is invented — the point of a results
     page is that it is true, and a mock full of fictional cars proves
     nothing about how the real feed will look.

     Twenty-four of the collection. The count is theirs.

     NO NEW DESIGN SYSTEM. The buttons, pills, eyebrows, type scale,
     hairlines, reveal choreography and finder fields are all the
     homepage's, used as they are. See assets/css/inventory.css for what
     is genuinely new and why it is only two objects.
     ============================================================ -->
<html lang="en">
{srp_head}
<body class="v2">

{mark_current(header, 'INVENTORY')}
{between.rstrip()}

<main>

  <section class="page-head" data-reveal>
    <div class="shell">
      <p class="micro eyebrow">The collection</p>
      <h1 class="page-head__title">
        <span class="ttl-line">Three hundred and one</span>
        <span class="ttl-line">cars worth chasing.</span>
      </h1>
      <p class="lede page-head__lede">Exotic, performance and collector vehicles across four
        showrooms — West Chicago, Naperville, Rock Hill and Tonganoxie — and delivered anywhere
        in the country.</p>

      <!-- The finder, horizontal. Same fields, same fieldless construction
           as the hero: label over value over a hairline. A results page
           that framed every input would read as a booking widget, and the
           homepage already settled that argument. -->
      <form class="filters" action="https://www.chicagomotorcars.com/used-cars-chicago-il/" method="get">
{sel("f-make", "Make", MAKES, "make")}
{sel("f-body", "Body Style", BODIES, "bodystyle")}
{sel("f-year", "Year", YEARS, "year")}
{sel("f-price", "Price", PRICES, "price")}
        <p class="filters__go">
          <button class="btn btn--line" type="submit">Apply <svg class="btn__arrow" width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true"><path d="M2 6.5h9M7.4 3 11 6.5 7.4 10" stroke="currentColor" stroke-width="1.3"/></svg></button>
        </p>
      </form>

      <!-- Keyword is a different question from the four above — you already
           know what the car is called — so it keeps its own line and its
           own action, exactly as it does on the homepage. -->
      <form class="invsearch" method="get"
            action="https://www.chicagomotorcars.com/used-cars-chicago-il/"
            role="search" aria-label="Search inventory by keyword">
        <label class="u-visually-hidden" for="srp-kw">Search make, model or keyword</label>
        <svg class="invsearch__icon" width="17" height="17" viewBox="0 0 17 17" fill="none" aria-hidden="true">
          <circle cx="7.2" cy="7.2" r="5.4" stroke="currentColor" stroke-width="1.4"/>
          <path d="m11.4 11.4 3.8 3.8" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
        </svg>
        <input class="invsearch__field" id="srp-kw" name="stockno" type="search"
               placeholder="Search make, model or keyword" autocomplete="off">
        <button class="btn btn--line invsearch__go" type="submit">Search <svg class="btn__arrow" width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true"><path d="M2 6.5h9M7.4 3 11 6.5 7.4 10" stroke="currentColor" stroke-width="1.3"/></svg></button>
      </form>

      <div class="page-head__meta">
        <p class="micro page-head__count"><b>24</b> of 301 vehicles</p>
        <p class="sortbar">
          <label class="micro" for="srp-sort">Sort</label>
          <select id="srp-sort">
{"".join("            <option>%s</option>%s" % (s, chr(10)) for s in SORTS).rstrip(chr(10))}
          </select>
        </p>
      </div>
    </div>
  </section>

  <section class="inv-results">
    <div class="shell">
      <div class="grid">
{chr(10).join(card(c, i) for i, c in enumerate(cars))}
      </div>

      <!-- Thirteen pages at twenty-four a page is the real shape of 301.
           The numbers are the control: they say where you are as well as
           where you can go, which a pair of chevrons does not. -->
      <nav class="pager" aria-label="Inventory pages">
        <a class="pager__link" href="srp.html" aria-current="page">1</a>
        <a class="pager__link" href="srp.html">2</a>
        <a class="pager__link" href="srp.html">3</a>
        <a class="pager__link" href="srp.html">4</a>
        <span class="pager__gap" aria-hidden="true">&hellip;</span>
        <a class="pager__link" href="srp.html">13</a>
        <a class="micro pager__rest" href="https://www.chicagomotorcars.com/used-cars-chicago-il/">See all 301 on the live site &rarr;</a>
      </nav>
    </div>
  </section>

</main>

  {footer}

{script}
</body>
</html>
"""

# ---- the VDP ---------------------------------------------------------
V = cars[0]
GALLERY = ["assets/img/inventory-live/vdp-viper-%d.jpg" % n for n in range(1, 7)]
SPEC = [("Type","Used"), ("Year","2017"), ("Make","Dodge"), ("Model","Viper GTC ACR"),
        ("Stock","22703"), ("Mileage","38 mi"), ("Exterior","Venom Black Clear Coat"),
        ("Interior","Black"), ("VIN","1C3BDEDZXHV500169")]
HILITE = ["645 horsepower", "1 of 31 produced", "Extreme Aero package",
          "19-inch satin black ACR wheels", "ACR interior package", "Delivery miles — 38 from new"]

def specrow(k, v):
    return f'''          <div class="spec__item">
            <span class="micro spec__k">{k}</span>
            <span class="spec__v">{html.escape(v)}</span>
          </div>'''

def thumb(i, src_):
    cur = "true" if i == 0 else "false"
    eager = "eager" if i == 0 else "lazy"
    return f'''          <button class="gal__thumb" type="button" data-frame="{i}" aria-current="{cur}"
                  aria-label="Photograph {i+1} of 6">
            <img src="{src_}" alt="" width="1600" height="1066" loading="{eager}" decoding="async">
          </button>'''

def frame(i, src_):
    cls = "is-active" if i == 0 else ""
    load = 'fetchpriority="high"' if i == 0 else 'loading="lazy"'
    return f'''          <img class="{cls}" data-frame="{i}" src="{src_}"
               alt="2017 Dodge Viper GTC ACR Voodoo II, photograph {i+1} of 6"
               width="1600" height="1066" {load} decoding="async">'''

others = [c for c in cars if not c.get("vdp")][:3]

vdp_head = make_head(
    "2017 Dodge Viper GTC ACR Voodoo II — Chicago Motor Cars",
    "2017 Dodge Viper GTC ACR Voodoo II Extreme Aero. One of 31 produced, 38 delivery miles. "
    "Stock 22703 at Chicago Motor Cars.",
    '<link rel="preload" as="image" href="assets/img/inventory-live/vdp-viper-1.jpg" fetchpriority="high">')

vdp = f"""<!DOCTYPE html>
<!-- ============================================================
     vdp.html — THE VEHICLE DETAIL PAGE
     ============================================================
     Built 2026-08-17 for the index_2 preview. Head, masthead and footer
     are copied from index_2.html at build time, same as srp.html.

     THIS IS A REAL CAR AND EVERY FIGURE ON THE PAGE IS THEIRS.
     2017 Dodge Viper GTC ACR Voodoo II Extreme Aero, stock 22703, VIN
     1C3BDEDZXHV500169, 38 miles, Venom Black Clear Coat over black,
     $899,500 plus a $377 documentation fee and a $35 electronic filing
     fee for a $899,912 total. All six photographs are the listing's own.
     Pulled from chicagomotorcars.com on 2026-08-17.

     THE PRICE BREAKDOWN IS THE ONE REAL IDEA HERE. Their feed already
     carries those three figures separately and almost every dealer site
     collapses them into one number with a disclaimer underneath. Showing
     the addition is more honest AND better looking in this register: it
     is a receipt, and a receipt is the most editorial financial object
     there is.
     ============================================================ -->
<html lang="en">
{vdp_head}
<body class="v2">

{mark_current(header, 'INVENTORY')}
{between.rstrip()}

<main>

  <section class="vdp">
    <div class="shell">

      <a class="backlink" href="srp.html">
        <svg width="14" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M13 5H1M5.5 1 1 5l4.5 4" stroke="currentColor" stroke-width="1.3"/></svg>
        Back to inventory
      </a>

      <div class="vdp__grid">

        <div class="gal">
          <div class="gal__stage">
{chr(10).join(frame(i, s) for i, s in enumerate(GALLERY))}
          </div>
          <div class="gal__strip" role="group" aria-label="Photographs">
{chr(10).join(thumb(i, s) for i, s in enumerate(GALLERY))}
          </div>

        </div>

        <div class="vdp__rail">
          <p class="micro vdp__eyebrow">Stock 22703 &middot; 1 of 31</p>
          <h1 class="vdp__title">2017 Dodge Viper GTC ACR<br>Voodoo II Extreme Aero</h1>
          <p class="vdp__trim">Thirty-eight miles from new, in Venom Black Clear Coat over black,
            with the Extreme Aero package and the ACR interior. One of thirty-one built.</p>

          <!-- Three figures and their sum, because that is what the feed
               actually carries. Nothing is rounded and nothing is hidden
               behind an asterisk. -->
          <dl class="price">
            <div class="price__row"><dt>Price</dt><dd>$899,500</dd></div>
            <div class="price__row"><dt>Documentation fee</dt><dd>$377</dd></div>
            <div class="price__row"><dt>Electronic filing fee</dt><dd>$35</dd></div>
            <div class="price__row price__row--total">
              <dt>Total price</dt>
              <dd class="price__total">$899,912</dd>
            </div>
          </dl>

          <div class="vdp__acts">
            <a class="btn btn--accent" href="https://www.chicagomotorcars.com/finance-application/">
              Get financing
              <svg class="btn__arrow" width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true"><path d="M2 6.5h9M7.4 3 11 6.5 7.4 10" stroke="currentColor" stroke-width="1.3"/></svg>
            </a>
            <a class="btn btn--line" href="https://www.chicagomotorcars.com/contact-chicago-motor-cars-in-chicago-il/">
              Talk to a specialist
              <svg class="btn__arrow" width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true"><path d="M2 6.5h9M7.4 3 11 6.5 7.4 10" stroke="currentColor" stroke-width="1.3"/></svg>
            </a>
          </div>

        </div>

      </div>

      <!-- FULL WIDTH, under both columns. In the rail it left the left
           column empty; in the left column it left the right empty. It
           belongs to neither: the gallery and the rail are a matched
           pair — look at it, decide about it — and the specification is
           what you read after both. Spanning the measure also lets it be
           four columns instead of three, which is what a table wants. -->
      <div class="spec">
{chr(10).join(specrow(k, v) for k, v in SPEC)}
      </div>

      <ul class="hilite">
{chr(10).join("        <li>%s</li>" % h for h in HILITE)}
      </ul>
    </div>
  </section>

  <!-- Three more, from the same results page this car was reached through.
       Same card, same grid, no second component. -->
  <section class="inv-results" data-reveal>
    <div class="shell">
      <p class="micro eyebrow">More from the collection</p>
      <div class="grid">
{chr(10).join(card(c, i) for i, c in enumerate(others))}
      </div>
    </div>
  </section>

</main>

  {footer}

{script}
</body>
</html>
"""

open(os.path.join(ROOT, "srp.html"), "w").write(srp)
open(os.path.join(ROOT, "vdp.html"), "w").write(vdp)
print("srp.html %d bytes, %d cards" % (len(srp), len(cars)))
print("vdp.html %d bytes" % len(vdp))
