REAL Chicago Motor Cars inventory assets. Two sets, one of them live.

--------------------------------------------------------------------
LIVE — the cut-outs (cutout-*.png)
--------------------------------------------------------------------
These four are what the Featured Inventory section renders.

  cutout-porsche-gt2rs.png          2018 Porsche 911 GT2 RS Weissach
  cutout-aventador-svj-roadster.png 2021 Lamborghini Aventador SVJ Roadster
  cutout-koenigsegg-regera.png      2021 Koenigsegg Regera
  cutout-ferrari-812-gts.png        2023 Ferrari 812 GTS

Supplied by Alex as transparent PNGs with a soft contact shadow already
baked in under the wheels. Do NOT add a second shadow in CSS — that was
tried and it is what made the cars read as pasted.

They are not cut alike. The GT2 RS and the Aventador were traced with
real margin around the bodywork; the Regera and the 812 run almost edge
to edge inside their own frame. main.css sizes those two smaller so all
four sit in the field with comparable air. If a cut-out is replaced,
check its margin before assuming the default width fits.

--------------------------------------------------------------------
NOT CURRENTLY USED — the photographic frames (cmc-*.jpg)
--------------------------------------------------------------------
Kept because they are the fallback for any vehicle that has no cut-out,
and because two of them are the only frames found in a genuinely clean
environment.

Origin: chicagomotorcars.com's own image CDN (/imagetag/...), read off
the live inventory listing on 2026-08-07. Their own frames of their own
cars. Not synthetic, not stock, no gen- prefix. 1920x1280, all 3:2.

  cmc-porsche-gt2rs.jpg   \  the Kansas industrial space — black steel,
  cmc-porsche-gt3.jpg     /  polished concrete, no turntable, no
                             showroom curtain, no burned-in wordmark.
                             The only clean-environment set in the
                             inventory; everything else is shot on a
                             turntable against a grey curtain with the
                             script wordmark burned into the frame.
  cmc-koenigsegg-regera.jpg \ seamless studio, car isolated, clean.
  cmc-rimac-nevera.jpg      /

--------------------------------------------------------------------
THE DATA IS REAL AND IT IS DATED
--------------------------------------------------------------------
Every price, mileage and vehicle on the cards was read off the same live
listing, sorted price high-low. Prices and mileage move, and the fleet
count was 299 at an earlier capture and 301 here. RE-PULL BEFORE THIS
GOES IN FRONT OF ANYONE.

OUTSTANDING: the "Just in" pill is static. It is a claim about a
vehicle's arrival date and the feed exposes none, so right now it sits
over whichever car is active — which asserts all four are new arrivals.
Bind it to a real date-added field and render it conditionally.
