"""Build AGENT_REGISTRY.md by scanning every .claude/agents/**/*.md frontmatter.

Sources scanned:
  - ~/.claude/agents/wshobson/*.md (just imported)
  - ruflo's bundled @claude-flow/cli agents
  - ruflo's bundled agentic-flow agents

Output: ~/.claude/AGENT_REGISTRY.md — one line per agent, used by the deploy-agents hook.
"""
import os, re, sys
from pathlib import Path

ROOTS = [
    Path(r"C:\Users\A\.claude\agents"),
    Path(r"C:\Users\A\AppData\Roaming\npm\node_modules\ruflo\node_modules\@claude-flow\cli\.claude\agents"),
    Path(r"C:\Users\A\AppData\Roaming\npm\node_modules\ruflo\node_modules\agentic-flow\.claude\agents"),
]

OUT = Path(r"C:\Users\A\.claude\AGENT_REGISTRY.md")
FRONTMATTER = re.compile(r'^---\s*\n(.*?)\n---', re.DOTALL)

def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER.match(text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, _, v = line.partition(':')
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out

agents = {}  # name -> (description, source)

for root in ROOTS:
    if not root.exists():
        continue
    rs = str(root)
    if 'agentic-flow' in rs:
        source_label = 'agentic-flow'
    elif '@claude-flow' in rs:
        source_label = 'claude-flow'
    elif r'A\.claude\agents' in rs:  # user's own .claude/agents folder
        source_label = 'user'
    else:
        source_label = 'unknown'

    for md in root.rglob("*.md"):
        try:
            text = md.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        fm = parse_frontmatter(text)
        name = fm.get('name', md.stem)
        desc = fm.get('description', '').strip()
        if not desc:
            # take first non-frontmatter paragraph
            body = FRONTMATTER.sub('', text).strip()
            first = body.split('\n\n', 1)[0][:200] if body else ''
            desc = first
        # only first occurrence wins (first source listed has priority)
        if name not in agents:
            agents[name] = (desc[:300], source_label)

# Group by source for readability
groups = {'user': [], 'claude-flow': [], 'agentic-flow': [], 'unknown': []}
for name, (desc, source) in agents.items():
    groups.setdefault(source, []).append((name, desc))

lines = ["# Agent Registry",
         "",
         f"Auto-generated index of {len(agents)} agents available via the Agent tool.",
         "Sources: ~/.claude/agents (wshobson imports), bundled @claude-flow/cli, bundled agentic-flow.",
         "",
         "Used by the `deploy-agents` UserPromptSubmit hook to surface candidates when you say 'deploy agents <task>'.",
         ""]

for source in ['user', 'claude-flow', 'agentic-flow', 'unknown']:
    items = sorted(groups.get(source, []))
    if not items:
        continue
    lines.append(f"## {source} ({len(items)})")
    lines.append("")
    for name, desc in items:
        # one-liner, truncate description
        short = desc.replace('\n', ' ').strip()
        if len(short) > 140:
            short = short[:137] + "..."
        lines.append(f"- **{name}** — {short}")
    lines.append("")

OUT.write_text('\n'.join(lines), encoding='utf-8')
print(f"Wrote {OUT}: {len(agents)} agents across {sum(1 for v in groups.values() if v)} sources")
for source, items in groups.items():
    print(f"  {source}: {len(items)}")
