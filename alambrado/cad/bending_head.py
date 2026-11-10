"""
Cabecote de dobra -- maquina de tela alambrado.

Base: VITA Technical Bulletin 51025-BK (1981), dominio publico.

Principio: tubo com fenda helicoidal. O arame entra pela fenda, enrola na
lamina interna e sai como espiral plana -- que vira o ziguezague da tela.

Regra do manual VITA:
  tubo 2" + lamina 2"   -> malha de 10 cm (4")
  tubo 1 1/2" + lamina  -> malha de 7,6 cm (3")
  fenda                 -> 5 mm (3/16")
  tira de papel         -> 8 cm para tubo de 2"

O trecho junto ao mancal fica SEM corte, senao o tubo perde rigidez.
"""

import math
import os

import FreeCAD as App
import Part
from FreeCAD import Vector

# ---------------- parametros ----------------
TUBE_OD = 60.0      # diametro externo (tubo 2" NPS = 60,3 mm)
TUBE_ID = 50.0      # diametro interno nominal
TUBE_LEN = 620.0    # comprimento (largura da tela + sobra)
SLOT_W = 5.0        # largura da fenda (3/16" = 4,76 mm)
PITCH = 80.0        # passo da helice (tira de papel de 8 cm)
UNCUT = 50.0        # trecho sem corte junto ao mancal
SECTIONS = 260      # resolucao do loft
# --------------------------------------------

OUT = r"C:\DEV\3dprint\alambrado\export"

SLOT_LEN = TUBE_LEN - UNCUT
TURNS = SLOT_LEN / PITCH

# a fenda e medida perpendicular ao caminho da helice; o passo em Z e maior
HELIX_ANGLE = math.atan(PITCH / (math.pi * TUBE_OD))
SLOT_Z = SLOT_W / math.cos(HELIX_ANGLE)


def make_tube():
    outer = Part.makeCylinder(TUBE_OD / 2.0, TUBE_LEN)
    inner = Part.makeCylinder(TUBE_ID / 2.0, TUBE_LEN)
    return outer.cut(inner)


def section(t):
    """Retangulo radial em z, girado de theta -- uma secao da fenda."""
    theta = 2.0 * math.pi * TURNS * t
    z = SLOT_LEN * t
    ux, uy = math.cos(theta), math.sin(theta)

    r_in = TUBE_ID / 2.0 - 2.0
    r_out = TUBE_OD / 2.0 + 2.0
    z0 = z - SLOT_Z / 2.0
    z1 = z + SLOT_Z / 2.0

    pts = [
        Vector(r_in * ux, r_in * uy, z0),
        Vector(r_out * ux, r_out * uy, z0),
        Vector(r_out * ux, r_out * uy, z1),
        Vector(r_in * ux, r_in * uy, z1),
    ]
    edges = [Part.LineSegment(pts[i], pts[(i + 1) % 4]).toShape() for i in range(4)]
    return Part.Wire(edges)


def make_slot_cutter():
    secs = [section(i / (SECTIONS - 1.0)) for i in range(SECTIONS)]
    return Part.makeLoft(secs, True, False, False)


def main():
    doc = App.newDocument("bending_head")

    tube = make_tube()
    print(f"tubo bruto        : {tube.Volume:10.2f} mm3")

    cutter = make_slot_cutter()
    print(f"corte (fenda)     : {cutter.Volume:10.2f} mm3")

    head = tube.cut(cutter)
    head = head.removeSplitter()

    obj = doc.addObject("Part::Feature", "Cabecote")
    obj.Shape = head
    doc.recompute()

    bb = head.BoundBox
    print()
    print(f"cabecote          : {head.Volume:10.2f} mm3")
    print(f"bbox              : {bb.XLength:.2f} x {bb.YLength:.2f} x {bb.ZLength:.2f} mm")
    print(f"valido            : {head.isValid()}")
    print(f"solidos           : {len(head.Solids)}")
    print(f"volumes fechados  : {head.isClosed()}")
    print()
    print(f"fenda             : {SLOT_W} mm perpend. / {SLOT_Z:.2f} mm em Z")
    print(f"helice            : {TURNS:.2f} voltas, passo {PITCH} mm")
    print(f"angulo da helice  : {math.degrees(HELIX_ANGLE):.1f} graus")
    print(f"trecho sem corte  : {UNCUT} mm (junto ao mancal)")

    # conferencia: o tubo tem que continuar sendo 1 peca so
    if len(head.Solids) != 1:
        print("ATENCAO: a fenda partiu o tubo em mais de um solido")

    Part.export([obj], os.path.join(OUT, "cabecote_dobra.step"))
    head.exportStl(os.path.join(OUT, "cabecote_dobra.stl"))
    print("\nexportado: cabecote_dobra.step / cabecote_dobra.stl")

    try:
        import FreeCADGui as Gui
        v = Gui.activeDocument().activeView()
        v.viewAxonometric()
        v.fitAll()
        v.saveImage(os.path.join(OUT, "cabecote_dobra.png"), 1200, 900, "White")
        print("screenshot: cabecote_dobra.png")
    except Exception as exc:
        print(f"screenshot indisponivel: {exc}")


main()
