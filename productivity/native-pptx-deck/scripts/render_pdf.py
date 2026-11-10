#!/usr/bin/env python3
# /// script
# dependencies = ["pymupdf", "pillow"]
# ///
"""Render a PDF to page PNGs and a numbered contact sheet without ImageMagick."""
import argparse
import re
import tempfile
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw


def positive_int(value):
    value = int(value)
    if value < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("outdir", type=Path)
    parser.add_argument("--dpi", type=positive_int, default=110)
    parser.add_argument("--cols", type=positive_int, default=3)
    parser.add_argument("--thumb-width", type=positive_int, default=460)
    args = parser.parse_args()
    dest = args.outdir.resolve()
    dest.mkdir(parents=True, exist_ok=True)
    # Complete rendering before replacing earlier previews. Preserve unrelated files.
    with pymupdf.open(args.pdf) as doc, tempfile.TemporaryDirectory(prefix=".pptx-png-", dir=dest.parent) as tmp:
        if len(doc) == 0:
            parser.error("the PDF has no pages")
        stage = Path(tmp)
        thumbs = []
        max_height = 1
        for i, page in enumerate(doc):
            target = stage / f"p-{i:02d}.png"
            page.get_pixmap(dpi=args.dpi, alpha=False).save(target)
            with Image.open(target) as im:
                height = max(1, round(im.height * args.thumb_width / im.width))
                thumb = im.resize((args.thumb_width, height), Image.Resampling.LANCZOS)
            thumbs.append(thumb)
            max_height = max(max_height, height)
        gap, label_height = 10, 24
        cell_w = args.thumb_width + gap
        cell_h = max_height + label_height + gap
        cols = min(args.cols, len(doc))
        rows = (len(doc) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cell_w + gap, rows * cell_h + gap), "#dddddd")
        draw = ImageDraw.Draw(sheet)
        for i, thumb in enumerate(thumbs):
            x = gap + (i % cols) * cell_w
            y = gap + (i // cols) * cell_h
            draw.text((x, y + 3), f"p{i + 1}", fill="black")
            sheet.paste(thumb, (x, y + label_height))
            thumb.close()
        sheet.save(stage / "contact.png")
        for old in dest.iterdir():
            if old.is_file() and (re.fullmatch(r"p-\d+\.png", old.name) or old.name == "contact.png"):
                old.unlink()
        for generated in stage.iterdir():
            generated.replace(dest / generated.name)
        print(f"{len(doc)} pages + contact.png -> {dest}")


if __name__ == "__main__":
    main()
