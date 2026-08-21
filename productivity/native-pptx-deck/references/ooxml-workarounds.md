# python-pptx に API が無いもの

すべて実測（python-pptx 1.0.2）。**共通する危険は「代入しても例外が出ず、何も起きない」**こと。
書けたつもりで効いていないまま本番を迎えるのがいちばん多い事故。

必ず生成した .pptx を unzip して XML を見て確認する。

```bash
unzip -q -o out/deck.pptx -d /tmp/x && grep -o '<c:smooth val="[01]"/>' /tmp/x/ppt/charts/chart1.xml
```

## 1. letter-spacing

キッカーの `0.18em` のようなトラッキング。公式 API なし。`a:rPr@spc` に **1/100 pt 単位**で書く。

```python
def set_spacing(run, em):
    size_pt = run.font.size.pt if run.font.size else 18
    run.font._rPr.set("spc", str(int(size_pt * em * 100)))
```

## 2. 塗り・線の透明度

`rgba(24,24,26,.10)` のような半透明。公式 API なし。`a:srgbClr` の下に `a:alpha` を差す。

```python
def set_alpha(spPr, alpha_pct):
    srgb = spPr.find(".//" + qn("a:srgbClr"))
    if srgb is not None:
        srgb.append(srgb.makeelement(qn("a:alpha"), {"val": str(alpha_pct * 1000)}))
```

不要なら避けるほうが早い。背景色が固定なら**合成後の不透明色を計算して置く**（`--line` を
`#e3e1db` に潰すなど）。トークン定義にその旨をコメントで残すこと。

## 3. 曲線のスムージング ★ 無言で失敗する

**`XySeries` に `smooth` プロパティが存在しない。** `ser.smooth = True` はインスタンス属性を
生やすだけで、XML は `<c:smooth val="0"/>` のまま。例外も警告も出ない。

```python
print('smooth' in dir(XySeries))   # False
```

散布図＋線は既定でカクカクの折れ線になる。滑らかにするには XML を直接書き換える。

```python
def set_smooth(chart, on=True):
    for s in chart._chartSpace.iter(qn("c:smooth")):
        s.set("val", "1" if on else "0")
```

## 4. 影 ★ 2 段構えで消す

既定でテーマの影が付く。`shape.shadow.inherit = False` **だけでは消えない**。
`add_shape` / `add_connector` が付ける `<p:style>` の `effectRef` から継承するため、
**`<p:style>` ごと外す**必要がある。

```python
def noshadow(shape):
    el = shape._element
    spPr = el.spPr
    for e in spPr.findall(qn("a:effectLst")):
        spPr.remove(e)
    spPr.append(spPr.makeelement(qn("a:effectLst"), {}))
    for style in el.findall(qn("p:style")):
        el.remove(style)
    return shape
```

罫線にまで影が付くと一気に安っぽくなる。**全図形のコンストラクタで呼ぶ**こと。

## 5. テキストの自動縮小を切る

`normAutofit` が効いていると、入りきらない文字が勝手に縮んでサイズ階層が壊れる。
`a:noAutofit` を入れるが、**`bodyPr` の子要素はスキーマ順が厳格**なので末尾に append しない。

順序は `prstTxWarp` → autofit → `scene3d` → `sp3d` → `flatTx` → `extLst`。

```python
_BODYPR_ORDER = ("a:prstTxWarp", "a:noAutofit", "a:normAutofit", "a:spAutoFit",
                 "a:scene3d", "a:sp3d", "a:flatTx", "a:extLst")
```

同じ理由で `spPr` の子も順序が決まっている（`xfrm` → 幾何 → 塗り → `ln` → `effectLst` → …）。
`append` する前に、自分が入れる要素が末尾で正しいか確かめる。

## 6. 日本語グリフのフォント指定

`run.font.name` はラテン用（`a:latin`）にしか効かない。日本語は `a:ea` を別に指定しないと
テーマ既定の別書体になる。

```python
rPr = run.font._rPr
for tag in ("a:ea", "a:cs"):
    rPr.append(rPr.makeelement(qn(tag), {"typeface": font}))
```

## 7. ネイティブグラフは十分に使える

「python-pptx はデザインが弱い」は誤り。チャート 73 種・プリセット図形 182 種があり、
2 曲線のグラフはトークン配色そのままでネイティブに描ける。

```python
gf = slide.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER_LINES_NO_MARKERS, x, y, w, h, cd)
ch = gf.chart
ch.has_legend = False
for i, ser in enumerate(ch.plots[0].series):
    ser.format.line.color.rgb = ACCENT if i == 0 else SEVERE
    ser.format.line.width = Pt(2.75)
for ax in (ch.value_axis, ch.category_axis):
    ax.has_major_gridlines = False
    ax.visible = False
set_smooth(ch)          # ← これを忘れると折れ線のまま
```

- 凡例 OFF・グリッド OFF・軸非表示・軸ラベルのフォント／サイズはすべて API で指定できる
- **グラフの裏に Excel が入る**（`chart.part.chart_workbook`）。PowerPoint 上で「データの編集」が開く
- `chart.replace_data(cd)` でデータだけ差し替えられる。**毎月更新する資料と相性が良い**
- プロットエリアの背景塗りだけは API が薄く、`spPr` を自分で足す必要がある

**何も指定しなければ既定の PowerPoint の見た目になる。**「デザインできない」のではなく
「全部明示的に指定しないと既定になる」だけ。
