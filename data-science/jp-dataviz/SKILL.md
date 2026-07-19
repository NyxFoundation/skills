---
name: jp-dataviz
description: |
  Generate charts/graphs with matplotlib on this NixOS machine, including Japanese text that renders
  correctly (Noto Sans CJK JP font-cache fix — direct fname loading of the VF .ttc FAILS). Covers the
  uv run template, chart quality defaults, saving to ~/.hermes/workspace/, and delivering to the Slack
  thread. Load whenever the user asks for a chart, graph, plot, visualization, グラフ, 図, 可視化 —
  ESPECIALLY if any label/title contains Japanese.
version: 1.0.0
author: gohan (via Claude Code tuning)
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [chart, graph, matplotlib, visualization, japanese, cjk, dataviz, グラフ, 可視化]
---

# Charts with Japanese Text (matplotlib on NixOS)

## Execution template

Always via uv (never bare python3):

```bash
uv run --with matplotlib,numpy,pandas python3 - <<'EOF'
# chart code here
EOF
```

Add `seaborn`, `scipy`, `pillow` to `--with` as needed.

## Japanese font setup — THE ONLY WAY THAT WORKS

`Noto Sans CJK JP` is installed as a Variable Font .ttc under
`/run/current-system/sw/share/fonts/opentype/noto-cjk/`.

**DO NOT** load it via `FontProperties(fname=…NotoSansCJK-VF.otf.ttc)` NOR
`fm.fontManager.addfont(…)` — matplotlib's FT2Font cannot read the VF .ttc and raises
`RuntimeError: Can not load face (SFNT font table missing; error code 0x8e)`.

**DO** refresh the font cache and select by family-name list:

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

try:
    fm._load_fontmanager(try_read_cache=False)  # refresh stale cache so the VF font is seen
except Exception:
    pass
plt.rcParams["font.family"] = [
    "Noto Sans CJK JP", "Noto Serif CJK JP", "Noto Sans CJK SC",  # NixOS
    "DejaVu Sans", "sans-serif",                                   # fallback
]
plt.rcParams["axes.unicode_minus"] = False   # avoid tofu on minus signs
```

Last resort if no CJK family resolves at all: switch labels/titles to English rather than shipping tofu.

If Japanese still renders as tofu (□), the cache refresh was skipped — it is required once per process.

## Quality defaults

```python
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
# … plot …
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig("/home/gohan/.hermes/workspace/chart.png", bbox_inches="tight")
```

- Save as PNG into `~/.hermes/workspace/` (unique, descriptive filename)
- Label axes and title in the user's language; add units
- Prefer horizontal bar charts when category names are long Japanese strings

## Delivery

After saving, upload to Slack **in the current thread** — follow skill `slack-image-upload`
(3-step API, `channel_id` + `thread_ts` both required). Never post directly to the channel.
