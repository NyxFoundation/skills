#!/usr/bin/env python3
"""Screenshot each storyboard stage of a demo HTML (for review, slides, or README stills).

Usage:
  python snap.py demo.html                 # snaps stages 0..N into ./snaps/stage-N.png
  python snap.py demo.html --stages 2 4    # only these
  python snap.py demo.html --wait 12       # seconds to let a stage finish animating (default 10)

Stages are triggered with keyboard digits (the engine binds 0-9 to stages, r to replay).
Always look at these before recording — a still shows layout bugs a video hides.

Requires: playwright (`uv run --with playwright python snap.py …` works too).
"""
import argparse, os, sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _browser import launch_chromium

ap = argparse.ArgumentParser()
ap.add_argument("html"); ap.add_argument("--stages", type=int, nargs="*")
ap.add_argument("--wait", type=float, default=10); ap.add_argument("--outdir", default="snaps")
ap.add_argument("--width", type=int, default=1600); ap.add_argument("--height", type=int, default=1000)
a = ap.parse_args()
os.makedirs(a.outdir, exist_ok=True)
html = os.path.abspath(a.html)
with sync_playwright() as p:
    b = launch_chromium(p)
    pg = b.new_page(viewport={"width": a.width, "height": a.height})
    errors = []; pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(f"file://{html}?rec=1"); pg.wait_for_timeout(600)
    n = pg.evaluate("document.querySelectorAll('#steps button[data-step]').length")
    stages = a.stages if a.stages else list(range(n))
    for s in stages:
        pg.keyboard.press(str(s)); pg.wait_for_timeout(int(a.wait * 1000))
        path = os.path.join(a.outdir, f"stage-{s}.png"); pg.screenshot(path=path); print("wrote", path)
    if errors: print("JS errors:", *errors, sep="\n  ")
    b.close()
