# Hooks System

Hooks are Python scripts the Claude Code harness fires on lifecycle events. Unlike skills (which advise Claude), hooks **enforce** behavior regardless of what the agent decides.

## The 6 hooks

### 1. `deploy_agents.py` (UserPromptSubmit)
Fires when prompt matches `deploy agents` / `spawn agents` / `fire agents` / `deploy a swarm`. Injects the agent registry + dispatch protocol so Claude picks 3-7 relevant agents and dispatches them in parallel via the `Task` tool. No-op for other prompts.

**Why:** Without this, you'd have to remember which agents exist and dispatch them manually. The hook auto-surfaces the registry.

### 2. `design_conductor.py` (UserPromptSubmit)
Fires on explicit triggers only: `design conductor`, `/design`, `design:`, `redesign:`. Injects the design-conductor SKILL.md body so Claude follows the 5-stage routing playbook (PLAN → STYLE → BUILD → REFINE → AUDIT).

**Why:** Routes design work through a single canonical playbook so output is consistent across sessions.

### 3. `build_detector.py` (UserPromptSubmit)
Fires on any prompt combining a build verb (build, create, make, design, refactor) + a UI noun (landing page, dashboard, component, modal, app, site, etc). Injects the taste-skill baseline (banned fonts, layout rules, motion defaults) without needing an explicit `/design` trigger.

**Why:** Catches the 80% case where the user wants UI work but doesn't say "design conductor." Auto-baselines the build.

### 4. `skill_dedup_watch.py` (SessionStart)
Runs on every session start in <1 second. Compares the current skill set against a baseline stored at `~/.claude/skills/_audit_state.json`. Silent if nothing changed. If new skills were added AND any have ≥60% description-keyword overlap with existing skills, injects a warning with the suspected duplicate pairs.

**Why:** Catches "you just installed a skill that duplicates one you already have" before it becomes confusion. Auto-runs without you having to remember to audit.

### 5. `post_compact_review.py` (SessionStart, matcher: compact)
Fires after a context-compaction event. Re-reads recent decisions from project memory so the agent doesn't fabricate facts from fuzzy post-compaction recall.

**Why:** Compaction is a known footgun — the agent confabulates numbers/decisions after compression. This hook forces a fact-anchored restart.

### 6. `build_agent_registry.py` (manual, not a hook)
Standalone script. Walks `~/.claude/agents/` and generates `AGENT_REGISTRY.md` with one-line descriptions per agent. Run after `fetch_agents.sh` to rebuild the index.

## Event reference

| Event | When | Hooks in this stack |
|-------|------|--------------------|
| `UserPromptSubmit` | Every user message before Claude responds | deploy_agents, design_conductor, build_detector |
| `SessionStart` | Session begin / resume | skill_dedup_watch |
| `SessionStart` (compact matcher) | After context compaction | post_compact_review |
| `Stop` | Agent attempts to end turn | (optional: taskmaster, not in this repo by default) |
| `PreToolUse` | Before any tool call | (optional: spawn budget, observability) |
| `PostToolUse` | After any tool call | (optional: audit trail) |

## Adding a new hook

1. Write the Python script under `hooks/<name>.py`. Read JSON payload from stdin, write output to stdout (the harness injects stdout into Claude's context).
2. Add the registration to `settings.example.json`:
```json
{
  "hooks": {
    "<EventName>": [
      {
        "hooks": [
          { "type": "command", "command": "python ~/.claude/hooks/<name>.py", "timeout": 5 }
        ]
      }
    ]
  }
}
```
3. Re-run `./scripts/install.sh` to merge.
4. Restart Claude Code.

## Hook design rules

- **Fail silent.** If your hook crashes, the session shouldn't die. Wrap in try/except, exit 0 on error.
- **Be fast.** Hooks fire on every event — keep them under 1 second. The `timeout` in settings.json is a hard cap, not a target.
- **Don't write to the conversation unless triggered.** Match a specific pattern, then write. Otherwise stay silent.
- **Idempotent.** Running the hook twice on the same input should produce the same output.

## How to disable a hook temporarily

Comment out the entry in `~/.claude/settings.json` or rename the hook file with a `.disabled` suffix. The harness silently skips missing/invalid entries.
