# Workflow: audit a codebase

Multi-dimensional audit (security + quality + performance + a11y) using the security skill suite + UI audit + agent dispatch.

## The prompt to use

```
deploy agents to audit <REPO_PATH> across <DIMENSIONS>.

Dimensions: <security | performance | accessibility | architecture | testing | dependencies | all>
Stack: <Next.js 15 / Expo SDK 54 / FastAPI / etc>
Output: ranked report with P0/P1/P2 severity, file:line refs, fix suggestions
```

The `deploy_agents.py` hook fires on `deploy agents`, injects the agent registry, and dispatches 3-7 specialists in parallel.

## Agents dispatched (per dimension)

| Dimension | Primary agents |
|-----------|---------------|
| Security | code-reviewer, security-auditor, backend-security-coder, frontend-security-coder, pentest-source-code-scanning skill, owasp-security skill |
| Performance | performance-engineer, perf-analyzer, database-optimizer, observability-engineer |
| Accessibility | accessibility-expert, ui-visual-validator |
| Architecture | architect-review, architecture skill, api-design skill |
| Testing | test-automator, tdd-orchestrator, test-long-runner |
| Dependencies | tob-supply-chain skill, security-scan skill |

## Security-only example

```
deploy agents to audit ~/projects/myapp for security vulnerabilities.

Focus: OWASP Top 10, exposed secrets, auth/session bugs, SSRF/SQLi/XSS, supply-chain risk
Stack: Next.js 15 + Prisma + Supabase auth
Output: SARIF report + executive summary
```

This dispatches:
- `pentest-source-code-scanning` skill (full SAST sweep)
- `tob-semgrep` skill (rule-based pattern matching)
- `tob-codeql` skill (taint flow analysis)
- `tob-supply-chain` skill (dependency risk)
- `security-auditor` agent (synthesizes findings)
- `owasp-security` skill (severity rating per OWASP rubric)

Results converge via `tob-sarif-parsing` skill into one ranked report.

## Verification gate

If the `taskmaster` Stop hook is installed (recommended for audit work), the agent CANNOT end the turn without proving:
- All requested dimensions were actually checked
- Findings include file:line references
- P0 findings have concrete fix suggestions

No "audit complete" without evidence.

## Output format

```markdown
# Audit Report: <repo>
## Severity summary
- P0 (block ship): 3
- P1 (fix soon): 12
- P2 (technical debt): 28

## P0 — Critical

### 1. SQLi via unsanitized search param
- **File:** src/api/search.ts:42
- **Pattern:** `db.raw(\`SELECT * FROM users WHERE name LIKE '${q}'\`)`
- **Fix:** Use parameterized query: `db.where('name', 'like', `%${q}%`)`
- **Severity:** P0 — direct database compromise
- **Tools that caught it:** tob-codeql, pentest-source-code-scanning, tob-semgrep

[... continues per finding ...]
```

## Cost

- Agent dispatch is local, $0 in API calls (uses your existing Claude session)
- Long-running audits on large repos may take 30-60 min wall time
