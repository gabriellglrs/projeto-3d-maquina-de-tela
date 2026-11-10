#!/usr/bin/env python3
"""Acoplamento motor <-> virabrequim (projeto alambrado).

Peça FORA do manual VITA (a VITA é manual): liga o eixo do motoredutor à
haste do virabrequim (Ø25,4 mm = 1") que sai do mancal 1A. O manual usa
manivela; a automacao com ESP32 substitui a manivela por este acoplamento.

Geometria (X = comprimento, Y = largura, Z = altura, origem no canto x=0):
  corpo    caixa 72 x 60 x 46, quinas R6 nas 4 arestas paralelas a X
  furo A   Ø25.6 x 36 a partir de x=0  (haste 1", folga 0,2)
  furo B   Ø12.3 x 30 a partir de x=72 (eixo do motor Ø12, folga 0,3)
  fendas   2 fendas de 3 mm (|z| <= 1.5), x 0..30 e x 42..72, largura total
           -> cada ponta vira uma mola que aperta no eixo (castello)
  aperto   4 parafusos M6 x 35, eixo Z, x=15 (fenda A) e x=57 (fenda B),
           y = +-19: folga Ø6.6 no flange superior + piloto Ø5.2 no inferior
  prisioneiro M5 x 20 em x=57, y=0, de z=23 ate o furo B (Ø4.2 x 16,85):
           trava positiva no eixo do motor (contra o derrapagem do castello)

Analise de torque (o que o motor precisa vencer, a 60 rpm):
  plastificacao do arame #12 (d=2,77) ao redor da quina da lamina:
      Mp = sigma_y * d^3/6 = 1,24 N.m      (aco galvanizado, sigma_y=350 MPa)
      P  = Mp * v / R_form                 (v = 0,30 m/s de arame a 60 rpm)
  + arrasto do trem de tensao (50 N a 35 mm de braço)
"""
from __future__ import annotations

import math

# --- parametros geometricos ------------------------------------------------
L = 72.0     # comprimento do corpo
Wy = 60.0    # largura  (Y)
Hz = 46.0    # altura   (Z)
Rf = 6.0     # raio das quinas

d_rod = 25.4        # haste do virabrequim (1")
d_rod_bore = 25.6   # furo A
d_shaft = 12.0      # eixo do motoredutor (padrao)
d_shaft_bore = 12.3 # furo B

slit_t = 3.0        # abertura da fenda (|z| <= 1.5)
slitA = (0.0, 30.0)
slitB = (42.0, 72.0)

bolt_x = (15.0, 57.0)   # posicao X dos 2 apertos (1 por fenda)
bolt_y = 19.0           # Y dos 2 apertos por fenda (+-19)
d_clear = 6.6           # folga M6
d_pilot = 5.2           # piloto M6 (auto-roscante / broca de rosca)
z_top = Hz / 2          # 23: face superior
z_slit_top = slit_t / 2 # 1.5: face do flange superior
z_bot = -slit_t / 2     # -1.5: face do flange inferior
z_pilot_end = -13.0     # fim do piloto

# --- volumes ---------------------------------------------------------------
def strip_area(r: float, h: float) -> float:
    """Area da faixa |z| <= h de um circulo de raio r."""
    return 2.0 * (h * math.sqrt(r * r - h * h) + r * r * math.asin(h / r))

box = L * Wy * Hz
vfil = 4.0 * (Rf * Rf - math.pi * Rf * Rf / 4.0) * L
rA, rB = d_rod_bore / 2, d_shaft_bore / 2
vboreA = math.pi * rA * rA * 36.0
vboreB = math.pi * rB * rB * 30.0
vslit = 2.0 * (slit_t * Wy * 30.0)
# fendas atravessam os furos: devolve a interseccao (nao contar 2x)
vslit_bore = strip_area(rA, slit_t / 2) * 30.0 + strip_area(rB, slit_t / 2) * 30.0
len_clear = z_top - z_slit_top          # 21.5 (nao invade a fenda)
len_pilot = -z_pilot_end - z_slit_top   # 11.5 (de -1.5 a -13)
vbolt = 4.0 * (math.pi * (d_clear / 2) ** 2 * len_clear +
               math.pi * (d_pilot / 2) ** 2 * len_pilot)
# prisioneiro M5 no eixo do motor: de z=23 ate o furo B (z = rB)
d_set, z_set_end = 4.2, rB
vset = math.pi * (d_set / 2) ** 2 * (z_top - z_set_end)

v = box - vfil - vboreA - vboreB - vslit + vslit_bore - vbolt - vset
bbox = ((0.0, -Wy / 2, -Hz / 2), (L, Wy / 2, Hz / 2))

# --- torque ---------------------------------------------------------------
d_wire = 2.77e-3          # arame #12 (mm -> m)
sigma_y = 350e6           # aco galvanizado
Mp = sigma_y * d_wire ** 3 / 6.0          # momento plastico total, N.m
w = 2.0 * math.pi * 60 / 60.0             # 60 rpm em rad/s
v_wire = 0.30                            # m/s de arame por volta de manivela

