#!/usr/bin/env python3
"""Volumes esperados do mancal do cabo -- blocos 1A e 1B (VITA 51025-BK).

Fontes
------
Fig. 1  : bloco 1A (mancal do virabrequim) -- 2 furos verticais + furo horizontal
Fig. 2  : bloco 1B (fixacao do tubo)        -- 3 furos verticais + furo horizontal
Fig. 18 : secao da fixacao (ancorada no tubo OD 60 mm) -- altura e posicao dos parafusos
Texto   : "A 6-inch strap iron ... three 1/4-inch holes to match the holes in the blocks"

O manual so cotA A = 5 cm para os blocos (a tabela A..M cobre as figs. 1-4).
O resto saiu das figuras:

  A   = 50 mm   meio-passo dos parafusos  (cota "A - CL - A" das figs. 1 e 2)
  bx  = 152 mm  largura da face frontal   (= 6", o comprimento da bracadeira 8)
  bz  = 110 mm  altura do bloco           (fig. 18 medida sobre o tubo OD 60)
  zsp = 55 mm   plano de divisao = eixo do furo horizontal (fig. 18)
  hd  = 6,4 mm  furo de fixacao (VITA: 1/4")
  bore1a = 25 mm  (VITA: 1")
  bore1b = 57 mm  (VITA: 2 1/4")
  cb   = 13 x 6,4 mm contra-furacao do parafuso 14 (VITA: 1/2" x 1/4")

Eixos: X = largura, Y = ao longo do eixo do furo, Z = vertical.
       1A em Y 0..y1a, 1B em Y y1a..y1a+y1b, bracadeira em cima do 1B.
"""
from __future__ import annotations

import math

# --- parametros -------------------------------------------------------------
A = 50.0        # meio-passo dos parafusos (VITA: A = 5 cm)
bx = 152.0      # largura (= bracadeira de 6")
bz = 110.0      # altura do bloco (fig. 18)
hd = 6.4        # furo de fixacao (VITA: 1/4")

y1a = 60.0      # comprimento do 1A ao longo do eixo  (nao cotado)
y1b = 80.0      # comprimento do 1B ao longo do eixo  (nao cotado)

bore1a = 25.0   # VITA: 2,5 cm (1")
bore1b = 57.0   # VITA: 5,7 cm (2 1/4")

cbd = 13.0      # contra-furacao (VITA: 1,3 cm = 1/2")
cbh = 6.4       # profundidade (VITA: 0,6 cm = 1/4")

bw = 30.0       # largura da bracadeira (nao cotada)
bt = 6.0        # espessura da bracadeira (nao cotada)

# --- derivados -------------------------------------------------------------
zsp = bz / 2.0                    # plano de divisao = eixo do furo
hr = hd / 2.0
r1a, r1b = bore1a / 2.0, bore1b / 2.0
ztop1b = zsp + r1b                # coroa do furo do 1B (z = 83,5)

# --- bloco 1A (2 metades = caixa - furo - 2 furos verticais) ---------------
caixa1a = bx * y1a * bz
furo1a = math.pi * r1a**2 * y1a
vpar1a = 2.0 * math.pi * hr**2 * bz
v1a = caixa1a - furo1a - vpar1a

# --- bloco 1B --------------------------------------------------------------
caixa1b = bx * y1b * bz
furo1b = math.pi * r1b**2 * y1b
vpar1b = 2.0 * math.pi * hr**2 * bz
# furo central: so na metade superior, da coroa do furo (83,5) ate o topo (110)
vcentral = math.pi * hr**2 * (bz - ztop1b)
# contra-fura: o cilindro do furo de 6,4 ja esta contido na parte central
vcb = math.pi * (cbd / 2.0) ** 2 * cbh - math.pi * hr**2 * cbh
v1b = caixa1b - furo1b - vpar1b - vcentral - vcb

# --- bracadeira (152 x 30 x 6 - 3 furos) ----------------------------------
vbr = bx * bw * bt - 3.0 * math.pi * hr**2 * bt

# --- totais ----------------------------------------------------------------
total = v1a + v1b + vbr
bbox = ((-bx / 2.0, 0.0, 0.0), (bx / 2.0, y1a + y1b, bz + bt))

if __name__ == "__main__":
    print(f"zsp = {zsp:.1f}   ztop1b = {ztop1b:.1f}   hr = {hr:.2f}")
    print(f"caixa 1A = {caixa1a:12.3f}  -furo {furo1a:9.3f}  -parafusos {vpar1a:9.3f}")
    print(f"V 1A     = {v1a:12.3f} mm3   (2 metades)")
    print(f"caixa 1B = {caixa1b:12.3f}  -furo {furo1b:9.3f}  -parafusos {vpar1b:9.3f}")
    print(f"           -central {vcentral:8.3f}  -contrafura {vcb:8.3f}")
    print(f"V 1B     = {v1b:12.3f} mm3   (2 metades)")
    print(f"bracadeira = {vbr:10.3f} mm3")
    print(f"TOTAL    = {total:12.3f} mm3   corpos = 5")
    print(f"bbox min = {bbox[0]}   bbox max = {bbox[1]}")

    # --- verificacoes de projeto (mesma rigorosidade do trem_tensao) --------
    print("\n--- verificacoes ---")
    print(f"parede acima do tubo      = {zsp - r1b:6.2f} mm   (fig. 18: ~26)")
    print(f"folga parafuso <-> tubo   = {A - hr - r1b:6.2f} mm")
    print(f"folga parafuso <-> borda  = {bx / 2.0 - A - hr:6.2f} mm")
    print(f"folga parafuso 1A <-> furo= {A - hr - r1a:6.2f} mm")
    print(f"parede lateral do furo 1B = {(bx - bore1b) / 2.0:6.2f} mm")
    print(f"metade superior 1B livre  = {bz - ztop1b:6.2f} mm  (furo central + contra-fura {cbh})")
    ok = (zsp - r1b > 20 and A - hr - r1b > 10 and bx / 2.0 - A - hr > 15
          and bz - ztop1b > cbh + 5)
    print(f"aprovado: {ok}")
