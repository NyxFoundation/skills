# レイアウトとテキスト

## 根本問題：テキストが測れない

python-pptx に**テキストメトリクスが無い**。文字列が何行に折り返されるかを知る手段がない。
CSS なら flexbox が吸収していた部分が、絶対座標（EMU）になった瞬間に全部露出する。

実際に起きること：

- カードの高さを目分量で決める → 1 行あふれて枠の外に文字が出る
- 見出しが 2 行になる → 下のリード文と重なる
- 文言を 1 文字足す → 別のスライドが崩れる

**例外は出ない。** レンダリングして見るまで気づけない。

## 対策 1：行数を概算する

全角 1.0em / 半角 0.5em で幅を見積もる。厳密ではないが、**目分量よりはるかにマシ**。

```python
def _em_width(text):
    w = 0.0
    for c in text:
        o = ord(c)
        full = (0x3000 <= o <= 0x30FF or 0x4E00 <= o <= 0x9FFF
                or 0xFF00 <= o <= 0xFF60 or 0x3400 <= o <= 0x4DBF)
        w += 1.0 if full else 0.5
    return w

def est_lines(text, width_emu, size_pt):
    per_line = max(1.0, (width_emu / 12700.0) / size_pt)
    return max(1, math.ceil(_em_width(text) / per_line))
```

**安全率を必ず外側に掛ける（1.15〜1.2）。** 実測値ではないうえ、PowerPoint と LibreOffice で
折り返し位置が違う。詰めるとどちらかで溢れる。

## 対策 2：コンテナを内容に合わせる

高さを固定せず、中身から計算する。

```python
rh = padding_top + est_height(lines, inner_w, size, line_ratio) + padding_bottom
ch = max(rh, MIN_HEIGHT)
card(s, x, y, w, ch)
```

見出しが可変長なら、その下の要素も追従させる。

```python
hl = est_lines(title, CW, 36)
lead_y = head_y + inches(0.42) + Emu(int(hl * 36 * 1.18 * 12700)) + inches(0.28)
```

## 対策 3：グリッドに載せる

**今日ぶつかった崩れのほぼ全部が、座標をその場で決めていたことに由来する。**

```python
card(s, cx, inches(2.35), cw, inches(3.4))     # 2.35 と 3.4 の根拠が無い
rule(s, cx + inches(0.2), inches(3.3), ...)    # 3.3 も無い
```

12 カラム × 8pt ベースラインを敷いて、そこにしか置けなくする。

```python
COLS, GUTTER = 12, Emu(114300)          # 0.125in
def col(start, span):
    """1-indexed。x と幅を返す。"""
    unit = (CONTENT_W - GUTTER * (COLS - 1)) / COLS
    x = MARGIN + (unit + GUTTER) * (start - 1)
    return Emu(int(x)), Emu(int(unit * span + GUTTER * (span - 1)))

BASE = Emu(101600)                       # 8pt
def band(n):
    return Emu(int(BASE * n))
```

これで `inches(2.35)` のようなマジックナンバーがコードから消え、
**縦位置が自動的に揃う**。Müller-Brockmann のグリッドシステムのそのままの適用。

## z 順の罠

**後から追加した図形が前面に来る。** カードを後で足すと本文が全部隠れる。
実際に「左カードの中身が消えた」事故があった。

```python
# 図形を先に全部置いてから、テキストを置く
card(s, X, top, lw, ch)
card(s, rx, top, rw, ch, highlight=True)
# ── ここから下がテキスト
```

## 座標は必ず整数 EMU

`(CW - inches(0.45)) / 2` は **float を返す**。そのまま渡すと XML に `x="838200.0"` と出て、
厳しいパーサが落ちる。プリミティブの入口で `Emu(int(...))` に丸める。

## レイアウトのフレームワーク

| 枠組み | 何を規定するか |
|---|---|
| **グリッドシステム**（Müller-Brockmann, 1981） | 版面をカラムとフィールドに割り、全要素をその線に載せる。この分野の正典 |
| **CRAP**（Robin Williams） | Contrast / Repetition / Alignment / Proximity。粗いが機械的に検査できる |
| **ゲシュタルト原則** | 近接・類同・共通領域・連続。CRAP の根拠側 |
| **モジュラースケール** | 文字サイズを比率（1.25 / 1.333）で刻む |
| **8pt ベースライングリッド** | 縦のリズム。余白を 8 の倍数に固定 |
| **Tufte** | データインク比、small multiples、レイヤリング |

## 縦バランスのチェック

コンタクトシートで見て、**下 1/3 が空いていたら設計ミス**。
上詰めで組むと必ずこうなる。バンドを広げるか、要素を増やすか、判型を見直す。
