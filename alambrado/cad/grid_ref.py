"""Sobre uma grade com coordenadas numa figura do VITA e amplia."""
import io, sys
from pathlib import Path
from PIL import Image, ImageDraw

REF = Path(r'C:\DEV\3dprint\alambrado\ref')
OUT = Path(r'C:\Users\gabri\AppData\Local\Temp\opencode')

name = sys.argv[1]
scale = int(sys.argv[2]) if len(sys.argv) > 2 else 4
step = int(sys.argv[3]) if len(sys.argv) > 3 else 50

im = Image.open(REF / f'{name}.gif').convert('RGB')
w, h = im.size
im = im.resize((w * scale, h * scale), Image.LANCZOS)
d = ImageDraw.Draw(im)
for x in range(0, w + 1, step):
    X = x * scale
    d.line([(X, 0), (X, im.height)], fill=(255, 0, 0), width=1)
    d.text((X + 2, 2), str(x), fill=(255, 0, 0))
    d.text((X + 2, im.height - 14), str(x), fill=(255, 0, 0))
for y in range(0, h + 1, step):
    Y = y * scale
    d.line([(0, Y), (im.width, Y)], fill=(0, 120, 255), width=1)
    d.text((2, Y + 2), str(y), fill=(0, 120, 255))
    d.text((im.width - 40, Y + 2), str(y), fill=(0, 120, 255))
dst = OUT / f'{name}_grid.png'
im.save(dst)
print(f'{name} {w}x{h} x{scale} step {step} -> {dst} {im.size}')
