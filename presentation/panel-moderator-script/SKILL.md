---
name: panel-moderator-script
description: |
  Write a run-of-show script a moderator can read aloud on stage — opening, panelist
  introductions, curated questions, audience Q&A, close — for panel discussions, conferences,
  and MC'd events, then harden it through a recursive external-agent review loop until an
  independent reviewer stops finding defects. Combines the broadcast-newsroom script grammar
  (toss / tag / tease) with Kristin Arnold's Powerful Panels task order. The core move is the
  **受け (tag)**: restating each answer in the audience's words — without it a panel becomes
  three experts talking while 200 people listen sideways. Also covers spoken-Japanese register
  (no bold in read-aloud text, one breath per sentence), a hand-raise device in the opening that
  is paid off in the close, question design that is sharp *and* answerable by listed-company and
  regulated-industry speakers, timing arithmetic that actually sums to the slot, and separating
  the speaker-facing page from the moderator's private notes. Trigger on: 「司会台本」「進行台本」
  「モデレーター台本」「パネルの質問を作って」「run of show」「MC script」「登壇者に送る進行案」,
  or any request to turn a session outline into something a host reads on the day.
---

# Panel moderator script

**A list of questions is not a script.** It is the single most common failure: the moderator asks,
the panelist answers, the moderator asks the next question. Nothing is restated, nothing is
translated, and the audience watches a private conversation.

This skill produces two artifacts that must not be mixed:

| # | Artifact | Who reads it | Contains |
|---|---|---|---|
| 1 | **司会台本** (repo `.md`) | The moderator, on stage | Read-aloud lines **plus** private prep notes in collapsed toggles |
| 2 | **登壇者ページ** (Notion / doc) | The speakers, in advance | Read-aloud lines **only** — never the prep notes |

Row 2's exclusion is not cosmetic. Prep notes legitimately contain things like *"this panelist is at
a listed securities firm and cannot answer 御社では questions"* and *"if the moderator is from our
side, do not let this sound like a pitch for our own proposal."* Those are correct notes to write and
catastrophic to publish. See `references/artifact-split.md`.

---

## Workflow

Eight phases. Do not collapse 3 into 5 — writing spoken lines before the questions are settled
produces prose that then has to be re-cut, and the re-cutting is what leaves the AI seams.

### 0. Intake

Ask the unanswered ones in one batch, propose a default, start on defaults if told 「任せる」.

| # | 確認事項 | 既定値 |
|---|---|---|
| 1 | 枠の長さと開始時刻 | — 必須。時間配分の全部がここから決まる |
| 2 | 登壇者の確定状況（氏名・所属・確定/打診中） | 打診中は台本に入れるが、紹介と問いを **1 組で** 外せる形にする |
| 3 | 形式（パネル / 単独講演 / 5 名以上） | パネル。**5 名以上なら 1 人 1 問に切り替える**（下記） |
| 4 | 使用言語と字幕の有無 | 日本語・正面スクリーンに字幕 |
| 5 | 客席の構成（職掌の比率） | — 必須。持ち帰りを誰向けに書くかが決まる |
| 6 | 登壇者のスライドの有無 | なし。**あるなら転換の秒数を別に取る** |
| 7 | モデレーターは誰か | — 未定なら台本は叩き台。**本人の言い回しに直す前提で書く** |
| 8 | 触れられない領域（守秘・上場・係争） | — 必須。ここを聞かずに書くと、当日「答えられません」で進行が止まる |
| 9 | レビュー担当エージェント | `codex exec` |
| 10 | 既存資料（ブリーフ・過去の質問リスト） | あれば先に読む。**置き換えるなら旧版はトグルに畳んで残す** |

### 1. 骨格を決める

`references/frameworks.md` の task order を枠の長さに割り付ける。**合計が枠に収まることを
`assets/timing_check.py` で検算する。**見出しに分数を書いていない区間（会場質疑を書き忘れる
のが定番）があると、合計が 8 分足りない台本ができあがる。

### 2. 質問を設計する

`references/question-design.md`。5 つの規準で作り、3 つの禁止に触れないことを確認する。
**この順番を逆にしない。**鋭さを先に作り、そのあと答えられるかを検査する。先に安全側から
書くと、二度と鋭くならない。

### 3. 一次情報で固有名詞を裏取りする

質問に製品名・数値・規制名を入れるなら、**入れる前に一次情報に当たる。**
台本は声に出すものなので、誤りは登壇者の目の前で露見する。実例は
`references/question-design.md` の「裏取りの失敗例」。

### 4. 声に出す文を書く

`references/spoken-japanese.md`。**読み上げ文に太字を入れない。**一文は読点で息継ぎできる長さ。
地ならし・フリ・受け・つなぎ・予告の 5 動作で組む。**受けを書き忘れるのがいちばん多い欠陥。**

### 5. 機械検査

```bash
python assets/timing_check.py script.md      # 本編 ＋ 予備 ＝ 枠
python assets/spoken_check.py script.md      # 太字・長文・受け・地ならし・挙手の欠落
```

**両方が exit 0 になるまで直す。**目視では 100% 見落とす。

**時間の規約は「本編 ＋ 予備 ＝ 枠」。**本編だけで枠を埋めない。既定の予備は 2 分
（`--reserve` で変える）。予備を食いつぶす配分は、検査上「収まっている」とみなさない。

