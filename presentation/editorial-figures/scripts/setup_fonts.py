#!/usr/bin/env python3
"""
setup_fonts.py — warm & verify the Japanese (Noto CJK JP) font cache used by the
editorial figure style, and report what was found.

Normally you do NOT need to run this: importing `style.py` performs the same
extraction automatically on first use. Run this only to pre-warm fonts or to
troubleshoot Japanese rendering ("tofu"/□ boxes).

    uv run --with matplotlib --with numpy --with uharfbuzz --with fonttools \
        python scripts/setup_fonts.py

How it works (see assets/style.py for the authoritative implementation):
  1. `fc-list` locates the system Noto CJK fonts — works on NixOS (nix-store
     paths) and standard Linux/macOS alike. NixOS ships them as variable-font
     .ttc collections.
  2. HarfBuzz (uharfbuzz) subsets each weight to a Japanese glyph set and
     instances the `wght` axis (~0.6s/weight) — fast.
  3. fontTools converts the resulting variable CFF2 to a static CFF so
     matplotlib/FreeType can load it, and writes the face to the cache dir
     ($EDITORIAL_FIGURES_FONTDIR, else ~/.cache/editorial-figures/fonts).
First run warms all 8 weights in ~2-3 min; later runs are instant.

If uharfbuzz is missing it falls back to the (slow) fontTools instancer. If the
system Noto CJK fonts are missing entirely, matplotlib falls back to any
Japanese-capable family it can find (weights may differ).
"""
import os, sys, subprocess

def find_cjk():
    """Report the Noto CJK font files fc-list knows about."""
    try:
        out = subprocess.check_output(["fc-list"], stderr=subprocess.DEVNULL).decode("utf-8", "ignore")
    except Exception as e:
        print(f"⚠ could not run fc-list: {e}")
        return []
    hits = sorted({ln.split(":", 1)[0] for ln in out.splitlines()
                   if "Noto Sans CJK JP" in ln or "Noto Serif CJK JP" in ln})
    return hits

def main():
    print("== system Noto CJK JP files (fc-list) ==")
    hits = find_cjk()
    for h in hits:
        print("  •", h)
    if not hits:
        print("  (none found — Japanese will fall back to another CJK family if any)")

    # import the style module (sibling assets/style.py); this warms the cache
    here = os.path.dirname(os.path.abspath(__file__))
    assets = os.path.normpath(os.path.join(here, "..", "assets"))
    sys.path.insert(0, assets)
    print("\n== warming cache (import style) ==")
    try:
        import style as S
    except Exception as e:
        print(f"⚠ failed to import style.py from {assets}: {e}")
        return 1
    print("  cache dir:", S.FONTS_DIR)

    # verify each cached face actually loads in matplotlib/FreeType
    print("\n== verify faces load in matplotlib ==")
    ok = 0
    try:
        import matplotlib.ft2font as ft
    except Exception as e:
        print(f"⚠ matplotlib unavailable: {e}")
        ft = None
    for name in S._FACES:
        p = os.path.join(S.FONTS_DIR, name)
        if not os.path.exists(p):
            print(f"  ⚠ missing  {name}")
            continue
        if ft is None:
            print(f"  · present  {name}"); ok += 1; continue
        try:
            face = ft.FT2Font(p)
            # sanity: a common kanji resolves to a non-zero glyph index
            has_kanji = face.get_char_index(0x691C) != 0  # 検
            flag = "OK " if has_kanji else "no-JP?"
            print(f"  ✓ {flag} {name}  ({face.family_name})"); ok += 1
        except Exception as e:
            print(f"  ⚠ load-fail {name}: {e}")
    print(f"\n{ok}/{len(S._FACES)} faces available in {S.FONTS_DIR}")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
