---
name: native-pptx-deck
description: >-
  Create, revise, and simplify editable PowerPoint (.pptx) decks with python-pptx,
  evidence-led presentation design, concise copy, and rendered visual checks.
  Use for PowerPoint authoring, pitch decks, lecture decks, and requests to make
  difficult slides easier to understand. Preserve an existing deck's intent and
  manual edits. For an existing Slidev or HTML source, retain that authoring format
  unless a native editable PPTX is requested.
---

# Native PowerPoint decks

読み手が解読せずに要点をつかめる、編集可能なPPTXを作る。投影用の短い画面と、話す内容・配布用の詳細を分ける。

見出し・ラベル・数値は原則として編集可能なオブジェクトにする。実物のスクリーンショット、写真、外部の原図は画像でよい。スライド全体を画像で包む方式とは区別する。

## 最初に守ること

- **依頼者が伝えたい内容を変えない。** 分かりやすくするための構成変更と、目的のすり替えを区別する。例えば「侵入後の損失を制限する」を「検知を速める」へ置き換えない。
- **1枚につき、理解してほしいことを1つ。** 主張に合う証拠を先に選び、必要なら結果・実例の次に仕組みを置く。章全体を一律の順序にはめない。
- **読める・単純・一目で分かる。** 見出し、主視覚、解釈に必要な直接ラベルへ絞る。説明文や抽象図を増やして解決しない。
- **固有名詞、数量、利用者の動作で書く。** 見出しは具体的な主張を基本とし、表紙・節扉・対象の紹介では短い名称も使う。文型・語数・枚数を目的にしない。
- **証拠には出所と文脈を残す。** タイトルだけの切り抜き、全文を読めないサイズのスクショ、内容と関係のない写真では主張を支えられない。
- **短くしても真偽を変えない。** 母数・期間・補助の有無、候補と確定結果、説明用モデルと本番の実績、証明の前提を区別する。

これはYC等の原則を、講演・技術資料にも応用する編集方針。資金調達の章立て、5〜7枚、1枚15語、60pt等を全用途の義務にしない。出典と適用範囲は[一次資料](references/pitch-principles.md)を参照。

## 1. 依頼と正本を確認する

会話・既存資料から、聴き手、場、尺、投影か配布か、伝えたい結論、対象ページ、固定する文言、成果物と保存先を把握する。分かっている事項を再質問しない。重要な不明点だけ確認し、独立して進められる作業は続ける。

既存デッキでは対象ページを描画して見てから直す。手修正がある場合は[手修正とソースの同期](references/manual-source-sync.md)を先に行う。分割でページが増えたら元→新の対応を残す。利用者のノート・引用表記・公開範囲の指定を維持する。

## 2. 証拠とコピーを決める

コピーを書く前に[画面に置く言葉](references/slide-copy-rules.md)を読む。未確認の外部ルールを「YCの鉄則」として引用する場合は[一次資料](references/pitch-principles.md)で根拠を確認する。

作業に必要な範囲で、次を短く記録する。単純な1枚の修正に長い企画書は作らない。

| ページ | 聴き手に分かってほしいこと | 証拠・出典 | 見出し | 主視覚 | 残す限定 |
|---|---|---|---|---|---|

資料・リポジトリを読み、主張を支える部分まで確認する。研究・実装の例は[技術事例](references/technical-case-studies.md)、記事・投稿・製品画面は[証拠画像](references/evidence-images.md)を参照する。

視覚を選ぶ基準：

- **誰が発表したか・実在するか**：発行元、人物、記事の概要を含む実物。
- **何が起きるか**：入出力、設定値、修正差分、実際の実行結果。
- **どのくらいか**：同じ定義・単位で比較できるチャート。
- **どうつながるか**：関係そのものが主題なら図。抽象的な箱や矢印を具体例の代用にしない。

「抽象図を使わない」等の指定がある場合は守る。図が適切な場合だけ[型カタログ](references/slide-type-catalogue.md)を使い、版面を[レイアウト](references/layout-patterns.md)から選ぶ。すべての枚を図にする必要はない。

## 3. Native PPTXとして実装する

既存のテーマ・書体・プリミティブを再利用する。新規のデザイン層を組む場合は[design-system](references/design-system.md)を参照。Nyxの配色・書体はNyx用の既定値であり、他社資料へ強制しない。

- レイアウト・書体・OOXMLの処理と、各ページの内容を分ける。
- 文字が入らない場合は、内容を削る・分割する・版面を変える。自動縮小で隠さない。
- 投影では見出し32〜36pt、主要な要点24pt前後を出発点に、実寸の見え方で調整する。出所を示す画像内の小字を精読させない。
- 日本語にラテン書体の偽斜体を当てない。画像の縦横比を保つ。

折り返し・重なりは[layout-and-text](references/layout-and-text.md)、影・字間等は[OOXML](references/ooxml-workarounds.md)、インポート問題は[portability](references/portability.md)を必要時に読む。

## 4. 描画して、意味と見え方を確認する

[ビルド・描画・納品](references/build-and-delivery.md)の手順でPPTXからPDFとPNGを生成する。ビルド→描画→アップロードは依存順に完了を待つ。

- コンタクトシートで並びと重心を見て、対象の各PNGを開く。
- 見出しと日本語の要点だけで理解できるか。画像はその主張を実際に支えているか。
- コピーの短縮で目的や条件が変わっていないか。スクショに会社・人物・ツールの文脈があるか。
- 字切れ、スクショの途中で切れた文章、フッタとの衝突、無意味な余白埋めを直す。

`assets/selfcheck.py` はコピー・数字等の検査補助、`assets/preflight.py` はPPTXの移植性検査。機械検査だけで理解しやすさを保証しない。

複数枚の再構成、外部への配布、技術・数値の主張がある場合は、[レビュー](references/review-loop.md)に従い、根拠の確認とPNGだけの視聴者レビューを分ける。利用可能・許可された独立レビューを使い、実修正に結び付く指摘へ絞る。回数を固定しない。

## 5. 成果物をそろえて渡す

PPTX・PDF・必要なソースを同じ完成版から生成する。既に依頼されたDrive差し替え等は[納品手順](references/build-and-delivery.md)まで実行する。スキルの使用だけで共有変更・メール送信・外部公開を追加しない。

同じファイルの差し替えでは既存IDと共有状態を保ち、取得し直した内容を検証する。最終回答は変更範囲、確認したこと、成果物のリンクを簡潔に伝える。確認していないPowerPoint実機・Google Slidesの動作や、受けていないレビューを合格扱いにしない。

## 道具と参照

- `assets/nyx_design.py`：Nyx用のデザイン層の参考実装。
- `assets/render.sh`：PPTX→PDF→PNG・コンタクトシート。
- `scripts/render_pdf.py`：既存PDFからPNG・コンタクトシート。ImageMagick不要。
- `assets/measure.py`：文字・段落・画像数の目安。画像内の文字は数えられない。
- `assets/selfcheck.py`：対象ページを指定できる内容検査補助。
- `assets/preflight.py`：transform・図形寸法・OOXML順序・書体等の確認。
- `assets/png_to_pptx.py`：明示的に画像ラップでよい場合の別経路。Native編集可能とは呼ばない。
