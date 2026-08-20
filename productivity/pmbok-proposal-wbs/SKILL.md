---
name: pmbok-proposal-wbs
description: |
  Author an enterprise-grade proposal (docx) plus a PMBOK-style WBS / Gantt / estimate workbook (xlsx)
  that can be handed to a large corporate or public-sector client as-is, then harden it through a
  recursive external-agent review loop (Codex CLI / hermes) until an independent reviewer rules it
  submittable. Covers the client-ready writing rules (no meta text, no revision history, no AI tells),
  numeric-consistency invariants (task rollup must equal role-based effort), explicit buffer accounting,
  minimal-deliverable design, rendered figures instead of code blocks, heading outline levels, unit-price
  separation, and the Drive / GitHub distribution steps. Trigger on: 「提案書を作って」「WBS を引いて」
  「ガントチャート」「見積を出して」「PMBOK」「提案資料の体裁」, or any request to turn a scope into a
  client-facing proposal + schedule + estimate.
---

# PMBOK-style proposal & WBS

Produce three artifacts that survive a procurement review:

| # | Artifact | Format | Role |
|---|---|---|---|
| 1 | 提案書 | `.docx` | The document the client reads and circulates internally |
| 2 | WBS・ガント・見積 | `.xlsx` | The schedule and effort the client's PMO checks |
| 3 | Source docs | `.md` in a private repo | Your working notes, design intent, and the "why" — **never shipped** |

The separation in row 3 is the whole game. Everything that explains *how you decided* lives in the repo.
Everything in the docx is addressed to the client. Mixing them is the single most common way a proposal
gets killed — see `references/client-ready-rules.md`.

---

## Workflow

```
1  Scope        — read the brief; identify the phase chain and the gate structure
2  Source docs  — write the internal .md set first (background, scope, WBS, deliverables, RACI, risks)
3  Numbers      — build the WBS, then reconcile task rollup ↔ role capacity ↔ estimate  ← invariant
4  Figures      — render actual images for anything structural; inspect every PNG
5  Generate     — make_docx.js and make_xlsx.py emit the client artifacts from the source docs
6  Review loop  — external agent reviews the extracted full text; iterate until "提出可"
7  Distribute   — private repo push, then Drive (docx/xlsx originals + native Google Docs/Sheets)
```

Do **not** skip step 2 into step 5. Writing the docx first produces a document full of reasoning
that then has to be scrubbed out, and the scrubbing is what leaves the tell-tale seams.

---

## The rules, in priority order

Full text in `references/client-ready-rules.md`. The compressed version:

### 1. Client-ready or it does not ship

Nothing in the docx may reveal that it was drafted, revised, or reasoned about.

- **No meta text.** 「本書の目的は」「〜という方針で構成した」「以下に整理する」
- **No revision history.** No "当初案 25 点 → 10 点", no diff tables, no "前回ご提示案からの変更点"
- **No internal cost defence.** 「当社側の作成工数」「追加請求を避けるための措置」「ここは削っていません」
- **No self-criticism.** Corrections belong in the repo commit message, not the deliverable
- **No AI tells.** Repeated identical sentence endings, 過剰敬語（でございます／申し上げます）, mechanical
  enumeration, empty intensifiers, over-hedging. Write です・ます, short sentences
- **No unqualified superlatives.** 「原理的に不可能」「唯一」「最高水準」「確実に」「最も容易」
  → attach the condition: 「確認した公開情報の範囲では」「前提条件が満たされていれば」

### 2. Every external number carries a source

Verify with a primary source before writing it. Collect them in an appendix table.
Never blend your own track record with third-party results in one sentence. If a figure only exists
in press coverage, either cite it as coverage or leave it out.

### 3. Numeric consistency is an invariant, not a goal

The reviewer will find every contradiction. Reconcile before generating:

- **Task rollup == role-based effort.** Build the WBS first, sum the vendor-side tasks, then derive
  the role table from that sum — not the other way round
- **Capacity check.** `Σ role effort ≤ business days × headcount`. 80% utilisation is realistic for a
  dedicated engagement; 55% means the plan cannot be executed as costed
- **Meeting hours must reconcile with person-days.** State explicitly which is the subset of which
- **One number per concept.** If property count is "30本以上", it is never also 40, 45, or 30〜60
- **State the rounding rule** when converting person-days to person-months

### 4. Buffer is explicit and named

- Book **~15% of the work effort as 予備工数**, shown as its own line
- **Do not distribute it across phases** — each phase will consume its allocation
- Keep the **schedule buffer** (business days) as a separate item from the effort buffer
- Write how it is absorbed when consumed, the cap, and what happens if unused

### 5. Deliverables: fewest that achieve the objective

Every document you ship is review cost for the client. Fold judgement tables, figures, and
intermediate analyses into the parent deliverable. Keep automatically generated artifacts (audit
trails, logs) as-is because they cost nothing to produce and carry evidentiary value.
Present this as a **構成方針**, never as a reduction from an earlier draft.

### 6. Structural content gets a rendered figure

A mermaid block, a DOT file, or a state-diagram in text does not communicate. Render it.
- Never rely on colour alone — a bar that is only a fill disappears in B&W print and PDF export.
  Put a glyph (`■`) in the cell too
- **Open every PNG with the Read tool and fix it.** Tofu glyphs, overlaps, and overflow are invisible
  until rendered