**形式が違うセッションは検査を外せる。**本文にマーカーを置く。

```
<!-- checks: skip -->                     このセクションを検査しない
<!-- checks: no-hands, no-clap -->        挙手・拍手の検査だけ外す
```

`no-hands` / `no-clap` / `no-call` / `no-setup` / `no-tag` が指定できる。
**行数で自動的に除外しない。**短い枠ほど無検査で通ってしまう。

### 6. 再帰的外部レビュー

`references/review-loop.md`。**3 視点（登壇者・参加者・進行）で回す。**
**必ず「鈍化していないか」のラウンドを入れる。**これを入れないと、レビュアーは質問を安全側に
倒し続け、最終的に当たり障りのない台本が「合格」になる。

**打ち切り条件（これを書かないとループが終わらない）**

| | |
|---|---|
| 上限 | **3 ラウンド。**超えるのは、新しい実害が出続けているときだけ |
| 合格 | 「当日読み上げて実害が出る指摘」が **2 ラウンド連続でゼロ** |
| 強制終了 | 指摘が「もっと詳しく定義すべき」「網羅性」「文体の好み」の水準に移ったとき |
| 差し戻し | 修正して指摘が減らないなら、直しているのは症状。**構造（枠の配分・質問の立て方）を変える** |

**未解決のまま残した指摘は、依頼者に渡す。**勝手に握り潰さない。

### 7. 分配

司会台本は repo。登壇者ページは Notion / doc に、**prep notes を外して**転記。
既存のブリーフがあれば `<details>` に畳んで残す。消さない。

---

## 5 名以上なら構成が変わる

40 分に 5 名なら 1 人 8 分。**共通質問は成立しない。**第 2・第 3 ラウンドを作らず、
**1 人 1 問、その人にしか答えられないもの**を用意する。追い質問は 1 回まで。
2 回目を入れると必ず溢れる。

| 人数 | 第 1 ラウンド | 第 2 | 第 3 |
|---|---|---|---|
| 2 名 | 各 5〜6 分 | 割れる論点 | 全員に同じ 1 問 |
| 3 名 | 各 4 分 | 割れる論点 | 全員に同じ 1 問 |
| 4 名 | 各 3 分 | 割れる論点（短く） | 落とす |
| **5 名以上** | **各 5 分・1 人 1 問** | **作らない** | **作らない** |

---

## 形式が違えば、装置も変える

**挙手と拍手は、対面・大人数・くだけた場を前提にした装置。**そのまま持ち込まない。

| 形式 | 挙手のかわり | 拍手 |
|---|---|---|
| 対面・50 名以上 | そのまま挙手（2 段構え） | 促す |
| 対面・20 名以下 | **挙手させない。**「◯◯の方、いらっしゃいますか」と目で確認する | 促さない。不自然になる |
| オンライン | チャットに一言、投票機能、リアクション | 「チャットに拍手を」 |
| ハイブリッド | **会場とオンラインの両方に振る。**片方だけだともう片方が疎外される | 両方に促す |
| 追悼・表彰・厳粛な場 | **参加型の装置を使わない。**地ならしだけ置く | 式次第に従う |

**挙げにくい挙手を設計しない。**「失敗したことがある方」「規制違反を経験した方」は、
挙げたら不利になる。**挙げても損しないものだけ**を聞く。

## 絶対に守る 5 つ

1. **受けを飛ばさない。**答えを客席の言葉に置き直す。専門語が出たら、その場で一拍おいて言い換える
2. **読み上げ文に太字を入れない。**声に太字はない。書き物の体裁のまま喋らせない
3. **冒頭で挙手をさせ、締めで回収する。**60 秒で客席が自分ごとになるかが決まる。**回収すると枠がひとつにまとまる**
4. **拍手を促す。**言わないと客席はタイミングを迷う
5. **答えられない質問を投げない。**返ってくるのは一般論で、**鈍い質問と同じ結果になる**

---

## References

| File | 内容 |
|---|---|
| `references/frameworks.md` | toss / tag / tease と Powerful Panels の task order、5 動作の定義、時間配分の式 |
| `references/spoken-japanese.md` | 声に出す文の書き方。AI 臭の 8 つの兆候と、それぞれの直し方 |
| `references/question-design.md` | 5 つの規準と 3 つの禁止。鋭さと答えやすさを両立させる書き換え表 |
| `references/artifact-split.md` | 司会台本と登壇者ページの分け方。何を出して何を出さないか |
| `references/review-loop.md` | 3 視点 × 再帰レビュー。**反鈍化ラウンド**の設計と打ち切り条件 |

| Asset | 用途 |
|---|---|
| `assets/timing_check.py` | 区間の合計が枠に収まるかを検算。会場質疑の書き忘れを検出 |
| `assets/spoken_check.py` | 読み上げ文の太字・長文・受けの欠落・地ならしの欠落・挙手の欠落を機械検出 |

**この skill の中の例は、実際に使った台本から取っています。**製品名・金額・年・人数は
そのイベントのもので、**そのまま別のイベントに持ち込むと嘘になります。**
`[製品名]`『[金額]』のように読み替えて、**一次情報で取り直してください。**
