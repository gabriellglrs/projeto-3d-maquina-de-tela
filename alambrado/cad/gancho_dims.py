#!/usr/bin/env python3
"""Gancho de sustentação da tela (peça 11 do VITA) — projeto alambrado.

Geometria tirada da **fig. 7** (recuperada do servidor, `ref/clf7x7.gif`) e da
tabela de cotas N–X da fig. 10:

  R = 8,9 cm = 89 mm ... alcance horizontal, centro do olho -> linha da perna
  S = 5,0 cm = 50 mm ... queda vertical, centro do olho -> fundo do U
  T = 2,5 cm = 25 mm ... altura da ponta virada, fundo -> topo da perna
  olho = 0,3 cm (1/8") = 3,2 mm de furo

Arame #10 galvanizado (Ø3,25). O olho da fig. 7 é um laço **achatado**: o arame
dobra 180° e volta paralelo, deixando um furo de 3,2 mm entre as duas pernas.
Modelado como um laço contínuo (mesmo sweep do corpo, sem booleano):

  olho ....... reta de 12 mm + meia-volta de raio 3,225 (furo 3,2)
  corpo ...... reta, dobra 45° r=8, diagonal, U r=10, perna de T

Sistema do desenho: X = alcance, Y = altura (para baixo negativo); a peça é
girada 90° em X no fim, ficando no plano XZ (olho em cima, perna para baixo).

Carga: tela #12, malha 10 cm, 2,44 x 3,0 m ~ 10,2 kg em 9 ganchos = 11,3 N por
gancho; braço no olho = R = 89 mm -> 1,01 N.m. Momento plástico do arame #10
(sigma_y 350 MPa): Mp = sigma_y*d^3/6 = 2,00 N.m -> margem 1,98x.
"""
from __future__ import annotations

import math

# --- parametros (os mesmos do modelo .sc) ----------------------------------
wire_d = 3.25      # arame #10 galvanizado (mm)
wire_r = wire_d / 2.0
eye_r = 3.225      # raio da linha media do laco do olho -> furo 3,20
eye_l = 12.0       # comprimento reto do olho (mm)
R = 89.0           # fig. 7 R (mm)
S = 50.0           # fig. 7 S (mm)
T = 25.0           # fig. 7 T (mm)
b45 = 8.0          # raio da dobra de 45 graus (mm)
u_r = 10.0         # raio do U de baixo (mm)
k = math.sqrt(0.5)

# --- derivados -------------------------------------------------------------
h = -eye_r                         # altura da reta do corpo
u_cx = R - u_r                     # centro do U
u_cy = u_r - S
u_sx = u_cx - u_r * k              # inicio do U (tangente a 45)
u_sy = u_cy - u_r * k
bend_cy = h - b45                  # centro da dobra de 45
bend_ex = None                     # calculado abaixo
drop = S + h - (1.0 - k) * (b45 + u_r)   # queda vertical da diagonal
diag = drop * math.sqrt(2.0)
bend_cx = u_sx - b45 * k - (bend_cy + b45 * k - u_sy)
bend_ex = bend_cx + b45 * k
bend_ey = bend_cy + b45 * k
leg = S - u_r - T                  # perna virada para cima
horizontal = bend_cx

len_path = (eye_l + math.pi * eye_r + horizontal + math.pi * b45 / 4.0
            + diag + 3.0 * math.pi * u_r / 4.0 + leg)
area = math.pi * wire_r * wire_r
vol = area * len_path

# bbox no sistema do desenho (antes da rotacao de 90 graus em X)
xmin, xmax = -(eye_r + wire_r), R + wire_r
ymin, ymax = -(S + wire_r), eye_r + wire_r
# depois da rotacao: X e o alcance, Y = espessura, Z = altura
bbox = (xmax - xmin, wire_d, ymax - ymin)

# --- carga -----------------------------------------------------------------
massa_tela = 10.2                 # kg, painel 2,44 x 3,0 m de malha 10 cm
n_ganchos = 9
f_gancho = massa_tela * 9.81 / n_ganchos       # N
braco = R * 1e-3                  # m (olho -> U)
m_fletor = f_gancho * braco       # N.m
mp = 350e6 * (wire_d / 1000.0) ** 3 / 6.0      # N.m
furo_olho = 2.0 * eye_r - wire_d
boca_u = 2.0 * u_r - wire_d

if __name__ == "__main__":
    print("=== geometria (fig. 7) ===")
    print(f"furo do olho         = {furo_olho:7.3f} mm (1/8\" = 3,2)")
    print(f"boca do U de baixo   = {boca_u:7.3f} mm")
    print(f"alcance X            = {bbox[0]:7.3f} mm  (R = {R:g})")
    print(f"altura Z             = {bbox[2]:7.3f} mm  (S+T+arame)")
    print(f"comprimento de arame = {len_path:7.3f} mm")
    print(f"  olho {eye_l + math.pi*eye_r:7.2f} | reta {horizontal:6.2f} | "
          f"dobra {math.pi*b45/4:5.2f} | diag {diag:6.2f} | "
          f"U {3*math.pi*u_r/4:5.2f} | perna {leg:5.2f}")

    print("\n=== volume ===")
    print(f"area do arame #10    = {area:7.3f} mm2")
    print(f"TOTAL                = {vol:10.3f} mm3   corpos = 1")
    print(f"bbox                 = {bbox[0]:.3f} x {bbox[1]:.3f} x {bbox[2]:.3f}")
    print(f"massa aco 7,85       = {vol/1000.0*7.85:6.2f} g  (9 ganchos = "
          f"{9*vol/1000.0*7.85:.0f} g, {9*len_path/1000.0:.2f} m de arame)")

    print("\n=== carga ===")
    print(f"tela {massa_tela} kg / {n_ganchos} ganchos = {f_gancho:5.1f} N cada")
    print(f"momento no olho      = {m_fletor:5.2f} N.m")
    print(f"momento plastico Mp  = {mp:5.2f} N.m  -> margem {mp/m_fletor:4.2f}x")

    ok = (abs(furo_olho - 3.2) < 0.05 and boca_u > 2.77
          and mp / m_fletor >= 1.5)
    print(f"aprovado: {ok}")
