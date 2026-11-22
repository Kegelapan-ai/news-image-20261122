#!/usr/bin/env python3
"""Draw the 22 November 2026 front page: one 1024x1024 PNG.

Everything here is local and fixed: bundled DejaVu fonts, no clock,
no random numbers, no network. Running this twice writes the same bytes.
"""

import math
import os
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "image.png")

W, H = 1024, 1024
PAPER = (251, 247, 236)
INK = (26, 26, 26)
RULE = (26, 26, 26)
ACCENT = (178, 38, 30)
CARD_BG = (255, 255, 255)
LEAD_BG = (245, 238, 221)
FOOT_BG = (239, 233, 216)
MUTED = (90, 84, 70)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 56)
F_DATE = font("DejaVuSans-Bold.ttf", 20)
F_SUB = font("DejaVuSans.ttf", 15)
F_KICK = font("DejaVuSans-Bold.ttf", 13)
F_HEAD = font("DejaVuSerif-Bold.ttf", 21)
F_HEAD_LEAD = font("DejaVuSerif-Bold.ttf", 30)
F_HEAD_STRIP = font("DejaVuSerif-Bold.ttf", 22)
F_BODY = font("DejaVuSans.ttf", 15)
F_BODY_LEAD = font("DejaVuSans.ttf", 16)
F_FOOT = font("DejaVuSans.ttf", 12)
F_FOOT_B = font("DejaVuSans-Bold.ttf", 12)
F_SRC = font("DejaVuSans.ttf", 11)


