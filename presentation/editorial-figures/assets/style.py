# -*- coding: utf-8 -*-
"""
Editorial figure style for matplotlib.

Self-contained: on import it locates the system Japanese (Noto CJK JP) fonts,
extracts / instances the weight faces it needs into a cache dir, sets up an
editorial palette, and exposes helper drawing functions.

Usage:
    import style as S
    fig, ax = S.new(12.8, 7.0)            # paper-coloured fig+ax, axis off
    S.t(ax, x, y, "見出し", fp="bold", size=14, color=S.INK)
    S.rrect(ax, x, y, w, h, fc=S.CARD, ec=S.HAIR)
    S.title_block(fig, "Headline", "Sub-headline.")
    S.save(fig, "my_figure.png")          # -> cwd (or $EDITORIAL_FIGURES_OUTDIR)

Requires: matplotlib, numpy, fonttools (for first-time font extraction).

Environment notes (NixOS / cross-platform):
- System Noto CJK fonts are discovered via `fc-list`, so nix-store paths work
  (NixOS ships them as variable-font .ttc collections; Debian ships per-weight
  files). No hard-coded /usr/share path is required.
- Extracted faces are cached OUTSIDE the repo, under
  $EDITORIAL_FIGURES_FONTDIR or ~/.cache/editorial-figures/fonts, so the skill
  directory never fills with ~100 MB of generated fonts. First import warms the
  cache (~1 min); later imports are instant.
- If fonttools or the system Noto CJK fonts are unavailable, it falls back to
  whatever Japanese-capable family matplotlib can find (text still renders; the
  exact weights may differ).
"""
import os, subprocess
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge, Rectangle

# --------------------------------------------------------------------- fonts
_HERE = os.path.dirname(os.path.abspath(__file__))

def _font_cache_dir():
    d = os.environ.get("EDITORIAL_FIGURES_FONTDIR")
    if not d:
        base = os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache")
        d = os.path.join(base, "editorial-figures", "fonts")
    os.makedirs(d, exist_ok=True)
    return d

FONTS_DIR = _font_cache_dir()

# cached output face -> (fc-list family, variable-font wght instance)
_FACES = {
    "NotoSansJP-Regular.otf":   ("Noto Sans CJK JP", 400),
    "NotoSansJP-Medium.otf":    ("Noto Sans CJK JP", 500),
    "NotoSansJP-Bold.otf":      ("Noto Sans CJK JP", 700),
    "NotoSansJP-Black.otf":     ("Noto Sans CJK JP", 900),
    "NotoSansJP-Light.otf":     ("Noto Sans CJK JP", 300),
    "NotoSerifJP-Medium.otf":   ("Noto Serif CJK JP", 500),
    "NotoSerifJP-Bold.otf":     ("Noto Serif CJK JP", 700),
    "NotoSerifJP-SemiBold.otf": ("Noto Serif CJK JP", 600),
}

# Unicode blocks kept when subsetting the (huge, 65k-glyph) CJK font down to a
# Japanese working set: Latin+punct, arrows, enclosed/geometric, kana & CJK
# symbols, CJK Ext-A, CJK Unified Ideographs, compat ideographs, fullwidth forms.
_JP_RANGES = [(0x20, 0xFF), (0x2000, 0x206F), (0x2190, 0x21FF), (0x2460, 0x24FF),
              (0x25A0, 0x25FF), (0x3000, 0x30FF), (0x3400, 0x4DBF), (0x4E00, 0x9FFF),
              (0xF900, 0xFAFF), (0xFF00, 0xFFEF)]

def _fc_paths(family):
    """Font files fc-list knows for `family`, .ttc collections first."""
    try:
        out = subprocess.check_output(["fc-list"], stderr=subprocess.DEVNULL).decode("utf-8", "ignore")
    except Exception:
        return []
    paths = []
    for line in out.splitlines():
        p = line.split(":", 1)[0].strip()
        if family in line and p.lower().endswith((".ttc", ".otf", ".ttf")):
            paths.append(p)
    paths.sort(key=lambda p: 0 if p.lower().endswith(".ttc") else 1)
    seen, uniq = set(), []
    for p in paths:
        if p not in seen:
            seen.add(p); uniq.append(p)
    return uniq

def _jp_face_index(path):
    """In a .ttc collection, the index of the '… CJK JP' face (else 0)."""
    try:
        from fontTools.ttLib import TTCollection
        tc = TTCollection(path)
        for i, f in enumerate(tc.fonts):
            for rec in f["name"].names:
                if rec.nameID == 1:
                    try:
                        if rec.toUnicode().strip().endswith("CJK JP"):
                            return i
                    except Exception:
                        pass
        return 0
    except Exception:
        return 0  # not a collection / unreadable

