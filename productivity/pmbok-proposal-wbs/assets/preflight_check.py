# -*- coding: utf-8 -*-
"""Pre-flight check for a client-facing .docx — run BEFORE the external review round.

    uv run --quiet python preflight_check.py proposal.docx [--dump dump.md]

Catches the defects an external reviewer would otherwise spend a round on:
  1. corrupt / unopenable XML parts
  2. missing heading outline levels (empty navigation pane)
  3. banned internal-facing vocabulary (meta text, revision history, cost defence)
  4. AI tells (archaic keigo, sentence-ending monotony)
  5. unqualified superlatives
  6. stale cross-references after renumbering (「N.M をご参照」 pointing at a missing heading)
  7. numeric drift — the same concept quoted with different values
Exit code is non-zero when a BLOCKER is found.
"""
import re
import sys
import zipfile
import collections
from xml.dom import minidom

BANNED = {  # substring -> why it blocks
    "当初案": "旧版への言及（改訂履歴）",
    "前回ご提示": "旧版への言及（改訂履歴）",
    "初版": "旧版への言及（改訂履歴）",
    "からの変更点": "差分表",
    "当社側の作成工数": "社内コスト事情",
    "追加請求": "社内コスト事情",
    "削減しました": "社内コスト事情",
    "削減しておりません": "社内コスト事情",
    "本書の目的は": "メタ記述",
    "以下に整理します": "メタ記述",
    "本ドキュメント": "メタ記述",
    "でございます": "過剰敬語",
    "申し上げ": "過剰敬語",
    "存じます": "過剰敬語",
    "おります": "過剰敬語（〜ています に）",
}
SUPERLATIVE = ["原理的に", "唯一", "最高水準", "確実に", "最も容易", "必ず検出", "完全に防"]
HEDGE_OK = ["確認した範囲", "確認した公開情報の範囲", "前提条件が満たされ", "本 PoC の対象条件"]


def load(path):
    z = zipfile.ZipFile(path)
    bad = []
    for n in z.namelist():
        if n.endswith(".xml"):
            try:
                minidom.parseString(z.read(n))
            except Exception as e:            # noqa: BLE001
                bad.append((n, str(e)[:80]))
    return z, bad


def extract(z):
    d = minidom.parseString(z.read("word/document.xml"))

    def txt(n):
        return "".join("".join(c.data for c in t.childNodes if c.nodeType == c.TEXT_NODE)
                       for t in n.getElementsByTagName("w:t"))

    lines, heads = [], []
    for el in d.getElementsByTagName("w:body")[0].childNodes:
        if el.nodeName == "w:p":
            t = "［図］" if el.getElementsByTagName("w:drawing") else txt(el)
            ps = el.getElementsByTagName("w:pStyle")
            style = ps[0].getAttribute("w:val") if ps else ""
            if t.strip():
                lines.append(t)
                if style.startswith("Heading"):
                    heads.append((style, t.strip()))
        elif el.nodeName == "w:tbl":
            for tr in el.getElementsByTagName("w:tr"):
                lines.append("| " + " | ".join(txt(tc).strip()
                             for tc in tr.getElementsByTagName("w:tc")) + " |")
    return lines, heads


def main():
    path = sys.argv[1]
    dump = None
    if "--dump" in sys.argv:
        dump = sys.argv[sys.argv.index("--dump") + 1]

    z, bad_xml = load(path)
    lines, heads = extract(z)
    full = "\n".join(lines)
    xml = z.read("word/document.xml").decode()
    if dump:
        open(dump, "w", encoding="utf-8").write(full)

    blockers, warns = [], []

    # 1. XML ---------------------------------------------------------------
    for n, e in bad_xml:
        blockers.append(f"XML 破損: {n} — {e}")

    # 2. outline levels ----------------------------------------------------
    lv = {l: xml.count(f'<w:outlineLvl w:val="{l}"') for l in "012"}
    if lv["0"] == 0:
        blockers.append("見出しに outlineLevel が無い（ナビゲーションウィンドウが空になる）")
    else:
        print(f"  outlineLevel  H1={lv['0']} H2={lv['1']} H3={lv['2']}  見出し {len(heads)} 件")

    # 3. banned vocabulary -------------------------------------------------
    for w, why in BANNED.items():
        n = full.count(w)
        if n:
            blockers.append(f"禁止語「{w}」× {n}  — {why}")

    # 4. sentence-ending monotony -----------------------------------------
    sents = [s for s in re.split(r"[。\n]", full) if len(s) > 25]
    if sents:
        top, cnt = collections.Counter(s[-6:] for s in sents).most_common(1)[0]
        ratio = cnt / len(sents)
        if ratio > 0.18:
            warns.append(f"文末の偏り: 「…{top}」が長文の {ratio:.0%}（{cnt}/{len(sents)}）")

    # 5. superlatives ------------------------------------------------------
    for w in SUPERLATIVE:
        for ln in lines:
            if w in ln and not any(h in ln for h in HEDGE_OK):
                warns.append(f"無条件の断定「{w}」: {ln[:70]}")
                break

    # 6. stale cross-references -------------------------------------------
    numbers = {h.split("　")[0].split(" ")[0].rstrip(".") for _, h in heads}
    for m in set(re.findall(r"(\d+\.\d+)\s*(?:を|の|に|は)?ご?参照|(\d+\.\d+)\s*に記載", full)):
        ref = (m[0] or m[1])
        if ref and ref not in numbers:
            blockers.append(f"参照先が存在しない: 「{ref}」")
    for ap in set(re.findall(r"付録\s*([A-Z])\s*(?:に|を|の)", full)):
        if not any(h.startswith(f"付録 {ap}") for _, h in heads):
            blockers.append(f"参照先が存在しない: 「付録 {ap}」")

    # 7. numeric drift -----------------------------------------------------
    for label, pat in [("人日合計", r"([\d.]+)\s*人日"), ("人月", r"([\d.]+)\s*人月")]:
        vals = collections.Counter(re.findall(pat, full))
        big = {v: c for v, c in vals.items() if float(v) > 20}
        if len(big) > 4:
            warns.append(f"{label} の値が {len(big)} 種類: {sorted(big, key=float)} — 整合を確認")

    # report ---------------------------------------------------------------
    print()
    if blockers:
        print(f"BLOCKER {len(blockers)} 件")
        for b in blockers:
            print("  ✗", b)
    if warns:
        print(f"\nWARN {len(warns)} 件")
        for w in warns:
            print("  !", w)
    if not blockers and not warns:
        print("clean — 外部レビューに回して問題ありません")
    print(f"\n{len(lines)} 行 / {len(full)} 文字")
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())
