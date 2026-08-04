# problem_translation_wall.py — 「見過ごされてきた根本問題」冒頭挿入図 (v2)
# PR原稿: Aladdin Security 共同研究 (Notion: PR-Aladdin-Security-3a2d05af0d5a817a879ad23ac2f5197e)
#
# 生成: uv run --with matplotlib python3 figures/problem_translation_wall.py
# 出力: public/images/problem_translation_wall.png
#
# v2改訂の経緯: 初版は「自然言語→Lean命題の翻訳」を圏論が保証する、という筋書きだったが、
# 社内研究メモ「圈論的中間表現によるLean証明AI強化」はこれを明示的に否定している
# （formalization gapは圏論化でも消えない、とオープンクエスチョンに明記）。
# 圏論が実際に効くのはLean命題確定"後"の証明探索層 (H1探索圧縮/H2転移学習/H3計画可視化)。
# 従って問題図も「翻訳の壁」ではなく「具体構造ごとに証明をゼロから独立探索している非効率」
# (定理の「在庫」が構造の数だけ膨張する) に描き直す。solution_category_theory.py と対で読む。

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyArrowPatch, Circle, Polygon

candidates = ["Noto Sans CJK JP", "Noto Sans JP", "IPAexGothic", "IPAGothic", "TakaoGothic"]
available = {f.name for f in fm.fontManager.ttflist}
font_family = next((c for c in candidates if c in available), "sans-serif")
plt.rcParams["font.family"] = font_family
plt.rcParams["axes.unicode_minus"] = False

OUT = "/home/gohan/workspace/pr-aladdin-security/public/images/problem_translation_wall.png"

SURFACE = "#ffffff"
GRAY = "#475569"
TEXT_PRIMARY = "#1f2937"
TEXT_MUTED = "#6b7280"
RED = "#dc2626"

fig, ax = plt.subplots(figsize=(13.4, 6.6), dpi=200)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
ax.set_xlim(0, 1260)
ax.set_ylim(70, 590)
ax.axis("off")


# ---------------------------------------------------------------- icon library
def icon_document(cx, cy, s=24, color=GRAY):
    w, h = s * 1.05, s * 1.3
    fold = s * 0.36
    pts = [(cx - w / 2, cy - h / 2), (cx - w / 2, cy + h / 2), (cx + w / 2 - fold, cy + h / 2),
           (cx + w / 2, cy + h / 2 - fold), (cx + w / 2, cy - h / 2)]
    ax.add_patch(Polygon(pts, closed=True, facecolor="white", edgecolor=color, linewidth=1.8, zorder=8))
    ax.add_patch(Polygon([(cx + w / 2 - fold, cy + h / 2), (cx + w / 2, cy + h / 2 - fold),
                           (cx + w / 2 - fold, cy + h / 2 - fold)], closed=True,
                          facecolor=color, edgecolor="none", zorder=8, alpha=0.5))
    for dy in (0.12, -0.14, -0.4):
        ax.plot([cx - w * 0.3, cx + w * 0.22], [cy + dy * h, cy + dy * h],
                color=color, linewidth=1.6, zorder=9, solid_capstyle="round")