def _finalize_and_save(ft_font, dst):
    """Make a matplotlib-loadable static OTF: CFF2 -> CFF (FreeType needs 'CFF ',
    not the variable 'CFF2'). CJK fonts are CID-keyed, which trips fontTools'
    hhea/vhea width recalc on save (KeyError on a glyph name) — the CFF is valid
    and FreeType loads it, so we suppress that recalc and keep the metrics as-is.
    """
    if "CFF2" in ft_font:
        from fontTools.cffLib.CFF2ToCFF import convertCFF2ToCFF
        convertCFF2ToCFF(ft_font)
        ft_font["hhea"].recalc = lambda t: None
        if "vhea" in ft_font:
            ft_font["vhea"].recalc = lambda t: None
    ft_font.save(dst)

def _hb_build(src_data, face_idx, wght, dst):
    """Fast path: HarfBuzz subset+instance (~0.6s/weight) — JP glyphs, wght pinned."""
    import uharfbuzz as hb
    from io import BytesIO
    from fontTools.ttLib import TTFont
    face = hb.Face(src_data, face_idx)
    inp = hb.SubsetInput()
    us = inp.unicode_set
    for a, b in _JP_RANGES:
        for c in range(a, b + 1):
            us.add(c)
    try:
        inp.pin_axis_location(face, "wght", float(wght))  # instance the variable font
    except Exception:
        pass  # non-variable source: plain subset
    sub = hb.subset(face, inp)
    _finalize_and_save(TTFont(BytesIO(bytes(sub.blob.data))), dst)

def _ft_build(src, face_idx, wght, dst):
    """Slow fallback: fontTools instancer (~70s/weight) if uharfbuzz is missing."""
    from fontTools.ttLib import TTFont
    try:
        font = TTFont(src, fontNumber=face_idx)
    except Exception:
        font = TTFont(src)
    if "fvar" in font:
        from fontTools.varLib import instancer
        font = instancer.instantiateVariableFont(font, {"wght": wght}, inplace=True, optimize=False)
    _finalize_and_save(font, dst)

def _ensure_faces():
    """Warm the font cache: extract/instance each needed weight (idempotent)."""
    missing = {o: v for o, v in _FACES.items() if not os.path.exists(os.path.join(FONTS_DIR, o))}
    if not missing:
        return
    src_cache = {}
    for out, (family, wght) in missing.items():
        if family not in src_cache:
            paths = _fc_paths(family)
            src = paths[0] if paths else None
            data = None
            if src:
                try:
                    with open(src, "rb") as fh:
                        data = fh.read()
                except Exception:
                    data = None
            src_cache[family] = (src, _jp_face_index(src) if src else 0, data)
        src, idx, data = src_cache[family]
        if not src:
            continue
        dst = os.path.join(FONTS_DIR, out)
        try:
            _hb_build(data, idx, wght, dst)
        except Exception:
            try:
                _ft_build(src, idx, wght, dst)
            except Exception:
                pass

try:
    _ensure_faces()
except Exception:
    pass

def _fp(outfile, fallback_weight="normal"):
    p = os.path.join(FONTS_DIR, outfile)
    if os.path.exists(p):
        return FontProperties(fname=p)
    # graceful fallback: ask matplotlib for a Japanese-capable family
    fam = "Noto Serif CJK JP" if "Serif" in outfile else "Noto Sans CJK JP"
    try:
        fp = FontProperties(family=fam, weight=fallback_weight)
        findfont(fp, fallback_to_default=False)
        return fp
    except Exception:
        return FontProperties(family="sans-serif", weight=fallback_weight)

F = {
    "reg":   _fp("NotoSansJP-Regular.otf"),
    "med":   _fp("NotoSansJP-Medium.otf"),
    "bold":  _fp("NotoSansJP-Bold.otf",  fallback_weight="bold"),
    "black": _fp("NotoSansJP-Black.otf", fallback_weight="bold"),
    "light": _fp("NotoSansJP-Light.otf"),
    "smed":  _fp("NotoSerifJP-Medium.otf"),
    "sbold": _fp("NotoSerifJP-Bold.otf", fallback_weight="bold"),
    "ssemi": _fp("NotoSerifJP-SemiBold.otf"),
}

# --------------------------------------------------------------------- palette
PAPER  = "#F7F4ED"   # warm off-white background
CARD   = "#FFFFFF"   # cards / panels (brighter than paper)
INK    = "#1C1B19"   # near-black, warm — primary text & emphasis
SOFT   = "#55524A"   # secondary text
MUTED  = "#938E82"   # tertiary text / source lines
FAINT  = "#BCB6A8"   # faint markers / guides
HAIR   = "#E4DED1"   # hairline borders

