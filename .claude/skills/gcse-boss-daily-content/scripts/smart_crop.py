#!/usr/bin/env python3
"""Aspect-ratio crop with focal-point control.

bottom_trim_pct is the PRIMARY watermark defence. Default 0.18. Do not lower it:
on 9:16 and 2:3 targets the strip_watermark patch becomes visible if you do.
"""
from PIL import Image


def smart_crop(img, target_w, target_h, fx=0.5, fy=0.5, bottom_trim_pct=0.18):
    img = img.convert("RGB")
    W, H = img.size

    # 1. Discard the bottom band (watermark zone) BEFORE the aspect crop.
    keep_h = int(H * (1.0 - bottom_trim_pct))
    img = img.crop((0, 0, W, keep_h))
    W, H = img.size

    # 2. Largest rect of target aspect that fits.
    target_ar = target_w / target_h
    src_ar = W / H
    if src_ar > target_ar:
        ch = H
        cw = int(round(H * target_ar))
    else:
        cw = W
        ch = int(round(W / target_ar))

    # 3. Position by focal point, clamped to bounds.
    cx = int(round(fx * W)) - cw // 2
    cy = int(round(fy * H)) - ch // 2
    cx = max(0, min(cx, W - cw))
    cy = max(0, min(cy, H - ch))

    return img.crop((cx, cy, cx + cw, cy + ch)).resize(
        (target_w, target_h), Image.LANCZOS)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--w", type=int, required=True)
    ap.add_argument("--h", type=int, required=True)
    ap.add_argument("--fx", type=float, default=0.5)
    ap.add_argument("--fy", type=float, default=0.5)
    ap.add_argument("--bottom-trim", type=float, default=0.18)
    a = ap.parse_args()
    smart_crop(Image.open(a.src), a.w, a.h, a.fx, a.fy, a.bottom_trim).save(a.dst)
    print(f"OUT={a.dst}")
