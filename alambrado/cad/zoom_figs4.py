#!/usr/bin/env python3
"""Zoom 12x da fig. 8 (base do trem) — cantos X e V."""
from PIL import Image

im = Image.open("ref/clf8x7.gif").convert("RGB")
w, h = im.size
print("orig", im.size)
jobs = [
    ("f8_x", (0.00, 0.05, 0.45, 0.50)),
    ("f8_v", (0.55, 0.35, 1.00, 0.85)),
    ("f8_all", (0.00, 0.00, 1.00, 1.00), 6),
]
for name, box, *z in jobs:
    zoom = z[0] if z else 12
    c = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    c = c.resize((c.width * zoom, c.height * zoom), Image.LANCZOS)
    c.save(f"ref/zoom/{name}.png")
    print(name, c.size)
