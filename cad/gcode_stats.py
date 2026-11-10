"""Le um G-code do OrcaSlicer e imprime estatisticas reais.

Uso:  python gcode_stats.py <arquivo.gcode> [...]
"""

import re
import sys
from pathlib import Path

INTEREST = [
    "estimated printing time",
    "filament used",
    "total filament",
    "total layer number",
    "layer_height",
    "nozzle_diameter",
    "filament_type",
    "total estimated",
    "support_material",
    "brim_width",
    "sparse_infill_density",
    "sparse_infill_pattern",
    "wall_loops",
    "top_shell_layers",
    "bottom_shell_layers",
    "bed_temperature",
    "temperature",
    "printer_model",
    "gcode_flavor",
    "max_layer_z",
]


def stats(path: Path) -> None:
    raw = path.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()
    print(f"\n=== {path.name} ===")
    print(f"  tamanho        : {path.stat().st_size / 1024:.0f} KB")
    print(f"  linhas         : {len(lines)}")

    for line in lines:
        if not line.startswith(";"):
            continue
        low = line.lower()
        if any(k in low for k in INTEREST):
            print("  " + line.strip())

    layers = sum(1 for ln in lines if re.match(r"^;LAYER_CHANGE|^; CHANGE_LAYER", ln))
    zvals = [float(m.group(1)) for m in re.finditer(r"^;Z:([\d.]+)", raw, re.M)]
    print(f"  camadas (marcos): {layers}")
    if zvals:
        print(f"  Z maximo        : {max(zvals):.2f} mm")
    g1 = sum(1 for ln in lines if ln.startswith("G1 "))
    print(f"  movimentos G1   : {g1}")


def main() -> int:
    if len(sys.argv) < 2:
        print("uso: python gcode_stats.py <arquivo.gcode> [...]")
        return 2
    for arg in sys.argv[1:]:
        p = Path(arg)
        if not p.exists():
            print(f"nao encontrado: {p}")
            continue
        stats(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
