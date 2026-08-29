# Client-ready rules

The test for every sentence: **would this be fine if the client's procurement lead read it aloud
in a meeting?** If it exposes how the document was made, defends your pricing, or reads like it
came out of a model, cut it.

These rules were derived from an actual enterprise engagement where an independent reviewer's
verdict on the first draft was 「要修正」 with the note that internal-facing text and pricing gaps
alone would stop it at procurement.

---

## 1. Meta text

Anything that talks *about* the document rather than *to* the reader.

| ✗ | ✓ |
|---|---|
| 本書の目的は、実施内容と体制を整理することです | （削除。目次と各章が示している） |
| 以下に、3 つの観点から整理します | 実施内容は次のとおりです |
| このセクションでは〜について説明します | （見出しが既に示している） |
| ※ 本表は説明のために簡略化しています | （簡略化しない、または簡略化した事実を注記せず正確に書く） |

Legitimate exception: a disclaimer that the client needs in order to read the content correctly —
「説明のために作成した例です。実際の対象システムの仕様に基づいて生成します」 is not meta text,
it is a factual scope statement about a figure.

## 2. Revision history and version diffs

Never ship evidence that an earlier version existed.

| ✗ | ✓ |
|---|---|
| 当初案では 25 点の成果物を想定していましたが、10 点に集約しました | 最終成果物は 10 点です |
| ### 前回ご提示案からの変更点（差分表） | （章ごと削除） |
| 成果物の絞り込みにより工数は 4.25 人日減少しています | （書かない。確定値だけ示す） |
| 当初案はバッファを含まない理想値でした | （書かない） |

The reasoning belongs in the repo. A commit message is the right home for
「ロール別の稼働率がタスク積み上げと整合していなかったため補正」.

## 3. Internal cost defence

The client does not care about your production cost, and saying it invites scrutiny of your price.

| ✗ | ✓ |
|---|---|
| 文書点数を増やすと当社側の作成工数が増えます | 受入とその後の運用に必要なものに絞っています |
| 監査証跡は自動生成のため追加の作成工数が発生しません | 監査証跡は、要約や再編集をせず実行時に生成された形のまま納品します |
| 形式手法エンジニアの工数は削減していません | （書かない。工数表が示している） |
| これは追加請求を避けるための措置です | この揺れをあらかじめ見込んだうえで、上限を定めています |
| 文書作成に充てるはずであった工数は検出に充当します | 継続してご利用いただく資産は D-02〜D-04 に収録します |

Rewrite rule: **replace the cost statement with the client-side benefit it produces.**

## 4. Self-criticism and hedged apologies

A proposal that criticises itself has already lost. If something was wrong, fix it silently.

Also avoid pre-emptive defensiveness — 「本手法は万能ではありませんが」「限界はありますが」.
State the scope positively: 「本 PoC で形式化するのは中核の不変条件 5〜10 本に限定します」.

## 5. AI tells

The reviewer flagged these by name. Japanese business writing that reads as machine-generated:

| Tell | Fix |
|---|---|
| Same sentence ending repeated 20+ times in a row | Vary; prefer plain です・ます |
| 過剰敬語: でございます / 申し上げます / 存じます | です / します / 考えます |
| 「〜という点でございます」 | 「〜です」 |
| Long compound sentences with three subordinate clauses | Split into two or three sentences |
| Mechanical enumeration where prose would do | Use a table if it is data, prose if it is argument |
| Empty intensifiers: 極めて / 非常に / 大変 | Delete, or replace with the number |
| Over-hedging: 〜と考えられます / 可能性がございます stacked | Commit or state the condition |
| Parallel structures too perfect ("第一に…第二に…第三に" everywhere) | Fine once; not in every section |

Quick audit before shipping:

```bash
# count the offenders in the extracted text
for w in でございます 申し上げ 存じます おります 極めて 非常に; do
  printf "%6d  %s\n" "$(grep -o "$w" dump.md | wc -l)" "$w"
done
# sentence-ending distribution — a single ending over ~15% of long sentences is a smell
python3 -c "
import re,collections,sys
t=open('dump.md',encoding='utf-8').read()
s=[x for x in re.split(r'[。\n]',t) if len(x)>25]
for e,c in collections.Counter(x[-6:] for x in s).most_common(10): print(c,e)"
```

## 6. Overclaiming

Every unqualified superlative is an invitation to be asked for proof.

| ✗ | ✓ |
|---|---|
| パターン照合では原理的に検出できません | 仕様や業務文脈を与えないパターン照合だけでは単独で捉えることが難しい領域です |
| 〜を採っているのは当社のみです | 当社が確認した公開情報の範囲では、同様の構成は限られています |
| 公開ベンチマークで最高水準の精度 | 公開ベンチマーク X で精度 88.9 パーセント |
| 4 週間で確実に完走できます | 前提条件が満たされていれば、4 週間での完走可能性が最も高い構成です |
| 形式化が最も容易な領域です | 本手法の対象としては形式化の負荷が小さい領域です |
| 日本人として唯一 Top20 に入賞 | Top20 に入賞 |

Replace the superlative with **the number** or **the condition**. Both are stronger.

Special case — **do not disparage the client's existing tooling**. They bought it. Frame as
補完: 「既存の静的解析・動的解析と併用することを前提としています」.

## 7. Claims about what your method proves

The most dangerous overclaim is a technical one, because it becomes a contractual promise.

- A formal proof guarantees a property **within the formalised model**, not in the production
  implementation. Say so, and name the工程 that connect the two
- A failed proof is **not** a vulnerability. It can also mean the model is incomplete, an assumption
  is unstated, or the correspondence is wrong. Define a candidate → confirmed pipeline and only call
  something confirmed after independent reproduction
