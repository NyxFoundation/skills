---
name: docx-proposal-filler
description: >
  自治体・ふるさと納税・補助金の提案書を .docx で仕上げるワークフロー。配布された原本様式の
  レイアウトを保ったまま本文を流し込む、Notion の長文と表を A4横の docx に変換する、スライド
  PNG から別冊の法人紹介資料を組む、の3経路をカバーする。「様式に流し込んで」「docx で出して」
  「提出用の Word にして」「補助金の申請書を作って」と言われたときに読む。
tags: [docx, python-docx, proposal, 補助金, 自治体, 提出書類]
---

# SKILL: docx-proposal-filler

## いつ使うか

提出先が **Word の原本様式を配っている** ときと、Notion や Markdown で書いた内容を
**提出用の体裁に落とす** とき。PDF で出せば済む場面では使わない（体裁の再現に手間がかかるため）。

役所・補助金の提出物は「様式のセル構造を壊さないこと」が実質的な合否条件になる。ゼロから
docx を組むより、**配布された原本を開いて中身だけ差し替える**ほうが安全で速い。

## 3つの経路

| やりたいこと | スクリプト | 方式 |
|---|---|---|
| 配布された原本様式に本文を流し込む | `scripts/fill_form_template.py` | 原本 .docx をコピーし、表のセルだけ書き換える |
| Notion / Markdown の長文と表を提出用 docx に | `scripts/notion_to_docx.py` | A4横・表フル幅で組み直す |
| スライド PNG から別冊の法人紹介資料を組む | `scripts/deck_to_profile_docx.py` | 画像 + 補足文を1ページずつ並べる |

いずれも実際の提出物（南砺市の実証事業）で通した実装。**そのまま動く汎用ツールではなく、
先頭の定数を差し替えて使う参照実装**として読むこと。各スクリプトの冒頭に、取得元のコメント
エンドポイント・入出力ディレクトリ・章マーカーが定数で置いてある。

```bash
# 原本様式への流し込み（SOURCE_DIR / OUTPUT_DIR / COMMENT_ENDPOINT を書き換えてから）
uv run --with python-docx python3 scripts/fill_form_template.py

# Notion の保存 JSON から A4横の docx
uv run --with python-docx python3 scripts/notion_to_docx.py <enhanced_markdown.json>
```

## 原本様式を壊さないための実装ルール

`fill_form_template.py` がこの塊。ここを踏み外すと、提出直前に表が潰れる。

- **セル内のネスト表は dxa の固定幅で指定する。** パーセント（pct）指定は、親セルに `tcW` が
  無い様式だと幅ゼロに潰れる。親セルの実幅を測って `total_dxa` を渡し、`tblGrid` も明示する
  （`set_nested_table_width` / `nested_column_percents`）。
- **`tblPr` の子要素は順序が決まっている。** 罫線や幅を後から足すと Word が読めない docx に
  なるので、書き換えたら `reorder_tblpr` で並べ直す。
- **セルは空にしてから書く。** `clear_cell` で既存の段落を落とさずに追記すると、原本のプレース
  ホルダ文言が残る。
- **日本語フォントは `w:eastAsia` を明示する。** `run.font.name` だけでは日本語部分に効かない。

```python
run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "ＭＳ 明朝")
```

- **書き出したら必ず検証する。** `validate()` が、原本に存在した見出し語が出力にも残っているか、
  ネスト表が全幅になっているかを数える。目視で開く前にここで落とす。

## Notion → docx で効く小技

`notion_to_docx.py` はこれらを実装済み。

- Notion の PDF エクスポートは**幅の広い表がはみ出す**。A4横（`WD_ORIENT.LANDSCAPE`）にして
  `table_full_width` で表を版面いっぱいに広げると読める体裁になる。
- 表のヘッダ行は `repeat_header` でページ跨ぎに繰り返す。
- 列幅は中身の文字数から `column_percents` で配分する。等幅にすると数値列が間延びする。
- 図は Notion 側の画像を落とさず、**ローカルで再生成した PNG を埋める**。解像度と日本語
  フォントを自分で握れる（→ `presentation/editorial-figures`、`presentation/arch-diagram`）。

## 提出前の内容監査（レイアウト検証とは別に必ずやる）

`validate()` が見るのは体裁だけで、**約束したことが本文に残っているか**は見ていない。
提出物は何度も書き直されるので、差し戻しで入れた一文が次の版で消える事故が起きる。
レンダリング結果の文字列に対して、正規表現のアサーションを並べたスクリプトを1本置き、
提出前に走らせる。docx を組む前の Markdown / Notion 原稿の段階で回すのが早い。

肝は**否定アサーションも書く**こと。提出物には「入っていてはいけない語」がある。

```python
checks = [   # (名前, 対象テキスト, 全部マッチすべきパターン)
    ("必要最低補助額", main, [r"必要最低補助額.*5,000\s*千円"]),
    ("工程と人月の対応", combined, [r"1人月.*20人日.*160時間", r"人月単価.*1,200"]),
]
negative = [ # (名前, 対象テキスト, 1つも出てはいけないパターン)
    ("内部経緯語なし", main + supplement, r"市側|フィードバック|指摘に対|修正方針"),
    ("提出物のメタ説明なし", main + supplement, r"転写用|本コメントは|資料1〜4には"),
]
```

- **数値は必ず正のアサーションに入れる。** 金額・人月・点数・単価は版を跨いで最も壊れる。
- **否定側に入れるのは、査読の内部事情と自己言及。** 「市側の指摘」「修正方針」のような
  推敲の痕跡、「本コメントは」のような提出物自身への言及は、完成版に残っていると減点になる。
- 落ちたチェック名を並べて `SystemExit(1)`。PASS/FAIL を全部出してから落とすと、
  1回の実行で直す箇所がまとめて分かる。

## 図のタイトルの流儀

行政・補助金・公式文書では、キャッチコピーではなく**内容と範囲がわかる説明的タイトル**を使う
（例:「補助額別の年間工程及び工程別人月」）。示唆や主張はサブタイトルか注記に置く。
詳細は `presentation/editorial-figures` の Conventions を参照。

## 落とし穴

- **`python-docx` は NixOS に入っていない。** `uv run --with python-docx python3 ...` で走らせる
  （→ `nixos-environment`）。
- 原本テンプレは**必ずコピーしてから触る**。上書きすると再ダウンロードになる。
- 長文を GitHub のコメントから取ってくる場合、シェルを経由させない。`gh api` の JSON を
  Python 側で読む（`get_comment_body`）。同じ理由で issue 側の更新は
  `personal/new-task/scripts/patch_issue_comment.js` を使う。
