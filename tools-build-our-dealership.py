#!/usr/bin/env python3
"""Assemble our-dealership.html from index_3.html's head, masthead and footer.

Same principle as tools-build-inventory-pages.py: anything shared is
COPIED at build time rather than retyped, so the pages cannot drift.
index_3 is the source because it is the approved variant.

It writes our-dealership.html and NOTHING ELSE. The inventory builder once wrote
srp.html as well and deleted 525 lines of hand-maintained head; a script
that can only create the one file it is named after cannot repeat that.
"""
import re, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(ROOT, "our-dealership.html")
src  = open(os.path.join(ROOT, "index_3.html")).read()


def cut(start, end):
    """Slice src between two literals, refusing to guess.

    open(f,'w').write(x.index(...)) truncated build.py to zero bytes once,
    because the file was opened for writing before the expression was
    evaluated. Every slice here is computed and checked first; the output
    file is opened on the last line of the script.
    """
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
           "<title>Our Dealership — Chicago Motor Cars</title>", h, flags=re.S)
h = re.sub(r'<meta name="description" content=".*?">',
           '<meta name="description" content="Chicago Motor Cars has sold more than 40,000 '
           'exotic, luxury and collector vehicles since 2003, from four showrooms with a fifth '
           'opening in Newport Beach.">', h, flags=re.S)

# The LCP element here is the film band's POSTER, not the homepage's hero
# frame. It is preloaded and the film is not: the still is what paints,
# and the 2.6MB behind it is fetched by script only when the band is a
# viewport away — and never at all under reduced motion.
h, n = re.subn(r'<link rel="preload" as="image"[^>]*>',
               '<link rel="preload" as="image" '
               'href="assets/img/locations/loc-west-chicago-1200.jpg" fetchpriority="high">', h)
if n != 1:
    raise SystemExit("ABORT: expected exactly one image preload in the head, found %d" % n)

h, n = re.subn(r'(<link rel="stylesheet" href="assets/css/v3\.css\?v=\d+">)',
               r'\1\n<!-- our-dealership.html only. Last, so it wins on equal specificity. -->\n'
               r'<link rel="stylesheet" href="assets/css/our-dealership.css?v=9">', h)
if n != 1:
    raise SystemExit("ABORT: could not place our-dealership.css after v3.css (%d matches). The head "
                     "changed shape; fix this script rather than shipping a page whose "
                     "stylesheet silently never loads." % n)


# ---- their words, verbatim --------------------------------------------
# chicagomotorcars.com/about-chicago-motor-cars-in-chicago-il, read
# 2026-08-28. Four paragraphs, not one word changed — including the
# ellipsis in the first and the grammar in the second. The HEADINGS are
# ours: their page runs the four as one unbroken column, and a heading per
# paragraph is what makes it scannable without editing a business's own
# description of itself.
STORY = [
 ("The passion",
  "To be successful in this business, you have to start with a passion. Our enthusiasm "
  "for automobiles is the foundation that drives Chicago Motor Cars. When you walk "
  "through our doors, it’s not just a car dealership. It’s an organization built on the "
  "principle that driving emotion shouldn’t be a dream…it should be an experience."),
 ("What we keep",
  "Our staff enjoy the opportunity to offer the finest in McLaren, Ferrari, Lamborghini, "
  "Bentley, Porsche, Aston-Martin, Rolls-Royce, BMW, Land Rover, Mercedes-Benz and "
  "Maserati automobiles, among other. We hand-pick each and every car we offer, and our "
  "expert buyers sources the finest from coast-to-coast. Our goal is to offer the highest "
  "quality pre-owned sports, luxury and exotic vehicles at competitive market prices to "
  "make people’s dreams come true."),
 ("Going east",
  "In 2021, we expanded our geographical footprint with Chicago Motor Cars – South "
  "Carolina. Our South Carolina location hosts an impeccable collection of inventory and "
  "more opportunity to find the ideal vehicle for our clients, not to mention our east "
  "coast clientele that has chosen to entrust Chicago Motor Cars with their automotive "
  "needs. You can expect the same level of professionalism and quality that the Chicago "
  "Motor Cars team has delivered for years."),
 ("Come and see",
  "Be sure to visit us often as our inventory changes daily. Give our team a call at "
  "(630) 221-1800 and you’ll get in touch with a professional who will walk you through "
  "your options to help you move forward in securing the vehicle of your dreams. It’s a "
  "little different here at Chicago Motor Cars. We look forward to welcoming you to the "
  "Chicago Motor Cars family."),
]

