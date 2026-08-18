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
    # inventory.css goes last, after v2.css — MATCHED BY PATTERN, NOT BY
    # LITERAL. The first version of this line carried "v2.css?v=58"
    # spelled out. index_2 moved to v61, the replace stopped matching,
    # and it failed the worst way a string replace can: silently. The
    # rebuilt page simply had no inventory.css link and rendered as an
    # unstyled stack of six full-size photographs.
    #
    # The version for inventory.css is read off srp.html, which is
    # hand-maintained and therefore always current, so the two pages
    # cannot ask for different builds of the same file again.
    inv_v = "1"
    try:
        srp_src = open(os.path.join(ROOT, "srp.html")).read()
        m = re.search(r"inventory\.css\?v=(\d+)", srp_src)
        if m:
            inv_v = m.group(1)
    except OSError:
        pass
    h, n = re.subn(r'(<link rel="stylesheet" href="assets/css/v2\.css\?v=\d+">)',
                   r'\1\n<!-- Last again. srp.html and vdp.html load this; index_2.html\n'
                   r'     does not, and index.html loads neither. -->\n'
                   r'<link rel="stylesheet" href="assets/css/inventory.css?v=%s">' % inv_v,
                   h)
    if n != 1:
        raise SystemExit("ABORT: could not place inventory.css after v2.css "
                         "(matched %d times). The head changed shape; fix this "
                         "script rather than shipping a page with no stylesheet." % n)
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

# ---- the panel's rows. EVERY ONE OF THESE IS IN THE FEED ------------
# Transmission and drivetrain are deliberately absent. The 2017 Viper is
# a six-speed rear-drive car and everybody knows it, but the listing does
# not say so, and this page does not get to fill gaps from general
# knowledge — the reason for wiring it to the live feed was that it says
# only what the business says.
PANEL = [("Year", "2017"), ("Make", "Dodge"), ("Model", "Viper GTC ACR"),
         ("Exterior", "Venom Black Clear Coat"), ("Interior", "Black"),
         ("Mileage", "38 mi"), ("Stock", "22703"), ("VIN", "1C3BDEDZXHV500169")]

EQUIP = ["Extreme Aero package", "ACR interior package",
         "19-inch satin black ACR wheels", "645 horsepower",
         "Venom Black Clear Coat over black", "Delivery miles — 38 from new"]

STANDARDS = [
    ("Inspected in house",
     "Chicago Motor Cars runs its own service department — inspection, brakes, "
     "alignment, electrical and transmission work happen on site rather than at "
     "a third party."),
    ("Coverage available",
     "Aftermarket plans for pre-owned exotic, performance and collector vehicles, "
     "matched to the car rather than sold as one product."),
    ("Delivered nationwide",
     "Four showrooms across Illinois, South Carolina and Kansas, and delivery to "
     "your door anywhere in the country."),
    ("Since 2003",
     "More than 40,000 exotic, luxury and collector vehicles sold, and over "
     "$4 billion in worldwide sales."),
]

NL = chr(10)


def prow(k, v):
    return '            <div class="srow"><dt>%s</dt><dd>%s</dd></div>' % (k, html.escape(v))


def shot(i, src_):
    return ('        <a href="%s" target="_blank" rel="noopener" '
            'aria-label="Photograph %d of 6, full size">%s'
            '          <img src="%s" alt="2017 Dodge Viper GTC ACR Voodoo II, photograph %d of 6"%s'
            '               width="1600" height="1066" loading="lazy" decoding="async">%s'
            '        </a>') % (src_, i + 1, NL, src_, i + 1, NL, NL)


others = [c for c in cars if not c.get("vdp")][:3]

PANEL_ROWS = NL.join(prow(k, v) for k, v in PANEL)
FRAMES = NL.join(frame(i, s) for i, s in enumerate(GALLERY))
THUMBS = NL.join(thumb(i, s) for i, s in enumerate(GALLERY))
SHOTS = NL.join(shot(i, s) for i, s in enumerate(GALLERY))
EQUIP_LIS = NL.join('              <li>%s</li>' % e for e in EQUIP)
STD_ITEMS = NL.join(
    '          <div class="stds__item"><span class="stds__k">%s</span>'
    '<span class="stds__v">%s</span></div>' % (k, v) for k, v in STANDARDS)
