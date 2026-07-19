---
name: devops-workflows
description: DevOps and infrastructure automation workflows. Covers exporting Slidev presentations to PNG, webhook subscriptions for event-driven agent activation, and Microsoft Teams meeting summarization pipelines. Use when the task involves infrastructure glue, presentation exports, webhooks, or meeting automation.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [devops, webhook, slidev, teams, automation, infrastructure]
---

# DevOps Workflows

This skill covers infrastructure-adjacent automation: presentation exports, webhook subscriptions, and meeting pipeline operations.

---

## Slidev Export to PNG

Export Slidev presentations to PNG images on NixOS/Linux.

### Setup
```bash
npm install
npm install -D playwright-chromium
```

### Export with System Chrome
On NixOS/Linux, Playwright often fails due to missing system libraries. Use system Chrome:
```bash
npx slidev export --format png --per-slide --executable-path /run/current-system/sw/bin/google-chrome-stable
```
Common Chrome paths: `/run/current-system/sw/bin/google-chrome-stable`, `/usr/bin/google-chrome-stable`, `/usr/bin/chromium-browser`.

### Output
- PNG files saved to `./slides-export/` named `01.png`, `02.png`, etc.

### Pitfalls
- Do NOT run `npx playwright install-deps chromium` on NixOS — it fails with sudo errors
- If `playwright-chromium` alone doesn't work, use `--executable-path` pointing to system Chrome first
- Large presentations may OOM; export in batches with `--range`

---

## Webhook Subscriptions

Create dynamic webhook subscriptions so external services can trigger Hermes agent runs.

### Prerequisites
Enable the webhook platform first:
```bash
hermes webhook list
```
If not enabled, add to `~/.hermes/config.yaml`:
```yaml
platforms:
  webhook:
    enabled: true
    extra:
      host: "0.0.0.0"
      port: 8644
      secret: "generate-a-strong-secret-here"
```
Then restart: `hermes gateway run` and verify with `curl http://localhost:8644/health`.

### Commands
```bash
# Create subscription
hermes webhook subscribe <name> \
  --prompt "Prompt template with {payload.fields}" \
  --events "event1,event2" \
  --description "What this does" \
  --skills "skill1,skill2" \
  --deliver telegram \
  --deliver-chat-id "12345"

# List / remove / test
hermes webhook list
hermes webhook remove <name>
hermes webhook test <name> --payload '{"key":"value"}'
```

### Prompt Templates
Support `{dot.notation}` for nested payload fields:
- `{issue.title}` — GitHub issue title
- `{pull_request.user.login}` — PR author
- `{data.object.amount}` — Stripe payment amount

### Direct Delivery (No Agent)
For notifications without LLM cost, add `--deliver-only`:
```bash
hermes webhook subscribe antenna-matches \
  --deliver telegram --deliver-chat-id "123" \
  --deliver-only \
  --prompt "🎉 New match: {match.user_name}!"
```

### Security
- Each subscription gets an auto-generated HMAC-SHA256 secret
- Signatures validated on every incoming POST
- Subscriptions persist to `~/.hermes/webhook_subscriptions.json`

### Pitfalls
- Always verify webhook signatures to prevent spoofing
- Implement idempotency keys for at-least-once delivery guarantees
- Log all webhook receipts for debugging
- Firewall/NAT: webhook URL must be reachable from the service; use ngrok or cloudflared for local dev

---

## Teams Meeting Pipeline

Operate the Teams meeting summary pipeline via Hermes CLI.

### Prerequisites
Environment variables in `~/.hermes/.env`:
```bash
MSGRAPH_TENANT_ID=...
MSGRAPH_CLIENT_ID=...
MSGRAPH_CLIENT_SECRET=...
```

### Commands
```bash
# Validate config
hermes teams-pipeline validate
hermes teams-pipeline token-health
hermes teams-pipeline token-health --force-refresh

# List and inspect jobs
hermes teams-pipeline list
hermes teams-pipeline list --status failed
hermes teams-pipeline show <job-id>

# Replay / debug
hermes teams-pipeline run <job-id>
hermes teams-pipeline fetch --meeting-id <id>
hermes teams-pipeline fetch --join-web-url "<url>"

# Subscription management
hermes teams-pipeline subscriptions
hermes teams-pipeline subscribe --resource communications/onlineMeetings/getAllTranscripts --notification-url https://<host>/msgraph/webhook --client-state "$MSGRAPH_WEBHOOK_CLIENT_STATE"
hermes teams-pipeline maintain-subscriptions
hermes teams-pipeline maintain-subscriptions --dry-run
```

### Critical Pitfall: Graph Subscriptions Expire in 72 Hours
Microsoft Graph caps webhook subscriptions at 72 hours and does NOT auto-renew. If `maintain-subscriptions` is not scheduled, meeting notifications silently stop.

**Fix:** Schedule automated renewal via cron/systemd timer every 12 hours.

### Decision Tree
- "Why didn't I get a summary?" → `list --status failed` → `show <job-id>` → check `subscriptions`
- "Is setup working?" → `validate` → `token-health` → `subscriptions`
- "Re-run summary for meeting X" → `list` → `run <job-id>`

### Pitfalls
- Graph API tokens expire; refresh before long-running operations
- Transcript availability depends on Teams recording settings
- Large meetings may exceed token limits; chunk before summarizing
- If token-health passes but API calls return 401/403, admin consent may need re-granting in Azure portal
