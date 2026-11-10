# 3D Print — CAD por código

Ambiente de modelagem paramétrica para impressão 3D. Tudo roda por script:
o modelo é um arquivo de texto, versionável e reproduzível.

## Estrutura

```
C:\DEV\3dprint\
  cad\        scripts (.py / .scad / .sc) e STL/STEP gerados
  models\     modelos baixados da internet (Printables, MakerWorld...)
  export\     arquivos prontos pra fatiar
  alambrado\  máquina de tela alambrado (cad\ export\ ref\ README.md)
```

> Não coloque nada disso dentro da OneDrive. A biblioteca de STL cresce
> rápido e a sincronização trava a máquina.

## Os quatro caminhos instalados

| Ferramenta | Onde | Quando usar |
|---|---|---|
| **SolidCraft 0.30.1** | `C:\Program Files\SolidCraft` | **Padrão.** CLI headless, `eval` mede o B-rep, STEP/STL/3MF, mecanismos |
| **CadQuery 2.8.0** | `pip` global (Python 3.12) | Peça de engenharia, precisa de STEP, validação numérica |
| **OpenSCAD 2026.11.06** | `C:\DEV\tools\openscad\OpenSCAD-2026.11.06-x86-64` | Peça prismática rápida; editar na mão depois |
| **FreeCAD 1.1.4** | `%LOCALAPPDATA%\Programs\FreeCAD 1.1` | GUI, FEM, ou quando quiser *ver* o modelo montando |

### CadQuery

```powershell
cd C:\DEV\3dprint\cad
python clearance_gauge.py
```

Exporta STL + STEP.

### OpenSCAD

Está no PATH. Pela linha de comando:

```powershell
openscad -o peca.stl -D 'parte="placa"' peca.scad
```

Ou abra o `.scad` na GUI e use o Customizer.

### FreeCAD

**Headless** (sem GUI, via CLI):

```powershell
& "$env:LOCALAPPDATA\Programs\FreeCAD 1.1\bin\freecadcmd.exe" script.py
```

**Pela GUI + MCP** (para o agente controlar ao vivo):

Usa o **MCP Bridge** (`CREATeNG/freecad-mcp-bridge`), que roda o servidor
MCP *dentro* do FreeCAD — sem processo externo, sem dependência.

1. Abrir FreeCAD
2. Clicar o botão **MCP Bridge** na toolbar, ou o botão **MCP Off** na barra
   de status
3. Ele vira **MCP On** e mostra `MCP Bridge: Listening on 127.0.0.1:39280`

Configurado no `opencode.json` como:

```json
"freecad": {
  "type": "remote",
  "url": "http://127.0.0.1:39280/mcp"
}
```

Ferramentas expostas (3):

| Tool | O que faz |
|---|---|
| `execute_python` | Roda Python na sessão viva. `App` e `Gui` já vinculados |
| `execute_python_file` | Roda um `.py` do disco, com `__file__` definido |
| `get_output_page` | Pagina saída longa (`has_more: true`) |

Porta e limites: `Edit → Preferences → MCP Bridge` (porta padrão 39280,
timeout de 15 s por página, página de 32 KB).

> O servidor fica **desligado até você ligar**, a cada sessão. Se as
> ferramentas `freecad` aparecerem desconectadas no OpenCode, é porque o
> botão está em MCP Off.

Alternativa (fallback, desativada no `opencode.json` como `freecad-rpc`):
o `neka-nat/freecad-mcp`, addon `FreeCADMCP` + `uvx freecad-mcp`. Expõe 17
ferramentas estruturadas (criar objeto, FEM, biblioteca de peças,
screenshots) e um `execute_code_headless` que roda num `freecadcmd` separado
— útil porque um crash do OpenCASCADE mata só o processo auxiliar, não a
GUI. Para reativar, trocar `"disabled": true` por `false`.

### SolidCraft (foco total desde 2026-11-08)

**`C:\Program Files\SolidCraft`** — v0.30.1, "parametric 3D CAD", escrito em
Rust sobre o kernel **truck** (ricosjp/truck, Apache-2.0). Licença MIT /
Apache-2.0 (`solidcraft-cli licences`). Interopera por **STEP**.

Por que trocou o FreeCAD como ferramenta principal:

| | FreeCAD + Bridge | SolidCraft |
|---|---|---|
| Precisa ligar a GUI toda sessão | **sim** (MCP Off por padrão) | não — CLI headless |
| Volume/massa direto do B-rep | não (precisa do `check_stl.py`) | **`eval` já devolve** |
| Screenshot | depende da GUI aberta | `snapshot` / `render` headless |
| Script reprodutível | `.py` com macro | **JSON de comandos**, diffável |
| Mecanismos (engrenagem, cames) | não | `joint.gear/cam/screw/solve` |

Três modos de uso:

