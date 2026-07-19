---
name: slack-image-upload
description: |
  Upload images/files to Slack ALWAYS into the current thread (never straight to the channel), using the
  3-step external upload API (files.getUploadURLExternal → PUT → files.completeUploadExternal) with
  thread_ts extracted from HERMES_SESSION_KEY. Load whenever posting an image, chart, or file to Slack.
version: 1.0.0
author: gohan (via Claude Code tuning)
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [slack, image, upload, thread, files]
---

# Slack Image Upload (thread-safe, 3-step API)

**Rule: ALWAYS post to the current thread. NEVER post directly to the channel.**

## Context extraction
- Session/thread info lives in `HERMES_SESSION_KEY`, format: `agent:main:slack:group:{channel_id}:{thread_ts}`
- Bot token: env var `SLACK_BOT_TOKEN`

## The 3 steps
1. `files.getUploadURLExternal` — get `upload_url` + `file_id` (params: `filename`, `length` in bytes)
2. `PUT` the raw file bytes to `upload_url`
3. `files.completeUploadExternal` — MUST include BOTH `channel_id` AND `thread_ts`

## Working script template

```bash
FILE=~/.hermes/workspace/chart.png
KEY="$HERMES_SESSION_KEY"                       # agent:main:slack:group:CXXXXXXXXXX:1234567890.123456
CHANNEL=$(echo "$KEY" | awk -F: '{print $(NF-1)}')
THREAD_TS=$(echo "$KEY" | awk -F: '{print $NF}')
LEN=$(stat -c%s "$FILE")

RESP=$(curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/files.getUploadURLExternal?filename=$(basename $FILE)&length=$LEN")
UPLOAD_URL=$(echo "$RESP" | jq -r .upload_url)
FILE_ID=$(echo "$RESP" | jq -r .file_id)

curl -s -X PUT -H "Content-Type: application/octet-stream" --data-binary @"$FILE" "$UPLOAD_URL"

curl -s -X POST https://slack.com/api/files.completeUploadExternal \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"files\":[{\"id\":\"$FILE_ID\",\"title\":\"$(basename $FILE)\"}],\"channel_id\":\"$CHANNEL\",\"thread_ts\":\"$THREAD_TS\"}"
```

## Failure modes
- Missing `thread_ts` in step 3 → image lands in the channel (forbidden here) — always pass both fields
- `invalid_auth` → check `SLACK_BOT_TOKEN` is the Bot token (xoxb-), not an app-level token
- If the session key has no thread part (DM), pass only `channel_id`
