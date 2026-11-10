"""Cria recortes ampliados de uma figura do VITA."""
from pathlib import Path
import sys
from PIL import Image

REF = Path(r"C:\DEV\3dprint\alambrado\ref")
OUT = Path(r"C:\Users\gabri\AppData\Local\Temp\opencode")

name = sys.argv[1]
box = tuple(int(v) for v in sys.argv[2:6])   # left, top, right, bottom
scale = int(sys.argv[6]) if len(sys.argv) > 6 else 4

im = Image.open(REF / f"{name}.gif").convert("RGB")
crop = im.crop(box)
crop = crop.resize((crop.width * scale, crop.height * scale), Image.LANCZOS)
dst = OUT / f"{name}_crop.png"
crop.save(dst)
print(f"{name} size={im.size} box={box} -> {dst} {crop.size}")
