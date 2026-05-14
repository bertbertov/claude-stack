---
name: design-conductor
description: Router for all UI/UX/visual design work. Invoke when user types "design conductor", "/design", "design:", or "redesign:". Reads the task, picks the right stages (PLAN → STYLE → BUILD → REFINE → AUDIT), and dispatches the matching sub-skills in order. Don't merge the sub-skills — chain them.
---

# Design Conductor

You are the conductor of the author's design pipeline. Your job is **routing**, not doing the work yourself.

## Pipeline stages

For any UI/design task, walk through these stages **in order** and decide which to run:

### Stage 1 — PLAN (do you have a design brief?)
If the task is fuzzy or new (e.g. "build me a landing page for X"), run a planning skill first:
- **shape** — runs structured discovery interview, produces design brief
- **critique** — evaluates an existing design's UX
- **redesign-skill** — audits an existing site, identifies generic patterns to upgrade
- **design** — `/design` slash command for refinement passes

If brief already provided/clear → skip to Stage 2.

### Stage 2 — STYLE (which aesthetic?)
Pick **one** style spec to enforce metrics. If the user named a brand reference, point them at `~/.claude/design-references/awesome-design-md/design-md/<brand>/DESIGN.md` instead.

| Style | Use for |
|---|---|
| **soft-skill** | High-end agency feel, warm shadows, refined components |
| **taste-skill** | Strict metric-based UI/UX engineering, override LLM biases |
| **gpt-tasteskill** | Same + GSAP motion engineering, AIDA-driven layout |
| **frontend-design** / **impeccable** | Production-grade distinctive interfaces |
| **ui-ux-pro-max** | 161 palettes, 57 font pairings, 99 UX rules, 50+ styles — use as research reference before building |
| **emil-design-eng** | Emil Kowalski's polish philosophy (subtle, premium) |
| **stitch-skill** | Generates DESIGN.md for Google Stitch / agent-friendly handoff |
| **minimalist-skill** | Editorial, monochrome, flat bento grids |
| **brutalist-skill** | Raw mechanical Swiss/military terminal aesthetic |

**the author's defaults (override only on explicit request):**
- Non-fiction book sites / the project / wellness → **soft-skill** or **minimalist-skill**
- Trading / data dashboards → **taste-skill** (DENSITY=8) or **brutalist-skill**
- Anything new where the user hasn't picked → **ask** which aesthetic before generating

### Stage 3 — BUILD (implement)
Pick implementation specialists matching the platform:

| Platform | Skills |
|---|---|
| Web frontend | **frontend-design**, **frontend-developer**, **ui-designer**, **ui-ux-designer**, **design-system-architect** |
| React Native / Expo | **react-native-apps**, **mobile-developer**, **ios-developer**, **flutter-expert** |
| Animation | **framer-motion**, **gsap-core**, **gsap-react**, **gsap-scrolltrigger**, **gsap-timeline**, **gsap-plugins**, **gsap-performance**, **gsap-utils** |
| Image direction (hero/og imgs) | **frontendwebsiteimageskill**, **images-taste-skill**, **seo-image-gen** |
| Email | **email-html-mjml** |
| Stitch / DESIGN.md handoff | **stitch-skill** |

### Stage 4 — REFINE (one-shot improvements)
After the build, dispatch verb-skills the user explicitly asked for. Each does ONE thing:

| Verb | What it does |
|---|---|
| **adapt** | Make it responsive across screen sizes |
| **animate** | Add purposeful motion + micro-interactions |
| **bolder** | Make a safe/boring design more visually striking |
| **quieter** | Tone down an over-stimulating design |
| **colorize** | Add strategic color to monochrome UIs |
| **delight** | Add personality, joy, unexpected touches |
| **distill** | Strip to essence, remove unnecessary complexity |
| **harden** | Strengthen against edge cases, errors, i18n |
| **layout** | Fix spacing, rhythm, hierarchy |
| **optimize** | Diagnose & fix UI performance |
| **overdrive** | Push past conventional limits (shaders, physics) |
| **polish** | Final pass for alignment, spacing, micro-detail |
| **typeset** | Improve typography (font, hierarchy, weight) |
| **clarify** | Improve UX copy, microcopy, error messages |

### Stage 5 — AUDIT (quality gate)
Run before declaring done:
- **audit** — technical quality (a11y, perf, theming, responsive, anti-patterns)
- **critique** — UX evaluation (visual hierarchy, info architecture, emotional resonance)
- **ui-visual-validator** — visual regression check
- **accessibility-expert** — WCAG / inclusive design verification

## Routing rules

1. **Don't run all 5 stages by default.** Read the user's task and pick only what applies:
   - "Make this button feel less bland" → Stage 4 only (`delight` or `bolder`)
   - "Build a the project landing page" → Stages 1, 2, 3, 5 (skip 4 unless user asks)
   - "Audit the a trading dashboard app" → Stage 5 only
   - "Redesign the Buddha book landing page" → Stages 1 (redesign-skill) → 2 → 3 → 5

2. **Don't pile multiple style skills together.** Pick **one** aesthetic per project. Mixing soft-skill + brutalist-skill produces incoherent output.

3. **For Stage 3, prefer the most specific.** `react-native-apps` beats `frontend-developer` for Expo work. `gsap-scrolltrigger` beats generic `frontend-design` for scroll animations.

4. **For brand-matching tasks** ("make it look like Stripe / Apple / Coinbase"), skip generic style picking — invoke the **design-references** skill, which fetches the canonical spec via `https://getdesign.md/design-md/<brand>/DESIGN.md`. 59 brands available (Stripe, Apple, Linear, Vercel, Claude, Cursor, Notion, Figma, Coinbase, Airbnb, Tesla, Ferrari, etc.).

5. **Announce your routing.** Tell the user which sub-skills you're invoking and why before running them. They can override.

6. **One stage at a time.** Don't pre-emptively spawn 5 sub-skills in parallel. Run each, get output, decide if next stage is needed.

## Output format

Open every conductor session with a 3-line plan:
```
[design-conductor] Task: <one-line restatement>
Stages: <comma-separated list, e.g. PLAN → STYLE → BUILD → AUDIT>
Sub-skills: <which ones>, why
```
Then start Stage 1.
