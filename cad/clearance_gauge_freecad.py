"""
Calibrador de folga (clearance) -- FreeCAD headless.

Mesma peca do clearance_gauge.py (CadQuery) e clearance_gauge.scad,
mas usando a API do FreeCAD. Roda sem GUI:

    "C:\\Program Files\\FreeCAD 1.1\\bin\\FreeCADCmd.exe" clearance_gauge_freecad.py

Gera STEP (B-rep exato) e STL.
"""
import os

import FreeCAD as App
import Part

PIN_D = 8.0
CLEARANCES = [0.10, 0.15, 0.20, 0.30, 0.40]
PLATE_T = 4.0
GAP = 6.0
MARGIN = 6.0

OUT = os.path.dirname(os.path.abspath(__file__))


def main():
    hole_ds = [PIN_D + 2 * c for c in CLEARANCES]
    largura = MARGIN * 2 + sum(hole_ds) + GAP * (len(hole_ds) - 1)
    altura = PIN_D + MARGIN * 2

    doc = App.newDocument("clearance")

    # placa: canto inferior esquerdo na origem
    placa = Part.makeBox(
        largura, altura, PLATE_T, App.Vector(-largura / 2, -altura / 2, 0)
    )

    # furos passantes (cilindro mais alto que a placa = corte garantido)
    x = -largura / 2 + MARGIN
    for d in hole_ds:
        cx = x + d / 2
        furo = Part.makeCylinder(d / 2, PLATE_T + 2, App.Vector(cx, 0, -1))
        placa = placa.cut(furo)
        x += d + GAP

    # pino 8 mm com flange
    pino = Part.makeCylinder(PIN_D / 2, 18, App.Vector(0, 0, 0))
    flange = Part.makeCylinder(PIN_D / 2 + 3, 3, App.Vector(0, 0, 18))
    pino = pino.fuse(flange)

    for nome, shape in (("Placa", placa), ("Pino", pino)):
        obj = doc.addObject("Part::Feature", nome)
        obj.Shape = shape
        bb = shape.BoundBox
        print(
            f"{nome:<6} volume={shape.Volume:8.2f} mm3   "
            f"bbox={bb.XLength:6.2f} x {bb.YLength:6.2f} x {bb.ZLength:5.2f}   "
            f"valido={shape.isValid()}"
        )

    doc.recompute()

    print(f"placa: {largura:.1f} x {altura:.1f} x {PLATE_T} mm")
    print("furos (mm): " + ", ".join(f"{d:.2f}" for d in hole_ds))

    Part.export([doc.getObject("Placa"), doc.getObject("Pino")],
                os.path.join(OUT, "clearance_freecad.step"))
    placa.exportStl(os.path.join(OUT, "clearance_plate_fc.stl"))
    pino.exportStl(os.path.join(OUT, "clearance_pin_fc.stl"))

    print(f"exportado em {OUT}")


main()
