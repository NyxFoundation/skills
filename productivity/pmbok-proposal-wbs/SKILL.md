---
name: pmbok-proposal-wbs
description: |
  Author an enterprise-grade proposal (docx) plus a PMBOK-style WBS / Gantt / estimate workbook (xlsx)
  that can be handed to a large corporate or public-sector client as-is, then harden it through a
  recursive external-agent review loop (Codex CLI / hermes) until an independent reviewer rules it
  submittable. Covers the client-ready writing rules (no meta text, no revision history, no AI tells,
  no internal paths in figure captions), the page budget and the 本編 / 技術別紙 split, reading the
  client's own API docs and OSS source before writing so "preliminary experiment" tasks disappear
  from the WBS, confirmation items phrased as 「私たちの理解は XX。正しいか」, numeric-consistency
  invariants (one script is the single source for schedule, effort and the body tables), explicit
  buffer accounting, option sets where every option reaches the goal, rendered figures with verified
  font weight, heading outline levels, unit-price separation, and the Drive / GitHub distribution
  steps. Trigger on: 「提案書を作って」「WBS を引いて」「ガントチャート」「見積を出して」「PMBOK」
  「提案資料の体裁」, or any request to turn a scope into a client-facing proposal + schedule + estimate.
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

Nine phases. Each ends with something checkable. Do **not** collapse 2 into 5 — writing the docx
first produces a document full of reasoning that then has to be scrubbed, and the scrubbing is what
leaves the tell-tale seams. Phase 1 now includes reading the client's own source and API docs;
skipping it is what puts an 8–10 person-day "preliminary experiment" into the WBS for no reason.

### 0. Intake — ask before writing

Ten questions. Ask the unanswered ones **in one batch**, propose a default for each, and start on the
defaults if the requester says "任せる". Leaving these implicit is what turns one pass into five.

| # | 確認事項 | 既定値 |
|---|---|---|
| 1 | 提出先（社名・部門・読み手の職掌） | — 必須。宛名と用語の粒度が決まる |
| 2 | 期間と着手日 | 4 カレンダー週。祝日を除いた営業日数を算出して提示 |
| 3 | 対象範囲（システム／業務） | 未定なら 8 章の選定観点を提示して客に選ばせる建て付け |
| 4 | 成果物の形式 | 提案書 docx ＋ WBS/ガント/見積 xlsx |
| 5 | 単価の扱い | 本文は工数のみ。単価と契約金額は別紙。xlsx に入力欄 |
| 6 | 実施主体の正式表記 | — 必須。途中で変わると全文書き換え |
| 7 | 配布先（repo / Drive フォルダ ID） | private repo ＋ Drive |
| 8 | 顧客名を repo に書いてよいか | **公開 repo なら書かない。** 一般化してテンプレート化 |
| 9 | レビュー担当エージェント | `codex exec` |
| 10 | 既存資料・過去のやり取り | issue / 過去提案 / 議事録があれば先に読む |

**出力**: 諸元が確定した状態。

### 1. Evidence — gather before arguing

Chapter 1 is the longest and carries every external claim. Collect first, write second.

- 一次情報を取りに行く: プレスリリース、公式製品ページ、論文（arXiv）、規格（ISO/IEC 等）
- 手法の中身は**実装を読む**。スキーマ・プロンプト・サンプル出力が、公式ドキュメントより正確
- 各数値に「該当箇所 / 内容 / 出典」の 3 列を持たせ、そのまま付録 D になる形で貯める
- 他社実績と自社実績を混ぜない。報道ベースは採用しないか、報道と明示する

#### 顧客の実装と API を先に読む — 「予備実験」を WBS に入れる前に

「着手直後に予備実験を行う」と書いたタスクは、**公開情報を読めば消えることが多い**。
実際に、8〜10 人日の予備実験タスクが丸ごと不要になった。読む対象:

- 顧客の API ドキュメント（注文種別、状態遷移、エラー、レート制限、**配信保証の有無**）
- 顧客が公開している OSS 実装のソース（何を検証していて、何を検証していないか）
- 採用予定ライブラリのソース（型の精度、拡張の制約。ドキュメントより正確）

読んだ結果は提案書に「**公開情報で確認済みの事項**」の表として載せる（確認したこと / 根拠 / 帰結）。
工数が減り、着手時に前提が揃い、**調べてきたことが相手に伝わる**。

そして確認事項の書き方が変わる。**抽象的に尋ねるのではなく、こちらの理解を書いて正誤を問う。**

