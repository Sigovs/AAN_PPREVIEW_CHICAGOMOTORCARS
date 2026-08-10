# Chicago Motor Cars — working rules

Static redesign preview, no build step. Open `index.html` directly or
`python3 -m http.server`.

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
