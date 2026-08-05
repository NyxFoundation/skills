---
name: notion-databases
description: |
  Nyx Notion workspace API patterns: the Scrapbox DB schema, working curl patterns for the Notion API
  (page creation, block-append gotchas, block surgery on existing pages, image/file upload), and where the workspace's database IDs live.
  Database IDs themselves are NOT hard-coded here — they are in docs/nyx-directory.md. Load when creating
  or updating Notion pages, querying a Nyx database, or debugging Notion API errors.
version: 1.2.0
author: gohan (via Claude Code tuning)
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [notion, database, api, scrapbox, workflow]
---

# Notion Databases & API Patterns

## Credentials
- API key: read from `~/.config/notion/api_key` (also available to MCP server `notion`) — configured
  per environment at setup, never committed to this repo.
- API version header: `Notion-Version: 2022-06-28` for the page/database calls below.
  The block-surgery scripts were run against `2025-09-03`; either works for
  `/blocks/*`, but keep one version per script — response shapes differ between them.
- Prefer the Notion MCP tools; fall back to direct `curl` when the MCP tool fails.

## Database IDs

Database IDs are **not** hard-coded in this skill. Look them up in
[`docs/nyx-directory.md`](../../docs/nyx-directory.md) (Business Card DB, Scrapbox DB, Log DB, 採用面談,
SPECA ROI simulation, White-hat Hacking Reward Distribution). Reference an ID from there rather than
copying it into each skill, so an ID change is a one-line edit in one place.

## Scrapbox DB Properties
- `Name`: title (required)
- `Tag`: multi_select
- `関連PJ`: relation
- `作成日時`: created_time
- `作成者`: created_by

## Create a page in Scrapbox DB

Use the Scrapbox DB id from `docs/nyx-directory.md` as `<scrapbox-db-id>`:

```bash
curl -s -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer $(cat ~/.config/notion/api_key)" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "<scrapbox-db-id>"},
    "properties": {
      "Name": {"title": [{"text": {"content": "Page Title Here"}}]},
      "Tag": {"multi_select": [{"name": "tag1"}]}
    },
    "children": [
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Page content here"}}]}}
    ]
  }'
```

## Editing an existing page (block surgery)

Revising a long page — swapping a figure, renaming a heading, replacing one
chapter — is not a `curl` one-liner: you must first *find* the block. Do it in a
small script rather than by hand.

```js
const headers = {
  Authorization: `Bearer ${process.env.NOTION_API_TOKEN}`,
  "Notion-Version": "2025-09-03",
  "Content-Type": "application/json",
};
const api = async (path, options = {}) => {
  const r = await fetch(`https://api.notion.com/v1${path}`, { headers, ...options });
  const t = await r.text();
  if (!r.ok) throw new Error(`${r.status}: ${t}`);   // Notion's error body names the bad field — print it
  return t ? JSON.parse(t) : {};
};
const textOf = (b) => (b[b.type]?.rich_text || []).map((i) => i.plain_text || "").join("");

// 1. Read ALL children — one request returns at most 100 blocks.
const blocks = [];
let cursor;
do {
  const q = new URLSearchParams({ page_size: "100" });
  if (cursor) q.set("start_cursor", cursor);
  const page = await api(`/blocks/${PAGE_ID}/children?${q}`);
  blocks.push(...page.results);
  cursor = page.has_more ? page.next_cursor : null;
} while (cursor);
```

With `blocks` in hand:

- **Locate a section** by its heading, then slice to the next heading of the same
  level — that range *is* the chapter:
  ```js
  const start = blocks.findIndex((b) => b.type === "heading_1" && textOf(b).startsWith("4."));
  const end   = blocks.findIndex((b, i) => i > start && b.type === "heading_1");
  const figure = blocks.slice(start + 1, end).find((b) => b.type === "image");
  ```
- **Insert at a position** — `PATCH /blocks/{page_id}/children` takes an `after`
  block id. Without it, children always land at the end of the page.
- **Delete** — `PATCH /blocks/{id}` with `{"archived": true}` (or `DELETE
  /blocks/{id}`). Archived blocks vanish from the page but stay recoverable.
- **Replace = insert then archive, in that order.** Add the new block `after` the
  heading first, then archive the old one. Archiving first leaves the page
  visibly broken if the insert fails.
- **Edit text in place** — `PATCH /blocks/{id}` with the block's own type key:
  ```js
  await api(`/blocks/${target.id}`, { method: "PATCH", body: JSON.stringify({
    heading_1: { rich_text: [{ type: "text", text: { content: "新しい見出し" } }] } }) });
  ```
- **Audit before and after.** Dump `type` + `textOf` for every block to check the
  heading tree, count figures, and confirm captions. On a page of a few hundred
  blocks this catches a mis-anchored insert immediately; scrolling the UI does not.

Tables are `table` blocks whose `children` are `table_row`s — build the rows with
the table, not in a second call.

**Swapping a figure** composes the two halves of this skill: upload the new PNG
with `ntn` (see below) to get an upload id, insert it `after` the section heading
as `{"type": "image", "image": {"type": "file_upload", "file_upload": {"id": …},
"caption": [rt("図3　…")]}}`, then archive the old image block. Set the caption in
the same call — adding it afterwards is a second round-trip against a block whose
id you would have to look up again.

## Known Gotchas

### Appending text blocks (`PATCH /v1/blocks/{id}/children`)
Each block type (`paragraph`, `heading_1`, …) needs a `rich_text` array whose elements are
`{"type": "text", "text": {"content": "…"}}`. Passing a plain string yields `validation_error`.

### File upload via `ntn` CLI (recommended)

The direct `POST /v1/file_uploads` → PUT to `upload_url` flow does not work reliably: Notion now
returns a Notion API endpoint (`/v1/file_uploads/{id}/send`) instead of a presigned S3 URL, and a
direct PUT to it returns `400 invalid_request_url`. **Use the official Notion CLI (`ntn`) instead.**

#### 1. Install `ntn`
```bash
npm install -g ntn
```

#### 2. Get your workspace ID
```bash
curl -s -X GET https://api.notion.com/v1/users/me \
  -H "Authorization: Bearer $(cat ~/.config/notion/api_key)" \
  -H "Notion-Version: 2022-06-28" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['bot']['workspace_id'])"
```

#### 3. Upload a file and capture the upload ID
```bash
UPLOAD_ID=$(NOTION_API_TOKEN=$(cat ~/.config/notion/api_key) \
  NOTION_WORKSPACE_ID=<workspace_id> \
  ntn files create --plain < ./image.jpeg | cut -f1)
```
`ntn files create --plain` returns a tab-separated line
(`UPLOAD_ID  FILENAME  uploaded  CONTENT_TYPE  SIZE  CREATED_TIME  EXPIRY_TIME`).

#### 4. Attach to a Notion page as an image block (within ~1hr)
```bash
curl -s -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $(cat ~/.config/notion/api_key)" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"children":[{"object":"block","type":"image","image":{"type":"file_upload","file_upload":{"id":"'"$UPLOAD_ID"'"}}}]}'
```

**Fallback if `ntn` is unavailable:** use an external image URL (`"type":"external"`), or continue
page creation and report the local image path. Never block the workflow on an upload failure.
