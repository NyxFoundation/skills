#!/usr/bin/env python3
"""台本の時間配分が枠に収まるかを検算する。

    python timing_check.py script.md [--slot 40]

見出しに書かれた分数を拾って、セッションごとに合計する。**見出しに分数を書き忘れた区間は
合計に入らないので、静かに 7〜8 分足りない台本ができる。**会場質疑の書き忘れが定番。

拾う書式（どれでもよい）:
    ### 冒頭（2 分）
    ### 冒頭（2 分 30 秒）
    ### 第 1 ラウンド（各 4 分）      ← 人数を掛ける。人数は「登壇：」行から数える
    ### 会場質疑（7 分）

セッションの区切りは `## ` 見出し。時刻レンジ（11:10–11:50）があれば枠を自動で取る。
"""
import argparse
import re
import sys

SEC_RE = re.compile(r"^## +(.+)$")
# findall で使うので re.M が要る。無いと 1 件も拾わず、静かに OK になる
# findall で使うので re.M が要る。無いと 1 件も拾わない。
# **\n を除外するのも必須。**[^（(] は改行にもマッチするので、括弧の無い見出しが
# 後続行を飲み込んで、遠くの（）まで 1 件として拾ってしまう
SUB_RE = re.compile(r"^### +([^（(\n]+)[（(]([^）)\n]*)[）)]", re.M)
TIME_RE = re.compile(r"(\d{1,2}):(\d{2})\s*[–\-−~〜]\s*(\d{1,2}):(\d{2})")
# 「3 分」「2 分 30 秒」「30 秒」「5 min」「2.5 minutes」を拾う
MIN_RE = re.compile(r"(?:各\s*)?(\d+(?:\.\d+)?)\s*(?:分|min(?:ute)?s?)(?:\s*(\d+)\s*秒)?")
SEC_ONLY_RE = re.compile(r"^\s*(\d+)\s*秒\s*$")
EACH_RE = re.compile(r"各\s*\d")
# 「登壇：A（X）／B（Y）／**あと 2 枠**」から確定人数を数える
NAME_SEP = re.compile(r"[／/]")


def speakers_in(block: str) -> int:
    for line in block.splitlines():
        if line.startswith("登壇") or line.startswith("Panel"):
            parts = [p for p in NAME_SEP.split(line.split("：", 1)[-1].split(":", 1)[-1])
                     if p.strip() and "枠" not in p and "調整中" not in p]
            return max(1, len(parts))
    return 1


class Unparsed(ValueError):
    """見出しの括弧から時間を読み取れなかった。**0 分として通してはいけない。**
    書き忘れた区間が静かに合計から落ちるのが、この検査で防ぎたい欠陥そのもの。"""


def minutes(spec: str, n_speakers: int) -> float:
    so = SEC_ONLY_RE.match(spec)
    if so:
        return int(so.group(1)) / 60
    m = MIN_RE.search(spec)
    if not m:
        raise Unparsed(spec)
    v = float(m.group(1)) + (int(m.group(2)) / 60 if m.group(2) else 0)
    return v * n_speakers if EACH_RE.search(spec) else v


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--slot", type=float, default=None,
                    help="枠の長さ（分）。省略時は見出しの時刻レンジから取る")
    ap.add_argument("--reserve", type=float, default=2.0,
                    help="確保しておく予備（分）。本編 ＋ 予備 ＝ 枠。"
                         "本編が枠−予備を超えたら押す。下回りすぎたら区間の書き忘れを疑う")
    args = ap.parse_args()

    text = open(args.path, encoding="utf-8").read()
    blocks, cur, name = [], [], None
    for line in text.splitlines():
        m = SEC_RE.match(line)
        if m:
            if name:
                blocks.append((name, "\n".join(cur)))
            name, cur = m.group(1), []
        elif name:
            cur.append(line)
    if name:
        blocks.append((name, "\n".join(cur)))

    bad = []
    for title, body in blocks:
        tm = TIME_RE.search(title)
        slot = args.slot
        if slot is None and tm:
            a = int(tm.group(1)) * 60 + int(tm.group(2))
            b = int(tm.group(3)) * 60 + int(tm.group(4))
            slot = b - a
        subs = SUB_RE.findall(body)
        # 時刻レンジのある見出しだけをセッションとみなす。説明章は検査しない
        if not subs or slot is None:
            continue
        n = speakers_in(body)
        total, unparsed = 0.0, []
        for h, spec in subs:
            try:
                total += minutes(spec, n)
            except Unparsed:
                unparsed.append(f"{h.strip()}（{spec}）")
        named = {h.strip() for h, _ in subs}
        # 説明章や、パネルでない枠（協賛の単独講演など）は必須区間を求めない
        is_panel = len(subs) >= 5 and slot and slot >= 30
        want = (("冒頭", "Opening"), ("会場質疑", "Q&A", "質疑"), ("締め", "Close"))
        missing = ["/".join(g) for g in want
                   if is_panel and not any(k in h for h in named for k in g)]
        line = f"{title[:46]:<48} 登壇 {n} 名  区間 {len(subs)}  合計 {total:5.1f} 分"
        if slot:
            line += f" / 枠 {slot:.0f} 分"
        print(line)
        for h, spec in subs:
            try:
                v = f"{minutes(spec, n):5.1f}"
            except Unparsed:
                v = "  ???"
            print(f"    {h.strip()[:28]:<30} {v}")
        if unparsed:
            bad.append(f"{title[:40]}: 時間を読み取れない区間 → {', '.join(unparsed)}"
                       f"（0 分として合計から落ちる）")
        if missing:
            bad.append(f"{title[:40]}: 区間の見出しが無い → {', '.join(missing)}")
        # 本編 ＋ 予備 ＝ 枠。予備を食いつぶす配分は「収まっている」とみなさない
        if slot and total > slot - args.reserve:
            bad.append(f"{title[:40]}: 本編 {total:.1f} 分。"
                       f"枠 {slot:.0f} 分から予備 {args.reserve:.0f} 分を引くと "
                       f"{slot - args.reserve:.1f} 分しかない")
        if slot and is_panel and total < slot - args.reserve * 2:
            bad.append(f"{title[:40]}: 本編 {total:.1f} 分。枠 {slot:.0f} 分に対して "
                       f"{slot - total:.1f} 分の空白がある（区間の書き忘れ？）")

    if bad:
        print("\n落ちた検査:", file=sys.stderr)
        for b in bad:
            print("  -", b, file=sys.stderr)
        return 1
    print("\nOK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
