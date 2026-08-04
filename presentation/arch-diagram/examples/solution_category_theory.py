# solution_category_theory.py — 「解決策：証明の中間表現への圏論の導入」冒頭挿入図 (v2)
# PR原稿: Aladdin Security 共同研究 (Notion: PR-Aladdin-Security-3a2d05af0d5a817a879ad23ac2f5197e)
#
# 生成: uv run --with matplotlib python3 figures/solution_category_theory.py
# 出力: public/images/solution_category_theory.png
#
# problem_translation_wall.py (v2) と対で読む図。問題図で示した「Grp/Top/Ringそれぞれで
# 同じ形の定理をゼロから探索している」状態に対し、抽象定理を圏論的中間表現として一度だけ証明し、
# 関手 (functor) で各具体構造へ転用する — というH2(翻訳辞書=転移学習)を主役に、
# H1(探索圧縮)・H3(証明計画の可視化)を脇に添えて描く。
# 圏論の役割はあくまで Lean命題確定後の証明探索層であり、自然言語→Lean命題の翻訳を保証する
# ものではない (社内研究メモのオープンクエスチョンに明記の通り)。

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

OUT = "/home/gohan/workspace/pr-aladdin-security/public/images/solution_category_theory.png"

SURFACE = "#ffffff"
GRAY = "#475569"
TEXT_PRIMARY = "#1f2937"
TEXT_MUTED = "#6b7280"
INDIGO = "#6366f1"

fig, ax = plt.subplots(figsize=(13.4, 6.6), dpi=200)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
ax.set_xlim(0, 1260)
ax.set_ylim(-40, 680)
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


def icon_category(cx, cy, s=30, color=INDIGO):
    """圏論的中間表現アイコン: 可換三角 (F, G, H=G∘F)。抽象定理そのものを表す。"""
    top = (cx, cy + s * 0.55)
    bl = (cx - s * 0.52, cy - s * 0.42)
    br = (cx + s * 0.52, cy - s * 0.42)
    for p1, p2 in [(top, bl), (top, br), (bl, br)]:
        a = FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=10,
                             linewidth=1.9, color=color, zorder=9, shrinkA=5, shrinkB=5)
        ax.add_patch(a)
    for p in (top, bl, br):
        ax.add_patch(Circle(p, s * 0.095, facecolor=color, edgecolor="none", zorder=10))


def icon_check(cx, cy, s=30, color=GRAY):
    ax.add_patch(Circle((cx, cy), s * 0.5, facecolor=color, edgecolor="none", zorder=8))
    ax.plot([cx - s * 0.24, cx - s * 0.04, cx + s * 0.28],
            [cy + s * 0.02, cy - s * 0.18, cy + s * 0.22],
            color="white", linewidth=2.4, solid_capstyle="round", solid_joinstyle="round", zorder=9)


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
TOP_Y = 650     # 抽象定理 (圏論的中間表現)
TRUNK_Y = 490   # 分岐トランクの水平線
ROW1_Y = 340    # 具体的な定理 (各構造)
ROW2_Y = 170    # 検証 (探索ほぼ不要)
COLS = [250, 630, 1010]
STRUCTS = ["Grp（群）", "Top（位相空間）", "Ring（環）"]

entity(630, TOP_Y, lambda cx, cy: icon_category(cx, cy, s=32), "抽象定理",
       sub="二項積を持つ任意の圏で一度だけ証明", color=TEXT_PRIMARY, sub_color=INDIGO,
       gap=48, subgap=24)

# 抽象定理 → 分岐トランク → 各具体構造へ関手で転用 (直角配線 + 合流ではなく分岐)
straight((630, TOP_Y - 110), (630, TRUNK_Y), lw=2.2, color=INDIGO)
ax.plot([COLS[0], COLS[2]], [TRUNK_Y, TRUNK_Y], color=INDIGO, linewidth=2.0, zorder=4)
ax.text(420, TRUNK_Y + 17, "関手で転用", ha="center", va="center", fontsize=14,
        fontweight="bold", color=INDIGO, zorder=6,
        bbox=dict(facecolor="white", edgecolor="none", pad=2))
for x in COLS:
    straight((x, TRUNK_Y), (x, ROW1_Y + 46), lw=2.0, color=INDIGO)

for x, struct in zip(COLS, STRUCTS):
    straight((x, ROW1_Y - 46), (x, ROW2_Y + 24), lw=2.0)
    entity(x, ROW1_Y, lambda cx, cy: icon_document(cx, cy, s=25), "具体的な定理", sub=struct,
           sub_color=TEXT_MUTED, on_line=True)
    entity(x, ROW2_Y, lambda cx, cy: icon_check(cx, cy, s=30, color=GRAY), "検証",
           sub="探索ほぼ不要 ✓", color=TEXT_PRIMARY, sub_color=TEXT_MUTED, gap=40, subgap=21)

# ===================================================================== 3つの効果
effects = [
    "① 証明探索の分岐削減：抽象定理を中間表現とすることで、無闇な探索を減らせる",
    "② 転移学習：抽象定理１つの証明で、対応する具体的な問題がまとめて解ける",
    "③ 証明計画の可視化：サブゴールの構造を人間が追跡可能な形で表現できる",
]
for i, line in enumerate(effects):
    ax.text(630, 45 - i * 30, line, ha="center", va="center", fontsize=15,
            fontweight="bold", color=INDIGO, zorder=12)

plt.tight_layout(pad=1.0)
plt.savefig(OUT, facecolor=SURFACE, bbox_inches="tight")
print("saved:", OUT, "| font:", font_family)
