#!/usr/bin/env python3
"""Draw a dense one-page broadsheet of Wednesday 25 November 2026 world news.

Writes /output/entry.png (1024x1024). Deterministic: no network, no clock,
no randomness, so two runs produce identical bytes.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (247, 243, 234)
INK = (20, 20, 20)
MUTED = (92, 86, 76)
RED = (176, 42, 30)
BLUE = (29, 78, 137)
TEAL = (23, 107, 107)
GOLD = (176, 120, 20)
LINE = (196, 188, 170)
PAPER = (255, 253, 248)

HERE = os.path.dirname(os.path.abspath(__file__))
SERIF_B = os.path.join(HERE, "fonts", "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(HERE, "fonts", "DejaVuSerif.ttf")
SANS = os.path.join(HERE, "fonts", "DejaVuSans.ttf")
SANS_B = os.path.join(HERE, "fonts", "DejaVuSans-Bold.ttf")
SANS_C = os.path.join(HERE, "fonts", "NotoSans-Condensed.ttf")
SANS_CB = os.path.join(HERE, "fonts", "NotoSans-CondensedBold.ttf")


def F(path, size):
    return ImageFont.truetype(path, int(size))


def wrap(d, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, width, text, fnt, fill=INK, leading=1.12, max_lines=None):
    lines = wrap(d, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    lh = int(fnt.size * leading)
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def tag(d, x, y, text, fill):
    fnt = F(SANS_CB, 10)
    w = int(d.textlength(text, font=fnt)) + 8
    d.rectangle([x, y, x + w, y + 14], outline=fill, width=1)
    d.text((x + 4, y + 1), text, font=fnt, fill=fill)
    return x + w


def scene_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(203, 224, 238))
    d.ellipse([x + 12, y + 8, x + 34, y + 30], fill=(250, 205, 90))
    for gx, gy in [(70, 12), (96, 20), (150, 10)]:
        d.arc([x + gx, y + gy, x + gx + 12, y + gy + 7], 200, 340, fill=(90, 110, 130), width=1)
        d.arc([x + gx + 10, y + gy, x + gx + 22, y + gy + 7], 200, 340, fill=(90, 110, 130), width=1)
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(70, 130, 180))
    for wx in range(x + 8, x + w - 10, 26):
        d.arc([wx, y + h - 16, wx + 18, y + h - 6], 0, 180, fill=(200, 225, 245), width=1)
    hull_y = y + h - 32
    d.polygon([(x + 14, hull_y), (x + w - 20, hull_y), (x + w - 38, hull_y + 14), (x + 30, hull_y + 14)], fill=(32, 32, 40))
    d.rectangle([x + 14, hull_y - 3, x + w - 20, hull_y], fill=(176, 42, 30))
    rows = [[(176, 42, 30), (29, 78, 137), (23, 107, 107), (176, 120, 20), (90, 90, 140)],
            [(29, 78, 137), (176, 120, 20), (176, 42, 30), (23, 107, 107), (120, 70, 130)]]
    labels = ["EU", "CHINA", "JAPAN", "KOREA", "VIETNAM"]
    for r in range(2):
        cx = x + 26
        for i in range(5):
            top = hull_y - 16 - r * 13
            d.rectangle([cx, top, cx + 36, top + 11], fill=rows[r][i], outline=(20, 20, 20), width=1)
            if r == 1:
                d.text((cx + 3, top + 1), labels[i], font=F(SANS_CB, 7.5), fill=(255, 255, 255))
            cx += 40
    d.rectangle([x + w - 52, hull_y - 34, x + w - 36, hull_y - 3], fill=(240, 240, 235))
    d.rectangle([x + w - 50, hull_y - 30, x + w - 38, hull_y - 24], fill=(70, 130, 180))
    d.line([(x + w - 44, hull_y - 34), (x + w - 44, hull_y - 44)], fill=INK, width=1)
    # port crane behind
    d.line([(x + 8, hull_y - 4), (x + 8, y + 26)], fill=(60, 70, 90), width=3)
    d.line([(x + 8, y + 26), (x + 120, y + 26)], fill=(60, 70, 90), width=3)
    d.line([(x + 96, y + 26), (x + 96, y + 38)], fill=(60, 70, 90), width=1)
    d.ellipse([x + w - 64, y + 6, x + w - 12, y + 38], fill=(176, 42, 30))
    d.text((x + w - 58, y + 12), "20%", font=F(SANS_B, 15), fill=(255, 255, 255))
    d.text((x + 8, y + h - 13), "TARIFFS ON 14 PARTNERS", font=F(SANS_CB, 9), fill=(255, 255, 255))


def scene_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 34, 48))
    for gy in range(y + 14, y + h - 8, 14):
        d.line([(x + 8, gy), (x + w - 8, gy)], fill=(70, 64, 92), width=1)
    for gx in range(x + 30, x + w - 8, 34):
        d.line([(gx, y + 8), (gx, y + h - 8)], fill=(56, 50, 76), width=1)
    pts = [(0.05, 0.30), (0.20, 0.38), (0.32, 0.30), (0.45, 0.48), (0.58, 0.42), (0.72, 0.62), (0.85, 0.72), (0.96, 0.82)]
    xy = [(x + int(px * w), y + int(py * h)) for px, py in pts]
    d.polygon(xy + [(x + w - 6, y + h - 6), (x + 10, y + h - 6)], fill=(90, 44, 54))
    d.line(xy, fill=(240, 90, 80), width=3)
    for px, py in xy[::2]:
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))
    d.rectangle([x + 14, y + 10, x + 52, y + 40], outline=(240, 200, 90), width=2)
    d.text((x + 22, y + 17), "AI", font=F(SANS_B, 15), fill=(240, 200, 90))
    rows = [("KOSPI", "-6.2%"), ("SK HYNIX", "-11.1%"), ("SAMSUNG", "-9.9%"), ("TAIEX", "-4.8%"), ("NIKKEI", "-2.8%")]
    ry = y + 8
    for name, val in rows:
        d.text((x + w - 128, ry), name, font=F(SANS_CB, 10), fill=(200, 200, 215))
        d.polygon([(x + w - 62, ry + 2), (x + w - 54, ry + 2), (x + w - 58, ry + 8)], fill=(240, 90, 80))
        d.text((x + w - 50, ry), val, font=F(SANS_CB, 11), fill=(255, 255, 255))
        ry += 13
    d.text((x + 14, y + h - 24), "4,697.51", font=F(SANS_B, 16), fill=(255, 255, 255))
    d.text((x + 92, y + h - 20), "ASIA CLOSE · WED 25 NOV", font=F(SANS_CB, 9), fill=(200, 200, 215))


def scene_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 34, 64))
    for sx, sy in [(20, 14), (60, 30), (110, 12), (170, 24), (230, 14), (270, 34), (140, 40), (40, 44)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    import math
    ecx, ecy, erx, ery = x + w / 2, y + h + 34, w / 2 + 46, 58
    arc = []
    for t in range(0, 181, 6):
        a = math.radians(180 + t)
        px, py = ecx + erx * math.cos(a), ecy + ery * math.sin(a)
        arc.append((px, min(py, y + h)))
    d.polygon(arc + [(x + w, y + h), (x, y + h)], fill=(60, 120, 190))
    d.ellipse([x + 30, y + h - 12, x + 90, y + h - 1], fill=(90, 160, 90))
    d.ellipse([x + 150, y + h - 9, x + 210, y + h - 1], fill=(90, 160, 90))
    rx = x + 56
    d.polygon([(rx, y + 10), (rx + 11, y + 36), (rx + 11, y + 60), (rx - 11, y + 60), (rx - 11, y + 36)], fill=(240, 240, 235))
    d.rectangle([rx - 11, y + 46, rx + 11, y + 52], fill=(176, 42, 30))
    d.ellipse([rx - 5, y + 26, rx + 5, y + 36], fill=(29, 78, 137))
    d.polygon([(rx - 11, y + 60), (rx - 20, y + 70), (rx - 11, y + 70)], fill=(200, 200, 200))
    d.polygon([(rx + 11, y + 60), (rx + 20, y + 70), (rx + 11, y + 70)], fill=(200, 200, 200))
    d.polygon([(rx - 6, y + 60), (rx + 6, y + 60), (rx, y + 80)], fill=(240, 140, 40))
    d.polygon([(rx - 3, y + 60), (rx + 3, y + 60), (rx, y + 72)], fill=(250, 200, 80))
    sx = x + w - 118
    d.rectangle([sx, y + 30, sx + 66, y + 41], fill=(200, 205, 215))
    d.rectangle([sx + 26, y + 20, sx + 40, y + 30], fill=(200, 205, 215))
    for px0 in (sx - 36, sx + 70):
        d.rectangle([px0, y + 25, px0 + 30, y + 46], fill=(70, 130, 180))
        for lx in range(px0 + 6, px0 + 30, 8):
            d.line([(lx, y + 25), (lx, y + 46)], fill=(40, 80, 120), width=1)
    d.line([(rx + 14, y + 34), (sx - 38, y + 34)], fill=(200, 200, 200), width=1)
    d.text((x + 8, y + 6), "LONG MARCH 2F", font=F(SANS_CB, 9), fill=(200, 200, 215))
    d.text((x + 10, y + h - 13), "SHENZHOU-24", font=F(SANS_CB, 10), fill=(255, 255, 255))
    d.text((x + w - 70, y + h - 13), "TIANGONG", font=F(SANS_CB, 10), fill=(255, 255, 255))


def mini_scene(d, x, y, w, h, kind, label):
    fills = {"bolt": (250, 225, 160), "drone": (210, 225, 240), "bill": (235, 220, 190),
             "flag": (215, 235, 220), "shirt": (240, 215, 225), "mine": (225, 210, 190),
             "fire": (245, 205, 180), "gavel": (220, 215, 235), "tanker": (245, 200, 170),
             "chip": (205, 220, 245)}
    d.rectangle([x, y, x + w, y + h], fill=fills.get(kind, (230, 230, 220)))
    cx, cy = x + w // 2, y + h // 2
    d.line([(x + 4, y + h - 5), (x + w - 4, y + h - 5)], fill=(150, 140, 120), width=1)
    if kind == "bolt":
        d.line([(cx - 26, cy + 12), (cx - 26, cy - 10)], fill=INK, width=2)
        d.line([(cx - 32, cy - 8), (cx - 20, cy - 8)], fill=INK, width=2)
        d.polygon([(cx + 4, cy - 14), (cx - 8, cy + 2), (cx - 1, cy + 2), (cx - 5, cy + 14), (cx + 9, cy - 3), (cx + 1, cy - 3)], fill=(176, 120, 20))
        d.rectangle([cx + 16, cy + 2, cx + 30, cy + 12], fill=(90, 90, 90))
        d.polygon([(cx + 14, cy + 2), (cx + 23, cy - 4), (cx + 32, cy + 2)], fill=(60, 60, 60))
    elif kind == "drone":
        for rr in (8, 13):
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(120, 150, 190))
        d.rectangle([cx - 12, cy - 3, cx + 12, cy + 3], fill=INK)
        for dx, dy in [(-16, -8), (16, -8), (-16, 8), (16, 8)]:
            d.line([(cx, cy), (cx + dx, cy + dy)], fill=INK, width=2)
            d.ellipse([cx + dx - 4, cy + dy - 2, cx + dx + 4, cy + dy + 2], outline=INK)
        d.line([(cx + 24, cy + 12), (cx + 34, cy + 2)], fill=RED, width=2)
        d.line([(cx + 34, cy + 12), (cx + 24, cy + 2)], fill=RED, width=2)
    elif kind == "bill":
        d.rectangle([cx - 34, cy + 2, cx - 18, cy + 12], fill=(240, 240, 235), outline=INK)
        d.polygon([(cx - 36, cy + 2), (cx - 26, cy - 5), (cx - 16, cy + 2)], fill=(176, 42, 30))
        d.rectangle([cx - 12, cy - 13, cx + 12, cy + 13], fill=(255, 255, 255), outline=INK)
        d.text((cx - 8, cy - 8), "£", font=F(SANS_B, 13), fill=RED)
        for ly in (cy + 2, cy + 6, cy + 10):
            d.line([(cx - 8, ly), (cx + 8, ly)], fill=(160, 160, 160), width=1)
        d.polygon([(cx + 16, cy - 8), (cx + 24, cy - 8), (cx + 20, cy - 2)], fill=RED)
        d.text((cx + 14, cy + 1), "26%", font=F(SANS_CB, 9), fill=RED)
    elif kind == "flag":
        d.line([(cx - 26, cy - 12), (cx - 26, cy + 12)], fill=INK, width=2)
        d.polygon([(cx - 26, cy - 12), (cx - 6, cy - 8), (cx - 26, cy - 4)], fill=(29, 78, 137))
        d.line([(cx + 26, cy - 12), (cx + 26, cy + 12)], fill=INK, width=2)
        d.polygon([(cx + 26, cy - 12), (cx + 6, cy - 8), (cx + 26, cy - 4)], fill=TEAL)
        d.rectangle([cx - 14, cy + 6, cx + 14, cy + 9], fill=(110, 80, 50))
        d.rectangle([cx - 8, cy - 1, cx + 8, cy + 6], fill=(255, 255, 255), outline=INK)
    elif kind == "shirt":
        d.rectangle([cx - 36, cy - 2, cx - 20, cy + 12], fill=(190, 170, 190))
        d.rectangle([cx - 34, cy - 10, cx - 29, cy - 2], fill=(150, 130, 160))
        d.polygon([(cx - 6, cy - 10), (cx - 16, cy - 4), (cx - 11, cy + 2), (cx - 11, cy + 12), (cx + 11, cy + 12), (cx + 11, cy + 2), (cx + 16, cy - 4), (cx + 6, cy - 10)], fill=(150, 70, 110))
        d.arc([cx - 5, cy - 12, cx + 5, cy - 4], 0, 180, fill=(110, 50, 80), width=2)
        d.text((cx + 16, cy - 4), "+36%", font=F(SANS_CB, 10), fill=(110, 50, 80))
    elif kind == "mine":
        d.polygon([(cx - 22, cy + 12), (cx - 4, cy - 12), (cx + 14, cy + 12)], fill=(120, 95, 60))
        d.rectangle([cx - 8, cy + 2, cx, cy + 12], fill=(40, 30, 20))
        d.rectangle([cx + 6, cy + 6, cx + 30, cy + 12], fill=(70, 130, 180))
        d.arc([cx + 8, cy + 4, cx + 20, cy + 10], 0, 180, fill=(200, 225, 245), width=1)
        d.text((cx + 16, cy - 10), "100m", font=F(SANS_CB, 9), fill=INK)
    elif kind == "fire":
        d.rectangle([cx - 30, cy - 6, cx - 16, cy + 12], fill=(200, 190, 175))
        d.rectangle([cx - 27, cy - 3, cx - 23, cy + 1], fill=(90, 90, 90))
        d.rectangle([cx - 21, cy + 3, cx - 17, cy + 7], fill=(90, 90, 90))
        d.polygon([(cx, cy - 15), (cx + 9, cy + 4), (cx + 4, cy + 12), (cx - 4, cy + 12), (cx - 9, cy + 4)], fill=(220, 90, 30))
        d.polygon([(cx, cy - 6), (cx + 5, cy + 5), (cx - 5, cy + 5)], fill=(250, 180, 60))
        d.ellipse([cx + 14, cy - 12, cx + 24, cy - 4], fill=(120, 115, 110))
        d.ellipse([cx + 20, cy - 8, cx + 28, cy - 2], fill=(150, 145, 140))
    elif kind == "gavel":
        d.line([(cx, cy - 12), (cx, cy + 8)], fill=INK, width=2)
        d.line([(cx - 18, cy - 8), (cx + 18, cy - 8)], fill=INK, width=2)
        d.polygon([(cx - 24, cy - 2), (cx - 12, cy - 2), (cx - 18, cy + 4)], outline=INK)
        d.polygon([(cx + 12, cy - 2), (cx + 24, cy - 2), (cx + 18, cy + 4)], outline=INK)
        d.rectangle([cx - 14, cy + 10, cx + 14, cy + 13], fill=INK)
    elif kind == "tanker":
        d.rectangle([cx - 24, cy - 4, cx + 8, cy + 5], fill=(200, 90, 40))
        d.rectangle([cx + 8, cy - 1, cx + 16, cy + 5], fill=INK)
        d.rectangle([cx + 10, cy - 4, cx + 15, cy - 1], fill=(70, 130, 180))
        for dx in (-16, 6):
            d.ellipse([cx + dx - 4, cy + 5, cx + dx + 4, cy + 13], fill=INK)
        d.polygon([(cx - 8, cy - 14), (cx - 2, cy - 5), (cx - 5, cy - 4), (cx - 11, cy - 5)], fill=(220, 90, 30))
        d.ellipse([cx + 2, cy - 13, cx + 12, cy - 6], fill=(120, 115, 110))
    elif kind == "chip":
        d.rectangle([cx - 11, cy - 11, cx + 11, cy + 11], fill=(29, 78, 137))
        d.rectangle([cx - 5, cy - 5, cx + 5, cy + 5], fill=(160, 200, 240))
    d.text((x + 5, y + 3), label, font=F(SANS_CB, 10), fill=INK)


def lead(d, x, y, w, scene, kick, tg, headline, summary, why):
    scene(d, x, y, w, 86)
    cy = y + 92
    d.text((x, cy), kick.upper(), font=F(SANS_CB, 11.5), fill=RED)
    tag(d, x + w - 62, cy - 1, tg, BLUE if tg == "REPORTED" else TEAL)
    cy = block(d, x, cy + 17, w, headline, F(SERIF_B, 17), leading=1.06, max_lines=3)
    cy = block(d, x, cy + 2, w, summary, F(SANS_C, 12), fill=MUTED, leading=1.12, max_lines=3)
    block(d, x, cy + 2, w, f"WHY IT MATTERS  {why}", F(SANS_C, 11), fill=(52, 48, 42), leading=1.1, max_lines=2)


def card(d, x, y, w, h, kind, label, kick, headline, summary, source, sure):
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=LINE, width=1)
    mini_scene(d, x + 1, y + 1, w - 2, 34, kind, label)
    cy = y + 40
    d.text((x + 7, cy), kick.upper(), font=F(SANS_CB, 9.5), fill=RED)
    d.text((x + w - 14, cy), sure, font=F(SANS_CB, 9.5), fill=BLUE)
    cy = block(d, x + 7, cy + 13, w - 14, headline, F(SERIF_B, 12.5), leading=1.05, max_lines=3)
    block(d, x + 7, cy + 1, w - 14, summary, F(SANS_C, 10.5), fill=MUTED, leading=1.1, max_lines=2)
    d.text((x + 7, y + h - 14), source, font=F(SANS_C, 9), fill=(120, 112, 98))


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 232), outline=LINE, width=1)
    land = (205, 200, 175)
    # continent outlines as (lon, lat) polygons, equirectangular projection
    continents = [
        [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66), (-80, 62), (-78, 58),
         (-85, 55), (-92, 57), (-95, 50), (-89, 48), (-84, 46), (-76, 44), (-70, 42), (-74, 39),
         (-76, 35), (-80, 32), (-81, 26), (-84, 30), (-89, 30), (-94, 29), (-97, 26), (-97, 22),
         (-94, 18), (-90, 14), (-83, 9), (-79, 9), (-83, 15), (-87, 16), (-92, 15), (-97, 16),
         (-102, 18), (-105, 20), (-110, 24), (-114, 29), (-117, 33), (-122, 37), (-124, 42),
         (-124, 48), (-130, 54), (-140, 60), (-152, 60), (-162, 61)],
        [(-79, 9), (-72, 12), (-64, 10), (-52, 5), (-44, -3), (-35, -8), (-39, -13), (-40, -21),
         (-48, -26), (-52, -33), (-57, -39), (-62, -41), (-65, -45), (-67, -50), (-68, -55),
         (-71, -54), (-74, -50), (-73, -44), (-73, -37), (-71, -30), (-70, -20), (-70, -15),
         (-75, -15), (-79, -8), (-81, -4), (-80, 1), (-77, 4)],
        [(-10, 36), (-2, 37), (0, 39), (3, 42), (7, 44), (10, 44), (12, 46), (14, 45), (18, 40),
         (16, 38), (19, 42), (23, 36), (23, 37), (26, 38), (27, 37), (30, 36), (36, 36), (36, 31),
         (34, 28), (32, 31), (30, 36), (27, 41), (28, 45), (30, 46), (28, 48), (24, 48), (22, 50),
         (19, 52), (21, 55), (24, 58), (21, 60), (18, 59), (12, 56), (8, 57), (8, 54), (5, 53),
         (3, 51), (0, 49), (-2, 49), (-5, 48), (-2, 44), (-9, 43), (-9, 37)],
        [(-6, 35), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (35, 28), (38, 22), (40, 15),
         (43, 12), (48, 11), (51, 12), (48, 5), (41, -2), (40, -10), (36, -18), (33, -26), (27, -34),
         (20, -35), (17, -32), (14, -22), (12, -15), (13, -10), (9, -1), (9, 4), (4, 6), (-2, 5),
         (-8, 5), (-13, 8), (-17, 15), (-17, 21), (-15, 25), (-10, 29), (-6, 33)],
        [(36, 36), (44, 38), (48, 30), (50, 26), (52, 25), (55, 24), (58, 23), (60, 25), (57, 27),
         (52, 28), (48, 30), (50, 29), (54, 26), (59, 22), (61, 25), (66, 25), (72, 20), (72, 19),
         (76, 10), (77, 8), (80, 13), (80, 15), (84, 19), (88, 22), (91, 22), (92, 21), (94, 17),
         (97, 16), (98, 10), (100, 6), (103, 1), (104, 9), (107, 12), (109, 15), (106, 20),
         (108, 21), (110, 20), (114, 22), (118, 25), (121, 28), (122, 31), (120, 34), (122, 37),
         (126, 38), (126, 41), (130, 42), (132, 43), (135, 45), (137, 46), (140, 48), (142, 50),
         (140, 52), (142, 55), (150, 60), (156, 52), (158, 53), (162, 60), (170, 66), (178, 65),
         (178, 68), (160, 70), (140, 72), (120, 73), (100, 77), (80, 73), (60, 69), (45, 68),
         (35, 65), (32, 60), (30, 55), (28, 48), (30, 46), (36, 41), (36, 36)],
        [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (130, -32), (136, -35),
         (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (151, -24), (149, -20),
         (146, -19), (142, -11), (142, -15), (141, -17), (136, -15), (135, -12), (132, -11),
         (126, -14), (122, -17), (118, -20), (114, -21)],
        [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (142, 44), (140, 42), (139, 38),
         (136, 35), (132, 33), (130, 32)],
        [(-5, 50), (-3, 53), (-5, 55), (-3, 57), (-5, 58), (-8, 55), (-6, 53), (-5, 51)],
    ]
    for poly in continents:
        pts = [(x + (lon + 180) / 360 * w, y + (90 - lat) / 180 * h) for lon, lat in poly]
        d.polygon(pts, fill=land)
    pts = [(-77, 39, "1"), (127, 37, "2"), (98, 40, "3"), (31, 50, "4"), (50, 27, "5"),
           (0, 51, "6"), (149, -35, "7"), (90, 24, "8"), (107, -7, "9"), (34, 32, "10"),
           (18, -34, "11"), (35, 32, "12"), (31, 30, "13"), (24, 13, "14"), (3, 6, "15"),
           (-99, 19, "16"), (67, 25, "17"), (114, 22, "18")]
    for lon, lat, n in pts:
        px = x + (lon + 180) / 360 * w
        py = y + (90 - lat) / 180 * h
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(255, 255, 255), outline=RED, width=1)
        tw = d.textlength(n, font=F(SANS_CB, 8))
        d.text((px - tw / 2, py - 5), n, font=F(SANS_CB, 8), fill=RED)
    d.text((x + 6, y + 4), "WHERE IT HAPPENED", font=F(SANS_CB, 10), fill=INK)
    d.text((x + 6, y + h - 14), "dots = story numbers", font=F(SANS_C, 9), fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    m = 28
    inner = W - 2 * m

    d.text((m, 14), "THE WORLD IN ONE DAY", font=F(SANS_CB, 13), fill=INK)
    right = "49 STORIES · 7 REGIONS · ALL FIRST REPORTED WEDNESDAY 25 NOVEMBER 2026"
    d.text((W - m - d.textlength(right, font=F(SANS_CB, 11)), 16), right, font=F(SANS_CB, 11), fill=MUTED)
    d.text((m, 34), "Wednesday 25 November 2026", font=F(SERIF_B, 52), fill=INK)
    d.text((m, 96), "US tariffs and the world's reply · Asian chip rout · Pakistan's first astronaut · Cairo tanker fire",
           font=F(SERIF, 15), fill=(52, 48, 42))

    # region chips
    regions = [("EUROPE 10", (176, 42, 30)), ("ASIA 7", (29, 78, 137)), ("MIDDLE EAST 6", (23, 107, 107)),
               ("AMERICAS 6", (90, 90, 140)), ("AFRICA 5", (176, 120, 20)), ("OCEANIA 3", (150, 70, 110)),
               ("WORLD 2", (92, 86, 76))]
    cx = m
    for label, col in regions:
        wch = int(d.textlength(label, font=F(SANS_CB, 11))) + 14
        d.rectangle([cx, 122, cx + wch, 140], fill=col)
        d.text((cx + 7, 125), label, font=F(SANS_CB, 11), fill=(255, 255, 255))
        cx += wch + 6
    d.text((m, 144), "FIELDS  War 7 · Disaster 5 · Justice 5 · Diplomacy 3 · Tech 3 · Economy 2 · Labour 2 · Markets 2 · Trade 2 · Space 1",
           font=F(SANS_C, 11.5), fill=MUTED)

    # stat strip
    stats = [("20%", "top proposed US tariff on EU, China +12"), ("-6.2%", "Kospi close, worst in AI sell-off"),
             ("+26%", "UK energy price cap from 1 January"), ("30+", "killed in Cairo tanker fire"),
             ("9 dead", "17 trapped in Java gold pit")]
    sy = 166
    sw = inner // 5
    for i, (num, cap) in enumerate(stats):
        sx = m + i * sw
        d.text((sx, sy), num, font=F(SERIF_B, 30), fill=RED if i == 1 else INK)
        block(d, sx, sy + 38, sw - 12, cap, F(SANS_C, 11), fill=MUTED, leading=1.1, max_lines=2)

    # UTC timeline
    ty = 232
    d.text((m, ty), "THE DAY IN UTC", font=F(SANS_CB, 11), fill=INK)
    events = [("00:18", "Shenzhou-24 lifts off"), ("00:30", "Australia CPI 4.9%"), ("03:56", "Shenzhou docks"),
              ("05:30", "Taiex closes -4.8%"), ("06:30", "Kospi closes -6.2%"), ("06:35", "Crew enters Tiangong"),
              ("07:00", "Ofgem: cap +26%"), ("13:30", "US GDP revised to 4.3%"), ("21:00", "Dow ends above 50,000")]
    ex = m + 92
    d.line([(ex, ty + 22), (W - m, ty + 22)], fill=LINE, width=2)
    step = (W - m - ex) // len(events)
    for i, (t, label) in enumerate(events):
        px = ex + i * step + 4
        d.ellipse([px - 3, ty + 19, px + 3, ty + 25], fill=RED)
        d.text((px - 4, ty + 2), t, font=F(SANS_CB, 10), fill=INK)
        block(d, px - 4, ty + 28, step - 4, label, F(SANS_C, 9.5), fill=MUTED, leading=1.05, max_lines=2)

    # leads
    ly = 286
    lw = (inner - 16) // 3
    lead(d, m, ly, lw, scene_ship, "1 Washington · Trade", "OFFICIAL",
         "US proposes tariffs of up to 20% on EU, China and 12 more",
         "China faces the top rate. EU 'strongly rejects the premise'; Beijing calls overcapacity 'a false issue.'",
         "Two of the top US trade partners face duties.")
    lead(d, m + lw + 8, ly, lw, scene_chart, "2 Seoul · Tokyo · Taipei · Markets", "REPORTED",
         "AI doubts sink Asian chip stocks: Kospi closes -6.2%",
         "Kospi ends at 4,697.51, SK hynix -11.1%, Samsung -9.9%. Taiwan's Taiex -4.8%, Japan's Nikkei -2.8%.",
         "Investors doubt the AI spending boom will pay off.")
    lead(d, m + 2 * (lw + 8), ly, lw, scene_rocket, "3 Jiuquan, China · Space", "OFFICIAL",
         "Pakistan's first astronaut docks at China's space station",
         "Muhammad Zeeshan Ali, 40, first foreigner on Tiangong, flew on Shenzhou-24; stays 5 to 10 days.",
         "China's station takes its first foreign astronaut.")

    # cards
    cards = [
        ("bolt", "5 REGIONS", "4 Ukraine · War", "Russian strikes kill 5, cut power in 5 regions",
         "Zaporizhzhia plant on diesel after 17th grid loss this year.", "REUTERS · AL JAZEERA", "C"),
        ("drone", "4 DRONES", "5 Ras Tanura · War", "Saudis down Houthi drones after Hodeidah strike",
         "Coalition: 4 drones destroyed, no casualties.", "AL JAZEERA · REUTERS", "C"),
        ("bill", "+26% · £2,166", "6 London · Energy", "UK energy price cap to rise 26% in January",
         "Ofgem: typical bill £1,723 to £2,166 a year.", "OFGEM", "O"),
        ("flag", "NO FOREIGN BASES", "7 Canberra · Diplomacy", "Solomon Islands signs security pact with Australia",
         "Australia a security partner; A$740m over 10 years.", "NHK · AAP", "C"),
        ("shirt", "17,500 TAKA", "8 Dhaka · Labour", "Garment workers offered higher minimum wage",
         "Wage board: 12,500 to 17,500 taka ($100 to $136).", "REDIFF · PROTHOM ALO", "C"),
        ("mine", "9 DEAD · 100m", "9 Bogor · Disaster", "9 dead, 17 still trapped in flooded gold mine",
         "Bodies pulled from the 100-metre unlicensed pit.", "AP · LA TIMES", "C"),
        ("fire", "7 KILLED", "10 Gaza City · War", "Israeli strike kills Hamas security chief",
         "Abu al-Awf, his wife and 2 daughters died in Shati.", "BBC", "R"),
        ("gavel", "RULING", "11 Cape Town · Justice", "Court lifts 'Farmgate' threat to Ramaphosa",
         "Judges void the 2022 impeachment panel report.", "AL JAZEERA · GBC", "C"),
        ("gavel", "3 CASES", "12 Jerusalem · Justice", "Judges urge rethink of Netanyahu graft charges",
         "Bribery case faces 'considerable difficulties'.", "AL-MONITOR", "R"),
        ("tanker", "30 DEAD", "13 Giza · Disaster", "Fuel tanker fire kills at least 30 near Cairo",
         "Tanker overturned and exploded on a ring road.", "ABC · BBC · TELEGRAPH", "C"),
    ]
    gy = 522
    cw = (inner - 32) // 5
    chh = 128
    for i, (kind, label, kick, head, summ, src, sure) in enumerate(cards):
        cx = m + (i % 5) * (cw + 8)
        cyy = gy + (i // 5) * (chh + 8)
        card(d, cx, cyy, cw, chh, kind, label, kick, head, summ, src, sure)

    # map + also-on
    by = gy + 2 * (chh + 8) + 4
    map_w = 330
    draw_map(d, m, by, map_w, 176)
    ax = m + map_w + 14
    d.text((ax, by), "ALSO ON WEDNESDAY 25 NOVEMBER", font=F(SANS_CB, 12), fill=INK)
    briefs = [
        "14 Pyongyang: Swiss envoy given 48 hours to leave",
        "15 Brussels: EU proposes a EUR 50bn fund on quantum tech",
        "16 London: UK warns companies of Russian sabotage threat",
        "17 Kyiv: Ukraine seeks EUR 115bn in aid for 2027",
        "18 Paris: Five arrested in case of stolen 10th-century relic",
        "19 Luxembourg: EU court orders cage-free timeline",
        "20 Jerusalem: Knesset advances bill for a 7 October inquiry",
        "21 Gaza: Amnesty urges ICC genocide probe over deaths",
        "22 Darfur: RSF drone attack kills at least 19 in Sudan",
        "23 Kuala Lumpur: Malaysia sues Google over YouTube",
        "24 Sydney: Australia's inflation jumps to 4.9% in October",
        "25 Sydney: Ex-policeman guilty of double murder",
        "26 Lagos: Nigeria's navy rescues 17 from capsized boat",
        "27 Brasilia: US also proposes 10% tariff on Embraer jets",
        "28 Washington: FCC clears SpaceX orbital data centers",
        "29 Iowa: US Army blows up 10,000 lb of lead azide",
        "30 Mississippi: Divers recover 6 plane-crash bodies",
        "31 London: Poundland collapses, 11,000 jobs at risk",
        "32 Karachi: Building collapse kills at least 3, injures 14",
        "33 Harare: Arrest warrant for Mugabe's son",
        "34 Space: Hera finds stadium-sized DART crater",
        "35 Lisbon: Champions League: Sporting 2-2 Man United",
        "36 Mexico City: Mexico protests US extradition refusal",
        "37 UN: 16 days of action on violence on women begin",
        "38 Hormuz: Two tankers hit mines and burn, Iran says",
        "39 Samara: Ukrainian drones hit two refineries ablaze",
        "40 Shenzhen: Huawei rejects US guilty verdict",
        "41 Ituri: WHO pulls staff out of Ebola zone hospital",
        "42 Tokyo: Tokyo Electron -12.5%, Advantest -12.9%",
        "43 London: Tube strike shuts Circle and Piccadilly lines",
        "44 Sanaa: Houthis shut Saudi Red Sea ports, IRGC says",
        "45 Odesa: Russian strike kills a teenager",
        "46 Washington: Hackers breached CIA-ODNI system",
        "47 Caracas: Venezuela debt $237.5bn, 242% of GDP",
        "48 Havana: WHO chief urges end to Cuba fuel blockade",
        "49 Suva: Fiji drought leaves 92 communities dry",
    ]
    colw = (W - m - ax - 16) // 3
    for i, b in enumerate(briefs):
        bx = ax + (i % 3) * (colw + 8)
        byy = by + 20 + (i // 3) * 12
        block(d, bx, byy, colw, b, F(SANS_C, 9.5), leading=1.05, max_lines=1)

    # footer
    fy = by + 184
    d.rectangle([m, fy, W - m, fy + 1], fill=INK)
    d.text((m, fy + 6), "DATE CHECK", font=F(SANS_CB, 11), fill=RED)
    block(d, m + 78, fy + 6, inner - 78,
          "Every story above happened or was first reported on Wednesday 25 November 2026. "
          "Left out as earlier news: Houthi strike on Riyadh's tallest tower (Tue 24), Hungary's PM Magyar in Kyiv (Tue 24).",
          F(SANS_C, 10.5), fill=(52, 48, 42), leading=1.1, max_lines=2)
    d.text((m, fy + 34), "HOW SURE  O official record · C confirmed by 2+ major outlets · R one outlet's reporting · Sources: Reuters, AP, Al Jazeera, BBC, France 24, CNBC, Ofgem. Every drawing original.",
           font=F(SANS_C, 10), fill=MUTED)

    out = os.environ.get("ENTRY_OUT", "/output/entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, format="PNG")


if __name__ == "__main__":
    main()
