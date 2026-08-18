# The listing copy for stock 22703, as supplied by Alex 2026-08-18.
#
# ONE TEXT, HEADINGS AND LINES. His instruction: "давай одним текстом,
# только заголовки и только текст перечисление." So there are no cards,
# no columns, no hairlines and no price chips here — a heading, then its
# lines, then the next heading. The structure is the feed's own.
#
# The asterisks and the ALL CAPS come off, because that is how you set
# emphasis in a plain-text field and this page has type for it. Nothing
# else is touched: not a word is added, removed or reordered.

LEAD = "Venom Black Clear Coat over Black Interior"

# Each entry is (heading or None, [lines]). None means the block runs
# without one — the opening claims have no header in the source.
BLOCKS = [
    (None, [
        "Only 3,100 miles",
        "ACR Interior Package",
        "Extreme Aero Package",
        "Collector quality example",
        "Ultra-rare Voodoo II Edition",
        "Chassis #29 of 31 ever produced",
        "1 of just 31 units ever produced",
        "Excellent condition throughout",
        "American made high-performance track car",
    ]),

    ("Factory options include", [
        "ACR Package (Originally $19,000)",
        "ACR Badge",
        "SRT 6-Vent Hood",
        "Lower Dive Planes",
        "Front Splitter Assembly",
        "Satin Black Front Decal",
        "Finned Differential Cooler",
        "Satin Black Fuel Filler Door",
        '19" Satin Black ACR Wheels',
        "Manually Adjustable Suspension",
        "Red Brembo Brake Calipers w/ Viper Logo",
        "Exposed Weave Carbon Fiber Exterior Wing",
        "",
        "Voodoo II Edition (Originally $8,300)",
        "Custom Car Cover",
        "Voodoo II Sill Decal",
        "Voodoo II Serialized Badge",
        "Voodoo II Driver Stripe w/Tracer",
        "",
        "Extreme Aero Package (Originally $6,900)",
        "Extreme Hood",
        "Upper Drive Planes",
        "Extreme Rear Diffuser",
        "Adjustable Extreme Aero Wing",
        "",
        "ACR Interior Package (Originally $6,000)",
        "ACR Console",
        "ACR Door Trim Panel",
        "ACR Instrument Panel",
        "High-Grip Alcantara Leather Seats",
        "Alcantara Wrapped Steering Wheel",
    ]),

    ("Vehicle highlights", [
        "8.4 Liter 10-Cylinder Engine",
        "645 Horsepower",
        "600 Lb/ft of Torque",
        "Rear Wheel Drive",
        "6-Speed Manual Transmission",
    ]),

    ("Exterior highlights", [
        "LED Rear Taillights",
        "Front Fender Venting",
        "LED Front Headlights",
        "ACR Extreme Aero Wing",
        "Gloss Black Rear Diffuser",
        "Gloss Red Tow Hook Accent",
        "Intermittent Windshield Wipers",
        "SRT Hood Vents & Hood Scoop",
        "Satin Black Viper Logo on Hood",
        "Ground Effects / Lower Spoilers",
        "Front Dual Carbon Fiber Canards",
        "Power Adjustable Exterior Mirrors",
        'Satin Black Gas Cap w/ "Viper" Logo',
        'Side "VOODOO II" Badging In Black & Red',
        "Vented Hood w/ Grey & Red Single Stripe Accent",
        'Red Painted Brembo Brake Calipers w/ "Viper" Logo',
        "Rear Carbon Fiber Spoiler w/ Gloss Black & Red Accents",
        "Dual Side Exit Performance Exhaust System w/Stainless Steel Tips",
    ]),

    ("Interior highlights", [
        "Cruise Control System",
        "Black Suede Headliner",
        "Black Leather Shift Boot",
        "Rear View Camera System",
        "Manual Adjustable Seating",
        "Multi-Function Steering Wheel",
        "White Accent Interior Stitching",
        "Black Leather Emergency Brake",
        "Electronic Launch Control System",
        "Automatic Climate Control System",
        'Aluminum Door Sills w/ "Viper" Logo',
        "Black Alcantara / Leather Door Panels",
        "Digital Driver Instrument Cluster Display",
        "HD Navigation System w/Live Traffic Info",
        "Harman / Kardon Premium Sound System",
        'Passenger Dashboard "Voodoo II" Badging',
        "Adjustable Adaptive Driving Modes & Suspension",
        "Multifunction Center Entertainment Touch Display Screen",
        "Black Alcantara Steering Wheel w/ White Accent Stitching",
        "Manual Adjustable Black Alcantara / Leather Front Seating w/ White Accent Stitching",
    ]),

    ("Vehicle history", [
        "8.4 Liter V10 Engine",
        "Rare Voodoo II Edition",
        "Unit 5 of 31 Ever Produced",
        "Excellent Condition Throughout",
        "A Must Have for Any Viper Fan or Collector",
        "Highly Desired Viper GTC VoooDoo II Model",
        "645 Horsepower American Made High-Performance Muscle Car",
    ]),

    ("Includes", [
        "Original Car Cover",
        "Original Floor Mat Set",
        "Original Owners Manual",
        "Two Master Remote Keys",
    ]),
]

# Their disclaimer, still theirs, still at the foot.
DISCLAIMER = [
    "Please remember, every one of our cars has been enjoyed by their original owners, "
    "and these are not factory-new cars. This means they have actually been driven, and "
    "regardless of the level of care, every car will exhibit some wear-and-tear. Our "
    "vehicles are advertised with the current mileage at the time of listing, so mileage "
    "at the time of sale may vary due to test drives, transportation for reconditioning, etc.",

    "We do all within our power to avoid mistakes or misprints, so if you see any inaccuracy "
    "within our listing, we only ask that you bring this to our attention so that we can "
    "immediately rectify the information. Since our ultimate goal is 100% customer "
    "satisfaction, we ask every customer to verify the listed equipment at the time of "
    "purchase with their salesperson.",

    "All sales must add tax, title, license and $300.00 Illinois Doc fee. Fees may vary by "
    "state and county of new vehicle registration. Contact dealer for details.",
]


# The standards band. "Delivered nationwide" now points at the shipping
# calculator further down the page, because a claim with a working
# estimator behind it is a different kind of claim.
STANDARDS = [
    ("Inspected in house",
     "Chicago Motor Cars runs its own service department \u2014 inspection, brakes, "
     "alignment, electrical and transmission work happen on site rather than at "
     "a third party."),
    ("Coverage available",
     "Aftermarket plans for pre-owned exotic, performance and collector vehicles, "
     "matched to the car rather than sold as one product."),
    ("Delivered nationwide",
     'Four showrooms across Illinois, South Carolina and Kansas, and delivery to '
     'your door anywhere in the country. '
     '<a class="stds__link" href="#shipping" data-open-panel>Estimate shipping &rarr;</a>'),
    ("Since 2003",
     "More than 40,000 exotic, luxury and collector vehicles sold, and over "
     "$4 billion in worldwide sales."),
]
