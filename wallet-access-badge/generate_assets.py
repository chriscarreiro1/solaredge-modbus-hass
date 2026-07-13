"""Generate placeholder PNG assets for an Apple Wallet generic pass."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _save_resolutions(base: Image.Image, stem: str, sizes: list[tuple[int, int]], out_dir: Path) -> None:
    for idx, (w, h) in enumerate(sizes):
        scaled = base.resize((w, h), Image.Resampling.LANCZOS)
        suffix = "" if idx == 0 else f"@{idx + 1}x"
        scaled.save(out_dir / f"{stem}{suffix}.png", "PNG")


def generate_icon(out_dir: Path, accent: tuple[int, int, int] = (0, 122, 255)) -> None:
    """29pt icon — notifications and info screen."""
    base = Image.new("RGBA", (29, 29), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle((2, 2, 27, 27), radius=6, fill=accent)
    draw.text((8, 6), "★", fill=(255, 255, 255, 255), font=_font(14))
    _save_resolutions(base, "icon", [(29, 29), (58, 58), (87, 87)], out_dir)


def generate_logo(out_dir: Path, text: str = "MagicMobile") -> None:
    """Logo shown top-left on pass front."""
    base = Image.new("RGBA", (160, 50), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    draw.text((0, 12), text[:18], fill=(255, 255, 255, 255), font=_font(16))
    _save_resolutions(base, "logo", [(160, 50), (320, 100), (480, 150)], out_dir)


def generate_thumbnail(
    out_dir: Path,
    guest_name: str,
    subtitle: str = "Access Badge",
) -> None:
    """Square preview image on pass front and info screen header."""
    base = Image.new("RGBA", (90, 90), (20, 20, 22, 255))
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle((4, 4, 86, 86), radius=8, fill=(35, 35, 38, 255))
    draw.rounded_rectangle((8, 8, 82, 52), radius=4, fill=(0, 80, 160, 255))
    draw.text((10, 56), guest_name[:12], fill=(255, 255, 255, 255), font=_font(9))
    draw.text((10, 68), subtitle[:14], fill=(174, 174, 178, 255), font=_font(7))
    _save_resolutions(base, "thumbnail", [(90, 90), (180, 180), (270, 270)], out_dir)


def generate_all(out_dir: Path, guest_name: str, logo_text: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    generate_icon(out_dir)
    short_logo = logo_text.split()[-2] if " " in logo_text else logo_text[:12]
    generate_logo(out_dir, short_logo)
    generate_thumbnail(out_dir, guest_name)