- See `presentation/editorial-figures` for the house style and `references/toolchain.md` for pitfalls

### 7. Unit price is separated from the document

The body states effort as a fixed value. Unit price and contract amount go to a separate 見積書.
Do **not** ship a table with an empty 単価 column for the client to fill in — procurement cannot
budget from that. Put the input cells in the workbook instead (yellow fill), including the buffer ratio.

### 8. Format requirements that are silently broken

- Headings need real outline levels or the navigation pane and Google Docs outline stay empty.
  `HeadingLevel` alone is not enough — the default heading style overrides your design, so set the
  run formatting explicitly as well (`references/toolchain.md`)
- Tables need both `columnWidths` and a `width` on every cell
- A proposal to a financial institution needs a 作業規則 section: prohibited operations, access
  control, work logs, immediate reporting of critical findings, incident notification deadlines,
  subcontracting, data residency, backup erasure, liability, background IP

---

## The recursive review loop

This is what turns a decent draft into a submittable one. Detail in `references/review-loop.md`.

```bash
# 1. Extract the full document text (tables as | -separated rows)
uv run --quiet python extract_docx_text.py proposal.docx > proposal_dump.md

# 2. Hand it to an independent agent — NOTE the stdin redirect
cd <dir with proposal_dump.md>
codex exec --skip-git-repo-check -c model_reasoning_effort="high" \
  "$(cat review_prompt.txt)" < /dev/null > review.txt 2>&1
```

**`< /dev/null` is mandatory.** Without it `codex exec` sees a non-TTY stdin, prints
`Reading additional input from stdin...`, and returns nothing.

Each round:

1. Ask for **A: submission-blocking defects** first, then logic, numbers, feasibility, gaps
2. Triage every finding — a finding that contradicts an explicit user instruction is not
   automatically right. Satisfy the underlying concern a different way and say so
3. Fix, regenerate, re-extract, re-review — **feed the previous round's fix list into the next prompt**
   so the reviewer verifies the fixes rather than re-deriving them
4. Narrow the scope each round. The final round asks **submission verdict only**, explicitly ruling
   out style preferences and further-refinement suggestions — otherwise the loop never converges
5. Stop at 「このまま提出可 / 実害のある問題：なし」

Expect 4–7 rounds. A typical trajectory: 12 findings → 8 → 6 → 5 → 4 → 3 → clear.
The highest-value findings are almost always **numeric inconsistency** and **overclaiming**.

Reviewer agents available: `codex exec` (Codex CLI), hermes, or a Claude subagent. Use one that did
not write the document.

---

## Generating the artifacts

Templates in `assets/`. Run from a directory holding the assets and any figure PNGs.

```bash
npm install docx                                            # docx-js
node make_docx.js                                           # → proposal .docx
uv run --quiet --with openpyxl python make_xlsx.py          # → WBS/Gantt/estimate .xlsx
```

`assets/make_docx.js` ships the helpers you need: cover page, `h1/h2/h3` with working outline levels,
`p`, `bullet`, `note`, `table` (dual-width, safe shading), `code`, `figure` (ImageRun), `caption`,
header/footer with page numbers, and a table-based Gantt that reads in B&W.

`assets/make_xlsx.py` ships: the WBS row schema, a conditional-formatting Gantt keyed on start/end
columns so bars follow edits, phase colouring, gate rows, and an estimate sheet whose unit-price and
buffer-ratio cells are the designated inputs.

---

## Distribution

```bash
# private repo
git add -A && git commit && git push

# Drive — originals
rclone copy proposal.docx gdrive: --drive-root-folder-id <FOLDER_ID> --tpslimit 2

# Drive — native Google Docs/Sheets (rclone --drive-import-formats does NOT convert; use the API)
curl -X POST "https://www.googleapis.com/drive/v3/files/<FILE_ID>/copy" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"...","mimeType":"application/vnd.google-apps.document","parents":["<FOLDER_ID>"]}'

# updating an existing Google Doc IN PLACE keeps its URL — do this, don't re-copy
curl -X PATCH "https://www.googleapis.com/upload/drive/v3/files/<DOC_ID>?uploadType=media" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document" \
  --data-binary @proposal.docx
```

Drive API returns 403 quota errors readily — retry with 2–5 minute backoff.
Full notes, including where the OAuth token lives, in `references/toolchain.md`.

---

## Honesty rules

- If LibreOffice is unavailable you **cannot** visually verify the docx or recalculate the xlsx.
  Say so explicitly when reporting: schema, table structure, and formula references were checked
  programmatically; page breaks and rendering were not
- Report what the external reviewer actually said, including the rounds it took
- When a review finding is declined, state which instruction it conflicts with and how the concern
  was addressed instead

## Files

- `references/client-ready-rules.md` — the full client-ready checklist, with before/after examples
- `references/wbs-and-estimation.md` — WBS construction, gate design, effort reconciliation, buffer
- `references/review-loop.md` — prompt templates for each round, triage rules, convergence
- `references/toolchain.md` — docx-js / openpyxl / matplotlib / rclone / Drive API pitfalls
- `assets/make_docx.js`, `assets/make_xlsx.py` — generator skeletons

## Related skills

`presentation/editorial-figures` (figure house style), `productivity/docx-proposal-filler`
(filling a client-supplied form instead of authoring), `productivity/google-drive-upload`
(when the Drive API path is blocked), `devops/nixos-environment` (uv / font notes).
