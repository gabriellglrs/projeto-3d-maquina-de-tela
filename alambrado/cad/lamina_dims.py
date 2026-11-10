#!/usr/bin/env python3
"""Volume esperado da lamina interna / bending arm (VITA 51025-BK).

Fontes
------
Fig. 3  : desenho da peca 4 -- retangulo com furo a distancia B de uma ponta
          e quinas arredondadas de raio C ("round off corners")
Texto   : "Drill 0.6cm (1/4") diameter hole in bending-head arm (4) and round
          off corners." <see figure 3>
Texto   : "5cm (2") ID bending-head pipe used with 5cm (2") wide bending-head
          arm ... fencing with 10cm (4") mesh"
Texto   : crankshaft -- "A 3/16-inch slot is cut in the end, so that it will
          fit over the 'blade', or bending arm"  -> espessura = 0,5 cm
Tabela  : B = 1 cm   (distancia furo <-> ponta)
          C = 0,5 cm (raio das quinas)
          F = 0,5 cm (largura da fenda da manivela = espessura da lamina)

Comprimento (o manual nao cotA)
------------------------------
Fig. 13 mostra a lamina (4) saindo dos DOIS lados do tubo (7), quase simetrica:
medida em pixels, com a escala fixada pela OD do tubo (192 px <-> 60 mm):

    escala              = 3,2 px/mm
    tubo desenhado      = 599 px -> 187 mm  (o tubo do VITA e curto)
    lamina desenhada    = 1000 px -> 312 mm
    sobra lado manivela = 197 px -> 62 mm
    sobra lado oposto   = 201 px -> 63 mm

A sobra e uma cota ABSOLUTA: e la que a fenda da manivela encaixa e que entra
o parafuso a B = 1 cm da ponta. Logo ela nao escala com o tubo. O nosso tubo
tem 620 mm (bending_head.py), entao:

    L = 620 + 2 x 62 = 744 mm

Eixos: X = comprimento, Y = largura, Z = espessura (a lamina deita na mesa).
       Furo na ponta -X, centro em Y = largura/2.
"""
from __future__ import annotations

import math

# --- parametros -------------------------------------------------------------
L = 744.0     # comprimento  (620 do tubo + 2 x 62 de sobra)
W = 50.0      # largura      (VITA: 5 cm -- = ID do tubo de 2")
T = 5.0       # espessura    (VITA: 0,5 cm = largura da fenda da manivela)
B = 10.0      # centro do furo a partir da ponta (tabela: B = 1 cm)
R = 5.0       # raio das quinas (tabela: C = 0,5 cm)
hd = 6.4      # diametro do furo (VITA: 0,6 cm = 1/4")

# --- volumes ---------------------------------------------------------------
caixa = L * W * T
vquinas = 4.0 * (R * R - math.pi * R * R / 4.0) * T
vfuro = math.pi * (hd / 2.0) ** 2 * T
v = caixa - vquinas - vfuro

bbox = ((0.0, 0.0, 0.0), (L, W, T))

if __name__ == "__main__":
    print(f"caixa          = {caixa:12.3f} mm3")
    print(f"- 4 quinas R{R:g} = {vquinas:12.3f} mm3")
    print(f"- furo O{hd:g}    = {vfuro:12.3f} mm3")
    print(f"TOTAL          = {v:12.3f} mm3   corpos = 1")
    print(f"bbox min = {bbox[0]}   bbox max = {bbox[1]}")
    print(f"massa em aco (7,85 g/cm3) = {v / 1000.0 * 7.85:.1f} g")

    # --- verificacoes de projeto ------------------------------------------
    print("\n--- verificacoes ---")
    print(f"metal na ponta do furo   = {B - hd / 2.0:6.2f} mm  (min 3)")
    print(f"metal lateral do furo    = {W / 2.0 - hd / 2.0:6.2f} mm")
    print(f"folga furo <-> quina     = "
          f"{math.hypot(B - R, W / 2.0 - R) - R - hd / 2.0:6.2f} mm")
    print(f"sobra fora do tubo       = {(L - 620.0) / 2.0:6.2f} mm")
    print(f"lamina x tubo (2,5 cm)   = {L / 620.0:6.3f}")
    ok = (B - hd / 2.0 >= 3 and math.hypot(B - R, W / 2.0 - R) - R - hd / 2.0 >= 3
          and L > 620.0 and T <= 5.0)
    print(f"aprovado: {ok}")
