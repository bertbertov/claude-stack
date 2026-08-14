---
name: anti-generic-frontend
description: Hard gate plus a countable rule set for any website, landing page, hero, marketing section or portfolio, so the output cannot ship as Claude-generic. Fires on build, redesign, "make it premium", or any rejection as templated, AI-made, slop or boring. Routes to taste-skill for the deep rule library and signature-web for motion and effect tiers.
---

# Anti-Generic Frontend

Generic output is the **expected** output, not a failure. Models regress to the statistical centre of the web, shared component defaults look alike, and every system prompt chases the same safe adjectives. So the fix has to be an **upstream constraint**, never a downstream nudge. "Make it nicer" produces a nicer average. Deciding the tokens before writing markup produces a design.

Written from the kamalov.systems build, 2026-08-14, where every value came out of a measured reference stylesheet rather than taste.

---

## 🛑 STOP GATE — do not write markup until this is answered

**Name the cluster you are closest to, and say what structural change breaks it.** A hue swap is not a change. `#0B0A09` to `#1A0A0A` is the same design.

| # | Cluster | Signature |
|---|---|---|
| a | Warm cream + high-contrast serif + terracotta | `#F4F1EA` ground, Fraunces or Instrument Serif, rust accent |
| b | Near-black + one acid accent + gradient-clipped headline | `#0a0801` + `#caa100`, gradient text |
| c | Broadsheet | hairline rules, zero radius, dense newspaper columns |
| d | Navy/slate + gold or purple | emoji headings, identical rounded stat cards, centred everything |
| e | Premium-consumer beige and brass | bg `#f5f1ea`/`#f7f5f1`, accent `#b08947`/`#b6553a`, ink `#1a1714` |

**Ground the alternative in the subject's own world** — its materials, instruments, artifacts, vernacular. A brokerage has order books, session clocks, spreads, latency. A bakery has proof times, flour, steam. Take the signature from there. A style menu is just a smaller distribution to collapse onto.

**Rotation rule:** if the last project in this category used a palette family, this one may not.

---

## 1. Design read — one line, before anything

> Reading this as: a `<page kind>` for `<audience>`, in a `<vibe>` language, leaning `<direction>`.

If that sentence could describe any site, it is not a read.

---

## 2. Token contract before markup

Write it to `UI-SPEC.md` in the project. Not a comment, a file, so a later audit can grade the build against it.

- **4 to 6 named hex.** Ground, surface, ink, muted, accent, plus semantic status colours if the subject needs them.
- **`Accent reserved for:` an explicit list.** "All interactive elements" is not an answer. Name the four things. mora.com ships with **no accent at all** and still reads expensive.
- **60/30/10** by area.
- **2 or 3 type roles**, real families, with the scale ratio fixed here.
- **Layout concept plus an ASCII wireframe.**
- **One signature element**, with a `why` written in terms of the subject. "Depth" is not a why.

Then **re-derive the plan from a generic version of the same brief.** Anything that survives both is a default. Revise it, and state what changed.

---

## 3. Countable rules

These are checkable, which is the point. Felt quality is unfalsifiable.

**Type**
- 🛑 **The single loudest AI tell is the 12px uppercase letter-spaced MONO micro-label** sitting above a grotesque-sans heading. That pairing is every AI-generated SaaS page. It reads "competent startup", never "expensive". Rejected in production 2026-08-14 with: *"fonts reveal ugly claude generic design."*
- **Expensive means a display serif.** Luxury references (izanami, Vogue, private banks, editorial) run Didone or high-contrast serif at large size with air. If the brief says premium, fancy, luxury or expensive, reach for **Bodoni Moda, Cormorant, Cinzel, Playfair or Marcellus** and set eyebrows in **serif italic**, not mono uppercase. Fraunces and Instrument Serif stay banned; they are the LLM-favourite two.
- Didone hairlines need care on dark grounds. Verify contrast at the real display size before shipping.
- Text-range font sizes **≤ 4**. Weights **≤ 3**.
- Ratio ~1.25 through text, opening to ~1.4 at display. A real canyon between body and hero is what makes a claim land.
- Force comes from **size and tracking, not weight**. mParticle uses weight 700 fifteen times on its entire site.
- `font-variant-numeric: tabular-nums` on every figure. Non-negotiable when the subject is numbers.
- Prose measure **≤ 719px**.
- Uppercase mono eyebrows: 12px, `letter-spacing: .09em`.

**Colour**
- Accent on **≤ 4 unique element types** (audit tools flag at 10; aim far tighter).
- Never `#000000`. Off-black with a cast.
- No neon or outer glow. No gradient headline text. No purple-blue gradient.
- Shadows take a colour cast, never pure black. `rgb(0,2,4)` reads better than `#000`.

**Layout**
- **Radius: two values, nothing between.** A 4/8/12/16/20/24 ladder is what makes a page look assembled.
- Eyebrows **≤ ceil(sections / 3)**. Count `uppercase tracking` instances. Panel labels inside a card are a different job; give them a different class and do not count them.
- Hero: headline **≤ 2 lines**, subtext **≤ 20 words**, **≤ 4 text elements**.
- Consecutive image-text zigzags **≤ 2**. Distinct layout families **≥ 4** across 8 sections.
- Bento cells **== item count** exactly. An empty cell means you planned wrong.
- **No three equal feature cards.** The most common AI layout tell.
- Asymmetric splits, never 50/50. Nav one line, ≤ 80px.

**Copy**
- **Zero em-dashes.** Binary because "sparingly" gets ignored. Headlines, eyebrows, pills, body, quotes, captions, buttons, alt text, `<title>`.
- No filler verbs: elevate, seamless, unleash, revolutionize, next-gen, empower.
- No fake-perfect numbers. `99.99%` and `50%` read as invented; `47.2%` and `$0.65` read as measured.
- No Acme, Nexus, John Doe. No section-number eyebrows (`001 · Capabilities`). Middle-dot rationed to one per line.
- No decorative status dots. A dot must mean something.