```powershell
$sc = "C:\Program Files\SolidCraft\solidcraft-cli.exe"

& $sc commands                                   # catálogo completo (6273 linhas)
& $sc eval  design.json                          # mede: volume, massa, área, centro de massa
& $sc run   design.json --out out.step           # executa e exporta
& $sc exec  solid.cylinder '{"radius":10,"height":20}'   # um comando só
& $sc snapshot --in design.json --out shot.png   # imagem headless
```

Um script é um **array JSON** de `{id, params}`:

```json
[{"id":"solid.cylinder","params":{"radius":20,"height":10,"body_name":"disco"}},
 {"id":"solid.cylinder","params":{"radius":8,"height":30,"body_name":"furo",
   "operation":"cut","targets":["disco"]}}]
```

**Armadilhas descobertas na marra:**

1. **`.sc` é JSON.** Um arquivo de texto puro dá `expected value at line 1 column 1`.
2. **`name` nomeia a *feature*; `body_name` nomeia o *body*.** Referências em
   booleanos (`targets`) usam o **body** — usar `name` dá `unknown body`.
3. **Booleano inline:** o comando que cria já aceita `operation` +
   `targets`, dispensa um `solid.combine` separado.
4. **`solid.combine` pede `tools`** (plural, lista) — não `tool`.
5. **Booleanos helicoidais são lentos e superlineares:** 1 volta = 20 s,
   7,12 voltas ≈ **5 min 42 s**. Não é tangência (testado com seção
   superdimensionada: mesmo tempo). Para fenda longa, cortar **1 volta** e
   **repetir em Z** com `solid.pattern.rectangular` (o passo da hélice é
   auto-similar), em vez de um único booleano gigante.
6. **`eval` usa densidade 1,29 g/cm³ (PLA).** Para peça em aço multiplicar
   o volume por 7,85 — o `mass_g` mostrado não serve.
7. **Console Windows é cp1252:** os textos de `params` trazem `→` e quebram
   com `UnicodeEncodeError`. `sc_help.py` já faz
   `sys.stdout.reconfigure(encoding="utf-8")`.
8. **`solidcraft-cli mcp setup --client opencode` não serve aqui:** ele grava
   em `C:\Users\gabri\.config\opencode\opencode.json` (que nem existe) com
   schema `mcp.solidcraft`, enquanto o config real é
   `Projeto Padrão\opencode.json` com `mcp.servers`. Registro manual.
9. **Export bloqueado por padrão** para pastas fora de `recovery`/`temp`.
   Resolver com `--allow-path DIR` nos argumentos do MCP (já em
   `opencode.json`, aponta para `C:\DEV\3dprint`).
10. **`expect` no `batch` é o que garante a peça:** calcula-se o volume
    analíticamente *antes* de construir e o passo falha se não bater.
    `ok: true` sozinho não prova nada.

Ferramenta de consulta: **`cad/sc_help.py`** — imprime o contrato de
qualquer comando (`python sc_help.py solid.coil`, ou regex, ou `--ids`).

Registrado em `opencode.json` como servidor local `solidcraft`
(`solidcraft-cli mcp --allow-path C:\DEV\3dprint`).

## Validação — sempre

Nunca confie no "o CAD disse que é válido". Rode o validador independente:

```powershell
python check_stl.py peca.stl
```

Checa volume, bounding box, triângulos degenerados e **watertight**
(arestas abertas / non-manifold). Aceita STL binário e ASCII.

## Peça de teste: calibrador de folga

`clearance_gauge.*` existe em três versões (CadQuery, OpenSCAD, FreeCAD).
Placa de 78.3 × 20 × 4 mm com 5 furos (8.20 → 8.80 mm) + pino de 8 mm.

Imprima, descubra em qual furo o pino entra com aperto suave, e use essa
folga em todas as peças com encaixe. É o primeiro print mais útil.

| Versão | Volume placa | Watertight |
|---|---|---|
| CadQuery (com fillet) | 5108.55 mm³ | sim |
| FreeCAD (sem fillet) | 5139.17 mm³ | sim |
| OpenSCAD (hull) | 5109.75 mm³ | sim |

A diferença entre CadQuery e FreeCAD (30.6 mm³) é exatamente o volume dos
4 fillets de raio 3 mm. Duas implementações independentes concordando.

## Fatiar no OrcaSlicer (CLI, sem GUI)

OrcaSlicer 2.4.2 em `C:\Program Files\OrcaSlicer\orca-slicer.exe`
(instalado por `winget install SoftFever.OrcaSlicer`).

Os perfis ficam em `C:\DEV\3dprint\orca_profiles\` — **copiados** para fora
de `Program Files` de propósito, porque o CLI do Orca **quebra com espaços no
caminho** dos arquivos de perfil (ele parte o argumento no espaço).

```
orca_profiles\
  machine.json          MyMarlin 0.4 nozzle  (genérica 250x250x250)
  process_base.json     0.20 mm, 3 paredes, gyroid 20%, brim 3 mm
  process_part.json     idem, sem brim
  process_solid.json    100% de preenchimento (peça flexível)
  filament_pla.json     PLA 210/60 C, densidade 1.24
