"""SessionStart hook — auto-detects skill duplicates when the collection grows.

Runs on every session start. Cheap regex-based scan (sub-second). Only
emits a warning when:
  1. New skills were added since last session, AND
  2. Those skills have >=60% description-keyword overlap with existing skills.

Output goes to stdout, which Claude Code injects into the session context.
Claude sees it at start of next conversation and can flag to user or
auto-archive high-confidence (>=85%) duplicates.

State persisted at ~/.claude/skills/_audit_state.json so we only fire when
something changed.
"""
import json, sys, os, re
from pathlib import Path
from datetime import datetime, timezone

os.environ["PYTHONIOENCODING"] = "utf-8"
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SKILLS_DIR = Path.home() / ".claude" / "skills"
STATE_FILE = SKILLS_DIR / "_audit_state.json"

# Tunables
DUPE_THRESHOLD = 0.60   # min desc-keyword overlap to flag as candidate
AUTO_ARCHIVE_THRESHOLD = 0.85  # not used — Claude decides; just informational
MAX_REPORTED = 8        # top N pairs to surface

STOPWORDS = {
    "the", "a", "and", "or", "for", "with", "to", "of", "in", "on", "is",
    "use", "when", "user", "wants", "this", "that", "skill", "skills",
    "from", "into", "via", "via", "by", "as", "an", "be", "are", "it",
    "you", "your", "i", "we", "they", "all", "any", "any", "only", "also",
    "use", "uses", "using", "based", "builds", "build", "building", "create",
    "creates", "creating", "make", "makes", "making", "set", "sets",
}


def parse_frontmatter(skill_md: Path) -> tuple[str | None, str]:
    """Extract name + description from SKILL.md YAML frontmatter."""
    try:
        text = skill_md.read_text(encoding="utf-8", errors="ignore")[:1500]
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

    name = name_m.group(1).strip().strip("\"'") if name_m else None
    desc = desc_m.group(1).strip().strip("\"'")[:400] if desc_m else ""
    return name, desc


def keyword_set(text: str) -> set[str]:
    """Extract content-bearing words from a description."""
    words = re.findall(r"\b[a-z]{4,}\b", text.lower())
    return set(w for w in words if w not in STOPWORDS)


def jaccard(s1: set, s2: set) -> float:
    if not s1 or not s2:
        return 0.0
    return len(s1 & s2) / len(s1 | s2)


def scan_skills() -> dict[str, str]:
    """Return {skill_name: description} for all active (non-archived) skills."""
    out = {}
    if not SKILLS_DIR.exists():
        return out
    for d in SKILLS_DIR.iterdir():
        if not d.is_dir():
            continue
        if d.name.startswith("_"):  # _archive, _audit_state etc
            continue
        skill_md = d / "SKILL.md"
        if not skill_md.exists():
            continue
        name, desc = parse_frontmatter(skill_md)
        if name and desc:
            out[name] = desc
    return out


def find_dupe_pairs(skills: dict[str, str]) -> list[tuple[float, str, str]]:
    """Return [(overlap, name_a, name_b), ...] sorted desc."""
    keysets = {n: keyword_set(d) for n, d in skills.items()}
    pairs = []
    names = list(skills.keys())
    for i, n1 in enumerate(names):
        for n2 in names[i + 1:]:
            score = jaccard(keysets[n1], keysets[n2])
            if score >= DUPE_THRESHOLD:
                pairs.append((score, n1, n2))
    return sorted(pairs, reverse=True)


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_state(state: dict) -> None:
    try:
        STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    except Exception:
        pass


def main() -> int:
    state = load_state()
    skills = scan_skills()
    current_count = len(skills)
    last_count = state.get("skill_count", 0)
    last_known_names = set(state.get("known_names", []))
    current_names = set(skills.keys())
    new_names = current_names - last_known_names

    # First run: seed state, no warning
    if not last_known_names:
        save_state({
            "skill_count": current_count,
            "known_names": sorted(current_names),
            "last_check_iso": datetime.now(timezone.utc).isoformat(),
        })
        return 0

    # No new skills → silent
    if not new_names:
        # Update last-check timestamp only
        state["last_check_iso"] = datetime.now(timezone.utc).isoformat()
        state["skill_count"] = current_count
        save_state(state)
        return 0

    # Find dupes that involve at least one new skill
    pairs = find_dupe_pairs(skills)
    relevant = [(s, a, b) for (s, a, b) in pairs if a in new_names or b in new_names]

    if relevant:
        out = []
        out.append("================================================================")
        out.append("[SKILL-DEDUPE-WATCH — auto-triggered]")
        out.append("================================================================")
        out.append("")
        out.append(f"{len(new_names)} new skill(s) added since last session: {', '.join(sorted(new_names))}")
        out.append(f"{len(relevant)} potential duplicate pair(s) detected (>={int(DUPE_THRESHOLD*100)}% description overlap):")
        out.append("")
        for score, n1, n2 in relevant[:MAX_REPORTED]:
            marker = "[HIGH]" if score >= AUTO_ARCHIVE_THRESHOLD else "[CHECK]"
            out.append(f"  {marker} {n1}  <->  {n2}  ({score:.0%})")
        out.append("")
        out.append("Action for Claude:")
        out.append("  - At natural conversation pause, surface this list to user.")
        out.append("  - For HIGH (>=85%) pairs, suggest archiving the duplicate.")
        out.append("  - For CHECK pairs, ask user before any retire decision.")
        out.append("  - Archive moves go to ~/.claude/skills/_archive/ (revertible).")
        out.append("================================================================")
        sys.stdout.write("\n".join(out) + "\n")

    # Persist new state
    save_state({
        "skill_count": current_count,
        "known_names": sorted(current_names),
        "last_check_iso": datetime.now(timezone.utc).isoformat(),
    })
    return 0


if __name__ == "__main__":
    sys.exit(main())
