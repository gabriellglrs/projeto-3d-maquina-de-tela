#!/usr/bin/env python3
"""Recortes ampliados adicionais (figs 15/18)."""
import os

from PIL import Image

os.makedirs("ref/zoom", exist_ok=True)
jobs = [
    ("CLF15X3.gif", "f15_left", (0.00, 0.00, 0.55, 0.60), 6),
    ("CLF15X3.gif", "f15_right", (0.45, 0.00, 1.00, 0.60), 6),
    ("CLF18X4.gif", "f18_full", (0.00, 0.00, 1.00, 1.00), 3),
    ("clf10x8.gif", "f10_tab", (0.00, 0.00, 0.55, 0.45), 8),
]
for src, name, box, z in jobs:
    im = Image.open("ref/" + src).convert("RGB")
    w, h = im.size
    c = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    c = c.resize((c.width * z, c.height * z), Image.LANCZOS)
    c.save("ref/zoom/" + name + ".png")
    print(name, c.size)