t_bend = []
for Rf_form in (0.005, 0.0065, 0.008):    # raio de contato na quina da lamina
    P = Mp * v_wire / Rf_form
    t_bend.append((Rf_form, P, P / w))
t_tens = 50.0 * 0.035                    # 50 N de tensao x 35 mm de braco
t_need = t_bend[1][2] + t_tens           # caso de projeto: R=6,5 mm

# capacidade do castello (2 M6 por fenda, pre-aperto M6 a 12 N.m ~= 10 kN)
f_pre = 10000.0                          # N, pre-aperto do M6 a 12 N.m
eta, mu = 0.35, 0.15                     # eficiencia do castello, atrito
t_cap_rod = eta * mu * (2 * 2 * f_pre) * (d_rod_bore / 2) / 1000.0
t_cap_shaft = eta * mu * (2 * 2 * f_pre) * (d_shaft_bore / 2) / 1000.0
# prisioneiro M5 (pre-aperto 4 kN) no eixo do motor: atrito + trava positiva
t_cap_set = mu * 4000.0 * (d_shaft_bore / 2) / 1000.0
t_cap_total = t_cap_shaft + t_cap_set

if __name__ == "__main__":
    print("=== volumes ===")
    print(f"caixa            = {box:12.3f} mm3")
    print(f"- quinas R{Rf:g}     = {vfil:12.3f} mm3")
    print(f"- furo A O{d_rod_bore:g}     = {vboreA:12.3f} mm3")
    print(f"- furo B O{d_shaft_bore:g}     = {vboreB:12.3f} mm3")
    print(f"- 2 fendas 3mm    = {vslit:12.3f} mm3  (+{vslit_bore:.1f} devolvido)")
    print(f"- 4 furos M6      = {vbolt:12.3f} mm3")
    print(f"- prisioneiro M5  = {vset:12.3f} mm3")
    print(f"TOTAL            = {v:12.3f} mm3   corpos = 1")
    print(f"bbox min = {bbox[0]}   bbox max = {bbox[1]}")
    print(f"massa PLA/PETG (1,24 g/cm3) = {v / 1000.0 * 1.24:.1f} g")

    print("\n=== torque @ 60 rpm ===")
    print(f"momento plastico Mp = {Mp:.3f} N.m  (arame #12, sigma_y 350 MPa)")
    for rf, P, T in t_bend:
        print(f"  R_form {rf*1000:3.0f} mm -> P {P:5.1f} W -> T {T:5.1f} N.m")
    print(f"+ tensao do trem de tensao = {t_tens:.2f} N.m")
    print(f"= caso de projeto (R 6,5 mm) T_necessario = {t_need:.1f} N.m")
    print(f"  potencia mecanica = {t_need * w:.0f} W  ->  motor >= ~{t_need * w / 0.6 / 1000 * 1000:.0f} W eletrico (n 0,6)")
    print(f"capacidade castello: haste {t_cap_rod:.1f} N.m | "
          f"eixo motor {t_cap_shaft:.1f} + prisioneiro {t_cap_set:.1f} "
          f"= {t_cap_total:.1f} N.m")

    print("\n=== verificacoes ===")
    wall_bolt = bolt_y - d_rod_bore / 2 - d_clear / 2
    wall_edge = Wy / 2 - bolt_y - d_clear / 2
    ring = slitB[0] - 36.0
    print(f"parede furo A <-> furo M6  = {wall_bolt:6.2f} mm (min 2,5)")
    print(f"parede furo M6 <-> borda   = {wall_edge:6.2f} mm (min 3)")
    print(f"anel solido entre furos    = {ring:6.1f} mm (min 4)")
    print(f"folga haste (0,2)          = {d_rod_bore - d_rod:6.2f} mm")
    print(f"folga eixo motor (0,3)     = {d_shaft_bore - d_shaft:6.2f} mm")
    print(f"fenda A alcance furo A     = {slitA[1] <= 36.0}")
    print(f"fenda B alcance furo B     = {slitB == (42.0, 72.0)}")
    print(f"margem motor 12 N.m @60rpm = {12.0 / t_need:6.2f}x")
    print(f"margem aperto eixo motor   = {t_cap_total / t_need:6.2f}x")
    print("motorizacao: 30 rpm (>=18 N.m) folgado | 60 rpm (12 N.m) no limite,")
    print("             usar soft-start no PWM do ESP32")
    ok = (wall_bolt >= 2.5 and wall_edge >= 3 and ring >= 4
          and 0.1 <= d_rod_bore - d_rod <= 0.4
          and t_cap_total >= t_need and t_need < 12.0
          and vset > 0 and d_shaft_bore - d_shaft > 0)
    print(f"aprovado: {ok}")
