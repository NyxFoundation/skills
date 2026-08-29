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
  8. markdown leakage — literal ** left in the body by a converter that does not span lines
  9. internal paths — repo file names, script names, output directories
 10. fragmented paragraphs — the markdown converter emitting one paragraph per wrapped line
 11. length — character count and an estimated page count against the budget
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
SUPERLATIVE = ["原理的に", "唯一", "最高水準", "確実に", "最も容易", "必ず検出", "完全に防",
               "必ず破綻", "一切信頼", "最大の要因"]
HEDGE_OK = ["確認した範囲", "確認した公開情報の範囲", "前提条件が満たされ", "本 PoC の対象条件",
            "調査した範囲", "確認できた範囲", "本提案で確認した"]

# 文書が自分自身に言及する型。読み手には要らない情報で、AI が書いた気配として最も出やすい。
AI_TELL = [
    "順序はこうです", "ここは順序が大事", "先に断っておき", "最初に比較の限界",
    "本節は", "本節では", "本項では", "以下、", "ここでは", "書いておきます", "書いておく",
    "明示しておき", "述べておき", "示しておき", "整理しておき", "断っておく",
    "切り分けておき", "先に片付け", "まとめると", "以上のように", "つまるところ",
    "結論から言うと", "念のため申し添え",
]

# 相手に判断を委ねて終わる型。構造で説明していないサイン。
ABDICATION = ["御社の事業判断です", "貴社の事業判断です", "側の事業判断です", "判断に委ね",
              "お任せします", "ご判断ください。以上"]

# 提出物に出てはいけない内部の痕跡
INTERNAL = [
    (r"\bnotes/", "リポジトリのパス"),
    (r"\bout/", "出力ディレクトリ"),
    (r"\bbin/", "スクリプトのパス"),
    # src/ は相手方のリポジトリでも普通に出るので対象外。自分の生成物だけを見る
    (r"[\w-]+\.(?:py|js|sh|md)\b", "ソースファイル名"),
    (r"README", "リポジトリの README"),
    (r"\bv\d+\.\d+ (?:から|より|で入った|の変更)", "版間の差分への言及"),
]


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

    lines, heads, listed = [], [], set()
    for el in d.getElementsByTagName("w:body")[0].childNodes:
        if el.nodeName == "w:p":
            t = "［図］" if el.getElementsByTagName("w:drawing") else txt(el)
            ps = el.getElementsByTagName("w:pStyle")
            style = ps[0].getAttribute("w:val") if ps else ""
            if t.strip():
                lines.append(t)
                if style.startswith("Heading"):
                    heads.append((style, t.strip()))
                # 箇条書きは句点で終わらないのが普通。段落分断の検査から外す
                if style.startswith("List") or el.getElementsByTagName("w:numPr"):
                    listed.add(t.strip())
        elif el.nodeName == "w:tbl":
            for tr in el.getElementsByTagName("w:tr"):
                lines.append("| " + " | ".join(txt(tc).strip()
                             for tc in tr.getElementsByTagName("w:tc")) + " |")
    return lines, heads, listed


def main():
    path = sys.argv[1]
    dump = None
    if "--dump" in sys.argv:
        dump = sys.argv[sys.argv.index("--dump") + 1]

    z, bad_xml = load(path)
    lines, heads, listed = extract(z)
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
    # 「別紙 5.6」「付録 A 2.1」のような他文書への参照は対象外
    for m in re.finditer(r"(別紙|付録|添付)?\s*(\d+\.\d+)\s*(?:を|の|に|は)?ご?参照"
                         r"|(別紙|付録|添付)?\s*(\d+\.\d+)\s*に記載", full):
        other = m.group(1) or m.group(3)
        ref = m.group(2) or m.group(4)
        if other:                              # 他文書の節番号は解決しない
            continue
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

    # 8. markdown leakage --------------------------------------------------
    n_ast = sum(1 for ln in lines if "**" in ln)
    if n_ast:
        blockers.append(f"アスタリスクが本文に露出 × {n_ast} 行 — 強調記法が行をまたいでいる。"
                        "markdown 側で 1 行に収める")
    for mark in ("`", "|---", "](http"):
        n = sum(1 for ln in lines if mark in ln and not ln.startswith("|"))
        if n > 2:
            warns.append(f"markdown 記法らしき文字列「{mark}」× {n} 行")

    # 9. internal traces ---------------------------------------------------
    for pat, why in INTERNAL:
        hits = set()
        for ln in lines:
            if not re.search(pat, ln):
                continue
            # 相手方の公開リポジトリや URL の引用は痕跡ではない
            if "http" in ln or "github.com" in ln:
                continue
            hits.add(ln.strip()[:70])
        if hits:
            blockers.append(f"内部の痕跡（{why}）× {len(hits)}: {list(hits)[0]}")

    # 10. fragmented paragraphs --------------------------------------------
    # 変換器が markdown の折り返しを 1 行 1 段落で出すと、文の途中で段落が切れる。
    # 「。」「：」「表・図の行」以外で終わる段落が多いときは、その疑いが濃い。
    skip = {t for _, t in heads} | listed
    body = [ln for ln in lines
            if not ln.startswith("|") and len(ln) > 20 and ln.strip() not in skip
            and not re.match(r"^\s*[・\-\d]", ln)]
    if body:
        frag = [ln for ln in body if not re.search(r"[。：:）\)]$", ln)]
        ratio = len(frag) / len(body)
        if ratio > 0.25:
            blockers.append(
                f"段落の途中で改行されている疑い: {ratio:.0%}（{len(frag)}/{len(body)}）が句点で終わらない。"
                "変換器が markdown の折り返し行を 1 段落ずつ出していないか確認する")

    # 11. AI tells / abdication --------------------------------------------
    for w in AI_TELL:
        hit = next((ln for ln in lines if w in ln), None)
        if hit:
            warns.append(f"文書が自分に言及している「{w}」: {hit.strip()[:60]}")
    for w in ABDICATION:
        hit = next((ln for ln in lines if w in ln), None)
        if hit:
            warns.append(f"判断を委ねて終わっている「{w}」: {hit.strip()[:60]}")

    # 12. length -----------------------------------------------------------
    est = len(full) / 1400          # A4 縦・本文 10.5pt・表混在での実測係数
    print(f"  分量  {len(full):,} 文字 / 推定 {est:.0f} ページ")
    if est > 32:
        warns.append(f"推定 {est:.0f} ページ。30 ページを超えるなら本編と別紙に割ることを検討する")

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
