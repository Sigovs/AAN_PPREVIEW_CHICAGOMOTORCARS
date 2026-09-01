#!/usr/bin/env python3
"""Assemble videos.html from index_3.html's head, masthead and footer.

Same principle as tools-build-our-dealership.py: anything shared is COPIED
at build time rather than retyped, so the pages cannot drift. index_3 is
the source because it is the approved variant.

It writes videos.html and NOTHING ELSE. The inventory builder once wrote
srp.html as well and deleted 525 lines of hand-maintained head; a script
that can only create the one file it is named after cannot repeat that.

NOTE ON THE FIRST BUILD. Python is not installed on the machine this page
was authored on, so the artefact was produced by a one-off transliteration
of this script and then verified in the browser. If a regeneration here
ever differs from the committed videos.html, THIS file is the authority
and the difference is a bug in the transliteration, not in the page.
"""
import re, os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(ROOT, "videos.html")
src  = open(os.path.join(ROOT, "index_3.html"), encoding="utf-8").read()

# The Our Videos entries still point at the homepage. They appear in BOTH
# the desktop masthead AND the collapsed mobile menu, and the mobile menu
# sits between </header> and <main> — outside the header slice. Repointing
# only the slice left a dead link on the phone, so the replacement runs
# over the whole assembled document at the end instead.
VIDEO_LABELS = [
    "Our Videos",
    "Our videos",
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
           "<title>Our Videos &#8212; Chicago Motor Cars</title>", h, flags=re.S)
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
               '\\1\n<!-- videos.html only. Last, so it wins on equal specificity. -->\n'
               '<link rel="stylesheet" href="assets/css/videos.css?v=2">', h)
if n != 1:
    raise SystemExit("ABORT: could not place videos.css after v3.css (%d matches). The head "
                     "changed shape; fix this script rather than shipping a page whose "
                     "stylesheet silently never loads." % n)


# ---- the masthead's own Our Videos links ------------------------------
nav = header


