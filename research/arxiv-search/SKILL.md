---
name: arxiv-search
description: >
  arXiv API を直接叩いて、関連研究をタイトル・著者・要約つきで一覧する。先行研究サーベイ、
  research issue の裏取り、論文の Related Work を埋める作業の入口。Web 検索より再現性が高く、
  クエリを構造化できる（ti: / au: / cat: / all: を AND OR で組む）。
tags: [arxiv, literature-review, related-work, research]
---

# SKILL: arxiv-search

## 使い方

```bash
python3 scripts/arxiv_search.py 'all:"AI alignment" AND all:economy'
python3 scripts/arxiv_search.py -n 10 --sort-by submittedDate 'ti:"formal verification" AND cat:cs.CR'
python3 scripts/arxiv_search.py --json 'all:singleton AND all:AI' > hits.json

# 複数クエリを一度に（ラベルは順に対応）
python3 scripts/arxiv_search.py \
  --label 'singleton理論' --label 'エージェント交渉' \
  'all:singleton AND all:AI' 'all:autonomous AND all:agent AND all:negotiation'
```

**`uv run --no-project` では走らない。** その環境には CA 証明書が無く、arXiv への HTTPS が
`CERTIFICATE_VERIFY_FAILED` で落ちる。このスクリプトは標準ライブラリだけで書いてあるので、
システムの `python3` でそのまま動く。

## クエリの組み方

| 接頭辞 | 対象 |
|---|---|
| `all:` | 全フィールド |
| `ti:` | タイトル |
| `abs:` | 要約 |
| `au:` | 著者 |
| `cat:` | カテゴリ（`cs.CR` `cs.LO` `cs.MA` など） |

- フレーズは `all:"multi-agent"` のようにダブルクォートで囲う。囲まないと語がバラける。
- `AND` / `OR` / `ANDNOT` は大文字。
- 網羅性が要るときは**同じ概念を別の言い回しで複数クエリに割る**。arXiv の検索は語形の揺れを
  吸収しないので、1本の完璧なクエリより 3〜5 本の角度違いのほうが取りこぼさない。
- 新しさが要るなら `--sort-by submittedDate`、定番を拾うなら既定の `relevance`。

## 出力の使い道

`--json` で出したものを、そのまま research issue の下地にする
（→ `research/research-idea-to-github`、`research/blockchain-formalization-research`）。

## 落とし穴

- **arXiv API はレート制限がある。** 連続で叩くと 5xx が返る。クエリ間に間隔を置く。
- 検索は arXiv 内部のインデックス依存で、**Google Scholar のような網羅性は無い**。
  査読済みの版や非 arXiv の文献は別途取りに行く。
- 要約は既定で 400 字に切っている。全文が要るときは `--summary-chars 0`。
