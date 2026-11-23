#!/usr/bin/env python3
"""Draws the Store's generated wallpapers: flat, minimal scenes, layered
silhouettes under gradient skies.

Each style is a function of a seeded random generator, so a run always draws
the same pictures. Writes `wallpapers/<id>.jpg` (1440 x 3120) and
`wallpapers/<id>_thumb.jpg` (360 x 780) next to this folder, and prints the
catalogue entries to paste into `catalog.json`.

    python3 store/tools/make_wallpapers.py            # every style
    python3 store/tools/make_wallpapers.py ember night # just these

Needs Pillow only.
"""

import math
import random
import sys
from datetime import date
from functools import partial
from pathlib import Path

from PIL import Image, ImageDraw

W, H = 1440, 3120
THUMB = (360, 780)
SS = 2  # drawn at twice the size, then scaled down for clean edges
OUT = Path(__file__).resolve().parent.parent / "wallpapers"


def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def canvas(bg):
    img = Image.new("RGB", (W * SS, H * SS), hexc(bg))
    return img, ImageDraw.Draw(img)


def vgradient(d, stops, top=0, bottom=None):
    """Fills rows [top, bottom) with a vertical blend through [stops]."""
    bottom = H * SS if bottom is None else bottom
    span = bottom - top
    n = len(stops) - 1
    for y in range(int(top), int(bottom), SS):
        t = (y - top) / span * n
        k = min(int(t), n - 1)
        d.rectangle([0, y, W * SS, y + SS], fill=mix(stops[k], stops[k + 1], t - k))


def ridge(rng, base, height, rough, step=24):
    """A jagged skyline across the screen, by midpoint displacement."""
    pts = [base - rng.uniform(0, height), base - rng.uniform(0, height)]
    amp = height
    while len(pts) - 1 < W / step:
        nxt = []
        for a, b in zip(pts, pts[1:]):
            nxt += [a, (a + b) / 2 + rng.uniform(-amp, amp)]
        pts = nxt + [pts[-1]]
        amp *= rough
    dx = W * SS / (len(pts) - 1)
    return [(i * dx, y) for i, y in enumerate(pts)]


def fill_below(d, line, color):
    d.polygon(line + [(W * SS, H * SS), (0, H * SS)], fill=color)


def pine(d, x, base, h, color):
    """A pine: stacked triangles standing on [base], widest at the bottom."""
    w = h * 0.38
    for k in range(4):
        tier_bottom = base - h * k * 0.2
        tier_w = w * (1 - k * 0.2)
        d.polygon([(x - tier_w / 2, tier_bottom), (x + tier_w / 2, tier_bottom),
                   (x, tier_bottom - h * 0.38)], fill=color)


def birds(d, rng, cx, cy, count, size, color):
    for _ in range(count):
        x = cx + rng.uniform(-1, 1) * size * 9
        y = cy + rng.uniform(-1, 1) * size * 4
        s = size * rng.uniform(0.5, 1)
        d.line([(x - s, y - s * 0.4), (x, y), (x + s, y - s * 0.4)],
               fill=color, width=max(2, int(s * 0.25)))


def ember(rng):
    """Dusk over orange ranges fading to a dark pine forest."""
    img, d = canvas("#fbdcc4")
    vgradient(d, [hexc("#fde3cf"), hexc("#f9c8a4"), hexc("#f2a477")], 0, H * SS * 0.5)
    far, near = hexc("#f08a4b"), hexc("#7a1a3a")
    layers = 5
    for i in range(layers):
        base = H * SS * (0.40 + 0.09 * i)
        fill_below(d, ridge(rng, base, (180 - 25 * i) * SS, 0.55),
                   mix(far, near, i / (layers - 1)))
    birds(d, rng, W * SS * 0.7, H * SS * 0.36, 9, 22 * SS, hexc("#5a1a2e"))
    for row, (y, h, gap) in enumerate(((0.70, 420, 110), (0.80, 620, 150))):
        tone = mix(hexc("#4a1230"), hexc("#2b0d1f"), row)
        x = -rng.uniform(0, gap) * SS
        while x < W * SS + 100 * SS:
            pine(d, x, H * SS * y, h * SS * rng.uniform(0.7, 1.1), tone)
            x += gap * SS * rng.uniform(0.6, 1.2)
        d.rectangle([0, H * SS * y, W * SS, H * SS], fill=tone)
    return img


def summit(rng):
    """A coral sun setting behind one jagged peak, snow catching the light."""
    img, d = canvas("#1d1240")
    vgradient(d, [hexc("#1a0f3a"), hexc("#2b2a66"), hexc("#363a78")])
    r = 230 * SS
    cx, cy = W * SS * 0.5, H * SS * 0.53
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hexc("#e87a6e"))
    peak = (W * SS * 0.49, H * SS * 0.56)
    left = [(-W * SS * 0.1, H * SS * 0.78), (W * SS * 0.18, H * SS * 0.66),
            (W * SS * 0.30, H * SS * 0.64), peak]
    right = [peak, (W * SS * 0.62, H * SS * 0.60), (W * SS * 0.74, H * SS * 0.64),
             (W * SS * 0.90, H * SS * 0.70), (W * SS * 1.1, H * SS * 0.76)]
    body = left + right[1:] + [(W * SS * 1.1, H * SS), (-W * SS * 0.1, H * SS)]
    d.polygon(body, fill=hexc("#2e2340"))
    # The lit faces: jagged snow down the sunward side of each ridge.
    snow, shade = hexc("#d9d3e3"), hexc("#9a8fb0")
    for (ax, ay), (bx, by) in zip(right, right[1:]):
        for k in range(3):
            t0, t1 = k / 3, (k + 1) / 3
            p0 = (ax + (bx - ax) * t0, ay + (by - ay) * t0)
            p1 = (ax + (bx - ax) * t1, ay + (by - ay) * t1)
            tip = (p0[0] + (p1[0] - p0[0]) * rng.uniform(0.2, 0.6),
                   p0[1] + rng.uniform(120, 360) * SS)
            d.polygon([p0, p1, tip], fill=mix(snow, shade, rng.uniform(0, 0.5)))
    d.polygon([peak, (W * SS * 0.42, H * SS * 0.62), (W * SS * 0.47, H * SS * 0.60)],
              fill=hexc("#b8aecb"))
    return img


