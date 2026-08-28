#!/usr/bin/env python3
"""Assemble locations.html from index_3.html's head, masthead and footer.

Same principle as the other two builders: anything shared is COPIED at
build time rather than retyped, so the pages cannot drift. index_3 is the
source because it is the approved variant.

It writes locations.html and NOTHING ELSE. The inventory builder once
wrote srp.html as well and deleted 525 lines of hand-maintained head; a
script that can only create the file it is named after cannot repeat it.
"""
import re, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(ROOT, "locations.html")
src  = open(os.path.join(ROOT, "index_3.html")).read()


def cut(start, end):
    """Slice src between two literals, refusing to guess. Every slice is
    computed and checked before the output file is opened — the whole
    string exists before anything is written."""
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
           "<title>Locations — Chicago Motor Cars</title>", h, flags=re.S)
h = re.sub(r'<meta name="description" content=".*?">',
           '<meta name="description" content="Chicago Motor Cars showrooms in West Chicago '
           'and Naperville, Illinois; Rock Hill, South Carolina; Tonganoxie, Kansas. Newport '
           'Beach, California, opening soon.">', h, flags=re.S)

# The first block's poster is what paints; the films are fetched by
# script only as each block comes near, and never under reduced motion.
h, n = re.subn(r'<link rel="preload" as="image"[^>]*>',
               '<link rel="preload" as="image" '
               'href="assets/img/locations/loc-west-chicago-1200.jpg" fetchpriority="high">', h)
if n != 1:
    raise SystemExit("ABORT: expected exactly one image preload in the head, found %d" % n)

h, n = re.subn(r'(<link rel="stylesheet" href="assets/css/v3\.css\?v=\d+">)',
               r'\1\n<!-- locations.html only. Last, so it wins on equal specificity. -->\n'
               r'<link rel="stylesheet" href="assets/css/locations.css?v=2">', h)
if n != 1:
    raise SystemExit("ABORT: could not place locations.css after v3.css (%d matches). The "
                     "head changed shape; fix this script rather than shipping a page whose "
                     "stylesheet silently never loads." % n)


