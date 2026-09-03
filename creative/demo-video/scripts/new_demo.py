#!/usr/bin/env python3
"""Assemble a self-contained demo HTML from the shared engine + one surface pack.

Usage:
  python scripts/new_demo.py --list
  python scripts/new_demo.py --surface ide --out speca-demo.html --title "SPECA"
  python scripts/new_demo.py -s terminal -o agent.html -t "nyx agent"

The output is ONE file with the engine, the surface chrome and a starter
storyboard inlined — assemble once, then edit that file. Re-running the
assembler on the same --out overwrites your edits (it refuses unless --force).
"""
import argparse, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SURF = os.path.join(ROOT, "surfaces")
read = lambda *p: open(os.path.join(*p), encoding="utf-8").read()
surfaces = sorted(d for d in os.listdir(SURF) if os.path.isdir(os.path.join(SURF, d)))

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--surface", default="ide", help=f"one of: {', '.join(surfaces)}")
ap.add_argument("-o", "--out", default=None, help="output html (default <surface>-demo.html)")
ap.add_argument("-t", "--title", default=None, help="tool name shown in the chrome/controls")
ap.add_argument("--list", action="store_true", help="list surfaces with their one-line pitch")
ap.add_argument("--force", action="store_true", help="overwrite an existing output file")
a = ap.parse_args()

if a.list:
    for s in surfaces:
        pitch = ""
        notes = os.path.join(SURF, s, "NOTES.md")
        if os.path.exists(notes):
            for line in read(notes).splitlines():
                if line.strip() and not line.startswith("#"):
                    pitch = line.strip(); break
        print(f"{s:10} {pitch}")
    sys.exit(0)

if a.surface not in surfaces:
    sys.exit(f"unknown surface {a.surface!r}; available: {', '.join(surfaces)}")

out = a.out or f"{a.surface}-demo.html"
if os.path.exists(out) and not a.force:
    sys.exit(f"{out} already exists — edit it directly, or pass --force to regenerate from the template")
title = a.title or os.path.splitext(os.path.basename(out))[0]

page = (read(ROOT, "core", "shell.html")
        .replace("{{ENGINE_CSS}}", read(ROOT, "core", "engine.css"))
        .replace("{{SURFACE_CSS}}", read(SURF, a.surface, "surface.css"))
        .replace("{{SURFACE_HTML}}", read(SURF, a.surface, "surface.html"))
        .replace("{{ENGINE_JS}}", read(ROOT, "core", "engine.js"))
        .replace("{{SURFACE_JS}}", read(SURF, a.surface, "surface.js"))
        .replace("{{STORYBOARD_JS}}", read(SURF, a.surface, "storyboard.js"))
        .replace("{{SURFACE}}", a.surface)
        .replace("{{TITLE}}", title))

with open(out, "w", encoding="utf-8") as f:
    f.write(page)
print(f"wrote {out}  ({a.surface} surface)\n"
      f"next: read surfaces/{a.surface}/NOTES.md, fill the chrome + content,\n"
      f"      script the beats in D.define([...]), then review the stills:\n"
      f"  python {os.path.join(ROOT, 'scripts', 'snap.py')} {out}")
