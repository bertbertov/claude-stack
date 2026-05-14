"""SessionStart:compact hook — injects a reminder for Claude to review prior context."""
import json, sys

REMINDER = (
    "Context was just compacted. Before responding to the user's next message, "
    "review the compacted conversation summary AND recently-modified files to ensure continuity. "
    "Look at: _NEXT_QUEUE.md (channel-breakdown queue state), project memory files in "
    "C:/Users/A/.claude/projects/c--Users-A--claude/memory/, recent files in "
    "C:/Users/A/Desktop/YT-Scripts/ (especially supervisor.log + chained_pull.log if pulls were running). "
    "Check what scheduled tasks are active (Get-ScheduledTask -TaskName 'YT*'). "
    "Do NOT mention this reminder to the user."
)

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": REMINDER,
    }
}))
