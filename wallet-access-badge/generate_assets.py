"""Generate Disney MagicMobile–style placeholder assets for Apple Wallet."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


STRIP_SIZES = [(375, 144), (750, 288), (1125, 432)]
THUMB_SIZES = [(90, 90), (180, 180), (270, 270)]


def _font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    path = bold_path if bold else regular
    if Path(path).exists():
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _save_resolutions(base: Image.Image, stem: str, sizes: list[tuple[int, int]], out_dir: Path) -> None:
    for idx, (w, h) in enumerate(sizes):
        scaled = base.resize((w, h), Image.Resampling.LANCZOS)
        suffix = "" if idx == 0 else f"@{idx + 1}x"
        scaled.save(out_dir / f"{stem}{suffix}.png", "PNG")


def _draw_star(draw: ImageDraw.ImageDraw, x: int, y: int, size: int, color: tuple[int, ...]) -> None:
    points = []
    for i in range(8):
        angle = math.pi / 4 * i - math.pi / 2
        r = size if i % 2 == 0 else size * 0.35
        points.append((x + r * math.cos(angle), y + r * math.sin(angle)))
    draw.polygon(points, fill=color)


def _draw_falcon(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: float) -> None:
    s = scale
    hull = [
        (cx - 70 * s, cy + 8 * s),
        (cx - 18 * s, cy - 34 * s),
        (cx + 52 * s, cy - 8 * s),
        (cx + 78 * s, cy + 2 * s),
        (cx + 52 * s, cy + 12 * s),
        (cx - 18 * s, cy + 34 * s),
    ]
    draw.polygon(hull, fill=(235, 238, 245))
    draw.polygon(
        [
            (cx - 8 * s, cy - 18 * s),
            (cx + 24 * s, cy - 6 * s),
            (cx + 24 * s, cy + 6 * s),
            (cx - 8 * s, cy + 18 * s),
        ],
        fill=(210, 214, 222),
    )
    draw.ellipse(
        (cx - 4 * s, cy - 4 * s, cx + 20 * s, cy + 20 * s),
        fill=(120, 128, 140),
    )
    draw.rectangle(
        (cx - 42 * s, cy - 2 * s, cx - 28 * s, cy + 10 * s),
        fill=(190, 48, 48),
    )
    draw.rectangle(
        (cx + 8 * s, cy - 2 * s, cx + 22 * s, cy + 10 * s),
        fill=(190, 48, 48),
    )
    draw.polygon(
        [
            (cx - 92 * s, cy + 4 * s),
            (cx - 74 * s, cy - 2 * s),
            (cx - 74 * s, cy + 10 * s),
        ],
        fill=(170, 178, 190),
    )
    draw.polygon(
        [
            (cx + 84 * s, cy + 2 * s),
            (cx + 110 * s, cy - 4 * s),
            (cx + 110 * s, cy + 8 * s),
        ],
        fill=(170, 178, 190),
    )
    draw.ellipse(
        (cx + 78 * s, cy - 6 * s, cx + 118 * s, cy + 10 * s),
        fill=(90, 170, 230, 120),
    )


def _draw_tie(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float) -> None:
    s = scale
    draw.polygon(
        [(x, y - 16 * s), (x - 18 * s, y + 10 * s), (x + 18 * s, y + 10 * s)],
        fill=(28, 42, 82),
    )
    draw.ellipse((x - 7 * s, y + 8 * s, x + 7 * s, y + 22 * s), fill=(40, 56, 96))


def generate_strip(out_dir: Path, guest_name: str) -> None:
    """Full-width pass front — flat space battle similar to MagicMobile."""
    w, h = STRIP_SIZES[0]
    footer_h = int(h * 0.18)
    art_h = h - footer_h

    img = Image.new("RGB", (w, h), (12, 20, 48))
    draw = ImageDraw.Draw(img)

    for y in range(art_h):
        t = y / max(art_h - 1, 1)
        r = int(12 + (28 - 12) * (1 - t) + 20 * (0.5 - abs(t - 0.45)))
        g = int(20 + (48 - 20) * (1 - t) + 30 * (0.5 - abs(t - 0.45)))
        b = int(48 + (92 - 48) * (1 - t) + 40 * (0.5 - abs(t - 0.45)))
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    stars = [(34, 18), (88, 42), (142, 22), (210, 36), (290, 14), (330, 48), (52, 62), (248, 58)]
    for sx, sy in stars:
        _draw_star(draw, sx, sy, 3, (255, 255, 255))

    _draw_tie(draw, 72, 44, 1.0)
    _draw_tie(draw, 38, 28, 0.7)
    draw.line([(30, 70), (10, 108)], fill=(72, 220, 96), width=3)
    draw.line([(42, 66), (24, 104)], fill=(72, 220, 96), width=3)

    _draw_falcon(draw, 220, 58, 1.0)

    draw.rectangle((0, art_h, w, h), fill=(14, 22, 52))
    draw.text((14, art_h + 8), guest_name, fill=(255, 255, 255), font=_font(15))

    _save_resolutions(img, "strip", STRIP_SIZES, out_dir)


def generate_thumbnail(out_dir: Path, guest_name: str, subtitle: str = "Access Badge") -> None:
    """Small pass preview for the info (ⓘ) screen header."""
    w, h = THUMB_SIZES[0]
    img = Image.new("RGB", (w, h), (14, 22, 52))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle((4, 4, w - 4, 58), radius=6, fill=(18, 30, 68))
    _draw_star(draw, 16, 16, 2, (255, 255, 255))
    _draw_star(draw, 70, 22, 2, (255, 255, 255))
    _draw_tie(draw, 18, 24, 0.45)
    _draw_falcon(draw, 58, 30, 0.42)
    draw.line([(8, 48), (2, 56)], fill=(72, 220, 96), width=1)

    draw.text((8, 62), guest_name[:14], fill=(255, 255, 255), font=_font(8))
    draw.text((8, 74), subtitle[:16], fill=(170, 174, 182), font=_font(7, bold=False))

    _save_resolutions(img, "thumbnail", THUMB_SIZES, out_dir)


def generate_icon(out_dir: Path) -> None:
    base = Image.new("RGBA", (29, 29), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle((1, 1, 28, 28), radius=6, fill=(14, 22, 52, 255))
    _draw_star(draw, 14, 14, 5, (255, 255, 255, 255))
    _save_resolutions(base, "icon", [(29, 29), (58, 58), (87, 87)], out_dir)


def generate_logo(out_dir: Path) -> None:
    """Minimal logo — keeps the pass front clean."""
    base = Image.new("RGBA", (160, 50), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    draw.text((0, 16), "WDW", fill=(255, 255, 255, 220), font=_font(14))
    _save_resolutions(base, "logo", [(160, 50), (320, 100), (480, 150)], out_dir)


def generate_all(out_dir: Path, guest_name: str, logo_text: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    generate_icon(out_dir)
    generate_logo(out_dir)
    generate_strip(out_dir, guest_name)
    generate_thumbnail(out_dir, guest_name)
