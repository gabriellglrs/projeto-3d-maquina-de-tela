"""
Clipe de filamento -- parametrico.

Prende a ponta do filamento na aba do carretel pra ele nao desenrolar.
Imprime deitado, sem suporte.

    L x W x T  = corpo
    encaixe    = fenda larga que abraca a aba do carretel
    garra      = fenda estreita que morde o filamento (1.75 mm)
"""

import os

import FreeCAD as App
import Part
from FreeCAD import Vector

# ---------------- parametros ----------------
L = 30.0          # comprimento
W = 16.0          # largura
T = 3.0           # espessura

FLANGE_W = 4.0    # espessura da aba do carretel (medir o seu!)
FLANGE_D = 13.0   # quanto o encaixe avanca

FIL_W = 1.8       # fenda do filamento (1.75 + folga minima = aperto)
FIL_D = 10.0      # profundidade da garra

R_CANTO = 2.0     # raio das quinas externas
# --------------------------------------------

OUT = r"C:\DEV\3dprint\cad"


def main():
    doc = App.newDocument("filament_clip")

    corpo = Part.makeBox(L, W, T)

    # encaixe da aba: entra pela lateral x = 0
    encaixe = Part.makeBox(
        FLANGE_D, FLANGE_W, T + 2,
        Vector(0, (W - FLANGE_W) / 2, -1),
    )
    corpo = corpo.cut(encaixe)

    # garra do filamento: entra pela lateral x = L
    garra = Part.makeBox(
        FIL_D, FIL_W, T + 2,
        Vector(L - FIL_D, (W - FIL_W) / 2, -1),
    )
    corpo = corpo.cut(garra)

    # arredonda so as 4 quinas externas (as internas das fendas ficam retas)
    bb = corpo.BoundBox

    def quina_externa(e):
        if abs(e.tangentAt(0).z) < 0.99:
            return False
        c = e.CenterOfMass
        nx = min(abs(c.x - bb.XMin), abs(c.x - bb.XMax)) < 0.01
        ny = min(abs(c.y - bb.YMin), abs(c.y - bb.YMax)) < 0.01
        return nx and ny

    quinas = [e for e in corpo.Edges if quina_externa(e)]
    try:
        corpo = corpo.makeFillet(R_CANTO, quinas)
        print(f"fillet R{R_CANTO} aplicado em {len(quinas)} quinas")
    except Exception as exc:
        print(f"fillet falhou ({exc}); seguindo sem arredondar")

    obj = doc.addObject("Part::Feature", "FilamentClip")
    obj.Shape = corpo
    doc.recompute()

    b = corpo.BoundBox
    print(f"volume  : {corpo.Volume:.2f} mm3")
    print(f"bbox    : {b.XLength:.2f} x {b.YLength:.2f} x {b.ZLength:.2f} mm")
    print(f"valido  : {corpo.isValid()}")
    print(f"solidos : {len(corpo.Solids)}")

    Part.export([obj], os.path.join(OUT, "filament_clip.step"))
    corpo.exportStl(os.path.join(OUT, "filament_clip.stl"))
    print("exportado: filament_clip.step / filament_clip.stl")

    # screenshot pra conferir visualmente
    try:
        import FreeCADGui as Gui
        Gui.activeDocument().activeView().viewAxonometric()
        Gui.activeDocument().activeView().fitAll()
        Gui.activeDocument().activeView().saveImage(
            os.path.join(OUT, "filament_clip.png"), 1200, 900, "White"
        )
        print("screenshot: filament_clip.png")
    except Exception as exc:
        print(f"screenshot indisponivel: {exc}")


main()
