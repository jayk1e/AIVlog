#!/usr/bin/env python3
"""
Shared title/end card renderer for AIVlog. Draws PNGs with Pillow (this machine's
ffmpeg lacks the drawtext filter). Cards land in an episode's clips/<slug>/ so
stitch.sh can wrap them around the clips.

An episode calls make_cards.render(...) with its own text, or you can import and
call it standalone. See make_cards() at the bottom for the callable.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BG = (18, 14, 10)                # warm near-black
FG = (240, 224, 198)            # warm cream
ACCENT = (198, 150, 92)         # muted gold
FONT_PATH = "/System/Library/Fonts/Supplemental/Georgia.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"


def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def _centered(draw, text, f, y, fill, W):
    box = draw.textbbox((0, 0), text, font=f)
    w = box[2] - box[0]
    draw.text(((W - w) / 2, y), text, font=f, fill=fill)
    return box[3] - box[1]


def _rule(draw, y, W, half=180):
    cx = W / 2
    draw.line([(cx - half, y), (cx + half, y)], fill=ACCENT, width=3)


def render(out_dir, *, title, subtitle="", end_line1="", end_line2="", landscape=False):
    """Write card_00_title.png + card_99_end.png into out_dir. Returns their paths."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    W, H = (1920, 1080) if landscape else (1080, 1920)

    # Title card
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    big = _font(FONT_BOLD, 130 if landscape else 150)
    small = _font(FONT_PATH, 56 if landscape else 64)
    cy = H * 0.40
    h1 = _centered(d, title, big, cy, FG, W)
    if subtitle:
        _rule(d, cy + h1 + 60, W)
        _centered(d, subtitle, small, cy + h1 + 100, ACCENT, W)
    title_path = out_dir / "card_00_title.png"
    img.save(title_path)

    # End card
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    mid = _font(FONT_PATH, 72 if landscape else 84)
    cy = H * 0.42
    h1 = _centered(d, end_line1, mid, cy, FG, W)
    h2 = _centered(d, end_line2, mid, cy + h1 + 30, FG, W) if end_line2 else 0
    _rule(d, cy + h1 + 30 + 140, W)
    end_path = out_dir / "card_99_end.png"
    img.save(end_path)

    return title_path, end_path
