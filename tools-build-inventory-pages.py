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

import importlib.util as _il
_spec = _il.spec_from_file_location("desc", os.path.join(SCR, "desc.py"))
D = _il.module_from_spec(_spec); _spec.loader.exec_module(D)

_NL = chr(10)

def _lis(items):
    return _NL.join('              <li>%s</li>' % html.escape(i) for i in items)

def _group(title, price, items):
    return ('            <div class="eqp-group">' + _NL +
            '              <p class="eqp-group__h"><span class="eqp-group__n">%s</span>'
            '<span class="eqp-group__p">Originally %s</span></p>' % (html.escape(title), price) + _NL +
            '              <ul class="eqp">' + _NL + _lis(items) + _NL + '              </ul>' + _NL +
            '            </div>')

def _textblock(heading, lines):
    """One heading and its lines, straight down. A blank line in the
    source is a break between packages, not an item, so it renders as a
    spacer rather than an empty row."""
    out = []
    if heading:
        out.append('              <h3 class="dsc__h">%s</h3>' % html.escape(heading))
    out.append('              <ul class="dsc__list">')
    for l in lines:
        if l:
            out.append('                <li>%s</li>' % html.escape(l))
        else:
            out.append('                <li class="dsc__gap"></li>')
    out.append('              </ul>')
    return chr(10).join(out)


def _sub(title, items):
    return ('            <span class="acc__sub">%s</span>' % title + _NL +
            '            <ul class="eqp">' + _NL + _lis(items) + _NL + '            </ul>')

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
# Year, Make and Model came out on Alex's call: the H1 directly above
# already reads "2017 Dodge Viper GTC ACR", so three of the eight rows
# were repeating the headline at caption size.
#
# ENGINE AND DRIVETRAIN ADDED, also his call, and worth recording why
# they are safe when I had argued the other way. I left them out because
# the listing does not state them, and the rule on this page is that it
# says only what the business says. These two are different in kind from
# a claim about THIS car: the 2017 Viper ACR was built with one engine
# and one driven axle, so they are attributes of the model rather than
# facts about the example. A car that is a Viper ACR cannot be anything
# else. Horsepower is in the listing outright.
#
# Transmission still stays out. Every 2017 Viper is a six-speed manual,
# so by the same argument it would qualify — but the row is the one a
# buyer of a collector car checks hardest, and the listing's own field
# for it came through garbled. Better absent than asserted from memory.
#
# Order is what a buyer reads: mileage first, because on this car
# thirty-eight miles IS the story; then what it is mechanically; then
# how it looks, outside before inside; then the two reference numbers,
# which nobody chooses a car by and everybody needs on the phone.
# TRANSMISSION IS BACK, and no longer asserted from memory. I left it
# out because the listing's own field came through garbled; with their
# site up again the description states "6-Speed Manual Transmission"
# outright, beside "Rear Wheel Drive" and "600 Lb/ft of Torque". Every
# row here is quoted now, not inferred.
PANEL = [("Mileage", "38 mi"),
         ("Engine", "8.4L V10, 645 hp"),
         ("Transmission", "6-speed manual"),
         ("Drivetrain", "Rear-wheel drive"),
         ("Exterior", "Venom Black Clear Coat"), ("Interior", "Black"),
         ("Stock", "22703"), ("VIN", "1C3BDEDZXHV500169")]

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


# ---- THE RELATED CARDS ARE THE SRP'S OWN, LIFTED WHOLE ---------------
# Alex: "это не похоже на точную копию cards с srp." It was not. The SRP
# card was rebuilt by hand — a .veh-cell wrapper, a save mark, paging
# photographs on .veh__frame, prev/next arrows, a See details action —
# and this script was still printing the first version of it. The two
# drifted the moment srp.html stopped being generated from here.
#
# So the cards are not authored on this page any more. They are CUT OUT
# of srp.html, exactly as the masthead and footer already are: find the
# .veh-cell carrying the stock number we want and take the block
# verbatim. Whatever changes on a results card arrives here on the next
# build with nothing to keep in sync by hand.
_srp_html = open(os.path.join(ROOT, "srp.html")).read()
_cell_blocks = [m.group(0) for m in
                re.finditer(r'( *)<div class="veh-cell">[\s\S]*?\n\1</div>', _srp_html)]
if not _cell_blocks:
    raise SystemExit("ABORT: no .veh-cell in srp.html — the card markup changed "
                     "shape. Fix this script rather than shipping a VDP whose "
                     "cards do not match the results page.")