# Addresses, numbers and handles are the locations panel's, so the two
# cannot disagree. `_own` marks an account belonging to THAT showroom;
# everything else falls back to the house account and says so in its
# aria-label, which is why no mark here is a dead link.
SHOWROOMS = [
 dict(city="West Chicago", addr="27W110 North Avenue, West Chicago, IL 60185",
      tel="630-221-1800", tel_href="+16302211800",
      dest="27W110+North+Avenue%2C+West+Chicago%2C+IL+60185",
      ig="https://www.instagram.com/chicagomotorcars/", ig_own=False,
      fb="https://www.facebook.com/chicagomotorcars", fb_own=False),
 dict(city="Naperville", addr="2104 Ferry Road, Naperville, IL 60563",
      tel="630-221-1800", tel_href="+16302211800",
      dest="2104+Ferry+Road%2C+Naperville%2C+IL+60563",
      ig="https://www.instagram.com/chicagomotorcars/", ig_own=False,
      fb="https://www.facebook.com/chicagomotorcars", fb_own=False),
 dict(city="Rock Hill", addr="727 Marine Drive, Rock Hill, SC 29730",
      tel="803-891-7788", tel_href="+18038917788",
      dest="727+Marine+Drive%2C+Rock+Hill%2C+SC+29730",
      ig="https://www.instagram.com/chicagomotorcarssc/", ig_own=True,
      fb="https://www.facebook.com/chicagomotorcarssc", fb_own=True),
 dict(city="Tonganoxie", addr="1650 Commerce Ave, Tonganoxie, KS 66086",
      tel="913-845-9633", tel_href="+19138459633",
      dest="1650+Commerce+Ave%2C+Tonganoxie%2C+KS+66086",
      ig="https://www.instagram.com/chicagomotorcarskc/", ig_own=True,
      fb="https://www.facebook.com/chicagomotorcarskc", fb_own=True),
 dict(city="Newport Beach", addr="California — opening soon",
      tel="630-221-1800", tel_href="+16302211800",
      dest=None, query="Newport+Beach%2C+CA", soon=True,
      ig="https://www.instagram.com/chicagomotorcars/", ig_own=False,
      fb="https://www.facebook.com/chicagomotorcars", fb_own=False),
]

IG_SVG = ('<svg viewBox="0 0 20 20" aria-hidden="true">'
          '<rect x="2.6" y="2.6" width="14.8" height="14.8" rx="4.4" fill="none" '
          'stroke="currentColor" stroke-width="1.5"/>'
          '<circle cx="10" cy="10" r="3.6" fill="none" stroke="currentColor" stroke-width="1.5"/>'
          '<circle cx="14.6" cy="5.4" r="1" fill="currentColor"/></svg>')
FB_SVG = ('<svg viewBox="0 0 20 20" aria-hidden="true">'
          '<path d="M12.6 6.7h1.9V3.9c-.33-.05-1.46-.15-2.77-.15-2.74 0-4.62 1.72-4.62 4.89v2.24'
          'H5.2v3.1h2.9v7.77h3.47v-7.77h2.78l.44-3.1h-3.22V8.95c0-.9.24-1.51 1.53-1.51Z" '
          'fill="currentColor" transform="translate(0 -1.4)"/></svg>')
ARROW = ('<svg class="btn__arrow" width="13" height="13" viewBox="0 0 13 13" fill="none" '
         'aria-hidden="true"><path d="M2 6.5h9M7.4 3 11 6.5 7.4 10" stroke="currentColor" '
         'stroke-width="1.3"/></svg>')
