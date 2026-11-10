"""Amplia figuras do VITA para leitura."""
from pathlib import Path

from PIL import Image

REF = Path(r"C:\DEV\3dprint\alambrado\ref")
OUT = Path(r"C:\Users\gabri\AppData\Local\Temp\opencode")
OUT.mkdir(parents=True, exist_ok=True)

import sys

for name in sys.argv[1:]:
    src = REF / f"{name}.gif"
    if not src.exists():
        print("falta", src.name)
        continue
    im = Image.open(src).convert("RGB")
    w, h = im.size
    im.resize((w * 3, h * 3), Image.LANCZOS).save(OUT / f"{name}_3x.png")
    print(f"{name}: {w}x{h} -> {OUT / (name + '_3x.png')}")
