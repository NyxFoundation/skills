#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""ネイティブ .pptx の出荷前チェック。

    uv run assets/preflight.py out/deck.pptx

「保存できた」と「他の環境で開ける」は別。PowerPoint と Keynote が許容して
Google Slides だけが落ちる条件を、渡す前に潰す。

検査するもの:
  1. transform の欠落（a:off / a:ext が無い図形）
  2. 退化した extent（cx か cy が 0）── コネクタの水平線でよく起きる
  3. 座標に小数点（float が XML に出ている）
  4. spPr / bodyPr の子要素順（スキーマ順が厳格）
  5. 空の grpSpPr（group transform が null になる）
  6. 使われている書体がローカルにあるか

終了コード: 問題があれば 1。
"""

import re
import subprocess
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"

SPPR_ORDER = ["xfrm", "custGeom", "prstGeom", "noFill", "solidFill", "gradFill",
              "blipFill", "pattFill", "grpFill", "ln", "effectLst", "effectDag",
              "scene3d", "sp3d", "extLst"]
BODYPR_ORDER = ["prstTxWarp", "noAutofit", "normAutofit", "spAutoFit",
                "scene3d", "sp3d", "flatTx", "extLst"]


def local(tag: str) -> str:
    return tag.split("}")[-1]


def check_order(parent, order):
    idx = [order.index(local(c.tag)) for c in parent if local(c.tag) in order]
    return idx == sorted(idx)


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1])
    if not path.exists():
        sys.exit(f"見つかりません: {path}")

    zf = zipfile.ZipFile(path)
    slides = sorted(n for n in zf.namelist()
                    if re.match(r"ppt/slides/slide\d+\.xml$", n))

    problems = []
    shapes = 0
    fonts = Counter()

    for name in slides:
        raw = zf.read(name).decode("utf-8")
        root = ET.fromstring(raw)
        sl = name.split("/")[-1]

        # 5. 空の grpSpPr
        for grp in root.iter(P + "grpSpPr"):
            if grp.find(A + "xfrm") is None:
                problems.append((sl, "grpSpPr に xfrm が無い（group transform が null）"))

        # 1 / 2. transform
        for tag in ("sp", "cxnSp", "pic", "graphicFrame"):
            for sh in root.iter(P + tag):
                shapes += 1
                nm = ""
                cnv = sh.find(".//" + P + "cNvPr")
                if cnv is not None:
                    nm = cnv.get("name", "")
                xfrm = sh.find(".//" + A + "xfrm") or sh.find(".//" + P + "xfrm")
                if xfrm is None:
                    problems.append((sl, f"{tag} '{nm}' に xfrm が無い"))
                    continue
                off = xfrm.find(A + "off")
                ext = xfrm.find(A + "ext")
                if off is None:
                    problems.append((sl, f"{tag} '{nm}' に a:off が無い"))
                if ext is None:
                    problems.append((sl, f"{tag} '{nm}' に a:ext が無い"))
                elif ext.get("cx") == "0" or ext.get("cy") == "0":
                    problems.append(
                        (sl, f"{tag} '{nm}' の extent が 0（退化した transform。"
                             "コネクタの水平線なら矩形に置き換える）"))

        # 3. float 座標
        for m in re.finditer(r'<a:(?:off|ext) [^>]*?="(-?\d+\.\d+)"', raw):
            problems.append((sl, f"座標が小数: {m.group(1)}"))

        # 4. 子要素順
        for spPr in root.iter(P + "spPr"):
            if not check_order(spPr, SPPR_ORDER):
                problems.append((sl, "spPr の子要素順が不正: "
                                     + ",".join(local(c.tag) for c in spPr)))
        for bodyPr in root.iter(A + "bodyPr"):
            if not check_order(bodyPr, BODYPR_ORDER):
                problems.append((sl, "bodyPr の子要素順が不正: "
                                     + ",".join(local(c.tag) for c in bodyPr)))

        # 6. 書体
        for m in re.finditer(r'typeface="([^"]+)"', raw):
            if not m.group(1).startswith("+"):
                fonts[m.group(1)] += 1

    print(f"{path.name} — スライド {len(slides)} 枚 / 図形 {shapes} 個")

    print("\n使われている書体:")
    try:
        installed = subprocess.run(["fc-list", ":", "family"],
                                   capture_output=True, text=True, timeout=30).stdout
    except Exception:
        installed = ""
    missing = []
    for f, n in fonts.most_common():
        ok = any(f == part.strip() for line in installed.splitlines()
                 for part in line.split(","))
        mark = "OK " if ok else "無し"
        if not ok:
            missing.append(f)
        print(f"  {mark} {f}  ({n})")
    if missing and installed:
        print(f"\n  ※ {', '.join(missing)} はこの環境に無い。"
              "開く環境に入っていないと黙って別書体に置換される。")

    if problems:
        print(f"\n問題 {len(problems)} 件:")
        seen = Counter()
        for sl, msg in problems:
            key = (sl, msg[:50])
            seen[key] += 1
            if seen[key] <= 3:
                print(f"  {sl}: {msg}")
        extra = len(problems) - sum(min(v, 3) for v in seen.values())
        if extra > 0:
            print(f"  … ほか {extra} 件")
        print("\n判定: NG — references/portability.md を見て直す")
        return 1

    print("\n判定: OK — 移植性の問題は見つからなかった")
    print("※ ただし最終確認は実機の PowerPoint で開くこと。ローカル描画は近似でしかない。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
