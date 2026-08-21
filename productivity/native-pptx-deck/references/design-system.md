# デザイン層

`scripts/build_pptx/<project>.py` に置く。**内容側のコードから OOXML を一切見せない**のが目的。

## 構成

```
トークン（色・書体）
判型とグリッド（col / band）
OOXML ヘルパ（set_spacing / set_alpha / set_smooth / noshadow / no_autofit / fix_group_xfrm）
テキスト計測（est_lines / est_height）
プリミティブ（canvas / textbox / run / para / rule / kicker / display / body / card / verse）
```

## トークン

CSS のトークンをそのまま定数にする。**半透明は合成後の不透明色に潰す**（`a:alpha` を避けられる）。

```python
BG        = RGBColor(0xFA, 0xF9, 0xF5)
BG2       = RGBColor(0xF3, 0xF1, 0xEA)
INK       = RGBColor(0x18, 0x18, 0x1A)
INK_DIM   = RGBColor(0x55, 0x52, 0x4C)
INK_FAINT = RGBColor(0x9A, 0x95, 0x8C)
LINE      = RGBColor(0xE3, 0xE1, 0xDB)   # rgba(24,24,26,.10) を bg 上でフラット化
LINE_STR  = RGBColor(0xCF, 0xCD, 0xC6)
ACCENT    = RGBColor(0x1F, 0x3A, 0x52)
SEVERE    = RGBColor(0xA2, 0x54, 0x34)
```

**色の意味は固定する。** accent = 肯定・検証、severe = リスク・退行。
スライドをまたいで意味が揺れると読めなくなる。

## 書体

役割ごとに割り当て、コードから直接フォント名を書かない。

```python
SERIF    = "Cormorant Garamond"   # 装飾 em・数字。ラテン専用
JP       = "Shippori Mincho"      # 日本語本文・見出し
MONO     = "JetBrains Mono"       # キッカー・ラベル・コード
WORDMARK = "BIZ UDPMincho"        # ワードマーク
```

**ラテン書体を日本語に当てない。** `references/writing-rules.md` を参照。

## サイズ階層

投影時の最小可読サイズを下限として固定する。

| 役割 | サイズ |
|---|---|
| 見出し（display） | 32–36pt |
| Hero | 44–52pt |
| リード | 15–16pt |
| 本文・カード | 13–14pt |
| キッカー・ラベル | 11–12pt |

**本文 12pt 未満・ラベル 11pt 未満は使わない。** 読めない文字は無いのと同じ。

## グリッド

これを敷かないと座標がその場しのぎになり、崩れが再発する。

```python
COLS, GUTTER = 12, Emu(114300)

def col(start, span):
    """1-indexed。(x, width) を返す。"""
    unit = (CONTENT_W - GUTTER * (COLS - 1)) / COLS
    return Emu(int(MARGIN + (unit + GUTTER) * (start - 1))), \
           Emu(int(unit * span + GUTTER * (span - 1)))

BASE = Emu(101600)            # 8pt
def band(n):
    return Emu(int(BASE * n))
```

内容側では `inches(2.35)` のような数字を書かず、`col()` と `band()` だけを使う。

## プリミティブに必ず入れること

| プリミティブ | 忘れると起きること |
|---|---|
| すべての図形 | `noshadow()` を呼ぶ。忘れるとテーマの影が付いて安っぽくなる |
| すべての図形 | 座標を `Emu(int(...))` に丸める。float が XML に出ると壊れる |
| `canvas()` | `fix_group_xfrm()` を呼ぶ。Google Slides 対策 |
| `textbox()` | `no_autofit()` を呼ぶ。文字が勝手に縮むとサイズ階層が壊れる |
| `run()` | `a:ea` を設定する。日本語が別書体になる |
| `rule()` | コネクタを使わない。高さ 0 の図形は Google Slides を落とす |
| `display()` | 日本語には italic を当てない |

## 参考実装

`assets/nyx_design.py` が上記を全部満たした実装。トークンと書体名を差し替えれば
別プロジェクトでそのまま使える。
