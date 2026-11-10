"""Tabela comparativa de G-codes fatiados."""

import re
import sys
from pathlib import Path

KEYS = [
    "total filament used [g]",
    "filament used [mm]",
    "filament used [cm3]",
    "estimated printing time (normal mode)",
    "total layer number",
    "sparse_infill_density",
    "wall_loops",
    "brim_width",
    "nozzle_temperature",
    "first_layer_bed_temperature",
]


def read(path: Path) -> dict[str, str]:
    txt = path.read_text(encoding="utf-8", errors="replace")
    out = {}
    for k in KEYS:
        m = re.search(r"^; " + re.escape(k) + r"\s*[:=]\s*(.+)$", txt, re.M)
        out[k] = m.group(1).strip() if m else "-"
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print("uso: python slice_table.py <a.gcode> <b.gcode> ...")
        return 2

    rows = []
    for arg in sys.argv[1:]:
        p = Path(arg)
        if p.exists():
            rows.append((p.name, read(p)))

    labels = {
        "total filament used [g]": "massa",
        "filament used [mm]": "filamento",
        "filament used [cm3]": "volume",
        "estimated printing time (normal mode)": "tempo",
        "total layer number": "camadas",
        "sparse_infill_density": "infill",
        "wall_loops": "paredes",
        "brim_width": "brim",
        "nozzle_temperature": "bico",
        "first_layer_bed_temperature": "mesa",
    }

    w = max(len(n) for n, _ in rows) + 2
    print(f"{'':22}" + "".join(f"{n:<{w}}" for n, _ in rows))
    for k in KEYS:
        print(f"{labels[k]:22}" + "".join(f"{d[k]:<{w}}" for _, d in rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
