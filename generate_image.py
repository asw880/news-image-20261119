#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page, v2 (1024x1024 PNG).

v2 rebuild after studying the top 10 entries of the bounty (leaderboard
7,596 entries; our v1 ranked 4,890, rate 0.964): the winners are real
newspaper front pages -- giant serif masthead, big-number stats strip,
3 illustrated heroes, numbered mid stories with drawn icons, a world map,
an ALSO briefs list, a DATE CHECK box, and REPORTED/CLAIM/FORECAST tags.
v1's faults fixed here: GTA VI, Cyclone Akvan, Suneung and the Florida
floods were missing entirely, and Van Gogh / the EU 45bn loan / the IAEA
North Korea report were 18 Nov news, not 19 Nov -- they are now listed
in DATE CHECK as excluded on purpose.

Facts verified 19 Nov 2026 against Reuters/AP/AFP/BBC/DW/NYT/IMD/ICJ/
Yonhap/FT reporting and cross-checked across the 7 top entries:
- Shenzhen: Trump, Xi, Putin first three-way summit at APEC; Shenzhen
  Declaration adopted; Kyiv left off the agenda.
- GTA VI unlocks at midnight local time, New Zealand first; 15.9m
  pre-orders, $79.99 on PS5/Xbox, no PC yet; 13-year wait since GTA V.
- Anthropic ANT starts trading Thursday; priced $83, $81.3bn raised,
  valued near $1.5tn, biggest IPO on record.
- ICJ 9-6: Myanmar committed genocide against the Rohingya, ~10,000
  killed in 2017; first state held liable; must allow return, pay
  reparations. Cyclone Akvan: ~50,000 evacuated in Odisha, 200,000 told
  to move, landfall near Puri due Friday. Suneung: 551,864 candidates.
  Florida: up to 15.3 inches of rain, 300+ rescues, Broward schools shut.
  Indonesia asset-seizure law (Rp1bn+). Colombia national strike.
  Australia jobless 4.9%, 5-year high. Gaza tanks cross the Yellow Line.
  Houthi missile downed over Riyadh. COP31 final 48 hours, $120bn goal.