```

Fatiar:

```powershell
pwsh -File C:\DEV\3dprint\cad\slice.ps1 -Stl peca.stl -Profile part
# -Profile: base (com brim) | part (sem brim) | solid (100% infill)
```

Sai `export\<nome>.gcode`.

### Quatro armadilhas do CLI (todas custaram uma rodada)

| Erro | Causa | Correção |
|---|---|---|
| `No such file: Files\OrcaSlicer\...` | caminho com espaço | copiar os perfis pra um diretório sem espaço |
| exit `-17` `CLI_PROCESS_NOT_COMPATIBLE` | em STL puro, o processo **precisa** listar a impressora | `"compatible_printers": ["MyMarlin 0.4 nozzle"]` |
| exit `-51` `CLI_VALIDATE_ERROR` | extrusão relativa exige reset por camada | `"layer_change_gcode": "G92 E0"` |
| massa `0.00 g` no G-code | `inherits` do **filamento** não é resolvido | perfil de filamento completo, com `filament_density` |

Detalhe: a mensagem de erro manda editar `layer_gcode`, mas no 2.4 a chave
é **`layer_change_gcode`**. A mensagem está desatualizada.

E a mesa vem em 35 °C por padrão (chapa "Cool Plate"). Precisa de
`"curr_bed_type": "Textured PEI Plate"` pra usar os 60 °C do PLA.

### Validar o G-code, não só o STL

```powershell
python gcode_stats.py export\peca.gcode     # massa, tempo, camadas, infill
python gcode_check.py export\peca.gcode     # limites XY/Z, temperaturas, G92
python bridge_audit.py export\peca.gcode    # maior vão impresso sobre o ar
python layer_times.py export\peca.gcode     # tempo por camada (risco < 5 s)
python plot_layer.py export\peca.gcode 4.8 camada.png
```

`bridge_audit.py` é o mais útil: mede o **trecho contínuo mais longo impresso
sobre o ar**. Acima de ~5 mm sem apoio, afunda.

`layer_times.py` aproxima o tempo de cada camada pelos feedrates. Ignora
aceleração, então subestima. Camada abaixo de 5 s não dá tempo do plástico
resfriar e a peça deforma.

## Case do ESP32 — v1 vs v2 (fatiado de verdade)

Perfil: 0.4 mm, 0.2 mm de camada, 3 paredes, gyroid 20%, PLA 210/60 °C.

| Peça | Massa | Filamento | Tempo | Camadas |
|---|---|---|---|---|
| base v1 | 7.82 g | 2621 mm | 33m03s | 78 |
| **base v2** | **7.80 g** | 2615 mm | **32m09s** | 78 |
| tampa v1 (plugue maciço) | 4.87 g | 1631 mm | 19m19s | 18 |
| **tampa v2 (anel)** | **4.18 g** | 1401 mm | **15m27s** | 18 |
| clipe (100% infill) | 1.68 g | 564 mm | 9m06s | 15 |

Conjunto v2 completo: **13.66 g**, ~57 min, R$ 1,62.

Tempo por camada (aproximado pelos feedrates): a camada mais rápida é
**11,9 s** na base, **11,2 s** na tampa e **13,2 s** no clipe. Nenhuma abaixo
de 5 s, então nada de plástico mole por camada rápida demais.

### O que a v2 realmente consertou

**Overhang do USB** — medido no G-code, não estimado:

| | maior trecho sobre o ar | onde |
|---|---|---|
| v1 (recorte reto) | **12.68 mm** | Z = 4.80 |
| v2 (recorte em arco) | **1.64 mm** | Z = 6.60 |

Queda de 87%. Em 1.64 mm o bico atravessa sem apoio nenhum — o arco se
fecha sozinho. Em 12.68 mm o fio cede e o teto do recorte afunda.

**Tampa** — a economia real foi menor que a estimada. Eu tinha previsto
7.18 g → 3.8 g olhando o volume maciço, mas o fatiador nunca imprime o
miolo maciço: com 20% de infill ele já era oco. O ganho verdadeiro é
**4.87 → 4.18 g (−14%)** e **19m19s → 15m27s (−20%)**. Ainda vale, mas não
era 76% de desperdício.

## Regras de projeto que evitam falha silenciosa

- **Nunca use tangência exata** entre sólidos que vão passar por booleano.
  Faça as geometrias se sobreporem claramente. Tangência pode fazer o kernel
  descartar o sólido sem erro nenhum.
- Cilindro de corte sempre **mais alto** que a peça, nunca exatamente igual.
- Furo passante: use `h = espessura + 2` e desloque `z = -1`.
- Overhang acima de 45° sem suporte tende a falhar.
- Valide o STL final, não o objeto do CAD.

## Notas de segurança

O addon do FreeCAD expõe `execute_code`, que roda Python arbitrário com as
permissões do teu usuário. Por padrão escuta só em `localhost` e recusa
requisições de navegador. **Não** habilite *Remote Connections* sem
`--auth-token` e sem restringir *Allowed IPs*.
