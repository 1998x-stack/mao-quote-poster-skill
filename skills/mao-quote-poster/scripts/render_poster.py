#!/usr/bin/env python3
"""Render exact Chinese quote typography over an image-generation background."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


CANVAS = (1080, 1920)
TEXT_COLOR = (255, 241, 174, 255)
GLOW_COLOR = (255, 190, 55, 170)
SHADOW_COLOR = (65, 8, 8, 145)

FONT_CANDIDATES = [
    # macOS
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
    "/System/Library/Fonts/Supplemental/Kaiti.ttc",
    # Linux
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    # Windows
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/simsun.ttc",
]

ATTRIBUTION_FONT_CANDIDATES = [
    # Prefer a Kai-style face for the small signature.
    "/System/Library/Fonts/Supplemental/Kaiti.ttc",
    "/System/Library/Fonts/STKaiti.ttf",
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc",
    "C:/Windows/Fonts/simkai.ttf",
    "C:/Windows/Fonts/simsun.ttc",
]


def find_font(explicit: str | None = None, attribution: bool = False) -> str:
    if explicit:
        path = Path(explicit).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"Font file not found: {path}")
        return str(path)

    candidates = ATTRIBUTION_FONT_CANDIDATES if attribution else FONT_CANDIDATES
    for candidate in candidates:
        if Path(candidate).is_file():
            return candidate

    raise FileNotFoundError(
        "No supported CJK font found. Install Noto Sans CJK / Noto Serif CJK, "
        "or pass --font /path/to/cjk-font.ttc."
    )


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def is_closing_punctuation(char: str) -> bool:
    return char in "，。！？；：、）》】」』〉〕］｝）…％"


def wrap_by_width(
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    """Wrap text by measured pixel width, preserving explicit newlines."""
    output: list[str] = []
    for paragraph in text.splitlines() or [text]:
        if paragraph == "":
            output.append("")
            continue

        line = ""
        for char in paragraph:
            candidate = line + char
            if line and font.getlength(candidate) > max_width:
                # Avoid placing closing punctuation at the beginning of a line.
                if is_closing_punctuation(char):
                    line += char
                    output.append(line)
                    line = ""
                else:
                    output.append(line)
                    line = char
            else:
                line = candidate
        if line:
            output.append(line)

    return output


def choose_layout(
    quote: str,
    font_path: str,
    max_width: int = 920,
    max_height: int = 850,
) -> tuple[ImageFont.FreeTypeFont, list[str], int, int]:
    for size in range(164, 59, -2):
        font = load_font(font_path, size)
        lines = wrap_by_width(quote, font, max_width)
        line_gap = max(14, int(size * 0.24))
        line_height = int(size * 1.18)
        total_height = len(lines) * line_height + max(0, len(lines) - 1) * line_gap
        widest = max((font.getlength(line) for line in lines), default=0)
        if widest <= max_width and total_height <= max_height:
            return font, lines, line_height, line_gap

    font = load_font(font_path, 60)
    lines = wrap_by_width(quote, font, max_width)
    return font, lines, 72, 14


def draw_centered_text(
    layer: Image.Image,
    lines: Iterable[str],
    font: ImageFont.FreeTypeFont,
    line_height: int,
    line_gap: int,
    center_y: int,
    fill: tuple[int, int, int, int],
    stroke_width: int = 0,
    stroke_fill: tuple[int, int, int, int] = (0, 0, 0, 0),
) -> tuple[int, int, int, int]:
    draw = ImageDraw.Draw(layer)
    lines = list(lines)
    heights = [line_height] * len(lines)
    total_h = sum(heights) + max(0, len(lines) - 1) * line_gap
    y = int(center_y - total_h / 2)
    all_boxes = []

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=stroke_width)
        width = bbox[2] - bbox[0]
        x = int((CANVAS[0] - width) / 2 - bbox[0])
        draw.text(
            (x, y - bbox[1]),
            line,
            font=font,
            fill=fill,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
        )
        all_boxes.append((x + bbox[0], y, x + bbox[2], y + line_height))
        y += line_height + line_gap

    if not all_boxes:
        return (0, 0, 0, 0)
    return (
        min(b[0] for b in all_boxes),
        min(b[1] for b in all_boxes),
        max(b[2] for b in all_boxes),
        max(b[3] for b in all_boxes),
    )


def render(
    background: Path,
    quote: str,
    output: Path,
    attribution: str = "毛泽东",
    font_path: str | None = None,
    attribution_font_path: str | None = None,
    no_attribution: bool = False,
) -> None:
    quote = quote.strip()
    if not quote:
        raise ValueError("The quotation is empty.")

    main_font_path = find_font(font_path)
    if attribution_font_path:
        attr_font_path = find_font(attribution_font_path, attribution=True)
    else:
        try:
            attr_font_path = find_font(attribution=True)
        except FileNotFoundError:
            attr_font_path = main_font_path

    base = Image.open(background).convert("RGB")
    base = ImageOps.fit(base, CANVAS, method=Image.Resampling.LANCZOS)
    base = base.convert("RGBA")

    # A restrained dark-red veil improves text contrast without flattening the texture.
    veil = Image.new("RGBA", CANVAS, (88, 0, 0, 34))
    base = Image.alpha_composite(base, veil)

    font, lines, line_height, line_gap = choose_layout(quote, main_font_path)
    text_layer = Image.new("RGBA", CANVAS, (0, 0, 0, 0))

    # Place the quotation in the upper-middle field, leaving room for attribution.
    quote_box = draw_centered_text(
        text_layer,
        lines,
        font,
        line_height,
        line_gap,
        center_y=720,
        fill=TEXT_COLOR,
        stroke_width=1,
        stroke_fill=(255, 225, 140, 210),
    )

    # Layered amber glow and subtle shadow.
    glow = text_layer.filter(ImageFilter.GaussianBlur(18))
    glow2 = text_layer.filter(ImageFilter.GaussianBlur(7))
    shadow = make_offset_shadow(text_layer, dx=3, dy=7, color=SHADOW_COLOR)

    base = Image.alpha_composite(base, shadow)
    base = Image.alpha_composite(base, glow)
    base = Image.alpha_composite(base, glow2)
    base = Image.alpha_composite(base, text_layer)

    if not no_attribution and attribution:
        attr_size = 62
        attr_font = load_font(attr_font_path, attr_size)
        attr_layer = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
        draw = ImageDraw.Draw(attr_layer)
        bbox = draw.textbbox((0, 0), attribution, font=attr_font)
        attr_w = bbox[2] - bbox[0]
        # Position the signature slightly right of center, below the quote.
        x = min(CANVAS[0] - attr_w - 110, max(580, quote_box[2] - attr_w))
        y = min(quote_box[3] + 58, 1230)
        draw.text((x, y), attribution, font=attr_font, fill=(255, 231, 151, 255))
        attr_glow = attr_layer.filter(ImageFilter.GaussianBlur(5))
        base = Image.alpha_composite(base, attr_glow)
        base = Image.alpha_composite(base, attr_layer)

    output.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(output, quality=95)
    print(f"Saved poster: {output}")


def make_offset_shadow(
    image: Image.Image,
    dx: int,
    dy: int,
    color: tuple[int, int, int, int],
) -> Image.Image:
    """Create a tinted, offset shadow from the alpha channel."""
    alpha = image.getchannel("A")
    shifted = Image.new("L", CANVAS, 0)
    shifted.paste(alpha, (dx, dy))
    shadow = Image.new("RGBA", CANVAS, color)
    shadow.putalpha(shifted.point(lambda p: int(p * color[3] / 255)))
    return shadow


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--background", required=True, help="Generated background image")
    parser.add_argument("--quote", required=True, help="Exact quotation text")
    parser.add_argument("--output", required=True, help="Output poster PNG/JPG path")
    parser.add_argument("--attribution", default="毛泽东", help="Attribution text (default: 毛泽东)")
    parser.add_argument("--font", help="Explicit CJK font path for the main quotation")
    parser.add_argument("--attribution-font", help="Explicit CJK font path for attribution")
    parser.add_argument("--no-attribution", action="store_true", help="Omit attribution")
    args = parser.parse_args()

    try:
        render(
            Path(args.background),
            args.quote,
            Path(args.output),
            attribution=args.attribution,
            font_path=args.font,
            attribution_font_path=args.attribution_font,
            no_attribution=args.no_attribution,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
