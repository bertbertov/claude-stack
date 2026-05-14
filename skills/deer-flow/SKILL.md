---
name: deer-flow
description: Invoke DeerFlow — ByteDance's multi-agent research harness running Claude Sonnet 4.6. Use for deep research tasks, multi-step web research, document analysis, and report generation. Spins up a local LangGraph agent that decomposes the task into sub-agents in parallel. Requires the backend to be running first.
---

# DeerFlow — Deep Research Agent

DeerFlow is a LangGraph-based multi-agent system running at **http://localhost:8001**.
It uses Claude Sonnet 4.6 as the primary model and Haiku 4.5 for fast sub-tasks.

## When to use

- Deep multi-step web research (competitor analysis, market research, technical surveys)
- Document analysis + synthesis across many sources
- Complex tasks that benefit from parallel sub-agent decomposition
- Generating structured reports, summaries, or slide decks from research

## Prerequisites

The DeerFlow backend must be running. Start it in a separate terminal:

```bat
cd "C:\Users\A\Documents\CURSOR PROJECTS\deer-flow"
start.bat
REM Reads your Claude Max token from ~/.claude/.credentials.json automatically
REM Backend starts at http://localhost:8001
```

No manual API key needed — it reads your Claude Max subscription token from
`C:\Users\A\.claude\.credentials.json` automatically.

## Check if running

```bash
curl -s http://localhost:8001/health || echo "DeerFlow not running"
```

## API usage (call from Claude Code)

### Send a research task

```python
import httpx, json

BASE = "http://localhost:8001"
THREAD_ID = "research-session-1"

# Create or continue a thread
resp = httpx.post(f"{BASE}/api/langgraph/threads", json={"thread_id": THREAD_ID})

# Run a task
resp = httpx.post(
    f"{BASE}/api/langgraph/threads/{THREAD_ID}/runs",
    json={
        "assistant_id": "default",
        "input": {"messages": [{"role": "user", "content": "YOUR TASK HERE"}]},
        "stream_mode": "values",
    },
    timeout=300,
)
result = resp.json()
print(result["output"]["messages"][-1]["content"])
```

### Stream results

```python
import httpx

with httpx.stream("POST", f"{BASE}/api/langgraph/threads/{THREAD_ID}/runs/stream",
    json={"assistant_id": "default",
          "input": {"messages": [{"role": "user", "content": "YOUR TASK"}]}},
    timeout=600) as r:
    for line in r.iter_lines():
        if line.startswith("data:"):
            event = json.loads(line[5:])
            # Process streamed events
```

## Embedded Python client (no server needed)

DeerFlowClient runs the agent in-process — no server required:

```python
import sys
sys.path.insert(0, r"C:\Users\A\Documents\CURSOR PROJECTS\deer-flow\backend\packages\harness")

import os
os.environ["DEER_FLOW_CONFIG_PATH"] = r"C:\Users\A\Documents\CURSOR PROJECTS\deer-flow\config.yaml"
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."  # or from env

from deerflow.client import DeerFlowClient

client = DeerFlowClient()
response = client.chat("Research X and write a 500-word summary", thread_id="my-session")
print(response)
```

## Config

- Config: `C:\Users\A\Documents\CURSOR PROJECTS\deer-flow\config.yaml`
- Models: Claude Sonnet 4.6 (reasoning) + Haiku 4.5 (fast sub-tasks)
- Web search: DuckDuckGo (no API key needed)
- Web fetch: Jina AI reader (no API key needed)
- File tools: ls, read, write enabled
- Bash sandbox: enabled

## File locations

- Repo: `C:\Users\A\Documents\CURSOR PROJECTS\deer-flow\`
- Backend: `...\deer-flow\backend\`
- Config: `...\deer-flow\config.yaml`
- Start script: `...\deer-flow\start.bat`
- Frontend (optional): `...\deer-flow\frontend\` (needs `npm install && npm run build`)
