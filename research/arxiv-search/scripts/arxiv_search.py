#!/usr/bin/env python3
"""arXiv API を叩いて検索結果を要約付きで出す。

Usage:
    uv run python3 arxiv_search.py 'all:"AI alignment" AND all:economy'
    uv run python3 arxiv_search.py -n 10 --json 'ti:"formal verification" AND cat:cs.CR'
    uv run python3 arxiv_search.py --label 'singleton理論' 'all:singleton AND all:AI'

複数クエリを渡すと順に実行する。ラベルは --label を繰り返すか、省略すればクエリ文字列がそのまま使われる。
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}

BASE_URL = "https://export.arxiv.org/api/query"


def search_arxiv(query: str, max_results: int = 5, sort_by: str = "relevance") -> str:
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": sort_by,
        "sortOrder": "descending",
    }
    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_results(xml_data: str, summary_chars: int = 400) -> list[dict]:
    results = []
    root = ET.fromstring(xml_data)
    for entry in root.findall("atom:entry", NS):
        def text(tag: str) -> str:
            el = entry.find(tag, NS)
            return el.text.strip() if el is not None and el.text else ""

        summary = " ".join(text("atom:summary").split())
        if summary_chars and len(summary) > summary_chars:
            summary = summary[:summary_chars] + "..."
        results.append(
            {
                "title": " ".join(text("atom:title").split()),
                "url": text("atom:id"),
                "published": text("atom:published")[:10],
                "authors": [
                    a.findtext("atom:name", default="", namespaces=NS)
                    for a in entry.findall("atom:author", NS)
                ],
                "summary": summary,
            }
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("queries", nargs="+", help="arXiv API のクエリ文字列（all: / ti: / au: / cat: を AND OR で組む）")
    parser.add_argument("-n", "--max-results", type=int, default=5)
    parser.add_argument("--label", action="append", default=[], help="クエリごとの見出し。クエリと同じ数だけ繰り返す")
    parser.add_argument("--sort-by", default="relevance", choices=["relevance", "lastUpdatedDate", "submittedDate"])
    parser.add_argument("--summary-chars", type=int, default=400, help="0 で全文")
    parser.add_argument("--json", action="store_true", help="機械可読な JSON で出す")
    args = parser.parse_args()

    out = []
    for i, query in enumerate(args.queries):
        label = args.label[i] if i < len(args.label) else query
        try:
            results = parse_results(search_arxiv(query, args.max_results, args.sort_by), args.summary_chars)
        except Exception as exc:  # ネットワーク断・API 側の 5xx をクエリ単位で握る
            print(f"ERROR ({label}): {exc}", file=sys.stderr)
            results = []
        out.append({"label": label, "query": query, "results": results})

        if args.json:
            continue
        print(f"\n{'=' * 80}\nQUERY: {label}\n{'=' * 80}")
        if not results:
            print("  (no results)")
        for n, r in enumerate(results, 1):
            authors = ", ".join(r["authors"][:3]) + (" ほか" if len(r["authors"]) > 3 else "")
            print(f"\n  [{n}] {r['title']}")
            print(f"      {r['published']} | {authors}")
            print(f"      {r['url']}")
            print(f"      {r['summary']}")

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
