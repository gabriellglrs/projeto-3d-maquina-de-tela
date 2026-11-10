"""Estima o tempo de cada camada a partir dos feedrates do G-code.

Aproximacao: soma distancia/velocidade de cada G1. Ignora aceleracao,
entao subestima um pouco. Serve para achar camada rapida demais
(regra pratica: abaixo de ~5 s o plastico nao resfria).

Uso: python layer_times.py <arquivo.gcode>
"""

import re
import sys
from pathlib import Path

G1 = re.compile(r"^G1\s+(.*)$")
X = re.compile(r"X([-\d.]+)")
Y = re.compile(r"Y([-\d.]+)")
Z = re.compile(r"Z([-\d.]+)")
F = re.compile(r"F([-\d.]+)")
Z_LINE = re.compile(r"^;\s*Z:([\d.]+)")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"nao encontrado: {path}")
        return 1

    x = y = 0.0
    feed = 3000.0
    z = 0.0
    t = 0.0
    per_layer: dict[float, float] = {}

    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = Z_LINE.match(line)
        if m:
            z = float(m.group(1))
            per_layer.setdefault(z, 0.0)
            continue
        if not line.startswith("G1 "):
            continue
        m = G1.match(line)
        if not m:
            continue
        body = m.group(1)
        mf = F.search(body)
        if mf:
            feed = max(float(mf.group(1)), 1.0)
        mx, my = X.search(body), Y.search(body)
        nx = float(mx.group(1)) if mx else x
        ny = float(my.group(1)) if my else y
        dist = ((nx - x) ** 2 + (ny - y) ** 2) ** 0.5
        x, y = nx, ny
        if dist <= 0:
            continue
        dt = dist / (feed / 60.0)
        t += dt
        if z in per_layer:
            per_layer[z] += dt

    if not per_layer:
        print("nenhuma camada encontrada")
        return 1

    vals = [(z, v) for z, v in per_layer.items() if v > 0.01]
    vals.sort(key=lambda kv: kv[1])
    total = sum(v for _, v in vals)

    print(f"\n=== {path.name} ===")
    print(f"  camadas           : {len(vals)}")
    print(f"  tempo estimado    : {total/60:.1f} min")
    print("  mais rapidas:")
    for zz, vv in vals[:5]:
        flag = "  <-- risco" if vv < 5 else ""
        print(f"    Z={zz:6.2f}  {vv:5.1f} s{flag}")
    print("  mais lentas:")
    for zz, vv in vals[-3:]:
        print(f"    Z={zz:6.2f}  {vv:5.1f} s")
    rapidas = sum(1 for _, v in vals if v < 5)
    print(f"  camadas < 5 s     : {rapidas}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
