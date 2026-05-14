# claude-stack

> A working Claude Code config from a solo builder who ships.

Not another agent megapack. This is the actual setup — skills, hooks, routers, workflows — that runs a one-person shop across web, mobile, video, security, and automation.

**What's different about this stack:**

- **Conductor pattern** — a router skill that decomposes a domain into stages (PLAN → STYLE → BUILD → REFINE → AUDIT) and picks the right sub-skill per stage. Not "200 unranked agents," but a routing layer that knows which tool to reach for.
- **Hooks that enforce, not advise** — auto-trigger skills on intent detection, auto-dedupe new skills, auto-route design work. Not markdown that asks nicely; settings.json plumbing that just fires.
- **Skill + agent + hook integration** — most repos ship one layer. This ships all three working together.
- **Anti-AI-tells tooling** — the `de-ai` humanizer + `taste-skill` design enforcer kill the "looks AI-generated" failure mode in both text and UI.

## Install

```bash
git clone https://github.com/<your-username>/claude-stack ~/claude-stack
cd ~/claude-stack
./scripts/install.sh
```

This copies skills into `~/.claude/skills/`, hooks into `~/.claude/hooks/`, and merges `settings.example.json` into your `~/.claude/settings.json`.

For the optional wshobson agents (113 specialized subagents): `./scripts/fetch_agents.sh`.

## What's inside

```
claude-stack/
├── skills/                   ~140 sanitized SKILL.md files
│   ├── design/               conductor + 12 design sub-skills
│   ├── refinement/           17 single-purpose UI verb skills (adapt, animate, polish, ...)
│   ├── media/                image / video / audio generation pipelines
│   ├── mobile/               Expo + React Native + Android
│   ├── frontend/             GSAP + Framer Motion specialists
│   ├── security/             owasp + pentest + trail-of-bits skills
│   ├── seo/                  full SEO toolkit (22 sub-skills)
│   ├── automation/           n8n + webhooks
│   ├── research/             multi-source research + deep-research
│   ├── quality/              de-ai humanizer + output discipline
│   └── meta/                 skill-compass + mcp-builder
├── hooks/                    6 working hooks
│   ├── build_detector.py     auto-fires taste rules on UI build prompts
│   ├── deploy_agents.py      auto-fires on "deploy agents" trigger
│   ├── design_conductor.py   auto-fires on /design intent
│   ├── skill_dedup_watch.py  auto-detects new skill duplicates at SessionStart
│   ├── post_compact_review.py auto-fires after context compaction
│   └── build_agent_registry.py regenerates the agent index
├── scripts/
│   ├── install.sh            one-command setup
│   ├── fetch_agents.sh       pulls wshobson/agents (optional 113 specialists)
│   └── build_registry.py     generates AGENT_REGISTRY.md
├── workflows/                composed examples
│   ├── ship-a-landing-page.md
│   ├── redesign-an-existing-site.md
│   ├── audit-a-codebase.md
│   ├── build-a-mobile-app.md
│   ├── ship-an-image-pipeline.md
│   └── verify-end-to-end.md
├── docs/
│   ├── CONDUCTOR-PATTERN.md   the routing pattern explained
│   ├── HOOKS-SYSTEM.md        the 6 hooks and what they do
│   └── DEDUP-WATCH.md         auto-dedupe rationale
├── settings.example.json     hook registrations
└── ARCHITECTURE.md            the three-layer model
```

## The three layers

Most Claude Code repos ship one layer. This stack uses three working together:

1. **Skills** (`~/.claude/skills/*/SKILL.md`) — domain knowledge Claude reads when invoking a topic. Markdown only.
2. **Agents** (`~/.claude/agents/*.md`) — subagent personas you dispatch via the Task tool for isolated work. Optional via `fetch_agents.sh`.
3. **Hooks** (`~/.claude/hooks/*.py` + `settings.json`) — Python scripts the harness fires on lifecycle events (UserPromptSubmit, SessionStart, Stop). These ENFORCE behavior the agent might otherwise skip.

See `ARCHITECTURE.md` for how the layers compose, and `docs/CONDUCTOR-PATTERN.md` for the routing pattern that makes the whole thing usable past ~50 skills.

## License

MIT. Use freely, attribution appreciated.

## Credits

- `wshobson/agents` — the 113-specialist subagent collection (fetched separately to avoid duplication)
- `obra/superpowers` — process skills (test-driven-development, systematic-debugging, brainstorming, etc.)
- `trailofbits/skills` — security audit skills
- `anthropics/skills` — first-party patterns
- Individual skill authors — credited in their `SKILL.md` frontmatter where known
