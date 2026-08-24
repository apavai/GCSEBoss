#!/usr/bin/env python3
"""Defensive layer 1: paint a blurred patch over the bottom-right AI watermark.

The primary defence is smart_crop.py's bottom_trim_pct (default 0.18).
This is belt-and-braces for aspect ratios that keep more of the bottom.
"""
from PIL import Image, ImageFilter


def strip_watermark(img, patch_w=0.30, patch_h=0.085, blur=22):
    """Return a copy of `img` with the bottom-right watermark zone painted over
    with a blurred, upscaled sample taken from just above the zone."""
    img = img.convert("RGB").copy()
    W, H = img.size
    pw, ph = int(W * patch_w), int(H * patch_h)
    x0, y0 = W - pw, H - ph

    # Sample the band immediately ABOVE the watermark zone, same width.
    src_y1 = max(0, y0)
    src_y0 = max(0, src_y1 - ph)
    sample = img.crop((x0, src_y0, W, src_y1))
    sample = sample.resize((pw, ph), Image.LANCZOS).filter(
        ImageFilter.GaussianBlur(blur))
    img.paste(sample, (x0, y0))
    return img


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    a = ap.parse_args()
    strip_watermark(Image.open(a.src)).save(a.dst)
    print(f"OUT={a.dst}")
