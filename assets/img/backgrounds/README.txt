Background frames — full-bleed section grounds.

--------------------------------------------------------------------
cmc-ford-gt-showroom.jpg           5760 x 2550   2.05 MB   MASTER
cmc-ford-gt-showroom-2560.jpg      2560 x 1133    113 KB   served
cmc-ford-gt-showroom-1600.jpg      1600 x  708     57 KB   served
--------------------------------------------------------------------

Supplied by Alex on 2026-08-10, dropped in as image.jpeg and renamed
here. It is the ground of the STORY section ("Built on more than
exceptional cars").

The master stays as the source and nothing serves it: the band is
full-bleed, so a 1440 viewport asks for 1600 and a 2x one for 2560.
2.05 MB -> 57 KB / 113 KB. Rebuild the derivatives from the master, not
from each other:

  ffmpeg -i cmc-ford-gt-showroom.jpg -vf "scale=2560:-2:flags=lanczos" \
         -q:v 4 cmc-ford-gt-showroom-2560.jpg

Subject: two Ford GTs — a first-generation car in white with blue
stripes and a second-generation car in blue — on a dark reflective
floor, against a wall carrying Ford and Shelby Cobra murals, with a red
rim light behind the blue car. The lower third of the frame is empty
floor, which is where the statistics sit.

NOT SYNTHETIC. No gen- prefix, and none is owed: this is a photograph,
so generated-imagery does not apply to it.

--------------------------------------------------------------------
TWO THINGS ARE UNCONFIRMED, AND BOTH MATTER BEFORE IT GOES TO A CLIENT
--------------------------------------------------------------------
1. ORIGIN. Whether this is CMC's own photograph, a Ford press image, or
   stock is not established. The same open question sits on
   assets/img/hero/hero_d.txt. An image with no declared origin is the
   failure mode this project has already named once.

2. WHAT IT CLAIMS. It runs under "For over two decades, Chicago Motor
   Cars has connected enthusiasts and collectors..." — so it reads as
   CMC's own room and CMC's own cars. If the cars or the wall are not
   theirs, the section is making a claim the photograph cannot support,
   and the art direction's "real inventory cars, not stock supercars"
   is the rule it breaks.

Neither is a rendering problem and neither is fixed by CSS. Confirm the
provenance or swap the frame.
