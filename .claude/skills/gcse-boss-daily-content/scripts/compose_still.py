#!/usr/bin/env python3
"""LOCKED overlay composer for GCSE Boss social stills.

Implements the visual design spec in gcse-boss/SKILL.md verbatim:
gradient + blue vertical line + headline + sub-quote + URL pill + dog watermark.

compose() takes per-element alphas so build_tiktok_mp4.py can reuse the exact
same geometry for its animated fades. Still images call it with all alphas = 1.0.

Treat this file as LOCKED. Extend with new params; do not change core geometry.
"""
import os
from PIL import Image, ImageDraw, ImageFont

# ---- Palette (project skill) -------------------------------------------------
PRIMARY_BLUE = (46, 168, 224)
WHITE = (255, 255, 255)
SUB_GREY = (232, 232, 232)
# Permanently excluded: purple #9b5de5, pink #d04ba6.

# ---- Geometry constants (LOCKED) ---------------------------------------------
MARGIN_PCT = 0.055
LINE_W_PCT = 0.005
TEXT_GAP_PCT = 0.022
HEAD_PCT = 0.078
SUB_PCT = 0.030
PILL_PCT = 0.028
HEAD_LH = 1.05
SUB_LH = 1.35
GRAD_START = 0.40          # gradient begins 40% from top
GRAD_INTENSITY = 0.82
BOTTOM_CLEARANCE_PCT = 0.115
WM_MARGIN_PCT = 0.03
WM_WIDTH_PCT = 0.085
WM_ALPHA = 0.75
LOGO_DOG_CROP_X = 0.58     # right-of-this fraction of the logo is the dog only

