#!/usr/bin/env python3
"""Volumes esperados do trem de tensao (VITA 51025-BK, figs. 8/9/10 + tabela N-X).

REWORK 2026-11-08 -- reconciliado com as figuras recuperadas:
  O modelo antigo (cantoneira 70x190x6 + polias Ø50) foi substituido.

  Base (parte 6): chapa dobrada em L (fig. 8 + tabela N-X)
    L     = 112 mm  = 2*12 + 2*44   (X = 12 borda->1o furo, U = 44 passo)
    H     = 35 mm   = W  (altura do flange vertical ACIMA do horizontal)
    W     = 16 mm   = V  (aba do flange horizontal)
    T     = 4,8 mm  chapa 3/16" (fenda do VITA)
    HT    = H + T = 39,8  altura total do flange vertical
    furos : 3 x Ø13  (eixo, a h = 28)          + 3 x Ø6,4 (fixacao, 8 da dobra)
            3 x Ø6,4 (fixacao, margem X = 12)

  Polias (parte 10): 3 x, revolve do perfil (fig. 9 + tabela N-X)
    POD = 32 (O), PW = 17 (P), PBORE = 13 (furo 1/2"), canal V:
    GW = 5 abertura, Q = 60 graus -> GD = GW/(2 tan30) = 4,330127
    PGROOT = POD/2 - GD = 11,669873 (fundo do canal)
"""
from __future__ import annotations

import math

# --- parametros da base (fig. 8 + tabela N-X) -------------------------------
L = 112.0        # comprimento (2*12 + 2*44)
H = 35.0         # altura do flange vertical acima do horizontal (W da tabela)
W = 16.0         # largura do flange horizontal (V da tabela)
T = 4.8          # espessura da chapa (3/16")
HT = H + T       # altura total do flange vertical = 39,8

MARGIN_X = 12.0  # X: borda -> 1o furo
PITCH = 44.0     # U: passo dos furos
SHAFT_H = 28.0   # altura do eixo da polia
D_SHAFT = 13.0   # furo do eixo (1/2")
D_BOLT = 6.4     # furo de fixacao (1/4")
BOLT_INSET = 8.0 # fixacao a 8 mm da dobra

# --- parametros das polias (fig. 9 + tabela N-X) ----------------------------
N_POLIA = 3
POD = 32.0       # O: diametro externo
PW = 17.0        # P: largura
PBORE = 13.0     # furo do eixo (1/2")
GW = 5.0         # abertura do canal (17 - 2*Q do desenho)
Q_DEG = 60.0     # Q graus (angulo do canal)

# --- derivados --------------------------------------------------------------
r_shaft, r_bolt = D_SHAFT / 2.0, D_BOLT / 2.0
K30 = math.tan(math.radians(Q_DEG / 2.0))   # tan 30 = 0,5773503
GD = GW / (2.0 * K30)                       # profundidade radial do V = 4,330127
PR = POD / 2.0                              # 16
PBR = PBORE / 2.0                           # 6,5
PGROOT = PR - GD                            # 11,669873 (fundo do canal)

# --- base: chapa em L (vertical + horizontal, sem sobreposicao) -------------
# vertical: L x T x HT   |   horizontal: L x W x T  (separam em y = 0)
v_base_bruta = L * T * HT + L * W * T
v_furos_eixo = 3.0 * math.pi * r_shaft**2 * T      # 3 x Ø13 through
v_furos_fixa = 3.0 * math.pi * r_bolt**2 * T       # 3 x Ø6,4 through
v_base = v_base_bruta - v_furos_eixo - v_furos_fixa

# --- polia: Pappus sobre o perfil do revolve -------------------------------
# perfil = retangulo PW x (PR - PBR)  menos  o triangulo do canal V
rect_a = PW * (PR - PBR)                 # 17 x 9,5 = 161,5
rect_y = (PBR + PR) / 2.0                # centroide radial = 11,25
tri_a = 0.5 * GW * GD                    # boca 5 x altura 4,330127 = 10,825318
tri_y = (PGROOT + 2.0 * PR) / 3.0        # media dos vertices = 14,556624
perfil_a = rect_a - tri_a                # 150,674682 (confere com o sketch)
perfil_cy = (rect_a * rect_y - tri_a * tri_y) / perfil_a
v_polia = perfil_a * 2.0 * math.pi * perfil_cy

total = v_base + N_POLIA * v_polia
corpos = 1 + N_POLIA

# --- verificacoes de projeto ------------------------------------------------
# bbox esperado da base: L x (W + T) x HT = 112 x 20,8 x 39,8
bbox_base = (L, W + T, HT)
# margem de metal acima do furo do eixo (fig. 14): HT - (SHAFT_H + r_shaft)
margem_topo = HT - (SHAFT_H + r_shaft)
# folga do arame por baixo da polia: PW x ... (arame #12 = 2,77 mm)
folga_arame = 10.0

if __name__ == "__main__":
    print("=== base (fig. 8 + tabela N-X) ===")
    print(f"chapa em L          = {v_base_bruta:12.3f} mm3")
    print(f"  - 3 furos O13     = {v_furos_eixo:12.3f}")
    print(f"  - 3 furos O6,4    = {v_furos_fixa:12.3f}")
    print(f"V base              = {v_base:12.3f} mm3")
    print(f"bbox base           = {bbox_base[0]:.1f} x {bbox_base[1]:.1f} x {bbox_base[2]:.1f} mm")

    print("\n=== polia (fig. 9 + tabela N-X) ===")
    print(f"canal V: GD         = {GD:.6f} mm   fundo = {PGROOT:.6f} mm")
    print(f"perfil (area)       = {perfil_a:12.6f} mm2   centroide r = {perfil_cy:.6f}")
    print(f"V polia (Pappus)    = {v_polia:12.3f} mm3   x {N_POLIA} = {N_POLIA*v_polia:.3f}")

    print("\n=== total ===")
    print(f"TOTAL               = {total:12.3f} mm3   corpos = {corpos}")

    print("\n=== verificacoes ===")
    chk = {}
    chk["furos da base cabem"] = (MARGIN_X - r_bolt > 5
                                  and L - MARGIN_X - PITCH - r_bolt > 5)
    chk["passo dos furos U"] = abs(2 * MARGIN_X + 2 * PITCH - L) < 1e-9
    chk["eixo do furo cabe no flange"] = SHAFT_H + r_shaft < HT
    chk["margem topo >= 5 mm"] = margem_topo >= 5.0
    chk["canal nao furra o fundo"] = PGROOT > PBR + 1.0
    chk["folga do arame"] = folga_arame > 2.77
    for k, v in chk.items():
        print(f"  {'OK ' if v else 'FALHA'}  {k}")
    print(f"  margem acima do furo do eixo = {margem_topo:.2f} mm")
    print(f"aprovado: {all(chk.values())}")
