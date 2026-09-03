#!/usr/bin/env python3
"""Record a demo HTML to MP4 / GIF, deterministically.

Usage:
  python record.py demo.html                       # -> demo.mp4  (1600x1000, 30s, 25fps)
  python record.py demo.html --seconds 40 --out out.mp4
  python record.py demo.html --gif                 # also writes out.gif (for READMEs)
  python record.py demo.html --width 1920 --height 1200   # stage scales to width; keep 16:10

Requires: playwright + ffmpeg on PATH (`uv run --with playwright python record.py …` works too).
The page is opened with ?rec=1 (hides authoring controls) and simply left to auto-play,
so the recording is reproducible: same HTML in, same video out.
"""
import argparse, glob, os, subprocess, sys, tempfile
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _browser import launch_chromium

ap = argparse.ArgumentParser()
ap.add_argument("html")
ap.add_argument("--out", default=None)
ap.add_argument("--seconds", type=float, default=30, help="must cover the whole story plus ~2s")
ap.add_argument("--width", type=int, default=1600)
ap.add_argument("--height", type=int, default=1000)
ap.add_argument("--gif", action="store_true")
ap.add_argument("--settle", type=float, default=0.8, help="seconds trimmed off the front (font swap / first paint)")
a = ap.parse_args()

html = os.path.abspath(a.html)
out = a.out or os.path.splitext(html)[0] + ".mp4"
tmp = tempfile.mkdtemp(prefix="rec_")

with sync_playwright() as p:
    b = launch_chromium(p)
    ctx = b.new_context(viewport={"width": a.width, "height": a.height},
                        record_video_dir=tmp, record_video_size={"width": a.width, "height": a.height})
    pg = ctx.new_page()
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(f"file://{html}?rec=1")
    pg.wait_for_timeout(int(a.seconds * 1000))
    ctx.close(); b.close()
    if errors:
        print("JS errors during recording:", *errors, sep="\n  ", file=sys.stderr)

webm = max(glob.glob(os.path.join(tmp, "*.webm")), key=os.path.getmtime)
# trim the first `settle` seconds (font swap / first paint) so the video starts clean
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(a.settle), "-i", webm,
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", out], check=True)
print("wrote", out)
if a.gif:
    gif = os.path.splitext(out)[0] + ".gif"
    pal = os.path.join(tmp, "pal.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-vf", "fps=12,scale=1200:-1:flags=lanczos,palettegen", pal], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-i", pal, "-lavfi", "fps=12,scale=1200:-1:flags=lanczos[x];[x][1:v]paletteuse", gif], check=True)
    print("wrote", gif)
