# ビルド・描画・納品

読む場面：PPTXの実装、PDF/PNG生成、既存Driveファイルの差し替え。
ユーザーが依頼した成果物・保存先の範囲で行う。

## ソースと実装

既存プロジェクトの構造を保ち、デザイン層とページの内容を分ける。新規なら例えば：

```text
scripts/build-deck.py       内容・構成
scripts/design.py           トークン・グリッド・OOXMLヘルパ
assets/evidence/            元資料と来歴
out/deck.pptx
out/render/                 PDF・ページPNG・contact.png
```

Pythonスクリプトの依存は既存の環境管理に合わせる。NixOS等で再現しやすくする場合はPEP 723を使う。

```python
# /// script
# dependencies = ["python-pptx>=1.0"]
# ///
```

画像や図形を追加してもテキストが自動的に収まるとは限らない。改行・高さを概算して余裕を取り、座標を整数EMUへそろえる。影・字間等の処理はデザイン層に集め、XMLや描画で効いているか確認する。

定期デッキなら、固定する表紙・説明と、その回に更新する内容を分ける。差分が重要な場合は前回との変化を示す。全案件に同じ章立てを強制しない。

## 描画と検査

作業プロジェクトで実行する。`DECK_SKILL` は、この `SKILL.md` がある実際の絶対パスへ置き換える。

```bash
DECK_SKILL=/absolute/path/to/native-pptx-deck
uv run scripts/build-deck.py out/deck.pptx
bash "$DECK_SKILL/assets/render.sh" out/deck.pptx out/render
uv run "$DECK_SKILL/assets/selfcheck.py" out/deck.pptx
uv run "$DECK_SKILL/assets/preflight.py" out/deck.pptx
```

`build-deck.py` は作業プロジェクトのスクリプト。他のコマンドは本スキルの道具。既存PDFからの画像化だけなら：

```bash
uv run "$DECK_SKILL/scripts/render_pdf.py" out/render/deck.pdf out/render
```

`render.sh` はLibreOffice（未導入ならNix環境の利用可能なパッケージ）、`render_pdf.py` はPyMuPDFとPillowを使う。ページPNGは0始まりの `p-00.png`、コンタクトシートの表示は人が読む1始まりのページ番号。ImageMagickに依存しない。

- ビルドの終了を待ってから描画し、描画の終了を待ってからアップロードする。画像の再生成が終わる前にビルドしない。
- 改訂後のPPTXから毎回PDFを生成し直す。古いPDFや別の版のPNGを完成版と取り違えない。
- コンタクトシートを先に見て、変更した各PNGと前後の接続を確認する。新規デッキでは全ページを見る。
- 部分改訂の内容検査は `assets/selfcheck.py deck.pptx --slides 23-27` のように対象を明示できる。移植性のpreflightはデッキ全体に行う。
- selfcheckの文体・密度・見出し等は判断材料。画像内の小字、意味、引用の範囲、前提はPNGと原資料で確認する。誤検出を隠すために本文を変えない。

LibreOfficeの描画はPowerPoint・Google Slidesの実機確認の代わりではない。実際に確認した範囲を報告する。指定書体が受け手の環境にない場合はPDFの併送や互換書体を検討する。

## Drive等への差し替え

既に差し替えを依頼されている場合、追加の確認を挟まず検証まで行う。保存先が不明な場合は接続先や既存資料から特定し、必要な情報だけ尋ねる。

1. 既存ID・MIME種別・保存先を確認する。手修正の証拠があれば[manual-source-sync](manual-source-sync.md)で取り込む。
2. 対応する接続ツールを優先する。保存されたPPTX/PDFのバイト差し替えと、ネイティブGoogle Slidesの編集・変換を区別する。
3. 同じIDへの差し替えを求められたら、共有状態・保存場所を維持して指定ファイルだけ更新する。`out/`全体を無差別にアップロードしない。
4. 完了後に取得し直し、バイト一致またはハッシュ一致を確かめる。ネイティブ形式へ変換した場合はメタデータ・ページ数・サムネイル等で変換結果を確認し、元PPTXとのバイト一致は要求しない。
5. 取得できたリンクを返す。アップロード要求の送信だけを完了の根拠にしない。

接続ツールでできない場合は、既存のrclone等の認証済み手段を使える。宛先を限定し、取得内容の照合まで行う。新しい共有権限・外部公開・メール等の送信はスキル使用だけでは追加しない。

プレビューが古いという報告があれば、まず取得ファイルの内容を照合する。プレビューが必ずキャッシュされるとは断定せず、原因を確かめる。不要な複製を既定で増やさない。

## 完了報告

変更した範囲、確認内容、成果物リンクを短く伝える。受け手に影響する未確認事項があれば具体的に添える。内部の編集履歴・実装パス・全レビューの逐語記録を、講演のスライドへ混ぜない。
