#!/usr/bin/env python3
"""Assemble team.html from index_3.html's head, masthead and footer.

Same principle as tools-build-our-dealership.py: anything shared is COPIED
at build time rather than retyped, so the pages cannot drift. index_3 is
the source because it is the approved variant.

It writes team.html and NOTHING ELSE. The inventory builder once wrote
srp.html as well and deleted 525 lines of hand-maintained head; a script
that can only create the one file it is named after cannot repeat that.

NOTE ON THE FIRST BUILD. Python is not installed on the machine this page
was authored on, so the artefact was produced by a one-off transliteration
of this script and then verified in the browser. If a regeneration here
ever differs from the committed team.html, THIS file is the authority
and the difference is a bug in the transliteration, not in the page.
"""
import re, os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(ROOT, "team.html")
src  = open(os.path.join(ROOT, "index_3.html"), encoding="utf-8").read()

# The Our Team entries in the copied masthead still point at the homepage.
# They are repointed HERE rather than in index_3, because this script must
# never write a file it is not named after.
TEAM_LABELS = [
    "Our Team",
    "Our team",
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
           "<title>Our Team &#8212; Chicago Motor Cars</title>", h, flags=re.S)
h = re.sub(r'<meta name="description" content=".*?">',
           '<meta name="description" content="The nineteen people behind Chicago Motor Cars, '
           'across showrooms in West Chicago, Naperville, Rock Hill and Tonganoxie.">', h, flags=re.S)

# NOTHING IS PRELOADED HERE, AND THE ABSENCE IS THE DECISION. This page
# opens on type, not on a photograph: the first portrait is a lazily loaded
# 380px plate well below the fold. Carrying the homepage's hero preload
# across would fetch a large image nobody sees before the LCP, which is the
# wasted-preload defect financing.html was caught on.
h, n = re.subn(r'\s*<link rel="preload" as="image"[^>]*>', '', h)
if n != 1:
    raise SystemExit("ABORT: expected exactly one image preload to remove, found %d" % n)

h, n = re.subn(r'(<link rel="stylesheet" href="assets/css/v3\.css\?v=\d+">)',
               '\\1\n<!-- team.html only. Last, so it wins on equal specificity. -->\n'
               '<link rel="stylesheet" href="assets/css/team.css?v=4">', h)
if n != 1:
    raise SystemExit("ABORT: could not place team.css after v3.css (%d matches). The head "
                     "changed shape; fix this script rather than shipping a page whose "
                     "stylesheet silently never loads." % n)


# ---- the masthead's own Our Team links --------------------------------
nav = header
for label in TEAM_LABELS:
    nav = nav.replace('href="index_3.html">' + label,
                      'href="team.html">' + label)


