"""Generate a smooth multi-persona emotion-curve graph for a slide deck.

Usage:
    uv run --with matplotlib,numpy,scipy python3 generate_emotion_curve.py <data.json> [out.png]
    # or, with deps already installed:
    python3 generate_emotion_curve.py <data.json> [out.png]

Input JSON format:
{
  "title": "デッキ感情曲線分析",
  "x_label": "スライド",
  "y_label": "感情スコア (+5 〜 -5)",
  "sections": ["タイトル", "問題", "解決策", "実績", "未来", "CTA"],
  "personas": [
    {"name": "投資家A", "scores": [2, -3, 1, 3, 4, 2], "color": "#E74C3C"},
    {"name": "技術審査員B", "scores": [1, 2, 4, 2, 1, 1], "color": "#3498DB"}
  ],
  "highlight_valleys": [1],
  "highlight_landings": [5]
}

Output: PNG (default ./emotion_curve.png, override with the 2nd arg).
"""
import json
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from scipy.interpolate import make_interp_spline


def setup_cjk_font():
    """Make CJK (Japanese) labels render instead of tofu (□).

    Pass font *names* (not a file path). Variable Fonts such as NixOS's
    NotoSansCJK-VF.otf.ttc crash matplotlib's FT2Font when given via
    FontProperties(fname=...) ("SFNT font table missing; error code 0x8e"),
    so we rely on a name fallback list and let matplotlib pick what exists.
    If no CJK font is installed, labels fall back to DejaVu Sans (ASCII fine,
    CJK shows as tofu) — install e.g. fonts-noto-cjk to fix.
    """
    try:
        fm._load_fontmanager(try_read_cache=False)
    except Exception:
        pass
    plt.rcParams['font.family'] = [
        'Noto Sans CJK JP',
        'Noto Serif CJK JP',
        'Noto Sans CJK SC',
        'IPAexGothic',
        'IPAGothic',
        'Hiragino Sans',
        'Yu Gothic',
        'Meiryo',
        'DejaVu Sans',
        'sans-serif',
    ]
    plt.rcParams['axes.unicode_minus'] = False


setup_cjk_font()


def generate_emotion_curve(data_path, output_path=None):
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    sections = data.get("sections", [])
    personas = data.get("personas", [])
    title = data.get("title", "感情曲線分析")
    x_label = data.get("x_label", "スライド")
    y_label = data.get("y_label", "感情スコア (+5 〜 -5)")
    highlight_valleys = data.get("highlight_valleys", [])
    highlight_landings = data.get("highlight_landings", [])

    n_sections = len(sections)
    x = np.arange(n_sections)

    fig, ax = plt.subplots(figsize=(14, 8))

    # 中立ライン
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)

    for persona in personas:
        name = persona["name"]
        scores = persona["scores"]
        color = persona.get("color", None)

        # スプライン補間で滑らかな曲線（3点以上で3次、2点は線形）
        if len(scores) >= 3:
            x_input = np.arange(len(scores))
            x_smooth = np.linspace(x_input.min(), x_input.max(), 300)
            spl = make_interp_spline(x_input, scores, k=3)
            y_smooth = np.clip(spl(x_smooth), -5.5, 5.5)
            ax.plot(x_smooth, y_smooth, label=name, linewidth=2.5,
                    color=color, alpha=0.85)
        else:
            ax.plot(x, scores, label=name, linewidth=2.5,
                    color=color, alpha=0.85)

        # データポイントにマーカー＋数値ラベル
        for xi, yi in zip(x, scores):
            ax.plot(xi, yi, 'o', color=color, markersize=8,
                    markeredgecolor='white', markeredgewidth=1.5, zorder=5)
            offset = 12 if yi >= 0 else -18
            ax.annotate(f'{yi:+d}', (xi, yi), textcoords="offset points",
                        xytext=(0, offset), ha='center', fontsize=9, alpha=0.8,
                        color=color, fontweight='bold')

    # スライド境界の縦線
    for xi in x:
        ax.axvline(x=xi, color='gray', alpha=0.08, linewidth=0.5)

    # 谷（共通の低ポイント）
    for vi in highlight_valleys:
        if 0 <= vi < n_sections:
            ax.axvspan(vi - 0.25, vi + 0.25, alpha=0.08, color='red', zorder=0)
            ax.annotate('▼ Valley', (vi, -5.0), fontsize=10, color='#C0392B',
                        ha='center', fontweight='bold', alpha=0.8)

    # 着地（終了時の印象）
    for li in highlight_landings:
        if 0 <= li < n_sections:
            ax.axvspan(li - 0.25, li + 0.25, alpha=0.08, color='green', zorder=0)
            ax.annotate('▲ Landing', (li, 5.0), fontsize=10, color='#27AE60',
                        ha='center', fontweight='bold', alpha=0.8)

    ax.set_xticks(x)
    ax.set_xticklabels(sections, fontsize=11)
    ax.set_ylim(-5.5, 5.5)
    ax.set_yticks(range(-5, 6))
    ax.set_yticklabels([str(i) for i in range(-5, 6)], fontsize=10)
    ax.tick_params(axis='y', colors='gray')

    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)

    # 感情ゾーンの背景色
    ax.axhspan(0, 5.5, alpha=0.02, color='green')
    ax.axhspan(-5.5, 0, alpha=0.02, color='red')

    ax.legend(loc='upper right', fontsize=11, framealpha=0.9,
              edgecolor='lightgray', fancybox=True, shadow=False)
    ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5, axis='y')
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color('lightgray')
        spine.set_linewidth(0.5)

    plt.tight_layout()

    if output_path is None:
        output_path = 'emotion_curve.png'
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f'Saved to {output_path}')
    return output_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python generate_emotion_curve.py <data.json> [output.png]")
        sys.exit(1)
    data_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    generate_emotion_curve(data_path, output_path)
