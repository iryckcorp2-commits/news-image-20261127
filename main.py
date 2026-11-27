#!/usr/bin/env python3
"""The World Today: a one-page newspaper front page for Friday 27 November 2026.

Renders six Reuters-based stories as a printable-style broadsheet image
(1024x1024 PNG) using only the Python standard library plus Pillow.
Deterministic: same input always produces the same pixels.

Stories (lead first):
  1. Mines strike tankers near the Strait of Hormuz
  2. Houthi strikes hit Saudi Arabia
  3. Russia hits grain ships near Odesa
  4. Asian markets bounce while Nvidia slides
  5. Trump demands a probe of GDP data
  6. Guinea-Bissau delays its elections
"""

import os

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024
MARGIN = 36
GUTTER = 18

PAPER = (250, 246, 236)
INK = (18, 18, 18)
RULE = (18, 18, 18)
MUTED = (90, 86, 78)
CARD = (255, 253, 247)
ACCENT = (150, 28, 24)
LEAD_BG = (24, 32, 54)
LEAD_INK = (250, 246, 236)
LEAD_MUTED = (196, 200, 214)
GOLD = (232, 176, 92)

FONT_DIRS = (
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/TTF",
    "/usr/share/fonts",
)


def find_font(bold=False, serif=False):
    """Return the path of a usable TTF font, preferring DejaVu."""
    names = []
    if serif:
        names += ["DejaVuSerif-Bold.ttf", "DejaVuSerif.ttf"]
    if bold:
        names += ["DejaVuSans-Bold.ttf", "DejaVuSans.ttf"]
    else:
        names += ["DejaVuSans.ttf", "DejaVuSans-Bold.ttf"]
    names += ["LiberationSans-Regular.ttf", "LiberationSerif-Regular.ttf"]
    for directory in FONT_DIRS:
        for name in names:
            path = os.path.join(directory, name)
            if os.path.isfile(path):
                return path
    return None


def load(size, bold=False, serif=False):
    path = find_font(bold=bold, serif=serif)
    if path is None:
        return ImageFont.load_default()
    return ImageFont.truetype(path, size)


F_TITLE = load(84, bold=True, serif=True)
F_DATE = load(21, bold=True)
F_KICKER = load(19, bold=True)
F_HEAD_SMALL = load(24, bold=True)
F_LEAD_HEAD = load(40, bold=True)
F_BODY = load(19)
F_LEAD_BODY = load(22)
F_FOOT = load(17)

STORIES = [
    {
        "kicker": "STRAIT OF HORMUZ",
        "headline": "Mines strike tankers near Hormuz as Gulf shipping reels",
        "body": (
            "Two tankers exploded after hitting mines near Oman's Khasab, "
            "Iran's Revolutionary Guard said, one a supertanker carrying "
            "more than two million barrels. UKMTO reported an outbound "
            "tanker hit by a projectile 18 nautical miles east of Khasab, "
            "and another explosion 50 nautical miles west of Dubai."
        ),
        "lead": True,
    },
    {
        "kicker": "SAUDI ARABIA",
        "headline": "Houthi strikes hit Saudi refinery and Riyadh tower",
        "body": (
            "The Houthis claimed strikes on the Ras Tanura refinery and "
            "Riyadh's financial district. A drone hit the tallest tower."
        ),
    },
    {
        "kicker": "UKRAINE WAR",
        "headline": "Russia hits two grain ships near Odesa",
        "body": (
            "Russian strikes hit two grain ships near Odesa, putting more "
            "than 100,000 tons of grain at risk on a vital export route."
        ),
    },
    {
        "kicker": "MARKETS",
        "headline": "Asia bounces as Nvidia slides from its peak",
        "body": (
            "The Nikkei rose 1.6% and the Kospi 1.9%, while Nvidia fell "
            "3.9%, now 2.3 trillion dollars below its October peak."
        ),
    },
    {
        "kicker": "UNITED STATES",
        "headline": "Trump demands probe of GDP data",
        "body": (
            "President Trump demanded an investigation of GDP figures, "
            "calling the numbers fake ahead of the midterm elections."
        ),
    },
    {
        "kicker": "WEST AFRICA",
        "headline": "Guinea-Bissau delays elections by two years",
        "body": (
            "Guinea-Bissau pushed its elections back by about two years "
            "to November 2028, a year after the coup."
        ),
    },
]


