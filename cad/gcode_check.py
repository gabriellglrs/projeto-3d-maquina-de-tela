"""Sanidade de um G-code: limites XY, Z, extrusao, temperaturas.

Uso: python gcode_check.py <arquivo.gcode> [...]
"""

import re
import sys
from pathlib import Path

MOVE = re.compile(r"^G1\s+(.*)$")
X = re.compile(r"X([-\d.]+)")
Y = re.compile(r"Y([-\d.]+)")
Z = re.compile(r"Z([-\d.]+)")
E = re.compile(r"E([-\d.]+)")


def check(path: Path) -> None:
    txt = path.read_text(encoding="utf-8", errors="replace")
    lines = txt.splitlines()

    xs, ys, zs = [], [], []
    bad = []
    for ln in lines:
        if ln.startswith("G1 "):
            m = MOVE.match(ln)
            if not m:
                continue
            body = m.group(1)
            mx, my, mz, me = X.search(body), Y.search(body), Z.search(body), E.search(body)
            if mx:
                xs.append(float(mx.group(1)))
            if my:
                ys.append(float(my.group(1)))
            if mz:
                zs.append(float(mz.group(1)))
            if me and float(me.group(1)) < 0:
                bad.append(ln)

    print(f"\n=== {path.name} ===")
    print(f"  X: {min(xs):7.2f} .. {max(xs):7.2f} mm")
    print(f"  Y: {min(ys):7.2f} .. {max(ys):7.2f} mm")
    print(f"  Z: {min(zs):7.2f} .. {max(zs):7.2f} mm")
    print(f"  E negativo em G1 : {len(bad)} linha(s)")

    temps = sorted({m.group(1) for m in re.finditer(r"^M10[49] S(\d+)", txt, re.M)}, key=int)
    beds = sorted({m.group(1) for m in re.finditer(r"^M1[49]0 S(\d+)", txt, re.M)}, key=int)
    print(f"  temperaturas bico: {', '.join(temps)} C")
    print(f"  temperaturas mesa: {', '.join(beds)} C")

    fans = sorted({m.group(1) for m in re.finditer(r"^M106 S(\d+)", txt, re.M)}, key=int)
    print(f"  velocidades fan   : {', '.join(fans)}")

    g92 = sum(1 for ln in lines if ln.startswith("G92 E0"))
    layers = len(re.findall(r"^;LAYER_CHANGE", txt, re.M))
    print(f"  G92 E0           : {g92} (camadas: {layers})")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    for a in sys.argv[1:]:
        p = Path(a)
        if p.exists():
            check(p)
        else:
            print(f"nao encontrado: {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