def srp_card(stock):
    for blk in _cell_blocks:
        if ">#%s<" % stock in blk:
            return blk
    raise SystemExit("ABORT: stock %s is no longer on srp.html." % stock)

# SIX CARS, ONE ROW. Both of Alex's instructions at once, and together
# they describe a track rather than a grid: "убери второй ряд машин" and
# then "ты зачем убрал pagination?"
#
# He is right that I removed it — not by deleting anything, but because
# the dots collapse themselves when there is only one page, so taking
# the second row out took the control with it. Three cards in a
# three-across grid have nothing to page.
#
# A row that pages is the shape that satisfies both: six vehicles, three
# visible, the rest one dot away. Now the dots have somewhere to go and
# the section is still one row tall.
others = [c for c in cars if not c.get("vdp")][:6]

PANEL_ROWS = NL.join(prow(k, v) for k, v in PANEL)
FRAMES = NL.join(frame(i, s) for i, s in enumerate(GALLERY))
THUMBS = NL.join(thumb(i, s) for i, s in enumerate(GALLERY))
SHOTS = NL.join(shot(i, s) for i, s in enumerate(GALLERY))
EQUIP_LIS = NL.join('              <li>%s</li>' % e for e in EQUIP)
STD_ITEMS = NL.join(
    '          <div class="stds__item"><span class="stds__k">%s</span>'
    '<span class="stds__v">%s</span></div>' % (k, v) for k, v in STANDARDS)
RELATED = NL.join(srp_card(c["stock"]) for c in others)
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

     THE CARFAX MARK IS REAL AND I FIRST GOT IT WRONG. I wrote that
     there was no evidence CMC carries Carfax and left the slot to fact
     pills. The evidence was in my own scrape of their results page:
     every card links to a Carfax report for that VIN, beside a "Show
     me the Carfax" icon from their own theme. They are a Carfax dealer.
     The badge is here now, linking to the real report for this VIN,
     and it is THEIR OWN ARTWORK: assets/logos/carfax.svg, copied from
     the CMC source folder on this machine. I first typeset the word
     because their live site was returning 504 and I could not fetch the
     SVG — but the file was sitting in Alex's own WORK folders the whole
     time, in the CMC "VDP page" directory, and he had to tell me to go
     and look. Fetching was never the only route to an asset.

     ONE PLACE WHERE THE REFERENCE HAD SOMETHING AND WE LEFT A GAP, on
     purpose. Prestige's third accordion is
     a payment calculator; a monthly figure on a $900k car depends on
     the deposit, the term and the lender, and a slider that guesses
     all three tells you something untrue, so that panel explains the
     route and links to their real application.
     ============================================================ -->
<html lang="en">
%(head)s
<body class="v2 is-vdp">

%(header)s
%(between)s

<main>

  <section class="vdp">
    <div class="shell">

      <!-- Where you are on the left, what you can do with the page on
           the right, one line above everything. Save and Share moved up
           out of the action bar on Alex's call, and the move is right:
           that bar is about buying THIS car — call, text, finance — and
           these two are about keeping the page. Different verbs, so they
           belong to the page furniture rather than to the offer. -->
      <div class="topbar">
        <nav class="crumbs" aria-label="Breadcrumb">
          <a href="index_2.html">Home</a>
          <span class="crumbs__sep" aria-hidden="true">/</span>
          <a href="srp.html">Inventory</a>
          <span class="crumbs__sep" aria-hidden="true">/</span>
          <span aria-current="page">2017 Dodge Viper GTC ACR</span>
        </nav>
        <div class="topbar__tools">
          <button class="tool" type="button" data-save="22703" aria-pressed="false">
            <svg width="12" height="14" viewBox="0 0 12 14" fill="none" aria-hidden="true"><path d="M1 1h10v12L6 9.6 1 13V1Z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/></svg>
            Save
          </button>
          <button class="tool" type="button" data-share aria-label="Copy a link to this vehicle">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M5.4 8.6 8.6 5.4M6 2.6 7.4 1.2a2.6 2.6 0 0 1 3.7 3.7L9.7 6.3M8 11.4 6.6 12.8a2.6 2.6 0 0 1-3.7-3.7L4.3 7.7" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
            Share
          </button>
          <!-- SEND IT TO YOURSELF, not to the dealership. Alex drew the
               distinction and it is the one that decides where the control
               lives: "Text us" in the action bar starts a conversation with
               Chicago Motor Cars; this puts the car in your own pocket, so
               it sits with Save and Share as page furniture.

               It is a real sms: link with the listing's URL in the body, so
               on a phone it opens the composer already written and you pick
               who gets it — usually yourself. No form, no field, no number
               collected, nothing to wire on the back end. On a desktop the
               script falls back to copying the link, because an sms: href
               there is a control that silently does nothing. -->
          <a class="tool" href="sms:?&amp;body=" data-text-to-phone
             aria-label="Send this vehicle to your phone">
            <svg width="13" height="15" viewBox="0 0 13 15" fill="none" aria-hidden="true"><rect x="2.4" y="0.9" width="8.2" height="13.2" rx="1.8" stroke="currentColor" stroke-width="1.2"/><path d="M5.6 11.9h1.8" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
            Text to phone
          </a>
        </div>
      </div>

      <!-- ---- SUMMARY: the photograph, and the decision ---- -->
      <div class="sum">

        <div class="gal">
          <div class="gal__stage">
