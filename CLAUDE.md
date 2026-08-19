# Chicago Motor Cars — working rules

Static redesign preview, no build step. Open `index.html` directly or
`python3 -m http.server`.

## AAN / Ivaylo / Master27 styling is BANNED in this project

`~/.claude/skills/aan-dealer-mockups/` is a **global** skill whose own
description claims every dealership design task, in these words: *"Use this
skill whenever designing or revising ANY web design work for a car dealer
site … **even if the user never mentions AAN, WordPress, or Bootstrap**."*
It carries a component kit — `$btn-radius: 4px`, `$btn-padding: 14px 28px`,
Bootstrap 4 grid, Owl Carousel — that directly contradicts this project's
own controls.

**For Chicago Motor Cars it has ZERO authority.** Do not read it, apply it,
or borrow its buttons, links, underlines, cards, spacing, typography, grids,
responsive patterns or hover treatments. It is not deleted, because other
projects use it; the ban is scoped to this folder.

### Source priority for every visual decision here

1. Alex's explicit art direction.
2. **The approved rendered CMC homepage** — it is the source of truth for
   component styling.
3. Approved existing CMC components and tokens.
4. Design DNA — for **composition, hierarchy, rhythm, negative space and art
   direction only.** It does not define button or link styling.

**A NEW SECTION IS NOT A NEW BUTTON SYSTEM.** A new chapter earns its
identity from composition — scale, spacing, asymmetry, typographic placement.
Its actions reuse the existing primitives. Inventing a control style for one
section is the failure mode this rule exists to stop; it has happened, with a
giant underlined text link in Financing, and it was rejected on sight.

**Audit before you change.** A component inventory taken from a working tree
that already contains your own edits is worthless — it describes your
experiment, not the approved system. Restore to the last approved commit
first, then read the render.

## Design DNA governs every visual decision here

**Before any design, layout, CSS, typography, colour, imagery or motion work,
invoke the `design-dna` skill.** It is installed globally and routes to the
manifest and to whichever taste skill the task needs.

`design_dna/` in this folder is a **live git clone**, not a copy — so it is a
legitimate source, and `npm run sync` inside it keeps it current. Run that before
design work rather than trusting whatever it held last time.

The mandate is **REDESIGN**. Carried through untouched: the handwritten
wordmark, red `#CB141D`, the KARMA status, four locations, the fact set.

## The art direction, named by Alex 2026-08-06

**Performance Editorial / Private Collection.** Not nightclub, not
crypto-luxury, not standard dealership. Its terms, and what each one has already
changed:

| Direction | State |
|---|---|
| deep navy, not pure black | `--bg: #0B101C`, `--bg-rgb: 11 16 28` |
| warm off-white, not white | already true — `--ink: #F4F2EF`, `--bone` |
| large, slightly condensed type | display is now a **serif** |
| thin technical captions | JetBrains Mono at the 14px floor |
| real inventory cars, not stock supercars | `assets/img/stock/` — ten real CMC frames. **`hero_d.jpg` is unresolved, see its sidecar** |
| slow cinematic transitions | `--dur-3: 520ms`, `--dur-4: 760ms` |
| minimum decorative glassmorphism | blur cut 24px → 12px; the ground does the legibility work, the blur was the decoration |
| rarity, specification, provenance | not started — belongs to the sections below the hero |

**Type is now three voices, and the display face is a serif:**
`Instrument Serif` display · `Instrument Sans` body · `JetBrains Mono` data.

This REVERSES the earlier "no serif" decision. The reversal is the client's
direction, not a change of mind: the reference sets the claim in a high-contrast
serif. "No serif" was itself a *named yield* on the dialect — the dialect asks
for a didone display — so this returns to the dialect rather than breaking it.
What the old reasoning got right still governs: character comes from scale,
position and air. The serif is allowed **at display size only**; body stays the
grotesque and nothing else gets set in it because it looks expensive.

Two dialect yields stand with their reasons: `color D2` for the undesaturated
red, `anti-patterns D6` for two doors of equal rank. **Do not silently re-derive
any of this**; reopen only with an argument, and record the argument.

Invariants never yield to this project's direction. Contrast is measured **on the
composite render**, not on tokens — that rule exists because `--ink-3` shipped at
3.7:1 before it was caught.

## Imagery is synthetic until it is not

Every hero frame is currently an **AI placeholder**, and the README names this as
the project's main risk: both Semler records in the vault warn that large scale on
uneven photography magnifies an asset dependency.

`generated-imagery` binds. The practice already established in
`assets/img/hero/` is the correct one and must not regress:

- filename carries the **`gen-` prefix**, and it travels with the file;
- a `.txt` sidecar beside it records origin, model, date and subject, plus the GI
  audit;
- **nothing synthetic depicts a real CMC car, a real CMC showroom or a real
  person** (GI3) — this is a dealership, and a generated photograph of a car being
  sold is a false statement about that car.

