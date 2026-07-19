# matplotlib で日本語（CJK）ラベルを表示する

感情曲線グラフの軸・凡例に日本語を使うと、CJKフォントが無い環境では文字が豆腐（□）になる。

## 症状

```
findfont: Font family 'Noto Sans CJK JP' not found.
# あるいはラベルが □□□ になる
```

## 正しい対応（スクリプトが採用している方法）

フォントは**名前リスト**で渡し、matplotlibに存在するものを選ばせる：

```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

fm._load_fontmanager(try_read_cache=False)  # 新規インストールフォントを認識
plt.rcParams['font.family'] = [
    'Noto Sans CJK JP',
    'Noto Serif CJK JP',
    'Noto Sans CJK SC',
    'Hiragino Sans',   # macOS
    'Yu Gothic',       # Windows
    'Meiryo',          # Windows
    'DejaVu Sans',     # ASCII フォールバック
    'sans-serif',
]
plt.rcParams['axes.unicode_minus'] = False
```

## 避けるべき対応

Variable Font（VF）をファイルパスで直接渡すとクラッシュすることがある（特にNixOSの
`NotoSansCJK-VF.otf.ttc`）：

```python
# ❌ RuntimeError: Can not load face (SFNT font table missing; error code 0x8e)
prop = fm.FontProperties(fname='/.../NotoSansCJK-VF.otf.ttc')
plt.rcParams['font.family'] = prop.get_name()
```

名前リストでのフォールバックを使えばこの問題を避けられる。

## CJKフォントの導入

| 環境 | コマンド |
|---|---|
| Debian/Ubuntu | `sudo apt install fonts-noto-cjk` |
| macOS | Hiragino Sans がプリインストール済み |
| Windows | Yu Gothic / Meiryo がプリインストール済み |
| NixOS | `fonts.packages = [ pkgs.noto-fonts-cjk-sans ];` |

導入確認：

```bash
fc-list :lang=ja | head
```

CJKフォントをどうしても用意できない場合は、JSONの `title` / `sections` / `personas[].name`
を英語ラベルにして回避する。
