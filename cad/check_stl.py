#!/usr/bin/env python3
"""
Validador independente de STL binario.

Nao confia no CAD nem no slicer: le o arquivo final e mede o que
realmente vai para a impressora.

Uso:
    python check_stl.py peca.stl [peca2.stl ...]

Checa:
  - triangulos, degenerados
  - volume (signed tetrahedra) -> mm3
  - bounding box -> mm
  - watertight: toda aresta tem que aparecer exatamente 2x
  - non-manifold / bordas abertas
"""
import re
import struct
import sys
from collections import Counter


def _parse_binario(data, n):
    tris = []
    off = 84
    for _ in range(n):
        vals = struct.unpack("<12fH", data[off:off + 50])
        off += 50
        tris.append((vals[3:6], vals[6:9], vals[9:12]))
    return tris


_VERT = re.compile(
    rb"vertex\s+(-?[\d.]+(?:[eE][+-]?\d+)?)\s+"
    rb"(-?[\d.]+(?:[eE][+-]?\d+)?)\s+"
    rb"(-?[\d.]+(?:[eE][+-]?\d+)?)"
)


def _parse_ascii(data):
    vs = _VERT.findall(data)
    if not vs or len(vs) % 3 != 0:
        raise ValueError(f"STL ASCII invalido: {len(vs)} vertices")
    return [
        tuple(tuple(float(c) for c in v) for v in vs[i:i + 3])
        for i in range(0, len(vs), 3)
    ]


def read_stl(path):
    """Aceita STL binario ou ASCII. O FreeCAD exporta ASCII por padrao."""
    with open(path, "rb") as f:
        data = f.read()

    if len(data) < 84:
        raise ValueError("arquivo menor que o cabecalho STL")

    n = struct.unpack("<I", data[80:84])[0]
    if 84 + n * 50 == len(data):
        return _parse_binario(data, n), "binario"

    if b"vertex" in data[:4000]:
        return _parse_ascii(data), "ascii"

    raise ValueError(
        f"nao reconhecido: {len(data)} bytes, cabecalho sugere "
        f"{n} triangulos ({84 + n * 50} bytes)"
    )


def volume(tris):
    v = 0.0
    for a, b, c in tris:
        v += (
            a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0])
        ) / 6.0
    return v


def bbox(tris):
    xs = [p[0] for t in tris for p in t]
    ys = [p[1] for t in tris for p in t]
    zs = [p[2] for t in tris for p in t]
    return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))


def degenerate(tris, eps=1e-9):
    n = 0
    for a, b, c in tris:
        ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
        vx, vy, vz = c[0] - a[0], c[1] - a[1], c[2] - a[2]
        cx, cy, cz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
        if (cx * cx + cy * cy + cz * cz) ** 0.5 < eps:
            n += 1
    return n


def edge_report(tris, tol=1e-5):
    cont = Counter()
    for t in tris:
        for i in range(3):
            p, q = t[i], t[(i + 1) % 3]
            a = (round(p[0] / tol), round(p[1] / tol), round(p[2] / tol))
            b = (round(q[0] / tol), round(q[1] / tol), round(q[2] / tol))
            cont[(a, b) if a <= b else (b, a)] += 1

    abertas = sum(1 for v in cont.values() if v == 1)
    non_manifold = sum(1 for v in cont.values() if v > 2)
    return len(cont), abertas, non_manifold


def analisa(path):
    tris, formato = read_stl(path)
    if not tris:
        print(f"{path}: VAZIO")
        return False

    x0, x1, y0, y1, z0, z1 = bbox(tris)
    vol = volume(tris)
    ne, abertas, nm = edge_report(tris)
    deg = degenerate(tris)

    watertight = abertas == 0 and nm == 0

    print(f"\n=== {path} ===")
    print(f"  formato         : {formato}")
    print(f"  triangulos      : {len(tris)}")
    print(f"  degenerados     : {deg}")
    print(f"  bbox (mm)       : X {x1 - x0:.2f}  Y {y1 - y0:.2f}  Z {z1 - z0:.2f}")
    print(f"  volume (mm3)    : {abs(vol):.2f}")
    print(f"  arestas         : {ne}  (abertas {abertas}, non-manifold {nm})")
    print(f"  WATERTIGHT      : {'SIM' if watertight else 'NAO'}")

    if vol < 0:
        print("  AVISO           : volume negativo -> normais invertidas")
    if not watertight:
        print("  AVISO           : malha nao-fechada; o slicer pode fatiar errado")

    return watertight


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    ok = all([analisa(p) for p in sys.argv[1:]])
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
