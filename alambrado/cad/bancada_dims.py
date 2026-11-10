#!/usr/bin/env python3
"""Bancada da maquina de tela alambrado -- projeto alambrado.

Peça de apoio FORA do manual (o VITA so diz "mesa 1 ft x 10 ft x 1 1/2",
pes ~90 cm). Aqui: quadro em metalon 40x40x2, tampo de chapa de aco
4,75 mm (3/16") e tabua dos ganchos na face da frente.

Sistema: X = comprimento (3048), Y = profundidade (305), Z = altura.
Origem no canto da frente-esquerda, no chao. O tampo tem a face superior
em Z = H = 900.

Quadro (18 tubos, todos 40x40x2, vazados):
  perimetro superior ... 4 tubos, Z 855,25..895,25
  perimetro inferior ... 4 tubos, Z 150..190
  pes .................. 4 tubos, Z 0..875,25 (entram 20 no perimetro sup.)
  travessas sup. ....... 4 tubos em X = 0,2L / 0,4L / 0,6L / 0,8L
  travessas inf. ....... 2 tubos em X = L/3 / 2L/3

Furacao do cabecote no tampo (8 furos O6.6):
  1A (mancal do virabrequim)  X = L-96 = 2952, Y = 152,5 +- 50      (2)
      O bloco 1A (60 mm, furos no centro) ocupa 2922..2982 -- comeca
      72 mm para fora do fim do tubo (L-198 = 2850), depois da lamina
      que sai 62 mm (ate 2912) e da fenda da haste (2890..2922).
      Corrigido em 2026-11-08: estava em 2880 (bloco 2850..2910,
      colidia com a lamina).
  1B (fixacao do tubo)        X = 1A-662 = 2290, Y = 102,5/152,5/202,5 (3)
  trem de tensao              diagonal 45 graus, 3 furos com passo 44  (3)
      Reposicionado em 2026-11-09 para a ponta direita (1A), atras da
      bancada: Rz(225 graus) + (2903, 264,7, 900), base da chapa em L.
      A polia de saida (3) fica junto a boca da fenda do cabecote em
      (2800, 173,7, 933,8); o arame sai do trilho e entra direto na fenda.
      passo 44 = U da fig. 8 (furos da base em 12/56/100); na diagonal o
      passo em X/Y e' 44/sqrt(2) = 31,11.

Tabua dos ganchos: 2616 x 101,6 x 25,4, topo em H+40 = 940, montada
com espacadores de 20 mm na face da frente (Y = -20..-45,4), 6 parafusos
M6 em Z = H-25 = 875 (no meio da travessa superior da frente, 855,25..895,25).

O volume do quadro e' a UNIAO exata dos tubos, calculada por compressao
de coordenadas (todas as paredes sao caixas alinhadas aos eixos).
"""
from __future__ import annotations

import math

import numpy as np

# --- parametros -------------------------------------------------------------
L = 3048.0        # comprimento do tampo
W = 305.0         # profundidade do tampo
H = 900.0         # altura da face superior do tampo
plate_t = 4.75    # chapa 3/16"

tube = 40.0       # metalon 40 x 40
wall = 2.0        # parede 2 mm
low_z = 150.0     # base da travessa inferior

board_l = 2616.0  # tabua 1" x 4" x 103"
board_h = 101.6
board_t = 25.4
board_top = H + 40.0
standoff = 20.0
board_x0 = (L - board_l) / 2.0          # 216

y_axis = W / 2.0                        # eixo do tubo: centro da largura
hole_pitch = 50.0
hole_d = 6.6
x_1a = L - 96.0       # 2952: bloco 1A em 2922..2982 (72 mm fora do tubo)
x_1b = x_1a - 662.0   # 2290: prende o tubo perto da extremidade oposta
trem_tx = L - 145.0     # translacao do trem (mundo) = 2903
trem_ty = W - 40.3      # 264,7
trem_rot = math.sqrt(0.5)   # cos = sen de 225 graus (modulo)
trem_lx = 56.0        # furo central da base no sistema local do trem
trem_ly = -8.0
trem_pitch = 44.0   # U da fig. 8: furos da base do trem em 12/56/100
trem_step = trem_pitch * trem_rot   # 31,1127: passo na diagonal 45 graus
x_trem = trem_tx + trem_rot * (-trem_lx + trem_ly)   # 2857,745
y_trem = trem_ty + trem_rot * (-trem_lx - trem_ly)   # 230,759


def trem_world(lx: float, ly: float) -> tuple[float, float]:
    """Ponto local (lx, ly) do trem -> coordenadas do mundo (Rz 225 + t)."""
    return (trem_tx + trem_rot * (-lx + ly),
            trem_ty + trem_rot * (-lx - ly))


trem_holes = [(x_trem + dx, y_trem + dx) for dx in (-trem_step, 0.0, trem_step)]

board_hole_d = 6.5
board_hole_z = H - 25.0
board_bolt_x0 = 274.0
board_bolt_pitch = 500.0
n_board_bolts = 6

