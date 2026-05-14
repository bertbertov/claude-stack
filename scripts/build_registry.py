#!/usr/bin/env python3
"""Build a flat AGENT_REGISTRY.md index of every agent installed in ~/.claude/agents/

Reads YAML frontmatter (name + description) from each *.md file. Groups by
parent directory so the source is traceable.

Output goes to ~/.claude/AGENT_REGISTRY.md by default, or stdout if --stdout.
"""
import argparse
import re
from pathlib import Path

CLAUDE_HOME = Path.home() / ".claude"
AGENTS_DIR = CLAUDE_HOME / "agents"
OUTPUT_FILE = CLAUDE_HOME / "AGENT_REGISTRY.md"


def parse_frontmatter(md: Path) -> tuple[str | None, str]:
    try:
        text = md.read_text(encoding="utf-8", errors="ignore")[:2000]
    except Exception:
        return None, ""
    if not text.startswith("---"):
        return None, ""
    end = text.find("\n---", 4)
    if end == -1:
        return None, ""
    fm = text[3:end]
    name_m = re.search(r"^\s*name:\s*(.+)$", fm, re.M)
    desc_m = re.search(r"^\s*description:\s*(.+?)(?=\n[a-z_]+:|\Z)", fm, re.M | re.S)
    name = name_m.group(1).strip().strip('"\'') if name_m else None
    desc = (
        desc_m.group(1).strip().strip('"\'')[:200] + "..."
        if desc_m and len(desc_m.group(1).strip()) > 200
        else (desc_m.group(1).strip().strip('"\'') if desc_m else "")
    )
    return name, desc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stdout", action="store_true", help="Print to stdout")
    args = parser.parse_args()

    if not AGENTS_DIR.exists():
        print(f"No agents directory at {AGENTS_DIR}")
        return

    groups: dict[str, list[tuple[str, str]]] = {}
    for md in sorted(AGENTS_DIR.rglob("*.md")):
        name, desc = parse_frontmatter(md)
        if not name:
            continue
        # Group by parent dir name relative to AGENTS_DIR
        rel = md.relative_to(AGENTS_DIR)
        group = rel.parts[0] if len(rel.parts) > 1 else "root"
        groups.setdefault(group, []).append((name, desc))

    total = sum(len(items) for items in groups.values())

    lines: list[str] = []
    lines.append("# Agent Registry\n")
    lines.append(f"Auto-generated index of {total} agents under `~/.claude/agents/`.\n")
    lines.append("Grouped by source folder.\n")
    for group, items in sorted(groups.items()):
        lines.append(f"\n## {group} ({len(items)})\n")
        for name, desc in sorted(items):
            short = desc[:140] + "..." if len(desc) > 140 else desc
            lines.append(f"- **{name}** — {short}")

    output = "\n".join(lines) + "\n"
    if args.stdout:
        print(output)
    else:
        OUTPUT_FILE.write_text(output, encoding="utf-8")
        print(f"Wrote {total} agents → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
