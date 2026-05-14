#!/usr/bin/env bash
# fetch_agents.sh — optional wshobson/agents installer
#
# Pulls the 113 specialist subagents from wshobson/agents into
# ~/.claude/agents/wshobson/. Idempotent — re-run anytime to update.
#
set -euo pipefail

CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
TARGET="$CLAUDE_HOME/agents/wshobson"

mkdir -p "$CLAUDE_HOME/agents"

if [ -d "$TARGET/.git" ]; then
  echo "▸ Updating existing wshobson agents..."
  cd "$TARGET" && git pull --ff-only
else
  echo "▸ Cloning wshobson/agents..."
  rm -rf "$TARGET"
  git clone --depth 1 https://github.com/wshobson/agents "$TARGET"
fi

count=$(find "$TARGET" -name "*.md" -maxdepth 2 | wc -l)
echo "✓ $count agent files now in $TARGET"
echo ""
echo "Regenerate the agent registry:"
echo "  python $CLAUDE_HOME/hooks/build_agent_registry.py"