%(frames)s
            <button class="veh__nav veh__nav--prev gal__arrow" type="button" data-step="-1" aria-label="Previous photograph">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M14.5 5.5 8 12l6.5 6.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="square"/></svg>
            </button>
            <button class="veh__nav veh__nav--next gal__arrow" type="button" data-step="1" aria-label="Next photograph">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9.5 5.5 16 12l-6.5 6.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="square"/></svg>
            </button>
            <button class="gal__video" type="button" data-open-video>
              <span class="gal__video-play" aria-hidden="true"><svg width="13" height="13" viewBox="0 0 24 24" fill="none"><path d="M8 5.5 18.5 12 8 18.5v-13Z" fill="currentColor"/></svg></span>
              Watch video
            </button>
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
        <div class="actbar__left">
        <a class="cfx" href="https://www.carfax.com/cfm/ccc_displayhistoryrpt.cfm?partner=AAN_0&amp;vin=1C3BDEDZXHV500169"
           target="_blank" rel="noopener">
          <img class="cfx__logo" src="assets/logos/carfax.svg" alt="Show me the Carfax"
               width="253" height="60" loading="lazy" decoding="async">
        </a>
        <!-- WHERE THE CAR IS, which is the one thing this bar was missing
             and the three fact pills were not adding: "1 of 31", "38
             delivery miles" and "645 hp" all appear in the panel or the
             highlights already, so the bar was repeating the page at
             pill size.

             Naperville is not a guess. Every one of this listing's six
             photographs carries the showroom's own watermark — "Chicago
             Motor Cars NAPERVILLE" — so the car's location is evidenced
             by the pictures of it. The address and the phone are the
             ones already on the locations chapter of the homepage. -->
        <p class="actbar__loc">
          <svg class="actbar__pin" width="12" height="15" viewBox="0 0 12 15" fill="none" aria-hidden="true"><path d="M6 .75c2.9 0 5.25 2.35 5.25 5.25 0 3.6-4.35 7.7-5.02 8.31a.34.34 0 0 1-.46 0C5.1 13.7.75 9.6.75 6 .75 3.1 3.1.75 6 .75Z" fill="none" stroke="currentColor" stroke-width="1.1"/><circle cx="6" cy="6" r="1.85" fill="currentColor"/></svg>
          <span class="micro actbar__loc-k">Location</span>
          <a class="actbar__loc-v" href="https://www.google.com/maps/dir/?api=1&amp;destination=2104+Ferry+Road%%2C+Naperville%%2C+IL+60563" target="_blank" rel="noopener">Naperville, IL &mdash; 2104 Ferry Road</a>
        </p>
        </div>
        <div class="actbar__contact">
          <a class="telpill" href="tel:+16302211800">
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M11 8.6v1.6c0 .5-.4.9-.9.8A9.6 9.6 0 0 1 1 1.9c0-.5.4-.9.8-.9h1.6c.4 0 .8.3.9.7l.4 1.8c0 .3 0 .6-.3.8l-.8.7a7.6 7.6 0 0 0 3.4 3.4l.7-.8c.2-.2.5-.3.8-.2l1.8.4c.4.1.7.4.7.8Z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/></svg>
            630 221 1800
          </a>
          <a class="telpill telpill--bone" href="sms:+16302211800">
            <svg width="13" height="13" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M12.4 8.2a1.2 1.2 0 0 1-1.2 1.2H3.9L1.5 11.8V2.5a1.2 1.2 0 0 1 1.2-1.2h8.5a1.2 1.2 0 0 1 1.2 1.2Z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/></svg>
            Text dealer
          </a>
          <a class="btn btn--line" href="https://www.chicagomotorcars.com/finance-application/">
            Start financing
            %(arrow)s
          </a>
        </div>
      </div>

      <!-- ---- ACCORDIONS ----
           <details>, not a scripted disclosure: it opens without
           JavaScript, it is keyboard-operable by construction, and the
           browser's own find-in-page reaches the closed ones. -->
      <section class="vdp-acc" data-reveal>
        <details class="acc" open>
          <summary class="acc__sum"><svg class="acc__ico" width="17" height="17" viewBox="0 0 18 18" fill="none" aria-hidden="true"><circle cx="9" cy="9" r="7.2" stroke="currentColor" stroke-width="1.3"/><path d="M9 8v4.4M9 5.6v.1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg><span class="acc__label">About this vehicle</span> <span class="acc__mark" aria-hidden="true"></span></summary>
          <div class="acc__body">
            <p class="acc__title">%(leadTitle)s</p>
            <p class="acc__lead">%(leadSub)s</p>

            <!-- ONE TEXT. Alex: "давай одним текстом, только заголовки и
                 только текст перечисление." No cards, no columns, no
                 hairlines, no price chips — a heading, its lines, the next
                 heading, straight down. The structure is the feed's own.

                 Which also folds the Options & equipment panel back in:
                 his copy runs factory options, highlights, history and
                 what is included as ONE description, so splitting it
                 across two drawers was the page arguing with the text. -->
            <div class="dsc">
