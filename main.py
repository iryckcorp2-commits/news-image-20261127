#!/usr/bin/env python3
"""The World Today - news-image bounty entry for 27 November 2026.

Renders one 1024x1024 PNG newspaper front page, entirely in code:
no photos, no network, no randomness, no clock. Deterministic output.
Python 3.13 standard library only. Rebuilt in a fresh post-opening
session so the entry can be bundled under the competition rules.

Six stories for Friday 27 November 2026: Hormuz mine strikes, Houthi
strikes on Saudi energy assets and Riyadh, Russian strikes on grain ships
near Odesa, Asia markets bouncing as Nvidia slides, Trump demanding a GDP
data probe, and Guinea-Bissau delaying its elections.
"""

import os
import struct
import zlib

# ---------------------------------------------------------------- font ----
# Hand-built 5x7 bitmap glyphs, composed in this session. Each glyph is
# seven rows of five cells; '#' is ink, '.' is blank.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01111", "10000", "10000", "10111", "10001", "10001", "01110"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "11001", "10101", "10011", "10011", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10011", "10101", "11001", "10001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    '3': ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00010", "00100", "00100", "00100"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "00000", "01100"),
    ',': ("00000", "00000", "00000", "00000", "00000", "01100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "01100", "01000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '/': ("00001", "00001", "00010", "00100", "01000", "10000", "10000"),
    '(': ("00011", "00100", "01000", "01000", "01000", "00100", "00011"),
    ')': ("11000", "00100", "00010", "00010", "00010", "00100", "11000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '&': ("01100", "10010", "10010", "01000", "10101", "10010", "01101"),
    '+': ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    '=': ("00000", "00000", "01110", "00000", "01110", "00000", "00000"),
    '*': ("00000", "01010", "01110", "11111", "01110", "01010", "00000"),
}

# --------------------------------------------------------------- canvas ---
W, H = 1024, 1024
PAPER = (247, 242, 230)
INK = (18, 18, 18)
RED = (178, 34, 34)
CARD = (255, 255, 255)
GREY = (90, 86, 78)
BAR_COLORS = [
    (178, 34, 34), (31, 58, 95), (34, 90, 58),
    (196, 110, 16), (96, 48, 120), (14, 110, 110),
]


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def text(self, s, x, y, scale, color, bold=False):
        cx = x
        for ch in s.upper():
            glyph = FONT.get(ch, FONT[' '])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == '1':
                        for dy in range(scale):
                            for dx in range(scale):
                                self.set(cx + col * scale + dx,
                                         y + row * scale + dy, color)
                        if bold:
                            for dy in range(scale):
                                for dx in range(scale):
                                    self.set(cx + col * scale + dx + 1,
                                             y + row * scale + dy, color)
            cx += 6 * scale
        return cx

    def text_width(self, s, scale):
        return len(s) * 6 * scale - scale

    def centred(self, s, y, scale, color, bold=False):
        x = (self.w - self.text_width(s, scale)) // 2
        self.text(s, x, y, scale, color, bold=bold)

    def wrap(self, s, scale, max_w):
        lines, cur = [], ""
        for word in s.split(" "):
            trial = (cur + " " + word).strip()
            if self.text_width(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines


# ------------------------------------------------------------------ png ----
def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def png_bytes(canvas):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        raw.extend(canvas.px[y * stride:(y + 1) * stride])
    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    data = b"\x89PNG\r\n\x1a\n"
    data += chunk(b"IHDR", ihdr)
    data += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    data += chunk(b"IEND", b"")
    return data


# -------------------------------------------------------------- stories ----
STORIES = [
    ("1. STRAIT OF HORMUZ", "TWO TANKERS HIT MINES, BURN",
     "Iran's Guards say two tankers exploded after hitting mines near "
     "Oman's Khasab. One carried 2 million barrels of crude."),
    ("2. SAUDI UNDER FIRE", "HOUTHIS HIT REFINERY, RIYADH",
     "Houthis claim a strike on Ras Tanura refinery and Riyadh's "
     "financial district. A drone hit Riyadh's tallest tower."),
    ("3. UKRAINE WAR", "RUSSIA HITS TWO GRAIN SHIPS",
     "Russia attacks two foreign cargo ships carrying over 100,000 tons "
     "of grain near Odesa's Black Sea ports."),
    ("4. MARKETS", "ASIA BOUNCES, NVIDIA SLIDES",
     "Nikkei gains 1.6 percent and Kospi 1.9 percent. Nvidia falls 3.9 "
     "percent, 2.3 trillion below its October peak."),
    ("5. US POLITICS", "TRUMP DEMANDS GDP DATA PROBE",
     "Trump demands a probe into growth numbers released before the "
     "midterms, calling them fake."),
    ("6. AFRICA", "GUINEA-BISSAU DELAYS VOTE",
     "Military leaders delay elections by about two years to November "
     "2028, a year after the coup."),
]


def render():
    c = Canvas(W, H, PAPER)
    # Masthead.
    c.centred("THE WORLD TODAY", 26, 8, INK, bold=True)
    c.rect(60, 96, W - 120, 5, RED)
    # Date line and sub-line.
    c.centred("FRIDAY, 27 NOVEMBER 2026", 116, 3, INK, bold=True)
    c.centred("SIX STORIES THAT DEFINED THE DAY", 146, 2, GREY)
    c.rect(60, 178, W - 120, 2, INK)
    # Six story cards, 2 x 3 grid.
    margin, gap = 40, 24
    card_w = (W - 2 * margin - gap) // 2
    card_h = 236
    top = 200
    for i, (kicker, headline, summary) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = margin + col * (card_w + gap)
        y = top + row * (card_h + gap)
        c.rect(x, y, card_w, card_h, CARD)
        # 1px outline so the white card reads against the paper.
        c.rect(x, y, card_w, 1, INK)
        c.rect(x, y + card_h - 1, card_w, 1, INK)
        c.rect(x, y, 1, card_h, INK)
        c.rect(x + card_w - 1, y, 1, card_h, INK)
        c.rect(x + 1, y + 1, card_w - 2, 10, BAR_COLORS[i])
        c.text(kicker, x + 16, y + 22, 2, BAR_COLORS[i], bold=True)
        lines = c.wrap(headline, 3, card_w - 32)
        ly = y + 50
        for line in lines:
            c.text(line, x + 16, ly, 3, INK, bold=True)
            ly += 25
        slines = c.wrap(summary, 2, card_w - 32)
        ly += 6
        for line in slines:
            c.text(line, x + 16, ly, 2, (58, 54, 48))
            ly += 17
    # Footer.
    c.rect(60, 962, W - 120, 2, INK)
    c.centred("SOURCES: REUTERS / AP",
              976, 2, GREY)
    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = png_bytes(render())
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (path, len(data)))


if __name__ == "__main__":
    main()
