#!/usr/bin/env python3
"""
Regenerate assets/favicon/* from assets/logo.png.

Run this whenever assets/logo.png changes. Requires Pillow (pip install pillow).

Usage:
    python scripts/make_favicons.py
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "logo.png"
OUT = ROOT / "assets" / "favicon"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    im = Image.open(SRC).convert("RGBA")

    # Trim transparent padding, then re-pad a little so the mark isn't
    # flush to the edge — keeps it legible at 16x16 in a browser tab.
    im = im.crop(im.getbbox())
    w, h = im.size
    side = max(w, h)
    pad = int(side * 0.06)
    square = Image.new("RGBA", (side + pad * 2, side + pad * 2), (0, 0, 0, 0))
    square.paste(im, ((side - w) // 2 + pad, (side - h) // 2 + pad), im)

    named_sizes = {
        16: "favicon-16x16.png",
        32: "favicon-32x32.png",
        48: "favicon-48x48.png",
        96: "favicon-96x96.png",
        180: "apple-touch-icon.png",
        192: "android-chrome-192x192.png",
        512: "android-chrome-512x512.png",
    }
    for size, name in named_sizes.items():
        square.resize((size, size), Image.LANCZOS).save(OUT / name, optimize=True)
        print("wrote", name)

    square.resize((256, 256), Image.LANCZOS).save(
        OUT / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)]
    )
    print("wrote favicon.ico")


if __name__ == "__main__":
    main()