# The handset from .about__contact on the homepage, which is where this
# page's phone treatment comes from as well.
TEL_SVG = ('<span class="about__ico"><svg width="15" height="15" viewBox="0 0 15 15" '
           'aria-hidden="true"><path d="M4.2 1.6 5.9 4 4.6 5.7c.7 1.7 2 3 3.7 3.7L10 8.1l2.4 '
           '1.7c.4.3.5.8.2 1.2l-1 1.3c-.3.4-.8.5-1.2.4C5.9 11.6 2.4 8.1 1.3 3.6c-.1-.4 0-.9.4'
           '-1.2l1.3-1c.4-.3.9-.2 1.2.2Z" fill="currentColor"/></svg></span>')


def soc(url, own, label, svg):
    """One social mark. data-shared records that the link goes to the house
    account rather than this showroom's own — the locations panel's
    convention, and the reason nothing here points nowhere."""
    return ('<a class="%s" href="%s" target="_blank" rel="noopener" aria-label="%s"%s>%s</a>'
            % ("loc__soc is-own" if own else "loc__soc", url,
               html.escape(label, quote=True), "" if own else ' data-shared="true"', svg))


rooms = []
for s in SHOWROOMS:
    if s.get("dest"):
        map_href = "https://www.google.com/maps/dir/?api=1&amp;destination=" + s["dest"]
        map_txt  = "Get directions"
    else:
        map_href = "https://www.google.com/maps/search/?api=1&amp;query=" + s["query"]
        map_txt  = "See on map"
    rooms.append("""          <li class="ab-room%s">
            <span class="ab-room__city">%s</span>
            <span class="ab-room__addr">%s</span>
            <a class="about__tel ab-room__tel" href="tel:%s">%s<span>%s</span></a>
            <span class="ab-room__acts">
              <a class="loc__map" href="%s" rel="noopener">%s</a>
              <span class="loc__social">%s%s</span>
            </span>
          </li>""" % (
        " ab-room--soon" if s.get("soon") else "",
        html.escape(s["city"]), html.escape(s["addr"]),
        s["tel_href"], TEL_SVG, s["tel"], map_href, map_txt,
        soc(s["ig"], s["ig_own"], "%s on Instagram" % s["city"], IG_SVG),
        soc(s["fb"], s["fb_own"], "%s on Facebook" % s["city"], FB_SVG)))

story = []
for h3, para in STORY:
    story.append("""        <div class="ab-story__col">
          <h3 class="ab-story__h">%s</h3>
          <p class="ab-story__p">%s</p>
        </div>""" % (html.escape(h3), html.escape(para)))


