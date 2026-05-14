"""UserPromptSubmit hook — fires when the user invokes the design conductor explicitly.

ONLY fires on these intentional command patterns:
  - "design conductor"  (full phrase)
  - "/design"           (slash-style)
  - "design:"           (colon-prefix command)
  - "redesign:"         (colon-prefix command)

Does NOT fire on general design talk — only on the literal command tokens.
On fire, instructs Claude to read SKILL.md at ~/.claude/skills/design-conductor/
and follow its 5-stage routing playbook.
"""
import json, sys, re, os
from pathlib import Path

# Force UTF-8 stdout on Windows
os.environ["PYTHONIOENCODING"] = "utf-8"
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

SKILL_PATH = Path(r"C:\Users\A\.claude\skills\design-conductor\SKILL.md")

# Strict, intentional triggers only — no broad keyword matching.
TRIGGERS = [
    r"\bdesign\s+conductor\b",
    r"(?:^|\s)/design\b",
    r"(?:^|\s)design:\s",
    r"(?:^|\s)redesign:\s",
]
TRIGGER_RE = re.compile("|".join(TRIGGERS), re.IGNORECASE)

def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    prompt = payload.get("prompt", "") or ""
    if not TRIGGER_RE.search(prompt):
        return 0

    if not SKILL_PATH.exists():
        print(f"[design-conductor] SKILL.md missing at {SKILL_PATH}", file=sys.stdout)
        return 0

    skill_body = SKILL_PATH.read_text(encoding='utf-8')

    out = (
        "═══════════════════════════════════════════════════════════════\n"
        "[DESIGN CONDUCTOR — auto-triggered by user prompt]\n"
        "═══════════════════════════════════════════════════════════════\n\n"
        "User invoked the design conductor. BEFORE doing anything else:\n"
        "1. Read the user's task carefully.\n"
        "2. Follow the 5-stage routing playbook below (PLAN → STYLE → BUILD → REFINE → AUDIT).\n"
        "3. Pick ONLY the stages that apply — don't run all 5 by default.\n"
        "4. Announce your routing in the 3-line plan format before starting Stage 1.\n"
        "5. Run sub-skills sequentially, not in parallel. Wait for each stage's output.\n\n"
        "─── DESIGN CONDUCTOR PLAYBOOK ────────────────────────────────\n\n"
        f"{skill_body}\n"
        "═══════════════════════════════════════════════════════════════\n"
    )
    sys.stdout.write(out)
    return 0

if __name__ == "__main__":
    sys.exit(main())
