#!/usr/bin/env python3
"""Recortes ampliados das figuras recuperadas (para leitura de cotas)."""
import os

from PIL import Image

os.makedirs("ref/zoom", exist_ok=True)
jobs = [
    ("clf8x7.gif", "f8_topleft", (0.00, 0.00, 0.55, 0.55)),
    ("clf8x7.gif", "f8_botright", (0.45, 0.45, 1.00, 1.00)),
    ("clf9x8.gif", "f9_top", (0.25, 0.00, 1.00, 0.40)),
    ("clf9x8.gif", "f9_mid", (0.15, 0.30, 0.85, 0.75)),
    ("clf9x8.gif", "f9_bot", (0.25, 0.62, 1.00, 0.98)),
    ("clf7x7.gif", "f7_eye", (0.00, 0.00, 0.40, 0.40)),
    ("clf7x7.gif", "f7_bot", (0.55, 0.40, 1.00, 0.98)),
    ("CLF15X3.gif", "f15_yz", (0.50, 0.00, 1.00, 0.38)),
    ("CLF15X3.gif", "f15_tab", (0.00, 0.38, 0.55, 0.55)),
]
for src, name, box in jobs:
    im = Image.open("ref/" + src).convert("RGB")
    w, h = im.size
    c = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    c = c.resize((c.width * 8, c.height * 8), Image.LANCZOS)
    c.save("ref/zoom/" + name + ".png")
    print(name, c.size)
