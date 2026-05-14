# Workflow: redesign an existing site

For when you have a live site that looks generic-AI and needs to become distinctive.

## The prompt to use

```
/design redesign <URL>.

Why: <one-line — what's wrong with the current look>
Audience: <who visits this and what they want>
Goal: <one primary outcome>
Vibe: <target aesthetic OR brand match>
Constraints: <stack, mobile-first, anything load-bearing>
```

## Routing

| Stage | Skill | What happens |
|-------|-------|--------------|
| **PLAN** | redesign-skill | Audits the live site — identifies generic AI patterns, weak hierarchy, motion-less UI, generic copy |
| **STYLE** | design-references OR a flavor skill | Picks the new direction |
| **BUILD** | frontend-design | Implements the redesign |
| **REFINE** | layout → typeset → animate → polish | Tighten in order |
| **AUDIT** | critique + audit | UX + technical quality check |

## The redesign-skill diagnostic (auto-runs in PLAN stage)

It looks for:
- **Centered H1 hero** with stock photo gradient → AI-generic tell
- **3 equal cards** below the hero → cookie-cutter
- **Inter font + AI purple/blue gradient** → 2023 AI starter aesthetic
- **Filler copy** ("Elevate", "Seamless", "Unleash", "AI-Powered") → marketing slop
- **No motion** OR motion-everywhere → either dead or seizure-inducing
- **No hierarchy** — same font weight throughout

Each finding is severity-rated. P0 must fix before relaunch. P1 should fix.

## Anti-patterns that surface most often

1. **Centered everything** — subject center, title center, evenly spaced. Static. Replace with split-screen, asymmetric, or rule-of-thirds anchored.
2. **Subject < 35% of frame** with unexplained void = "I ran out of ideas." Fix by scaling subject to 45-60% OR filling void with one load-bearing element.
3. **Stock-photo hero faces** — generic stock model with white smile. Replace with single load-bearing metaphor (object, anatomy, location).
4. **Cards everywhere** — every section is a `border rounded-lg p-6` card. Use `border-t` dividers OR negative space for at least half the sections.
5. **Inter font + sans-serif body** — ubiquitous AI default. Switch to Cabinet Grotesk / Geist / Satoshi / Outfit.

## Output deliverable

A redesign PR (or new repo if greenfield) with:
- Audit doc listing P0/P1/P2 findings
- New design system tokens (color / type / spacing / motion)
- Hero section rebuild (the highest-impact change)
- 2-3 supporting sections rebuilt to demonstrate the new system
- Migration plan for the remaining sections

## Cost

- Pure local work, $0 in API calls
- If hero/section images need regenerating: fal.ai or local ComfyUI
