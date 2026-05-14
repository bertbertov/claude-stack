"""UserPromptSubmit hook — auto-injects taste-skill rules when user is building UI.

Fires when the prompt contains a BUILD VERB + UI NOUN combination.
Injects the critical taste-skill rules (forbidden patterns + baseline config)
so Claude applies them without being explicitly asked.

Does NOT fire on backend, API, DB, script, or infra work.
Does NOT fire if design-conductor was already triggered (to avoid doubling up).
"""
import json, sys, re, os
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SKILL_PATH = Path(r"C:\Users\A\.claude\skills\taste-skill\SKILL.md")

BUILD_VERBS = [
    r"\bbuild\b", r"\bcreate\b", r"\bmake\b", r"\bdesign\b",
    r"\brebuild\b", r"\bimplement\b", r"\bdevelop\b", r"\brefactor\b",
    r"\breadd\b", r"\breed(?:sign|esign)\b", r"\bupdate\b", r"\bimprove\b",
    r"\badd\b", r"\bfix\b",
]

UI_NOUNS = [
    r"\blanding[\s-]page\b", r"\bdashboard\b", r"\bwebsite\b", r"\bweb[\s-]app\b",
    r"\bmobile[\s-]app\b", r"\bcomponent\b", r"\bscreen\b", r"\blayout\b",
    r"\bhero\b", r"\bcard\b", r"\bmodal\b", r"\bnavbar\b", r"\bnavigation\b",
    r"\bsidebar\b", r"\bheader\b", r"\bfooter\b", r"\bform\b", r"\bbutton\b",
    r"\bui\b", r"\bfrontend\b", r"\bfront[\s-]end\b", r"\bpage\b",
    r"\bsection\b", r"\bpanel\b", r"\btable\b", r"\blist\b", r"\bgrid\b",
    r"\bapp\b", r"\bsite\b", r"\binterface\b", r"\bstyle\b", r"\btheme\b",
]

# Don't double-fire if design-conductor already picked it up
DESIGN_CONDUCTOR_TRIGGERS = [
    r"\bdesign\s+conductor\b", r"(?:^|\s)/design\b",
    r"(?:^|\s)design:\s", r"(?:^|\s)redesign:\s",
]

# Skip clearly non-UI work
SKIP_PATTERNS = [
    r"\bapi\b", r"\bbackend\b", r"\bserver\b", r"\bdatabase\b", r"\bsql\b",
    r"\bmigration\b", r"\bcron\b", r"\bscript\b", r"\bpipeline\b",
    r"\bworkflow\b", r"\bwebhook\b", r"\bcicd\b", r"\bdocker\b",
]

VERB_RE = re.compile("|".join(BUILD_VERBS), re.IGNORECASE)
NOUN_RE = re.compile("|".join(UI_NOUNS), re.IGNORECASE)
SKIP_RE = re.compile("|".join(SKIP_PATTERNS), re.IGNORECASE)
CONDUCTOR_RE = re.compile("|".join(DESIGN_CONDUCTOR_TRIGGERS), re.IGNORECASE)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    prompt = payload.get("prompt", "") or ""

    # Don't fire if design-conductor already handling it
    if CONDUCTOR_RE.search(prompt):
        return 0

    # Skip clearly non-UI prompts
    if SKIP_RE.search(prompt) and not NOUN_RE.search(prompt):
        return 0

    # Must have a build verb AND a UI noun
    if not VERB_RE.search(prompt) or not NOUN_RE.search(prompt):
        return 0

    out = (
        "================================================================\n"
        "[TASTE-SKILL — auto-triggered: UI build detected]\n"
        "================================================================\n\n"
        "Active baseline: DESIGN_VARIANCE=8  MOTION_INTENSITY=6  VISUAL_DENSITY=4\n\n"
        "FORBIDDEN (AI tells to avoid):\n"
        "- Font: NO Inter. Use Geist, Outfit, Cabinet Grotesk, or Satoshi\n"
        "- Layout: NO centered H1 hero. Use split-screen, left-aligned, or asymmetric\n"
        "- Cards: NO 3-equal-column card rows. Use zig-zag, asymmetric grid, or h-scroll\n"
        "- Color: NO AI purple/blue neon gradients. Zinc/Slate base + 1 accent max\n"
        "- Color: NO pure #000000. Use Zinc-950 / Off-Black / Charcoal\n"
        "- Sizing: NEVER h-screen. Always min-h-[100dvh]\n"
        "- Emojis: BANNED everywhere. Use SVG icons (Phosphor/Radix)\n"
        "- Copy: NO 'Elevate', 'Seamless', 'Unleash', 'Next-Gen'. Use concrete verbs\n"
        "- Data: NO 99.99%, round numbers. Use organic data (47.2%, +1 (312) 847-1928)\n"
        "- External images: NO Unsplash. Use picsum.photos/seed/{str}/800/600\n\n"
        "REQUIRED:\n"
        "- Dependency check: verify package.json before importing any 3rd-party lib\n"
        "- States: implement loading (skeleton), empty, and error states\n"
        "- Tactile feedback: -translate-y-[1px] or scale-[0.98] on :active\n"
        "- Animations: transform/opacity only — never top/left/width/height\n"
        "- Motion (intensity>5): Framer useMotionValue/useTransform, spring stiffness:100 damping:20\n\n"
        "Full rules: invoke taste-skill or ui-ux-pro-max if needed.\n"
        "================================================================\n"
    )
    sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
