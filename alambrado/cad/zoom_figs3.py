#!/usr/bin/env python3
"""Zoom grande da fig. 9 (polia) para leitura da secao."""
from PIL import Image

im = Image.open("ref/clf9x8.gif").convert("RGB")
w, h = im.size
print("orig", im.size)
c = im.crop((0, 0, w, h))
c = c.resize((c.width * 12, c.height * 12), Image.LANCZOS)
c.save("ref/zoom/f9_full12x.png")
print("full", c.size)
