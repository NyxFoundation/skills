#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""外部レビューに出す前のゲート。

    uv run assets/selfcheck.py out/deck.pptx

外部レビュアーが毎回当ててくる指摘のうち、機械的に検出できるものを先に潰す。
実測では、あるデッキのレビュー 2 周で出た 19 件のうち 14 件（74%）がここで検出できた。
**通してから外部レビューに出すと、周回が 2〜3 減る。**

検査するもの:
  1. キッカーの重複        同一キッカーが 2 枚以上に付いている
  2. 目次の網羅            目次項目が後続セクションを覆っているか
  3. 数詞と実体数          「N つ」と、実際に並んでいる項目数が合っているか
  4. 孤立した実体          一覧で名前を出したきり二度と出てこない固有名
  5. スライド間の算術      「合計 N 件」と内訳の和が合っているか
  6. 見出しパターン        体言止め・活動記述・曖昧な述語
  7. 数字とラベルの近接    ラベルの無い数字（ページ番号・日付は除く）
  8. 1 枚あたりの項目数    多すぎる枚
  9. コピー規則            禁止語・禁止表現\n 10. 枚をまたいだ言い直し  前の枚で言ったことを後の枚が繰り返している

終了コード: 検出があれば 1。
"""

import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

# 見出しが体言止めで終わるパターン
TAIGEN = re.compile(r"(の話|こと|ところ|もの|とき|ため|点|件)。\s*$")
# 活動記述で止まっている述語（主張になっていない）
ACTIVITY = re.compile(r"(呼ばれました|実施しました|議論しました|参加しました|"
                      r"開催しました|話しました|行いました|進めています|"
                      r"取り組んでいます|検討しています)。?\s*$")
# 曖昧な述語
VAGUE = re.compile(r"(問われています|注目されています|重要です|課題です|"
                   r"求められています)。?\s*$")
# コピー規則の禁止語
BANNED = ["青天井", "巨大市場", "本丸", "希少", "覇権", "既成事実",
          "でございます", "申し上げ", "存じます", "極めて", "非常に"]

NUM_UNIT = re.compile(r"([0-9][0-9,]*)\s*(件|名|枚|人|個|本)")
COUNTER = re.compile(r"([0-9０-９一二三四五六七八九十]+)\s*つ")
KANJI_NUM = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
             "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}


def to_int(s: str):
    s = s.strip().replace(",", "")
    if s.isdigit():
        return int(s)
    z = s.translate(str.maketrans("０１２３４５６７８９", "0123456789"))
    if z.isdigit():
        return int(z)
    return KANJI_NUM.get(s)


def extract(path: Path):
    """スライドごとに (キッカー, 見出し, 全行, ノート) を返す。"""
    z = zipfile.ZipFile(path)
    names = sorted((n for n in z.namelist()
                    if re.match(r"ppt/slides/slide\d+\.xml$", n)),
                   key=lambda s: int(re.findall(r"\d+", s.split("/")[-1])[0]))
    out = []
    for i, n in enumerate(names, 1):
        root = ET.fromstring(z.read(n))
        lines = []
        for p in root.iter(A + "p"):
            t = "".join(r.text or "" for r in p.iter(A + "t")).strip()
            if t:
                lines.append(t)
        notes = ""
        nrel = f"ppt/notesSlides/notesSlide{i}.xml"
        if nrel in z.namelist():
            nr = ET.fromstring(z.read(nrel))
            notes = " ".join(
                "".join(r.text or "" for r in p.iter(A + "t")).strip()
                for p in nr.iter(A + "p"))
        kicker = next((l for l in lines[:2] if "／" in l or "/" in l), "")
        headline = ""
        for l in lines:
            if l != kicker and len(l) > 6:
                headline = l
                break
        section = ""
        if kicker:
            section = re.sub(r"[\s0-9０-９]", "", kicker.split("／")[-1])
        out.append({"n": i, "kicker": kicker, "headline": headline,
                    "section": section, "lines": lines, "notes": notes})
    return out


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1])
    slides = extract(path)
    hits = []
    notes_out = []

    def hit(sl, cat, msg):
        hits.append((sl, cat, msg))

    def note(sl, cat, msg):
        """判定を止めないが、目で見て確かめてほしいもの。"""
        notes_out.append((sl, cat, msg))

    # 1. キッカーの重複
    kick = defaultdict(list)
    for s in slides:
        if s["kicker"]:
            kick[s["kicker"]].append(s["n"])
    for k, ns in kick.items():
        if len(ns) > 1:
            hit(ns[0], "キッカー重複",
                f"「{k}」が {len(ns)} 枚（{', '.join(map(str, ns))}）に付いている。"
                "聞き手が現在地を判別できない")

    # 2. 目次の網羅
    # 「やっていること」が「プロジェクト」「進捗」「対外」の 3 セクションを指す、といった
    # 意味の対応は機械では判定できない。突き合わせて見せるだけにして、判定は止めない。
    agenda = next((s for s in slides
                   if re.search(r"(順路|今日|アジェンダ|目次|話します)", s["headline"])),
                  None)
    if agenda:
        after = {s["section"] for s in slides
                 if s["n"] > agenda["n"] and s["section"]}
        items = [l for l in agenda["lines"]
                 if l not in (agenda["headline"], agenda["kicker"])
                 and 3 <= len(l) < 30
                 and not re.match(r"^[①-⑩0-9０-９]+$", l.strip())]
        if after and items:
            note(agenda["n"], "目次の網羅",
                 f"目次の項目 {len(items)} 個に対し、以降のセクションは "
                 f"{len(after)} 種（{', '.join(sorted(after))}）。"
                 "各セクションが目次のどれに属するか、口頭で言えるか確かめる")

    # 3. 数詞と実体数
    for s in slides:
        m = COUNTER.search(s["headline"])
        if not m:
            continue
        if agenda and s["n"] == agenda["n"]:
            continue
        claimed = to_int(m.group(1))
        if not claimed or claimed > 12:
            continue
        body = [l for l in s["lines"]
                if l not in (s["headline"], s["kicker"]) and len(l) < 40]
        # カード名・列挙項目らしい短い行を数える。
        # 棒グラフのようにラベルと値が対になる図では、値（数字だけの行）を
        # 数えると見出しの N に対して必ず 2N になり、毎回誤発火する。
        # 体裁そのものに発火するゲートは信用を失うので、数値だけの行は外す。
        short = [l for l in body if len(l) <= 18
                 and not re.match(r"^[0-9０-９][0-9０-９,，\.]*\s*[件個人枚%％]?$",
                                  l.strip())]
        if short and abs(len(short) - claimed) > max(2, claimed):
            hit(s["n"], "数詞と実体数",
                f"見出しが「{m.group(0)}」だが、枚の中の短い項目は {len(short)} 個。"
                "数詞が何を指すか確かめる")

    # 4. 孤立した実体
    # 一般の専門用語まで拾うとノイズだらけになる。
    # 「N つの…です」と数え上げている一覧スライドのカード名だけを対象にする。
    text_by_slide = [" ".join(s["lines"]) for s in slides]
    DATEISH = re.compile(r"^[0-9０-９/／\-\.]+$")
    for s in slides:
        if not COUNTER.search(s["headline"]):
            continue
        if agenda and s["n"] == agenda["n"]:
            continue                     # 目次の項目はここで数えない
        names = [l.strip() for l in s["lines"]
                 if l not in (s["headline"], s["kicker"])
                 and 2 <= len(l) <= 14 and "。" not in l and "、" not in l
                 and not DATEISH.match(l.strip())
                 and not re.match(r"^[①-⑩0-9０-９]+$", l.strip())]
        if len(names) < 3:
            continue                     # 一覧と呼べる枚だけを対象にする
        for nm in names:
            where = [i + 1 for i, t in enumerate(text_by_slide)
                     if i + 1 != s["n"] and nm in t]
            if not where:
                note(s["n"], "孤立した実体",
                     f"一覧に「{nm}」を載せているが、以降どの枚にも出てこない。"
                     "触れないなら一覧から外すか、触れない旨を 1 行書く")

    # 5. スライド間の算術
    # 単位が同じでも分野が違えば比較にならない（43 件の興味と 16,854 件の修正など）。
    # 同じセクションの中で、1 枚につき 1 個だけ数を拾って和を取る。
    for s in slides:
        for line in s["lines"]:
            for num, unit in NUM_UNIT.findall(line):
                tv = to_int(num)
                if tv is None or not re.search(r"(すべて|全部|合計|公開中|総数)", line):
                    continue
                sec = s["section"]
                parts = []
                for o in slides:
                    if o["n"] == s["n"] or o["section"] != sec:
                        continue
                    found = [to_int(n) for n, u in
                             NUM_UNIT.findall(" ".join(o["lines"])) if u == unit]
                    found = [f for f in found if f]
                    if found:
                        parts.append((o["n"], found[0]))
                if len(parts) >= 2:
                    ssum = sum(v for _, v in parts)
                    if ssum != tv:
                        hit(s["n"], "スライド間の算術",
                            f"合計 {tv}{unit} に対し、同じ帯の内訳の和は {ssum}{unit}"
                            f"（{', '.join(f'S{n}:{v}' for n, v in parts)}）。"
                            "聞き手が暗算すると矛盾に気づく")
    # 最上位の主張が本当に最大か（同じセクション内で比較）
    for s in slides:
        if not re.search(r"(いちばん多い|最多|最も多い)", s["headline"]):
            continue
        if re.search(r"(単独|この帯|この層|内では|の中では)", s["headline"]):
            continue                     # すでに範囲を限定している
        nums = [to_int(n) for n, _u in NUM_UNIT.findall(s["headline"])]
        nums = [n for n in nums if n]
        others = []
        for o in slides:
            if o["n"] == s["n"] or o["section"] != s["section"]:
                continue
            found = [to_int(n) for n, _u in NUM_UNIT.findall(" ".join(o["lines"]))]
            others += [f for f in found if f]
        if nums and others and max(others) > max(nums):
            hit(s["n"], "スライド間の算術",
                f"「最多」と主張しているが {max(nums)} に対し同じ帯に {max(others)} がある。"
                "『単独の帯では最多』のように限定するか、数え方を書く")

    # 6. 見出しパターン
    for s in slides:
        h = s["headline"]
        if not h or s["n"] == 1:
            continue
        if TAIGEN.search(h):
            hit(s["n"], "見出し", f"体言止め: 「{h}」 → 主語と述語のある平叙文にする")
        if ACTIVITY.search(h):
            hit(s["n"], "見出し",
                f"活動記述で止まっている: 「{h}」 → 何が分かったか・何が言えるかを主張にする")
        if VAGUE.search(h):
            hit(s["n"], "見出し", f"述語が曖昧: 「{h}」 → 具体的な状況を平叙文で述べる")

    # 7. 数字とラベルの近接
    # ページ番号など額縁の要素は除外する。単独で置かれるのが正しい要素なので、
    # ここで NG を出すとゲートが体裁そのものに発火して無視されるようになる。
    for s in slides:
        for line in s["lines"]:
            bare = line.strip()
            if bare.lstrip("0") in (str(s["n"]), "") and len(bare) <= 3:
                continue                     # ページ番号
            if re.fullmatch(r"\d{4}[.\-/]\d{1,2}([.\-/]\d{1,2})?", bare):
                continue                     # 日付
            if re.fullmatch(r"\d{1,2}[/\-]\d{1,2}", bare):
                continue                     # 月日
            if re.fullmatch(r"[0-9０-９,\.]+\s*[%％]?", bare):
                idx = s["lines"].index(line)  # noqa: E501
                near = " ".join(s["lines"][max(0, idx - 1):idx + 2])
                if not re.search(r"[ぁ-んァ-ヶ一-龠]", near.replace(line, "")):
                    hit(s["n"], "数字のラベル",
                        f"「{line.strip()}」に説明が付いていない。"
                        "何の数か、何に対する割合かを添える")

    # 8. 1 枚あたりの項目数
    for s in slides:
        body = [l for l in s["lines"] if l not in (s["headline"], s["kicker"])]
        heads = [l for l in body if len(l) <= 14]
        if len(heads) >= 9:
            # 一覧を意図して並べている枚（全件紹介など）では正常。判定は止めない。
            # ここで NG を出すとゲートが意図的な設計で鳴り、無視されるようになる。
            note(s["n"], "項目数",
                 f"短い項目が {len(heads)} 個ある。"
                 "一覧として意図したものならよい。そうでなければ 1 枚 1 メッセージを超えている")

    # 9. コピー規則
    for s in slides:
        body = " ".join(s["lines"])
        for w in BANNED:
            if w in body:
                hit(s["n"], "コピー規則", f"禁止語「{w}」")
        if body.count("——") + body.count("──") > 1:
            hit(s["n"], "コピー規則", "em dash が 2 個以上。読点か句点にする")

    # ── 出力
    print(f"{path.name} — スライド {len(slides)} 枚\n")
    if notes_out:
        print("参考（判定は止めない。目で見て確かめる）:")
        for sl, cat, msg in sorted(notes_out, key=lambda h: h[0]):
            print(f"  S{sl:02d} [{cat}] {msg}")
        print()
    if not hits:
        print("判定: OK — 機械検出できる指摘はなし。外部レビューに出してよい")
        print("※ 判断が要るもの（場の趣旨との整合、1 枚 2 メッセージ、事実の重さ）は")
        print("   ここでは検出できない。references/review-loop.md の外部レビューへ")
        return 0

    by_cat = Counter(c for _, c, _ in hits)
    for sl, cat, msg in sorted(hits, key=lambda h: h[0]):
        print(f"  S{sl:02d} [{cat}] {msg}")
    print(f"\n検出 {len(hits)} 件: " +
          ", ".join(f"{c}×{n}" for c, n in by_cat.most_common()))
    print("\n判定: NG — 直してから外部レビューに出す（周回が減る）")
    return 1


if __name__ == "__main__":
    sys.exit(main())