FONT_BOLD_CANDIDATES = [
    "/usr/share/fonts/truetype/inter/Inter-Bold.ttf",
    "/Library/Fonts/Inter-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
FONT_REG_CANDIDATES = [
    "/usr/share/fonts/truetype/inter/Inter-Regular.ttf",
    "/Library/Fonts/Inter-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def _font(cands, size):
    for p in cands:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def _wrap(draw, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def _gradient(size):
    """Soft dark gradient over the bottom 60%, eased t^1.5, peak alpha 0.82."""
    W, H = size
    grad = Image.new("L", (1, H), 0)
    px = grad.load()
    y0 = int(H * GRAD_START)
    span = max(1, H - y0)
    for y in range(y0, H):
        t = (y - y0) / span
        px[0, y] = int(255 * GRAD_INTENSITY * (t ** 1.5))
    mask = grad.resize((W, H), Image.BILINEAR)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.putalpha(mask)
    return layer


def _dog(logo_path, target_w):
    logo = Image.open(logo_path).convert("RGBA")
    LW, LH = logo.size
    right = logo.crop((int(LW * LOGO_DOG_CROP_X), 0, LW, LH))
    bbox = right.getbbox()
    if bbox:
        right = right.crop(bbox)
    w, h = right.size
    new_h = max(1, int(round(target_w * h / w)))
    right = right.resize((target_w, new_h), Image.LANCZOS)
    a = right.getchannel("A").point(lambda v: int(v * WM_ALPHA))
    right.putalpha(a)
    return right


def _alpha_layer(size, alpha):
    """Blank RGBA scratch layer, later flattened at `alpha`."""
    return Image.new("RGBA", size, (0, 0, 0, 0)), alpha


def _paste_at(base, layer, alpha):
    if alpha <= 0:
        return base
    if alpha < 1.0:
        a = layer.getchannel("A").point(lambda v: int(v * alpha))
        layer = layer.copy()
        layer.putalpha(a)
    return Image.alpha_composite(base, layer)


def layout(size, headline, sub, url):
    """Compute all geometry once. Returns a dict consumed by compose()."""
    W, H = size
    S = min(W, H)
    margin = int(S * MARGIN_PCT)
    line_w = max(2, int(S * LINE_W_PCT))
    text_x = margin + line_w + int(S * TEXT_GAP_PCT)
    max_text_w = W - text_x - margin

    f_head = _font(FONT_BOLD_CANDIDATES, int(S * HEAD_PCT))
    f_sub = _font(FONT_REG_CANDIDATES, int(S * SUB_PCT))
    f_pill = _font(FONT_BOLD_CANDIDATES, int(S * PILL_PCT))

    scratch = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    head_lines = _wrap(scratch, headline, f_head, max_text_w)
    sub_lines = _wrap(scratch, sub, f_sub, max_text_w)

    head_lh = int(f_head.size * HEAD_LH)
    sub_lh = int(f_sub.size * SUB_LH)
    head_h = head_lh * len(head_lines)
    sub_h = sub_lh * len(sub_lines)
    gap = int(S * 0.030)

    # URL pill sits at the bottom, everything else stacks upward from it.
    pill_pad_x = int(S * 0.026)
    pill_pad_y = int(S * 0.016)
    pill_tw = int(scratch.textlength(url, font=f_pill))
    pill_w = pill_tw + pill_pad_x * 2
    pill_h = f_pill.size + pill_pad_y * 2
    pill_bottom = H - int(S * BOTTOM_CLEARANCE_PCT)
    pill_top = pill_bottom - pill_h

    sub_bottom = pill_top - int(S * 0.045)
    sub_top = sub_bottom - sub_h
    head_bottom = sub_top - gap
    head_top = head_bottom - head_h

    # Blue line: from 1.2% above the headline to 0.5% below the sub.
    # Split at the headline/sub boundary so the MP4 can fade the two halves
    # with their matching text elements.
    line_top = head_top - int(S * 0.012)
    line_mid = head_bottom
    line_bot = sub_bottom + int(S * 0.005)

    return dict(
        W=W, H=H, S=S, margin=margin, line_w=line_w, text_x=text_x,
        f_head=f_head, f_sub=f_sub, f_pill=f_pill,
        head_lines=head_lines, sub_lines=sub_lines,
        head_lh=head_lh, sub_lh=sub_lh,
        head_top=head_top, sub_top=sub_top,
        pill_top=pill_top, pill_w=pill_w, pill_h=pill_h,
        pill_pad_x=pill_pad_x, pill_pad_y=pill_pad_y, url=url,
        line_top=line_top, line_mid=line_mid, line_bot=line_bot,
    )


def compose(bg, headline, sub, url="gcseboss.com",
            logo_path="/sessions/serene-funny-hawking/mnt/GCSEBoss/images/gcse-boss-transparent-bg.png",
            a_title=1.0, a_content=1.0, a_button=1.0, L=None):
    """Apply the locked overlay to `bg` (a PIL Image already at target size)."""
    base = bg.convert("RGBA")
    L = L or layout(base.size, headline, sub, url)
    W, H = L["W"], L["H"]

    base = Image.alpha_composite(base, _gradient((W, H)))

    # --- TITLE layer: headline + top half of the blue line ---
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rectangle([L["margin"], L["line_top"],
                 L["margin"] + L["line_w"], L["line_mid"]],
                fill=PRIMARY_BLUE + (255,))
    y = L["head_top"]
    for ln in L["head_lines"]:
        d.text((L["text_x"] + 2, y + 2), ln, font=L["f_head"], fill=(0, 0, 0, 180))
        d.text((L["text_x"], y), ln, font=L["f_head"], fill=WHITE + (255,))
        y += L["head_lh"]
    base = _paste_at(base, lay, a_title)

    # --- CONTENT layer: sub-quote + bottom half of the blue line ---
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rectangle([L["margin"], L["line_mid"],
                 L["margin"] + L["line_w"], L["line_bot"]],
                fill=PRIMARY_BLUE + (255,))
    y = L["sub_top"]
    for ln in L["sub_lines"]:
        d.text((L["text_x"] + 1, y + 1), ln, font=L["f_sub"], fill=(0, 0, 0, 160))
        d.text((L["text_x"], y), ln, font=L["f_sub"], fill=SUB_GREY + (255,))
        y += L["sub_lh"]
    base = _paste_at(base, lay, a_content)

    # --- BUTTON layer: URL pill ---
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle(
        [L["text_x"], L["pill_top"],
         L["text_x"] + L["pill_w"], L["pill_top"] + L["pill_h"]],
        radius=L["pill_h"] // 2, fill=PRIMARY_BLUE + (255,))
    d.text((L["text_x"] + L["pill_pad_x"], L["pill_top"] + L["pill_pad_y"]),
           L["url"], font=L["f_pill"], fill=WHITE + (255,))
    base = _paste_at(base, lay, a_button)

    # --- Watermark: dog only, always present, never animated ---
    if logo_path and os.path.exists(logo_path):
        dog = _dog(logo_path, int(W * WM_WIDTH_PCT))
        wm = int(L["S"] * WM_MARGIN_PCT)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lay.paste(dog, (W - wm - dog.size[0], H - wm - dog.size[1]), dog)
        base = Image.alpha_composite(base, lay)

    return base.convert("RGB")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--headline", required=True)
    ap.add_argument("--sub", required=True)
    ap.add_argument("--url", default="gcseboss.com")
    a = ap.parse_args()
    compose(Image.open(a.src), a.headline, a.sub, a.url).save(a.dst, quality=95)
    print(f"OUT={a.dst}")
