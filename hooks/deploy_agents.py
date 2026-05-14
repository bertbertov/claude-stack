"""UserPromptSubmit hook — fires when the user says "deploy agents".

When triggered, injects:
  1. The full AGENT_REGISTRY contents
  2. An instruction telling Claude to pick 3-7 most relevant agents from the registry
     and dispatch them in parallel via the Agent tool (single message, multiple tool uses).

Trigger phrases (case-insensitive, substring match):
  - "deploy agents"
  - "deploy a swarm"
  - "spawn agents"
  - "fire agents"

If trigger NOT found, the hook outputs nothing → no behavior change.
If trigger found, the hook prints additionalContext to stdout that Claude sees.
"""
import json, sys, re, os
from pathlib import Path

# Force UTF-8 stdout on Windows so box-drawing chars in the registry don't crash cp1252
os.environ["PYTHONIOENCODING"] = "utf-8"
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

REGISTRY = Path(r"C:\Users\A\.claude\AGENT_REGISTRY.md")
TRIGGERS = [
    r"\bdeploy\s+agents?\b",
    r"\bdeploy\s+a\s+swarm\b",
    r"\bspawn\s+agents?\b",
    r"\bfire\s+agents?\b",
]
TRIGGER_RE = re.compile("|".join(TRIGGERS), re.IGNORECASE)

def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # malformed, do nothing

    prompt = payload.get("prompt", "") or ""
    if not TRIGGER_RE.search(prompt):
        return 0  # no trigger, exit cleanly

    if not REGISTRY.exists():
        # Don't break Claude — just emit a clear note
        print("[deploy-agents] AGENT_REGISTRY.md is missing. "
              "Run: python ~/.claude/hooks/build_agent_registry.py", file=sys.stdout)
        return 0

    registry = REGISTRY.read_text(encoding='utf-8')

    # Inject as additionalContext via stdout — Claude Code surfaces this to the model.
    out = (
        "═══════════════════════════════════════════════════════════════\n"
        "[DEPLOY AGENTS — auto-triggered by user prompt]\n"
        "═══════════════════════════════════════════════════════════════\n\n"
        "The user used a 'deploy agents' trigger phrase. Follow this protocol:\n\n"
        "1. Read the user's task carefully (everything around/after the trigger phrase).\n"
        "2. Pick 3-7 agents from the registry below whose descriptions BEST match the task.\n"
        "   Prefer specialists over generalists. Diverse skills beat duplicates.\n"
        "3. Dispatch them IN PARALLEL using the Agent tool — a SINGLE message with MULTIPLE\n"
        "   Agent tool calls so they run concurrently (this is the whole point).\n"
        "4. Give each agent a self-contained, well-scoped prompt with the context it needs.\n"
        "   Tell each agent whether to research/report or to actually write code.\n"
        "5. After all agents return, synthesize their outputs for the user.\n\n"
        "Use the `subagent_type` parameter on each Agent call to select the agent. The\n"
        "subagent_type must match a name from the registry below. If the perfect agent\n"
        "isn't there, fall back to `general-purpose`.\n\n"
        "─── AGENT REGISTRY ───────────────────────────────────────────\n\n"
        f"{registry}\n"
        "═══════════════════════════════════════════════════════════════\n"
    )
    sys.stdout.write(out)
    return 0

if __name__ == "__main__":
    sys.exit(main())
