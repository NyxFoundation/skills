# 他の環境で開けるか

.pptx は「保存できた」と「開ける」が別。実測で踏んだ地雷を残す。

## Google Slides のインポータが落ちる

症状：Drive で「ファイルを開けませんでした。ページを更新してみてください。」

内部エラーを見せてもらえると原因が特定できる。実例：

```
TransformImporter.qdomOffsetToPunch → expected a non-null reference
  ← ShapeImporter.toPunchShape
```

**図形の transform が null**。原因は 3 つあった。

### (a) 退化した transform — 高さ 0 の図形 ★最有力

`add_connector` で**水平線**を引くと `<a:ext cy="0"/>` になる。罫線を全部これで引いていたので
40 個以上あった。Google Slides はこれで落ちる。

**コネクタを使わず、高さを持った薄い矩形で罫線を引く。** 描画も安定する
（LibreOffice ではコネクタが太いグレーの帯に見えていた）。

```python
def rule(slide, x, y, w, color, weight=1.0):
    h = Emu(max(9525, int(weight * 12700)))   # 最低 1px 相当
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Emu(int(w)), h)
    sh.fill.solid(); sh.fill.fore_color.rgb = color
    sh.line.fill.background()
    noshadow(sh)
    return sh
```

### (b) 空の `<p:grpSpPr/>`

python-pptx が作る spTree の group には `xfrm` が無い。group transform が null になる。
明示的に単位変換を書き込む。

```python
def fix_group_xfrm(slide):
    grpSpPr = slide.shapes._spTree.find(qn("p:grpSpPr"))
    if grpSpPr is None or grpSpPr.find(qn("a:xfrm")) is not None:
        return
    xfrm = grpSpPr.makeelement(qn("a:xfrm"), {})
    for tag, attrs in (("a:off", {"x": "0", "y": "0"}),
                       ("a:ext", {"cx": str(int(W)), "cy": str(int(H))}),
                       ("a:chOff", {"x": "0", "y": "0"}),
                       ("a:chExt", {"cx": str(int(W)), "cy": str(int(H))})):
        xfrm.append(xfrm.makeelement(qn(tag), attrs))
    grpSpPr.insert(0, xfrm)
```

### (c) 子要素の順序違反

`bodyPr` / `spPr` はスキーマ順が厳格。`append` で末尾に足すと壊れる。
`references/ooxml-workarounds.md` を参照。

**PowerPoint と Keynote はこれらを許容する。Google Slides だけが厳しい。**
Slides 変換を前提にするなら `assets/preflight.py` を必ず通す。

## フォント

webfont は使えない。開く環境にインストールされている必要がある。

- Google Fonts は TTF を直接落とせる：
  `https://github.com/google/fonts/raw/main/ofl/<family>/<File>.ttf`
- 入れて `fc-cache -f ~/.local/share/fonts`、`fc-list : family | grep <名前>` で確認
- **無いと黙って別書体に置換される。** サイズ階層もカーニングも崩れるが、エラーは出ない
- python-pptx に埋め込み API は無い。PowerPoint 本体の埋め込みは Windows 版のみ

自分のマシンから投影するなら解決する。**ファイルを人に渡す場合は制御できない**ので、
フォント名を添えて渡すか、PDF も一緒に渡す。

## SVG は貼れない。EMF なら貼れる

`add_picture` は内部で Pillow に投げるので、Pillow が読める形式が通る。

| 形式 | 可否 |
|---|---|
| PNG / JPEG / GIF / BMP / TIFF | OK |
| **EMF / WMF** | **OK（ベクタのまま入る）** |
| SVG | NG（`UnidentifiedImageError`） |

SVG 資産は **SVG → EMF** に変換すればベクタで入る。ラスタ化する必要はない。
NixOS なら `nix-shell -p inkscape --run "inkscape in.svg --export-type=emf -o out.emf"`。

## ローカル確認は近似でしかない

LibreOffice は nix で引ける（`nix-shell -p libreoffice-fresh`）。
pptx → PDF → PNG が出るので、描画 → 見る → 直すループは回せる。

**ただし PowerPoint の描画とは一致しない。** 特に折り返し位置が違い、
それがオーバーフローの有無を決める。**最終確認は実機の PowerPoint で開くこと。**
「LibreOffice で問題なかった」は「PowerPoint で問題ない」を意味しない。

## 出荷前チェック

`assets/preflight.py` が見るもの：

- transform の欠落（`a:off` / `a:ext` の無い図形）
- 退化した extent（`cx` か `cy` が 0）
- 座標に小数点が混じっていないか
- `spPr` / `bodyPr` の子要素順
- 空の `grpSpPr`
- 使われている書体がローカルに存在するか
