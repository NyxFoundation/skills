# Recursive external review

The draft you write is not the deliverable. The deliverable is what survives an independent agent
trying to kill it. Budget 4–7 rounds.

Use an agent that **did not author the document**. Self-review finds typos; a fresh reviewer finds
the contradiction between chapter 3's effort total and chapter 10's estimate table.

---

## Mechanics

### Extract the text first

Reviewers cannot read `.docx`. Dump it, keeping table structure:

```python
# extract_docx_text.py
import zipfile, sys
from xml.dom import minidom

z = zipfile.ZipFile(sys.argv[1])
d = minidom.parseString(z.read("word/document.xml"))

def txt(n):
    return "".join("".join(c.data for c in t.childNodes if c.nodeType == c.TEXT_NODE)
                   for t in n.getElementsByTagName("w:t"))

lines = []
for el in d.getElementsByTagName("w:body")[0].childNodes:
    if el.nodeName == "w:p":
        t = "［図］" if el.getElementsByTagName("w:drawing") else txt(el)
        if t.strip():
            lines.append(t)
    elif el.nodeName == "w:tbl":
        lines.append("")
        for tr in el.getElementsByTagName("w:tr"):
            lines.append("| " + " | ".join(txt(tc).strip()
                         for tc in tr.getElementsByTagName("w:tc")) + " |")
        lines.append("")
print("\n".join(lines))
```

Also validate every XML part while you are there — a malformed part means the file will not open:

```python
for n in z.namelist():
    if n.endswith(".xml"):
        minidom.parseString(z.read(n))     # raises on corruption
```

### Invoke the reviewer

```bash
cd <dir containing proposal_dump.md>
timeout 1500 codex exec --skip-git-repo-check -c model_reasoning_effort="high" \
  "$(cat review_prompt.txt)" < /dev/null > review.txt 2>&1
```

- **`< /dev/null` is mandatory.** Without it, `codex exec` detects non-TTY stdin, prints
  `Reading additional input from stdin...`, and exits having done nothing
- Put the prompt in a file. Heredocs inside `$( )` inside a backgrounded shell get mangled
- Run it in the background; a high-effort review of a 40k-character document takes 5–15 minutes
- Reference the file by name in the prompt — the agent reads it from its working directory

Alternatives: hermes, or a Claude subagent with a read-only toolset. Any agent with no memory of
writing the document works.

---

## Prompt design

### Round 1 — find everything

```
<file> は <client type> に提出予定の <document type> の全文テキストです
（Word から抽出。表は | 区切り）。

あなたは (a) 調達・セキュリティ担当 と (b) 提案側の事業責任者 の両方の視点を持つ厳しい
レビュアーです。この文書は「そのまま先方に提出する」ものです。
提出して恥をかく箇所、契約を打ち切られる箇所を容赦なく指摘してください。

【A. 提出可否に直結する致命傷】最優先
- 社内向けのメタ記述、改訂履歴、過去バージョンとの差分、自己批判、言い訳
- AI が書いたと分かる不自然な日本語（同じ言い回しの反復、機械的な列挙、過剰な hedging）
- 相手に失礼／卑屈すぎる箇所、提案側の内部事情が透けている箇所
【B. 論理】背景の問題設定に対して解決策が答えになっているか。飛躍の指摘
【C. 数値の整合性】章をまたいだ矛盾を具体的に
【D. 実行可能性】期間・要員・クリティカルパスに無理はないか
【E. 欠落】当然あるべきなのに書かれていない項目

出力は日本語。A を最優先に重要度順で最大 12 件。
各指摘は「指摘」「該当箇所（章番号や原文の引用）」「推奨する修正」の3点セット。
最後に「このまま提出可 / 軽微修正で提出可 / 要修正」で総合判定を1段落。
```

### Rounds 2..n — verify the fixes

**Feed the previous round's fix list into the prompt.** This is the highest-leverage detail in the
whole loop: it turns the reviewer from a re-deriver into a verifier, and surfaces fixes that were
applied incompletely.

