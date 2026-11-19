#!/usr/bin/env python3
"""Draw entry.png for the make.fun news-image-20261118 bounty.

A one-page newspaper front page summing up Wednesday 18 November 2026.
Stories were checked against wire reports of that day (AP / AFP / Reuters
via Outlook India, Open Chronicle, Dawn, Business Recorder, Qatar Tribune,
Japan Times, Straits Times, all dated 18 Nov 2026):

  1. Trump lands in Shenzhen for a historic trilateral with Xi and Putin.
  2. Ukraine strike partly destroys the Crimean Bridge (Zelensky confirms).
  3. Iran hits a US base in Kuwait; tankers struck in the Strait of Hormuz.
  4. Israel opens a "concentrated operation" in three areas of central Gaza.
  5. Peltola beats Sullivan in Alaska; Democrats projected 56-44 in Senate.
  6. Russian military plane crashes in Siberia; 19 dead.
  Also: Cyclone Akvan strengthens off Odisha; trains collide near Prague.

Run:  python3 tools/generate-entry.py   (writes entry.png next to main.ts)
Uses only Pillow + DejaVu fonts already on this machine. The entry program
itself (main.ts) only copies the finished PNG; it imports nothing.
"""

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 247, 239)   # warm ivory
INK = (22, 35, 63)        # deep navy
BODY = (51, 65, 92)       # slate navy
MUTED = (110, 118, 135)   # grey blue
RED = (179, 38, 30)
CARD = (255, 255, 255)
LINE = (203, 210, 220)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")
REG = str(FONT_DIR / "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def spaced(draw, xy, text, fnt, fill, tracking=3):
    """Draw text with manual letter tracking."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def draw_globe(draw, cx, cy, r, color, width=4):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=width)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=color, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=20, end=160, fill=color, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=200, end=340, fill=color, width=3)


def panel(draw, x, y, w, h, num, color, headline, body):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=CARD, outline=LINE, width=1)
    draw.rectangle([x, y, x + w, y + 7], fill=color)
    # number badge
    bx, by, br = x + 20, y + 26, 19
    draw.ellipse([bx - br, by - br, bx + br, by + br], fill=color)
    num_f = font(BOLD, 20)
    tw = draw.textlength(num, font=num_f)
    draw.text((bx - tw / 2, by - 13), num, font=num_f, fill=(255, 255, 255))
    # headline + body
    tx = x + 52
    twidth = x + w - 18 - tx
    hf = font(BOLD, 26)
    lines = wrap(draw, headline, hf, twidth)
    ly = y + 20
    for ln in lines[:2]:
        draw.text((tx, ly), ln, font=hf, fill=INK)
        ly += 31
    bf = font(REG, 20)
    blines = wrap(draw, body, bf, twidth)
    ly += 4
    for ln in blines[:2]:
        draw.text((tx, ly), ln, font=bf, fill=BODY)
        ly += 25


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36  # side margin

    # ---- masthead ----
    d.rectangle([mx, 26, W - mx, 32], fill=RED)
    spaced(d, (mx, 46), "THE WORLD TODAY", font(BOLD, 24), INK, tracking=4)
    wk = font(BOLD, 24)
    d.text((W - mx - d.textlength("WEDNESDAY", font=wk), 46),
           "WEDNESDAY", font=wk, fill=INK)
    d.text((mx, 82), "18 NOVEMBER 2026", font=font(BOLD, 66), fill=INK)
    d.text((mx, 152), "Six stories that defined the day, from Shenzhen to the Senate.",
           font=font(REG, 23), fill=MUTED)
    d.rectangle([mx, 186, W - mx, 188], fill=INK)

    # ---- lead story ----
    lx, ly, lw, lh = mx, 204, W - 2 * mx, 196
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10,
                        fill=CARD, outline=LINE, width=1)
    d.rectangle([lx, ly, lx + 10, ly + lh], fill=RED)
    tx = lx + 30
    d.text((tx, ly + 18), "SHENZHEN  •  APEC SUMMIT", font=font(BOLD, 21), fill=RED)
    d.text((tx, ly + 48), "TRUMP LANDS IN CHINA FOR", font=font(BOLD, 38), fill=INK)
    d.text((tx, ly + 92), "HISTORIC THREE-WAY TALKS", font=font(BOLD, 38), fill=INK)
    d.text((tx, ly + 144), "First trilateral with Xi and Putin; Xi and Putin",
           font=font(REG, 22), fill=BODY)
    d.text((tx, ly + 170), "met first to coordinate ahead of the summit.",
           font=font(REG, 22), fill=BODY)
    draw_globe(d, lx + lw - 78, ly + 100, 58, INK)

    # ---- story grid ----
    stories = [
        ("01", (29, 78, 137), "UKRAINE HITS CRIMEA BRIDGE",
         "Strike partly destroys the link to Crimea, Zelensky confirms."),
        ("02", (14, 124, 123), "GULF ON EDGE",
         "Iran hits a US base in Kuwait; tankers struck in the Strait of Hormuz."),
        ("03", (185, 122, 15), "ISRAEL OPENS GAZA OPERATION",
         "\u201cConcentrated operation\u201d begins in three areas of central Gaza."),
        ("04", (109, 59, 142), "SENATE FLIPS TO DEMOCRATS",
         "Peltola beats Sullivan in Alaska; Democrats projected 56\u201344."),
        ("05", (74, 85, 104), "19 DEAD IN SIBERIA AIR CRASH",
         "Russian military plane goes down; all on board killed."),
        ("06", (11, 94, 89), "CYCLONE AKVAN NEARS INDIA",
         "Severe storm bears down on Odisha; shelters open."),
    ]
    pw, ph, gap = 468, 164, 16
    gy = 416
    for i, (num, color, head, body) in enumerate(stories):
        x = mx + (i % 2) * (pw + gap)
        y = gy + (i // 2) * (ph + gap)
        panel(d, x, y, pw, ph, num, color, head, body)

    # ---- footer ----
    d.rectangle([mx, 946, W - mx, 947], fill=LINE)
    foot = "Wednesday 18 November 2026  •  Compiled from wire reports of the day"
    ff = font(REG, 19)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 960), foot, font=ff, fill=MUTED)
    also = "Also: trains collide near Prague, dozens hurt  •  India-US trade deal nearly done"
    af = font(REG, 18)
    d.text(((W - d.textlength(also, font=af)) / 2, 984), also, font=af, fill=MUTED)

    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, {img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