- "0 findings" means "no confirmed findings reproduced within the defined scope", never "it is safe"

Write the judgement table explicitly:

| 結果 | 扱い |
|---|---|
| 成立 | 明示した前提およびモデルの範囲で、当該性質は成り立つと判断します |
| 不成立（反例あり） | 候補とし、審査と再現検証にかけます |
| 不成立（論証に欠落） | 候補とし、モデル・前提の不足か実装の欠陥かを切り分けます |
| 未完了 | 未確定事項として、理由とともに報告します |

## 8. Gate and success-criteria hygiene

- A gate named 「所見確定」 that fires **before** reproduction is a contradiction. Name gates for
  what is actually true at that moment (候補所見の確定 → 確定所見の確定)
- A rate defined as "confirmed findings that reproduced ÷ confirmed findings" is circular.
  Define the denominator as the candidate set
- Every indicator needs a **zero case**: 「候補が 0 件の場合は本指標を適用せず、未達とはしません」
- If a phase's inputs are produced by a later gate, the phase dates are wrong. Split it:
  preparation before the gate, execution after

## 9. Financial-institution specifics

A proposal to a bank or insurer is read by risk and compliance too. Include:

- **作業規則** as contract terms, not "to be discussed at contract time": prohibited operations
  (scoped to production, so that patch work in an isolated branch is not accidentally banned),
  least-privilege access, work-log retention, immediate reporting of critical findings with a
  deadline, incident notification deadline, subcontracting policy, data residency, backup erasure
  with certificate, liability, background IP
- **Standards mapping** offered as an 対応整理資料 with an explicit non-guarantee:
  「対応関係を整理したものであり、準拠または適合を保証するものではありません」.
  Decide the requirement at the first gate, not "if requested"
- **Data handling**: production data never touched; synthetic or anonymised only

---

## Pre-flight checklist

Run before every generation:

```
[ ] 「当初案」「前回」「初版」「改訂」「差分」 が本文にゼロ
[ ] 「当社側の工数」「追加請求」「削減しました」 がゼロ
[ ] でございます / 申し上げ / 存じます がゼロ
[ ] 「唯一」「最高」「確実に」「原理的に」「最も」 が無条件で使われていない
[ ] 外部数値がすべて出典表に載っている
[ ] 同一概念の数値が文書内で一致している
[ ] タスク積み上げ = ロール別工数、capacity 内に収まっている
[ ] 会議時間と人日の包含関係が明示されている
[ ] 各指標に 0 件時の扱いがある
[ ] ゲート名が、その時点で真であることを表している
[ ] 単価欄を客に書かせる表がない
[ ] 見出しに outline level がある
[ ] 図が白黒で読める
[ ] 全 PNG を目視した
```

---

## 内部の痕跡は、本文だけでなく図とキャプションにも残る

「source docs は出荷しない」を守っていても、次の経路で漏れる。実際に漏れた。

- **図のフッタに出典として `notes/xxx.md` と書いてしまう。** 図を作るスクリプトのコメントから
  そのまま持ってきてしまうのが原因。図の出典は、顧客が確認できる正式名称か URL で書く
- 表の脚注、キャプション、`![FIG:key]` のようなプレースホルダ名
- 「v1.1 で入った」「前回ご提示から」のような版間の差分への言及
- Issue 番号、ブランチ名、生成スクリプト名、レビュー記録の名前

`preflight_check.py` が `notes/` `out/` `bin/` とソースファイル名を検出する。ただし
**相手方の公開リポジトリを証拠として引用するのは痕跡ではない**（むしろ調べた証拠になる）。
URL を伴う引用は除外している。

---

## AI が書いた気配は、文体ではなく「文書が自分に言及すること」で出る

過剰敬語や語尾の単調さより先に、次の型が疑われる。**書き手の思考過程が本文に残っている**状態で、
読み手には要らない情報である。

```
✗ 順序はこうです。まず〜
✗ 最初に比較の限界を書いておきます。
✗ 本節は本提案で最も強い主張を含むため、根拠を分解して示します。
✗ ここは順序が大事なので、先に断っておきます。
✗ 用語の問題を切り分けておきます。
✗ 確認した範囲を具体的に書きます。
✗ ここでは〜を整理します。／以下、〜を示します。
```

いずれも**その一文を消すだけで文意が通る**。通らないなら、本文が説明不足なので中身を直す。

`preflight_check.py` の `AI_TELL` に検出パターンを置いてある。文書の性格に合わせて足す。

---

## 相手に判断を丸投げして終わらない

弱点を正直に書くことと、判断を相手に投げることは別である。

```
✗ 枠をどこまで広げるかは御社の事業判断です。
✓ 上限が守られる保証が無い状態では、実際に消費されうる額は委譲枠を超えて広がりうるため、
   渡す側が確実に効かせられる調整は口座に置く額そのものを絞ることになります。
   上限が守られることを示せれば、委譲枠が実効的な歯止めとして機能します。
```

**構造として説明できるなら説明する。** そのうえで、断定できない部分（時期、幅、需要）だけを
条件として残す。「御社の判断です」で終わる段落は、たいてい論証をサボっている。

---

## 用語は読み手の職掌に合わせる

同じものでも、業界の実務者が使う語がある。初出で言い換えを添える。

| 一般語 | 取引所の実務者に通じる語 |
|---|---|
| データ | マーケットデータ（相場情報・指数） |
| 接続 | コロケーション・接続回線 |
| 認可層 | 参照モニタ／注文経路上の統制 |

**位置関係を「前段／後段」で書かない。** 読み手によって逆に取られる。
「A と B の間に置く」と書く。実際にこれで、図と本文が 6 版にわたり矛盾したまま残った。
