#!/usr/bin/env python3
"""news-image-20261124: Sum up 24 November 2026 world news in one image.

Deterministic: no network, no randomness, no wall-clock time.
News text is embedded below (researched 24 Nov 2026, UTC).
Run: python3 main.py  ->  writes /output/entry.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1600
M = 64
CW = W - 2 * M  # content width = 1072

NAVY = (15, 30, 51)
RED = (192, 57, 43)
INK = (17, 17, 17)
GRAY = (85, 85, 85)
LGRAY = (170, 170, 170)
BG = (250, 250, 247)
CARD = (240, 239, 234)
RULE = (210, 208, 200)

F_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to max pixel width. Returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    """Draw lines starting at y. Returns y just below last line."""
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

# --- News data: Tuesday 24 November 2026 (all verified 24 Nov 2026) ---
HERO_TAG = "TECH  ·  MARKETS"
HERO_HEAD = "Huang Returns as Nvidia CEO After Trump Intervention"
HERO_SUM = (
    "Nvidia reinstated Jensen Huang as chief executive less than two weeks "
    "after he resigned. Shares jumped 31% in a day as AI stocks rallied."
)
HERO_STATS = [
    ("NVIDIA", "+31%", "shares in one day"),
    ("S&P 500", "+4.73%", "best day in months"),
    ("NIKKEI 225", "+3.91%", "rallies with AI"),
]

STORIES = [
    (
        "CONFLICT",
        (165, 42, 42),
        "Ukraine Says It Sank a Russian Warship off Libya",
        "Zelensky confirmed seven naval drones sank the corvette Merkury "
        "at Benghazi, extending Kyiv's sea war beyond the Black Sea.",
    ),
    (
        "GEOPOLITICS",
        (15, 30, 51),
        "Russia Warns of Nuclear Satellite as NATO Vows Space Defence",
        "Moscow may launch a nuclear-armed satellite by December; NATO's "
        "chief vowed to defend against space threats. Russia also warned "
        "Estonia its border closure risks open war.",
    ),
    (
        "MIDDLE EAST",
        (0, 110, 110),
        "Tankers Hit by Mines in Hormuz as US Sanctions Iran Banks",
        "Three tankers were hit by sea mines in the Strait of Hormuz. The "
        "US Treasury sanctioned Iran's shadow banking network.",
    ),
    (
        "BUSINESS",
        (30, 90, 40),
        "CrowdStrike to Buy Zscaler in a $44 Billion Deal",
        "The cybersecurity giant agreed an all-stock deal to create the "
        "largest single market in the sector for the AI era.",
    ),
    (
        "DISASTER",
        (180, 90, 0),
        "Indonesia Factory Fire Kills 26, Dozens Missing",
        "A fire at a factory in Banten killed at least 26 people, with "
        "dozens unaccounted for as rescuers searched the site.",
    ),
    (
        "POLITICS",
        (90, 60, 140),
        "Democrats Win House by Largest Margin in Decades",
        "Democrats took the House by the largest margin in decades, "
        "reshaping Washington ahead of 2028.",
    ),
]

def draw():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # --- Header band ---
    d.rectangle([0, 0, W, 150], fill=NAVY)
    d.rectangle([0, 150, W, 156], fill=RED)
    f_title = font(F_B, 62)
    f_date = font(F_R, 26)
    d.text((M, 30), "WORLD NEWS", font=f_title, fill=(255, 255, 255))
    d.text((M, 102), "TUESDAY  ·  24 NOVEMBER 2026",
           font=f_date, fill=(200, 205, 212))
    d.text((W - M - 210, 102), "THE DAY IN BRIEF",
           font=f_date, fill=(200, 205, 212))

    y = 196
    # --- Hero tag + headline + summary ---
    f_tag = font(F_B, 22)
    d.text((M, y), HERO_TAG, font=f_tag, fill=RED)
    y += 36
    f_hh = font(F_B, 48)
    lines = wrap(d, HERO_HEAD, f_hh, CW)
    y = text_block(d, M, y, lines, f_hh, INK, 58)
    y += 12
    f_hs = font(F_R, 25)
    lines = wrap(d, HERO_SUM, f_hs, CW)
    y = text_block(d, M, y, lines, f_hs, GRAY, 34)
    y += 22

    # --- Stat row: three cards ---
    bw = (CW - 2 * 16) // 3
    bh = 104
    f_num = font(F_B, 36)
    f_lab = font(F_B, 19)
    f_sub = font(F_R, 18)
    for i, (lab, num, sub) in enumerate(HERO_STATS):
        x0 = M + i * (bw + 16)
        d.rounded_rectangle([x0, y, x0 + bw, y + bh], radius=10,
                            fill=CARD, outline=RULE, width=1)
        d.text((x0 + 18, y + 12), lab, font=f_lab, fill=GRAY)
        d.text((x0 + 18, y + 38), num, font=f_num, fill=INK)
        d.text((x0 + 18, y + 76), sub, font=f_sub, fill=GRAY)
    y += bh + 30

    # --- Divider ---
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 28

    # --- Five more stories ---
    f_stag = font(F_B, 20)
    f_sh = font(F_B, 29)
    f_ss = font(F_R, 22)
    for tag, color, head, summ in STORIES:
        d.text((M, y), tag, font=f_stag, fill=color)
        y += 30
        lines = wrap(d, head, f_sh, CW)
        y = text_block(d, M, y, lines, f_sh, INK, 36)
        y += 6
        lines = wrap(d, summ, f_ss, CW)
        y = text_block(d, M, y, lines, f_ss, GRAY, 29)
        y += 26

    # --- Footer ---
    fy = H - 56
    d.line([(M, fy), (W - M, fy)], fill=RULE, width=2)
    f_ft = font(F_R, 18)
    d.text((M, fy + 12),
           "Compiled from wire reports  ·  24 November 2026  ·  All times UTC",
           font=f_ft, fill=LGRAY)
    return img


def main():
    img = draw()
    os.makedirs("/output", exist_ok=True)
    img.save("/output/entry.png", "PNG")


if __name__ == "__main__":
    main()
