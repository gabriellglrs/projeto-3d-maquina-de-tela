"""
Case para ESP32 DevKit V1 (DOIT, 30 pinos) -- parametrico.  v2

Mudancas da v1:
  - recorte do USB com ARCO no topo (elimina a ponte de 9 mm)
  - tampa com ANEL em vez de plugue macico (-76% de material)

Fonte das dimensoes: espboards.dev (51.45 x 28.33 mm).
ATENCAO: clones variam. Medir a placa com paquimetro antes de imprimir
e ajustar BOARD_L / BOARD_W abaixo.
"""

import os

import FreeCAD as App
import Part
from FreeCAD import Vector

# ---------------- dimensoes da placa (MEDIR!) ----------------
BOARD_L = 51.45      # comprimento da PCB
BOARD_W = 28.33      # largura da PCB
# -----------------------------------------------------------

# ---------------- parametros do case ----------------
CLEAR = 0.35         # folga por lado (ajustar depois do calibrador)
WALL = 1.6           # espessura da parede
FLOOR = 1.6          # espessura do fundo
CAVITY_H = 14.0      # altura interna livre (componentes + pinos)

LID_T = 1.6          # espessura da tampa
LID_LIP = 2.0        # quanto o anel entra na base
LID_CLEAR = 0.25     # folga do anel
LID_RING_T = 1.6     # espessura do anel (era macico na v1)

USB_W = 9.0          # largura do recorte do micro-USB
USB_Z0 = 0.6         # altura da base do recorte
USB_H_STRAIGHT = 1.5 # parte reta antes do arco (raio = USB_W/2)

VENT_N = 4
VENT_W = 1.6
VENT_H = 5.0

R_CANTO = 3.0
# ----------------------------------------------------

OUT = r"C:\DEV\3dprint\cad"

OUTER_L = BOARD_L + 2 * CLEAR + 2 * WALL
OUTER_W = BOARD_W + 2 * CLEAR + 2 * WALL
INNER_L = BOARD_L + 2 * CLEAR
INNER_W = BOARD_W + 2 * CLEAR
BASE_H = FLOOR + CAVITY_H

LIP_L = INNER_L - 2 * LID_CLEAR
LIP_W = INNER_W - 2 * LID_CLEAR


def quinas_verticais(shape):
    bb = shape.BoundBox
    out = []
    for e in shape.Edges:
        if abs(e.tangentAt(0).z) < 0.99:
            continue
        c = e.CenterOfMass
        nx = min(abs(c.x - bb.XMin), abs(c.x - bb.XMax)) < 0.01
        ny = min(abs(c.y - bb.YMin), abs(c.y - bb.YMax)) < 0.01
        if nx and ny:
            out.append(e)
    return out


def recorte_usb():
    """Perfil retangulo + arco semicircular, extrudado pela parede.

    O arco faz a 'ponte' virar uma curva fechada, que imprime sem afundar.
    """
    r = USB_W / 2.0
    z1 = USB_Z0 + USB_H_STRAIGHT
    p1 = Vector(0, -r, USB_Z0)
    p2 = Vector(0, r, USB_Z0)
    p3 = Vector(0, r, z1)
    p4 = Vector(0, -r, z1)
    topo = Vector(0, 0, z1 + r)

    wire = Part.Wire([
        Part.LineSegment(p1, p2).toShape(),
        Part.LineSegment(p2, p3).toShape(),
        Part.Arc(p3, topo, p4).toShape(),
        Part.LineSegment(p4, p1).toShape(),
    ])
    face = Part.Face(wire)
    solido = face.extrude(Vector(WALL + 2, 0, 0))
    solido.translate(Vector(-OUTER_L / 2 - 1, 0, 0))
    return solido