BODY = """
<main>

  <!-- ============================================================
       1 — THE CLAIM, AND THE THREE FIGURES THAT SUPPORT IT
       ============================================================
       srp.html's page-head construction: eyebrow, headline in authored
       lines, one supporting sentence. The figures are the homepage's own
       .story__stats with the markup unchanged, so the counter in main.js
       finds them and the printed value stands if it never runs.

       40,000+ / 2003 / $4B+ are CMC's revised figures (2026-08-17). They
       appear in three places on this site and all three say the same
       thing; changing one means changing three.
       ============================================================ -->
  <section class="ab-head" data-reveal data-bloom="center">
    <div class="shell">
      <p class="micro ab-eyebrow">About Chicago Motor Cars</p>
      <h1 class="ab-title">
        <span class="ttl-line">Twenty-two years</span>
        <span class="ttl-line">of hand-picked cars.</span>
      </h1>
      <p class="lede">Four showrooms across Illinois, South Carolina and Kansas, a fifth
        opening in Newport Beach, and an inventory that changes daily.</p>

      <dl class="story__stats">
        <div class="stat stat--lead">
          <dt class="micro stat__label">Vehicles sold</dt>
          <dd class="stat__fig"><span class="stat__n" data-count-to="40000" data-suffix="+">40,000+</span></dd>
        </div>
        <div class="stat stat--proof">
          <dt class="micro stat__label">Since</dt>
          <dd class="stat__fig"><span class="stat__n">2003</span></dd>
        </div>
        <div class="stat stat--proof">
          <dt class="micro stat__label">Worldwide sales</dt>
          <dd class="stat__fig"><span class="stat__n">$4B+</span></dd>
        </div>
      </dl>
    </div>
  </section>

  <!-- ============================================================
       2 — THE BUILDING
       ============================================================
       The only photograph on the page, and the only one it is entitled
       to use. Three of the four paragraphs below are the business
       describing itself, which is the least verifiable copy there is;
       this is the frame that says the business exists somewhere.

       PROVENANCE IS SETTLED HERE, WHICH IS RARE IN THIS PROJECT. Alex's
       own dusk aerial of 27W110 North Avenue, supplied with the location
       films, and the same still the West Chicago panel opens on. Not
       synthetic, so no gen- prefix is owed. The two frames whose origin
       is NOT settled — cmc-mclaren-showroom and hero_d — are deliberately
       absent: an About page is exactly where an unattributed room makes
       its loudest claim.

       A BAND INSIDE THE SHELL, NOT A FULL-BLEED FIELD. Type over a
       full-bleed photograph is the homepage's move and it is spent twice
       there already. Framed, the picture reads as something the page is
       showing you rather than a room the page is standing in — which is
       also what keeps the paragraphs dominant.

       The caption names the address rather than describing the picture,
       because the address is the part a visitor can act on.
       ============================================================ -->
  <section class="ab-shot" data-reveal data-film>
    <div class="shell">
      <figure class="ab-shot__fig">
        <!-- THE SAME CONTRACT THE BREAK AND SERVICE BANDS USE: the source
             ships with data-src and no src, and main.js attaches it a
             viewport out. Under prefers-reduced-motion it is never
             fetched — not fetched-then-paused, not fetched at all — and
             the poster carries the band.

             The poster is not a separate asset. It is the still the West
             Chicago panel opens on, which is a real frame of this film,
             so there is no moment where the band is empty while the
             video decides whether it is ready, and the reduced-motion
             path is a photograph of the same building rather than a
             stand-in for one.

             muted, aria-hidden, tabindex -1: this is decoration in the
             accessibility tree. Every fact about the building is in the
             caption under it, which is text. -->
        <video class="ab-shot__video"
               poster="assets/img/locations/loc-west-chicago-1200.jpg"
               muted loop playsinline
               preload="none"
               width="1280" height="720"
               aria-hidden="true" tabindex="-1">
          <source data-src="assets/video/loc-west-chicago.mp4" type="video/mp4">
        </video>
        <figcaption class="micro ab-shot__cap">
          <span>27W110 North Avenue, West Chicago</span>
          <span>The first showroom, open since 2003</span>
        </figcaption>
      </figure>
    </div>
  </section>

  <!-- ============================================================
       3 — THEIR WORDS
       ============================================================
       Four paragraphs from chicagomotorcars.com/about-…, verbatim, read
       2026-08-28. Nothing rewritten, tightened or corrected — this is the
       business's own description of itself, and editing it here would put
       words in their mouth that they would then find on a preview.

       The HEADINGS are ours and are the only addition. Their page runs
       the four as one unbroken column; a heading per paragraph makes it
       scannable without touching a word of the copy.
       ============================================================ -->
  <section class="ab-story" data-reveal>
    <div class="shell">
      <p class="micro ab-eyebrow">In their own words</p>
      <h2 class="ab-h"><span class="ttl-line">Why we do this.</span></h2>
      <div class="ab-story__grid">
__STORY__
      </div>
    </div>
  </section>

  <!-- ============================================================
       4 — WHERE
       ============================================================
       A ruled list, NOT the homepage's panel accordion. That component is
       a piece of theatre and the visitor has just watched it perform;
       running it a second time turns a moment into a widget. Addresses on
       an About page are reference material and are set as reference.

       EVERY CONTROL IN THESE ROWS ALREADY EXISTS: .about__tel is the
       quiet phone link from "That's who we are", .loc__map the outlined
       directions pill from the locations panel, .loc__soc its social
       mark. Nothing new was drawn. .loc__acts is deliberately NOT reused
       — it carries the accordion's collapse and would arrive with zero
       height.

       THE PHONE IS NOT .loc__tel, AND THE FIRST RENDER IS WHY. That
       class is the red call pill, and the accordion only ever shows one
       panel's actions, so the homepage carries one red plane. Five rows
       show five at once: a column of #CB141D down the page, spent on the
       least important content on it. Same component, different container,
       different artefact. .about__tel keeps the number tappable and puts
       the red back on hover, where this project rations it.

       Marks for a showroom with its OWN account are .is-own; the rest
       fall back to the house account and say so in the aria-label. Only
       Rock Hill and Tonganoxie have their own, verified directly. Two
       marks per row rather than the panel's four: a panel has the width
       for a full set, a reference row does not, and a third mark that is
       the house account five times over is decoration.
       ============================================================ -->
  <section class="ab-rooms" data-reveal>
    <div class="shell">
      <p class="micro ab-eyebrow">Four showrooms, one opening</p>
      <h2 class="ab-h"><span class="ttl-line">Come and see them.</span></h2>
      <ul class="ab-rooms__list">
__ROOMS__
      </ul>
    </div>
  </section>

  <!-- ============================================================
       5 — THE WAY OUT
       ============================================================
       Centred, and the only centred mass on the page, which is what makes
       it read as an ending rather than as a fifth section. The pair is
       the site's standard ranking: the bone fill goes to the inventory,
       the outline to the phone.
       ============================================================ -->
  <section class="ab-cta" data-reveal>
    <div class="shell">
      <h2 class="ab-cta__h"><span class="ttl-line">Our inventory changes daily.</span></h2>
      <p class="lede">Three hundred cars on the floor right now, and the one you are after
        may not be there next week.</p>
      <div class="ab-cta__acts">
        <a class="btn btn--fill" href="srp.html">See the inventory __ARROW__</a>
        <a class="btn btn--line" href="tel:+16302211800">630-221-1800 __ARROW__</a>
      </div>
    </div>
  </section>

</main>
"""

