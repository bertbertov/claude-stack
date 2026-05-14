# The Conductor Pattern

> Why "200 unranked agents" fails, and what to do instead.

## The problem with agent megapacks

Most Claude Code skill/agent collections give you 200 tools with no routing logic. You're expected to know which to invoke for "build a landing page" vs "redesign an existing site" vs "audit a codebase." In practice the agent picks the first plausible match and you get inconsistent results.

The conductor pattern solves this by **separating routing from execution**:

1. A **conductor skill** owns a domain (design, research, content, deployment, audit).
2. The domain is decomposed into **stages** (4-6 typical).
3. The conductor reads the task and picks ONLY the stages that apply.
4. Per stage, the conductor knows the **canonical sub-skill** to dispatch.
5. Sub-skills are atomic and chained — never merged.

## Concrete example: design-conductor

The shipped `design-conductor` skill routes all UI/UX work through 5 stages:

```
PLAN  →  STYLE  →  BUILD  →  REFINE  →  AUDIT
```

### Stage breakdown

| Stage | Question | Sub-skills available |
|-------|----------|---------------------|
| **PLAN** | Do we have a brief? | shape, critique, redesign-skill |
| **STYLE** | Which aesthetic? | taste-skill, soft-skill, brutalist-skill, minimalist-skill, emil-design-eng, ui-ux-pro-max, design-references (brand match) |
| **BUILD** | Implementation specialist? | frontend-design, framer-motion, gsap-*, mck-ppt-design, email-html-mjml, react-native-apps |
| **REFINE** | One-shot improvements? | adapt, animate, bolder, clarify, colorize, delight, distill, harden, layout, optimize, overdrive, polish, quieter, typeset |
| **AUDIT** | Quality gate? | audit, critique |

### Routing rules

1. **Don't run all 5 stages by default.** "Make this button less bland" = REFINE only. "Build a landing page" = PLAN + STYLE + BUILD + AUDIT. "Audit the app" = AUDIT only.
2. **Don't merge sub-skills.** Pick ONE per stage, chain them sequentially.
3. **Brand match beats vibe.** If the user names a brand ("Stripe-style"), invoke design-references and fetch the canonical spec instead of picking a flavor.
4. **Announce the routing before executing.** Tell the user "Running stages X, Y, Z with sub-skills A, B, C — say redirect if wrong."

## The hook that makes it automatic

`hooks/design_conductor.py` is a UserPromptSubmit hook that detects explicit triggers (`/design`, `design:`, `design conductor`) and injects the routing playbook into context. So you don't have to remember to invoke it.

For implicit triggers (any "build / create / make a UI" prompt), `hooks/build_detector.py` fires the lighter `taste-skill` rules so even non-explicit design work gets baselined.

## How to spawn other conductors

The pattern generalizes. To build (for example) a `research-conductor`:

1. **Identify the stages** (4-6): GATHER → VERIFY → SYNTHESIZE → CITE → REPORT
2. **List the canonical sub-skill per stage:**
   - GATHER → deep-research-enterprise or deer-flow
   - VERIFY → fact-checking sub-skill (write or repurpose)
   - SYNTHESIZE → token-efficient + output-skill
   - CITE → citation-formatter (skill to write)
   - REPORT → structured-report (skill to write)
3. **Write the conductor SKILL.md** with the 5-stage table and routing rules.
4. **Optionally write a UserPromptSubmit hook** that auto-fires on `/research` or `research:` triggers.

## Other domains that benefit

| Conductor | Stages | When |
|-----------|--------|------|
| `deploy-conductor` | plan → build → test → ship → monitor | Production code changes |
| `content-conductor` | brief → outline → draft → humanize → audit | Long-form writing |
| `audit-conductor` | collect → analyze → flag → prioritize → report | Code/security/perf audits |
| `data-conductor` | profile → clean → model → validate → ship | Data pipelines |
| `pr-conductor` | review → request-changes → approve → merge → followup | Code review workflows |

## Why this beats "just pick the right agent"

When you have 200 agents, "just pick the right one" requires you to remember which is canonical for each stage. Over time you forget, the agent's description drifts, similar tools appear, and consistency erodes.

The conductor pattern fixes this by **freezing the routing decision once** in the conductor SKILL.md. Updates to sub-skills don't change the routing. New sub-skills get added to the conductor's table, not as parallel paths the agent has to choose between.

## Trade-off

Conductor skills are slightly longer (200-400 lines) than typical sub-skills (50-150 lines) because they encode the routing logic. The trade is one bigger skill that's load-bearing vs many ad-hoc invocations that vary.

For domains you touch often, write the conductor. For one-offs, just call the sub-skill directly.
