"""Recorte + grade de uma figura do VITA."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

REF = Path(r'C:\DEV\3dprint\alambrado\ref')
OUT = Path(r'C:\Users\gabri\AppData\Local\Temp\opencode')

name = sys.argv[1]
box = tuple(int(v) for v in sys.argv[2:6])
scale = int(sys.argv[6])
step = int(sys.argv[7]) if len(sys.argv) > 7 else 25

im = Image.open(REF / f'{name}.gif').convert('RGB').crop(box)
w, h = im.size
im = im.resize((w * scale, h * scale), Image.LANCZOS)
d = ImageDraw.Draw(im)
x0, y0 = box[0], box[1]
for x in range(x0 - x0 % step, box[2] + 1, step):
    X = (x - x0) * scale
    if X < 0 or X > im.width:
        continue
    d.line([(X, 0), (X, im.height)], fill=(255, 0, 0))
    d.text((X + 2, 2), str(x), fill=(255, 0, 0))
    d.text((X + 2, im.height - 14), str(x), fill=(255, 0, 0))
for y in range(y0 - y0 % step, box[3] + 1, step):
    Y = (y - y0) * scale
    if Y < 0 or Y > im.height:
        continue
    d.line([(0, Y), (im.width, Y)], fill=(0, 120, 255))
    d.text((2, Y + 2), str(y), fill=(0, 120, 255))
    d.text((im.width - 44, Y + 2), str(y), fill=(0, 120, 255))
dst = OUT / f'{name}_crop_grid.png'
im.save(dst)
print(f'{name} box={box} x{scale} step {step} -> {dst} {im.size}')