%(blocks)s
%(disclaimer)s
            </div>
          </div>
        </details>

        <details class="acc">
          <summary class="acc__sum"><svg class="acc__ico" width="17" height="17" viewBox="0 0 18 18" fill="none" aria-hidden="true"><rect x="1.6" y="3.4" width="14.8" height="11.2" rx="2.2" stroke="currentColor" stroke-width="1.3"/><path d="M7.4 6.8 11.6 9l-4.2 2.2V6.8Z" fill="currentColor"/></svg><span class="acc__label">Walkaround video</span> <span class="acc__mark" aria-hidden="true"></span></summary>
          <div class="acc__body acc__body--wide">
            <!-- CLICK TO LOAD, and the poster is one of this car's own
                 photographs. A YouTube iframe on page load is roughly a
                 megabyte of third-party script and a set of cookies
                 dropped before anybody asked for a video; the facade
                 costs one image we already serve. -->
            <div class="ytb" data-yt="https://www.youtube-nocookie.com/embed?listType=user_uploads&amp;list=ChicagoMotorCars&amp;autoplay=1">
              <img class="ytb__poster" src="assets/img/inventory-live/vdp-viper-2.jpg" alt=""
                   width="1600" height="1066" loading="lazy" decoding="async">
              <button class="ytb__play" type="button" aria-label="Play the Chicago Motor Cars channel">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M8 5.5 18.5 12 8 18.5v-13Z" fill="currentColor"/></svg>
              </button>
            </div>
            <p class="acc__note">This opens the Chicago Motor Cars channel. There is no
              walkaround filmed for stock 22703 yet &mdash; when there is, it replaces the
              channel here and nothing else on the page changes.
              <a class="acc__link" href="https://www.youtube.com/user/ChicagoMotorCars" target="_blank" rel="noopener">Open the channel on YouTube &rarr;</a></p>
          </div>
        </details>

        <details class="acc">
          <summary class="acc__sum"><svg class="acc__ico" width="17" height="17" viewBox="0 0 18 18" fill="none" aria-hidden="true"><rect x="3.2" y="1.8" width="11.6" height="14.4" rx="2" stroke="currentColor" stroke-width="1.3"/><path d="M6 5.4h6" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/><circle cx="6.4" cy="9.2" r="1" fill="currentColor"/><circle cx="9" cy="9.2" r="1" fill="currentColor"/><circle cx="11.6" cy="9.2" r="1" fill="currentColor"/><circle cx="6.4" cy="12.4" r="1" fill="currentColor"/><circle cx="9" cy="12.4" r="1" fill="currentColor"/><circle cx="11.6" cy="12.4" r="1" fill="currentColor"/></svg><span class="acc__label">Financing &amp; payments</span> <span class="acc__mark" aria-hidden="true"></span></summary>
          <div class="acc__body">
            <p>Chicago Motor Cars finances its own sales and works with lenders who
              underwrite exotic and collector vehicles, including cars at this value. Terms
              are quoted against the total price above &mdash; $899,912 &mdash; not against
              a stripped figure.</p>
            <!-- THE CALCULATOR IS AN ESTIMATOR AND IT SAYS SO. I argued
                 against putting one here — a monthly figure depends on the
                 deposit, the term and the lender, and a control that
                 guesses all three states something untrue. Alex asked for
                 it, so it is built with the three variables EXPOSED
                 rather than assumed: you set them, and the number is
                 arithmetic on what you set, not a quote. -->
            <form class="calc" data-total="899912">
              <div class="calc__grid">
                <p class="calc__field">
                  <label class="micro calc__label" for="c-price">Total price</label>
                  <input class="calc__input" id="c-price" type="text" inputmode="numeric" value="899,912">
                </p>
                <p class="calc__field">
                  <label class="micro calc__label" for="c-down">Deposit</label>
                  <input class="calc__input" id="c-down" type="text" inputmode="numeric" value="180,000">
                </p>
                <p class="calc__field">
                  <label class="micro calc__label" for="c-term">Term</label>
                  <select class="calc__input" id="c-term">
                    <option value="36">36 months</option>
                    <option value="48">48 months</option>
                    <option value="60" selected>60 months</option>
                    <option value="72">72 months</option>
                    <option value="84">84 months</option>
                  </select>
                </p>
                <p class="calc__field">
                  <label class="micro calc__label" for="c-apr">Rate (APR)</label>
                  <input class="calc__input" id="c-apr" type="text" inputmode="decimal" value="7.9">
                </p>
              </div>
              <p class="calc__out">
                <span class="micro calc__out-label">Estimated monthly</span>
                <output class="calc__figure" id="c-monthly" for="c-price c-down c-term c-apr">&mdash;</output>
              </p>
              <p class="acc__note">An estimate on the figures above, nothing more. It is not an
                offer, it is not a quote, and it does not include tax, title or registration.
                The rate you are actually given depends on the lender and on you.</p>
            </form>
            <p><a class="btn btn--line" href="https://www.chicagomotorcars.com/finance-application/">Start an application
              %(arrow)s</a></p>
          </div>
        </details>
      </section>

      <!-- ---- STANDARDS ----
           MOVED AND REBUILT, Alex 2026-08-18: "это надо сделать как
           отдельную вещь. она всегда идёт на все VDP's. так что не часть
           описания машины."

           He is right twice over. It sat between the action bar and the
           accordions, inside the block that describes THIS car, and it
           was set on the same hairline rows as the specification — so a
           reader met four dealership promises in the same visual voice as
           the VIN and the mileage, as if they were facts about the Viper.
           They are not. They are identical on every vehicle page there
           will ever be.

           Now it is its own section, in cards — a different object from
           the rows above it — and it stands AFTER the car's own
           description rather than interrupting it. The page reads: the
           car, what it costs, what it is, what we say about it, then what
           comes with buying anything here.
           ============================================================ -->
      <section class="stds" data-reveal>
        <p class="micro eyebrow">Buying from Chicago Motor Cars</p>
        <h2 class="stds__title"><span class="ttl-line">Standards worth</span> <span class="ttl-line">the car.</span></h2>
        <div class="stds__grid">