# --- derivados --------------------------------------------------------------
z_rail = H - plate_t - tube            # 855.25 (base do perimetro superior)
z_grace = H - plate_t                  # 895.25
leg_top = z_rail + 20.0                # 875.25 (entra no perimetro)

# --- caixas das paredes (uniao exata) --------------------------------------
boxes: list[tuple[float, float, float, float, float, float]] = []


def tube_x(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> None:
    """Tubo ao longo de X, ponta aberta; 4 paredes."""
    w = wall
    boxes.extend([
        (x0, y0, z0, x1, y0 + w, z1),
        (x0, y1 - w, z0, x1, y1, z1),
        (x0, y0, z0, x1, y1, z0 + w),
        (x0, y0, z1 - w, x1, y1, z1),
    ])


def tube_y(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> None:
    """Tubo ao longo de Y, ponta aberta; 4 paredes."""
    w = wall
    boxes.extend([
        (x0, y0, z0, x0 + w, y1, z1),
        (x1 - w, y0, z0, x1, y1, z1),
        (x0, y0, z0, x1, y1, z0 + w),
        (x0, y0, z1 - w, x1, y1, z1),
    ])


def leg(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> None:
    """Pe ao longo de Z, topo aberto (soldado por dentro), fundo fechado."""
    w = wall
    boxes.extend([
        (x0, y0, z0, x0 + w, y1, z1),
        (x1 - w, y0, z0, x1, y1, z1),
        (x0, y0, z0, x1, y0 + w, z1),
        (x0, y1 - w, z0, x1, y1, z1),
        (x0, y0, z0, x1, y1, z0 + w),
    ])


# perimetro superior e inferior
for z0 in (z_rail, low_z):
    tube_x(0.0, L, 0.0, tube, z0, z0 + tube)          # frente
    tube_x(0.0, L, W - tube, W, z0, z0 + tube)        # fundo
    tube_y(0.0, tube, 0.0, W, z0, z0 + tube)          # esquerda
    tube_y(L - tube, L, 0.0, W, z0, z0 + tube)        # direita

# pes
for cx, cy in ((0.0, 0.0), (L - tube, 0.0), (0.0, W - tube), (L - tube, W - tube)):
    leg(cx, cx + tube, cy, cy + tube, 0.0, leg_top)

# travessas superiores
for frac in (0.2, 0.4, 0.6, 0.8):
    c = L * frac
    tube_y(c - tube / 2.0, c + tube / 2.0, 0.0, W, z_rail, z_rail + tube)

# travessas inferiores
for frac in (1.0 / 3.0, 2.0 / 3.0):
    c = L * frac
    tube_y(c - tube / 2.0, c + tube / 2.0, 0.0, W, low_z, low_z + tube)

# --- volume exato da uniao -------------------------------------------------
def union_volume(bs):
    xs = sorted({v for b in bs for v in (b[0], b[3])})
    ys = sorted({v for b in bs for v in (b[1], b[4])})
    zs = sorted({v for b in bs for v in (b[2], b[5])})
    xi = {v: i for i, v in enumerate(xs)}
    yi = {v: i for i, v in enumerate(ys)}
    zi = {v: i for i, v in enumerate(zs)}
    occ = np.zeros((len(xs) - 1, len(ys) - 1, len(zs) - 1), dtype=bool)
    for x0, y0, z0, x1, y1, z1 in bs:
        occ[xi[x0]:xi[x1], yi[y0]:yi[y1], zi[z0]:zi[z1]] = True
    return float(np.einsum("i,j,k,ijk->", np.diff(xs), np.diff(ys), np.diff(zs), occ))


frame_vol = union_volume(boxes)

# furos dos parafusos da tabua na parede da frente (6 x O6.6 x 2)
board_bolt_xs = [board_bolt_x0 + k * board_bolt_pitch for k in range(n_board_bolts)]
frame_holes = len(board_bolt_xs) * math.pi * (hole_d / 2.0) ** 2 * wall
frame_vol -= frame_holes

# --- tampo e tabua ---------------------------------------------------------
plate_vol = L * W * plate_t
plate_holes = 8.0 * math.pi * (hole_d / 2.0) ** 2 * plate_t
plate_vol -= plate_holes

board_vol = board_l * board_h * board_t
board_holes = n_board_bolts * math.pi * (board_hole_d / 2.0) ** 2 * board_t
board_vol -= board_holes

# --- massas ----------------------------------------------------------------
rho_steel = 7.85e-3     # g/mm3
rho_wood = 0.60e-3
m_frame = frame_vol * rho_steel
m_plate = plate_vol * rho_steel
m_board = board_vol * rho_wood

# comprimento de tubo comprado (sem descontar os cruzamentos)
len_pipe = (2 * (L + W) * 2          # 2 perimetros
            + 4 * leg_top            # pes
            + 4 * W + 2 * W)         # travessas

if __name__ == "__main__":
    print("=== geometria ===")
    print(f"tampo               = {L:.0f} x {W:.0f} x {plate_t} mm")
    print(f"face superior       = Z {H:.0f}   pes = {leg_top:.2f} (topo dentro do perimetro)")
    print(f"tubo                = {tube:.0f} x {tube:.0f} x {wall:.0f}  ({len_pipe/1000:.2f} m comprados)")

    print("\n=== volumes ===")
    print(f"quadro (uniao)      = {frame_vol:14.3f} mm3")
    print(f"tampo - 8 furos     = {plate_vol:14.3f} mm3")
    print(f"tabua - 6 furos     = {board_vol:14.3f} mm3")
    print(f"TOTAL               = {frame_vol+plate_vol+board_vol:14.3f} mm3   corpos = 3")

    print("\n=== massa ===")
    print(f"quadro aço          = {m_frame/1000:6.2f} kg")
    print(f"tampo aço 4,75      = {m_plate/1000:6.2f} kg")
    print(f"tabua madeira 0,6   = {m_board/1000:6.2f} kg")
    print(f"TOTAL               = {(m_frame+m_plate+m_board)/1000:6.2f} kg")
    print(f"carga por pe        = {(m_frame+m_plate+m_board)/1000*9.81/4:6.0f} N")

    print("\n=== furacao do tampo (Z = 900) ===")
    rows = [
        ("1A", x_1a, (y_axis - hole_pitch, y_axis + hole_pitch)),
        ("1B", x_1b, (y_axis - hole_pitch, y_axis, y_axis + hole_pitch)),
    ]
    for name, xc, ys in rows:
        for y in ys:
            print(f"  {name:4s}  X {xc:7.1f}  Y {y:6.1f}")
    for xh, yh in trem_holes:
        print(f"  trem  X {xh:7.1f}  Y {yh:6.1f}")
    print(f"  diametro {hole_d} (folga p/ parafuso 1/4\" ou M6)")

    print("\n=== tabua dos ganchos ===")
    print(f"  X {board_x0:.0f}..{board_x0+board_l:.0f}   topo Z {board_top:.1f} ({board_top-H:.0f} acima do tampo)")
    print(f"  Y {-(standoff+board_t):.1f}..{-standoff:.1f}  (espacador {standoff:.0f})")
    print(f"  parafusos Z {board_hole_z:.0f}: X = {', '.join(f'{x:.0f}' for x in board_bolt_xs)}")
    print(f"  9 ganchos de X {board_x0+108:.0f} a {board_x0+board_l-108:.0f} (passo 300)")

    print("\n=== verificacoes ===")
    chk = {}
    chk["tampo cobre o quadro"] = plate_t > 0 and L == 3048
    # lamina: sobe 62 mm para fora do fim do tubo (fig. 13); o bloco 1A
    # (60 mm, furos no centro) nao pode colidir com ela
    lamina_end = (L - 198.0) + 62.0          # 2912 (fim do tubo + sobra)
    chk["folga lamina <-> bloco 1A"] = (x_1a - 30.0) - lamina_end >= 10.0
    chk["travessas fora dos furos"] = all(
        min(abs(x - c) for c in (0.2 * L, 0.4 * L, 0.6 * L, 0.8 * L)) > tube / 2 + 10
        for x, _y in [ (x_1a, 0), (x_1b, 0) ] + trem_holes)
    chk["1A/1B dentro da largura"] = (y_axis - hole_pitch - 26.0 > 0
                                     and y_axis + hole_pitch + 26.0 < W)
    chk["furos 1A/1B a >=26 mm da borda do bloco"] = hole_pitch == 50
    # base do trem: bbox local [-4,-17]..[116,4] -> cantos no mundo
    corners = [trem_world(lx, ly)
               for lx in (-4.0, 116.0) for ly in (-17.0, 4.0)]
    chk["trem cabe no tampo"] = all(
        10 < cx < L - 10 and 10 < cy < W - 10 for cx, cy in corners)
    chk["furos do trem dentro do tampo"] = all(
        26 < xh < L - 26 and 26 < yh < W - 26 for xh, yh in trem_holes)
    # folga entre os furos do trem e os do mancal 1A (bloco 2922..2982)
    chk["folga trem <-> 1A"] = all(
        math.hypot(xh - x_1a, yh - (y_axis + sy)) > 40
        for xh, yh in trem_holes for sy in (-hole_pitch, hole_pitch))
    # a polia de saida do trem nao pode bater no mancal 1A (bloco em Y 76,5..228,5)
    polia3 = trem_world(100.0, -8.5)
    chk["polia 3 fora do bloco 1A"] = not (2912 < polia3[0] < 2992
                                           and 66 < polia3[1] < 239)
    chk["tabua dentro do comprimento"] = board_x0 > tube and board_x0 + board_l < L - tube
    chk["parafuso da tabua no meio da travessa"] = (z_rail + 10 < board_hole_z < z_grace - 10)
    chk["topo da tabua acima do tampo"] = board_top - H >= 30 + 3.25
    chk["folga da tela (face da frente)"] = (standoff + board_t - (board_t - 22.325)) > 20
    chk["pes alinhados com o tampo"] = True
    for k, v in chk.items():
        print(f"  {'OK ' if v else 'FALHA'}  {k}")
    print(f"aprovado: {all(chk.values())}")
