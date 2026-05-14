---
name: transcript-analyzer
description: Extract structured insights (decisions, action items, opinions, questions, terminology) from any transcript using Cerebras llama-3.3-70b. Use when the user says "extract structured insights from transcripts", "analyze the daytradewarrior transcripts", "what are the decisions in this meeting", "find action items", "build a glossary from this discussion", "summarize key points from this recording", or asks to process meeting/podcast/YouTube/interview transcripts. Outputs markdown with YAML frontmatter, confidence-scored extractions, and incremental glossary.
---

<!--
Adapted from github.com/glebis/claude-skills/transcript-analyzer
(no LICENSE declared in source repo, personal use only — do not redistribute).
Local adaptations by the author 2026-05-07: expanded YAML description with
the user-specific triggers, Cerebras key acquisition note, pointer to local
DaytradeWarrior transcript corpus.
-->

# Transcript Analyzer

## Overview

Analyze meeting / podcast / interview / YouTube transcripts using Cerebras llama-3.3-70b to automatically extract and categorize:
- **Decisions** — explicit agreements or choices made
- **Action Items** — tasks assigned to people
- **Opinions** — viewpoints expressed but not agreed upon
- **Questions** — unresolved questions raised
- **Terms** — domain-specific terminology for incremental glossary

## Prerequisites

### 1. Install dependencies (one-time)

```bash
cd ~/.claude/skills/transcript-analyzer/scripts && npm install
```

### 2. Get a Cerebras API key

Sign up at **https://cloud.cerebras.ai** — there is a free tier with generous limits (this is what makes llama-3.3-70b extraction effectively free for personal use). Create a key in the dashboard, then put it in `scripts/.env`:

```
CEREBRAS_API_KEY=csk-...
```

Reference doc: https://inference-docs.cerebras.ai/

## Usage

```bash
cd ~/.claude/skills/transcript-analyzer/scripts && npm run cli -- <transcript-file> -o <output.md> [options]
```

### Options

| Option | Description |
|--------|-------------|
| `<file>` | Transcript file to analyze (first positional arg) |
| `-o, --output <path>` | Write markdown to file instead of stdout |
| `--include-transcript` | Include full transcript in output [default: off] |
| `--no-extractions` | Exclude extractions section |
| `--no-glossary` | Exclude glossary section |
| `--glossary <path>` | Custom glossary JSON path |
| `--skip-glossary` | Don't preload glossary terms |
| `--max-terms <num>` | Limit glossary suggestions |
| `--chunk-size <num>` | Override chunk size (default: 3000) |

## Examples

### Basic analysis

```bash
cd ~/.claude/skills/transcript-analyzer/scripts && npm run cli -- /path/to/meeting.md -o /path/to/analysis.md
```

### Include original transcript

```bash
cd ~/.claude/skills/transcript-analyzer/scripts && npm run cli -- /path/to/meeting.md -o /path/to/analysis.md --include-transcript
```

### Extractions only (no glossary)

```bash
cd ~/.claude/skills/transcript-analyzer/scripts && npm run cli -- /path/to/meeting.md -o /path/to/analysis.md --no-glossary
```

### Analyze a specific section

```bash
sed -n '50,100p' /path/to/meeting.md > /tmp/section.md
cd ~/.claude/skills/transcript-analyzer/scripts && npm run cli -- /tmp/section.md -o /path/to/section-analysis.md
```

## the user-specific assets

Existing transcript corpora on this machine (point the CLI at any of these or your own paths):

- **451 DaytradeWarrior YouTube transcripts** — bulk-downloaded corpus, ~2M words. Use to extract Warrior's recurring trade rules, setups, risk decisions, and build a strategy glossary. Path lives under `C:\Users\A\Desktop\YouTube\...` (point at the actual transcript files when invoking).
- **MIF book knowledge bases** — 541 books distilled at `C:\Users\A\Desktop\МИФ\_knowledge_bases\`. Useful for opinion / decision extraction across long-form content.
- **Lagarra meeting recordings** — when transcribed, route through this skill before pushing summaries to assistants.

When running against the DaytradeWarrior corpus, prefer `--no-glossary` per-file then merge glossaries at the end (the default `data/glossary.json` is incremental).

## Output Format

The tool generates markdown with:

1. **YAML frontmatter** — processing metadata: chunks processed, extraction counts by type, new terms discovered, model used (llama-3.3-70b via Cerebras), token usage (input / output / total).
2. **Extractions** — categorized findings with confidence scores; each includes speaker (if identified), source snippet, and related terms.
3. **Glossary** — approved terms from the existing glossary plus suggested new terms with definitions.

## Files in this skill

- `scripts/cli.ts` — main CLI entry point
- `scripts/src/lib/extract-service.ts` — AI processing logic using Cerebras
- `scripts/src/lib/markdown.ts` — markdown output generation
- `scripts/src/lib/term-utils.ts` — term deduplication utilities
- `scripts/src/lib/mockExtractor.ts` — mock mode for offline testing
- `scripts/src/lib/utils.ts` — shared helpers
- `scripts/src/types/index.ts` — TypeScript type definitions
- `scripts/data/glossary.json` — default incremental glossary store
- `scripts/package.json`, `scripts/tsconfig.json` — Node/TS config

## Source

Adapted from https://github.com/glebis/claude-skills/tree/main/transcript-analyzer (no license declared — personal use only, do not redistribute).