def monta_base():
    corpo = Part.makeBox(OUTER_L, OUTER_W, BASE_H,
                         Vector(-OUTER_L / 2, -OUTER_W / 2, 0))

    cav = Part.makeBox(INNER_L, INNER_W, CAVITY_H + 1,
                       Vector(-INNER_L / 2, -INNER_W / 2, FLOOR))
    corpo = corpo.cut(cav)

    corpo = corpo.cut(recorte_usb())

    for i in range(VENT_N):
        t = (i + 0.5) / VENT_N
        y = -OUTER_W / 2 + WALL + t * (OUTER_W - 2 * WALL)
        for sx in (-1, 1):
            v = Part.makeBox(WALL + 2, VENT_W, VENT_H,
                             Vector(sx * OUTER_L / 2 - 1,
                                    y - VENT_W / 2,
                                    FLOOR + 2.0))
            corpo = corpo.cut(v)

    try:
        corpo = corpo.makeFillet(R_CANTO, quinas_verticais(corpo))
    except Exception as exc:
        print(f"fillet base falhou: {exc}")

    return corpo


def monta_tampa():
    tampa = Part.makeBox(OUTER_L, OUTER_W, LID_T,
                         Vector(-OUTER_L / 2, -OUTER_W / 2, 0))

    # anel (nao mais macico)
    anel_ext = Part.makeBox(LIP_L, LIP_W, LID_LIP + 1,
                            Vector(-LIP_L / 2, -LIP_W / 2, -LID_LIP))
    anel_int = Part.makeBox(LIP_L - 2 * LID_RING_T, LIP_W - 2 * LID_RING_T,
                            LID_LIP + 2,
                            Vector(-(LIP_L - 2 * LID_RING_T) / 2,
                                   -(LIP_W - 2 * LID_RING_T) / 2,
                                   -LID_LIP - 0.5))
    anel = anel_ext.cut(anel_int)

    tampa = tampa.fuse(anel)

    try:
        tampa = tampa.makeFillet(R_CANTO, quinas_verticais(tampa))
    except Exception as exc:
        print(f"fillet tampa falhou: {exc}")

    return tampa


def main():
    doc = App.newDocument("esp32_case_v2")

    base = monta_base()
    tampa = monta_tampa()

    objs = {}
    for nome, shape in (("Base", base), ("Tampa", tampa)):
        o = doc.addObject("Part::Feature", nome)
        o.Shape = shape
        objs[nome] = o
        bb = shape.BoundBox
        print(f"{nome:<6} vol={shape.Volume:9.2f} mm3  "
              f"bbox={bb.XLength:6.2f} x {bb.YLength:6.2f} x {bb.ZLength:5.2f}  "
              f"valido={shape.isValid()}  solidos={len(shape.Solids)}")

    doc.recompute()

    # conferencia de encaixe
    tm = tampa.copy()
    tm.translate(Vector(0, 0, BASE_H))
    inter = base.common(tm)
    print(f"\ninterferencia base/tampa: {inter.Volume:.6f} mm3")

    print(f"placa assumida : {BOARD_L} x {BOARD_W} mm")
    print(f"externo        : {OUTER_L:.2f} x {OUTER_W:.2f} x {BASE_H:.2f} mm")
    print(f"abertura USB   : {USB_W:.1f} mm + arco R{USB_W/2:.1f}")
    print(f"anel da tampa  : {LID_RING_T} mm de espessura")

    Part.export([objs["Base"], objs["Tampa"]],
                os.path.join(OUT, "esp32_case_v2.step"))
    base.exportStl(os.path.join(OUT, "esp32_base_v2.stl"))
    tampa.exportStl(os.path.join(OUT, "esp32_lid_v2.stl"))
    print("exportado: esp32_case_v2.step / esp32_base_v2.stl / esp32_lid_v2.stl")

    try:
        import FreeCADGui as Gui
        v = Gui.activeDocument().activeView()
        v.viewAxonometric()
        v.fitAll()
        v.saveImage(os.path.join(OUT, "esp32_case_v2.png"), 1200, 900, "White")
        print("screenshot: esp32_case_v2.png")
    except Exception as exc:
        print(f"screenshot indisponivel: {exc}")


main()
