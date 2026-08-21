#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""枚ごとの密度を測る。

    uv run assets/measure.py out/deck.pptx

references/layout-patterns.md の「密度の目安」に対して、どの枚が重いかを出す。
図が 0 で文字が多い枚が続いていたら、そこが谷になっている。

目安:
  Statement（表紙・扉・命題・締め）   40 字以下
  通常の内容枚                       100〜150 字
  一覧・カタログ枚（許容の上限）      300 字
"""

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"

LIGHT, NORMAL, HEAVY = 40, 150, 300
DRAWN = 5          # 図形がこれ以上あれば「図で語っている枚」とみなす（罫線だけは除く）


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1])
    z = zipfile.ZipFile(path)
    names = sorted((n for n in z.namelist()
                    if re.match(r"ppt/slides/slide\d+\.xml$", n)),
                   key=lambda s: int(re.findall(r"\d+", s.split("/")[-1])[0]))

    print(f"{path.name} — {len(names)} 枚\n")
    print(" #  図 図形  段落  文字  判定   見出し")
    print("─" * 78)
    heavy, textwall = [], []
    for i, n in enumerate(names, 1):
        root = ET.fromstring(z.read(n))
        pics = len(list(root.iter(P + "pic"))) + len(list(root.iter(P + "graphicFrame")))
        # 自前で描いた図（矩形・矢印・バー）も「図」として数える。
        # 数えないと、図形で組んだ図解が「文字だけの枚」として誤検出される。
        # 罫線 1〜2 本は図ではないので、しきい値は下の DRAWN で見る。
        drawn = sum(1 for sp in root.iter(P + "sp")
                    if not any((t.text or "").strip() for t in sp.iter(A + "t")))
        txts = [("".join(r.text or "" for r in p.iter(A + "t"))).strip()
                for p in root.iter(A + "p")]
        txts = [t for t in txts if t]
        chars = sum(len(t) for t in txts)
        head = next((t for t in txts if len(t) > 6), txts[0] if txts else "")

        if chars <= LIGHT:
            mark = "軽  "
        elif chars <= NORMAL:
            mark = "適  "
        elif chars <= HEAVY:
            mark = "重  "
            heavy.append(i)
        else:
            mark = "超過"
            heavy.append(i)
        if pics == 0 and drawn < DRAWN and chars > NORMAL:
            textwall.append(i)
        print(f"{i:2d} {pics:3d} {drawn:4d} {len(txts):5d} {chars:5d}  "
              f"{mark}  {head[:34]}")

    print()
    if heavy:
        print(f"重い枚: {', '.join(f'S{i}' for i in heavy)}")
    if textwall:
        print(f"図が無く文字が多い枚: {', '.join(f'S{i}' for i in textwall)}")
        print("  → 連続していると、そこが谷になる。"
              "型が合っているか references/layout-patterns.md で確かめる")
    if not heavy and not textwall:
        print("密度の目安を超える枚はなし")
    return 0


if __name__ == "__main__":
    sys.exit(main())
