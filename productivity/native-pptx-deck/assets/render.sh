#!/usr/bin/env bash
# .pptx → PDF → PNG → contact sheet. ImageMagick is not required.
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
COLS="${TILE%%x*}"
SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

PPTX="$(readlink -f "$PPTX")"
mkdir -p "$OUT"
OUT="$(readlink -f "$OUT")"
STAGE="$(mktemp -d -t native-pptx-render.XXXXXXXX)"
trap 'rm -rf -- "$STAGE"' EXIT

echo "PDF に変換..."
if command -v soffice >/dev/null 2>&1; then
  soffice "-env:UserInstallation=file://$STAGE/profile" --headless \
    --convert-to pdf --outdir "$STAGE" "$PPTX"
else
  # NixOS: pip も apt も使わない。nix-shell で引く
  env NYX_RENDER_PPTX="$PPTX" NYX_RENDER_STAGE="$STAGE" \
    nix-shell -p libreoffice-fresh --run \
    'soffice "-env:UserInstallation=file://$NYX_RENDER_STAGE/profile" --headless --convert-to pdf --outdir "$NYX_RENDER_STAGE" "$NYX_RENDER_PPTX"'
fi

PDF="$STAGE/$(basename "${PPTX%.pptx}").pdf"
[ -f "$PDF" ] || { echo "PDF 変換に失敗した: $PDF" >&2; exit 1; }

echo "PNG に展開..."
uv run "$SKILL_ROOT/scripts/render_pdf.py" "$PDF" "$OUT" --dpi "$DENSITY" --cols "$COLS"
cp -- "$PDF" "$OUT/$(basename "$PDF")"

echo
echo "  $OUT/contact.png     ← まずこれを見る（溢れ・衝突・空白の偏りは縮小画像で見つかる）"
echo "  $OUT/p-NN.png        ← そのあと個別に文言を読む"
