# -*- coding: utf-8 -*-
"""図の検査 — docx に貼る前に、全 PNG に対して回す。

    uv run --quiet --with pillow --with matplotlib python figure_preflight.py figures/*.png

目視で見落とすものを機械で拾う。

  1. 使用フォントに静的な Bold があるか
     可変フォント 1 本の環境では matplotlib が weight=100(Thin) しか掴めず、
     fontweight="bold" が黙って無視される。単体で見ると読めるので気づけない。
  2. 線の細さ  Google ドキュメントは取り込み時に長辺を 2048px へ縮小する。
     縮小後に線が飛ぶ図は「画質は悪くないのに読めない」状態になる。
  3. 白黒印刷での可読性  塗り分けだけで区別している図は B&W で消える。
  4. 端でのクリッピング  bbox_inches="tight" を付け忘れると文字が切れる。
"""
import sys
import os


def font_report():
    try:
        import matplotlib.font_manager as fm
    except ImportError:
        print("  (matplotlib 無し。フォント検査をスキップ)")
        return
    cjk = {}
    for f in fm.fontManager.ttflist:
        if any(k in f.name for k in ("CJK", "Gothic", "Mincho", "JP")):
            cjk.setdefault(f.name, set()).add(f.weight)
    if not cjk:
        print("  ✗ 和文フォントが見つからない。図のラベルが豆腐になる")
        return
    for name, weights in sorted(cjk.items()):
        ws = sorted(str(w) for w in weights)
        bold_ok = any(isinstance(w, int) and w >= 600 for w in weights)
        mark = "  " if bold_ok else "✗ "
        print(f"  {mark}{name}: weight={','.join(ws)}"
              + ("" if bold_ok else "  ← Bold が選べない。縁取りで太らせること"))


def check(path):
    from PIL import Image, ImageStat
    im = Image.open(path).convert("RGB")
    w, h = im.size
    issues = []

    if max(w, h) > 2048:
        issues.append(f"長辺 {max(w,h)}px。Google ドキュメントが 2048px へ縮小する。"
                      "先に 2040px 以内へ落とす")

    g = im.convert("L")
    # 端 6px に濃い画素があればクリッピングの疑い
    edge = []
    px = g.load()
    for x in range(w):
        for y in list(range(6)) + list(range(h - 6, h)):
            if px[x, y] < 100:
                edge.append((x, y))
                break
    if len(edge) > w * 0.02:
        issues.append("上下の端に濃い画素が多い。bbox_inches='tight' の付け忘れか、はみ出し")

    # 白黒化したときのコントラスト分布
    st = ImageStat.Stat(g)
    if st.stddev[0] < 22:
        issues.append(f"白黒化後のコントラストが低い（stddev {st.stddev[0]:.0f}）。"
                      "塗り分けだけで区別していないか確認する")

    # 細線の割合。中間調（薄い線）が多いと縮小で飛ぶ
    hist = g.histogram()
    mid = sum(hist[120:210])
    dark = sum(hist[:120])
    if dark and mid / max(dark, 1) > 3.0:
        issues.append("中間調の画素が濃い画素の 3 倍を超える。線と文字が細すぎる疑い")

    print(f"\n{os.path.basename(path)}  {w}x{h}")
    if issues:
        for i in issues:
            print("  ✗", i)
    else:
        print("  ok")
    return len(issues)


def main():
    paths = [a for a in sys.argv[1:] if a.endswith(".png")]
    if not paths:
        print("usage: figure_preflight.py FIG.png [FIG2.png ...]")
        return 1
    print("使用可能な和文フォント")
    font_report()
    n = sum(check(p) for p in paths)
    print(f"\n{len(paths)} 図 / 指摘 {n} 件")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
