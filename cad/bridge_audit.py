"""Audita overhangs de um G-code do OrcaSlicer.

Para cada camada, mede o trecho continuo mais longo impresso sobre ar
(marcado como 'Overhang wall'), em mm. Trechos longos e retos afundam;
trechos curtos (arcos) saem limpos.

Uso:  python bridge_audit.py <arquivo.gcode> [...]
"""

import re
import sys
from pathlib import Path

MOVE = re.compile(r"^G1\s+X([-\d.]+)\s+Y([-\d.]+)(?:\s+E([-\d.]+))?")
Z_LINE = re.compile(r"^;\s*Z:([\d.]+)")
TYPE_LINE = re.compile(r"^;TYPE:(\S+.*)$")


def audit(path: Path) -> None:
    print(f"\n=== {path.name} ===")
    x = y = 0.0
    cur_type = ""
    z = 0.0
    run = 0.0
    per_layer: dict[float, float] = {}
    longest: dict[float, float] = {}
    total = 0.0

    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = Z_LINE.match(line)
        if m:
            z = float(m.group(1))
            continue
        m = TYPE_LINE.match(line)
        if m:
            cur_type = m.group(1).strip()
            continue
        if not line.startswith("G1 "):
            continue
        m = MOVE.match(line)
        if not m:
            continue
        nx, ny = float(m.group(1)), float(m.group(2))
        ext = m.group(3)
        dist = ((nx - x) ** 2 + (ny - y) ** 2) ** 0.5
        x, y = nx, ny
        if ext is None or dist <= 0:
            run = 0.0
            continue
        if "Overhang" in cur_type:
            run += dist
            total += dist
            per_layer[z] = per_layer.get(z, 0.0) + dist
            longest[z] = max(longest.get(z, 0.0), run)
        else:
            run = 0.0

    if not longest:
        print("  nenhum overhang wall no G-code")
        return

    print(f"  total overhang     : {total:.1f} mm")
    print(f"  camadas afetadas   : {len(longest)}")
    worst_z = max(longest, key=lambda k: longest[k])
    print(f"  MAIOR TRECHO       : {longest[worst_z]:.2f} mm na camada Z={worst_z:.2f}")

    top = sorted(longest.items(), key=lambda kv: -kv[1])[:5]
    print("  top 5 camadas:")
    for zz, ln in top:
        print(f"    Z={zz:6.2f}  trecho max={ln:6.2f} mm  total={per_layer[zz]:7.1f} mm")


def main() -> int:
    if len(sys.argv) < 2:
        print("uso: python bridge_audit.py <arquivo.gcode> [...]")
        return 2
    for arg in sys.argv[1:]:
        p = Path(arg)
        if p.exists():
            audit(p)
        else:
            print(f"nao encontrado: {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