BODY = r"""<main>

  <!-- ============================================================
       1 — THE CLAIM
       ============================================================
       ab-head's construction again — eyebrow, headline in authored
       lines, one supporting sentence — because this is the third inner
       page of the same kind and three inner pages that open three
       different ways is drift, not variety.

       NO FIGURES HERE. our-dealership and team both close their head
       with a .story__stats row; "4 films" is not a figure worth setting
       at counter scale, and a stat block whose numbers are trivial
       cheapens the ones that are not.
       ============================================================ -->
  <section class="vd-head" data-reveal data-bloom="center">
    <div class="shell">
      <p class="micro vd-eyebrow">Our videos</p>
      <h1 class="vd-title">
        <span class="ttl-line">The rooms, and</span>
        <span class="ttl-line">what is in them.</span>
      </h1>
      <p class="lede">Two films shot inside the showrooms, and the channel where the
        individual cars get their own.</p>
    </div>
  </section>


  <!-- ============================================================
       2 — THE TWO FILMS
       ============================================================
       CMC's own hosted videos, taken from their Our Videos page and
       re-encoded. Their titles are kept exactly as they set them.

       WHAT WAS WRONG WITH THE ORIGINALS, AND WHY THIS IS NOT MERELY A
       RESTYLE. Their page serves the Naperville film as 78 MB of HEVC
       in a .mov container — a codec and wrapper combination Chrome and
       Firefox will not play at all, so on their live site most visitors
       get a black rectangle. The Vault film is a 52 MB 3840x2160
       master. 130 MB on one page, and half of it undecodable. Both are
       re-encoded to H.264 720p with faststart: 29 MB together, and both
       actually play. See assets/video/VIDEOS.txt.

       preload="none" AND A REAL POSTER FRAME. Nothing is fetched until
       someone presses play, and the poster is a frame of the film
       itself — the practice assets/video/README.txt already sets for
       the break band, for the same reason: if the video never arrives,
       what is left is still the same room.
       ============================================================ -->
  <section class="vd-films" data-reveal aria-labelledby="vd-films-t">
    <div class="shell">

      <div class="vd-films__head">
        <p class="micro vd-eyebrow">Filmed on the floor</p>
        <h2 class="vd-h2" id="vd-films-t">
          <span class="ttl-line">Two walks through</span>
          <span class="ttl-line">the collection.</span>
        </h2>
      </div>

      <article class="vd-film">
        <div class="vd-film__meta">
          <h3 class="vd-film__t">Chicago Motor Cars Vault</h3>
          <p class="vd-film__d">Down the stairs into the basement collection: Ford GTs in
            Gulf livery and in black with silver stripes, a row of red Mustang Cobra R, and
            the Shelby Cobra mural running the length of the wall behind them.</p>
          <p class="micro vd-film__spec">1:27 <span class="vd-dot" aria-hidden="true">&middot;</span> West Chicago <span class="vd-dot" aria-hidden="true">&middot;</span> Sound on</p>
        </div>
        <div class="vd-film__stage">
          <video class="vd-video" controls preload="none" playsinline
                 poster="assets/img/videos/vid-cmc-vault-poster-1280.jpg"
                 width="1280" height="720"
                 aria-label="Chicago Motor Cars Vault — a walk through the basement collection">
            <source src="assets/video/vid-cmc-vault.mp4" type="video/mp4">
            <p class="vd-fallback">Your browser cannot play this film.
              <a class="vd-link" href="assets/video/vid-cmc-vault.mp4">Download it instead</a>.</p>
          </video>
        </div>
      </article>

      <article class="vd-film">
        <div class="vd-film__meta">
          <h3 class="vd-film__t">Chicago Motor Cars Naperville</h3>
          <p class="vd-film__d">The Naperville store from the inside — a white 911 GT3 on the
            floor, the glass frontage with the cars parked out under it, and the client lounge
            at the back.</p>
          <p class="micro vd-film__spec">1:17 <span class="vd-dot" aria-hidden="true">&middot;</span> Naperville <span class="vd-dot" aria-hidden="true">&middot;</span> Sound on</p>
        </div>
        <div class="vd-film__stage">
          <video class="vd-video" controls preload="none" playsinline
                 poster="assets/img/videos/vid-naperville-karma-poster-1280.jpg"
                 width="1280" height="720"
                 aria-label="Chicago Motor Cars Naperville — a walk through the showroom">
            <source src="assets/video/vid-naperville-karma.mp4" type="video/mp4">
            <p class="vd-fallback">Your browser cannot play this film.
              <a class="vd-link" href="assets/video/vid-naperville-karma.mp4">Download it instead</a>.</p>
          </video>
        </div>
      </article>

    </div>
  </section>


  <!-- ============================================================
       3 — THE CHANNEL
       ============================================================
       Two videos from CMC's own YouTube channel, embedded on their Our
       Videos page without titles. The titles here are the real ones,
       read from YouTube's oEmbed endpoint — a video with no name is a
       thumbnail nobody clicks.

       A FACADE, NOT AN IFRAME. A YouTube iframe loads Google's player
       and its cookies on page load, for every visitor, whether or not
       anyone presses play — two of them is roughly a megabyte of
       third-party script spent on nothing. The poster is served from
       this site, and the iframe is created on click. That is also why
       the thumbnails were downloaded rather than hotlinked from
       i.ytimg.com: hotlinking reports the visit to Google too.

       WITH NO SCRIPT the button is a plain link to the video on
       YouTube, which is where it was going anyway.
       ============================================================ -->
  <section class="vd-channel" data-reveal aria-labelledby="vd-channel-t">
    <div class="shell">

      <div class="vd-channel__head">
        <p class="micro vd-eyebrow">On the channel</p>
        <h2 class="vd-h2" id="vd-channel-t">
          <span class="ttl-line">One car</span>
          <span class="ttl-line">at a time.</span>
        </h2>
      </div>

      <ul class="vd-grid">
        <li class="vd-item">
          <a class="vd-embed" data-yt="r4bWG_HogDs"
             href="https://www.youtube.com/watch?v=r4bWG_HogDs"
             target="_blank" rel="noopener">
            <span class="vd-embed__frame">
              <img src="assets/img/videos/yt-r4bWG_HogDs-1280.jpg"
                   srcset="assets/img/videos/yt-r4bWG_HogDs-640.jpg 640w,
                           assets/img/videos/yt-r4bWG_HogDs-1280.jpg 1280w"
                   sizes="(max-width: 900px) 100vw, 44vw"
                   alt="" width="1280" height="720" loading="lazy" decoding="async">
              <span class="vd-play" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor"><path d="M8 5.5v13l11-6.5L8 5.5Z"/></svg>
              </span>
            </span>
            <span class="vd-item__t">2005 Ford GT, silver with black stripes</span>
            <span class="micro vd-item__meta">YouTube <span class="vd-dot" aria-hidden="true">&middot;</span> Four options, collector condition</span>
          </a>
        </li>
        <li class="vd-item">
          <a class="vd-embed" data-yt="21Ae3DDGfU8"
             href="https://www.youtube.com/watch?v=21Ae3DDGfU8"
             target="_blank" rel="noopener">
            <span class="vd-embed__frame">
              <img src="assets/img/videos/yt-21Ae3DDGfU8-1280.jpg"
                   srcset="assets/img/videos/yt-21Ae3DDGfU8-640.jpg 640w,
                           assets/img/videos/yt-21Ae3DDGfU8-1280.jpg 1280w"
                   sizes="(max-width: 900px) 100vw, 44vw"
                   alt="" width="1280" height="720" loading="lazy" decoding="async">
              <span class="vd-play" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor"><path d="M8 5.5v13l11-6.5L8 5.5Z"/></svg>
              </span>
            </span>
            <span class="vd-item__t">Alpha 16 GT-R takes first place</span>
            <span class="micro vd-item__meta">YouTube <span class="vd-dot" aria-hidden="true">&middot;</span> Texas Invitational Quick 16</span>
          </a>
        </li>
      </ul>

      <div class="vd-acts">
        <a class="fn-jump vd-jump" href="https://www.youtube.com/user/ChicagoMotorCars" target="_blank" rel="noopener">
          <span>Everything on the channel</span>
          <svg class="fn-jump__arrow" viewBox="0 0 16 16" width="15" height="15" fill="none" aria-hidden="true"><path d="M3 8h10M8.5 3.5 13 8l-4.5 4.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
      </div>

    </div>
  </section>


  <!-- ============================================================
       4 — THE WAY OUT
       ============================================================
       The existing pair, unchanged: the filled pill and the quiet arrow.
       ============================================================ -->
  <section class="vd-cta" data-reveal aria-labelledby="vd-cta-t">
    <div class="shell">
      <h2 class="vd-h2" id="vd-cta-t">
        <span class="ttl-line">The cars in these</span>
        <span class="ttl-line">films are for sale.</span>
      </h2>
      <p class="lede">Inventory changes daily, and what is on the floor is what is on the
        site.</p>
      <div class="vd-acts vd-acts--end">
        <a class="btn btn--fill" href="srp.html">Browse the inventory</a>
        <a class="fn-jump vd-jump" href="locations.html">
          <span>See the showrooms</span>
          <svg class="fn-jump__arrow" viewBox="0 0 16 16" width="15" height="15" fill="none" aria-hidden="true"><path d="M3 8h10M8.5 3.5 13 8l-4.5 4.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
      </div>
    </div>
  </section>

</main>"""


HEADER_COMMENT = """<!DOCTYPE html>
<html lang="en">
<!-- ============================================================
     videos.html &#8212; GENERATED. Do not hand-edit.

     Head, masthead and footer are COPIED from index_3.html at build
     time by tools-build-videos.py. index_3 is the source because it
     is the approved variant; a hand-copied nav is a nav that drifts.

     <body> carries `v2 is-vid`: v2 because every page on this site runs
     the v2 layer, is-vid because assets/css/videos.css is scoped
     entirely to it and may not reach another page.
     ============================================================ -->
"""

out = (HEADER_COMMENT
       + h + '\n<body class="v2 is-vid">\n'
       + nav + "\n" + (between if between.strip() else "\n") + "\n"
       + BODY + "\n" + footer + "\n" + script + "\n"
       + '<script src="assets/js/videos.js?v=1" defer></script>\n'
       + "</body>\n</html>\n")

for label in VIDEO_LABELS:
    out = out.replace('href="index_3.html">' + label,
                      'href="videos.html">' + label)

open(OUT, "w", encoding="utf-8").write(out)
print("written", OUT, len(out), "bytes")
