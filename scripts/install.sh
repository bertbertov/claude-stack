#!/usr/bin/env bash
# install.sh — set up claude-stack on this machine
#
# - Copies skills/ into ~/.claude/skills/ (skips existing)
# - Copies hooks/ into ~/.claude/hooks/
# - Merges settings.example.json into ~/.claude/settings.json
# - Does NOT install wshobson agents (run scripts/fetch_agents.sh for that)
# - Does NOT modify your .mcp.json (you pick which MCPs to enable yourself)
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"

mkdir -p "$CLAUDE_HOME/skills" "$CLAUDE_HOME/hooks"

echo "▸ Installing skills..."
copied=0
skipped=0
for d in "$REPO_ROOT/skills"/*/; do
  name="$(basename "$d")"
  if [ -d "$CLAUDE_HOME/skills/$name" ]; then
    skipped=$((skipped+1))
    continue
  fi
  cp -r "$d" "$CLAUDE_HOME/skills/$name"
  copied=$((copied+1))
done
echo "  $copied installed, $skipped already present"

echo "▸ Installing hooks..."
for f in "$REPO_ROOT/hooks"/*.py; do
  cp "$f" "$CLAUDE_HOME/hooks/"
done
echo "  $(ls "$REPO_ROOT/hooks"/*.py | wc -l) hooks copied"

echo "▸ Merging settings..."
SETTINGS="$CLAUDE_HOME/settings.json"
EXAMPLE="$REPO_ROOT/settings.example.json"
if [ ! -f "$SETTINGS" ]; then
  cp "$EXAMPLE" "$SETTINGS"
  echo "  Created $SETTINGS"
else
  if command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1; then
    PY="$(command -v python3 || command -v python)"
    "$PY" - "$SETTINGS" "$EXAMPLE" <<'PY'
import json, sys, pathlib
existing_path, example_path = sys.argv[1], sys.argv[2]
existing = json.loads(pathlib.Path(existing_path).read_text())
example  = json.loads(pathlib.Path(example_path).read_text())
# Deep-merge "hooks" by event name
existing.setdefault("hooks", {})
for event, blocks in example["hooks"].items():
    existing["hooks"].setdefault(event, [])
    for block in blocks:
        if block not in existing["hooks"][event]:
            existing["hooks"][event].append(block)
pathlib.Path(existing_path).write_text(json.dumps(existing, indent=2))
print(f"  Merged hooks into existing {existing_path}")
PY
  else
    echo "  python not found — merge $EXAMPLE into $SETTINGS by hand"
  fi
fi

echo ""
echo "✓ Done. Restart Claude Code to activate hooks."
echo ""
echo "Next steps:"
echo "  - For 113 specialist subagents:  ./scripts/fetch_agents.sh"
echo "  - For ccusage (token spend):     npx ccusage@latest"
echo "  - Per-project spec-kit:          uvx --from specify-cli specify init my-project"