def dusk(rng):
    """Purple dunes under a low pale moon."""
    img, d = canvas("#2a1d45")
    vgradient(d, [hexc("#1c1438"), hexc("#4a2c63"), hexc("#a5577a")], 0, H * SS * 0.62)
    r = 120 * SS
    cx, cy = W * SS * 0.66, H * SS * 0.44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hexc("#f4d9c6"))
    tones = [hexc(c) for c in ("#7a3e6e", "#5d2f62", "#432552", "#2c1a3c")]
    for i, tone in enumerate(tones):
        base = H * SS * (0.58 + 0.09 * i)
        amp = (110 - 15 * i) * SS
        ph = rng.uniform(0, math.pi * 2)
        pts = [(x, base + amp * math.sin(x / (W * SS) * math.pi * (1.2 + 0.3 * i) + ph))
               for x in range(0, W * SS + 8 * SS, 8 * SS)]
        fill_below(d, pts, tone)
    return img


# Metro: one accent colour, tone-on-tone flat shapes that sit quietly under
# tiles.


def tone(c, amount):
    """[c] lightened (amount > 0) or darkened (amount < 0) toward white or
    black."""
    return mix(c, (255, 255, 255) if amount > 0 else (0, 0, 0), abs(amount))


def metro_grid(base_hex, rng):
    """A sparse Start grid, a shade lighter than the accent behind it."""
    base = hexc(base_hex)
    img, d = canvas(base_hex)
    cell, gap = 300 * SS, 24 * SS
    margin = 120 * SS
    cols = (W * SS - 2 * margin + gap) // cell
    for r in range(0, (H * SS - 2 * margin) // cell):
        for c in range(cols):
            if rng.random() < 0.55:
                continue
            # Centred: whatever width the whole cells leave over is split
            # evenly between the two sides.
            x = (W * SS - (cols * cell - gap)) / 2 + c * cell
            y = margin + r * cell
            d.rectangle([x, y, x + cell - gap, y + cell - gap],
                        fill=tone(base, rng.choice((0.05, 0.08, 0.11))))
    return img


def metro_rings(base_hex, corner, rng):
    """Concentric arcs from a corner ((1, 0) top-right, (0, 1) bottom-left)."""
    base = hexc(base_hex)
    img, d = canvas(base_hex)
    cx = W * SS * (1.05 if corner[0] else -0.05)
    cy = H * SS * (1.05 if corner[1] else -0.05)
    r = H * SS * 0.95
    k = 0
    while r > 200 * SS:
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  fill=tone(base, 0.07 if k % 2 == 0 else 0.0))
        r -= 170 * SS
        k += 1
    return img


def night(rng):
    """A starry sky and a moon over a ridge of pines."""
    img, d = canvas("#0b1430")
    vgradient(d, [hexc("#070d22"), hexc("#13214a"), hexc("#26386b")], 0, H * SS * 0.75)
    for _ in range(220):
        x, y = rng.uniform(0, W * SS), rng.uniform(0, H * SS * 0.6)
        s = rng.choice((2, 2, 3, 4)) * SS
        d.ellipse([x - s, y - s, x + s, y + s],
                  fill=mix(hexc("#dfe6ff"), hexc("#26386b"), rng.uniform(0, 0.6)))
    r = 140 * SS
    cx, cy = W * SS * 0.70, H * SS * 0.24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hexc("#f3efdf"))
    fill_below(d, ridge(rng, H * SS * 0.70, 160 * SS, 0.5), hexc("#16224a"))
    x = -rng.uniform(0, 80) * SS
    tree = hexc("#0a1029")
    while x < W * SS + 80 * SS:
        pine(d, x, H * SS * 0.80, rng.uniform(260, 520) * SS, tree)
        x += rng.uniform(50, 120) * SS
    d.rectangle([0, H * SS * 0.80, W * SS, H * SS], fill=tree)
    return img


STYLES = {
    "ember": ("Ember", ember),
    "summit": ("Summit", summit),
    "dusk": ("Dusk", dusk),
    "night": ("Night", night),
    "metro-grid": ("Grid", partial(metro_grid, "#1f3fbf")),
    "metro-rings": ("Rings", partial(metro_rings, "#d91074", (1, 0))),
    "metro-rings-amber": ("Amber rings", partial(metro_rings, "#e0a010", (0, 1))),
}


def main(ids):
    OUT.mkdir(exist_ok=True)
    today = date.today().isoformat()
    for wid in ids or STYLES:
        name, draw = STYLES[wid]
        big = draw(random.Random(wid)).resize((W, H), Image.LANCZOS)
        big.save(OUT / f"{wid}.jpg", quality=88, optimize=True)
        big.resize(THUMB, Image.LANCZOS).save(
            OUT / f"{wid}_thumb.jpg", quality=85, optimize=True)
        print(f'    {{"id": "{wid}", "name": {{"en": "{name}"}}, '
              f'"file": "wallpapers/{wid}.jpg", '
              f'"thumb": "wallpapers/{wid}_thumb.jpg", "added": "{today}"}},')


if __name__ == "__main__":
    main(sys.argv[1:])