BODY = (BODY.replace("__STORY__", "\n".join(story))
            .replace("__ROOMS__", "\n".join(rooms))
            .replace("__ARROW__", ARROW))


BANNER = """<!DOCTYPE html>
<!-- ============================================================
     our-dealership.html — AN INNER PAGE, BUILT FROM THE APPROVED SYSTEM
     ============================================================
     GENERATED. Edit tools-build-our-dealership.py, not this file.

     Head, masthead and footer are COPIED from index_3.html at build time
     rather than retyped, so the three pages cannot drift apart. index_3
     is the source because it is the approved variant.

     THE FILE IS NAMED FOR THE NAV ITEM, THE CLASSES ARE NOT. "Our
     Dealership" is what CMC's own menu calls this page, so that is the
     URL; the body class and the .ab- prefix stay, because renaming a
     working selector set buys nothing and costs a sweep of every rule.

     <body> carries `v2 is-about`:
       .v2       so the approved deltas and the location controls apply
       .is-about so our-dealership.css cannot reach any other page

     WHAT THIS PAGE ADDS TO THE DESIGN SYSTEM: nothing. Every control,
     every type role, every colour and the entry motion come from files
     that already existed. our-dealership.css holds four arrangements and
     their intervals, and no styling for anything you can click.

     ONE FACT TO TAKE BACK TO CMC: their own About page still describes
     "West Chicago, IL, Naperville, IL, and Rock Hill, SC" — three
     showrooms. Tonganoxie and Newport Beach are missing from it. This
     page shows the current five; the discrepancy is in their copy, not
     in this build, and it is theirs to correct.
     ============================================================ -->
<html lang="en">
"""

out = BANNER + h + '\n<body class="v2 is-about">\n\n' + header + between + BODY + \
      "\n" + footer + "\n\n" + script + "\n</body>\n</html>\n"

# Computed in full, then written. Nothing is opened for writing until the
# whole string exists.
with open(OUT, "w") as f:
    f.write(out)

print("wrote %s  (%d bytes, %d lines)" % (OUT, len(out), out.count("\n") + 1))
