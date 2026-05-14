---
name: skill-compass
description: Audits all installed Claude Code skills for quality, redundancy, and dead weight. Use when the user asks to audit skills, find dead skills, evaluate skill coverage, compare skills, or identify the weakest skill in their library. Runs against ~/.claude/skills/ and surfaces which skills are stale, overlapping, or under-performing.
license: MIT
allowed-tools: Bash, Read
---

# skill-compass — audit your installed skills

A wrapper around the [SkillCompass](https://github.com/Evol-ai/SkillCompass) Node tool installed at `~/.claude/skill-compass/`. Use this skill when the user wants to:

- Find which skills they don't actually use
- Spot redundant/overlapping skills they should consolidate
- Evaluate skill quality with concrete metrics
- Compare two skills against the same task
- Trace why a skill is misfiring

## Commands

The tool exposes its slash-commands at `~/.claude/skill-compass/commands/`:

```
/eval-audit     # full audit of installed skills, scores each
/eval-compare   # head-to-head compare two skills on the same input
/eval-evolve    # iteratively improve a skill based on its own audit
/eval-improve   # one-shot improve a skill
/eval-merge     # merge two overlapping skills into one
```

## Invocation

From a Claude Code session:

```bash
node ~/.claude/skill-compass/oc/run.js audit ~/.claude/skills/<skill-name>
node ~/.claude/skill-compass/oc/run.js audit-all ~/.claude/skills/
```

Or read the SkillCompass `AGENTS.md` and `commands/eval-audit.md` for the full agent-driven flow:

```bash
cat ~/.claude/skill-compass/AGENTS.md
cat ~/.claude/skill-compass/commands/eval-audit.md
```

## When to invoke

- "audit my skills" / "which of my skills are dead weight"
- "are my skills overlapping"
- "score this skill"
- "improve this skill" / "fix this skill"
- After installing 5+ new skills (catch regressions early)

## Why it matters

the user has 200+ skills installed. Without this tool, identifying dead weight is manual eyeballing. SkillCompass produces ranked output with pass/fail signals per skill so the audit produces a punch list, not a wall of text.

## Source

- Repo: https://github.com/Evol-ai/SkillCompass
- Local install: `~/.claude/skill-compass/`
- License: MIT
