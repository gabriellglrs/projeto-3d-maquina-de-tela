#!/usr/bin/env python3
"""sc_help.py — imprime a especificacao de comandos do SolidCraft.

O `solidcraft-cli commands` devolve 6273 linhas de JSON com todos os comandos
(id, label, params, tab...). Esta ferramenta filtra pelo id (aceita substring e
regex) e imprime o contrato de cada um, que e o que se precisa para escrever
um script `.json` de modelagem.

Uso:
    python sc_help.py solid.cylinder
    python sc_help.py coil|sweep|thread          # regex
    python sc_help.py --ids                       # so lista os ids
    python sc_help.py --all                       # tudo (enorme)
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

CLI = r"C:\Program Files\SolidCraft\solidcraft-cli.exe"
CACHE = Path(__file__).with_name("solidcraft_commands.json")


def load_commands() -> list[dict]:
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    out = subprocess.run([CLI, "commands"], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    data = json.loads(out.stdout)
    CACHE.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    return data


def main() -> int:
    # o console do Windows e cp1252 e os textos de params trazem "→"
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cmds = load_commands()

    if len(sys.argv) < 2 or sys.argv[1] in ("--ids", "-i"):
        for c in cmds:
            print(f"{c['id']:<34} {c.get('label','')}")
        return 0

    pat = sys.argv[1]
    try:
        rx = re.compile(pat, re.I)
    except re.error:
        rx = re.compile(re.escape(pat), re.I)

    hits = [c for c in cmds if rx.search(c["id"])]
    if not hits:
        print(f"nenhum comando casa com {pat!r}", file=sys.stderr)
        return 1

    for c in hits:
        print("=" * 78)
        print(f"id      : {c['id']}")
        print(f"label   : {c.get('label','')}")
        print(f"tab     : {c.get('tab','')}   panel: {c.get('panel','')}")
        if c.get("disabled_reason"):
            print(f"aviso   : {c['disabled_reason']}")
        print(f"params  :\n  {c.get('params','')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
