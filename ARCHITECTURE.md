# Architecture

claude-stack runs on **three layers** working together. Most Claude Code repos ship one. The interesting behavior emerges from the composition.

## The three layers

### Layer 1 — Skills (`~/.claude/skills/<name>/SKILL.md`)

Markdown files Claude reads when invoking a topic. Pure knowledge — no code execution. YAML frontmatter declares `name`, `description`, and discovery triggers; body is the playbook.

**Used for:** domain expertise (taste-skill, de-ai, react-native-apps), routers (design-conductor), tool wrappers (find-models, prompt-images), refinement verbs (adapt, polish, harden).

### Layer 2 — Agents (`~/.claude/agents/<name>.md`) — optional via `fetch_agents.sh`

Subagent personas dispatched via the `Task` tool. Each agent runs in isolation with its own context window and persona, so the main conversation stays clean.

**Used for:** parallel research, isolated code review, specialized roles (security-auditor, frontend-developer, backend-architect).

### Layer 3 — Hooks (`~/.claude/hooks/<name>.py` + `settings.json`)

Python scripts the Claude Code harness fires on lifecycle events:

| Event | When it fires | What this stack does |
|-------|---------------|---------------------|
| `UserPromptSubmit` | Every user message | Detect intent, inject context |
| `SessionStart` | Session begin/resume | Check for new skill duplicates, post-compact recovery |
| `Stop` | Agent attempts to end turn | Block stop until completion is proven (taskmaster) |
| `PostToolUse` | After a tool runs | Audit trail (optional, via observability hooks) |

Hooks are the **enforcement layer**. Skills *advise* Claude; hooks *make Claude do something* regardless of whether Claude was going to.

## How the layers compose

### Example: "build a landing page"

1. **Hook fires** (`build_detector.py`) — pattern-matches "build" + UI noun → injects taste-skill rules into context
2. **Claude reads the injected rules** — banned fonts, layout constraints, motion defaults
3. **Skill invoked** (taste-skill) — full anti-LLM-bias playbook
4. **If brand mentioned** (e.g., "Stripe-style") — design-references skill fetches the canonical brand spec
5. **Code written** — Claude applies skills + rules to the actual build
6. **Stop hook fires** (taskmaster, if installed) — checks the work was verified before allowing the turn to end

No single layer accomplishes this alone. The hook fires automatically (skill discovery isn't guaranteed). The skill carries the deep knowledge (a hook can't hold a 400-line playbook). The Stop hook closes the loop (skills can't enforce verification, only describe it).

## The conductor pattern (key IP)

Most agent collections give you 200 unranked tools and let you guess which to use. This stack uses a **router skill** that:

1. Takes any task in a domain
2. Decomposes the domain into stages (e.g., design = PLAN → STYLE → BUILD → REFINE → AUDIT)
3. Picks ONLY the stages that apply to this specific task
4. Dispatches the canonical sub-skill per stage
5. Chains outputs

See `docs/CONDUCTOR-PATTERN.md` for the design-conductor implementation. The same pattern can spawn:
- `research-conductor` (gather → verify → synthesize → cite)
- `deploy-conductor` (plan → build → test → ship → monitor)
- `content-conductor` (brief → outline → draft → humanize → audit)
- `audit-conductor` (collect → analyze → flag → prioritize → report)

## Auto-dedupe (`skill_dedup_watch.py`)

Runs every SessionStart in under 1 second. Compares the current skill set against a persisted baseline (`_audit_state.json`). If new skills were added AND any have ≥60% description-keyword overlap with existing skills, injects a warning into Claude's context with the suspected pairs.

Silent when nothing changed. Catches "you just installed a skill that overlaps something you already have" before it becomes confusion.

## Settings layout

`settings.example.json` shows the hook registrations. Merge into `~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [/* 3 hooks chained */],
    "SessionStart": [/* dedup-watch + post-compact-review */],
    "Stop": [/* taskmaster — optional, enforces verify-before-completion */]
  }
}
```

The install script handles the merge.

## What this stack deliberately doesn't try to do

- **Vendor lock-in** — no required MCP, no required cloud service
- **One-size-fits-all** — each skill is ~50-200 lines, atomic, composable
- **Replace your judgment** — these are leverage tools, not autopilots
- **Ship secrets** — `.gitignore` blocks `.env`, `KEYS.env`, `memory/`, `projects/`

## What you bring

A working Claude Code install. That's it. The stack assumes you're a senior solo builder who wants enforced discipline (hooks), reachable expertise (skills), and parallel scaling (agents) — not someone learning Claude Code for the first time.
