#!/usr/bin/env python3
"""LOCKED TikTok animation builder: 15s @ 30fps, 1080x1920, h264.

Sequence (LOCKED):
  t = 0.0 - 0.5s  background + watermark only
  t = 0.5 - 1.0s  TITLE + blue-line top fade in   (0.5s linear)
  t = 1.5 - 2.0s  CONTENT + blue-line bottom fade in
  t = 2.5 - 3.0s  BUTTON (URL pill) fade in
  t = 3.0 - 15.0s full layout holds, background completely static

No Ken Burns zoom. Watermark present from t=0.
Only 4 distinct visual states exist, so we render 4 unique frames and repeat
them plus the 2 x 15 fade frames. Frames are piped raw to ffmpeg.
"""
import subprocess, sys
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from compose_still import compose, layout  # noqa: E402

FPS = 30
DUR = 15.0
W, H = 1080, 1920
FADE = 0.5
T_TITLE, T_CONTENT, T_BUTTON = 0.5, 1.5, 2.5


def _a(t, start):
    if t < start:
        return 0.0
    if t >= start + FADE:
        return 1.0
    return (t - start) / FADE


def build(bg_path, out_path, headline, sub, url="gcseboss.com", logo_path=None):
    bg = Image.open(bg_path).convert("RGB")
    if bg.size != (W, H):
        bg = bg.resize((W, H), Image.LANCZOS)
    L = layout((W, H), headline, sub, url)

    kw = dict(url=url, L=L)
    if logo_path:
        kw["logo_path"] = logo_path

    cache = {}

    def frame(t):
        key = (round(_a(t, T_TITLE), 3), round(_a(t, T_CONTENT), 3),
               round(_a(t, T_BUTTON), 3))
        if key not in cache:
            cache[key] = compose(bg, headline, sub, a_title=key[0],
                                 a_content=key[1], a_button=key[2],
                                 **kw).tobytes()
        return cache[key]

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart",
           "-r", str(FPS), str(out_path)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                         stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    n = int(round(DUR * FPS))
    for i in range(n):
        p.stdin.write(frame(i / FPS))
    p.stdin.close()
    err = p.stderr.read().decode()[-800:]
    if p.wait() != 0:
        raise RuntimeError(err)
    return out_path


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("bg"); ap.add_argument("out")
    ap.add_argument("--headline", required=True)
    ap.add_argument("--sub", required=True)
    ap.add_argument("--url", default="gcseboss.com")
    ap.add_argument("--logo", default=None)
    a = ap.parse_args()
    build(a.bg, a.out, a.headline, a.sub, a.url, a.logo)
    print(f"OUT={a.out}")
