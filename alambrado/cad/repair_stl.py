#!/usr/bin/env python3
"""repair_stl.py — repara o STL binário (T-junctions e faixas duplicadas).

Uso: python repair_stl.py entrada.stl [saida.stl] [--tol 0.05]

O que faz:
  1. solda vértices closer que --tol mm (padrão 0,05 mm = 50 µm) numa grade
     espacial — fecha trincas de T junction deixadas por nudges de boolean;
  2. remove triângulos degenerados (vértices repetidos);
  3. remove triângulos duplicados (mesmo conjunto de vértices);
  4. reconta as arestas e imprime o resultado (precisa terminar ESTANQUE);
  5. grava o STL binário reparado (padrão: <entrada>_fix.stl).

O padrão de saída é o mesmo do check_stl.py: aresta compartilhada por
exatamente 2 triângulos.
"""
import collections
import struct
import sys


def read_stl(path):
    with open(path, "rb") as f:
        header = f.read(84)
        n = struct.unpack("<I", header[80:84])[0]
        tris = []
        for _ in range(n):
            d = f.read(50)
            v = struct.unpack("<12fH", d)
            tris.append(((v[3], v[4], v[5]),
                         (v[6], v[7], v[8]),
                         (v[9], v[10], v[11])))
    return tris


def write_stl(path, tris, header=b"solid repaired"):
    with open(path, "wb") as f:
        f.write(header.ljust(80, b"\0")[:80])
        f.write(struct.pack("<I", len(tris)))
        for a, b, c in tris:
            ux, uy, uz = (b[0]-a[0], b[1]-a[1], b[2]-a[2])
            vx, vy, vz = (c[0]-a[0], c[1]-a[1], c[2]-a[2])
            nx, ny, nz = (uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx)
            ln = (nx*nx+ny*ny+nz*nz) ** 0.5 or 1.0
            f.write(struct.pack("<12fH", nx/ln, ny/ln, nz/ln,
                                a[0], a[1], a[2], b[0], b[1], b[2],
                                c[0], c[1], c[2], 0))


def weld(tris, tol):
    """Solda vértices com grade espacial; devolve triângulos por ids + lista de pontos."""
    inv = 1.0 / tol
    grid = {}
    reps = []  # pontos representantes

    def vid(p):
        cell = (int(p[0] * inv), int(p[1] * inv), int(p[2] * inv))
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for i in grid.get((cell[0]+dx, cell[1]+dy, cell[2]+dz), ()):
                        q = reps[i]
                        if (q[0]-p[0])**2 + (q[1]-p[1])**2 + (q[2]-p[2])**2 <= tol*tol:
                            return i
        i = len(reps)
        reps.append(p)
        grid.setdefault(cell, []).append(i)
        return i

    out = []
    for a, b, c in tris:
        out.append((vid(a), vid(b), vid(c)))
    return out, reps


def fill_holes(ids):
    """Fecha lacunas: arestas usadas por 1 triângulo viram loops e ganham
    triângulos (leque), orientados oposto ao vizinho existente."""
    directed = set()
    for a, b, c in ids:
        directed.update(((a, b), (b, c), (c, a)))
    und = {}
    for (u, v) in directed:
        k = (u, v) if u < v else (v, u)
        und.setdefault(k, []).append((u, v))
    succ = {}
    for k, dirs in und.items():
        if len(dirs) == 1:                # borda: só 1 triângulo usa
            u, v = dirs[0]
            succ[v] = u                    # leque usa (v,u), reverso do existente
    loops, used = [], set()
    for start in list(succ):
        if start in used:
            continue
        loop, cur = [], start
        while cur in succ and cur not in used:
            used.add(cur)
            loop.append(cur)
            cur = succ[cur]
        if len(loop) >= 3 and cur == start:
            loops.append(loop)
    for L in loops:
        for i in range(1, len(L) - 1):
            ids.append((L[0], L[i], L[i + 1]))
    return len(loops)


def main(argv):
    tol, skip = 0.05, set()
    if "--tol" in argv:
        tol = float(argv[argv.index("--tol") + 1])
        skip.update(("--tol", argv[argv.index("--tol") + 1]))
    args = [a for a in argv[1:] if a not in skip]
    if not args:
        print(__doc__)
        return 2
    src = args[0]
    dst = args[1] if len(args) > 1 else src[:-4] + "_fix.stl"

    tris = read_stl(src)
    ids, reps = weld(tris, tol)
    n0 = len(ids)

    # 1. degenerados
    ids = [t for t in ids if t[0] != t[1] and t[1] != t[2] and t[0] != t[2]]
    # 2. duplicados (mesmo conjunto de vértices): mantém o primeiro
    seen, uniq = set(), []
    for t in ids:
        k = tuple(sorted(t))
        if k in seen:
            continue
        seen.add(k)
        uniq.append(t)
    ids = uniq
    nholes = fill_holes(ids)

    edges = collections.Counter()
    for a, b, c in ids:
        for e in ((a, b), (b, c), (c, a)):
            edges[tuple(sorted(e))] += 1
    bad = sum(1 for n in edges.values() if n != 2)
    print(f"{src}: tris {n0} -> {len(ids)} (solda tol={tol} mm, "
          f"{nholes} lacuna(s) fechada(s)) "
          f"arestas!=2 = {bad} -> {'ESTANQUE' if bad == 0 else 'VAZADO'}")
    if bad:
        for e, n in list((e, n) for e, n in edges.items() if n != 2)[:8]:
            a, b = (reps[i] for i in e)
            print(f"  x{n}: ({a[0]:.3f},{a[1]:.3f},{a[2]:.3f})-({b[0]:.3f},{b[1]:.3f},{b[2]:.3f})")
        return 1
    write_stl(dst, [(reps[a], reps[b], reps[c]) for a, b, c in ids])
    print(f"  gravado: {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
