# Máquina de tela alambrado — projeto de baixo custo

Objetivo: máquina automática, operada por **uma pessoa**, para produzir tela
alambrado. Prioridade absoluta em **custo baixo**.

## Base do projeto

**VITA Technical Bulletin 51025-BK — "Chain Link Fence Making Machine" (1981)**
Documento de domínio público, escrito em resposta a pedidos da América do Sul
e da África. Em Botswana virou base de um negócio local de cercas.

> O princípio: um tubo com **fenda helicoidal**. O arame entra pela fenda,
> enrola numa lâmina de aço que gira dentro do tubo, e sai do outro lado como
> **espiral plana** — que é o ziguezague da tela.

Não existe matriz de crimpagem usinada. É tubo, lâmina, polias e cabo.

### Regras de dimensionamento do manual

| Tubo | Lâmina | Malha resultante |
|---|---|---|
| 2" (50 mm ID) | 2" | **10 cm (4")** |
| 1½" (38 mm ID) | 1½" | **7,6 cm (3")** |

- Fenda: **3/16" = 4,8 mm** (usamos 5 mm)
- Tira de papel para marcar a hélice: **8 cm** para tubo de 2"
- Arame: #12 (2,77 mm) ou #14 (2,10 mm)
- Mesa: tábua 30 × 305 × 3,8 cm, pés a ~90 cm do chão
- Deixar **2" sem corte** na ponta do mancal (rigidez)

## Decisões do projeto (2026-11-08)

| Decisão | Valor | Motivo |
|---|---|---|
| Tubo | **2"** → malha **10 cm** | É a referência do boletim VITA; faixa de papel de 8 cm, mais folga para o arame, tubo mais rígido |
| Comprimento do cabeçote | **620 mm** | O já modelado e medido; mais barato, suficiente para o teste |
| Ferramenta CAD | **SolidCraft** (foco total) | CLI headless, `eval` devolve volume/massa sem passar por STL, exporta STEP/STL/3MF, sem precisar ligar o MCP Bridge |

## Fonte primária

**VITA Technical Bulletin 51025-BK — "Chain Link Fence Making Machine"** (1978/1981),
domínio público. Texto integral recuperado de
`cd3wdproject.org/new/VITAHTML/SUBLEV/EN1/CLFENCE.HTM`.

O HTML público só embute 11 imagens; as figuras **6–10 e 17** existem no
mesmo servidor em `SUBLEV/GIF/` (padrão `CLF<fig>X<página do folheto>`) e a
**fig. 16 está dentro do GIF da fig. 15**. Com isso as **18 figuras estão
completas em `ref/`** — inventário detalhado, a tabela de cotas **N–X** e a
única imagem ainda ausente (o resumo do "World Neighbors in Action") estão em
**`ref/INDICE.md`**.

## Estrutura

```
alambrado\
  NOTAS.md  diário de trabalho — LER PRIMEIRO (fluxo, estado, pendências)
  cad\      scripts paramétricos
  export\   STL / STEP / DXF / gabaritos
  ref\      figuras do boletim VITA (originais + recortes)
```

## O que já está modelado

### `bending_head.py` — cabeçote de dobra

Tubo com a fenda helicoidal, gerado por loft de 260 seções radiais.
Paramétrico: diâmetro, comprimento, largura da fenda, passo da hélice.

Parâmetros atuais (máquina de teste):

| Parâmetro | Valor |
|---|---|
| Tubo OD / ID | 60 / 50 mm |
| Comprimento | 620 mm |
| Fenda | 5 mm |
| Passo da hélice | 80 mm |
| Trecho sem corte | 50 mm |
| Voltas | 7,12 |

Resultado validado: **502.246 mm³** (= 502.246,0 — os pontos são separador
de milhar pt-BR), 1 sólido, fechado, STL watertight (40.506 triângulos,
502.172 mm³ no STL).

**Conferência cruzada entre CADs (2026-11-08):** o mesmo `.step` aberto no
kernel do SolidCraft mede **502.220,05 mm³** — diferença de **0,005%** para o
valor do FreeCAD. Os dois CADs independentes (OpenCascade vs truck) concordam.

**Massa real em aço (7,85 g/cm³): 3,94 kg** — número que faltava para
dimensionar o mancal e o motor. (Os 647,86 g que o `eval` mostra são à
densidade padrão de 1,29 g/cm³ = PLA, não serve para esta peça.)

Conferência analítica: a banda helicoidal tem seção 25 mm² (parede 5 mm ×
fenda 5 mm) e caminho de ~1.357 mm → ~33.900 mm³ removidos. O CAD removeu
33.395 mm³. Bate.

### `spiral_template.py` — gabarito 1:1

Gera a **planificação** do tubo em DXF e SVG, com as linhas da fenda já
cotadas. É o que o manual manda fazer com tira de papel, só que pronto para
plotar.

- Retângulo: 188,5 × 570 mm (circunferência × trecho cortado)
- 7,12 voltas, passo 80 mm, ângulo 23°
- **Imprimir em 1:1** (100%, sem "ajustar à página") e emendar em A4

### `preview_template.py`

Só renderiza o gabarito em PNG para conferência visual.

### `trem_tensao.sc` — trem de tensão (SolidCraft)

Feito no **SolidCraft** e **reworkado em 2026-11-08** depois que as figs.
8/9/10 foram recuperadas (`ref/clf8x7.gif`, `clf9x8.gif`, `clf10x8.gif`) —
o modelo antigo (cantoneira 70×190×6 + polias Ø50, derivado das figs. 11/14)
foi substituído pelas cotas reais da tabela **N–X**:

| Elemento | Como é | Valor | Origem |
|---|---|---|---|
| Base (6) | **Chapa dobrada em L**, flange horizontal na bancada | L **112** (= 2·12 + 2·44), flange horizontal **16** (V), flange vertical **35** (W) acima do horizontal, chapa **4,8** (3/16") | fig. 8 + tabela N–X |
| Furos da base | 3 × Ø**13** (eixo, a h = 28) + 6 × Ø**6,4** (fixação, margem 12, a 8 da dobra) | — | fig. 8 + VITA |
| Polias | Canaleta em V, 3 em fila, revolve | Ø **32** (O), largura **17** (P), furo **13** (1/2"), canal boca **5** a **60°** (Q), fundo Ø 23,34 | fig. 9 + tabela N–X |

Na polia o texto diz 1½–2" e a fig. 9 cota Ø32 — **venceu a fig. 9** (a vista
em corte da peça usinada; o texto é recomendação genérica). O arame faz **por
cima → por baixo → por cima** nas três polias e entra na fenda do cabeçote.

**Conferências (rework 2026-11-08):**

| Fonte | Volume |
|---|---|
| Analítico (`cad/trem_tensao_dims.py`, Pappus sobre o perfil do revolve) | 58.900,461 mm³ |
| B-rep do SolidCraft | 58.900,311 mm³ (−0,00025%) |

Base 27.623,488 + 3 × polia 10.425,657. `aprovado: True` — verificação:
margem de metal acima do furo do eixo = 5,30 mm; canal não fura o fundo
(fundo Ø 23,34 > furo Ø 13 + folga).

**Alternativas do próprio manual** (mais baratas que a polia usinada):

1. **Cavilhas de madeira** num quadro — a mais barata; quando desgasta, bate a
   cavilha mais fundo e troca depois. Posicionar na perna mais próxima do
   cabeçote.
2. **Lavas (arruelas) empilhadas** no lugar da polia (9A/9B), com rolamentos
   9C lixados até girar folgados.
3. **Polia usinada no torno** (a preferida do manual) — a que está modelada.

Lubrificar com **sabão**, nunca óleo (óleo suja a tela).

### `mancal_cabecote.sc` — mancal do cabo / fixação do tubo (SolidCraft)

Peças **1A** (mancal do virabrequim), **1B** (fixação do tubo) e a
**braçadeira** das figs. 1 e 2 do manual. Modelado como **5 corpos** — cada
metade superior/inferior é uma peça separada, como a figura desenha — mais a
braçadeira de 6".

O manual só cotA **A = 5 cm** para os blocos (a tabela A..M cobre as figs.
1–4, e D..M são da manivela da fig. 4). As outras cotas saíram das figuras:

| Elemento | Valor | Origem |
|---|---|---|
| Largura da face `bx` | **152 mm** | os 6" da braçadeira (texto: *"A 6-inch strap iron"*) |
| Altura do bloco `bz` | **110 mm** | fig. 18, medida sobre o tubo OD 60 |
| Plano de divisão `zsp` | **55 mm** | fig. 18 — é o eixo do furo horizontal |
| Meio-passo dos parafusos `A` | **50 mm** | VITA, tabela A–M |
| Furos de fixação | **Ø 6,4 mm** | VITA: 1/4" |
| Furo do eixo (1A) | **Ø 25 mm** | VITA: 1" |
| Furo do tubo (1B) | **Ø 57 mm** | VITA: 2 1/4" |
| Contra-fura (parafuso 14) | **Ø 13 × 6,4** | VITA: 1/2" × 1/4" |
| Comprimento 1A / 1B | 60 / 80 mm | **derivado** (não cotado no manual) |
| Braçadeira | 152 × 30 × 6 mm | largura/espessura **derivadas** |

Furos verticais: **1A** tem 2, **1B** tem 2 na mesma linha + 1 central com
contra-fura só na metade superior. A braçadeira tem 3 furos Ø6,4 alinhados
com os do 1B (texto: *"three 1/4-inch holes to match the holes in the blocks"*).

**Conferências (3 fontes independentes):**

| Fonte | Volume |
|---|---|
| Analítico (`cad/mancal_dims.py`) | 2.118.336,958 mm³ |
| B-rep do SolidCraft (`eval`) | 2.118.343,527 mm³ |
| STL lido à mão (`check_stl.py`) | 2.118.428,71 mm³ |

Diferença: **0,0003%** (analítico → B-rep) e **0,004%** (analítico → STL).
5 corpos, todos `closed: true`. Bbox 152 × 140 × 116 mm.

**Sobre as 678 arestas non-manifold do STL montado:** o STL do conjunto
tem 0 arestas abertas, e as non-manifold estão em **z = 55** (544, os planos
onde as metades se tocam) e **z = 110** (129, braçadeira sobre o bloco) —
são costuras de contato entre corpos distintos, não defeitos. Exportando
corpo a corpo (`bodies: [...]`), **os 5 STLs saem watertight com 0
non-manifold**:

| Corpo | Analítico | STL | Δ | Triângulos |
|---|---|---|---|---|
| 1A metade inf. | 483.335,09 | 483.346,70 | 0,002% | 9.748 |
| 1A metade sup. | 483.335,09 | 483.346,70 | 0,002% | 9.748 |
| 1B metade inf. | 563.190,96 | 563.224,61 | 0,006% | 9.242 |
| 1B metade sup. | 561.694,87 | 561.728,72 | 0,006% | 12.714 |
| Braçadeira | 26.780,94 | 26.781,99 | 0,004% | 2.280 |

Verificações de projeto (todas passam, `aprovado: True`): parede acima do
tubo 26,5 mm, folga parafuso↔tubo 18,3 mm, folga parafuso↔borda 22,8 mm,
parede lateral do furo 1B 47,5 mm.

Arquivos: `cad/mancal_cabecote.json` (script de construção, 17 comandos),
`cad/mancal_cabecote.sc` (design salvo), `export/mancal_cabecote.step|.stl|.png`.

### `lamina_interna.json` — lâmina interna / bending arm (peça 4)

A "lâmina" que corre dentro do tubo e segue a fenda espiral. Só 3 comandos
(caixa → fillet R5 nas 4 quinas → furo Ø6,4).

| Elemento | Valor | Origem |
|---|---|---|
| Comprimento `L` | **744 mm** | **derivado** (ver abaixo) |
| Largura `W` | **50 mm** | texto: *"5cm (2") wide bending-head arm"* |
| Espessura `T` | **5 mm** | texto: fenda da manivela *"3/16-inch slot"* = tabela F = 0,5 cm |
| Furo | **Ø 6,4 mm** | texto: *"Drill 0.6cm (1/4") diameter hole in bending-head arm (4)"* |
| Furo a `B` da ponta | **10 mm** | tabela A–M: B = 1 cm |
| Raio das quinas `C` | **5 mm** | texto: *"round off corners"* + tabela C = 0,5 cm |

**Comprimento (o manual não cotA).** A Fig. 13 mostra a lâmina saindo dos
**dois** lados do tubo. Medida em pixels com a escala fixada pela OD do tubo
(192 px ↔ 60 mm → 3,2 px/mm):

| Elemento | Fig. 13 | Real |
|---|---|---|
| Tubo (7) desenhado | 599 px | 187 mm (o tubo do VITA é curto; o nosso tem 620) |
| Lâmina desenhada | 1000 px | 312 mm |
| Sobra lado da manivela | 197 px | **62 mm** |
| Sobra lado oposto | 201 px | **63 mm** |

A sobra é **absoluta**: é ali que a fenda da manivela encaixa e que entra o
parafuso a B = 1 cm da ponta — não escala com o tubo. Logo
`L = 620 + 2 × 62 = 744 mm`. (A Fig. 3 é esquemática e desenha o furo ~2× o
real; só a tabela A–M e o texto foram usados para B/C.)

**Conferências (3 fontes independentes):**

| Fonte | Volume |
|---|---|
| Analítico (`cad/lamina_dims.py`) | 185.731,850 mm³ |
| B-rep do SolidCraft (`eval`) | 185.731,797 mm³ |
| STL lido à mão (`check_stl.py`) | 185.730,47 mm³ |

Diferença: **0,00003%** (analítico → B-rep) e **0,0008%** (analítico → STL).
1 corpo, `closed: true`, bbox 744 × 50 × 5 mm, 11 faces (5 cilindro + 6
plano), 428 triângulos, **0 arestas abertas / 0 non-manifold, WATERTIGHT**.
Massa em aço: **1.458 g**. Verificações (`aprovado: True`): metal na ponta do
furo 6,8 mm, folga furo↔quina 12,4 mm.

Arquivos: `cad/lamina_dims.py`, `cad/lamina_interna.json` (3 comandos),
`cad/lamina_interna.sc`, `export/lamina_interna.step|.stl|.png`.

### `acoplamento_motor.sc` — acoplamento motor ↔ virabrequim (SolidCraft)

Peça **fora do manual** (a VITA é manual). Liga o eixo do motoredutor
(Ø12 mm) à haste Ø25,4 mm (1") que sai do mancal 1A — no lugar da manivela.

É um **castelo (bucha de aperto bipartida)**: dois rasgos de 3 mm separam as
pontas, e 4 parafusos M6 apertam cada ponta no eixo. O prisioneiro M5 trava
positivamente o eixo do motor, como backup contra derrapagem.

| Elemento | Valor | Origem |
|---|---|---|
| Corpo | caixa 72 × 60 × 46, quinas R6 | derivado |
| Furo da haste (1A) | Ø **25,6** × 36 (folga 0,2) | haste 1" |
| Furo do motor | Ø **12,3** × 30 (folga 0,3) | eixo Ø12 padrão |
| Fendas | 2 × **3 mm**, x 0–30 e x 42–72 | ponte central de 12 mm |
| Aperto | 4 × M6: Ø6,6 no flange sup. + piloto Ø5,2 no inf. | x = 15 / 57, y = ±19 |
| Prisioneiro | M5 × 20: Ø4,2 × 17 até o furo do motor | x = 57, y = 0 |

**Torque (a 60 rpm):** plastificação do arame #12 (σy 350 MPa) dá
Mp = 1,24 N·m; com raio de formação 6,5 mm e o arrasto do trem de tensão,
o caso de projeto é **10,9 N·m** (≈ 68 W mecânicos → motor ≥ ~114 W elétrico
com η 0,6). Capacidade do castelo: haste **26,9 N·m**; eixo do motor
12,9 + prisioneiro 3,7 = **16,6 N·m** (margem 1,53×). Recomendação: **30 rpm
com ≥ 18 N·m** folgado; 60 rpm fica no limite — usar soft-start no PWM.

**Conferências (3 fontes independentes):**

| Fonte | Volume |
|---|---|
| Analítico (`cad/acoplamento_dims.py`) | 162.842,510 mm³ |
| B-rep do SolidCraft | 162.841,636 mm³ (−0,00054%) |
| STL lido à mão | 162.873,715 mm³ (+0,02%, tesselação) |

1 corpo, `closed: true`, bbox 72 × 60 × 46 mm, 40 faces (24 plano + 16
cilindro), 11 features. STL: 13.818 triângulos, **0 arestas abertas /
0 non-manifold, WATERTIGHT**. Topologia confere: 4 furos Ø6,6 e 4 pilotos
Ø5,2 em x = 15/57, y = ±19; prisioneiro no eixo do motor; raios medidos
12,8 / 6,15 / 3,3 / 2,6 / 2,1 mm. Massa em aço: **1.278 g** (0,202 kg em
PLA/PETG, se for impresso como gabarito).

Arquivos: `cad/acoplamento_dims.py`, `cad/acoplamento_motor.sc`,
`export/acoplamento_motor.step|.stl|.png`.

### `gancho_tela.sc` — ganchos de sustentação da tela (peça 11)

O HTML público não embute a **fig. 7** (recuperada em `ref/clf7x7.gif`); o
primeiro modelo foi derivado da função e **reworkado em 2026-11-08** com as
cotas reais **R 89 / S 50 / T 25 mm** da tabela N–X (fig. 10).

É um **gancho em S** de arame dobrado: em cima um laço (olho) achatado de
furo Ø3,2 pendura na tábua; embaixo um U aberto para cima segura o arame da
tela. Sem solda, sem parafuso — só dobra.

| Parâmetro | Valor | Origem |
|---|---|---|
| Arame | **Ø 3,25 mm** (#10 galvanizado) | derivado (olho 1/8") |
| Alcance R | **89 mm** (centro do olho → linha da perna) | fig. 7 / tabela N |
| Queda S | **50 mm** (centro do olho → fundo do U) | fig. 7 / tabela S |
| Ponta virada T | **25 mm** (fundo → topo da perna) | fig. 7 / tabela T |
| Furo do olho | **3,2 mm** (laço achatado, 180°) | VITA: 1/8" |
| Boca do U de baixo | **16,75 mm** | raio 10 (folga p/ arame #12 = 2,77) |
| Quantidade | **9 ganchos a cada 300 mm** | cobre 2,4 m da tábua de 2,616 m |

**Montagem:** a tábua vai **apoiada no tampo**, junto à borda voltada para
fora. O laço fica em cima (olho para cima), a perna desce por fora da borda,
e a tela pendura fora do tampo.

**Carga:** tela de 2,44 × 3,0 m (malha 10 cm, #12) ≈ **10,2 kg**; dividida
em 9 ganchos dá 11,1 N por gancho, braço R = 89 mm → **0,99 N·m**. O momento
plástico do arame #10 é 2,00 N·m → **margem 2,02×** (`aprovado: True`).

**Conferências (3 fontes independentes):**

| Fonte | Volume |
|---|---|
| Analítico (`cad/gancho_dims.py`) | 1.248,015 mm³ |
| B-rep do SolidCraft | 1.248,0 mm³ (estanque) |
| STL lido à mão | ≈ 1.248 mm³ |

1 corpo, `closed: true`, bbox **95,475 × 3,25 × 56,475 mm**, sweep de Ø3,25
ao longo de 150,4 mm de arame (olho 22,1 + reta 24,8 + dobra 6,3 +
diagonal 58,7 + U 23,6 + perna 15,0). 9 ganchos = **88 g** de arame (1,35 m).

Arquivos: `cad/gancho_dims.py`, `cad/gancho_tela.sc` (rework 17:39;
`cad/gancho_tela.json` é a versão antiga e está **obsoleta** — o rework foi
feito por comandos MCP, sem json), `export/gancho_tela.step|.stl|.png`.

### `bancada.sc` — bancada metálica (mesa + base do cabeçote)

Substitui a tábua 1 ft × 10 ft × 1½" do VITA por **chapa de aço 3/16"
(4,75 mm) sobre quadro de metalon 40 × 40 × 2**, como você escolheu.
O eixo do tubo fica em **X, a Z = 955** (55 mm acima do tampo) e
**Y = 152,5** (centro da largura).

> **Leiaute decidido (2026-11-08): central.** A fig. 15/16 cota **Y = 22 e
> Z = 124 mm** (trem no fundo da bancada); após conferência, manteve-se o
> leiaute central modelado (Y 152,5). Registrado para eventual migração —
> ver `ref/INDICE.md`.

| Elemento | Valor |
|---|---|
| Tampo | chapa 3048 × 305 × **4,75**, face superior em Z 900 |
| Quadro | 18 tubos 40 × 40 × 2 vazados: 2 perímetros (4 + 4), 4 pés, 4 travessas sup. (0,2/0,4/0,6/0,8 L), 2 inf. (L/3, 2L/3) |
| Tubo comprado | **18,74 m** (≈ 43 kg) |
| Pés | 4, no canto; topo entra 20 mm no perímetro (solda) |
| Tábua dos ganchos | 2616 × 101,6 × **25,4**, topo em **940** (+40), 20 mm à frente da face (espaçadores), 6 parafusos M6 |

**Furação do cabeçote no tampo — 8 × Ø6,6** (folga p/ parafuso 1/4" ou M6):

| Peça | X | Y | Furos |
|---|---|---|---|
| 1A (virabrequim) | **2952** | 102,5 e 202,5 | 2 |
| 1B (tubo) | **2290** | 102,5 / 152,5 / 202,5 | 3 |
| Trem de tensão (diagonal 45°) | **2826,6 / 2857,7 / 2888,9** | **199,6 / 230,8 / 261,9** | 3 |

> **Correção 2026-11-08 (2):** o passo do trem era **62** (passo das polias
> do modelo antigo); a base nova (fig. 8, chapa em L 112) fura em **U = 44**
> (furos em 12/56/100). `trem_pitch` 62 → 44: agora os parafusos passam.

> **Reposicionamento 2026-11-09:** o trem saiu de X 2088 e foi para a
> **ponta direita, atrás da bancada, inclinado 45°** — `Rz(225°) + (2903,
> 264,7, 900)`. Motivo: a polia de saída (3) precisa ficar junto à **boca
> da fenda do cabeçote** em **(2800, 173,7, 933,8)**, para o arame sair do
> trilho e entrar direto na fenda, sem passar por cima da bancada. Os 3
> furos acompanham a diagonal (passo U = 44 → **31,11** em X e em Y):
> `trem_tx = L − 145`, `trem_ty = W − 40,3`,
> `trem_rot = 0,70710678` (sem unidade), `trem_lx/ly`,
> `trem_step` viraram parâmetros da bancada; `x_trem`/`y_trem` são
> derivados. Alinhamento conferido no B-rep: furos da base e do tampo
> coincidem em 0,0000001 mm.

> **Correção 2026-11-08:** 1A estava em **2880** (`L − 168`), o que colocava
> o bloco (2850–2910) colidindo com a lâmina, que sai 62 mm para fora do fim
> do tubo (até X 2912). Virou **2952** (`L − 96`): o bloco ocupa 2922–2982,
> começando **72 mm para fora do fim do tubo** (regra VITA: bloco para fora
> da ponta), com folga de 10 mm para a lâmina. `x_1b = x_1a − 662` mantém o
> 1B em 2290.

**Leiaute de montagem** (mesma origem do modelo): blocos 1A/1B assentados
no tampo (110 de altura, eixo a 955); tubo de 620 de **X 2230 a 2850**;
1B em 2290, **1A em 2952** (bloco 2922–2982, lâmina até 2912 com folga
10 mm). Trem de tensão na **ponta direita, atrás da bancada, a 45°**
(`Rz(225°) + (2903, 264,7, 900)`), polia de saída junto à boca da fenda
(2800, 173,7, 933,8); furos na diagonal **(2826,6 / 199,6), (2857,7 /
230,8), (2888,9 / 261,9)** (passo U = 44 → 31,11 em X e Y). Tábua de
X 216 a 2832; 9 ganchos de X 324 a 2724 (passo 300).

**Montagem da tábua:** 20 mm à frente da face da frente, presa por
6 parafusos M6 com espaçadores (porca-rebite na parede de 2 mm da
travessa de cima). Com o topo em 940, o gancho pendura com o U para fora:
a tela desce **~48 mm à frente** da face da bancada, e a perna curta do
gancho fica 10 mm acima do tampo.

**Massas:** quadro 43,14 kg + tampo 34,65 kg + tábua 4,05 kg (madeira
0,6 g/cm³) = **81,84 kg** → 201 N por pé.

**Conferências (3 fontes independentes):**

| Fonte | Volume |
|---|---|
| Analítico (`cad/bancada_dims.py`, união **exata** dos tubos por compressão de coordenadas) | 16.655.736,5 mm³ |
| B-rep do SolidCraft | 16.655.752,5 mm³ (+0,0001%) |
| STL lido à mão (fine) | 16.655.927,8 mm³ (+0,001%) |

3 corpos, todos `closed: true`: Tampo 4.414.493,4 / Quadro 5.495.350,5 /
Tábua 6.745.908,6 mm³. Exportando **corpo a corpo**, os 3 STLs saem
watertight; no STL do conjunto sobra **1 aresta non-manifold**, na linha
(0, 305, 895,25)–(3048, 305, 895,25): é a costura de contato
tampo ↔ travessa de trás, não defeito.

**Paramétrico:** testado com **L = 2800, W = 330, H = 880** — tampo,
quadro, tábua, furos e posições acompanham (`x_1a = L − 96`,
`trem_tx = L − 145`, `trem_ty = W − 40,3`, etc.),
sem erros; o design voltou ao original. Re-testado em 2026-11-09 com o
trem na diagonal: furos do trem em (2578,6/224,6) (2609,7/255,8)
(2640,9/286,9) — dentro do tampo de 2800 × 330 ✅.

**Fabricação:** chapa 3/16" com os 8 furos Ø6,6 (porcas/arruelas por
baixo, acesso entre as travessas); quadro soldado com 18,74 m de metalon
(pés cortados a 855,25 e soldados sob o perímetro); tábua 1" × 4" com
6 furos Ø6,5; tudo em aço carbono, pintura depois de furar.

Arquivos: `cad/bancada_dims.py`, `cad/bancada.json` (94 comandos),
`cad/bancada.sc`, `export/bancada.step|.stl|.png` (+ `bancada_topo.png`,
`bancada_frente.png`, `bancada_cabecote.png`).

### `virabrequim.sc` + `punho.sc` — manivela manual (peças 5 e 1)

Conjunto da manivela do modo manual: a **haste Ø25,4 (1")** dobrada em S que
gira no mancal 1A com uma ponta na lâmina (4), e o **punho** (tubo de 5")
que gira folgado sobre o braço da alça. Spec fechada em `NOTAS.md` (tabela
A–M + recortes da fig. 4; onde desenho e tabela divergem, a tabela vence).

| Elemento | Valor | Origem |
|---|---|---|
| Haste | Ø **25,4** (1") | texto VITA |
| Caminho total | **788,6 mm** | VITA 31" = 787,4 (+0,15%) |
| Braço fendido (journal) | **D = 210** | tabela D |
| Dobra 1 e 2 | **45°, R = 37,3** | derivado (J = 50 = R + 12,7 ✓) |
| Haste central | **M = 380** entre tangentes | tabela M |
| Braço da alça | **K = 140** | tabela K |
| Fenda na ponta | **F = 5 × E = 32** de profundidade | tabelas F e E |
| Furo da fenda | **Ø6,35 (1/4") a 32 da ponta** (raiz) | texto VITA |
| 4 furos | **Ø3,175 (1/8")** ⊥ ao plano da manivela | texto VITA |
| — braço fendido | h1 **37** da dobra (H), h2 **110** da dobra (I) | tabelas H/I |
| — braço da alça | **10** e **130** da ponta (K−L e L) | tabelas K/L |
| Punho (1) | tubo **127**, OD **33,4** / ID **26,64** | texto: 5", folga Ø1,2 |

A parte é **simétrica sobre o plano da manivela** (os dois dobram 45° para o
mesmo lado no desenvolvido → forma em S no plano), então não há peça
destra/esquerda. Divergência registrada: G = 160 (h1→ponta) daria 173
geométrico — usamos H/I, como previsto.

**Conferências (3 fontes independentes):**

| Peça | Analítico | B-rep | STL |
|---|---|---|---|
| Virabrequim | 394.046 mm³ (`virabrequim_dims.py`) | **393.962,07** (−0,021%) | 391.150,8 (−0,71%) |
| Punho | 40.484 mm³ | **40.480,31** (−0,009%) | 40.501,9 (+0,05%) |

O −0,71% do STL do virabrequim é **facetamento inscrito** dos cilindros
(≈30 segmentos na haste), não erro de construção. bbox exatos nos dois
(671,46 × 315,96 × 25,40 e 127 × 33,4 × 33,4), 1 corpo cada, 53 e 5 passos,
todos os sketches dof 0. Massa em aço: **3,09 kg** + punho **0,32 kg**.

**Malha:** o build do virabrequim disparou 4× `Boolean retry: tool
displacement 3e-3 mm` (furos em face curva) e o STL saiu com **8 arestas
não-manifold** (T-junctions de 3–34 µm + faixa duplicada nas bordas dos
furos). Reparado com `cad/repair_stl.py --tol 0.05` (solda espacial +
preenchimento de 2 lacunas): 6.044 triângulos, **ESTANQUE**, volume da malha
mudou 0,1 mm³. `export/virabrequim.stl` é o arquivo reparado; o punho saiu
watertight direto (7.416 triângulos).

**Fabricação:** barra 1" dobrada conforme fig. 4, fenda 3/16" na ponta
(torno/serra), furos 1/4" e 4× 1/8"; punho = tubo 1" Sch40 cortado em 5",
lixar a haste para o punho girar suave (o manual manda).

Arquivos: `cad/virabrequim_dims.py`, `cad/virabrequim.sc`, `cad/punho.sc`,
`cad/check_stl.py`, `cad/repair_stl.py`,
`export/virabrequim.step|.stl|.png` (+ `virabrequim_iso.png`),
`export/punho.step|.stl|.png`.

### `montagem.sc` — montagem 3D completa (SolidCraft)

**Tudo montado** no leiaute **central** (Y 152,5 — decisão de 2026-11-08;
migração para o leiaute da fig. 15/16 fica para depois): bancada + mancais
1A/1B + cabeçote + lâmina + virabrequim + punho + trem de tensão + **9
ganchos** + **arame** (caminho do rolo à boca da fenda). **22 ocorrências**
(21 com corpos + o componente `mancal_cabecote`, vazio e herdado do projeto),
**20 joints** (19 estruturais + o rígido do arame).

**Posições (mundo, mm):**

| Peça | Transform | Conferência |
|---|---|---|
| bancada | fixada (grounded) | — |
| mancal 1A | Rz(−90) + (2922, 152,5, 900) | bloco 2922–2982, eixo a 955 |
| mancal 1B + braçadeira | Rz(−90) + (2190, 152,5, 900) | bloco 2250–2330 |
| cabeçote (tubo) | Ry(90) + (2230, 152,5, 955) | tubo X 2230–2850 |
| lâmina | (−x+2912, z+150, y+930) | furo em 2902, plano XZ em Y 150–155 |
| trem de tensão | Rz(225°) + (2903, 264,7, 900) | furos (2826,6/199,6) (2857,7/230,8) (2888,9/261,9) batem com o tampo; polia 3 junto à boca da fenda (2800, 173,7, 933,8) |
| virabrequim | Rx(90) + (2890, 152,5, 955) | fork na ponta da lâmina |
| punho | (3428, 152,5, 1245,6) | no braço K, eixo Y152,5/Z1245,6 |
| 9 ganchos | Rz(−90), passo 300 | X 324–2724, olho em cima na tábua |
| arame | rígido com a bancada (joint 75) | Ø1,6; rolo em (3763, 1137, 150) → 3 polias → boca (2800, 173,7 / 933,8) |

**Mecanismo:** grupo rígido estático (bancada + mancais + braçadeira + tubo +
trem + ganchos + arame, 18 ocorrências) + grupo móvel [virabrequim, lâmina,
punho] ligado por **revolute "Virabrequim"** em (2952, 152,5, 955), eixo X.
`joint.drive` testado: 45° e volta a 0°, `moved: true`.

**Interferências nominais conhecidas** (não corrigidas — vêm das cotas do
VITA; anotadas como folgas de fabricação):

| Par | Prof. | Explicação |
|---|---|---|
| lâmina × cabeçote | 0,15 mm real* | canto reto da lâmina plana Ø50 × furo redondo Ø50 |
| mancal 1B × tubo | 1,6 mm | aperto intencional do bloco bipartida (OD60 × furo 57) |
| virabrequim × mancal 1A | 0,49/0,31 mm | haste Ø25,4 × furo Ø25 → furar 25,6–26 na fabricação |

\* o `contact.check` reporta 2,34 mm porque mede a **extensão lateral** da
região de arrasto; a interseção real (medida por booleano) são 23 fatias de
**0,15 mm**, total 380 mm³ (0,2% da lâmina).

**Acoplamento fora** — decisão do usuário: modo **manual (só punho)**; o
acoplamento do motor ocupa a mesma ponta do virabrequim (braço K = 140,
punho = 127, não cabe os dois) e fica como alternativa do modo motorizado.

#### Simulação (2026-11-10)

Dois estudos no SolidCraft: o **giro do virabrequim** e o **caminho do
arame** (modelado como sólido Ø1,6 e montado como componente `arame`,
ocorrência 73, dof 0).

**Giro do virabrequim — motion study "Giro 360"** (id 69): joint 67
(revolute) de 0° a 360° em **72 passos**.

| Verificação | Resultado |
|---|---|
| `motion.interference` 0→360° (51 pares × 73 amostras) | só os **3 pares nominais** já conhecidos: cabeçote × lâmina 2,39 mm, virabrequim × mancal 1A inf. 2,63 mm e sup. 1,30 mm (profundidades de malha) — **nenhum par novo** |
| `motion.trace` da quina da lâmina em (2168, 177,5, 955) | círculo **r = 25 mm** exato no plano YZ (X 2168), dentro do tubo Ø50 — a lâmina gira sem tocar a parede |
| `joint.drive` 90° e volta a 0° | `moved: true`; pose final restaurada (passo 0) |

**Caminho do arame.** Rolo no chão em **(3763, 1137, 150)**, atrás/direita da
bancada. O caminho foi resolvido analiticamente num plano vertical a 45°
(o plano que contém a linha do trem) com tangentes externas/internas e
**raio de contato 13,1 mm** (fundo do canal em V + raio do arame):

| Trecho | Envolvimento na polia |
|---|---|
| rolo → polia 1 (entra por cima) | **69,2°** |
| polia 1 → polia 2 (por baixo) | **73,1°** |
| polia 2 → polia 3 (por cima) | **48,1°** |
| polia 3 → boca da fenda | reta até (2800, 173,7 / 933,8) |

- Comprimento do arame: **1.610,7 mm** (volume Ø1,6 = 3.238,5 mm³; B-rep
  3.076,5 mm³ por causa dos cortes das pontas no pipe).
- **0 pontos** do caminho dentro da caixa da bancada; distância mínima ao
  eixo do tubo = **30,0 mm**, exatamente na boca (entra tangente, sem
  raspar).
- Interferência arame × polias: só **1,56 mm³** residual na polia 2 (o
  arame assenta no fundo do canal V; o resto foi eliminado subindo o raio de
  contato de 12,47 para 13,1). Tubo/bancada não concluídos por orçamento de
  tempo; nada indica contato.

**Artefatos:** `export/montagem_giro.gif` (giro sem o arame),
`export/montagem_giro_arame.gif` (giro com o arame), `export/montagem_giro_90.png`
(pose a 90°), `export/arame_trem.png` e `export/arame_boca.png` (detalhes do
arame no trem e na boca da fenda), `export/arame.step|.stl` (só o arame).

Arquivos: `cad/montagem.sc`, `export/montagem.step`,
`export/montagem_01|final|ganchos|cabecote|trem.png` +
`montagem_trem.png|montagem_trem_detalhe.png|montagem_caminho.png`
(reposicionamento do trem, 2026-11-09) +
`montagem_giro.gif|montagem_giro_arame.gif|montagem_giro_90.png` e
`arame_trem.png|arame_boca.png` (simulação, 2026-11-10).
`export/montagem.step` segue **sem** o arame (o arame tem export próprio);
`export/montagem_com_arame.step` (1,53 MB) é a montagem completa, com o
componente `arame`.

## Custo estimado (Brasil, 2026)

| Item | Faixa |
|---|---|
| Tubo 2" (1 m) | R$ 60–120 |
| Lâmina de aço (chapa 5 mm, 50 × 750) | R$ 40–90 |
| 3 polias / sheaves | R$ 60–150 |
| Cabo + mancais + parafusos | R$ 80–150 |
| Mesa / madeira | R$ 100–200 |
| Motor (usado, com redução) | R$ 150–400 |
| Arduino + sensor + relé | R$ 80–150 |
| **Total** | **R$ 570–1.260** |

Máquina comercial equivalente: R$ 15.000–80.000.

## Ordem de construção

1. ✅ **Cabeçote + gabarito** — `bending_head.py` + `spiral_template.py`
2. ✅ **Trem de tensão** (3 polias) — `trem_tensao.sc` (SolidCraft)
3. ✅ **Bancada e ganchos** — segurar a tela formada
   (✅ bancada — `bancada.sc`; ✅ ganchos — `gancho_tela.json`)
4. **Motorização** — motor no lugar do cabo, com redução
   (✅ acoplamento motor ↔ virabrequim — `acoplamento_motor.sc`;
   ✅ manivela manual — `virabrequim.sc` + `punho.sc`;
   falta o **suporte do motor**)
5. **Automação** — Arduino conta voltas, corta no comprimento, para no fim

## Ponto de risco

A **entrada do arame na fenda** e o **início de cada nova espiral** são os
pontos onde o manual original exige mão humana. Automatizar o corte e o
recomeço é o que separa "semiautomática" de "toda sozinha".

## Ainda não modelado

**Montagem:** ✅ `montagem.sc` — tudo montado (22 ocorrências, 20 joints,
revolute do virabrequim testado, giro simulado 0–360° e caminho do arame
modelado). Ver a seção acima.

**Do manual VITA** — só falta hardware de prateleira:

- ~~Trem de tensão (3 polias + base 6 + eixos 26A/26B)~~ ✅ `trem_tensao.sc`
- ~~Mancal do cabo (bloco 1A / 1B do manual) + braçadeira 8~~ ✅ `mancal_cabecote.sc`
- ~~Lâmina interna (bending arm, peça 4)~~ ✅ `lamina_interna.json`
- ~~Ganchos de sustentação da tela (peça 11)~~ ✅ `gancho_tela.json`
- ~~Bancada (peça 2) e tábua dos ganchos~~ ✅ `bancada.sc`
- ~~Virabrequim (5) — barra Ø25,4 (1") × 787 mm (31"), dobrada em "S",
  fenda de 3/16", furo de 1/4" na ponta e 4 × Ø3,2 (1/8")~~ ✅ `virabrequim.sc`
- ~~Punho (1) — tubo de 5" que gira sobre a manivela~~ ✅ `punho.sc`
- Parafusos (13), porca (14), arruelas — hardware de prateleira

**Fora do manual (automação):**

- ~~Acoplamento motor ↔ virabrequim~~ ✅ `acoplamento_motor.sc`
- ~~Caminho do arame (rolo → 3 polias → boca da fenda), modelado como
  sólido Ø1,6~~ ✅ `export/arame.step|.stl` + componente `arame` em
  `montagem.sc`
- Suporte/berço do motoredutor no lugar do cabo
- Desenrolador de arame (o rolo no chão e a guia de entrada ainda não são
  peças modeladas — só o caminho do arame)
- Cortador automático no comprimento da tela
- Guardas das polias, botoeira de emergência e quadro elétrico
- Firmware do Arduino (contagem de voltas + corte)

## Segurança

Arame galvanizado sob tensão corta. A máquina tem partes girando e arame
saindo com energia. Guarda nas polias, botoeira de emergência e óculos
obrigatórios.
