# WBS, gates, effort, buffer

The proposal's credibility rests on whether the numbers survive arithmetic. Build them in this order
— reversing it produces a plan that cannot be executed as costed.

```
phases → tasks (with effort) → vendor-side rollup → role table → capacity check → buffer → price
```

---

## 1. Phase and gate design

Structure the engagement as phases separated by **approval gates**. A gate is an event the client
owns: they judge, and the project does not proceed without it.

For each gate define four things:

| Field | Why |
|---|---|
| 期日 | A business-day number, not a date, so the plan survives a start-date change |
| 判定者 | A named client role. "全員" is not a judge |
| 通過条件 | Checkable at that moment. No condition that depends on a later phase |
| **不通過時の対応** | The most-read cell in the whole document |

### Gate naming

Name a gate for what is **actually true when it fires**. A gate at D14 called 「所見確定」 when
reproduction runs D14–D16 is a contradiction the reviewer will find immediately.

```
✗  G3 所見確定 (D14)        G4 再現性確定 (D16)
✓  G3 候補所見の確定 (D14)   G4 確定所見の確定 (D16)
```

### The unbreakable rule for gate failure

**Cut scope; do not extend the schedule.** A fixed-duration engagement whose gates slide has no
duration. State it once, prominently:

> ゲートを通過できない場合は、対象範囲を縮小して対応し、期間は延長しない方針としています。

Then every gate's 不通過時の対応 must be a scope reduction, not a delay.

### Phase ordering vs. gates

If phase N consumes an output that gate G produces, phase N cannot start before G. When you want
overlap for schedule reasons, **split the phase**:

```
第 5 フェーズ (D15–D18)
  D15–D16  候補所見に対する修正方針の検討     ← before G4, uses candidates
  D17–D18  実パッチの作成と再監査             ← after G4, uses confirmed findings
```

Say this in the phase goal line, not in a footnote.

---

## 2. WBS row schema

One row per task. The columns that matter:

| Column | Notes |
|---|---|
| ID | `P<phase>.<n>`; gates get `G<n>` |
| フェーズ | Drives the Gantt colour |
| 種別 | タスク / ゲート / 横断 / 予備工数 — drives conditional formatting |
| 作業内容 | Verb-first. What is produced, not what is "considered" |
| 主担当 / 協力 | One 主担当. Client-side tasks carry a client role here |
| 人日 | 0.25 granularity |
| 開始 / 終了 | Business-day numbers. **The Gantt reads these** |
| 主な成果物 | Which deliverable ID this feeds |
| 完了条件（DoD） | Checkable. 「〜を作成する」 is not a DoD; 「〜が全件、file:line に紐づく」 is |

Keep the task list at 60–80 rows for a 4-week engagement. Fewer and the client cannot see the work;
more and nobody reads it.

---

## 3. The reconciliation invariant

This is the finding an external reviewer will always produce if you get it wrong.

```
Σ (vendor-side task 人日)  ==  Σ (role table 人日)          ← must be equal
Σ (role table 人日)        ≤   business days × headcount     ← capacity check
```

Practical procedure:

1. Sum the WBS rows whose 主担当 is vendor-side. Call it `W`.
2. Distribute `W` across roles by who actually does those tasks.
3. Derive each role's utilisation: `role 人日 ÷ (that role's days on the project)`.
4. Sanity-check the utilisation. For a dedicated engagement **75–90% is realistic**.
   Below ~60% means you under-costed relative to the plan; above ~95% means no slack exists.

A worked failure from a real engagement:

```
role table said        46.7 人日   (utilisations 35–80%, avg 56%)
WBS task rollup said   61.0 人日
capacity              19 days × 4 technical staff = 76 人日
→ the plan needed 61 but was priced at 46.7. The task estimates were sound;
  the utilisations were wishful. Fixed by deriving the role table from the rollup.
