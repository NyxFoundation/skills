#!/usr/bin/env bash
# .pptx → PDF → 1 枚ずつの PNG → コンタクトシート
#
#   bash assets/render.sh out/deck.pptx /tmp/render
#
# 毎周これを回して「自分の目で見る」。python-pptx はテキストの溢れにも、
# 存在しないフォントにも、無言で失敗するプロパティにも例外を出さない。
#
# 注意: LibreOffice の描画は PowerPoint の描画ではない。特に折り返し位置が違い、
# それが溢れの有無を決める。最終確認は実機の PowerPoint で開くこと。
set -euo pipefail

PPTX="${1:?usage: render.sh <deck.pptx> [outdir]}"
OUT="${2:-/tmp/pptx-render}"
DENSITY="${DENSITY:-110}"
TILE="${TILE:-3x4}"

PPTX="$(readlink -f "$PPTX")"
rm -rf "$OUT" && mkdir -p "$OUT"

echo "PDF に変換..."
if command -v soffice >/dev/null 2>&1; then
  soffice --headless --convert-to pdf --outdir "$OUT" "$PPTX" >/dev/null 2>&1
else
  # NixOS: pip も apt も使わない。nix-shell で引く
  nix-shell -p libreoffice-fresh --run \
    "soffice --headless --convert-to pdf --outdir '$OUT' '$PPTX'" >/dev/null 2>&1
fi

PDF="$OUT/$(basename "${PPTX%.pptx}").pdf"
[ -f "$PDF" ] || { echo "PDF 変換に失敗した: $PDF" >&2; exit 1; }

echo "PNG に展開..."
magick -density "$DENSITY" "$PDF" -quality 90 "$OUT/p-%02d.png" >/dev/null 2>&1

N=$(find "$OUT" -name 'p-*.png' | wc -l)
echo "コンタクトシートを作成... ($N 枚)"
# shellcheck disable=SC2046
magick montage $(find "$OUT" -name 'p-*.png' | sort) \
  -tile "$TILE" -geometry 460x259+5+5 -background '#dddddd' \
  "$OUT/contact.png" >/dev/null 2>&1

echo
echo "  $OUT/contact.png     ← まずこれを見る（溢れ・衝突・空白の偏りは縮小画像で見つかる）"
echo "  $OUT/p-NN.png        ← そのあと個別に文言を読む"