def wrap(draw, text, fnt, width):
    """Greedy word wrap on pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, width, max_lines):
    """Wrap text and clip to max_lines, adding an ellipsis if cut."""
    lines = wrap(draw, text, fnt, width)
    if len(lines) <= max_lines:
        return lines
    print("WARNING: text clipped to %d lines: %r" % (max_lines, text[:60]),
          file=sys.stderr)
    cut = lines[:max_lines]
    while cut and draw.textlength(cut[-1] + " ...", font=fnt) > width:
        cut[-1] = cut[-1].rsplit(" ", 1)[0] if " " in cut[-1] else ""
    cut[-1] = (cut[-1] + " ...").strip()
    return cut


# ---------------------------------------------------------------- icons
# Each icon draws simple shapes inside a square box (x, y, size).


def icon_globe(d, x, y, s):
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=INK, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=INK, width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340, fill=INK, width=2)
    # small flame above the globe: the talks burned out
    fx, fy = cx, cy - r - 2
    d.polygon([(fx - 7, fy + 12), (fx, fy), (fx + 7, fy + 12)], fill=ACCENT)


def icon_flats(d, x, y, s):
    d.rectangle([x + 8, y + 18, x + 30, y + s - 6], outline=INK, width=2)
    d.rectangle([x + 34, y + 10, x + s - 8, y + s - 6], outline=INK, width=2)
    for wx in (x + 13, x + 21):
        for wy in (y + 24, y + 34, y + 44):
            d.rectangle([wx, wy, wx + 5, wy + 5], fill=INK)
    for wx in (x + 40, x + 48):
        for wy in (y + 16, y + 26, y + 36, y + 46):
            d.rectangle([wx, wy, wx + 5, wy + 5], fill=INK)
    # crack down the taller block
    d.line([x + 44, y + 10, x + 40, y + 30, x + 48, y + 48], fill=ACCENT, width=2)
    # tiny drone overhead
    d.line([x + 44, y + 2, x + s - 4, y + 2], fill=INK, width=2)
    d.ellipse([x + s - 12, y, x + s - 6, y + 6], outline=INK, width=2)


def icon_ship(d, x, y, s):
    d.polygon(
        [(x + 6, y + s - 22), (x + s - 6, y + s - 22),
         (x + s - 14, y + s - 8), (x + 14, y + s - 8)],
        outline=INK, width=2,
    )
    for i, cx in enumerate((x + 14, x + 28, x + 42)):
        d.rectangle([cx, y + s - 38, cx + 11, y + s - 23],
                    fill=ACCENT if i == 1 else INK)
    d.line([x + 4, y + s - 2, x + s - 4, y + s - 2], fill=INK, width=2)
    d.arc([x + 8, y + s - 10, x + 26, y + s + 4], 180, 360, fill=INK, width=2)
    d.arc([x + s - 28, y + s - 10, x + s - 10, y + s + 4], 180, 360,
          fill=INK, width=2)


def icon_factory(d, x, y, s):
    d.rectangle([x + 8, y + 26, x + s - 8, y + s - 6], outline=INK, width=2)
    d.line([x + 8, y + 26, x + 18, y + 16, x + 28, y + 26, x + 38, y + 16,
            x + 48, y + 26], fill=INK, width=2)
    d.rectangle([x + s - 16, y + 8, x + s - 10, y + 26], fill=INK)
    d.polygon([(x + s - 19, y + 2), (x + s - 13, y - 6), (x + s - 7, y + 2)],
              fill=ACCENT)
    for wx in (x + 13, x + 25, x + 37):
        d.rectangle([wx, y + 34, wx + 7, y + 41], fill=INK)
    d.polygon([(x + 16, y + s - 6), (x + 26, y + s - 20), (x + 36, y + s - 6)],
              fill=ACCENT)


def icon_boat(d, x, y, s):
    d.polygon([(x + 8, y + s - 26), (x + s - 8, y + s - 26),
               (x + s - 18, y + s - 10), (x + 18, y + s - 10)],
              outline=INK, width=2)
    for px in (x + 20, x + 32, x + 44):
        d.ellipse([px, y + s - 40, px + 7, y + s - 33], fill=INK)
        d.rectangle([px - 1, y + s - 32, px + 8, y + s - 26], fill=INK)
    d.arc([x + 6, y + s - 8, x + 26, y + s + 6], 180, 360, fill=INK, width=2)
    d.arc([x + s - 28, y + s - 8, x + s - 8, y + s + 6], 180, 360,
          fill=INK, width=2)


def icon_shield(d, x, y, s):
    pts = [(x + s // 2, y + 2), (x + s - 6, y + 12), (x + s - 6, y + s // 2),
           (x + s // 2, y + s - 4), (x + 6, y + s // 2), (x + 6, y + 12)]
    d.polygon(pts, outline=INK, width=3)
    cx, cy, r = x + s // 2, y + s // 2 - 2, 11
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        star.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(star, fill=ACCENT)


# ---------------------------------------------------------------- cards

def story_card(d, x, y, w, h, kicker, headline, body, icon, bg=CARD_BG):
    d.rectangle([x, y, x + w, y + h], fill=bg, outline=RULE, width=2)
    ix, iy, isize = x + 12, y + 40, 64
    icon(d, ix, iy, isize)
    tx = x + 92
    tw = w - 92 - 14
    d.text((tx, y + 10), kicker, font=F_KICK, fill=ACCENT)
    head = fit_lines(d, headline, F_HEAD, tw, 2)
    hy = y + 32
    for line in head:
        d.text((tx, hy), line, font=F_HEAD, fill=INK)
        hy += 26
    body_lines = fit_lines(d, body, F_BODY, tw, 4)
    by = hy + 6
    for line in body_lines:
        d.text((tx, by), line, font=F_BODY, fill=INK)
        by += 19
    # safety: nothing may run past the card's inner bottom edge
    assert by - 19 <= y + h - 10, "card text overflow: %s" % kicker


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([14, 14, W - 15, H - 15], outline=RULE, width=2)

    # ---- top strip
    d.text((30, 26), "THE WORLD  •  ONE DAY  •  ONE PAGE", font=F_KICK,
           fill=MUTED)
    right = "No. 326  •  2026"
    d.text((W - 30 - d.textlength(right, font=F_KICK), 26), right,
           font=F_KICK, fill=MUTED)

    # ---- masthead
    title = "THE DAY IN THE WORLD"
    d.text(((W - d.textlength(title, font=F_MAST)) // 2, 52), title,
           font=F_MAST, fill=INK)
    d.line([30, 128, W - 30, 128], fill=ACCENT, width=4)
    date = "SUNDAY  22  NOVEMBER  2026"
    d.text(((W - d.textlength(date, font=F_DATE)) // 2, 138), date,
           font=F_DATE, fill=ACCENT)
    sub = "Six stories that summed up the day — from Antalya to Kyiv, Bahrain to Bayelsa."
    d.text(((W - d.textlength(sub, font=F_SUB)) // 2, 166), sub,
           font=F_SUB, fill=MUTED)

    # ---- lead story: COP31, full width
    lx, ly, lw, lh = 30, 196, W - 60, 148
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=LEAD_BG, outline=RULE,
                width=2)
    icon_globe(d, lx + 14, ly + 42, 66)
    tx = lx + 100
    tw = lw - 100 - 16
    d.text((tx, ly + 10), "CLIMATE  •  LEAD STORY", font=F_KICK, fill=ACCENT)
    d.text((tx, ly + 32), "CLIMATE TALKS COLLAPSE — NO DEAL AT COP31",
           font=F_HEAD_LEAD, fill=INK)
    lead_body = (
        "After two weeks in Antalya, Türkiye, and two days of overtime, the UN "
        "climate summit ended on Sunday with no final pact. The draft deal did "
        "not mention fossil fuels at all, and the EU refused to endorse it. "
        "UN chief António Guterres called the outcome “deeply disappointing”."
    )
    lines = fit_lines(d, lead_body, F_BODY_LEAD, tw, 3)
    by = ly + 74
    for line in lines:
        d.text((tx, by), line, font=F_BODY_LEAD, fill=INK)
        by += 21
    assert by - 21 <= ly + lh - 10, "lead text overflow"

    # ---- four-card grid
    gx, gy = 30, 356
    cw, ch, gap = 477, 200, 10
    cards = [
        ("UKRAINE",
         "Drone flattens flats near Kyiv; 14 missing",
         "A Russian drone hit a five-storey block in Dymer, near Kyiv, on "
         "Sunday morning. Nine people were rescued; 14 were still missing. "
         "Zelenskyy said Russia fired 165 missiles at Ukraine in one week.",
         icon_flats),
        ("THE GULF",
         "Iran hits Bahrain; US denies jet claim",
         "Bahrain said two people were hurt when an Iranian strike hit a "
         "civilian site. Iran claimed it hit US Patriot radars. US Central "
         "Command denied Iran’s claim that it damaged a US F-16 jet.",
         icon_ship),
        ("INDONESIA",
         "Factory fire kills 3; dozens missing",
         "Rescuers searched a burned-out candy factory in Cikande, Banten, "
         "on Sunday. Three workers were killed and 36 were still missing. "
         "The cause has not been announced.",
         icon_factory),
        ("NIGERIA",
         "Boat toll rises to 24 after funeral trip",
         "At least 24 people died when a crowded boat carrying mourners to "
         "a funeral capsized in Bayelsa State. The toll rose on Sunday as "
         "more bodies were found; 24 survivors were rescued.",
         icon_boat),
    ]
    for i, (kick, head, body, icon) in enumerate(cards):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        story_card(d, cx, cy, cw, ch, kick, head, body, icon)

    # ---- NATO strip, full width
    sx, sy, sw, sh = 30, 778, W - 60, 100
    d.rectangle([sx, sy, sx + sw, sy + sh], fill=CARD_BG, outline=RULE,
                width=2)
    icon_shield(d, sx + 12, sy + 14, 62)
    tx = sx + 92
    d.text((tx, sy + 8), "NATO  •  POLAND", font=F_KICK, fill=ACCENT)
    d.text((tx, sy + 28), "NATO calls emergency talks after missiles land in Poland",
           font=F_HEAD_STRIP, fill=INK)
    strip_body = (
        "Ambassadors meet in Brussels on Monday after Russian missiles and a "
        "drone came down in south-east Poland. NATO chief Mark Rutte said the "
        "alliance will defend “every inch” of Polish territory."
    )
    lines = fit_lines(d, strip_body, F_BODY, sw - 92 - 14, 2)
    by = sy + 56
    for line in lines:
        d.text((tx, by), line, font=F_BODY, fill=INK)
        by += 19
    assert by - 19 <= sy + sh - 8, "strip text overflow"

    # ---- footer: also today, 2 x 2
    fx, fy, fw, fh = 30, 890, W - 60, 92
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=FOOT_BG, outline=RULE,
                width=2)
    d.text((fx + 12, fy + 6), "ALSO TODAY", font=F_KICK, fill=ACCENT)
    foot_items = [
        ("JAPAN — ", "Shuri Castle’s rebuilt main hall was celebrated in "
         "Okinawa on Sunday, seven years after fire destroyed it."),
        ("HORMUZ — ", "Two more tankers were struck near the strait on "
         "Saturday, monitors said, as attacks on shipping rose."),
        ("TRADE — ", "The EU and Indonesia signed a trade deal on Saturday "
         "after ten years of talks; tariffs on up to 98.5% of goods will "
         "fall."),
        ("WASHINGTON — ", "The Wall Street Journal reported that President "
         "Trump’s bid to meet North Korea’s Kim Jong Un failed."),
    ]
    cell_w, cell_h = (fw - 24) // 2, 30
    for i, (lead, rest) in enumerate(foot_items):
        cell_x = fx + 12 + (i % 2) * cell_w
        cell_y = fy + 26 + (i // 2) * cell_h
        full = lead + rest
        lines = fit_lines(d, full, F_FOOT, cell_w - 8, 2)
        ly2 = cell_y
        for line in lines:
            # bold the lead-in on the first line only
            if line is lines[0] and line.startswith(lead):
                d.text((cell_x, ly2), lead, font=F_FOOT_B, fill=INK)
                d.text((cell_x + d.textlength(lead, font=F_FOOT_B), ly2),
                       line[len(lead):], font=F_FOOT, fill=INK)
            else:
                d.text((cell_x, ly2), line, font=F_FOOT, fill=INK)
            ly2 += 15
        assert ly2 - 16 <= cell_y + cell_h - 2, "footer overflow"

    # ---- sources line
    src = ("Sources: Reuters  •  AP  •  UN News  •  CNN  •  NATO / Polish Press "
           "Agency — figures as reported on 22 Nov 2026.")
    d.text(((W - d.textlength(src, font=F_SRC)) // 2, 992), src,
           font=F_SRC, fill=MUTED)

    img.save(OUT, format="PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    build()