BODY = r"""<main>

  <!-- ============================================================
       1 — THE CLAIM
       ============================================================
       ab-head's construction, unchanged: eyebrow, headline in authored
       lines, one supporting sentence, then the figures. The paragraph
       is CMC's own, from their team page, read 2026-08-30 — the same
       practice our-dealership.html follows for the About copy. Not one
       word is edited, including the eBay accolade they choose to lead
       with.
       ============================================================ -->
  <section class="tm-head" data-reveal data-bloom="center">
    <div class="shell">
      <p class="micro tm-eyebrow">Our team</p>
      <h1 class="tm-title">
        <span class="ttl-line">Great cars are</span>
        <span class="ttl-line">the easy part.</span>
      </h1>
      <p class="lede">Nineteen specialists across four showrooms &mdash; and the reason
        the same buyers keep coming back is the people, not the inventory.</p>

      <dl class="story__stats">
        <div class="stat stat--lead">
          <dt class="micro stat__label">Specialists</dt>
          <dd class="stat__fig"><span class="stat__n" data-count-to="19">19</span></dd>
        </div>
        <div class="stat stat--proof">
          <dt class="micro stat__label">Showrooms</dt>
          <dd class="stat__fig"><span class="stat__n">4</span></dd>
        </div>
        <div class="stat stat--proof">
          <dt class="micro stat__label">Since</dt>
          <dd class="stat__fig"><span class="stat__n">2003</span></dd>
        </div>
      </dl>
    </div>
  </section>


  <!-- ============================================================
       2 — THEIR OWN WORDS ABOUT WHY THE PEOPLE MATTER
       ============================================================
       Verbatim from chicagomotorcars.com/team-chicago-motor-cars-in-chicago-il,
       read 2026-08-30. One paragraph, set as a lede-scale statement
       rather than body copy, because it is the page's argument and not
       its detail.
       ============================================================ -->
  <section class="tm-say" data-reveal>
    <div class="shell tm-say__inner">
      <blockquote class="tm-say__q">
        <p>We have been named the &ldquo;best dealership of Ebay&rdquo; and that accolade is not
          because of the cars we provide, it&rsquo;s because of the way we provide them. We do
          everything in our power to be accommodating to our customers. We will pick you up
          from the airport, help you ship your car, and even provide the warranties and
          service plans that you need.</p>
      </blockquote>
      <p class="micro tm-say__cite">Chicago Motor Cars, in their own words</p>
    </div>
  </section>


  <!-- ============================================================
       3 — THE ROSTER
       ============================================================
       Grouped by showroom, because that is the question a buyer
       actually has: who will I be dealing with, at the store I am
       going to. Not ranked by seniority — ranking nineteen colleagues
       in public is a decision for CMC, not for a redesign.

       ONE UNIFORM CARD, AND NO BIOGRAPHY IN IT. Eight of the nineteen
       have long personal bios and eleven have none. Putting them in
       these cells would make a grid whose rows are as tall as their
       longest member and whose gaps are the rest — so the bios get
       their own chapter below and this grid stays a clean answer to
       "who works here".

       THE PORTRAITS ARE MONOCHROME, AND THAT IS THE WHOLE ART
       DIRECTION OF THIS PAGE. CMC's thirteen photographs come from at
       least three shoots: a lit showroom series with the purple and
       blue Lamborghinis behind, a white studio series, and phone
       frames under office fluorescents. In colour they do not belong to
       one page — the purple car dominates every frame it is in. Desatured
       and lifted slightly in contrast they become one set. Nothing is
       retouched and no frame is faked; only the colour is taken off,
       and it is taken off in CSS so the originals stay as CMC shot them.
       ============================================================ -->
  <section class="tm-roster" data-reveal aria-labelledby="tm-roster-t">
    <div class="shell">
      <div class="tm-roster__head">
        <p class="micro tm-eyebrow">Who you will be dealing with</p>
        <h2 class="tm-h2" id="tm-roster-t">
          <span class="ttl-line">Four showrooms.</span>
          <span class="ttl-line">One phone call each.</span>
        </h2>
      </div>

      <div class="tm-group">
        <div class="tm-group__head">
          <h3 class="tm-group__t">West Chicago</h3>
          <p class="micro tm-group__meta">West Chicago, IL <span class="tm-group__dot" aria-hidden="true">&middot;</span> <a class="tm-link" href="tel:+16302211800">630-221-1800</a> <span class="tm-group__dot" aria-hidden="true">&middot;</span> 12 specialists</p>
        </div>
        <ul class="tm-cards">
          <li class="tm-card">
            <span class="tm-plate">
            <img src="assets/img/team/adam-wrobel-380.jpg"
                 srcset="assets/img/team/adam-wrobel-380.jpg 380w,
                         assets/img/team/adam-wrobel-760.jpg 760w"
                 sizes="(max-width: 640px) 42vw, 15vw"
                 alt="Adam Wrobel" width="380" height="475"
                 loading="lazy" decoding="async">
          </span>
            <p class="tm-card__name">Adam Wrobel</p>
            <p class="micro tm-card__role">Inventory Manager</p>
            
          </li>
          <li class="tm-card">
            <span class="tm-plate tm-plate--type" aria-hidden="true"><span class="tm-plate__mono">PS</span></span>
            <p class="tm-card__name">Parin Shah</p>
            
            <p class="tm-contact"><a class="tm-link" href="tel:+16302211800">630-221-1800</a><a class="tm-link" href="mailto:parin@chicagomotorcars.com" aria-label="Email Parin Shah">Email</a></p>
          </li>
          <li class="tm-card">
            <span class="tm-plate">
            <img src="assets/img/team/sam-salameh-380.jpg"
                 srcset="assets/img/team/sam-salameh-380.jpg 380w,
                         assets/img/team/sam-salameh-760.jpg 760w"
                 sizes="(max-width: 640px) 42vw, 15vw"
                 alt="Sam Salameh" width="380" height="475"
                 loading="lazy" decoding="async">
          </span>
            <p class="tm-card__name">Sam Salameh</p>
            <p class="micro tm-card__role">Business Manager</p>
            <p class="tm-contact"><a class="tm-link" href="tel:+16302211800">630-221-1800</a><a class="tm-link" href="mailto:sam@chicagomotorcars.com" aria-label="Email Sam Salameh">Email</a></p>
          </li>
          <li class="tm-card">
            <span class="tm-plate tm-plate--type" aria-hidden="true"><span class="tm-plate__mono">TP</span></span>
            <p class="tm-card__name">Travis Papenberg</p>
            
            <p class="tm-contact"><a class="tm-link" href="mailto:travis@chicagomotorcars.com" aria-label="Email Travis Papenberg">Email</a></p>
          </li>
          <li class="tm-card">
            <span class="tm-plate tm-plate--type" aria-hidden="true"><span class="tm-plate__mono">AM</span></span>
            <p class="tm-card__name">Ali Mafee</p>
            
            <p class="tm-contact"><a class="tm-link" href="tel:+13129271159">312-927-1159</a></p>
          </li>
          <li class="tm-card">
            <span class="tm-plate tm-plate--type" aria-hidden="true"><span class="tm-plate__mono">FS</span></span>
            <p class="tm-card__name">Frank Sacco</p>
            
            <p class="tm-contact"><a class="tm-link" href="tel:+16302211800">630-221-1800</a></p>
          </li>
          <li class="tm-card">
            <span class="tm-plate">
            <img src="assets/img/team/chris-johnson-380.jpg"
                 srcset="assets/img/team/chris-johnson-380.jpg 380w,
                         assets/img/team/chris-johnson-760.jpg 760w"
                 sizes="(max-width: 640px) 42vw, 15vw"
                 alt="Chris Johnson" width="380" height="475"
                 loading="lazy" decoding="async">
          </span>
            <p class="tm-card__name">Chris Johnson</p>
            <p class="micro tm-card__role">Semi Truck Manager</p>
            <p class="tm-contact"><a class="tm-link" href="tel:+16308578577">630-857-8577 <span class="tm-cell">cell</span></a><a class="tm-link" href="mailto:chris@chicagomotorcars.com" aria-label="Email Chris Johnson">Email</a></p>
          </li>
          <li class="tm-card">
            <span class="tm-plate">
            <img src="assets/img/team/mahmood-khalid-380.jpg"
                 srcset="assets/img/team/mahmood-khalid-380.jpg 380w,
                         assets/img/team/mahmood-khalid-760.jpg 760w"
                 sizes="(max-width: 640px) 42vw, 15vw"
                 alt="Mahmood Khalid" width="380" height="475"
                 loading="lazy" decoding="async">
          </span>
            <p class="tm-card__name">Mahmood Khalid</p>
            
            <p class="tm-contact"><a class="tm-link" href="tel:+16308545876">630-854-5876 <span class="tm-cell">cell</span></a><a class="tm-link" href="mailto:mahmood@chicagomotorcars.com" aria-label="Email Mahmood Khalid">Email</a></p>
          </li>
          <li class="tm-card">
            <span class="tm-plate">
            <img src="assets/img/team/sebastian-wrobel-380.jpg"
                 srcset="assets/img/team/sebastian-wrobel-380.jpg 380w,
                         assets/img/team/sebastian-wrobel-760.jpg 760w"
                 sizes="(max-width: 640px) 42vw, 15vw"
                 alt="Sebastian Wrobel" width="380" height="475"
                 loading="lazy" decoding="async">
          </span>
            <p class="tm-card__name">Sebastian Wrobel</p>
            <p class="micro tm-card__role">General Manager</p>
            <p class="tm-contact"><a class="tm-link" href="tel:+16302908701">630-290-8701 <span class="tm-cell">cell</span></a><a class="tm-link" href="mailto:sebastian@chicagomotorcars.com" aria-label="Email Sebastian Wrobel">Email</a></p>
          </li>
          <li class="tm-card">
            <span class="tm-plate">
            <img src="assets/img/team/jackson-jolicouer-380.jpg"
                 srcset="assets/img/team/jackson-jolicouer-380.jpg 380w,
                         assets/img/team/jackson-jolicouer-760.jpg 760w"
                 sizes="(max-width: 640px) 42vw, 15vw"
                 alt="Jackson Jolicouer" width="380" height="475"
                 loading="lazy" decoding="async">
          </span>
            <p class="tm-card__name">Jackson Jolicouer</p>
            
            <p class="tm-contact"><a class="tm-link" href="tel:+16309811141">630-981-1141 <span class="tm-cell">cell</span></a><a class="tm-link" href="mailto:jackson@chicagomotorcars.com" aria-label="Email Jackson Jolicouer">Email</a></p>
          </li>
          <li class="tm-card">
            <span class="tm-plate">
            <img src="assets/img/team/charlie-kall-380.jpg"
                 srcset="assets/img/team/charlie-kall-380.jpg 380w,
                         assets/img/team/charlie-kall-760.jpg 760w"
                 sizes="(max-width: 640px) 42vw, 15vw"
                 alt="Charlie Kall" width="380" height="475"
                 loading="lazy" decoding="async">
          </span>
            <p class="tm-card__name">Charlie Kall</p>
            
            <p class="tm-contact"><a class="tm-link" href="tel:+16303107665">630-310-7665 <span class="tm-cell">cell</span></a><a class="tm-link" href="mailto:charlie@chicagomotorcars.com" aria-label="Email Charlie Kall">Email</a></p>
          </li>
          <li class="tm-card">
            <span class="tm-plate tm-plate--type" aria-hidden="true"><span class="tm-plate__mono">GB</span></span>
            <p class="tm-card__name">Gary Blanchard</p>
            
            <p class="tm-contact"><a class="tm-link" href="mailto:gary@chicagomotorcars.com" aria-label="Email Gary Blanchard">Email</a></p>
          </li>
        </ul>
      </div>

      <div class="tm-group">
        <div class="tm-group__head">
          <h3 class="tm-group__t">Naperville</h3>
          <p class="micro tm-group__meta">Naperville, IL <span class="tm-group__dot" aria-hidden="true">&middot;</span> <a class="tm-link" href="tel:+16302211800">630-221-1800</a> <span class="tm-group__dot" aria-hidden="true">&middot;</span> 2 specialists</p>
        </div>
        <ul class="tm-cards">
          <li class="tm-card">
            <span class="tm-plate">
            <img src="assets/img/team/mike-salerno-380.jpg"
                 srcset="assets/img/team/mike-salerno-380.jpg 380w,
                         assets/img/team/mike-salerno-760.jpg 760w"
                 sizes="(max-width: 640px) 42vw, 15vw"
                 alt="Mike Salerno" width="380" height="475"
                 loading="lazy" decoding="async">
          </span>
            <p class="tm-card__name">Mike Salerno</p>
            
            <p class="tm-contact"><a class="tm-link" href="tel:+16302211800">630-221-1800</a><a class="tm-link" href="mailto:mike@chicagomotorcars.com" aria-label="Email Mike Salerno">Email</a></p>
          </li>
          <li class="tm-card">
            <span class="tm-plate">
            <img src="assets/img/team/peter-kolodziejczyk-380.jpg"
                 srcset="assets/img/team/peter-kolodziejczyk-380.jpg 380w,
                         assets/img/team/peter-kolodziejczyk-760.jpg 760w"
                 sizes="(max-width: 640px) 42vw, 15vw"
                 alt="Peter Kolodziejczyk" width="380" height="475"
                 loading="lazy" decoding="async">
          </span>
            <p class="tm-card__name">Peter Kolodziejczyk</p>
            
            <p class="tm-contact"><a class="tm-link" href="tel:+16307438755">630-743-8755 <span class="tm-cell">cell</span></a><a class="tm-link" href="mailto:peter@chicagomotorcars.com" aria-label="Email Peter Kolodziejczyk">Email</a></p>
          </li>
        </ul>
      </div>

      <div class="tm-group">
        <div class="tm-group__head">
          <h3 class="tm-group__t">South Carolina</h3>
          <p class="micro tm-group__meta">Rock Hill, SC <span class="tm-group__dot" aria-hidden="true">&middot;</span> <a class="tm-link" href="tel:+18038917788">803-891-7788</a> <span class="tm-group__dot" aria-hidden="true">&middot;</span> 4 specialists</p>
        </div>
        <ul class="tm-cards">
          <li class="tm-card">
            <span class="tm-plate">
            <img src="assets/img/team/sanjin-salihovic-380.jpg"
                 srcset="assets/img/team/sanjin-salihovic-380.jpg 380w,
                         assets/img/team/sanjin-salihovic-760.jpg 760w"
                 sizes="(max-width: 640px) 42vw, 15vw"
                 alt="Sanjin Salihovic" width="380" height="475"
                 loading="lazy" decoding="async">
          </span>
            <p class="tm-card__name">Sanjin Salihovic</p>
            
            <p class="tm-contact"><a class="tm-link" href="tel:+18038917788">803-891-7788</a><a class="tm-link" href="mailto:sanjin@chicagomotorcars.com" aria-label="Email Sanjin Salihovic">Email</a></p>
          </li>
          <li class="tm-card">
            <span class="tm-plate">
            <img src="assets/img/team/sara-vasic-380.jpg"
                 srcset="assets/img/team/sara-vasic-380.jpg 380w,
                         assets/img/team/sara-vasic-760.jpg 760w"
                 sizes="(max-width: 640px) 42vw, 15vw"
                 alt="Sara Vasic" width="380" height="475"
                 loading="lazy" decoding="async">
          </span>
            <p class="tm-card__name">Sara Vasic</p>
            
            <p class="tm-contact"><a class="tm-link" href="tel:+18038917788">803-891-7788</a><a class="tm-link" href="mailto:sara@chicagomotorcars.com" aria-label="Email Sara Vasic">Email</a></p>
          </li>
          <li class="tm-card">
            <span class="tm-plate">
            <img src="assets/img/team/sekou-dantzler-380.jpg"
                 srcset="assets/img/team/sekou-dantzler-380.jpg 380w,
                         assets/img/team/sekou-dantzler-760.jpg 760w"
                 sizes="(max-width: 640px) 42vw, 15vw"
                 alt="Sekou Dantzler" width="380" height="475"
                 loading="lazy" decoding="async">
          </span>
            <p class="tm-card__name">Sekou Dantzler</p>
            
            <p class="tm-contact"><a class="tm-link" href="tel:+12399109876">239-910-9876 <span class="tm-cell">cell</span></a><a class="tm-link" href="mailto:sekou@chicagomotorcars.com" aria-label="Email Sekou Dantzler">Email</a></p>
          </li>
          <li class="tm-card">
            <span class="tm-plate">
            <img src="assets/img/team/ricky-weimer-380.jpg"
                 srcset="assets/img/team/ricky-weimer-380.jpg 380w,
                         assets/img/team/ricky-weimer-760.jpg 760w"
                 sizes="(max-width: 640px) 42vw, 15vw"
                 alt="Ricky Weimer" width="380" height="475"
                 loading="lazy" decoding="async">
          </span>
            <p class="tm-card__name">Ricky Weimer</p>
            
            <p class="tm-contact"><a class="tm-link" href="tel:+17045172951">704-517-2951 <span class="tm-cell">cell</span></a><a class="tm-link" href="mailto:Ricky@chicagomotorcars.com" aria-label="Email Ricky Weimer">Email</a></p>
          </li>
        </ul>
      </div>

      <div class="tm-group">
        <div class="tm-group__head">
          <h3 class="tm-group__t">Kansas City</h3>
          <p class="micro tm-group__meta">Tonganoxie, KS <span class="tm-group__dot" aria-hidden="true">&middot;</span> <a class="tm-link" href="tel:+19138459633">913-845-9633</a> <span class="tm-group__dot" aria-hidden="true">&middot;</span> 1 specialist</p>
        </div>
        <ul class="tm-cards">
          <li class="tm-card">
            <span class="tm-plate tm-plate--type" aria-hidden="true"><span class="tm-plate__mono">JS</span></span>
            <p class="tm-card__name">James Sealey</p>
            <p class="micro tm-card__role">General Manager</p>
            <p class="tm-contact"><a class="tm-link" href="mailto:james@chicagomotorcars.com" aria-label="Email James Sealey">Email</a></p>
          </li>
        </ul>
      </div>
    </div>
  </section>


  <!-- ============================================================
       4 — IN THEIR OWN WORDS
       ============================================================
       Eight of the team wrote real biographies for CMC's site and they
       are the best copy the business has: specific, funny, and about
       people rather than about cars. They are reproduced verbatim.

       The row alternates side, which is this page's one rhythm device,
       and the portrait runs at the larger crop here — the same face at
       two scales doing two different jobs, an index entry above and a
       profile here.
       ============================================================ -->
  <section class="tm-voices" data-reveal aria-labelledby="tm-voices-t">
    <div class="shell">
      <div class="tm-voices__head">
        <p class="micro tm-eyebrow">In their own words</p>
        <h2 class="tm-h2" id="tm-voices-t">
          <span class="ttl-line">How they got</span>
          <span class="ttl-line">into this.</span>
        </h2>
      </div>

      <article class="tm-voice">
        <div class="tm-voice__fig"><span class="tm-plate">
            <img src="assets/img/team/mahmood-khalid-760.jpg"
                 srcset="assets/img/team/mahmood-khalid-380.jpg 380w,
                         assets/img/team/mahmood-khalid-760.jpg 760w"
                 sizes="(max-width: 900px) 60vw, 30vw"
                 alt="Mahmood Khalid" width="760" height="950"
                 loading="lazy" decoding="async">
          </span></div>
        <div class="tm-voice__body">
          <p class="micro tm-voice__where">West Chicago</p>
          <h3 class="tm-voice__name">Mahmood Khalid</h3>
          
          <p class="tm-voice__text">Mahmood AKA Mood started with Chicago Motor Cars back in 2004 as our first employee. He helped establish some of the groundwork early on for the company. He left for about 10 years to pursue his own classic car dealership and then returned back in 2019. He holds a bachelor's degree in Sales/Marketing from Northern Illinois University and an MBA from University of Illinois Urbana-Champaign. Taking his practical knowledge and merging it with his passion for cars is what has made him successful in his role. When he is not busy buying or selling cars, he is busy with his three kids with sports, working out or racing his own car.</p>
          <p class="tm-contact"><a class="tm-link" href="tel:+16308545876">630-854-5876 <span class="tm-cell">cell</span></a><a class="tm-link" href="mailto:mahmood@chicagomotorcars.com">mahmood@chicagomotorcars.com</a></p>
        </div>
      </article>

      <article class="tm-voice tm-voice--flip">
        <div class="tm-voice__fig"><span class="tm-plate">
            <img src="assets/img/team/jackson-jolicouer-760.jpg"
                 srcset="assets/img/team/jackson-jolicouer-380.jpg 380w,
                         assets/img/team/jackson-jolicouer-760.jpg 760w"
                 sizes="(max-width: 900px) 60vw, 30vw"
                 alt="Jackson Jolicouer" width="760" height="950"
                 loading="lazy" decoding="async">
          </span></div>
        <div class="tm-voice__body">
          <p class="micro tm-voice__where">West Chicago</p>
          <h3 class="tm-voice__name">Jackson Jolicouer</h3>
          
          <p class="tm-voice__text">From a young age, Jackson AKA Action Jackson has always been attracted to cars and he knew without doubt he wanted to be involved with supercars someday. He entered the car business over at Aston Martin of Chicago in 2017. With hopes to learn the &quot;ins and outs&quot; of the car business and one day joining the team of Chicago Motor Cars. That long term goal was achieved in 2022 with no plans of looking back. When Jackson is not at the store or participating in car shows, you will find him most likely on the golf course. As a young child he has always been an avid golfer and spends most of his free time on the fairway (hopefully)!</p>
          <p class="tm-contact"><a class="tm-link" href="tel:+16309811141">630-981-1141 <span class="tm-cell">cell</span></a><a class="tm-link" href="mailto:jackson@chicagomotorcars.com">jackson@chicagomotorcars.com</a></p>
        </div>
      </article>

      <article class="tm-voice">
        <div class="tm-voice__fig"><span class="tm-plate">
            <img src="assets/img/team/charlie-kall-760.jpg"
                 srcset="assets/img/team/charlie-kall-380.jpg 380w,
                         assets/img/team/charlie-kall-760.jpg 760w"
                 sizes="(max-width: 900px) 60vw, 30vw"
                 alt="Charlie Kall" width="760" height="950"
                 loading="lazy" decoding="async">
          </span></div>
        <div class="tm-voice__body">
          <p class="micro tm-voice__where">West Chicago</p>
          <h3 class="tm-voice__name">Charlie Kall</h3>
          
          <p class="tm-voice__text">Cars have been the center of Charlie&rsquo;s life and interest since his father put him on his lap and let him steer the riding lawn mower at 2 years old. He has been in the car business since 2017, with the intent of joining Chicago Motor Cars since day 1, something he told the GSM of Loves Park Audi/Mercedes/Land Rover the day he interviewed. After spending 6 years there, learning the business and being trusted with numerous CMC clientele for their new car needs, he achieved that original goal August of 2023 and has not looked back. When not at the store or car events he spends majority of time with his family at home in the pool and out in the yard.</p>
          <p class="tm-contact"><a class="tm-link" href="tel:+16303107665">630-310-7665 <span class="tm-cell">cell</span></a><a class="tm-link" href="mailto:charlie@chicagomotorcars.com">charlie@chicagomotorcars.com</a></p>
        </div>
      </article>

      <article class="tm-voice tm-voice--flip">
        <div class="tm-voice__fig"><span class="tm-plate">
            <img src="assets/img/team/mike-salerno-760.jpg"
                 srcset="assets/img/team/mike-salerno-380.jpg 380w,
                         assets/img/team/mike-salerno-760.jpg 760w"
                 sizes="(max-width: 900px) 60vw, 30vw"
                 alt="Mike Salerno" width="760" height="950"
                 loading="lazy" decoding="async">
          </span></div>
        <div class="tm-voice__body">
          <p class="micro tm-voice__where">Naperville</p>
          <h3 class="tm-voice__name">Mike Salerno</h3>
          
          <p class="tm-voice__text">Mike has been with Chicago Motor Cars since 2019 but has been in the auto industry since 2009. He is a true car enthusiast with an affinity for Porsche and anything JDM. When you can't find Mike at the dealership, he is probably charting with Crypto and hitting the range. As with all of our guys, Mike is a straight shooter and will always tell you how it is.</p>
          <p class="tm-contact"><a class="tm-link" href="tel:+16302211800">630-221-1800</a><a class="tm-link" href="mailto:mike@chicagomotorcars.com">mike@chicagomotorcars.com</a></p>
        </div>
      </article>

      <article class="tm-voice">
        <div class="tm-voice__fig"><span class="tm-plate">
            <img src="assets/img/team/sanjin-salihovic-760.jpg"
                 srcset="assets/img/team/sanjin-salihovic-380.jpg 380w,
                         assets/img/team/sanjin-salihovic-760.jpg 760w"
                 sizes="(max-width: 900px) 60vw, 30vw"
                 alt="Sanjin Salihovic" width="760" height="950"
                 loading="lazy" decoding="async">
          </span></div>
        <div class="tm-voice__body">
          <p class="micro tm-voice__where">South Carolina</p>
          <h3 class="tm-voice__name">Sanjin Salihovic</h3>
          
          <p class="tm-voice__text">Sanjin&rsquo;s been a car enthusiast for as long as he can remember. Prior to becoming a partner of Chicago Motor Cars SC, Sanjin was a customer &amp; supporter for almost 10 years. Never having experienced such amazing hospitality and customer service elsewhere, Sanjin became very good &amp; close friends with Parin. If you know Sanjin, you also know he has a thing for purple!</p>
          <p class="tm-contact"><a class="tm-link" href="tel:+18038917788">803-891-7788</a><a class="tm-link" href="mailto:sanjin@chicagomotorcars.com">sanjin@chicagomotorcars.com</a></p>
        </div>
      </article>

      <article class="tm-voice tm-voice--flip">
        <div class="tm-voice__fig"><span class="tm-plate">
            <img src="assets/img/team/sara-vasic-760.jpg"
                 srcset="assets/img/team/sara-vasic-380.jpg 380w,
                         assets/img/team/sara-vasic-760.jpg 760w"
                 sizes="(max-width: 900px) 60vw, 30vw"
                 alt="Sara Vasic" width="760" height="950"
                 loading="lazy" decoding="async">
          </span></div>
        <div class="tm-voice__body">
          <p class="micro tm-voice__where">South Carolina</p>
          <h3 class="tm-voice__name">Sara Vasic</h3>
          
          <p class="tm-voice__text">Sara comes from an operations background, working in different industries prior to joining Chicago Motor Cars SC, she's developed a love for exotic cars and the industry. She keeps our South Carolina location running smoothly, her top priority being the experience and exceptional service customers receive. When she's not at work, you can find her traveling, hanging out with friends, or spending time with her little brother, Benjamin.</p>
          <p class="tm-contact"><a class="tm-link" href="tel:+18038917788">803-891-7788</a><a class="tm-link" href="mailto:sara@chicagomotorcars.com">sara@chicagomotorcars.com</a></p>
        </div>
      </article>

      <article class="tm-voice">
        <div class="tm-voice__fig"><span class="tm-plate">
            <img src="assets/img/team/sekou-dantzler-760.jpg"
                 srcset="assets/img/team/sekou-dantzler-380.jpg 380w,
                         assets/img/team/sekou-dantzler-760.jpg 760w"
                 sizes="(max-width: 900px) 60vw, 30vw"
                 alt="Sekou Dantzler" width="760" height="950"
                 loading="lazy" decoding="async">
          </span></div>
        <div class="tm-voice__body">
          <p class="micro tm-voice__where">South Carolina</p>
          <h3 class="tm-voice__name">Sekou Dantzler</h3>
          
          <p class="tm-voice__text">Sekou joined the CMC team in launching the new South Carolina Location in 2021. He&rsquo;s a professional photographer that has a 10 plus year background in the banking sector. Sekou brings with him a strong sense of customer service and attention to detail. He truly focuses on building strong client relationships by communicating thoroughly and being transparent. With 95 percent of our business being &ldquo;site unseen&rdquo;, you can count on Sekou to be your eyes and ears on the ground. When he&rsquo;s not at the dealership, he enjoys cooking and making YouTube videos at home with his wife and kids.</p>
          <p class="tm-contact"><a class="tm-link" href="tel:+12399109876">239-910-9876 <span class="tm-cell">cell</span></a><a class="tm-link" href="mailto:sekou@chicagomotorcars.com">sekou@chicagomotorcars.com</a></p>
        </div>
      </article>

      <article class="tm-voice tm-voice--flip">
        <div class="tm-voice__fig"><span class="tm-plate">
            <img src="assets/img/team/ricky-weimer-760.jpg"
                 srcset="assets/img/team/ricky-weimer-380.jpg 380w,
                         assets/img/team/ricky-weimer-760.jpg 760w"
                 sizes="(max-width: 900px) 60vw, 30vw"
                 alt="Ricky Weimer" width="760" height="950"
                 loading="lazy" decoding="async">
          </span></div>
        <div class="tm-voice__body">
          <p class="micro tm-voice__where">South Carolina</p>
          <h3 class="tm-voice__name">Ricky Weimer</h3>
          
          <p class="tm-voice__text">Ricky is a lifelong car enthusiast. His family has an extensive history of mechanic shops, body shops, dozens of dealerships as well as years of racing. His love for cars and desire to work in the automotive industry led to him joining Chicago Motor Cars in 2023. Although his entire life has been spent believing the &quot;Mopar or no car&quot; mantra, his love for high end sports cars and exotics has taken precedent and he truly belongs in this industry.</p>
          <p class="tm-contact"><a class="tm-link" href="tel:+17045172951">704-517-2951 <span class="tm-cell">cell</span></a><a class="tm-link" href="mailto:Ricky@chicagomotorcars.com">Ricky@chicagomotorcars.com</a></p>
        </div>
      </article>
    </div>
  </section>


  <!-- ============================================================
       5 — THE WAY OUT
       ============================================================
       Two existing destinations, no new control style: the filled pill
       to the showrooms and the quiet arrow link to the inventory.
       ============================================================ -->
  <section class="tm-cta" data-reveal aria-labelledby="tm-cta-t">
    <div class="shell tm-cta__inner">
      <h2 class="tm-h2" id="tm-cta-t">
        <span class="ttl-line">Come and meet</span>
        <span class="ttl-line">one of them.</span>
      </h2>
      <p class="lede">Every showroom keeps its own hours and its own phone. Walk in, or call
        the store you are closest to.</p>
      <div class="tm-acts">
        <a class="btn btn--fill" href="locations.html">See the showrooms</a>
        <a class="fn-jump tm-jump" href="srp.html">
          <span>Browse the inventory</span>
          <svg class="fn-jump__arrow" viewBox="0 0 16 16" width="15" height="15" fill="none" aria-hidden="true"><path d="M3 8h10M8.5 3.5 13 8l-4.5 4.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
      </div>
    </div>
  </section>

</main>"""


HEADER_COMMENT = """<!DOCTYPE html>
<html lang="en">
<!-- ============================================================
     team.html &#8212; GENERATED. Do not hand-edit.

     Head, masthead and footer are COPIED from index_3.html at build
     time by tools-build-team.py. index_3 is the source because it
     is the approved variant; a hand-copied nav is a nav that drifts.

     <body> carries `v2 is-team`: v2 because every page on this site runs
     the v2 layer, is-team because assets/css/team.css is scoped
     entirely to it and may not reach another page.
     ============================================================ -->
"""

out = (HEADER_COMMENT
       + h + '\n<body class="v2 is-team">\n'
       + nav + "\n" + (between if between.strip() else "\n") + "\n"
       + BODY + "\n" + footer + "\n" + script + "\n"
       + "</body>\n</html>\n")

open(OUT, "w", encoding="utf-8").write(out)
print("written", OUT, len(out), "bytes")