def icon_search_tree(cx, cy, s=34, color=RED):
    """探索木アイコン: root→2分岐→4葉。3つの葉が赤い×(手戻り)、1つだけ成功。
    「広く探索してほとんど無駄になる」ことを形で示す。"""
    root = (cx, cy + s * 0.62)
    mids = [(cx - s * 0.36, cy + s * 0.08), (cx + s * 0.36, cy + s * 0.08)]
    leaves = [(cx - s * 0.58, cy - s * 0.55), (cx - s * 0.16, cy - s * 0.55),
              (cx + s * 0.16, cy - s * 0.55), (cx + s * 0.58, cy - s * 0.55)]
    for m in mids:
        ax.plot([root[0], m[0]], [root[1], m[1]], color=GRAY, linewidth=1.4, zorder=8)
    ax.plot([mids[0][0], leaves[0][0]], [mids[0][1], leaves[0][1]], color=GRAY, linewidth=1.2, zorder=8)
    ax.plot([mids[0][0], leaves[1][0]], [mids[0][1], leaves[1][1]], color=GRAY, linewidth=1.2, zorder=8)
    ax.plot([mids[1][0], leaves[2][0]], [mids[1][1], leaves[2][1]], color=GRAY, linewidth=1.2, zorder=8)
    ax.plot([mids[1][0], leaves[3][0]], [mids[1][1], leaves[3][1]], color=GRAY, linewidth=1.2, zorder=8)
    ax.add_patch(Circle(root, s * 0.075, facecolor=GRAY, edgecolor="none", zorder=9))
    for m in mids:
        ax.add_patch(Circle(m, s * 0.065, facecolor=GRAY, edgecolor="none", zorder=9))
    for i, leaf in enumerate(leaves):
        if i == 2:
            ax.add_patch(Circle(leaf, s * 0.1, facecolor=GRAY, edgecolor="none", zorder=9))
            ax.plot([leaf[0] - s * 0.06, leaf[0] - s * 0.01, leaf[0] + s * 0.08],
                    [leaf[1], leaf[1] - s * 0.06, leaf[1] + s * 0.07],
                    color="white", linewidth=1.8, zorder=10, solid_capstyle="round")
        else:
            d = s * 0.08
            ax.plot([leaf[0] - d, leaf[0] + d], [leaf[1] - d, leaf[1] + d], color=color, linewidth=2.2,
                    zorder=9, solid_capstyle="round")
            ax.plot([leaf[0] - d, leaf[0] + d], [leaf[1] + d, leaf[1] - d], color=color, linewidth=2.2,
                    zorder=9, solid_capstyle="round")


# ---------------------------------------------------------------- primitives
def entity(cx, cy, icon_fn, label, sub=None, color=TEXT_PRIMARY, sub_color=None,
           fontsize=17, subfontsize=15, gap=42, subgap=22, on_line=False, on_line_fc="white"):
    icon_fn(cx, cy)
    bbox = dict(facecolor=on_line_fc, edgecolor="none", pad=3) if on_line else None
    ax.text(cx, cy - gap, label, ha="center", va="center", fontsize=fontsize,
            fontweight="bold", color=color, zorder=12, bbox=bbox)
    if sub:
        ax.text(cx, cy - gap - subgap, sub, ha="center", va="center", fontsize=subfontsize,
                fontweight="bold", color=(sub_color or color), zorder=12, bbox=bbox)


def straight(p1, p2, color=GRAY, lw=2.4, ls="solid", z=4):
    a = FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=17, linewidth=lw,
                         color=color, linestyle=ls, zorder=z, shrinkA=2, shrinkB=2)
    ax.add_patch(a)


# ===================================================================== 座標定数
ROW1_Y = 465   # 具体的な定理
ROW2_Y = 300   # 証明探索 (毎回ゼロから)
COLS = [250, 630, 1010]
STRUCTS = ["Grp（群）", "Top（位相空間）", "Ring（環）"]

for x, struct in zip(COLS, STRUCTS):
    straight((x, ROW1_Y - 46), (x, ROW2_Y + 52), lw=2.2)
    entity(x, ROW1_Y, lambda cx, cy: icon_document(cx, cy, s=25), "具体的な定理", sub=struct,
           sub_color=TEXT_MUTED, on_line=True)
    entity(x, ROW2_Y, lambda cx, cy: icon_search_tree(cx, cy, s=36), "証明探索",
           sub="毎回ゼロから", color=TEXT_PRIMARY, sub_color=RED, gap=52, subgap=22)

# ===================================================================== 結論ラベル
ax.text(630, 175, "同じ「形」をした主張を、構造の数だけ独立に証明し直している",
        ha="center", va="center", fontsize=17, fontweight="bold", color=RED, zorder=12)
ax.text(630, 138, "定理の「在庫」は具体的な構造の数だけ膨張し、探索コストは増え続ける",
        ha="center", va="center", fontsize=14.5, fontweight="bold", color=TEXT_MUTED, zorder=12)

plt.tight_layout(pad=1.0)
plt.savefig(OUT, facecolor=SURFACE, bbox_inches="tight")
print("saved:", OUT, "| font:", font_family)