```
✗ 執行イベントの配信保証について教えてください。
✓ private stream は配信順序を保証せず、シーケンス番号もありません。したがって受信側は
   注文 ID ごとに最新の状態を真値として保持する設計になります。この理解で正しいですか。
   欠落があり得る場合、REST による定期リコンサイルで問題ないでしょうか。
```

回答者は「はい／いいえ」と差分だけ書けばよくなる。相手の負担が下がり、回答率が上がる。

**出力**: 出典表（付録 D の原型）＋「公開情報で確認済みの事項」表。

### 2. Source docs — the private set

Write the ten `.md` files. Structure and per-file contents in `references/document-skeleton.md`.

**出力**: `docs/00`〜`09` ＋ `README.md`。この時点で論理は完成している。

### 3. Numbers — reconcile before generating

```
phases → tasks (with effort) → vendor-side rollup → role table → capacity check → buffer
```

Build the WBS first and derive the role table from its rollup — never the reverse.
`Σ role effort ≤ business days × headcount`, 75–90% utilisation.
Details and the worked failure case in `references/wbs-and-estimation.md`.

**出力**: タスク積み上げ＝ロール別工数、capacity 内、予備工数が別行で計上済み。

### 4. Figures — render, then look at them

Anything structural (state machines, graphs, flows, architectures) gets a rendered PNG.
A mermaid block or a code listing does not communicate. Use `presentation/editorial-figures`.
Never rely on colour alone. **Open every PNG with the Read tool and fix it.**

**出力**: 目視済みの PNG。

### 5. Generate

```bash
npm install docx && node make_docx.js                       # → proposal .docx
uv run --quiet --with openpyxl python make_xlsx.py          # → WBS/Gantt/estimate .xlsx
```

Chapter order and the workbook sheet set: `references/document-skeleton.md`.

### 6. Self-check — before spending a review round

```bash
uv run --quiet python preflight_check.py proposal.docx --dump proposal_dump.md
```

Validates every XML part, counts outline levels, greps the banned vocabulary, measures
sentence-ending monotony, flags unqualified superlatives, finds cross-references that point at
missing headings, and reports numeric drift. **BLOCKER が 0 になるまで外部レビューに回さない** —
機械で見つかる指摘に人間のレビューラウンドを使わない。

**分量もここで見る。** `preflight_check.py` が推定ページ数を出す。30 ページを超えていたら、
外部レビューに回す前に本編と技術別紙へ割る。レビュー後に割ると参照が総崩れになる。

図は別に検査する。`figure_preflight.py` が、**指定した太字が実際に効いているか**を報告する。
可変フォントしか無い環境では `fontweight="bold"` が黙って無視される。

```bash
uv run --quiet --with pillow --with matplotlib python figure_preflight.py figures/*.png
```

### 7. Review loop — blocking

Hand `proposal_dump.md` to an agent that did not write it. Iterate until 「このまま提出可 /
実害のある問題：なし」. Budget 4–7 rounds; shrink the finding cap each round; the final round asks
for a verdict only. Prompts, triage rules, and convergence signals in `references/review-loop.md`.

```bash
codex exec --skip-git-repo-check -c model_reasoning_effort="high" \
  "$(cat review_prompt.txt)" < /dev/null > review.txt 2>&1      # < /dev/null is mandatory
```

**A finding that conflicts with an explicit instruction from the requester is not automatically
right.** Satisfy the concern another way and report both.

**出力**: 提出可の判定。要した巡回数と、却下した指摘とその理由。

### 8. Distribute

```bash
git add -A && git commit && git push                          # private repo

rclone copy proposal.docx gdrive: --drive-root-folder-id <ID> --tpslimit 2   # originals
rclone copy wbs.xlsx      gdrive: --drive-root-folder-id <ID> --tpslimit 2

# native Google Docs/Sheets — first time only (rclone --drive-import-formats does NOT convert)
curl -X POST ".../files/<FILE_ID>/copy" -d '{"mimeType":"application/vnd.google-apps.document",...}'

# thereafter update IN PLACE so the shared URL survives
curl -X PATCH ".../upload/drive/v3/files/<DOC_ID>?uploadType=media" --data-binary @proposal.docx
```

Full commands and the quota/backoff notes in `references/toolchain.md`.

---

## Definition of done

