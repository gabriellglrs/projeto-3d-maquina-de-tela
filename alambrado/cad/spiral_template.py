"""
Gabarito 1:1 da fenda helicoidal do cabecote de dobra.

Gera um DXF (e um SVG) com a planificacao do tubo: um retangulo de
largura = circunferencia externa e altura = trecho cortado, com as
linhas da helice marcadas.

Imprima em 1:1 (100%, sem "ajustar a pagina"), recorte e enrole no tubo.
E o que o manual VITA manda fazer com tira de papel -- so que ja cotado.

Uso:
    python spiral_template.py
"""

import math
from pathlib import Path

# ---------------- parametros (iguais ao bending_head.py) ----------------
TUBE_OD = 60.0
TUBE_LEN = 620.0
SLOT_W = 5.0
PITCH = 80.0
UNCUT = 50.0
# -----------------------------------------------------------------------

OUT = Path(r"C:\DEV\3dprint\alambrado\export")
CIRC = math.pi * TUBE_OD
SLOT_LEN = TUBE_LEN - UNCUT
TURNS = SLOT_LEN / PITCH
ANGLE = math.atan(PITCH / CIRC)


def helix_lines():
    """Linhas da helice dentro do retangulo 0..CIRC x 0..SLOT_LEN."""
    # perpendicular offset em Y para a largura da fenda
    dy = SLOT_W / math.cos(ANGLE)
    slope = PITCH / CIRC

    lines = []
    k0 = int(math.floor(-1))
    k1 = int(math.ceil(TURNS)) + 1
    for k in range(k0, k1):
        y0 = k * PITCH
        y1 = y0 + PITCH
        for off in (0.0, dy):
            y0o, y1o = y0 + off, y1 + off
            # recorta em y = 0 e y = SLOT_LEN
            if y1o <= 0 or y0o >= SLOT_LEN:
                continue
            xa, ya = 0.0, y0o
            xb, yb = CIRC, y1o
            if ya < 0:
                xa = (-ya) / slope
                ya = 0.0
            if yb > SLOT_LEN:
                xb = CIRC - (yb - SLOT_LEN) / slope
                yb = SLOT_LEN
            if xb > xa:
                lines.append((xa, ya, xb, yb))
    return lines


def write_dxf(path: Path, lines) -> None:
    """DXF R12 minimo: retangulo + linhas da helice. Unidades em mm."""
    def line(x1, y1, x2, y2, layer="HELICE"):
        return (
            "0\nLINE\n8\n" + layer + "\n"
            f"10\n{x1:.4f}\n20\n{y1:.4f}\n30\n0.0\n"
            f"11\n{x2:.4f}\n21\n{y2:.4f}\n31\n0.0\n"
        )

    parts = [
        "0\nSECTION\n2\nHEADER\n",
        "9\n$INSUNITS\n70\n4\n",          # 4 = milimetros
        "0\nENDSEC\n",
        "0\nSECTION\n2\nENTITIES\n",
    ]
    # moldura
    parts.append(line(0, 0, CIRC, 0, "MOLDURA"))
    parts.append(line(CIRC, 0, CIRC, SLOT_LEN, "MOLDURA"))
    parts.append(line(CIRC, SLOT_LEN, 0, SLOT_LEN, "MOLDURA"))
    parts.append(line(0, SLOT_LEN, 0, 0, "MOLDURA"))
    for x1, y1, x2, y2 in lines:
        parts.append(line(x1, y1, x2, y2))
    parts.append("0\nENDSEC\n0\nEOF\n")
    path.write_text("".join(parts), encoding="ascii")


def write_svg(path: Path, lines) -> None:
    pad = 10.0
    w = CIRC + 2 * pad
    h = SLOT_LEN + 2 * pad
    body = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" '
        f'viewBox="0 0 {w} {h}">',
        f'<rect width="{w}" height="{h}" fill="white"/>',
        f'<g transform="translate({pad},{pad}) scale(1,-1) translate(0,{-SLOT_LEN})">',
        f'<rect x="0" y="0" width="{CIRC}" height="{SLOT_LEN}" fill="none" '
        'stroke="black" stroke-width="0.3"/>',
    ]
    for x1, y1, x2, y2 in lines:
        body.append(
            f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" '
            'stroke="red" stroke-width="0.5"/>'
        )
    body.append("</g>")
    body.append(
        f'<text x="{pad}" y="{h - 2}" font-size="4" font-family="sans-serif">'
        f"tubo OD {TUBE_OD} mm | circunferencia {CIRC:.2f} mm | "
        f"{TURNS:.2f} voltas | passo {PITCH} mm | fenda {SLOT_W} mm | IMPRIMIR 100%"
        "</text>"
    )
    body.append("</svg>")
    path.write_text("\n".join(body), encoding="utf-8")


def main() -> int:
    lines = helix_lines()
    dxf = OUT / "gabarito_fenda.dxf"
    svg = OUT / "gabarito_fenda.svg"
    write_dxf(dxf, lines)
    write_svg(svg, lines)

    print(f"circunferencia    : {CIRC:.2f} mm")
    print(f"altura cortada    : {SLOT_LEN:.2f} mm")
    print(f"voltas            : {TURNS:.3f}")
    print(f"angulo da helice  : {math.degrees(ANGLE):.1f} graus")
    print(f"linhas geradas    : {len(lines)}")
    print(f"gerado            : {dxf.name}  ({dxf.stat().st_size} bytes)")
    print(f"gerado            : {svg.name}  ({svg.stat().st_size} bytes)")
    print()
    print("Imprima em 1:1 (100%, sem ajustar a pagina).")
    print(f"A tira tem {CIRC:.0f} x {SLOT_LEN:.0f} mm -- divide em A4 e emenda.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