```
これは前回のレビュー指摘を反映した改訂版です。

前回の指摘に対する対応は以下のとおりです。
1. <指摘> → <どう直したか>
2. ...

検証してください:
【A】上記 N 件が本当に解消されているか。不十分なものを具体的に指摘
【B】新たに混入した矛盾・重複・不整合（特に <今回変更した箇所> と既存章の整合）
【C】まだ残る「提出したら打ち切られる」レベルの記述

実害のある問題のみ、最大 <N-2> 件。
```

Shrink the cap each round (12 → 8 → 6 → 5 → 4 → 3). It forces prioritisation and signals convergence.

### Final round — verdict only

```
これは最終確認です。提出可否のみを判断してください。
提出を止めるべき実害のある問題が残っていれば最大 3 件挙げ、なければ「なし」と明記してください。
細かい精緻化の提案、文体の好み、さらに厳密にできる余地の指摘は不要です。
「このまま提出可 / 軽微修正で提出可 / 要修正」で総合判定を1段落。
```

Without the last two lines the loop never ends — a capable reviewer can always suggest one more
refinement, and each suggestion spawns another round.

---

## Triaging findings

**A finding is not automatically right.** Classify each one:

| Class | Action |
|---|---|
| **Correct** | Fix as recommended |
| **Correct diagnosis, wrong remedy** | Fix the underlying problem your way; note the divergence |
| **Conflicts with an explicit instruction from the requester** | Do **not** follow it. Satisfy the concern another way, and report both the finding and why it was declined |
| **Out of scope** (style preference, further refinement) | Decline; tighten the next prompt |

Worked example of the third class. The reviewer said "an empty 単価 column makes the document unusable
for procurement — insert the contract amount". The requester had explicitly asked for a
user-editable unit price. Resolution: **remove the price columns from the document body entirely**
(so it no longer asks the client to fill anything in), state effort as a fixed value, move price to a
separate 見積書, and keep the editable input cells in the workbook. Both constraints satisfied.

### Findings that recur across engagements

Fix these pre-emptively; they are the reviewer's reliable hits.

1. **Effort tables that do not reconcile** — task rollup vs. role table vs. estimate
2. **Overclaiming a method's guarantee** — "proof failed ⇒ vulnerability", "0 findings ⇒ safe"
3. **Gates named for a state that is not yet true** at that point in the schedule
4. **Circular indicator definitions** — a rate whose denominator is the numerator's own filter
5. **No zero case** for count-based indicators
6. **Internal cost defence** left in the body
7. **Colour-only Gantt bars** (invisible in B&W)
8. **Meeting hours that do not reconcile** with the person-day total
9. **A phase that starts before the gate producing its inputs**
10. **Cross-reference drift** after renumbering chapters — check 付録 A/B/C references especially

### Renumbering discipline

When inserting a chapter, renumber **in descending order** (13→14, 12→13, …) so replacements do not
collide, and sweep the in-text cross-references (「6.3 をご参照ください」「7.2 の観点により」) in the
same pass. Then grep for stale numbers.

---

## Convergence

A healthy trajectory:

```
R1  要修正 — 12 件   (price, blank Gantt, internal text, AI tone, overclaim, ...)
R2  要修正 —  8 件   (fixes verified; new inconsistencies from the edits)
R3  要修正 —  6 件   (gate semantics, Lean guarantee scope, cost language)
R4  要修正 —  5 件   (circular metric, phase/gate ordering, zero findings framing)
R5  要修正 —  4 件   (gate zero-case, existing-tooling conclusion, env deadline)
R6  要修正 —  3 件   (whole-run judgement at zero, conditional reproduction, guarantee wording)
R7  このまま提出可 — 実害のある問題：なし
```

If the count stops dropping, you are fixing symptoms. Re-read the finding class — usually a
structural decision (gate design, deliverable set, what the method claims) needs changing, not wording.

If the reviewer keeps producing *new* findings in areas it previously passed, your edits are
introducing regressions — re-extract and diff the dump between rounds.

---

## Reporting the loop

Tell the requester the truth about it: how many rounds, what the verdict was, and which findings you
declined and why. The round count is evidence of rigour, not of a weak first draft.

Never claim a review verdict you did not receive, and never paraphrase 要修正 as 軽微修正.
