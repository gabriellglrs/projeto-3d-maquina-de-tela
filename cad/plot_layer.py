"""Desenha as trajetorias de uma camada do G-code, destacando overhangs.

Uso:
    python plot_layer.py <arquivo.gcode> <z> <saida.png> [titulo]
"""

import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

MOVE = re.compile(r"^G1\s+X([-\d.]+)\s+Y([-\d.]+)(?:\s+E([-\d.]+))?")
Z_LINE = re.compile(r"^;\s*Z:([\d.]+)")
TYPE_LINE = re.compile(r"^;TYPE:(\S+.*)$")


def collect(path: Path, target_z: float):
    segs = {"normal": [], "overhang": []}
    x = y = 0.0
    cur_type = ""
    z = 0.0
    active = False

    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = Z_LINE.match(line)
        if m:
            z = float(m.group(1))
            active = abs(z - target_z) < 1e-6
            continue
        m = TYPE_LINE.match(line)
        if m:
            cur_type = m.group(1).strip()
            continue
        if not active or not line.startswith("G1 "):
            continue
        m = MOVE.match(line)
        if not m:
            continue
        nx, ny = float(m.group(1)), float(m.group(2))
        if m.group(3) is not None:
            key = "overhang" if "Overhang" in cur_type else "normal"
            segs[key].append(((x, y), (nx, ny)))
        x, y = nx, ny
    return segs


def main() -> int:
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    gcode, z, out = Path(sys.argv[1]), float(sys.argv[2]), Path(sys.argv[3])
    title = sys.argv[4] if len(sys.argv) > 4 else gcode.name

    segs = collect(gcode, z)
    n_ovh = len(segs["overhang"])
    n_norm = len(segs["normal"])

    fig, ax = plt.subplots(figsize=(9, 7))
    for (a, b) in segs["normal"]:
        ax.plot([a[0], b[0]], [a[1], b[1]], color="#3b6ea5", lw=0.9)
    for (a, b) in segs["overhang"]:
        ax.plot([a[0], b[0]], [a[1], b[1]], color="#d62728", lw=2.4)

    ax.set_aspect("equal")
    ax.set_title(f"{title}\nZ = {z:.2f} mm   |   {n_norm} segmentos normais, {n_ovh} de overhang", fontsize=11)
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.grid(True, lw=0.3, alpha=0.4)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    print(f"salvo: {out}  (normal={n_norm}, overhang={n_ovh})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