```

### Client-side effort

Client effort is **not** in the same pot. Two separate figures:

- Client tasks that appear as WBS rows (they own the task) — usually tiny, 1–2 人日
- Client attendance and review time — meetings, document review, acceptance

State the containment relationship explicitly, because the reviewer will check it:

> 御社側の 1.0 人日は、7.3 に記載する御社ご稼働 10.0 人日の内数です。

And reconcile the meeting hours against it:

| 内訳 | 開発ご担当 | セキュリティご担当 |
|---|---|---|
| 会議ご出席（合計 16.5 時間） | 1.5 人日 | 1.5 人日 |
| 資料の事前確認 | 2.5 人日 | 0.5 人日 |
| 環境提供・レビュー | 2.0 人日 | — |
| 成果物の受入確認 | 1.0 人日 | 1.0 人日 |
| **合計** | **7.0 人日** | **3.0 人日** |

「約 15 時間」と「10 人日」を並べて書くと、10 人日は 70〜80 時間なので矛盾に見える。
Sum the meeting list yourself and quote the exact figure.

---

## 4. Buffer

Two buffers, never merged:

| 種別 | 量 | 管理 |
|---|---|---|
| **予備工数** | 作業工数の約 15% | フェーズに配分せず PM が一括管理 |
| **日程予備** | 2 営業日（最終日の後ろ） | 同上 |

Why not distribute it: an allocated buffer is consumed. Hold it centrally and release it against a
stated reason.

The document must answer four questions:

1. **How is it absorbed when consumed?** 「各要員の稼働率引き上げ、または日程予備の使用により吸収します。
   追加要員が必要となる場合は、事前に御社の承認を得たうえで投入します」
2. **What is the cap?** 「9.0 人日を超える工数は、御社の承認なく発生させません」
3. **What if unused?** 「予備工数を消費せずに完了した場合、当該分は請求しません」
4. **How is consumption reported?** 「消費した場合は、消費量と理由を週次でご報告します」

Note the capacity trap: if the role table already saturates the calendar, the buffer has nowhere to
go. That is why (1) exists — name the release valve.

Call it **予備工数**, not バッファ. The Japanese term reads as a commitment; the loanword reads as slack.

---

## 5. Deliverable design

Deliverables are the client's review cost. Design for the minimum that achieves the objective.

Classify first, then cut:

| 区分 | 性格 | Cut policy |
|---|---|---|
| A 診断成果 | 現時点の健全性を示す | Merge judgement tables into the main report |
| B 継続資産 | 終了後も使える | **Never cut.** This is what justifies the next phase |
| C 判断材料 | 次の判断のための材料 | Merge into one final report |

Folding rules that worked:

- Judgement tables (3-gate results, reproduction outcomes, residual risk) → chapters of the main report.
  The raw basis survives in the machine-readable audit trail, so nothing is lost
- Same-purpose documents (remediation policy + patch set + PR + re-audit diff) → one deliverable
- Figures and traceability tables → appendices of the specification document
- Intermediate analyses (threat model, CWE coverage) → **attribute columns** of the catalogue
- Auto-generated artifacts → keep as-is, unedited. "Delivered in the form generated at execution time"
  is itself an evidentiary property

Give every deliverable a 受入基準 that is checkable, and an 内包するもの column so the client can see
nothing was dropped.

Present the result as a **構成方針**. Never as "we reduced 25 to 10" — see `client-ready-rules.md` §2.

---

## 6. Success criteria

Define them before work starts, and get them agreed at kickoff. Two traps:

**Trap 1 — measuring only what you find.** If the engagement's premise is that verification capacity
is the bottleneck, then verification cost must be a measured indicator, not just detection count:

| 指標 | 測定方法 |
|---|---|
| 1 所見あたりの確認時間 | 提示から真偽・優先度の判断完了までの実測 |
| 判定に要したレビュアー数 | 1 所見の確定に関与した担当者数 |
| 誤検知の処理に費やした時間 | 取り下げた所見に費やした時間の合計 |
| 根拠の自己確認率 | 説明なしで証拠のみで再検証できた所見の割合 |

**Trap 2 — no zero case.** Every count-based indicator needs one:

> 候補が 0 件の場合は本指標を適用せず、未達とは判定しません。

And the gate that depends on it needs the same clause, plus what it judges instead.

**Secondary benefits are measured but excluded from the verdict.** If the proposal argues a side
benefit (developer velocity, onboarding, audit readiness), measure it as a reference indicator and
report actuals — but do not let it into the pass/fail. Mixing it reads as an escape hatch and weakens
the core claim. State the split explicitly.

---

## 7. Gantt that survives printing

- Bars driven by conditional formatting on the start/end columns, so editing the dates moves the bar
- Phase colour + **a glyph in the cell** (`■`) so it reads in B&W
- Gates in a dedicated row, distinct colour, short label
- Week bands above the day columns
- Freeze panes at the first data row / first day column
- In the docx, reproduce a **phase-level** Gantt as a table (10 rows, not 70) — the full WBS lives
  in the workbook

Business-day numbering (D1…Dn) is the source of truth; calendar dates are illustrative. Say so:

> 上表はタスク単位の積み上げです。日程は営業日通番を正とし、日付は基準カレンダーに基づく参考値です。

Recompute holidays whenever the start date changes — a 4-calendar-week engagement is rarely 20
business days.

---

## スケジュールは 1 本のスクリプトから生成する

**本文の表、xlsx、工数の宣言値を別々に手で書かない。** 3 つが揃うのは最初だけで、
1 回でも直せばずれる。実際に、宣言値 425 人日と表の合計 447 人日が 3 版にわたり残った。

タスク定義を持つスクリプトを 1 本置き、そこから xlsx と本文用の markdown 表を出す。
`assets/make_schedule.py` がその形。

```python
TASKS = [
    # (ID, タスク, フェーズ, 担当, 人日 A, 人日 B, 人日 C, 開始/終了 × 3)
]
def emit_xlsx(path): ...      # 週次ガント、フェーズ色、ゲート行
def emit_md():      ...       # 提案書に貼る比較表・フェーズ表・マイルストーン表
```

本文の表は `--md` の出力を貼る。直したらスクリプトを直して貼り直す。
**ファイルの冒頭に「このファイルがスケジュールと工数の唯一の出典である」と書いておく。**

積み上げ方も同じスクリプトに持たせる。顧客側の工数を別枠で手入力すると必ずずれる。

```python
CLIENT_RATIO = {"共": 0.5, "N": 0.10}     # 共同タスクは自社の半分、自社主担当はレビュー分
CLIENT_ONLY  = {"1.4": {...}, "3.7": {...}}   # 顧客主担当タスクは個別見積
BUFFER_RATIO = 0.15                        # 予備工数。切り上げ。フェーズには配分しない
```

---

## 複数プランは、すべてが目的を達成する形にする

期間と費用で A/B/C を作るとき、**安い案がフェーズの前半だけを切り出した形になってはいけない。**
「A では目的を達成したと言えない」ものを選択肢として出すと、実質 1 案しかないのと同じである。

```
✗ 入れ子:  A = 仕様策定まで / B = A + 実装と証明 / C = B + 評価と公開
✓ 深さ:    A/B/C いずれも 仕様 → 実装 → 検証 → 公開 を通す。成果物も全部揃う
           変えるのは対象の広さ（範囲・種別・サポートする定義の数）と検証の深さ