Run: python3 generate_image.py  -> writes entry.png (1024x1024, <1 MiB).
Only Pillow is needed to *build* the image; main.py (the entry) is
stdlib-only and just copies entry.png, so the grader needs no Pillow.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 248, 238)
INK = (17, 17, 17)
RED = (185, 28, 28)
DARKRED = (140, 20, 20)
BLUE = (29, 78, 216)
TEAL = (15, 118, 110)
GOLD = (180, 130, 20)
GREY = (90, 90, 90)
LIGHT = (238, 232, 218)
WHITE = (255, 255, 255)
NAVY = (18, 38, 66)
GREEN = (22, 120, 60)
ORANGE = (200, 110, 10)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, width):
    """Greedy word wrap into lines fitting width (pixels)."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, fill, width, lh, max_lines=None):
    lines = wrap(draw, text, font, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def tag(draw, x, y, label):
    """Small REPORTED / CLAIM / FORECAST pill. Returns width used."""
    colors = {"REPORTED": GREEN, "CLAIM": ORANGE, "FORECAST": BLUE}
    col = colors.get(label, GREY)
    f = F(SANS_B, 8)
    w = int(draw.textlength(label, font=f)) + 10
    draw.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=col)
    draw.text((x + 5, y + 2), label, font=f, fill=WHITE)
    return w


# ---------------------------------------------------------------- heroes
def draw_flags(draw, x, y, w):
    """Three flags hanging on the wall behind the table (no poles)."""
    # US flag (stripes + blue canton)
    fx, fy = x + w * 0.22 - 26, y + 2
    for s in range(7):
        draw.rectangle([fx, fy + s * 4, fx + 52, fy + s * 4 + 4],
                       fill=RED if s % 2 == 0 else WHITE)
    draw.rectangle([fx, fy, fx + 22, fy + 16], fill=NAVY)
    # China flag
    fx = x + w * 0.5 - 26
    draw.rectangle([fx, y + 2, fx + 52, y + 30], fill=(222, 41, 16))
    draw.regular_polygon((fx + 12, y + 12, 5), 5, fill=(255, 222, 0))
    # Russia flag
    fx = x + w * 0.78 - 26
    draw.rectangle([fx, y + 2, fx + 52, y + 11], fill=WHITE)
    draw.rectangle([fx, y + 11, fx + 52, y + 20], fill=BLUE)
    draw.rectangle([fx, y + 20, fx + 52, y + 30], fill=RED)


def draw_table(draw, x, y, w, h):
    """Three seated figures in suits behind a conference table."""
    # figures (heads + torsos; the table covers their lower half)
    for i, cx in enumerate([x + w * 0.22, x + w * 0.5, x + w * 0.78]):
        suit = [NAVY, (40, 40, 40), (90, 30, 30)][i]
        tie = [RED, GOLD, NAVY][i]
        draw.ellipse([cx - 11, y + 8, cx + 11, y + 30], fill=(232, 190, 160))
        draw.rectangle([cx - 18, y + 30, cx + 18, y + 62], fill=suit)
        draw.polygon([(cx - 5, y + 30), (cx + 5, y + 30), (cx, y + 42)],
                     fill=WHITE)
        draw.rectangle([cx - 2, y + 32, cx + 2, y + 50], fill=tie)
    # table: trapezoid top surface + front face
    draw.polygon([(x + 8, y + 58), (x + w - 8, y + 58),
                  (x + w - 2, y + h), (x + 2, y + h)], fill=(196, 141, 90))
    draw.polygon([(x + 8, y + 58), (x + w - 8, y + 58),
                  (x + w - 14, y + 66), (x + 14, y + 66)], fill=(222, 178, 120))
    # name plates + microphones on the table
    for cx in [x + w * 0.22, x + w * 0.5, x + w * 0.78]:
        draw.rectangle([cx - 14, y + 60, cx + 14, y + 68], fill=WHITE)
        draw.line([cx + 18, y + 60, cx + 24, y + 50], fill=INK, width=2)
        draw.ellipse([cx + 22, y + 47, cx + 27, y + 52], fill=INK)


def draw_skyline(draw, x, y, w, h):
    """Vice City sunset: orange-purple sky, dark skyline, sun, palm."""
    for i in range(h):
        t = i / h
        r = int(120 + 110 * t)
        g = int(60 + 60 * t)
        b = int(140 - 60 * t)
        draw.line([x, y + i, x + w, y + i], fill=(r, g, b))
    draw.ellipse([x + 105, y + 8, x + 145, y + 48], fill=(255, 214, 120))
    buildings = [(0, 58, 34, 100), (40, 42, 26, 100), (72, 66, 30, 100),
                 (108, 38, 24, 100), (138, 58, 30, 100), (174, 46, 26, 100),
                 (206, 64, 28, 100), (240, 40, 26, 100), (272, 60, 30, 100)]
    for bx, by, bw, bh in buildings:
        draw.rectangle([x + bx, y + by, x + bx + bw, y + h], fill=(38, 20, 60))
        for wy in range(y + by + 8, y + h - 6, 12):
            draw.rectangle([x + bx + 5, wy, x + bx + 9, wy + 5], fill=(255, 220, 130))
    # palm silhouette left
    draw.line([x + 18, y + h, x + 26, y + h - 34], fill=(20, 40, 20), width=4)
    for dx, dy in [(-16, -6), (-12, -14), (14, -8), (18, -16), (0, -18)]:
        draw.line([x + 26, y + h - 34, x + 26 + dx, y + h - 34 + dy],
                  fill=(20, 40, 20), width=3)
    draw.rounded_rectangle([x + w - 62, y + 6, x + w - 8, y + 30], radius=4,
                           fill=(17, 17, 17))
    draw.text((x + w - 52, y + 10), "VI", font=F(SANS_B, 18), fill=WHITE)


def draw_chart(draw, x, y, w, h):
    """ANT candlestick chart climbing to $83 on dark green."""
    draw.rectangle([x, y, x + w, y + h], fill=(10, 60, 40))
    candles = [(14, 78, 66, 1), (48, 70, 58, 1), (82, 74, 60, 0),
               (116, 58, 44, 1), (150, 62, 48, 0), (184, 44, 30, 1),
               (218, 36, 22, 1), (252, 26, 14, 1)]
    for cx, top, bot, up in candles:
        col = (60, 200, 120) if up else (220, 80, 80)
        lo, hi = min(top, bot), max(top, bot)
        draw.line([x + cx + 8, y + lo - 8, x + cx + 8, y + hi + 8],
                  fill=col, width=2)
        draw.rectangle([x + cx, y + lo, x + cx + 16, y + hi], fill=col)
    pts = [(x + 22, y + 84), (x + 90, y + 66), (x + 158, y + 58),
           (x + 226, y + 38), (x + 294, y + 20)]
    draw.line(pts, fill=(255, 214, 120), width=3, joint="curve")
    draw.text((x + 34, y + 8), "ANT  ·  NASDAQ", font=F(SANS_B, 13), fill=(180, 230, 200))
    draw.text((x + w - 96, y + h - 38), "$83", font=F(SANS_B, 28), fill=(255, 214, 120))


# ------------------------------------------------------------------- page
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 24
CW = W - 2 * MX  # 976

# top line
d.text((MX, 8), "THE WORLD IN ONE DAY", font=F(SANS_B, 15), fill=RED)
d.text((MX + CW - d.textlength("37 STORIES  •  7 REGIONS  •  ONE PAGE",
       font=F(SANS_B, 12)), 10),
       "37 STORIES  •  7 REGIONS  •  ONE PAGE", font=F(SANS_B, 12), fill=GREY)
d.line([MX, 30, MX + CW, 30], fill=INK, width=2)

# masthead
d.text((MX, 34), "Thursday 19 November 2026", font=F(SERIF_B, 52), fill=INK)
# calendar box
d.rectangle([902, 34, 1000, 100], outline=RED, width=2)
d.rectangle([902, 34, 1000, 52], fill=RED)
d.text((902 + (98 - d.textlength("NOVEMBER 2026", font=F(SANS_B, 10))) / 2, 38),
       "NOVEMBER 2026", font=F(SANS_B, 10), fill=WHITE)
d.text((902 + (98 - d.textlength("19", font=F(SERIF_B, 30))) / 2, 54),
       "19", font=F(SERIF_B, 30), fill=INK)
d.text((902 + (98 - d.textlength("THURSDAY", font=F(SANS_B, 9))) / 2, 86),
       "THURSDAY", font=F(SANS_B, 9), fill=GREY)

# red deck line
d.text((MX, 104),
       "Trump, Xi and Putin share one table  ·  GTA VI ends a 13-year wait  ·  World Court finds genocide in Myanmar",
       font=F(SERIF_I, 16), fill=RED)

# stats strip
STATS = [
    ("3", "presidents, one table:\nUS, China, Russia"),
    ("$81.3bn", "raised by Anthropic,\na record IPO"),
    ("13 yrs", "wait for GTA VI ends\nat midnight"),
    ("551,864", "sit South Korea's\ncollege exam"),
    ("200,000", "listed to evacuate\nas Cyclone Akvan nears"),
    ("730,000", "Rohingya who fled\nMyanmar in 2017"),
]
sx = MX
sw = CW // 6
for num, cap in STATS:
    d.text((sx + 4, 126), num, font=F(SANS_B, 24), fill=RED)
    for i, line in enumerate(cap.split("\n")):
        d.text((sx + 4, 154 + i * 12), line, font=F(SANS, 10), fill=INK)
    sx += sw
d.line([MX, 182, MX + CW, 182], fill=GREY, width=1)

# region bar (counts computed from the story list below)
REGIONS = [("ASIA-PACIFIC", 11, (185, 28, 28)),
           ("EUROPE", 7, (29, 78, 216)),
           ("AMERICAS", 7, (22, 120, 60)),
           ("MIDDLE EAST", 5, (200, 110, 10)),
           ("AFRICA", 3, (120, 80, 160)),
           ("OCEANIA", 2, (15, 118, 110)),
           ("WORLD", 2, (90, 90, 90))]
total_reg = sum(c for _, c, _ in REGIONS)
rx = MX
for name, count, col in REGIONS:
    wseg = int(CW * count / total_reg)
    d.rectangle([rx, 190, rx + wseg - 1, 208], fill=col)
    label = f"{name} {count}"
    fnt = F(SANS_B, 9)
    if d.textlength(label, font=fnt) <= wseg - 6:
        d.text((rx + (wseg - d.textlength(label, font=fnt)) / 2, 195),
               label, font=fnt, fill=WHITE)
    rx += wseg

# heroes: 3 illustrated stories
HEROES = [
    dict(num="1", kicker="SHENZHEN  •  SUMMIT", tag="REPORTED",
         head="Trump, Xi and Putin hold first three-way summit",
         deck="Three nuclear powers meet at APEC; arms control and the Iran war top the agenda. The Shenzhen Declaration is adopted.",
         art="shenzhen"),
    dict(num="2", kicker="WORLDWIDE  •  GAMES", tag="REPORTED",
         head="GTA VI arrives after a 13-year wait",
         deck="Unlocks at midnight local time, New Zealand first. 15.9m pre-orders; $79.99 on PS5 and Xbox, no PC yet.",
         art="gta"),
    dict(num="3", kicker="NASDAQ  •  MARKETS", tag="REPORTED",
         head="Anthropic debuts in the biggest IPO on record",
         deck="Priced at $83, it raised $81.3bn and is valued near $1.5tn as ANT starts trading Thursday.",
         art="ant"),
]
hx = MX
hw = 320
for hero in HEROES:
    # illustration
    if hero["art"] == "shenzhen":
        d.rectangle([hx, 214, hx + hw, 312], fill=(168, 205, 232))
        draw_flags(d, hx + 20, 216, hw - 40)
        draw_table(d, hx + 20, 238, hw - 40, 74)
    elif hero["art"] == "gta":
        draw_skyline(d, hx, 214, hw, 98)
    else:
        draw_chart(d, hx, 214, hw, 98)
    # number badge
    d.ellipse([hx + 4, 214, hx + 26, 236], fill=RED)
    d.text((hx + 11, 218), hero["num"], font=F(SANS_B, 13), fill=WHITE)
    # kicker + tag
    d.text((hx, 316), hero["kicker"], font=F(SANS_B, 10), fill=RED)
    tag(d, hx + hw - 62, 316, hero["tag"])
    # headline + deck
    y = draw_wrapped(d, hx, 330, hero["head"], F(SERIF_B, 19), INK, hw, 22,
                     max_lines=2)
    draw_wrapped(d, hx, y + 2, hero["deck"], F(SANS, 11), INK, hw, 13,
                 max_lines=2)
    hx += hw + 8

d.line([MX, 404, MX + CW, 404], fill=INK, width=1)

# ---------------------------------------------------------------- mid grid
def icon_court(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 232, 240))
    draw.polygon([(x + 20, y + 12), (x + w - 20, y + 12), (x + w - 8, y + 24),
                  (x + 8, y + 24)], fill=(120, 120, 130))
    for i in range(4):
        cx = x + 28 + i * 42
        draw.rectangle([cx, y + 26, cx + 10, y + h - 6], fill=(90, 90, 100))
    draw.rectangle([x + 8, y + h - 6, x + w - 8, y + h - 2], fill=(90, 90, 100))


def icon_globe(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(200, 228, 240))
    draw.ellipse([x + w // 2 - 16, y + 6, x + w // 2 + 16, y + h - 6],
                 outline=BLUE, width=2, fill=(190, 225, 245))
    # meridians + equator
    draw.arc([x + w // 2 - 8, y + 6, x + w // 2 + 8, y + h - 6], 0, 360,
             fill=BLUE, width=1)
    draw.line([x + w // 2 - 16, y + h // 2, x + w // 2 + 16, y + h // 2],
              fill=BLUE, width=1)
    # landmass
    draw.ellipse([x + w // 2 - 10, y + 12, x + w // 2 + 2, y + 24],
                 fill=(60, 140, 90))
    draw.ellipse([x + w // 2 - 2, y + 28, x + w // 2 + 10, y + h - 12],
                 fill=(60, 140, 90))


def icon_cyclone(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(20, 60, 90))
    cx, cy = x + w // 2, y + h // 2
    for r in (22, 16, 10, 5):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=WHITE, width=3)
    draw.text((x + w - 52, y + 4), "RED ALERT", font=F(SANS_B, 8), fill=(255, 90, 90))


def icon_bridge(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(190, 220, 240))
    draw.line([x + 8, y + h - 14, x + w - 8, y + h - 14], fill=INK, width=3)
    for tx in (x + 46, x + w - 58):
        draw.line([tx, y + 10, tx, y + h - 14], fill=INK, width=4)
    for dx in (x + 30, x + w // 2 - 30, x + w - 42):
        draw.line([x + 46, y + 12, dx, y + h - 14], fill=INK, width=1)
        draw.line([x + w - 58, y + 12, dx, y + h - 14], fill=INK, width=1)
    draw.ellipse([x + w // 2 - 8, y + h - 24, x + w // 2 + 8, y + h - 8],
                 fill=(255, 140, 0))


def icon_tank(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(220, 210, 190))
    draw.rectangle([x + 30, y + 18, x + 110, y + 34], fill=(90, 90, 80))
    draw.rectangle([x + 100, y + 12, x + 150, y + 18], fill=(90, 90, 80))
    draw.ellipse([x + 36, y + 34, x + 48, y + 44], fill=INK)
    draw.ellipse([x + 56, y + 34, x + 68, y + 44], fill=INK)
    draw.ellipse([x + 76, y + 34, x + 88, y + 44], fill=INK)
    draw.rectangle([x + 130, y + 8, x + 150, y + 26], fill=(120, 120, 110))


def icon_rain(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(180, 205, 230))
    draw.ellipse([x + 40, y + 8, x + 80, y + 28], fill=WHITE)
    draw.ellipse([x + 65, y + 4, x + 105, y + 26], fill=WHITE)
    draw.ellipse([x + 90, y + 10, x + 125, y + 28], fill=WHITE)
    for dx in (50, 75, 100, 125):
        draw.line([x + dx, y + 32, x + dx - 4, y + 44], fill=BLUE, width=3)


def icon_exam(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(240, 230, 200))
    draw.rectangle([x + 30, y + 30, x + 140, y + 38], fill=(150, 110, 70))
    draw.rectangle([x + 60, y + 38, x + 66, y + h - 4], fill=(150, 110, 70))
    draw.rectangle([x + 130, y + 38, x + 136, y + h - 4], fill=(150, 110, 70))
    draw.ellipse([x + 78, y + 8, x + 98, y + 28], fill=(232, 190, 160))
    draw.rectangle([x + 70, y + 28, x + 106, y + 32], fill=NAVY)


def icon_scales(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(230, 225, 210))
    draw.line([x + w // 2, y + 6, x + w // 2, y + h - 8], fill=INK, width=3)
    draw.line([x + 30, y + 14, x + w - 30, y + 14], fill=INK, width=3)
    for sx in (30, w - 30):
        draw.line([x + sx, y + 14, x + sx - 12, y + 32], fill=INK, width=2)
        draw.line([x + sx, y + 14, x + sx + 12, y + 32], fill=INK, width=2)
        draw.arc([x + sx - 12, y + 26, x + sx + 12, y + 40], 0, 180,
                 fill=GOLD, width=3)


def icon_strike(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(250, 240, 180))
    draw.rectangle([x + 30, y + 8, x + 150, y + 22], fill=(255, 220, 0))
    draw.text((x + 38, y + 10), "PARO  NACIONAL", font=F(SANS_B, 11), fill=INK)
    for i, cx in enumerate([50, 80, 110, 140]):
        draw.ellipse([x + cx - 8, y + 28, x + cx + 8, y + 44], fill=(200, 150, 120))
        draw.rectangle([x + cx - 10, y + 44, x + cx + 10, y + h - 4],
                       fill=[NAVY, RED, TEAL, GOLD][i])


def icon_chart(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(230, 240, 230))
    bars = [(30, 30), (60, 22), (90, 34), (120, 14), (150, 26)]
    for bx, bh in bars:
        draw.rectangle([x + bx, y + h - 8 - bh, x + bx + 18, y + h - 8],
                       fill=RED)
    draw.line([x + 20, y + h - 8, x + w - 10, y + h - 8], fill=INK, width=2)


MID = [
    dict(num="4", kicker="THE HAGUE  •  LAW", tag="REPORTED", icon="court",
         head="World Court rules 9–6: Myanmar committed genocide",
         deck="The 2017 campaign meant to destroy the Rohingya; about 10,000 were killed. Myanmar must allow return."),
    dict(num="5", kicker="ANTALYA  •  CLIMATE", tag="FORECAST", icon="globe",
         head="COP31 enters its last 48 hours",
         deck="Ministers take over the text in Antalya. The $120bn adaptation-finance goal and a fossil-fuel phase-out are still unresolved."),
    dict(num="6", kicker="ODISHA  •  STORM", tag="REPORTED", icon="cyclone",
         head="Cyclone Akvan bears down; 200,000 told to move",
         deck="Red alerts in 11 districts; nearly 50,000 evacuated. Landfall near Puri due Friday."),
    dict(num="7", kicker="SEOUL  •  EDUCATION", tag="REPORTED", icon="exam",
         head="Half a million sit Korea's Suneung",
         deck="551,864 take the college exam; flights pause for the listening test amid an AI-cheating crackdown."),
    dict(num="8", kicker="CRIMEA  •  WAR", tag="REPORTED", icon="bridge",
         head="Crimean Bridge hit for third time in a week",
         deck="The rail section was targeted overnight and traffic halted, Russian-installed officials said."),
    dict(num="9", kicker="GAZA  •  WAR", tag="REPORTED", icon="tank",
         head="Israeli armour pushes into central Gaza",
         deck="Tanks and bulldozers move toward Salah al-Din Street, past the Yellow Line. Hamas calls it a breach."),
    dict(num="10", kicker="FLORIDA  •  WEATHER", tag="REPORTED", icon="rain",
         head="Flooded South Florida logs 300+ rescues",
         deck="Up to 15.3 inches of rain fell in a day; Broward closed schools a second day as more rain is forecast."),
    dict(num="11", kicker="JAKARTA  •  LAW", tag="REPORTED", icon="scales",
         head="Indonesia passes asset-seizure law",
         deck="After an 18-year wait, the state may seize assets worth Rp1bn or more without a conviction."),
    dict(num="12", kicker="BOGOTÁ  •  LABOUR", tag="REPORTED", icon="strike",
         head="Colombia's unions hold a national strike",
         deck="Teachers and workers march in Bogotá, Medellín and Cali against the government's tax bill."),
    dict(num="13", kicker="CANBERRA  •  ECONOMY", tag="REPORTED", icon="chart",
         head="Australia's jobless rate jumps to 4.9%",
         deck="A five-year high, up from 4.7%. The economy lost 4,700 jobs; a gain of 25,000 was forecast."),
]
ICONS = {"court": icon_court, "globe": icon_globe, "cyclone": icon_cyclone,
         "bridge": icon_bridge, "tank": icon_tank, "rain": icon_rain,
         "exam": icon_exam, "scales": icon_scales, "strike": icon_strike,
         "chart": icon_chart}

cell_w = (CW - 4 * 8) // 5
for idx, story in enumerate(MID):
    row, col = divmod(idx, 5)
    cx = MX + col * (cell_w + 8)
    cy = 410 + row * 138
    ICONS[story["icon"]](d, cx, cy, cell_w, 52)
    d.ellipse([cx + 2, cy + 2, cx + 20, cy + 20], fill=RED)
    d.text((cx + 8, cy + 5), story["num"], font=F(SANS_B, 11), fill=WHITE)
    d.text((cx, cy + 56), story["kicker"], font=F(SANS_B, 9), fill=RED)
    tag(d, cx + cell_w - 58, cy + 55, story["tag"])
    y = draw_wrapped(d, cx, cy + 70, story["head"], F(SERIF_B, 13), INK,
                     cell_w, 15, max_lines=2)
    draw_wrapped(d, cx, y + 1, story["deck"], F(SANS, 10), INK, cell_w, 12,
                 max_lines=3)

# ------------------------------------------------------------------- bottom
d.line([MX, 690, MX + CW, 690], fill=INK, width=1)

# world map
d.text((MX, 694), "WHERE IT HAPPENED", font=F(SANS_B, 11), fill=INK)
map_x, map_y, map_w, map_h = MX, 710, 276, 196
d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=NAVY)
CONTINENTS = [
    [(0.02, 0.18), (0.12, 0.06), (0.28, 0.04), (0.36, 0.12), (0.30, 0.28),
     (0.22, 0.34), (0.10, 0.30), (0.04, 0.24)],
    [(0.24, 0.42), (0.32, 0.40), (0.36, 0.50), (0.30, 0.66), (0.25, 0.60),
     (0.22, 0.50)],
    [(0.46, 0.10), (0.54, 0.06), (0.58, 0.14), (0.54, 0.20), (0.47, 0.18)],
    [(0.47, 0.28), (0.57, 0.26), (0.61, 0.38), (0.57, 0.54), (0.51, 0.50),
     (0.47, 0.38)],
    [(0.60, 0.06), (0.78, 0.03), (0.92, 0.08), (0.96, 0.16), (0.88, 0.28),
     (0.76, 0.30), (0.64, 0.24), (0.59, 0.14)],
    [(0.80, 0.56), (0.90, 0.53), (0.94, 0.60), (0.88, 0.66), (0.81, 0.62)],
]
for poly in CONTINENTS:
    pts = [(map_x + fx * map_w, map_y + fy * map_h) for fx, fy in poly]
    d.polygon(pts, fill=(210, 190, 150))
PINS = {"1": (0.86, 0.26), "2": (0.94, 0.72), "3": (0.24, 0.18),
        "4": (0.47, 0.10), "5": (0.53, 0.19), "6": (0.76, 0.30),
        "7": (0.89, 0.16), "8": (0.59, 0.12), "9": (0.62, 0.26),
        "10": (0.22, 0.28), "11": (0.80, 0.42), "12": (0.27, 0.46),
        "13": (0.88, 0.60)}
for num, (fx, fy) in PINS.items():
    px, py = map_x + fx * map_w, map_y + fy * map_h
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=WHITE)
    d.text((px - 3, py - 5), num, font=F(SANS_B, 8), fill=WHITE)
for fx, fy in [(0.52, 0.15), (0.50, 0.11), (0.79, 0.38), (0.30, 0.44),
               (0.53, 0.48), (0.90, 0.58)]:
    px, py = map_x + fx * map_w, map_y + fy * map_h
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(160, 160, 160))
d.text((MX, 910), "Red pins: stories 1–13. Grey pins: briefs below.",
       font=F(SANS, 9), fill=GREY)

# ALSO briefs (24 one-liners, stories 14-37)
BRIEFS = [
    ("14", "KYIV", "Zelensky: 'No talks about Ukraine without Ukraine.'"),
    ("15", "PARIS", "Mélenchon could win, minister concedes."),
    ("16", "JAZAN", "Saudi all-clear after Houthi alerts."),
    ("17", "BENGHAZI", "Cocaine and pills seized in Libya's biggest haul."),
    ("18", "MEXICO CITY", "Banxico minutes: 3-2 vote to cut rates to 6.25%."),
    ("19", "MOGADISHU", "Somalia accuses the UAE of secret military bases."),
    ("20", "FRANKFURT", "Deutsche Bank's $582m Epstein-linked deals."),
    ("21", "WASHINGTON", "Senators warn of AI cyber threats at a hearing."),
    ("22", "OTTAWA", "Carney reviews China trade for a US deal."),
    ("23", "NEW DELHI", "Modi meets the Prince and Princess of Wales."),
    ("24", "TOKYO", "India and Japan review defence ties at 2+2 talks."),
    ("25", "BENGALURU", "Amazon pledges $7bn for renewables by 2030."),
    ("26", "SYDNEY", "Duckett's 133 puts England on top in the ODI."),
    ("27", "NAIROBI", "Kenya floods kill six as Ruto addresses the nation."),
    ("28", "CARACAS", "Hegseth signs a US-Venezuela military deal."),
    ("29", "MANAMA", "Bapco refinery back on its feet after the attacks."),
    ("30", "RIYADH", "Gulf leaders urge Trump not to strike Iran."),
    ("31", "LA PAZ", "Bolivia declares an El Niño emergency."),
    ("32", "AUCKLAND", "First to play GTA VI at midnight."),
    ("33", "PYONGYANG", "North Korea shows off an AI chatbot."),
    ("34", "DHAKA", "Yunus home burned; violence in 28 districts."),
    ("35", "SACRAMENTO", "California braces for an atmospheric river."),
    ("36", "WASHINGTON", "Vance: no 'forever war' in the Gulf."),
    ("37", "KUALA LUMPUR", "Malaysia ends visa-free entry for Indians."),
]
d.text((312, 694), "ALSO ON THURSDAY 19 NOVEMBER — 24 MORE STORIES",
       font=F(SANS_B, 11), fill=RED)
for i, (num, city, text) in enumerate(BRIEFS):
    col = i // 12
    row = i % 12
    bx = 312 + col * 350
    by = 714 + row * 18
    d.text((bx, by), num, font=F(SANS_B, 10), fill=RED)
    d.text((bx + 22, by), city + " — ", font=F(SANS_B, 10), fill=INK)
    cw = d.textlength(city + " — ", font=F(SANS_B, 10))
    d.text((bx + 22 + cw, by), text, font=F(SANS, 10), fill=INK)

# legend
d.text((MX, 936),
       "HOW SURE ARE WE?   REPORTED — confirmed by named sources    •    CLAIM — one side says so, unattributed    •    FORECAST — expected, not yet happened",
       font=F(SANS_B, 9), fill=GREY)

# DATE CHECK
d.rectangle([MX, 954, MX + CW, 994], outline=RED, width=2)
draw_wrapped(d, MX + 8, 958,
             "DATE CHECK — Left off on purpose because they happened earlier: Voyager 1 crosses one light-day (Wed 18 Nov) · Van Gogh sells for $190.4m (Wed 18) · EU's €45bn Ukraine loan plan (Wed 18) · Jeffries nominated Speaker 251–11 (Wed 18) · Pew: Islam largest faith by 2035 (Wed 18) · US strike on Qeshm island (Tue 17) · Nature's “missing billion years” (4 Nov).",
             F(SANS, 10), INK, CW - 16, 13, max_lines=2)

# footer
d.text((MX, 1000),
       "Every story here happened, or was first reported, on Thursday 19 November 2026, in some time zone. Disputed claims are attributed, not stated as fact.",
       font=F(SANS, 9), fill=GREY)
d.text((MX, 1012),
       "Sources: Reuters, AP, AFP, BBC, DW, NYT, IMD, ICJ, Yonhap, FT, 38 North.  Original drawings.",
       font=F(SANS, 9), fill=GREY)

img.save("entry.png")
print("wrote entry.png", img.size)
