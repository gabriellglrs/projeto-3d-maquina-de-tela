#!/usr/bin/env python3
"""check_stl.py — verifica se STL(s) binário(s) são estanque (watertight).

Uso: python check_stl.py arquivo.stl [outro.stl ...]

Para cada arquivo:
  - lê os triângulos do STL binário;
  - quantiza os vértices a 1 µm e conta cada aresta (par ordenado de vértices);
  - estanque = toda aresta aparece em exatamente 2 triângulos;
  - calcula o volume pela soma assinada das tetraedros (divergência) e o bbox.

Imprime uma linha por arquivo e sai com código 1 se algum não estiver estanque.
"""
import collections
import struct
import sys

Q = float(sys.argv[sys.argv.index("--q") + 1]) if "--q" in sys.argv else 1e-3  # quantização em mm (padrão 1 µm)


def read_stl(path):
    with open(path, "rb") as f:
        header = f.read(84)
        if len(header) < 84:
            raise ValueError(f"{path}: arquivo curto demais para STL")
        n = struct.unpack("<I", header[80:84])[0]
        tris = []
        for _ in range(n):
            data = f.read(50)
            if len(data) < 50:
                raise ValueError(f"{path}: dados truncados ({len(tris)}/{n} triângulos)")
            v = struct.unpack("<12fH", data)
            tris.append(((v[3], v[4], v[5]),
                         (v[6], v[7], v[8]),
                         (v[9], v[10], v[11])))
    return tris


def check(path):
    tris = read_stl(path)
    edges = collections.Counter()
    verts = set()
    vol = 0.0
    lo = [float("inf")] * 3
    hi = [float("-inf")] * 3
    for a, b, c in tris:
        ka = (round(a[0] / Q), round(a[1] / Q), round(a[2] / Q))
        kb = (round(b[0] / Q), round(b[1] / Q), round(b[2] / Q))
        kc = (round(c[0] / Q), round(c[1] / Q), round(c[2] / Q))
        verts.update((ka, kb, kc))
        for e in ((ka, kb), (kb, kc), (kc, ka)):
            edges[tuple(sorted(e))] += 1
        vol += (a[0] * (b[1] * c[2] - b[2] * c[1])
                - a[1] * (b[0] * c[2] - b[2] * c[0])
                + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0
        for p in (a, b, c):
            for i in range(3):
                lo[i] = min(lo[i], p[i])
                hi[i] = max(hi[i], p[i])
    bad_edges = [(e, n) for e, n in edges.items() if n != 2]
    ok = not bad_edges
    print(f"{path}")
    print(f"  tris={len(tris)} verts={len(verts)} arestas={len(edges)} "
          f"arestas!=2={len(bad_edges)} (q={Q:g}) -> {'ESTANQUE' if ok else 'VAZADO'}")
    for e, n in bad_edges[:8]:
        (a, b) = e
        print(f"    x{n}: ({a[0]*Q:.3f},{a[1]*Q:.3f},{a[2]*Q:.3f})-"
              f"({b[0]*Q:.3f},{b[1]*Q:.3f},{b[2]*Q:.3f})")
    print(f"  volume_malha={abs(vol):.1f} mm³")
    print(f"  bbox=[{lo[0]:.3f},{lo[1]:.3f},{lo[2]:.3f}].."
          f"[{hi[0]:.3f},{hi[1]:.3f},{hi[2]:.3f}] "
          f"({hi[0]-lo[0]:.3f} x {hi[1]-lo[1]:.3f} x {hi[2]-lo[2]:.3f})")
    return ok


def main(argv):
    args, skip = [], False
    for a in argv[1:]:
        if skip:
            skip = False
            continue
        if a == "--q":
            skip = True
            continue
        args.append(a)
    if not args:
        print(__doc__)
        return 2
    allok = True
    for path in args:
        allok = check(path) and allok
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
