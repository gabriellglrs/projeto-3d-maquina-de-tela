#!/usr/bin/env python3
"""
Calibrador de folga (clearance) parametrico -- CadQuery.

Uma placa com 5 furos de diametro crescente + um pino de 8 mm.
Voce imprime, testa em qual furo o pino entra com aperto suave,
e usa essa folga como padrao em todas as pecas que tiverem encaixe.

Uso:
    python clearance_gauge.py
    python clearance_gauge.py --pin 6 --clearances 0.1 0.2 0.3
"""
import argparse
import os

import cadquery as cq

PLATE_T = 4.0
GAP = 6.0
MARGIN = 6.0


def monta_placa(pin_d, clearances):
    hole_ds = [pin_d + 2 * c for c in clearances]

    largura = MARGIN * 2 + sum(hole_ds) + GAP * (len(hole_ds) - 1)
    altura = pin_d + MARGIN * 2

    placa = (
        cq.Workplane("XY")
        .box(largura, altura, PLATE_T, centered=(True, True, False))
        .edges("|Z")
        .fillet(3)
    )

    x = -largura / 2 + MARGIN
    for d in hole_ds:
        placa = (
            placa.faces(">Z")
            .workplane()
            .pushPoints([(x + d / 2, 0)])
            .hole(d)
        )
        x += d + GAP

    return placa, hole_ds, largura, altura


def monta_pino(pin_d):
    comprimento = 18.0
    return (
        cq.Workplane("XY")
        .circle(pin_d / 2)
        .extrude(comprimento)
        .faces(">Z")
        .workplane()
        .circle(pin_d / 2 + 3)
        .extrude(3)
    )


def relatorio(nome, obj):
    s = obj.val()
    bb = s.BoundingBox()
    print(
        f"  {nome:<16} volume={s.Volume():8.2f} mm3   "
        f"bbox={bb.xlen:6.2f} x {bb.ylen:6.2f} x {bb.zlen:5.2f}   "
        f"valido={s.isValid()}"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pin", type=float, default=8.0)
    ap.add_argument("--clearances", type=float, nargs="+",
                    default=[0.10, 0.15, 0.20, 0.30, 0.40])
    ap.add_argument("--out", default=".")
    a = ap.parse_args()

    os.makedirs(a.out, exist_ok=True)

    placa, hole_ds, largura, altura = monta_placa(a.pin, a.clearances)
    pino = monta_pino(a.pin)

    print(f"placa: {largura:.1f} x {altura:.1f} x {PLATE_T} mm")
    print("furos (mm): " + ", ".join(f"{d:.2f}" for d in hole_ds))
    relatorio("placa", placa)
    relatorio("pino", pino)

    p_placa = os.path.join(a.out, "clearance_plate")
    p_pino = os.path.join(a.out, "clearance_pin")

    cq.exporters.export(placa, p_placa + ".stl")
    cq.exporters.export(placa, p_placa + ".step")
    cq.exporters.export(pino, p_pino + ".stl")
    cq.exporters.export(pino, p_pino + ".step")

    print(f"\nexportado em {os.path.abspath(a.out)}")


if __name__ == "__main__":
    main()