def wrap(draw, text, font, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_centered(draw, y, text, font, fill, width=WIDTH):
    w = draw.textlength(text, font=font)
    draw.text(((width - w) / 2, y), text, font=font, fill=fill)
    return y + font.size + 4


def draw_masthead(draw):
    draw.rectangle([0, 0, WIDTH, 128], fill=INK)
    draw_centered(draw, 14, "THE WORLD TODAY", F_TITLE, PAPER)
    draw_centered(draw, 100, "FRIDAY, 27 NOVEMBER 2026  |  SIX STORIES FROM AROUND THE GLOBE",
                  F_DATE, (200, 196, 186))
    draw.line([MARGIN, 140, WIDTH - MARGIN, 140], fill=RULE, width=3)
    draw.line([MARGIN, 146, WIDTH - MARGIN, 146], fill=RULE, width=1)


def draw_lead(draw, story, box):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=10, fill=LEAD_BG)
    pad = 26
    inner = x1 - x0 - 2 * pad
    y = y0 + 20
    draw.text((x0 + pad, y), story["kicker"], font=F_KICKER, fill=GOLD)
    y += 30
    for line in wrap(draw, story["headline"], F_LEAD_HEAD, inner):
        draw.text((x0 + pad, y), line, font=F_LEAD_HEAD, fill=LEAD_INK)
        y += 48
    y += 6
    for line in wrap(draw, story["body"], F_LEAD_BODY, inner):
        draw.text((x0 + pad, y), line, font=F_LEAD_BODY, fill=LEAD_MUTED)
        y += 29
    return y


def draw_card(draw, story, box):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=10, fill=CARD, outline=RULE, width=2)
    pad = 18
    inner = x1 - x0 - 2 * pad
    y = y0 + 12
    draw.text((x0 + pad, y), story["kicker"], font=F_KICKER, fill=ACCENT)
    y += 24
    for line in wrap(draw, story["headline"], F_HEAD_SMALL, inner):
        draw.text((x0 + pad, y), line, font=F_HEAD_SMALL, fill=INK)
        y += 28
    y += 2
    for line in wrap(draw, story["body"], F_BODY, inner):
        draw.text((x0 + pad, y), line, font=F_BODY, fill=MUTED)
        y += 24


def draw_footer(draw):
    y = HEIGHT - 30
    draw.line([MARGIN, y - 8, WIDTH - MARGIN, y - 8], fill=RULE, width=1)
    draw_centered(draw, y, "THE WORLD TODAY  |  FRIDAY, 27 NOVEMBER 2026  |  SIX STORIES, ONE PAGE",
                  F_FOOT, MUTED)


def render():
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)

    draw_lead(draw, STORIES[0], (MARGIN, 158, WIDTH - MARGIN, 462))

    rest = STORIES[1:]
    grid_top = 478
    grid_bottom = 838
    row_h = (grid_bottom - grid_top - GUTTER) // 2
    col_w = (WIDTH - 2 * MARGIN - GUTTER) // 2
    positions = []
    for row in range(2):
        for col in range(2):
            x0 = MARGIN + col * (col_w + GUTTER)
            y0 = grid_top + row * (row_h + GUTTER)
            positions.append((x0, y0, x0 + col_w, y0 + row_h))
    for story, box in zip(rest[:4], positions):
        draw_card(draw, story, box)

    draw_card(draw, rest[4], (MARGIN, 854, WIDTH - MARGIN, 974))
    draw_footer(draw)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img = render()
    img.save(path, format="PNG")
    print("wrote", path, img.size)


if __name__ == "__main__":
    main()
