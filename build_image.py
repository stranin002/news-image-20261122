"""Draw the 22 November 2026 world-news front page, 1024x1024 PNG.

Runs on the builder's machine (Pillow is available here). The graded
entrypoint is main.py, which only copies the finished entry.png: the
sandbox that grades it has no network and no Pillow, so this script is
the record of how the image was made, and the image ships in the repo.

Deterministic: same fonts, same sizes, same text, no timestamps, no
randomness, so two runs write byte-identical files.
"""
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")

PAPER = (247, 243, 232)
INK = (24, 24, 24)
NAVY = (27, 42, 74)
AMBER = (242, 193, 78)
TEAL = (14, 110, 110)
RUST = (168, 54, 32)
OLIVE = (96, 110, 44)
STEEL = (52, 92, 140)
PLUM = (104, 58, 112)
GREY = (92, 92, 92)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
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


def text_block(draw, x, y, text, fnt, color, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def star(draw, cx, cy, r, color):
    """A simple five-point star, drawn as one polygon."""
    import math

    pts = []
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy - rad * math.sin(ang)))
    draw.polygon(pts, fill=color)


def globe(draw, cx, cy, r, color):
    """A wireframe globe: circle, meridians and two latitude lines."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
                 outline=color, width=4)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=4)
    for dy in (-r // 2, r // 2):
        half = int((r * r - dy * dy) ** 0.5)
        draw.line([cx - half, cy + dy, cx + half, cy + dy],
                  fill=color, width=4)


def quake(draw, x, y, w, h, color):
    """A seismic zigzag across a small box."""
    pts = [(x, y + h // 2)]
    step = w // 8
    for i in range(1, 8):
        yy = y + h // 2 + (h // 2 - 6) * (1 if i % 2 else -1) * (0.4 + 0.6 * (i % 3) / 2)
        pts.append((x + i * step, yy))
    pts.append((x + w, y + h // 2))
    draw.line(pts, fill=color, width=5, joint="curve")


def ship(draw, x, y, w, color):
    """A tanker silhouette: hull, bridge, mast and two wave lines."""
    draw.polygon([(x, y + 34), (x + w, y + 34), (x + w - 14, y + 58),
                  (x + 14, y + 58)], fill=color)
    draw.rectangle([x + w // 2 - 8, y + 8, x + w // 2 + 22, y + 34], fill=color)
    draw.line([x + w // 2 + 30, y + 2, x + w // 2 + 30, y + 34],
              fill=color, width=4)
    for dy in (68, 80):
        draw.arc([x, y + dy, x + w // 3, y + dy + 14], 0, 180, fill=color, width=3)
        draw.arc([x + w // 2, y + dy, x + w, y + dy + 14], 0, 180, fill=color, width=3)


def rocket(draw, cx, y, color, s=1.0):
    """A simple rocket climbing: body, window, fins and flame."""
    x = lambda dx: cx + dx * s
    yy = lambda dy: y + dy * s
    draw.polygon([(x(-16), yy(74)), (x(16), yy(74)), (x(0), yy(0))],
                 fill=color)
    draw.rectangle([x(-16), yy(74), x(16), yy(118)], fill=color)
    draw.polygon([(x(-16), yy(118)), (x(-34), yy(140)), (x(-16), yy(128))],
                 fill=color)
    draw.polygon([(x(16), yy(118)), (x(34), yy(140)), (x(16), yy(128))],
                 fill=color)
    draw.ellipse([x(-8), yy(84), x(8), yy(100)], fill=PAPER)
    draw.polygon([(x(-10), yy(118)), (x(10), yy(118)), (x(0), yy(146))],
                 fill=AMBER)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 150], fill=NAVY)
    d.text((W // 2, 26), "THE WORLD TODAY", font=font(BOLD, 58),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 96), "SUNDAY 22 NOVEMBER 2026", font=font(BOLD, 30),
           fill=AMBER, anchor="ma")
    d.rectangle([0, 150, W, 158], fill=AMBER)

    # --- lead story: COP31 --------------------------------------------
    d.rectangle([24, 172, 1000, 496], outline=NAVY, width=3)
    d.text((48, 190), "CLIMATE  ·  ANTALYA, TÜRKİYE", font=font(BOLD, 22),
           fill=TEAL)
    y = text_block(d, 48, 224, "COP31 IN OVERTIME",
                   font(BOLD, 44), NAVY, 620, 52)
    text_block(d, 48, y + 8,
               "A new draft deal aims to avert collapse as the summit "
               "spills into a second extra day — still split over "
               "fossil fuels and money.",
               font(REG, 25), INK, 600, 32)
    d.text((48, 452), "Nearly 200 countries deadlocked; EU: a good deal or no deal.",
           font=font(BOLD, 22), fill=RUST)
    globe(d, 830, 330, 92, TEAL)

    # --- second row ----------------------------------------------------
    # Chapo Isidro, left
    d.rectangle([24, 512, 502, 744], outline=NAVY, width=2)
    d.rectangle([24, 512, 502, 556], fill=RUST)
    d.text((40, 518), "MEXICO", font=font(BOLD, 22), fill=(255, 255, 255))
    star(d, 462, 534, 16, AMBER)
    y = text_block(d, 40, 568, "FBI'S MOST WANTED, CAUGHT",
                   font(BOLD, 33), NAVY, 440, 40)
    text_block(d, 40, y + 8,
               "Fausto “El Chapo Isidro” Meza Flores arrested in a "
               "Sinaloa shootout; 11 killed as gunmen fought back.",
               font(REG, 22), INK, 440, 29)

    # Peru quake, right
    d.rectangle([522, 512, 1000, 744], outline=NAVY, width=2)
    d.rectangle([522, 512, 1000, 556], fill=OLIVE)
    d.text((538, 518), "PERU", font=font(BOLD, 22), fill=(255, 255, 255))
    y = text_block(d, 538, 568, "PERU SHAKEN: 6.8",
                   font(BOLD, 33), NAVY, 440, 40)
    text_block(d, 538, y + 8,
               "Strong quake hits Junín in the Andes and rattles Lima; "
               "residents rush into the streets. 15 injured, no deaths.",
               font(REG, 22), INK, 440, 29)
    quake(d, 928, 524, 56, 22, (255, 255, 255))

    # --- third row -----------------------------------------------------
    # Hormuz tankers, left
    d.rectangle([24, 760, 502, 956], outline=NAVY, width=2)
    d.rectangle([24, 760, 502, 800], fill=STEEL)
    d.text((40, 766), "THE GULF", font=font(BOLD, 20), fill=(255, 255, 255))
    y = text_block(d, 40, 812, "TANKERS HIT NEAR HORMUZ",
                   font(BOLD, 26), NAVY, 440, 32)
    text_block(d, 40, y + 8,
               "Two tankers struck leaving the Strait; Bahrain blames "
               "Iran for a fire at a civilian site.",
               font(REG, 21), INK, 330, 26)
    ship(d, 392, 860, 96, STEEL)

    # Ukraine, right
    d.rectangle([522, 760, 1000, 956], outline=NAVY, width=2)
    d.rectangle([522, 760, 1000, 800], fill=PLUM)
    d.text((538, 766), "UKRAINE", font=font(BOLD, 20), fill=(255, 255, 255))
    y = text_block(d, 538, 812, "UKRAINE'S BIGGEST ATTACK",
                   font(BOLD, 26), NAVY, 440, 32)
    text_block(d, 538, y + 8,
               "110 missiles, 400+ drones in one night; Zelenskyy "
               "calls Putin a “killer”.",
               font(REG, 21), INK, 330, 26)
    rocket(d, 920, 822, PLUM, 0.8)

    # --- footer --------------------------------------------------------
    d.text((W // 2, 972),
           "Also: Sparta II burns in the Gulf of Finland  ·  FBI probes "
           "crime-database hack  ·  COP32 to Addis Ababa",
           font=font(REG, 18), fill=GREY, anchor="ma")

    img.save(OUT, format="PNG")
    return OUT


if __name__ == "__main__":
    path = build()
    data = open(path, "rb").read()
    print(path, len(data), "bytes, sha256",
          hashlib.sha256(data).hexdigest()[:16])