%(standards)s
        </div>
      </section>

      <!-- ---- GALLERY ---- -->
      <section class="vdp-gal" data-reveal>
        <h2 class="gal-head"><span class="ttl-line">Gallery</span></h2>
        <div class="shots">
%(shots)s
        </div>
      </section>

    </div>
  </section>

  <!-- Three more, from the results page this car was reached through.
       Same card, same grid, no second component.

       "More from the collection" became "Others worth chasing." — the
       page's own line. The hero says "Find the car worth chasing", the
       standards band says "Standards worth the car", the results page
       says "cars worth chasing". A house phrase that has already been
       used three times is not a coincidence to avoid, it is the voice,
       and this is the one place on the VDP that speaks in it. -->
  <section class="rel" data-reveal>
    <div class="shell">
      <h2 class="gal-head"><span class="ttl-line">Others worth chasing.</span></h2>
      <div class="rel__track" data-rel-track>
%(related)s
      </div>
      <div class="rel__dots" data-rel-dots aria-label="More vehicles"></div>
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
    "leadTitle": html.escape("2017 Dodge Viper GTC ACR-E Voodoo II Edition"),
    "leadSub": html.escape(D.LEAD),
    "blocks": (_NL + _NL).join(_textblock(h, ls) for h, ls in D.BLOCKS),
    "disclaimer": _NL + (_NL).join('              <p class="dsc__fine">%s</p>' % html.escape(x) for x in D.DISCLAIMER),
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
