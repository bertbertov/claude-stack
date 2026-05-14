# Skill Dedup Watch

Auto-detects new skill duplicates at the start of every session.

## Why this exists

You install skills over time. After 50+ skills, you start forgetting what you have. When a new skill arrives that duplicates something you already installed (which happens constantly in the Claude Code ecosystem — there are 5 different "anti-AI-slop frontend" skills), the agent gets confused about which to invoke and consistency erodes.

The dedup-watch hook catches this automatically.

## Mechanism

`hooks/skill_dedup_watch.py` runs on every `SessionStart` event:

1. Walks `~/.claude/skills/<name>/SKILL.md` for every active skill (skips `_archive/`, `_audit_state.json`, broken entries).
2. Parses YAML frontmatter, extracts `name` + `description`.
3. Compares the current skill list against the persisted baseline at `~/.claude/skills/_audit_state.json`.
4. **Silent if nothing changed.** Zero noise.
5. If new skills were added since last session, AND any new skill has ≥60% description-keyword overlap with existing skills, prints a warning to stdout.
6. Updates the baseline with the new skill set.

The warning gets injected into the agent's context. At the start of the next conversation, the agent sees:

```
================================================================
[SKILL-DEDUPE-WATCH — auto-triggered]
================================================================

2 new skill(s) added since last session: foo-skill, bar-skill
1 potential duplicate pair(s) detected (>=60% description overlap):

  [HIGH] foo-skill  <->  existing-foo-skill  (87%)

Action for Claude:
  - At natural conversation pause, surface this list to user.
  - For HIGH (>=85%) pairs, suggest archiving the duplicate.
  - For CHECK pairs, ask user before any retire decision.
  - Archive moves go to ~/.claude/skills/_archive/ (revertible).
================================================================
```

## Tunables

In `hooks/skill_dedup_watch.py`:

| Constant | Default | What it controls |
|----------|---------|-----------------|
| `DUPE_THRESHOLD` | 0.60 | Min description-keyword Jaccard overlap to flag |
| `AUTO_ARCHIVE_THRESHOLD` | 0.85 | What counts as "HIGH" confidence (the agent suggests archive) |
| `MAX_REPORTED` | 8 | Cap on warnings per session (avoids spam if a megapack installs 50 skills) |

Lower `DUPE_THRESHOLD` = more aggressive flagging.
Raise `AUTO_ARCHIVE_THRESHOLD` = fewer auto-archive suggestions.

## The Jaccard math

For each pair of skills, the hook computes:

```
overlap = |words(desc_A) ∩ words(desc_B)|  /  |words(desc_A) ∪ words(desc_B)|
```

Where `words()` extracts ≥4-letter content words (stopwords filtered).

This is a cheap, deterministic test that takes <1ms per pair. For 200 skills that's 20k pairs ≈ <100ms.

## What it does NOT do

- **Semantic similarity via embeddings.** Would require an LLM call or local model. Trade-off: cheap-but-keyword vs slow-but-meaning-aware. Keyword Jaccard catches the ~85% case (overlapping topic words) and stays out of your way.
- **Auto-archive.** It only warns. You decide whether to archive. The agent will surface the pairs and ask before moving anything.
- **Cross-namespace dedup.** It only checks `~/.claude/skills/` top-level dirs. Plugin-bundled skills (`superpowers:*`, `analysis:*`, etc) are out of scope.

## False positives to expect

- **Sibling skills in the same family.** `gsap-core`, `gsap-react`, `gsap-scrolltrigger` all overlap on "gsap animation framework" keywords. They're not duplicates — they're domain-specific. Mark them as "not a dupe" by ignoring the warning; they'll keep flagging on every new install. Future enhancement: per-skill exclusion list in `_audit_state.json`.
- **Refinement verbs** (adapt, animate, polish, distill) all overlap on "improve / fix / refine UI" keywords. Not duplicates — atomic verbs. Ignore.

## Reset

Delete `~/.claude/skills/_audit_state.json` to reset the baseline. Next session start re-seeds from current state and won't fire any warnings until you install something new.

## Why "watch" and not "compass"

This stack ships `skill-compass` (a separate skill) which is a manual on-demand audit. Dedup-watch is the automatic background version. You don't run dedup-watch; it runs you. Skill-compass is what you invoke when you want a full report on demand.
