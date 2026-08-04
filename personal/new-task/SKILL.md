---
name: new-task
description: |
  Self-executing prompt system via GitHub Issues in grandchildrice/life.
  Each issue is a structured prompt that Hermes can read, understand,
  and execute without clarification. Execution history is preserved in
  comments; final output destinations are explicitly declared.
version: 2.0.0
author: gohan
platforms: [linux]
metadata:
  hermes:
    tags: [github, issues, task-management, prompt-engineering, personal-productivity]
    related_skills: [github-workflow, notion-databases]
---

# New Task — Self-Executing Prompt System

## Philosophy

Inspired by Anthropic's structured prompting principles (Goal, Loop, Prompt Engineering 101):
- **Each issue IS the prompt**: no separate instruction needed
- **Explicit over implicit**: every requirement is declared. If a result needs to be saved to a specific Drive folder or Notion DB, the absolute URL must be in the `## References` or `## Output` section.
- **Structured over freeform**: sections use explicit markdown headings for reliable parsing.
- **Chain-of-thought by default**: execution steps are logged in comments.
- **Self-contained context**: the issue body holds everything needed to execute.
- **Safety Guard**: When a task involves interacting with other people (interviews, outreach, direct messaging), avoid phrasing the goal as \"performing the action\" (e.g., \"interview members\"). Instead, phrase it as \"designing the process,\" \"listing candidates,\" or \"preparing content\" for those actions. The actual execution of communication must be a separate, explicitly approved step to avoid triggering system blocks.

## Quick Use

### `life-task` command (recommended for quick creation)

A shell script at `~/.local/bin/life-task` provides quick issue creation:

```bash
# Quick create with minimal template (good for capturing ideas fast)
life-task "Task: Fix login bug on mobile"

# Full create with body content
life-task "Task: Research ZKP benchmarks" "$(cat <<'EOF'
## Goal
Research and compare ZKP benchmark results

## Context
Need data for presentation next week

## Output
- Destination: Slack thread
- Format: Markdown table
EOF
)"
```

When the user says **"life-task \<title\>"** in Slack, immediately create an issue with:
- Title: the provided text (prefix with "Task: " if not already)
- Body: the structured template (Goal/Context/Approach/Output/Constraints/References) — fill known fields from conversation context, leave unknown fields empty
- Labels: `task,backlog`
- Post the issue URL back to the Slack thread

### Create a new task (manual template)

```bash
# Step 1: fill the template
cat > /tmp/task.md <<'EOF'
## Goal
<1-sentence objective>

## Context
<background, constraints, related resources>

## Approach
<recommended method, tools to use, steps to follow>

## Output
- Destination: <Slack / Notion:<DB> / GitHub:<repo> / file:<path>>
- Format: <markdown / JSON / PDF / ...>
- Naming: <how to name the output>

## Constraints
- Time: <expected duration or deadline>
- Tools: <specific tools to use or avoid>
- Quality: <acceptance criteria>

## References
- <URL or file path>
- <URL or file path>
EOF

# Step 2: create the issue
gh issue create --repo grandchildrice/life \
  --title "Task: <short action-oriented title>" \
  --body-file /tmp/task.md \
  --label "task,backlog"
```

## Issue Body Structure (MANDATORY)

Each task issue MUST use these sections. Empty sections are allowed but the heading must exist.

### `## Goal`
**What success looks like.** One sentence, action-oriented, verifiable.
- Good: "Summarize the last 3 months of ZKP research into a 2-page Notion doc"
- Bad: "ZKP research" (too vague; unclear when done)

### `## Context`
**Why this matters and what the agent needs to know.** Include:
- Background (why this task exists)
- Related prior work (link to past issues/results)
- Access requirements (API tokens, file paths, credentials)
- Domain-specific knowledge the agent needs

### `## Approach`
**How to execute.** Recommended but not rigid:
- Step-by-step plan (or "use your best judgment")
- Tools to use (or "use any available tools")
- Specific techniques or frameworks
- What NOT to do (negative constraints)

### `## Output`
**Where and in what form to deliver results.** Be explicit:
- **Destination**: Slack thread / Notion DB / GitHub repo / local file path
- **Format**: markdown, structured JSON, PDF, spreadsheet, code, etc.
- **Naming**: how to title/name the output artifact

### `## Constraints`
**Boundaries and quality gates.** Examples:
- Time: "Complete within 30 minutes; stop and report if longer"
- Scope: "Do NOT implement X; only research and summarize"
- Tools: "Use `uv run` for Python; never use bare `python3`"
- Quality: "Must include at least 3 primary sources; cite URLs"

### `## References`
**Links and file paths the agent will need.** One per line, with a brief note.

## Status Labels (State Machine)

| Label | Meaning | Who sets |
|-------|---------|----------|
| `backlog` | Ready to execute, not started yet | You or Hermes |
| `in-progress` | Hermes is actively working on this | Hermes |
| `waiting-review` | Done, awaiting your review | Hermes |
| `done` | Completed and confirmed | You (after review) |
| `blocked` | Waiting for dependency or clarification | You or Hermes |

### Transition commands

```bash
# Start execution
gh issue edit NUM --repo grandchildrice/life \
  --add-label "in-progress" --remove-label "backlog"

# Submit for review
gh issue edit NUM --repo grandchildrice/life \
  --add-label "waiting-review" --remove-label "in-progress"

# Mark done (close)
gh issue close NUM --repo grandchildrice/life
gh issue edit NUM --repo grandchildrice/life --add-label "done"

# Re-open if revision needed
gh issue reopen NUM --repo grandchildrice/life \
  --add-label "backlog" --remove-label "done"
```

