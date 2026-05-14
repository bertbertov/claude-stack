# Workflow: ship a landing page

End-to-end recipe for a production landing page using the conductor pattern.

## The prompt to use

```
/design build a landing page for <PRODUCT>.

Audience: <who buys this, in one line>
Goal: <one CTA, e.g. "trial booking" or "email signup">
Vibe: <one of: premium-quiet | editorial | brutalist | playful | data-dense> OR brand match (e.g. "Stripe-style", "Linear-feel" — fetched from design-references)
Stack: <Next.js 15 | Astro | plain HTML+Tailwind>
Constraints: <mobile-first, RTL-ready, AMOLED dark, anything specific>
```

## What auto-fires

1. **`design_conductor.py` hook** detects `/design` → injects 5-stage routing playbook
2. **`build_detector.py` hook** detects "build a landing page" → injects taste-skill baseline (banned fonts, layout rules, motion defaults)

Both fire on the same prompt. No conflict — they layer.

## Routing the conductor will pick

| Stage | Skill invoked | Why |
|-------|---------------|-----|
| **PLAN** | shape (if vibe is unclear) OR skip if brief is sharp | Avoid building toward fuzzy goals |
| **STYLE** | If brand named → design-references (fetch canonical spec). Otherwise → taste-skill + one flavor (soft / brutalist / minimalist / editorial) | One aesthetic, hold the line |
| **BUILD** | frontend-design + framer-motion (for the React animation specifics) | Production-grade implementation |
| **REFINE** | typeset → layout → polish (in that order) | Tighten typography first, rhythm second, micro-detail last |
| **AUDIT** | audit (technical) + critique (UX) | Quality gate before shipping |

## Pre-ship checklist (from taste-skill)

- [ ] No Inter font. Use Geist / Outfit / Cabinet Grotesk / Satoshi
- [ ] No centered H1 hero (use split-screen, left-aligned, or asymmetric)
- [ ] No 3-equal-column card rows (zig-zag, asymmetric grid, or h-scroll)
- [ ] No AI purple/blue neon gradients (zinc/slate base + 1 accent max)
- [ ] No pure #000000 (use Zinc-950 / Off-Black / Charcoal)
- [ ] No `h-screen` (use `min-h-[100dvh]`)
- [ ] No emojis (SVG icons only — Phosphor/Radix)
- [ ] No filler copy ("Elevate", "Seamless", "Unleash", "Next-Gen")
- [ ] All states: loading skeleton, empty state, error state
- [ ] Tactile feedback: `-translate-y-[1px]` or `scale-[0.98]` on `:active`
- [ ] Animations: transform/opacity only (never top/left/width/height)

## After ship

Verify on real devices:
- Lighthouse mobile ≥85
- Touch targets ≥44px
- Contrast 4.5:1 (text), 3:1 (large)
- FCP <2s on 4G
- Works with `prefers-reduced-motion`

## Cost

- Pure local work, $0 in API calls
- If hero images are needed: ~$0.08/image via fal.ai nano-banana-2 (text-heavy) OR free local Flux Krea
- If video hero needed: ~$0.20-0.50/sec via fal.ai Veo 3.1
