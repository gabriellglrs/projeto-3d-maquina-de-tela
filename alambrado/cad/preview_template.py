"""Pre-visualiza o gabarito da fenda (PNG) a partir das mesmas linhas do DXF."""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
import spiral_template as st

OUT = Path(r"C:\DEV\3dprint\alambrado\export")


def main() -> int:
    lines = st.helix_lines()

    fig, ax = plt.subplots(figsize=(5, 12))
    ax.add_patch(plt.Rectangle((0, 0), st.CIRC, st.SLOT_LEN,
                               fill=False, ec="black", lw=1.2))
    for x1, y1, x2, y2 in lines:
        ax.plot([x1, x2], [y1, y2], color="#c0392b", lw=1.6)

    ax.set_xlim(-5, st.CIRC + 5)
    ax.set_ylim(-10, st.SLOT_LEN + 10)
    ax.set_aspect("equal")
    ax.set_xlabel("desenvolvimento (mm)")
    ax.set_ylabel("comprimento do tubo (mm)")
    ax.set_title(
        f"Gabarito 1:1 — tubo OD {st.TUBE_OD:.0f} mm\n"
        f"{st.CIRC:.1f} x {st.SLOT_LEN:.0f} mm | {st.TURNS:.2f} voltas | "
        f"passo {st.PITCH:.0f} mm | fenda {st.SLOT_W:.0f} mm",
        fontsize=9,
    )
    ax.grid(True, lw=0.3, alpha=0.4)
    fig.tight_layout()

    out = OUT / "gabarito_fenda.png"
    fig.savefig(out, dpi=120)
    print(f"salvo: {out}")
    print(f"linhas: {len(lines)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