```

深さで差をつけると、比較表の行はこうなる。

| | A | B | C |
|---|---|---|---|
| 対象の広さ | 1 通貨ペア・指値のみ・定義 1 種類 | 複数ペア・成行を含む・定義 2 種類 | B + 障害耐性・記録の再生・精度測定 |
| 成果物 | D1〜D4（すべて） | D1〜D4（すべて） | D1〜D4（すべて） |
| 到達点 | 最小構成で作り、証明して公開する | 実運用に近い構成まで広げる | 実用性を数値で示す |

**どのプランで止めても中途で終わった形にならないこと**を、費用の章に明記する。
例外（リスク発動時に途中で終了する条件）があるなら、比較表に例外行として出す。

---

## 「予備実験」は、WBS へ入れる前に消せないか試す

「着手直後に予備実験を行う」と書いたタスクが 8〜10 人日を占めることがある。
その多くは、**公開情報を読めば実験せずに片が付く**。

先に読む:

- 顧客の API ドキュメント（注文種別、状態遷移、エラー、レート制限、配信保証）
- 顧客が公開している OSS 実装のソース（実際に何を検証しているか）
- 採用予定ライブラリのソース（型の精度、拡張の制約、公開 API）
- 依存する仕様の原文

読んだ結果は、提案書に「**公開情報で確認済みの事項**」の表として載せる。

| # | 確認したこと | 確認の根拠 | 帰結 |
|---|---|---|---|
| 1 | 現行の確認トークンに累計の概念は無い | 公開ソースの該当ファイル。検証はパラメータ一致と有効期限のみ | 主張は成立する |
| 2 | 注文訂正のエンドポイントが無い | REST API に amend 相当が無い | 状態機械に訂正イベントを置かない |
| 3 | 執行イベントは順序保証が無い | ドキュメントに明記。シーケンス番号も無い | スナップショット更新が必須になる |

効果は 3 つある。**工数が減る**（実験タスクが消える）。**初速が上がる**（着手時に前提が揃う）。
**調べてきたことが伝わる**（顧客の実装を読んだ提案は、読んでいない提案と明確に違って見える）。

残った不確実性だけを、目的・入力・判定条件つきの実験タスクとして WBS に置く。
