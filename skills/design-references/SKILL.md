---
name: design-references
description: Fetch brand-specific DESIGN.md system specs from getdesign.md when the user wants UI to match a known brand's aesthetic ("make it look like Stripe", "Apple-style", "Linear feel"). Covers 59 brands across SaaS, fintech, consumer tech, automotive, AI labs, and creator tools. Use BEFORE picking a generic style skill — brand match always beats generic.
---

# Design References — 59 brand DESIGN.md specs

When the user references a brand by name, fetch that brand's DESIGN.md instead of using a generic style skill (taste-skill, soft-skill, etc.). Brand-match always beats generic.

## How to use

1. User says "make it look like X" / "X-style" / "X feel" / "match Stripe's aesthetic" → look up brand below
2. Fetch the spec via WebFetch:
   ```
   https://getdesign.md/design-md/<brand>/DESIGN.md
   ```
3. Apply that spec as the source of truth for tokens, typography, motion, and components.
4. If the user names a brand NOT in this list, fall back to taste-skill / ui-ux-pro-max + the user's description.

## Available brands (59)

### SaaS / Dev tools
`airtable` · `cal` · `clickhouse` · `composio` · `cursor` · `expo` · `figma` · `framer` · `hashicorp` · `intercom` · `linear.app` · `lovable` · `mintlify` · `miro` · `mongodb` · `notion` · `opencode.ai` · `posthog` · `raycast` · `replicate` · `resend` · `sanity` · `semrush` · `sentry` · `supabase` · `superhuman` · `vercel` · `voltagent` · `warp` · `webflow` · `zapier`

### AI labs / models
`claude` · `cohere` · `elevenlabs` · `minimax` · `mistral.ai` · `nvidia` · `ollama` · `runwayml` · `together.ai` · `x.ai`

### Fintech / payments
`coinbase` · `kraken` · `revolut` · `stripe` · `wise`

### Consumer / lifestyle
`airbnb` · `apple` · `pinterest` · `spotify` · `uber`

### Automotive / hardware
`bmw` · `clay` · `ferrari` · `lamborghini` · `renault` · `spacex` · `tesla`

### Enterprise / infra
`ibm`

## Quick brand → vibe map

| Brand | Use for |
|-------|---------|
| **stripe** | Premium fintech, purple gradients, weight-300 elegance |
| **apple** | Consumer hardware, SF Pro, cinematic imagery, generous whitespace |
| **linear.app** | Software/SaaS, dark, neutral, ultra-precise spacing |
| **vercel** | Dev tools, Geist font, monochrome with electric accent |
| **claude** | AI products, warm/editorial, soft serif |
| **cursor** | Code editors, dark, tight sans, syntax-highlight palette |
| **notion** | Productivity, soft cream, warm blacks, friendly |
| **figma** | Creative tools, vibrant accents on neutral |
| **coinbase** | Crypto/finance, blue trust, clean grids |
| **airbnb** | Marketplace, photographic-first, soft shadows |
| **superhuman** | Email/productivity, dense, mono-adjacent |
| **raycast** | Launcher/utility, dark, command-palette aesthetic |
| **tesla** | Premium hardware, minimal/black, technical |
| **ferrari / lamborghini** | Luxury automotive, red/black, cinematic |
| **resend** | Dev/email, Geist + clean grayscale |
| **runwayml** | AI creative, experimental, dark + saturated |
| **posthog** | Analytics, hedgehog-quirky, friendly serious |
| **mintlify** | Docs, clean technical |
| **wise** | Banking, green/cream, friendly trust |

(For brands not in the table, just fetch the DESIGN.md — each starts with a one-line description.)

## What's in each DESIGN.md

Every spec contains tokens for:
- Color palette (semantic + raw)
- Typography (font stacks, scale, weights)
- Spacing scale + grid
- Motion / easing curves
- Border radius scale
- Shadows / elevation
- Component patterns (buttons, cards, nav)
- Brand voice / tone notes

Sizes range from ~20 KB (Stripe) to ~37 KB (Apple).

## Local mirror (offline reference, stub-only)

`C:\Users\A\.claude\design-references\awesome-design-md\design-md\<brand>\README.md`

These are stubs that point to the canonical URL. The actual content lives at getdesign.md.

## Routing rule

When invoked, the design-conductor stage 2 (STYLE) should prefer this skill over generic style picks if a brand match exists. Otherwise fall through to taste-skill / soft-skill / brutalist-skill / etc.