RELATED = NL.join(card(c, i) for i, c in enumerate(others))
ARROW = ('<svg class="btn__arrow" width="13" height="13" viewBox="0 0 13 13" fill="none" '
         'aria-hidden="true"><path d="M2 6.5h9M7.4 3 11 6.5 7.4 10" stroke="currentColor" '
         'stroke-width="1.3"/></svg>')

vdp = """<!DOCTYPE html>
<!-- ============================================================
     vdp.html — THE VEHICLE DETAIL PAGE
     ============================================================
     Rebuilt 2026-08-18 to the Prestige VDP's composition, on Alex's
     instruction, and to nothing else of it: "делай с нашими spacings,
     tags, pills, fonts, colors."

     WHAT WAS TAKEN from prestige-final/vdp.html is the ORDER OF THE
     ARGUMENT — breadcrumb, a summary with the photograph left and the
     decision right, a full-width action bar under it, a standards
     band, three accordions, the gallery at size, related vehicles —
     and one structural idea worth naming: the specification belongs
     BESIDE the price, not two screens below it. A buyer looking at the
     car wants the colour, the mileage and the VIN in the same glance.
     Our first build put the spec table under both columns, which reads
     well and answers the wrong question.

     WHAT WAS NOT TAKEN is everything you can see. Prestige is a light
     page of white boxes with black fill buttons and its own type.
     This is the CMC dark ground, the CMC card, the CMC hairline, the
     CMC red pill, the CMC type scale. Not one value was copied across.

     WHAT WE KEPT THAT PRESTIGE DOES NOT HAVE is the price receipt.
     Their panel shows a single number. Ours shows the three figures
     the feed actually carries and their sum — more honest, and decided
     here first, so the reference does not overrule it.

     EVERY FIGURE IS THEIRS. 2017 Dodge Viper GTC ACR Voodoo II Extreme
     Aero, stock 22703, VIN 1C3BDEDZXHV500169, 38 miles, Venom Black
     Clear Coat over black, $899,500 plus a $377 documentation fee and
     a $35 electronic filing fee for a $899,912 total, six of its own
     photographs. Pulled from chicagomotorcars.com 2026-08-17.

     TWO PLACES WHERE THE REFERENCE HAD SOMETHING AND WE LEFT A GAP,
     on purpose. Prestige's action bar carries Carfax, AutoCheck and
     iPacket marks; we have no evidence CMC carries any of the three,
     and an invented badge is worse than an empty corner, so the slot
     holds facts about this car instead. Prestige's third accordion is
     a payment calculator; a monthly figure on a $900k car depends on
     the deposit, the term and the lender, and a slider that guesses
     all three tells you something untrue, so that panel explains the
     route and links to their real application.
     ============================================================ -->
<html lang="en">
%(head)s
<body class="v2">

%(header)s
%(between)s

<main>

  <section class="vdp">
    <div class="shell">

      <nav class="crumbs" aria-label="Breadcrumb">
        <a href="index_2.html">Home</a>
        <span class="crumbs__sep" aria-hidden="true">/</span>
        <a href="srp.html">Inventory</a>
        <span class="crumbs__sep" aria-hidden="true">/</span>
        <span aria-current="page">2017 Dodge Viper GTC ACR</span>
      </nav>

      <!-- ---- SUMMARY: the photograph, and the decision ---- -->
      <div class="sum">

        <div class="gal">
          <div class="gal__stage">
%(frames)s
            <span class="gal__count">
              <svg width="13" height="12" viewBox="0 0 13 12" fill="none" aria-hidden="true"><rect x="0.6" y="2.1" width="11.8" height="9.3" rx="1.4" stroke="currentColor" stroke-width="1.1"/><path d="M3.6 2.1 4.6.6h3.8l1 1.5" stroke="currentColor" stroke-width="1.1"/><circle cx="6.5" cy="6.7" r="2.1" stroke="currentColor" stroke-width="1.1"/></svg>
              6 photographs
            </span>
          </div>
          <div class="gal__strip" role="group" aria-label="Photographs">
%(thumbs)s
          </div>
        </div>

        <div class="panel">
          <div class="panel__head">
            <p class="micro vdp__eyebrow">Stock 22703 &middot; 1 of 31</p>
            <h1 class="panel__title">2017 Dodge Viper GTC ACR<br>Voodoo II Extreme Aero</h1>
          </div>

          <!-- Three figures and their sum, because that is what the feed
               carries. Nothing rounded, nothing behind an asterisk. -->
          <div class="panel__price">
            <dl class="price">
              <div class="price__row"><dt>Price</dt><dd>$899,500</dd></div>
              <div class="price__row"><dt>Documentation fee</dt><dd>$377</dd></div>
              <div class="price__row"><dt>Electronic filing fee</dt><dd>$35</dd></div>
              <div class="price__row price__row--total">
                <dt>Total price</dt>
                <dd class="price__total">$899,912</dd>
              </div>
            </dl>
          </div>

          <dl class="panel__specs">
%(panelrows)s
          </dl>

          <div class="panel__act">
            <a class="btn btn--accent" href="https://www.chicagomotorcars.com/contact-chicago-motor-cars-in-chicago-il/">
              Enquire about this car
              %(arrow)s
            </a>
          </div>
        </div>
      </div>

      <!-- ---- ACTION BAR ---- -->
      <div class="actbar">
        <div class="actbar__facts">
          <span class="veh__pill">1 of 31 produced</span>
          <span class="veh__pill">38 delivery miles</span>
          <span class="veh__pill">645 hp</span>
        </div>
        <div class="actbar__tools">
          <button class="tool" type="button" data-save="22703" aria-pressed="false">
            <svg width="12" height="14" viewBox="0 0 12 14" fill="none" aria-hidden="true"><path d="M1 1h10v12L6 9.6 1 13V1Z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/></svg>
            Save
          </button>
          <button class="tool" type="button" data-share aria-label="Copy a link to this vehicle">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M5.4 8.6 8.6 5.4M6 2.6 7.4 1.2a2.6 2.6 0 0 1 3.7 3.7L9.7 6.3M8 11.4 6.6 12.8a2.6 2.6 0 0 1-3.7-3.7L4.3 7.7" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
            Share
          </button>
        </div>
        <div class="actbar__contact">
          <a class="telpill" href="tel:+16302211800">
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M11 8.6v1.6c0 .5-.4.9-.9.8A9.6 9.6 0 0 1 1 1.9c0-.5.4-.9.8-.9h1.6c.4 0 .8.3.9.7l.4 1.8c0 .3 0 .6-.3.8l-.8.7a7.6 7.6 0 0 0 3.4 3.4l.7-.8c.2-.2.5-.3.8-.2l1.8.4c.4.1.7.4.7.8Z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/></svg>
            630 221 1800
          </a>
          <a class="btn btn--line" href="https://www.chicagomotorcars.com/finance-application/">
            Start financing
            %(arrow)s
          </a>
        </div>
      </div>

      <!-- ---- STANDARDS ----
           Prestige's band is "First-Class Standards" over a 110-point
           inspection. CMC publishes no point count, so this one claims
           only what their own site says: the service department's real
           list, the warranty offer, four showrooms with nationwide
           delivery, and the two figures the homepage already carries.
           No number here exists to fill a shape. -->
      <section class="stds" data-reveal>
        <p class="micro eyebrow">What comes with it</p>
        <h2 class="stds__title"><span class="ttl-line">Standards worth</span> <span class="ttl-line">the car.</span></h2>
        <div class="stds__grid">
%(standards)s
        </div>
      </section>

      <!-- ---- ACCORDIONS ----
           <details>, not a scripted disclosure: it opens without
           JavaScript, it is keyboard-operable by construction, and the
           browser's own find-in-page reaches the closed ones. -->
      <section class="vdp-acc" data-reveal>
        <details class="acc" open>
          <summary class="acc__sum">About this vehicle <span class="acc__mark" aria-hidden="true"></span></summary>
          <div class="acc__body">
            <p>Thirty-eight miles from new. This is a delivery-mileage car: it left the
              factory, it was transported, and it has not been used since.</p>
            <span class="acc__sub">The specification</span>
            <p>Viper GTC ACR in Venom Black Clear Coat over black, with the Extreme Aero
              package and the ACR interior package, on 19-inch satin black ACR wheels.
              645 horsepower.</p>
            <span class="acc__sub">Why it is rare</span>
            <p>One of thirty-one produced. GTC was Dodge's bespoke-order programme, so this
              combination of colour, aero and interior was specified once and built once.</p>
            <span class="acc__sub">What we can tell you</span>
            <p>Everything above is from the listing itself. For service history,
              documentation and anything not stated here, call 630 221 1800 and ask — a car
              at this mileage is worth a conversation rather than a form.</p>
          </div>
        </details>

        <details class="acc">
          <summary class="acc__sum">Options &amp; equipment <span class="acc__mark" aria-hidden="true"></span></summary>
          <div class="acc__body">
            <ul class="eqp">
%(equip)s
            </ul>
            <p>This is the equipment named in the listing. It is not a full build sheet —
              ask for one and we will send it.</p>
          </div>
        </details>

        <details class="acc">
          <summary class="acc__sum">Financing <span class="acc__mark" aria-hidden="true"></span></summary>
          <div class="acc__body">
            <p>Chicago Motor Cars finances its own sales and works with lenders who
              underwrite exotic and collector vehicles, including cars at this value. Terms
              are quoted against the total price above &mdash; $899,912 &mdash; not against
              a stripped figure.</p>
            <p>There is no payment calculator on this page on purpose. A monthly number on a
              car like this depends on the deposit, the term and the lender, and a slider
              that guesses all three tells you something that is not true.</p>
            <p><a class="btn btn--line" href="https://www.chicagomotorcars.com/finance-application/">Start an application
              %(arrow)s</a></p>
          </div>
        </details>
      </section>

      <!-- ---- GALLERY ---- -->
      <section class="vdp-gal" data-reveal>
        <p class="micro eyebrow">Gallery</p>
        <h2 class="stds__title"><span class="ttl-line">Six photographs.</span></h2>
        <div class="shots">
%(shots)s
        </div>
      </section>

    </div>
  </section>

  <!-- Three more, from the results page this car was reached through.
       Same card, same grid, no second component. -->
  <section class="inv-results" data-reveal>
    <div class="shell">
      <p class="micro eyebrow">More from the collection</p>
      <div class="grid">
%(related)s
      </div>
    </div>
  </section>

</main>

  %(footer)s

%(script)s
</body>
</html>
""" % {
    "head": vdp_head,
    "header": mark_current(header, 'INVENTORY'),
    "between": between.rstrip(),
    "frames": FRAMES,
    "thumbs": THUMBS,
    "panelrows": PANEL_ROWS,
    "standards": STD_ITEMS,
    "equip": EQUIP_LIS,
    "shots": SHOTS,
    "related": RELATED,
    "arrow": ARROW,
    "footer": footer,
    "script": script,
}

# srp.html IS NO LONGER WRITTEN BY THIS SCRIPT, and that is deliberate.
#
# It was hand-rebuilt across nine commits on 2026-08-18 — a new head
# ported from the Vegas reference, working filters, srp-head.css and
# srp.js — none of which this script knows about. Running it regenerated
# srp.html from the old template and silently deleted 525 lines of that
# work. It was caught by a git diff and restored, but only because the
# rebuild happened to break something else and sent me looking.
#
# A generator that owns a file someone else is editing by hand is a
# generator that will eat their work eventually. This one now owns
# vdp.html only. The `srp` string above is still built because the card
# markup and the head assembly are shared with the VDP; it is simply not
# written to disk.
open(os.path.join(ROOT, "vdp.html"), "w").write(vdp)
print("vdp.html %d bytes  (srp.html deliberately NOT written — hand-maintained)" % len(vdp))