## Execution Comment Protocol

After each significant step, Hermes comments on the issue. This preserves the chain-of-thought and creates an audit trail.

### Comment format

```markdown
### Step N: <what was done>
**Timestamp**: YYYY-MM-DD HH:MM
**Status**: ✅ success / ⚠️ partial / ❌ failed

<details>
<summary>Details</summary>

- Action taken: <brief description>
- Tool used: <which Hermes tool>
- Intermediate result: <link or summary>
- Blockers encountered: <if any>
</details>
```

### Final Result comment (MANDATORY)

When execution completes, post this exact structure:

```markdown
## ✅ Result

| Destination | Link / Path |
|-------------|-------------|
| Slack thread | <URL or "this thread"> |
| Notion page | <URL> |
| GitHub issue/PR | <URL> |
| Local file | `<absolute path>` |
| Other | <description> |

### Summary
<2-3 sentence recap of what was accomplished>

### Verification
- [ ] Output matches requested format
- [ ] All constraints satisfied
- [ ] References cited correctly
```

## Hermes Execution Flow

When you say "Issue #N を実行して", Hermes follows this sequence:

1. **Read** the issue body from `grandchildrice/life`
2. **Parse** Goal, Context, Approach, Output, Constraints, References
3. **Plan** execution steps (silent or as Slack reply)
4. **Execute** using appropriate tools
5. **Log** each step as an issue comment
6. **Deliver** final output to declared destination(s)
7. **Label** transition: `in-progress` → `waiting-review`
8. **Post** Final Result comment with all output links

## Finding and Reusing Past Tasks

```bash
# View full execution history (comments)
gh issue view NUM --repo grandchildrice/life --comments

# List open tasks
gh issue list --repo grandchildrice/life --state open --label backlog

# List completed tasks
gh issue list --repo grandchildrice/life --state closed

# Search by keyword
gh issue list --repo grandchildrice/life --search "ZKP"
```

## Mobile Workflow (GitHub Mobile App)

- Create issues from the "+" button
- Paste the template, fill sections
- Add comments to provide clarification
- Close done issues with a swipe

## Anti-Patterns (AVOID)

- ❌ Vague titles like "Research" or "Look into X" → use action verbs
- ❌ Missing `## Output` section → Hermes won't know where to deliver
- ❌ Editing the original body for progress → use comments only
- ❌ Multiple unrelated tasks in one issue → one goal per issue
- **Self-Introduction (Personal Brand)**: Create a dedicated Issue for managing self-introduction versions. Store the "Gold Standard" in the description and specific versions/occurrences (date, event, tone) in the comments. Use patterns like 'v1.0', 'v1.1' to track evolution.

## Example: Well-Structured Task

```markdown
## Goal
Generate a comparison table of 3 ZK-proof systems (Groth16, PLONK, STARKs)
in Japanese, save as a Notion page under the Research DB.

## Context
Preparing a presentation for ZKTokyo 2026. Audience is technical but
needs accessible explanations. Prior work in life#7 covers FHE basics.

## Approach
1. Use web_search to find recent comparison articles (2024-2025)
2. Extract key metrics: proof size, verification time, trusted setup requirement
3. Write in narrative Japanese (not bullet points), following user's preference
4. Include specific examples for each system

## Output
- Destination: Notion: Research DB
- Format: Page with heading structure
- Naming: "ZKP比較: Groth16 vs PLONK vs STARKs"

## Constraints
- Must cite at least 2 primary sources per system
- Avoid LaTeX in output (plain text / markdown only)
- Complete within 20 minutes; report if more time needed

## References
- https://eprint.iacr.org/2024/xxx (PLONK update)
- life#7 — FHE入門まとめ
```

## 長文の本文・コメントを更新する（scripts/patch_issue_comment.js）

長い提案書や表を `gh issue comment --body "..."` でシェル経由に渡すと、バッククォート・`$`・
引用符の食い違いで壊れる。`scripts/patch_issue_comment.js` は `gh api` で本文を取得し、
Node の文字列操作で置換して JSON を stdin から PATCH するので、本文が一度もシェルを通らない。

```bash
# 見出しから次の見出しまでを差し替え（--dry-run で確認してから実行）
node scripts/patch_issue_comment.js \
  --endpoint repos/grandchildrice/life/issues/comments/<ID> \
  --between "## 事業の全体像" "## 実施体制" --with-file new_section.md --dry-run

# issue 本文まるごと差し替え
node scripts/patch_issue_comment.js --endpoint repos/grandchildrice/life/issues/55 --body-file body.md

# 正規表現置換（見出しレベルの一括調整など）
node scripts/patch_issue_comment.js --endpoint ... --regex "^成果の測定(.*)$" --with '#### 成果の測定$1'
```

- `--between` と `--regex` は繰り返せる。開始マーカーが本文に複数あるとエラーで止まる
  （意図しない場所を書き換えないため）。
- `--dry-run` は PATCH せず、置換前後の文字数と最初の差分位置の前後 40 字だけを出す。
  **破壊的更新なので、まず dry-run で確認する。**
- 長文の生成側（docx など）は `productivity/docx-proposal-filler` を参照。

## Recommended Labels

```bash
# Create once (already done during setup)
for label in "task" "backlog" "in-progress" "waiting-review" "done" "blocked" \
             "research" "dev" "admin" "critical" "high" "normal" "low"; do
  gh label create "$label" --repo grandchildrice/life --color "ededed" --force 2>/dev/null
done
```