# ---- the five showrooms ----------------------------------------------
# Addresses, numbers, films, posters and handles are the locations
# panel's, lifted rather than retyped so the two cannot disagree.
#
# `own` marks an account belonging to THAT showroom. Only Rock Hill and
# Tonganoxie have their own, verified directly against Instagram and
# Facebook; the rest fall back to the house account and say so in the
# aria-label, which is why nothing here is a dead link.
#
# `synthetic` is on exactly one entry and it changes what gets rendered.
SHOWROOMS = [
 dict(id="west-chicago", city="West Chicago", state="Illinois",
      addr="27W110 North Avenue, West Chicago, IL 60185",
      tel="630-221-1800", tel_href="+16302211800",
      dest="27W110+North+Avenue%2C+West+Chicago%2C+IL+60185",
      film="assets/video/loc-west-chicago.mp4",
      poster="assets/img/locations/loc-west-chicago-1200.jpg",
      alt="The West Chicago showroom at dusk, seen from the air: a lit glass building on "
          "North Avenue with its lot behind it.",
      ig="https://www.instagram.com/chicagomotorcars/", ig_own=False,
      fb="https://www.facebook.com/chicagomotorcars", fb_own=False,
      yt="https://www.youtube.com/user/ChicagoMotorCars", yt_own=False),
 dict(id="naperville", city="Naperville", state="Illinois",
      addr="2104 Ferry Road, Naperville, IL 60563",
      tel="630-221-1800", tel_href="+16302211800",
      dest="2104+Ferry+Road%2C+Naperville%2C+IL+60563",
      film="assets/video/loc-naperville.mp4",
      poster="assets/img/locations/loc-naperville-1200.jpg",
      alt="The Naperville showroom on Ferry Road, seen from the air.",
      ig="https://www.instagram.com/chicagomotorcars/", ig_own=False,
      fb="https://www.facebook.com/chicagomotorcars", fb_own=False,
      yt="https://www.youtube.com/user/ChicagoMotorCars", yt_own=False),
 dict(id="rock-hill", city="Rock Hill", state="South Carolina",
      addr="727 Marine Drive, Rock Hill, SC 29730",
      tel="803-891-7788", tel_href="+18038917788",
      dest="727+Marine+Drive%2C+Rock+Hill%2C+SC+29730",
      film="assets/video/loc-rock-hill.mp4",
      poster="assets/img/locations/loc-rock-hill-1200.jpg",
      alt="The Rock Hill showroom on Marine Drive, seen from the air.",
      ig="https://www.instagram.com/chicagomotorcarssc/", ig_own=True,
      fb="https://www.facebook.com/chicagomotorcarssc", fb_own=True,
      yt="https://www.youtube.com/@chicagomotorcarssc", yt_own=True),
 dict(id="tonganoxie", city="Tonganoxie", state="Kansas",
      addr="1650 Commerce Ave, Tonganoxie, KS 66086",
      tel="913-845-9633", tel_href="+19138459633",
      dest="1650+Commerce+Ave%2C+Tonganoxie%2C+KS+66086",
      film="assets/video/loc-tonganoxie.mp4",
      poster="assets/img/locations/loc-tonganoxie-1200.jpg",
      alt="The Tonganoxie showroom on Commerce Avenue, seen from the air.",
      ig="https://www.instagram.com/chicagomotorcarskc/", ig_own=True,
      fb="https://www.facebook.com/chicagomotorcarskc", fb_own=True,
      yt="https://www.youtube.com/user/ChicagoMotorCars", yt_own=False),
 dict(id="newport-beach", city="Newport Beach", state="California — opening soon",
      addr="The fifth floor. Call the West Chicago desk for an opening date.",
      tel="630-221-1800", tel_href="+16302211800",
      dest=None, query="Newport+Beach%2C+CA", soon=True, synthetic=True,
      film="assets/video/gen-loc-newport-beach.mp4",
      poster="assets/img/locations/gen-loc-newport-beach-1200.jpg",
      alt="A rendering of the planned Newport Beach showroom: a curved glass facade lit "
          "from a cove, with a car standing at the entrance.",
      ig="https://www.instagram.com/chicagomotorcars/", ig_own=False,
      fb="https://www.facebook.com/chicagomotorcars", fb_own=False,
      yt="https://www.youtube.com/user/ChicagoMotorCars", yt_own=False),
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
YT_SVG = ('<svg viewBox="0 0 20 20" aria-hidden="true">'
          '<rect x="1.6" y="4.4" width="16.8" height="11.2" rx="3.4" fill="none" '
          'stroke="currentColor" stroke-width="1.5"/>'
          '<path d="M8.4 7.6 13 10l-4.6 2.4V7.6Z" fill="currentColor"/></svg>')
TEL_SVG = ('<span class="about__ico"><svg width="15" height="15" viewBox="0 0 15 15" '
           'aria-hidden="true"><path d="M4.2 1.6 5.9 4 4.6 5.7c.7 1.7 2 3 3.7 3.7L10 8.1l2.4 '
           '1.7c.4.3.5.8.2 1.2l-1 1.3c-.3.4-.8.5-1.2.4C5.9 11.6 2.4 8.1 1.3 3.6c-.1-.4 0-.9.4'
           '-1.2l1.3-1c.4-.3.9-.2 1.2.2Z" fill="currentColor"/></svg></span>')
ARROW = ('<svg class="btn__arrow" width="13" height="13" viewBox="0 0 13 13" fill="none" '
         'aria-hidden="true"><path d="M2 6.5h9M7.4 3 11 6.5 7.4 10" stroke="currentColor" '
         'stroke-width="1.3"/></svg>')


def soc(url, own, label, svg):
    """One social mark. data-shared records that the link goes to the
    house account rather than this showroom's own — the locations panel's
    convention, and the reason nothing here points nowhere."""
    return ('<a class="%s" href="%s" target="_blank" rel="noopener" aria-label="%s"%s>%s</a>'
            % ("loc__soc is-own" if own else "loc__soc", url,
               html.escape(label, quote=True), "" if own else ' data-shared="true"', svg))


jump = "\n".join(
    '        <a class="btn btn--line" href="#%s">%s</a>' % (s["id"], html.escape(s["city"]))
    for s in SHOWROOMS)

rooms = []
for s in SHOWROOMS:
    if s.get("dest"):
        map_href = "https://www.google.com/maps/dir/?api=1&amp;destination=" + s["dest"]
        map_txt  = "Get directions"
    else:
        map_href = "https://www.google.com/maps/search/?api=1&amp;query=" + s["query"]
        map_txt  = "See on map"

    # ONE WORD, ON ONE FRAME. See the GI note in the section comment.
    plate = ('\n          <span class="micro lo-room__plate">Rendering</span>'
             if s.get("synthetic") else "")

    rooms.append("""      <article class="lo-room" id="%s" data-reveal data-film="25%%">
        <figure class="lo-room__film">
          <video class="lo-room__video"
                 poster="%s"
                 muted loop playsinline
                 preload="none"
                 width="1280" height="720"
                 aria-label="%s" tabindex="-1">
            <source data-src="%s" type="video/mp4">
          </video>%s
        </figure>
        <div class="lo-room__body">
          <h2 class="lo-room__city"><span class="ttl-line">%s</span><span class="micro lo-room__state">%s</span></h2>
          <p class="lo-room__addr">%s</p>
          <div class="lo-room__acts">
            <a class="about__tel" href="tel:%s">%s<span>%s</span></a>
            <a class="loc__map" href="%s" rel="noopener">%s</a>
            <span class="loc__social">%s%s%s</span>
          </div>
        </div>
      </article>""" % (
        s["id"], s["poster"], html.escape(s["alt"], quote=True), s["film"], plate,
        html.escape(s["city"]), html.escape(s["state"]), html.escape(s["addr"]),
        s["tel_href"], TEL_SVG, s["tel"], map_href, map_txt,
        soc(s["ig"], s["ig_own"], "%s on Instagram" % s["city"], IG_SVG),
        soc(s["fb"], s["fb_own"], "%s on Facebook" % s["city"], FB_SVG),
        soc(s["yt"], s["yt_own"], "%s on YouTube" % s["city"], YT_SVG)))


BODY = """
<main>

  <!-- ============================================================
       1 — THE HEAD, AND THE WAY PAST IT
       ============================================================
       srp.html's opening height, so the three inner pages start on one
       line under the fixed masthead. The bloom is the reviews chapter's
       own, the same rule at the same strength.

       The jump row is five outline pills, unmodified — a row of anchors
       is not a new control. It earns its place on length: five blocks is
       about 3,000px, and somebody who came for the Rock Hill number
       should not scroll through Illinois and Kansas to reach it. The
       masthead's Locations menu does not do this job; it points at
       inventory filtered by city, which is a different question.
       ============================================================ -->
  <section class="lo-head" data-reveal data-bloom="center">
    <div class="shell">
      <p class="micro ab-eyebrow">Locations</p>
      <h1 class="lo-title">
        <span class="ttl-line">Four floors open,</span>
        <span class="ttl-line">and a fifth coming.</span>
      </h1>
      <p class="lede">Illinois, South Carolina and Kansas, with Newport Beach, California,
        opening soon. Every car in the inventory can be seen at the floor it is standing on.</p>
      <nav class="lo-jump" aria-label="Jump to a showroom">
__JUMP__
      </nav>
    </div>
  </section>

  <!-- ============================================================
       2 — THE FIVE
       ============================================================
       Film and facts side by side, alternating which side the film is
       on. NOT the homepage's hover accordion: that component shows one
       showroom at a time and hides four addresses behind a pointer,
       which is the wrong instrument for a page whose whole job is
       choosing between them. Alternating is this site's own fix for
       repetition — index_3's sell band flips for exactly this reason.

       THE FILMS ARE REAL AND THE PROVENANCE IS SETTLED FOR FOUR OF
       THEM. Alex supplied the aerials on 2026-08-17, each named by the
       address it was shot at, and every open showroom shows its own
       building. That was the section's oldest content risk and it is
       closed.

       THE FIFTH IS A RENDERING AND NOW SAYS SO. Newport Beach has not
       opened, so no photograph of its showroom can exist; the frame is
       synthetic and carries the gen- prefix. Four verified aerials and
       one render presented identically is precisely what GI3 forbids —
       the synthetic one inherits the credibility of the four beside it,
       and nobody has a reason to treat one block in a uniform sequence
       differently. Its own sidecar prescribes the fix in one word, in
       the caption's existing register, on that frame only, and this is
       it. The caption already said the LOCATION is opening soon; that is
       a claim about the business, not about the picture.

       WHAT IS MISSING AND IS NOT INVENTED: opening hours. They are
       nowhere in this repository and CMC has not supplied them. A
       plausible set of hours on a page a customer drives to is the kind
       of invention that gets someone standing in a car park, so there
       are none until CMC sends them.
       ============================================================ -->
  <section class="lo-rooms">
    <div class="shell">
__ROOMS__
    </div>
  </section>

  <!-- ============================================================
       3 — THE WAY OUT
       ============================================================
       Centred, the only centred mass on the page, which is what marks it
       as an ending rather than a sixth block.
       ============================================================ -->
  <section class="lo-cta" data-reveal>
    <div class="shell">
      <h2 class="lo-cta__h"><span class="ttl-line">Come and stand next to one.</span></h2>
      <p class="lede">Three hundred cars across four floors, and the inventory changes daily.</p>
      <div class="lo-cta__acts">
        <a class="btn btn--fill" href="srp.html">See the inventory __ARROW__</a>
        <a class="btn btn--line" href="tel:+16302211800">630-221-1800 __ARROW__</a>
      </div>
    </div>
  </section>

</main>
"""

BODY = (BODY.replace("__JUMP__", jump)
            .replace("__ROOMS__", "\n".join(rooms))
            .replace("__ARROW__", ARROW))


BANNER = """<!DOCTYPE html>
<!-- ============================================================
     locations.html — THE SHOWROOM PAGE
     ============================================================
     GENERATED. Edit tools-build-locations.py, not this file.

     Head, masthead and footer are COPIED from index_3.html at build time
     rather than retyped, so the pages cannot drift apart. index_3 is the
     source because it is the approved variant.

     <body> carries `v2 is-locs`:
       .v2      so the approved deltas and the location controls apply
       .is-locs so locations.css cannot reach any other page

     WHAT THIS PAGE ADDS TO THE DESIGN SYSTEM: nothing you can click.
     The films use [data-film], the phone is .about__tel, directions are
     .loc__map, the marks are .loc__soc, the jump row and the close are
     .btn. locations.css holds four arrangements and one plate.

     TWO THINGS TO TAKE BACK TO CMC:
       1. OPENING HOURS. Not in this repository and not invented. This
          page has none until they send them, and it is the one fact a
          locations page owes that this one cannot yet pay.
       2. THE NEWPORT BEACH FRAME is a rendering and is now labelled as
          one. It was raised on 2026-08-17 and left undone; a page that
          gives it a block of its own could not leave it undone again.
          Replace it the day there is a building to film.
     ============================================================ -->
<html lang="en">
"""

out = BANNER + h + '\n<body class="v2 is-locs">\n\n' + header + between + BODY + \
      "\n" + footer + "\n\n" + script + "\n</body>\n</html>\n"

# Computed in full, then written. Nothing is opened for writing until the
# whole string exists.
with open(OUT, "w") as f:
    f.write(out)

print("wrote %s  (%d bytes, %d lines)" % (OUT, len(out), out.count("\n") + 1))
