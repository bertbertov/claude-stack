# Workflow: verify end-to-end

The discipline that prevents "fixed it, should work now" claims that don't actually verify the user-visible outcome.

## The problem

Agents (and humans) routinely report success when they've only completed an intermediate step. "Deployed to prod" can mean: the build started, the build succeeded, the artifacts uploaded, the new pod is running, the new pod is serving traffic, the new pod is serving traffic without errors. Only the last counts. The first 5 are intermediate.

Saying "deployed" after step 3 is a lie of confidence.

## The rule

Don't claim a task is done until you have checked the **user-visible outcome**. The fix isn't done until the TERMINAL node ran with `status=success` and the side effect is observable.

**Trigger phrases that mean STOP and verify first:**
- "should work now"
- "fixed via API"
- "cache should reload"
- "will fire on next trigger"
- "after OAuth refresh"
- "once quota resets"
- "trigger updated"
- "PUT 13 nodes"
- "syntax OK"
- "saved"
- "restarted"

These are intermediate signals, not verifications.

## The walking-the-pipeline pattern

For any pipeline (CI/CD, n8n workflow, cron, webhook chain, deploy chain):

1. **Identify every stage.** What's the chain from "I clicked deploy" to "user sees new feature"?
2. **For each stage, what's the verification?** Logs, status endpoint, side effect observable from outside.
3. **Walk every stage.** Confirm `status=success` on each.
4. **Find the LAST node that ran.** If it's not the terminal node, the pipeline broke before completion.
5. **Confirm the side effect.** The reason you ran the pipeline — did it happen? Email sent? Database row inserted? UI updated?

Only after step 5 do you claim done.

## The enforcement layer

`taskmaster` (optional, install via `git clone https://github.com/blader/taskmaster && cd taskmaster && ./install.sh`) wires a Stop hook that blocks the agent from ending its turn without emitting a deterministic completion token.

When installed, your prompt becomes:

```
<task>
Deploy the n8n workflow update.

Verification requirement: confirm the new trigger fires by checking
execution count drops from 1/min to 1/5min over the next 10 minutes,
not just that the workflow was saved.
</task>
```

The agent CANNOT claim done without proof.

## Quota / rate-limit verification

Separate sub-rule. Never declare a polling/quota/rate fix done without showing before/after numbers.

If you change a trigger from 1 min to 5 min, verify by counting actual executions per hour. If the count didn't drop, the fix didn't take effect — likely the workflow didn't reload, or there are two triggers, or the cron didn't re-register.

## Quick verification commands

| Stack | Verify it |
|-------|-----------|
| n8n workflow | `curl <n8n>/rest/workflows/<id>` and check `active: true` + new schedule. Also `tail -f` the n8n logs. |
| Vercel deploy | `vercel inspect <url>` — check `state: READY` and `deploymentTarget: production`. |
| Cron job | `crontab -l` AND `tail -f /var/log/syslog | grep CRON` to confirm it actually fires. |
| Systemd service | `systemctl status <service>` AND `journalctl -u <service> -n 50` to confirm it's running AND emitting logs. |
| Docker container | `docker ps` AND `docker logs <id> --tail 50` AND hit the endpoint with `curl`. |
| Webhook chain | Trigger the upstream event, check downstream side effect. The webhook returning 200 doesn't mean the handler succeeded. |

## Skill / hook references

- Skill: `agent-introspection-debugging` — structured self-debug after a failure
- Skill (bundled): `superpowers:verification-before-completion` — process discipline (advisory)
- Hook (optional): taskmaster — Stop hook enforcement (blocking)