An image with no declared origin is the failure mode. `hero_d.jpg` now has a
sidecar (`hero_d.txt`) and correctly carries **no** `gen-` prefix, because it is
not synthetic — but its sidecar records a real open question: whether it is CMC's
own frame or a stock/press image is unconfirmed, and the art direction rules out
universal stock supercars. Resolve before it goes to the client.

## design.html is STALE as of 2026-08-06

The specimen sheet still documents the previous system — black ground, a
grotesque display face, pill-shaped buttons — none of which is true now. Its
runtime machinery is honest (it prints families from computed style and sweeps
its own contrast), so it will report the serif correctly, but the PROSE around it
lies. A page that measures itself and then misdescribes itself is worse than one
that does neither. It needs a pass before it is shown to anyone.

## The cache trap

Stylesheet links carry `?v=N`. **Editing `tokens.css` or `main.css` means bumping
the number in `index.html`**, or the browser serves the cached file. This has
already cost two iterations — a type-scale change that appeared to do nothing
because the token was correct and the CSS never loaded.

`assets/css/tokens.css` is the single source of truth for colour, type scale and
spacing. Values go there, never inline.

## Section entry motion is a project rule, not a per-section effect

**Every section below the hero uses one shared entry language.** The hero is
excluded and keeps its own cinematic behaviour.

| Role | Motion |
|---|---|
| headline | one **line** at a time, in from the **left**, −56px → 0 |
| paragraph | one block, from **below**, +32px → 0 |
| action | quiet vertical settle, +10px → 0 |
| eyebrow | fade with 6px, never competing with the headline |
| secondary proof | may enter from the **right** where the composition asks |

Durations live in `tokens.css` as `--rv-line` / `--rv-lede` / `--rv-cta` and the
staircase interval as `--rv-step`. Easing is `--ease-out`. Nothing in this system
is written inline.

**A new section opts in with `data-reveal` on the section and the existing role
classes on its parts** — `.ttl-line` per headline line, `.lede`, the CTA. It then
inherits the choreography with no new CSS. Do not author a different entrance for
a new chapter; add it to this system.

Scroll-**triggered**, not scroll-linked: one IntersectionObserver, `rootMargin`
`-22%`, `unobserve` on first hit. One reveal per visit, and a section taller than
the viewport still fires — a ratio threshold would not.

`html.reveal-armed` is added **by script, after checking `prefers-reduced-motion`**.
Nothing is hidden without it, so a blocked script or a reduced-motion setting
leaves every section complete. The hidden state is written once per role as
`[data-reveal]:not(.is-revealed)`; the revealed state is simply the element.

**These animations survive later layout work.** Redesigning a section does not
remove its entry motion unless Alex asks for that specifically.

Recorded dialect yield: `motion-taste D1` caps travel at 8px and prefers a
crossfade. The headline travels 56px horizontally, on the stated exit — direction
encoding progress. Transform and opacity only; no geometry animates.

## There are TWO motion systems, and picking the wrong one is why this keeps getting rebuilt

The section-entry rule above covers the **one-shot** case. It is not the
only system, and the second one was never written down — which is why it
has been re-derived from scratch more than once, with a new set of
keyframes each time. Both are already built. Neither needs inventing.

| | ONE-SHOT ENTRY | SCRUBBED PASS |
|---|---|---|
| when | a section arrives and stays | a thing arrives **and leaves** with the scroll |
| driver | `IntersectionObserver` → `.is-revealed` | `animation-timeline: view()` |
| opt in | `data-reveal` + role classes | `hero-in` + `hero-exit` |
| tuning | `--rv-line/-lede/-cta/-step` | `--in-rise`, `--in-blur`, `--rise`, `--blur` per element |
| staggering | `transition-delay` | **shifted `animation-range`, never delay** |

**`hero-in` and `hero-exit` are the house gesture for in-and-out.** They
are in `main.css` and already drive the hero claim and the break section.
Anything that has to enter and leave uses them, with its own rise values
and its own short range. Writing a third keyframe pair for one row is the
failure this table exists to stop.

**Stagger a scrubbed pass by shifting each item's `animation-range`.** A
`delay` staggers the entrance and then piles every exit into one frame —
they must leave in the order they arrived.

**Ranges stay short.** Recorded against `vault/morningstar-ventures`,
whose logged weakness is this exact gesture run at length: the page stops
on frames where the outgoing thing is half gone and the incoming one is
not yet there.

**A scrubbed timeline runs backwards when the scroll does.** Coming back
up the page, a thing re-enters from the direction it left. That is not a
bug to fix — it is what scrubbing is. Always-one-direction means giving
up the scrub for a one-shot on scroll direction, and that is a different
decision, to be made deliberately.

**Blur belongs to type, not to plates.** In the hero it is tied to speed
because letterforms smear. A hard-edged white card blurred reads as the
render failing.
