#!/usr/bin/env python3
"""読み上げ文が「声に出す文」になっているかを機械検査する。

    python spoken_check.py script.md

引用符（>）の中を読み上げ文とみなす。`<details>` の中（準備メモ）は検査しない。

検出するもの:
  1. 読み上げ文の太字            声に太字はない。書き物の体裁のまま喋らせている
  2. 一文が長い                  読点で息継ぎできる長さにする（既定 60 字）
  3. 受けが無いセッション        答えを客席の言葉に置き直す動作。**いちばん抜ける**
  4. 地ならしが無いセッション    いま何が起きているかの説明。**2 番目に抜ける**
  5. 挙手が無いセッション        60 秒で客席が自分ごとになるかが決まる
  6. 拍手を促していない          言わないと客席はタイミングを迷う
  7. 呼びかけが無い              「みなさん」が一度も出てこない
  8. ぼかし                      司会は言い切る
"""
import argparse
import re
import sys

SEC_RE = re.compile(r"^## +(.+)$")
TIME_RE = re.compile(r"\d{1,2}:\d{2}\s*[–\-−~〜]\s*\d{1,2}:\d{2}")
BOLD_RE = re.compile(r"\*\*[^*]+\*\*")
HEDGE_RE = re.compile(r"かもしれません|と思われます|一般的には|なのではないでしょうか")
# 受け・地ならし・挙手・拍手・呼びかけの検出語
TAG_HINT = ("つまり", "ということですね", "ということでした", "言い換える",
            "もう一度だけ", "分かったことがあります", "受け", "Bridge", "bridge")
SETUP_HINT = ("ここ 1 年", "この 1 年", "この半年", "ざっくり言うと", "指しているのは",
              "いま世の中", "もう動き始め", "出そろい", "いま起きているのは",
              "いまの市場", "地ならし",
              "in the last year", "over the past year", "what changed",
              "right now, ", "what is happening")
HAND_HINT = ("手を挙げ", "挙げていただけますか", "show of hands", "hands up",
             "手を下ろし", "keep your hand up")
CLAP_HINT = ("拍手", "applause", "thanking our panel")
CALL_HINT = ("みなさん", "皆さん", "everyone", "this room")


def spoken_lines(body: str):
    """引用行のうち、<details> の外にあるものだけ返す。"""
    out, depth = [], 0
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("<details"):
            depth += 1
        elif s.startswith("</details>"):
            depth = max(0, depth - 1)
        elif depth == 0 and s.startswith(">"):
            out.append(s.lstrip("> ").strip())
    return out


def structure_markers(body: str) -> str:
    """<details> の外にある構造ラベル（**受け** / *Bridge:* など）を集める。

    これも「受けが書いてあるか」の証拠になる。引用行だけ見ていると、
    ラベルだけ置いて中身を型で示している箇所を取りこぼす。"""
    out, depth = [], 0
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("<details"):
            depth += 1
        elif s.startswith("</details>"):
            depth = max(0, depth - 1)
        elif depth == 0 and not s.startswith(">"):
            out.append(s)
    return "\n".join(out)


def sentences(line: str):
    t = re.sub(r"<br\s*/?>", "。", line)
    return [x for x in re.split(r"(?<=[。？！?!])", t) if x.strip()]


def limit_for(line: str, base: int) -> int:
    """英語は 1 語あたりの字数が多いので上限を上げる。日本語基準を英文に当てると全部落ちる。"""
    ascii_ratio = sum(c.isascii() for c in line) / max(1, len(line))
    return int(base * 2.0) if ascii_ratio > 0.8 else base


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--max-chars", type=int, default=60)
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
        lines = spoken_lines(body)
        joined = "\n".join(lines) + "\n" + structure_markers(body)
        # 英語の検出語は大小を区別しない。"Show of hands" を取りこぼしていた
        hay = joined.lower()
        label = title[:40]
        # セッションの台本だけを検査する。**行数で除外しない。**
        # 短い枠ほど無検査で通ってしまう。除外は本文に明示のマーカーを置く：
        #     <!-- checks: skip -->              このセクションを検査しない
        #     <!-- checks: no-hands, no-clap -->  挙手・拍手の検査だけ外す
        if not TIME_RE.search(title):
            continue
        opts = set()
        mo = re.search(r"<!--\s*checks:\s*([^>]*?)-->", body)
        if mo:
            opts = {x.strip() for x in mo.group(1).split(",") if x.strip()}
        if "skip" in opts:
            print(f"{label:<42} 検査を外してあります（checks: skip）")
            continue

        for ln in lines:
            if BOLD_RE.search(ln):
                bad.append(f"{label}: 読み上げ文に太字 → {ln[:38]}")
                break
        for ln in lines:
            lim = limit_for(ln, args.max_chars)
            for s in sentences(ln):
                if len(s.strip()) > lim:
                    bad.append(f"{label}: 一文が {len(s.strip())} 字（上限 {lim}）"
                               f" → {s.strip()[:38]}…")
                    break
            else:
                continue
            break
        if "no-tag" not in opts and not any(h.lower() in hay for h in TAG_HINT):
            bad.append(f"{label}: **受けが無い**（答えを客席の言葉に置き直す動作）")
        if "no-setup" not in opts and not any(h.lower() in hay for h in SETUP_HINT):
            bad.append(f"{label}: **地ならしが無い**（いま何が起きているかの説明）")
        if "no-hands" not in opts and not any(h.lower() in hay for h in HAND_HINT):
            bad.append(f"{label}: 挙手が無い")
        if "no-clap" not in opts and not any(h.lower() in hay for h in CLAP_HINT):
            bad.append(f"{label}: 拍手を promptしていない")
        if "no-call" not in opts and not any(h.lower() in hay for h in CALL_HINT):
            bad.append(f"{label}: 客席への呼びかけが無い")
        for ln in lines:
            if HEDGE_RE.search(ln):
                bad.append(f"{label}: ぼかし → {ln[:38]}")
                break
        print(f"{label:<42} 読み上げ {len(lines):3} 行")

    if bad:
        print(f"\n落ちた検査 {len(bad)} 件:", file=sys.stderr)
        for b in bad:
            print("  -", b, file=sys.stderr)
        return 1
    print("\nOK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
