#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page (1024x1024 PNG).

News researched 19 Nov 2026 from Horizon / Open Chronicle / OneTurn:
- Shenzhen: Trump, Xi and Putin hold first trilateral summit (APEC)
- The Hague: ICJ rules on the Rohingya genocide case against Myanmar
- Crimea: Ukraine strikes the Crimean Bridge again, traffic suspended
- Gulf: Iran attacks Kuwait and Bahrain after the US strike on Qeshm
- Antalya: COP31 ministers race to unblock the climate talks
- Dhaka: Bangladesh in turmoil, Yunus home burned, 28 districts hit
- Markets: Anthropic $81.3B IPO record; Van Gogh sells for $190.4M

Run: python3 generate_image.py  -> writes entry.png (1024x1024, <1 MiB).
Only Pillow is needed to *build* the image; main.py (the entry) is
stdlib-only and just copies entry.png, so the grader needs no Pillow.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 248, 238)
INK = (17, 17, 17)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
TEAL = (15, 118, 110)
GOLD = (180, 130, 20)
GREY = (90, 90, 90)
LIGHT = (238, 232, 218)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap, returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=4):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def card(draw, x, y, w, h, tag, tag_color, headline, deck):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=WHITE, outline=(200, 190, 170), width=2)
    draw.rectangle([x, y, x + w, y + 8], fill=tag_color)
    yy = y + 18
    draw.text((x + 14, yy), tag, font=font(SANS_B, 17), fill=tag_color)
    yy += 28
    yy = text_block(draw, x + 14, yy, headline, font(SANS_B, 27),
                    INK, w - 28, leading=2)
    yy += 2
    text_block(draw, x + 14, yy, deck, font(SANS, 19),
               (60, 60, 60), w - 28, leading=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Top black bar
    d.rectangle([0, 0, W, 58], fill=INK)
    d.text((24, 14), "THE WORLD IN ONE DAY", font=font(SANS_B, 26), fill=WHITE)
    d.text((W - 24, 16), "THURSDAY 19 NOVEMBER 2026",
           font=font(SANS_B, 22), fill=(255, 210, 90), anchor="ra")

    # Kicker + main headline
    d.text((24, 74), "SHENZHEN  •  THE HAGUE  •  KYIV  •  THE GULF  •  ANTALYA  •  DHAKA",
           font=font(SANS_B, 19), fill=RED)
    y = 102
    y = text_block(d, 24, y, "Trump, Xi and Putin meet",
                   font(SERIF_B, 56), INK, W - 48, leading=0)
    y = text_block(d, 24, y - 6, "in Shenzhen",
                   font(SERIF_B, 56), INK, W - 48, leading=0)

    # Hero deck: one line so the hero strip stays high on the page
    y += 4
    y = text_block(d, 24, y,
                   "First trilateral summit at APEC. Ukraine and nuclear arms top the agenda.",
                   font(SANS, 22), (40, 40, 40), W - 48, leading=3)

    # Hero strip: three leaders, three flags as coloured chips
    hy = y + 12
    d.rounded_rectangle([24, hy, W - 24, hy + 118], radius=12,
                        fill=(16, 42, 90), outline=(16, 42, 90))
    leaders = [
        ("USA", "TRUMP", (178, 34, 34)),
        ("CHINA", "XI JINPING", (200, 30, 30)),
        ("RUSSIA", "PUTIN", (29, 78, 216)),
    ]
    cx = 48
    for country, name, col in leaders:
        d.rounded_rectangle([cx, hy + 18, cx + 288, hy + 100], radius=10,
                            fill=WHITE)
        d.rectangle([cx, hy + 18, cx + 288, hy + 28], fill=col)
        d.text((cx + 16, hy + 38), country, font=font(SANS_B, 20), fill=GREY)
        d.text((cx + 16, hy + 62), name, font=font(SANS_B, 30), fill=INK)
        cx += 312
    d.text((24, hy + 128), "APEC SUMMIT  •  SHENZHEN, CHINA  •  19 NOVEMBER 2026",
           font=font(SANS_B, 18), fill=GREY)

    # Six story cards, 2 columns x 3 rows
    cards = [
        ("THE HAGUE", TEAL,
         "ICJ rules on Rohingya genocide",
         "Myanmar faces a genocide verdict over the 2017 crackdown that drove 730,000 Rohingya to Bangladesh."),
        ("CRIMEA", RED,
         "Ukraine hits Crimean Bridge again",
         "Traffic suspended after a new strike — the third in a week on the key link to occupied Crimea."),
        ("THE GULF", BLUE,
         "Iran widens war to Gulf states",
         "Kuwait and Bahrain targeted after the US strike on Qeshm. IEA: Hormuz crisis threatens energy security."),
        ("ANTALYA", TEAL,
         "COP31: ministers race to unblock talks",
         "Negotiators in Turkey push for a final climate text as the summit enters its decisive phase."),
        ("DHAKA", RED,
         "Bangladesh in turmoil",
         "Yunus ancestral home burned; violence and bomb blasts in 28 districts as Hasina return looms."),
        ("MARKETS", GOLD,
         "Anthropic IPO sets $81.3B record",
         "Valued at $1.5 trillion. Van Gogh sells for $190.4M, a record. Brent $89.59, VIX 24.6."),
    ]
    gx, gy = 24, hy + 158
    cw, ch, gap = 476, 148, 24
    for i, (tag, col, head, deck) in enumerate(cards):
        x = gx + (i % 2) * (cw + gap)
        yy = gy + (i // 2) * (ch + 14)
        card(d, x, yy, cw, ch, tag, col, head, deck)

    # Bottom strip: also today
    by = 908
    d.rectangle([0, by, W, H], fill=INK)
    d.text((24, by + 10), "ALSO TODAY",
           font=font(SANS_B, 19), fill=(255, 210, 90))
    d.text((24, by + 36),
           "Gaza op beyond ceasefire line  •  EU €45B loan to Ukraine",
           font=font(SANS, 18), fill=WHITE)
    d.text((24, by + 60),
           "N. Korea expands uranium enrichment  •  US loses measles-free status",
           font=font(SANS, 18), fill=WHITE)
    d.text((24, H - 22), "All stories reported on 19 Nov 2026  •  Sources: Horizon, Open Chronicle, OneTurn",
           font=font(SANS, 13), fill=(180, 180, 180))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
