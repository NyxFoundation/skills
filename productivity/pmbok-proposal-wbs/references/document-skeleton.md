# Document skeleton

The chapter structure below survived six rounds of external review for a 4-week engagement proposal
to a Japanese financial institution. Use it as the default and cut what does not apply — inventing a
structure per engagement is where turns get burned.

Two rules govern the split:

- **Source `.md` → repo. Chapters → client.** The source docs hold the reasoning; the chapters hold
  the address to the reader. Never let a source doc's framing leak into a chapter.
- **Write the source docs first.** Generating the docx from reasoning-laden prose means scrubbing,
  and scrubbing leaves seams.

---

## Source document set (private repo)

Ten files. Numbered so they read in order. `NN-name.md`.

| File | Holds | Feeds chapters |
|---|---|---|
| `00-background.md` | Why now. Market/technology shift, the problem framing, all external evidence **with sources**, and the secondary-benefit argument | 1, 5 |
| `01-executive-summary.md` | The one-page answer: what we prove, effort, success criteria, top-3 blockers, recommendation | 2, 10, 11 |
| `02-scope-and-assumptions.md` | Scope IN/OUT, method-depth definition (the expectation-setting doc), assumptions with their failure impact, data-handling policy | 2, 13, 14 |
| `03-wbs.md` | Phase table, task rows with DoD, gates with pass/fail actions, critical path, buffer policy | 3, 6, 7 |
| `04-gantt.md` | Calendar mapping, milestone table, client meeting slots, parallelism design intent | 7 |
| `05-deliverables.md` | Deliverable catalogue with acceptance criteria, the folding rules, handover repo layout | 4 |
| `06-team-raci.md` | Org chart, role definitions, RACI matrix, effort by role, meeting cadence, escalation | 6 |
| `07-target-selection.md` | How the client should choose the target: scoring criteria, category fit, recommended configurations, anti-patterns | 8 |
| `08-preflight-checklist.md` | Everything to confirm before quoting. Grouped A–G, with "impact if unanswered" | 9, 付録 B |
| `09-risks-kpi-nextsteps.md` | Risk register (L×I scored), success KPIs, post-engagement roadmap, abort criteria | 11, 12 |

`README.md` at the repo root: what the package is, the three questions it answers, deliverable list,
and pointers. This is also where the working notes about *why* decisions were made belong.

---

## Proposal chapters (client-facing docx)

14 chapters + 4 appendices. Adjust the count, keep the order — it follows how a procurement reader
builds understanding: why → what → how → what I get → what else → who → when → which target → what
you need from me → how much → how we judge → what next → how you protect my data → what is excluded.

| # | Chapter | Contents | Notes |
|---|---|---|---|
| 1 | ご提案の背景 | 1.1 経緯／1.2 環境の構造変化／1.3–1.4 業界動向（一次情報）／1.5 論点の統合／1.6 手法の位置づけ／1.7 課題認識 | Longest chapter. Earns the right to propose |
| 2 | ご提案の概要 | 2.1 位置づけ（諸元表）／2.2 手法概要（段階表＋判定表）／2.3–2.4 中核技術の解説（**図必須**）／2.5 既存施策との関係 | 2.3–2.4 is where a rendered figure replaces a code block |
| 3 | 実施内容 | 3.1 全体の流れ（フェーズ表・工数・ゲート）／3.2〜 各フェーズ = 目的・詳細・作業表・成果物・承認ゲートの5点セット | Same 5-part shape for every phase |
| 4 | 成果物 | 区分（A診断/B資産/C判断材料）／4.1 一覧（内包するもの列つき）／4.2 構成方針／4.3 中間成果物 | 「絞り込みの経緯」ではなく「構成方針」 |
| 5 | 副次的効果 | 効果一覧（成果物IDとの対応・発現時期）／各効果の説明／時間軸 | Optional. Include only if the method genuinely produces reusable assets |
| 6 | 実施体制 | 6.1 座組（体制図）／6.2 要員構成（工数）／6.3 分担オプション／6.4 会議体・エスカレーション | 6.2 must equal the WBS rollup |
| 7 | スケジュール | 7.1 全体（ガント表）／7.2 承認ゲート／7.3 ご出席をお願いする会議（内訳表つき） | Meeting hours must reconcile with client person-days |
| 8 | 対象の選定について | 8.1 考え方／8.2 評価観点（採点表）／8.3 種別ごとの適性／8.4 推奨構成／8.5 適さないもの／8.6 進め方 | Only when the client picks the target |
| 9 | 事前にご確認いただきたい事項 | 9.1 最優先3点／9.2 見積直結の8項目／9.3 全体構成 | Full form goes to 付録 B |
| 10 | お見積り | 10.1 工数（**単価欄なし**）／10.2 変動費／10.3 前提変動の影響 | Price goes to a separate 見積書 |
| 11 | 成功判定 | 定量指標（**0件時の扱いつき**）／11.1 検証コストの測定 | The zero case is always asked about |
| 12 | 本 PoC 後の展開 | 段階ロードマップ（費用構造の変化）／12.1 結果別の次アクション | |
| 13 | 情報のお取り扱いと作業規則 | 13.1 取扱方針／13.2 作業規則（契約条件として） | Mandatory for financial/public sector |
| 14 | 前提条件および対象外事項 | 14.1 前提（崩れた場合の影響つき）／14.2 対象外／14.3 手法の適用範囲 | 14.3 is the overclaim firewall |
| 付録 A | 用語のご説明 | 12〜15語。セキュリティ担当が読める粒度 | |
| 付録 B | 事前確認シート | 記入式。A〜G 区分、50〜60項目 | そのまま配れる形に |
| 付録 C | 対象評価シート | 候補×観点の採点表 | 8章とセット |
| 付録 D | 出典 | 該当箇所・内容・出典の3列 | 外部数値は全件 |

### Chapter-level invariants

- **1章の問題設定に、11章の成功指標が答えていること。** 「検証能力が不足している」と書いたなら、
  検証コストの改善が指標に入っていなければ論理が閉じない。レビュアーはここを突く
- **2.2 の判定表と 3章のゲート名と 11章の指標が同じ語彙**であること
- **3.1 の工数合計 = 6.2 の要員工数 = 10.1 の工数表**
- **各フェーズの成果物行が、4.1 の成果物IDを指していること**
- **5章を入れたなら、11章で「合否には含めないが参考指標として実測する」と明記**

---

## Workbook sheets (xlsx)

| Sheet | Contents |
|---|---|
| 表紙・凡例 | 諸元、シート構成、凡例（フェーズ色・ゲート・**入力欄**）、利用上の注意 |
| WBS・ガント | 全タスク行 + 条件付き書式ガント（19営業日）+ 予備工数行 + 合計 |
| 工数・見積 | 前提（稼働日数）／ロール別工数・単価入力・金額／予備工数（比率入力）／合計／変動費／前提変動の影響 |
| マイルストーン | ゲートID・名称・期日・判定者・通過条件・不通過時 |
| 成果物一覧 | No.・成果物・区分・形式・作成時期・受入基準・内包するもの |
| 会議体 | 会議・日程・所要・出席依頼者・目的 |

---

## What to reuse verbatim, what to rewrite

**Reuse:** the chapter order, the 5-part phase shape, the gate table columns, the deliverable
classification (A/B/C), the preflight grouping (A–G), the appendix set.

**Rewrite every time:** all prose, all numbers, the phase names, the figures. A proposal that reads
like a template is worse than one with a weaker structure — the client can tell.