SLATE   = "#3C5A74"  # cool/calm  (use for "down", "cheap", neutral bars)
SLATE_L = "#7C93A8"
SLATE_BG= "#EAEFF3"  # light slate fill (chips, tinted zones)
RUST    = "#B0472E"  # warm — "rising", risk, or sparing emphasis
RUST_L  = "#CC7A62"
GOLD    = "#A9842F"
TEAL    = "#3F6F63"
PLUM    = "#6B5B7B"
OLIVE   = "#6E7B4E"

# cohesive, mid-value categorical sequence (desaturated, equal weight)
CAT = [SLATE, TEAL, PLUM, GOLD, OLIVE, SLATE_L, "#A89B86", RUST_L]

plt.rcParams["axes.unicode_minus"] = False

def _out_dir():
    d = os.environ.get("EDITORIAL_FIGURES_OUTDIR")
    if d:
        os.makedirs(d, exist_ok=True); return d
    legacy = "/mnt/user-data/outputs"          # honoured if it happens to exist
    return legacy if os.path.isdir(legacy) else os.getcwd()
OUT = _out_dir()

# --------------------------------------------------------------------- helpers
def lighten(hex_color, amt=0.85):
    """Blend a hex colour toward white by `amt` (0=original, 1=white)."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    f = lambda c: int(round(c + (255 - c) * amt))
    return f"#{f(r):02X}{f(g):02X}{f(b):02X}"

def new(w=12.8, h=7.0, axis_off=True, xlim=None, ylim=None):
    """Paper-coloured fig+ax. By default axis is off with xlim=(0,w),ylim=(0,h)."""
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(PAPER); ax.set_facecolor(PAPER)
    if axis_off:
        ax.set_xlim(xlim or (0, w)); ax.set_ylim(ylim or (0, h)); ax.axis("off")
    return fig, ax

def t(ax, x, y, s, fp="reg", size=12, color=INK, ha="left", va="baseline", **kw):
    return ax.text(x, y, s, fontproperties=F.get(fp, F["reg"]),
                   fontsize=size, color=color, ha=ha, va=va, **kw)

def rrect(ax, x, y, w, h, fc=CARD, ec=HAIR, lw=1.2, rs=0.06, z=1, **kw):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0,rounding_size={rs}",
                       fc=fc, ec=ec, lw=lw, zorder=z, **kw)
    ax.add_patch(p); return p

def arrow(ax, p0, p1, color=SOFT, lw=1.8, style="-|>", ms=12, rad=0.0, z=2, alpha=1.0):
    a = FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, lw=lw,
                        color=color, shrinkA=3, shrinkB=3, zorder=z, alpha=alpha,
                        connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(a); return a

def chip(ax, x, y, w, h, label, fc=SLATE_BG, ec=SLATE_L, tc=SLATE,
         fp="med", size=10.5, lw=1.0, rs=0.18, z=2):
    """Small rounded 'pill' tag with centred label."""
    rrect(ax, x, y, w, h, fc=fc, ec=ec, lw=lw, rs=rs, z=z)
    t(ax, x + w / 2, y + h / 2, label, fp=fp, size=size, color=tc,
      ha="center", va="center", zorder=z + 1)

def title_block(fig, head, sub=None, x=0.065, y=0.955, hs=20, ss=11.5):
    """Editorial title: serif-bold headline + soft sans sub-headline (figure coords)."""
    fig.text(x, y, head, fontproperties=F["sbold"], fontsize=hs, color=INK, va="top")
    if sub:
        fig.text(x, y - 0.058, sub, fontproperties=F["reg"], fontsize=ss, color=SOFT, va="top")

def save(fig, name, out=None, dpi=200, pad=0.28):
    """Save to the outputs dir (tight bbox, paper background). Returns the path."""
    path = os.path.join(out or OUT, name)
    fig.savefig(path, dpi=dpi, facecolor=PAPER, bbox_inches="tight", pad_inches=pad)
    plt.close(fig)
    return path

# convenient re-exports for recipe code
__all__ = ["F","PAPER","CARD","INK","SOFT","MUTED","FAINT","HAIR","SLATE","SLATE_L",
           "SLATE_BG","RUST","RUST_L","GOLD","TEAL","PLUM","OLIVE","CAT","OUT",
           "plt","np","FancyBboxPatch","FancyArrowPatch","Circle","Wedge","Rectangle",
           "lighten","new","t","rrect","arrow","chip","title_block","save"]