```
[ ] 諸元 10 項目が確定している（不明なものは仮定として明記した）
[ ] 外部数値が全件、付録 D の出典表に載っている
[ ] タスク積み上げ = ロール別工数 ≤ capacity、予備工数が別建て
[ ] 構造的な内容が図になっていて、全 PNG を目視した
[ ] preflight_check.py が clean
[ ] 外部エージェントが「提出可」と判定した
[ ] private repo に push 済み、Drive に反映済み（共有済み URL は維持）
[ ] レンダリング検証の可否を報告に明記した（LibreOffice が無ければ「未検証」と書く）
```

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
  run formatting explicitly as well (`references/toolchain.md`). In python-docx, append
  `w:outlineLvl` to the heading's `pPr` yourself
- **Markdown → docx: join wrapped source lines into one paragraph.** A converter that emits one
  paragraph per line inflates the document by 30–40% and splits sentences visually
- **Count literal `**` in the generated file and require 0.** Inline emphasis that spans a source
  line leaks the asterisks into the client's document
- Tables need both `columnWidths` and a `width` on every cell
- A proposal to a financial institution needs a 作業規則 section: prohibited operations, access
  control, work logs, immediate reporting of critical findings, incident notification deadlines,
  subcontracting, data residency, backup erasure, liability, background IP

---

### 9. Length is a design constraint, not an outcome

Decide the budget before writing: **本編 25〜30 ページ、技術別紙 15〜25 ページ、工程表は xlsx**.
Anything the reader does not need in order to *decide* goes to the 別紙. Task-level effort and the
weekly Gantt never appear in the body — the workbook holds them.

A 60-page proposal does not read as thorough. It reads as something the sender did not curate.
`references/document-skeleton.md` has what goes where, and how to cut when you overshoot.

### 10. Every option must reach the goal

When you offer 3 price/duration options, do **not** build them as nested prefixes where the cheapest
one stops halfway through the phase chain. Every option runs 仕様 → 実装 → 検証 → 公開 and produces
the full deliverable set; what varies is **scope breadth and verification depth**. An option that
cannot claim the objective is not an option — you have offered one plan and two excuses.

### 11. State the mechanism; do not hand the judgement back

「〜は御社の事業判断です」 ends a paragraph that should have contained an argument. Explain the
structure — why the current constraint binds, what changes when it is removed — and leave only the
genuinely unknowable (timing, magnitude, demand) as a stated condition.

### 12. Background is facts; the proposal chapter carries the benefits

Put 「what the client gets」 in the background chapter and you will write it twice. Chapter 1 says
what is happening and what is not currently covered. Chapter 2 says the goal, why it comes first,
the claim with its falsification condition, and what follows as a by-product.

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
uv run --quiet --with openpyxl python make_schedule.py      # → schedule .xlsx（唯一の出典）
uv run --quiet --with openpyxl python make_schedule.py --md # → 本文に貼る表
uv run --quiet --with openpyxl python make_xlsx.py          # → WBS/estimate .xlsx
uv run --quiet python preflight_check.py proposal.docx      # BLOCKER 0 が外部レビューの前提
uv run --quiet --with pillow --with matplotlib python figure_preflight.py figures/*.png
```

`make_schedule.py` holds the task table, the effort ratios, the buffer ratio and the milestone dates
in one place, and emits both the workbook and the markdown tables you paste into the body. Editing
the body table by hand is how 425 and 447 person-days ended up in the same document for three
revisions.

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

- `references/document-skeleton.md` — **the chapter structure and source-doc set. Read this first.**
- `references/client-ready-rules.md` — the full client-ready checklist, with before/after examples
- `references/wbs-and-estimation.md` — WBS construction, gate design, effort reconciliation, buffer
- `references/review-loop.md` — prompt templates for each round, triage rules, convergence
- `references/toolchain.md` — docx-js / openpyxl / matplotlib / rclone / Drive API pitfalls
- `assets/make_docx.js`, `assets/make_xlsx.py` — generator skeletons (runnable as-is)
- `assets/make_schedule.py` — single-source schedule: tasks → xlsx Gantt + markdown tables
- `assets/figure_preflight.py` — font weight, stroke width and B&W legibility of every PNG
- `assets/preflight_check.py` — pre-review self-check; exits non-zero on a blocker

## Related skills

`presentation/editorial-figures` (figure house style), `productivity/docx-proposal-filler`
(filling a client-supplied form instead of authoring), `productivity/google-drive-upload`
(when the Drive API path is blocked), `devops/nixos-environment` (uv / font notes).