**Motion**
- One orchestrated moment beats scattered micro-interactions.
- Entrance decelerates, exit accelerates, **never `linear` for spatial movement**.
- Nothing over 700ms. Total stagger under 500ms.
- Marquees at **~32 px/s** with `translate3d(0 → -50%)` over a duplicated group, and a `transparent 0% / black 5% / black 95% / transparent 100%` mask.
- Only `transform` and `opacity` animate per frame.
- `prefers-reduced-motion` gets a **legible fallback**, not "animations off".

---

## 4. Assets and honesty

- **Never fabricate client logos, awards, testimonials or metrics.** A marquee of *real integrations* is visually identical and entirely true. Invented logos imply clients that do not exist.
- Real photo means a real URL with a real extension. Anything conceptual emits a delimited image-generation prompt block instead. **Never invent a link.**
- **No div-built fake screenshots.** A live component showing real data is fine and better; a stack of divs pretending to be a product screenshot is not.
- If real user content is displayed, anonymize it. Publishing customer conversations exposes them.

---

## 5. Verification — score it, do not eyeball it

**Reading the diff is not verification. Open the page.**

Mechanical pass, all must hold:
```bash
grep -c '—' page.html                      # 0
grep -oE 'font-weight:[0-9]+' page.html | sort -u | wc -l   # <= 3
grep -oE 'border-radius:[^;}]+' page.html | sort -u          # 2 values
grep -c 'class="eyebrow"' page.html         # <= ceil(sections/3)
grep -o 'var(--accent)' page.html | wc -l   # <= ~6 including hover states
```

Visual pass at **1440 / 768 / 375**. Score six pillars 1 to 4 — copy, visual, colour, type, spacing, experience — for a total out of 24, **assuming every pillar fails until a screenshot proves otherwise**. Publish gate: no pillar at 1, total ≥ 20.

Also: console clean, no 404 assets, keyboard focus visible, reduced-motion path exercised, and **every script the page claims to support actually renders** without tofu.

⚠️ **A backgrounded tab throttles transitions and rAF.** `document.hidden === true` means CSS transitions may sit at their start value and screenshots capture a blank or pre-animation frame. **Assert `document.hidden` before trusting any visual check**, and never conclude "the element is broken" from a hidden-tab capture. This wasted several rounds on 2026-08-14, first misdiagnosed as a `mix-blend-mode` compositing bug.

⚠️ **A JS error in one script block kills every script after it.** A dead `getElementById` left behind after removing a section threw `null.appendChild`, which silently killed an unrelated component further down the file. **Read the console after any structural edit** — the symptom appears in a component you did not touch.

⚠️ **`resize_window` cannot go below Chrome's minimum window width** (~500px). Asking for 375 silently returns ~1448 and you will "verify" mobile at desktop width. Use devtools viewport emulation for anything under 500px.

**The mirror test:** would a design-led studio ship this, or does it read "an AI made a landing page"? If the latter, return to the gate. Do not tune spacing and re-ship.

---

## 6. Failure modes

| Tell | How it gets in | Mechanical check | Fix |
|---|---|---|---|
| "Still generic" after a recolour | Changed hue, not structure | Cluster named in the gate? | Change what carries meaning |
| Three identical cards | Default feature-row shape | Count equal-width siblings | Zigzag, asymmetric grid, or a table |
| Value and caption run together | Sibling `<span>`s with no `display:block` | Render and read it | Block the child |
| Headline overflows to 3 lines | `max-width` in `ch` set against display size | Measure height / line-height | Widen the measure or cut words |
| Marquee shows dead gaps | Items too wide for the loop | Item width vs viewport | Cap item width, ellipsis |
| Mobile "verified" but broken | Window would not shrink | Assert `clientWidth` | devtools emulation |
| Tofu in non-Latin text | Display face lacks the script | Render every claimed script | Explicit Noto fallback chain |
| Beautiful, nothing moves right | Motion added ad hoc | One personality named? | Lock easing, 3 durations, one entrance |
| Janky scroll | Animating layout properties | Which properties animate | transform and opacity only |
| Impressive tech, hollow page | Technology chosen first | Does the effect have a subject-grounded why | Cut it |

---

## 7. Route to another skill

- **`taste-skill`** (v2, 1,206 lines) is the deep rule library. This skill is the gate and the countable subset. Use both.
- **`signature-web`** for motion identity and the CSS → Canvas → GSAP → Three.js effect-tier decision with budgets.
- **`premium-pdf-design`** for print, decks and one-pagers.
- **`super-book-cover`** for covers and thumbnails.
- **`de-ai`** for the copy itself. The em-dash ban and the filler-verb ban are the same rule in both places.

---

## Worked example, kamalov.systems, 2026-08-14

Cluster risk was (b) and (d). Broken structurally: **light bone ground with a green-grey undertone** rather than near-black, **olive neutrals** rather than slate, **cobalt** rather than gold, accent used **4 times on the whole page**.

Type: **Archivo variable at `wdth 115`**. The expanded width axis is the characterful choice and it is why the hero reads as instrument-panel authority rather than default grotesque.

Signature: a full-bleed drift of real anonymized agent messages, each pill stamped with channel, language and reply latency. **Eleven languages is a claim no headline can prove; five scripts drifting past in peripheral vision proves it in two seconds.** It also removed any need for client logos.

Three bugs found only by looking: metric values rendering inline with their captions, a hero wrapping to three lines against a two-line cap, and marquee chips wide enough to drift a dead gap through the viewport.
