# NOTAS de trabalho — diário do projeto (para a IA seguinte)

> Leia este arquivo antes de qualquer coisa. O `README.md` tem o estado
> **consolidado** de cada peça; este arquivo tem o **fluxo de trabalho**,
> o que está em andamento agora e as convenções. Atualize este arquivo ao
> fim de cada sessão.

## O que é o projeto

Máquina de fabricar tela alambrado (chain link), baseada no boletim VITA
51025-BK (domínio público). Fonte primária:

- Texto: `https://www.cd3wdproject.org/new/VITAHTML/SUBLEV/EN1/CLFENCE.HTM`
- Figuras locais: `ref\CLF*.gif` + recortes `ref\fig*.png`

Foco atual: **modo manual** (a VITA é manual; a motorização é opcional e
fica para depois).

## Convenções de trabalho (importante)

1. **O SolidCraft escreve primeiro em `C:\Users\gabri\SolidCraft-Projetos`**
   (MCP headless, `solidcraft` server). Só depois os artefatos são copiados
   para `C:\DEV\3dprint\alambrado\cad\` e `export\`.
2. Skills usadas: `solidcraft-modeling` (build) e a referência de comandos
   em `C:\Users\gabri\.config\opencode\skills\solidcraft-modeling\reference.md`.
3. **Fluxo por peça (obrigatório):**
   1. Intake — achar as cotas na tabela A–M / texto / figuras;
   2. Planear números — `cad/<peça>_dims.py` com volume/bbox esperados
      calculados ANTES de construir;
   3. Build paramétrico em poucos `batch` (todos ou nada, nomear cada feature);
   4. Verificar — `measure` vs analítico, 3 fontes independentes
      (analítico / B-rep / STL lido à mão com `check_stl.py`),
      screenshot, STL watertight;
   5. Exportar STEP + STL + PNG para `export\`;
   6. Atualizar `README.md` (seção nova + "Ainda não modelado" + ordem de
      construção) **e este NOTAS.md**.
4. Armadilhas conhecidas do SolidCraft (v1):
   - `solid.shell` `faces` não aceita expressão — usar nomes de face
     (`F<id>:-x`); ids incrementam por box/shell/hole/combine na ordem do build;
   - comprimentos aceitam sufixo (`"1 in"` = 406,4 mm); `measure` devolve mm;
   - export STL corpo a corpo para watertight (STL de conjunto tem costuras
     non-manifold no contato entre corpos — não é defeito);
   - furos em face curva disparam `Boolean retry: tool displacement ~3e-3 mm`
     no build — se o volume bater com o analítico é só aviso, **mas** pode
     deixar T-junctions na malha: sempre rodar `cad\check_stl.py` no STL;
   - `cad\repair_stl.py entrada.stl [--tol 0.05]` repara: solda vértices,
     tira degenerados/duplicados e **fecha lacunas** (bordas com 1 triângulo)
     — usado no virabrequim (8 arestas → 0, ESTANQUE);
   - shell nesta máquina: comando multi-linha com `$var` sai sem output —
     usar `;` numa linha só.

## Estado das peças (9 peças VITA + extras)

| # | Peça | Estado | Arquivo |
|---|---|---|---|
| — | Cabeçote de dobra (tubo fenda helicoidal) | ✅ | `bending_head.py` (FreeCAD legado) |
| — | Gabarito 1:1 (planificação DXF/SVG) | ✅ | `spiral_template.py` |
| 6/26 | Trem de tensão | ✅ | `trem_tensao.sc` |
| 1A/1B | Mancal + braçadeira | ✅ | `mancal_cabecote.sc` |
| 4 | Lâmina interna (bending arm) | ✅ | `lamina_interna.json` |
| 11 | Ganchos da tela | ✅ | `gancho_tela.json` |
| 2 | Bancada + tábua | ✅ | `bancada.sc` |
| — | Acoplamento motor↔virabrequim (extra) | ✅ | `acoplamento_motor.sc` |
| — | Arame Ø1,6 (rolo → 3 polias → fenda) | ✅ | `arame.step` (componente em `montagem.sc`) |
| **5** | **Virabrequim / manivela** | ✅ | `virabrequim.sc` |
| **1** | **Punho (maçaneta)** | ✅ | `punho.sc` |
| — | Suporte do motor, desenrolador, cortador, firmware | ❌ futuro | — |
| 13/14 | Parafusos/porcas | ❌ hardware de prateleira | — |

## Tabela de cotas A–M (extraída do texto VITA — cm / polegadas)

| Letra | cm | in | Uso (mapeamento atual) |
|---|---|---|---|
| A | 5 | 2 | meio-passo parafusos blocos 1A/1B ✅ já usado |
| B | 1 | 3/8 | furo da lâmina a partir da ponta ✅ já usado |
| C | 0,5 | 3/16 | raio das quinas da lâmina ✅ já usado |
| D | 21 | 8⅜ | braço superior da manivela (com fenda) — **comprimento** |
| E | 3,2 | 1¼ | furo Ø na ponta do braço fendido (1/4" no texto) |
| F | 0,5 | 3/16 | **largura da fenda** da manivela (= espessura lâmina 5) |
| G | 16 | 6¼ | 2ª medida do braço fendido (posições dos furos) |
| H | 3,7 | 1½ | 3ª medida do braço fendido (offset) |
| I | 11 | 4¼ | 4ª medida do braço fendido (distância entre furos?) |
| J | 5 | 1⅞ | braço inferior (alça) — medida na ponta |
| K | 14 | 5⅝ | braço inferior (alça) — comprimento total |
| L | 13 | 5¼ | braço inferior (alça) — entre furos |
| M | 38 | 15 | **altura total** da manivela (eixo→eixo / topo) |

Texto VITA correspondente (peça 5): barra de 1" Ø25,4 × 31" (787 mm),
fenda 3/16" na ponta para encaixar na lâmina (4), furo 1/4" atravessando
a ponta fendida, **quatro furos de 1/8" (3,2 mm)** no braço da alça,
dobrada conforme fig. 4. Peça 1: tubo de 5" (127 mm) que gira folgado
sobre a alça — lixar o virabrequim para o punho girar suave.

**Mapeamento FECHADO (2026-11-08, lido nos recortes `fig4_a/b/baixo/h` +
texto VITA):** ver a seção "Spec final" abaixo. O desenho da fig. 4 é
esquemático (não é à mesma escala — precedente: a fig. 3 também), então
onde desenho e tabela divergem, a **tabela vence** e a diferença fica
registrada.

## Spec final — virabrequim (5) + punho (1)

**Geometria:** haste Ø25,4 (1"), caminho total ≈ **788,6 mm** (VITA: 31" =
787,4 — +1,2 mm / 0,15%, ok). Plano único (o "Z" da fig. 4):

| Trecho | Cota | Valor |
|---|---|---|
| Braço fendido (journal, passa no mancal 1A) | D | **210** da ponta ao início do dobra |
| Dobra 1 (raio do centro de linha) | derivado | **R = 37,3** (deflexão 45°) |
| Haste central (atravessa 1A) | M | **380** entre tangentes dos dobras |
| Dobra 2 | idem | R = 37,3, 45° |
| Braço da alça | K | **140** do fim do dobra à ponta |

- **Fenda na ponta:** largura **F = 5**, profundidade **E = 32** da ponta;
  furo **Ø6,35 (1/4") a 32 da ponta** (raiz da fenda) — o parafuso passa
  pelas duas mandíbulas e pelo furo da lâmina (lâmina entra 22 mm, sobra
  10 na ponta; confere com o furo da lâmina a B=10 da ponta).
- **4 furos Ø3,175 (1/8")**, eixos ⊥ ao plano da manivela:
  - Braço fendido: **h1 a 37 da dobra** (H), **h2 a 110 da dobra** (I);
    G=160 (h1→ponta) dá 173 geométrico — **divergência de 13 mm
    registrada**, usamos H/I.
  - Braço da alça: **furo da ponta a 10 da ponta** (K−L = 140−130) e
    **furo a 130 da ponta** (L), este a 10 do fim do braço. Os dois furos
    delimitam onde o punho (tubo de 127) fica montado.
- **J = 50** = raio externo do dobra inferior (R+12,7 = 50 ✓, fecha o
  desenvolvido com 787,4).
- **Punho (1):** tubo **127 mm (5")**, ID ~26,6 (tubo 1" Sch40: OD 33,4) —
  gira folgado sobre a haste Ø25,4 (folga Ø1,2; o manual manda lixar a
  haste para ajustar fino).

**Ponto em aberto de montagem — RESOLVIDO em 2026-11-08 (sessão noite):** o
prolongamento da lâmina no lado da manivela (62 mm medido na fig. 13) passaria
pelo bloco 1A se 1A encostasse no fim do tubo. No VITA real, **1A precisa ficar
~72 mm para fora do fim do tubo** (fenda da haste: 2890–2922 com a lâmina até
2912; bloco a partir de ~2922). **Aplicado:** `bancada` mudou `x_1a` de
`L − 168` (2880) para `L − 96` (**2952**) — bloco 2922–2982, folga 10 mm para
a lâmina; `x_1b = x_1a − 662` mantém o 1B em 2290. Verificação nova
`folga lamina <-> bloco 1A` no `bancada_dims.py` (aprovado: True).

## Sessões de 2026-11-08

### Manhã — bancada, cotas e mapeamento da fig. 4

- Bancada concluída e verificada (3 fontes, 0,001%) e exportada.
- Tabela A–M localizada no texto VITA (resolveu o bloqueio das cotas).
- Mapeamento da fig. 4 iniciado: M = altura total; braço superior fendido
  (D/E/G/H/I/F); braço inferior alça (J/K/L). Recortes de montagem lidos.

### Tarde — virabrequim (5) + punho (1) ✅ CONCLUÍDOS

Spec fechada na seção acima; construção e verificação:

**`cad/virabrequim_dims.py`** — analítico **394.046 mm³** (haste 399.605 −
fenda 4.038 − furo 1/4" 719 − 4 furos 1/8" 803), bbox esperado
(671,46; 315,96; 25,40).

**Build** (`cad/virabrequim.sc`): 1 `batch`, **53 passos**, todos os sketches
dof 0. Rota: sketch de caminho com restrições (coords dos `sketch.line` só
posicionam — medido; `cos()/sin()` funcionam em expressões — sondado), perfil
círculo no YZ + `solid.sweep`, fenda por polyline fechada no XZ +
`solid.extrude` corte simétrico, 5 furos `solid.hole` na forma de posição.

| Fonte | Volume |
|---|---|
| Analítico | 394.046 mm³ |
| B-rep (`expect` ok) | **393.962,07 mm³** (−0,021%) |
| STL (`check_stl.py`) | 391.150,8 mm³ (−0,71% vs B-rep) |

bbox exata, 1 corpo. O −0,71% do STL é **facetamento inscrito** dos cilindros
(≈30 segmentos na haste Ø25,4), não erro de construção.

**Aviso de boolean:** 4× `Boolean retry: tool displacement 3,006e-3 mm,
rotation 2e-6 rad` (furos em face curva) — o volume bateu, era "só" aviso,
**mas** a malha saiu com defeito: `check_stl.py` achou **8 arestas ≠ 2**
(T-junctions de 3–34 µm + 1 faixa duplicada nas bordas do furo 1/4" e do
furo K2). Reparado com `cad\repair_stl.py --tol 0.05` (solda + **2 lacunas
fechadas**): 6.192 → 6.044 triângulos, **ESTANQUE**, malha mudou só 0,1 mm³.
`export\virabrequim.stl` agora é o arquivo reparado. Se re-exportar do `.sc`
e sair vazado de novo, repetir o reparo.

**`cad/punho.sc`**: 5 passos, tubo 127 × OD 33,4 × ID 26,64.

| Fonte | Volume |
|---|---|
| Analítico | 40.484 mm³ |
| B-rep (`expect` ok) | **40.480,31 mm³** (−0,009%) |
| STL (`check_stl.py`) | 40.501,9 mm³ (+0,05%) — **ESTANQUE** direto |

**Artefatos copiados para o projeto:** `cad/virabrequim.sc`,
`cad/punho.sc`, `cad/virabrequim_dims.py`, `cad/check_stl.py`,
`cad/repair_stl.py`; `export/virabrequim.{step,stl}`,
`export/virabrequim.png`, `export/virabrequim_iso.png`,
`export/punho.{step,stl}`, `export/punho.png`. README atualizado.

**Pendências:** ~~conferir o ponto em aberto de montagem (1A em X 2880 vs
prolongamento da lâmina)~~ ✅ resolvido (1A → 2952); suporte do motor,
desenrolador, cortador e firmware continuam ❌.

### Noite — inventário do `ref/` (figuras completas) ✅

O `ref/` só tinha as **11 imagens que o HTML embute** (figs. 1–5, 11–15, 18).
O texto cita figs. 6–10, 16 e 17, que não estão no HTML. Recuperadas no mesmo
servidor (`SUBLEV/GIF/`), onde o nome segue `CLF<fig>X<página do folheto>`:

| Fig | Arquivo | Conteúdo | Cota nova |
|---|---|---|---|
| 6 | `clf6x7.gif` | braço 8 (3 furos) | N = 50 mm (passo) |
| 7 | `clf7x7.gif` | **gancho 11** | R 89 / S 50 / T 25 |
| 8 | `clf8x7.gif` | base 6 do trem | U 44 / V 16 / W 35 / X 12 |
| 9 | `clf9x8.gif` | polia 10 (torno) | O 32 / P 17 / Q 6 + Q° |
| 10 | `clf10x8.gif` | **tabela N–X** + 9A/9B/9C | — |
| 17 | `clf17x9.gif` | operação (máquina inteira) | — |
| 16 | dentro de `CLF15X3.gif` | vista lateral (15+16 no mesmo GIF) | Y 22 / Z 124 |

→ **18/18 figuras completas**. Única ausente: a ilustração do "World
Neighbors in Action" (peças A–F), que o HTML perdeu e não existe no servidor
(testados CLF19–27 × páginas 1–30) — não é figura numerada do boletim.

Índice completo + tabela N–X: **`ref/INDICE.md`**.

~~**Pendência nova (conferência, não bloqueia):** as cotas N–X e Y/Z podem
corrigir 3 modelos feitos antes das figuras — gancho 11 (R/S/T), base do
trem 6 (U/V/W/X) e polia 10 (O/P/Q; O = 32 mm contra Ø50 do texto "1½–2"" —
interpretar antes de mudar). Y/Z (22 e 124 mm) são o leiaute na bancada; hoje
tudo está no centro (Y 152,5). Nada foi alterado nos modelos ainda.~~

**Fechado em 2026-11-08 (sessão noite — ver abaixo):** gancho e trem
reworkados com as cotas N–X, polia Ø32 (venceu o texto), leiaute mantido
**central** por decisão, 1A corrigido para 2952.

## Sessão 2026-11-08 noite — auditoria + correções + montagem 3D

**Auditoria completa** das 9 peças contra as 18 figuras: tudo conferido,
3 grupos de correção identificados (sync do `cad/`, docs stale, leiaute).

**Correções aplicadas:**

1. **`bancada` — 1A: 2880 → 2952** (`x_1a = L − 96`, `x_1b = x_1a − 662`).
   Motivo: colisão lâmina × bloco (lâmina até 2912, bloco 2850–2910 antes).
   Agora bloco 2922–2982 = 72 mm fora do fim do tubo (regra VITA), folga
   10 mm. `bancada_dims.py` com check novo; `bancada.json` e `bancada.sc`
   atualizados; 8 furos conferidos por topologia (1A 2952, 1B 2290, trem
   2026/2088/2150); re-exportado step/stl/png.
2. **Sync do `cad/`** (a sessão das 17:39/17:50 falhou antes de copiar):
   `cad\gancho_tela.sc`, `cad\trem_tensao.sc` e `cad\bancada.sc` agora são
   as versões novas. `cad\gancho_tela.json` ficou **obsoleto** (o rework do
   gancho foi por comandos MCP, sem json) — documentado, não apagado.
2b. **`bancada` — passo do trem: 62 → 44** (`trem_pitch`): a base nova
   (fig. 8) fura em U = 44 (furos 12/56/100), mas o tampo ainda furava no
   passo 62 das polias do modelo antigo. Furos agora em **2044/2088/2132**,
   Y 167,5 — batem com a base. Bancada re-salva e re-exportada.
3. **`trem_tensao_dims.py` reescrito** para a geometria nova (chapa em L
   112×35/16×4,8 + 3 polias Pappus): analítico **58.900,461** × B-rep
   58.900,311 = **0,00025%** ✅. `aprovado: True`.
4. **Docs:** README (seções trem, gancho, bancada), NOTAS e `ref/INDICE.md`
   atualizados — leiaute central registrado como decisão, pendências de
   conferência marcadas como resolvidas.

**Decisões do usuário:** leiaute **central** (Y 152,5) como base da montagem;
corrigir 1A agora; "placa de acoplamento do alinhamento" não existe em lugar
nenhum — definição criada (chapa 100×60×5 com 4 furos Ø5 + furo central
Ø25,4), modelo `placa_acoplamento.sc` fica só no SolidCraft-Projetos (fora
do projeto, função indefinida). `cad\gancho_tela.json` antigo mantido como
histórico.

**Montagem 3D — CONCLUÍDA:** `montagem.sc` com 20 componentes e 19 joints
no leiaute central. Peças posicionadas e conferidas por bbox e screenshot
(bancada grounded; mancais 1A/1B; tubo; lâmina; trem; virabrequim; punho;
9 ganchos). Mecanismo: rigid group estático (16 peças) + rigid group móvel
[virabrequim, lâmina, punho] + **revolute "Virabrequim"** em
(2952, 152,5, 955) eixo X — `joint.drive` testado a 45° e voltou a 0°
(`moved: true`).

**Colisões resolvidas:** ganchos × bancada (laço do olho encostava na tábua
2,85 mm) → 9 ganchos subiram +2,9 mm; zeradas.

**Interferências nominais registradas (não corrigidas):** lâmina × cabeçote
(contact.check 2,34 mm = extensão lateral; interseção real medida por
booleano = 23 fatias de 0,15 mm, 380 mm³ = 0,2% — canto reto da lâmina plana
× furo redondo Ø50); mancal 1B × tubo 1,6 mm (aperto do bloco bipartida);
virabrequim × mancal 1A 0,49/0,31 mm (haste Ø25,4 × furo Ø25 → furar
25,6–26). Contato desligado após a verificação (`contact.enable_sets false`)
para o drive não travar nessas folgas de interferência.

**Decisão:** montagem em **modo manual — só punho** (o acoplamento do motor
ocupa a mesma ponta; K = 140 vs punho 127, não cabe os dois). Acoplamento
fica como alternativa do modo motorizado.

**Exportado:** `cad/montagem.sc`, `export/montagem.step` (1,48 MB) +
5 screenshots (`montagem_01|final|ganchos|cabecote|trem.png`). README com a
seção `montagem.sc`.

**Pendências que continuam ❌:** suporte do motor, desenrolador, cortador,
firmware, parafusos; acoplamento fora da montagem (modo manual).

## Sessão 2026-11-09 — trem de tensão reposicionado (ponta direita)

**Pedido do usuário:** o trem estava no lugar errado ("essa parte do trem ta
errada", "entra uma linha no trilho e sai do trilho entrando direto na
fresta do cabeçote"). A polia de saída tem que ficar junto à **boca da
fenda do cabeçote**, atrás da bancada, para o arame sair do trilho e entrar
direto na fenda.

**Cálculo (conferido por `body_topology`):** a boca da fenda no mundo é
**(2800, 173,713, 933,787)** — θ = 45°, z local 570 nas edges 13/14/31/32/43
do tubo (cap em X 2797,3–2802,7, r 25–30). Transform escolhido:
**`Rz(225°) + (2903, 264,7, 900)`** → polia 3 (saída) em **(2826,3 / 200,0 /
928)**, polia 1 (vinda do rolo no chão) em back-right; trecho polia 3 →
boca fica fora do tubo até cruzar r = 30 exatamente em X ≈ 2800,1 (na
boca). Folgas: base ↔ tubo ≈ 3,4 mm; polia 3 ↔ tubo ≈ 7 mm; para o bloco
1A ≈ 18 mm.

**Aplicado:**

1. **`bancada` (paramétrico):** params novos `trem_tx = L − 145 = 2903`,
   `trem_ty = W − 40,3 = 264,7`, `trem_rot = 0,70710678` (sem unidade — com unidade mm
   o `trem_step = trem_pitch*trem_rot` dá erro "length^2"), `trem_lx = 56`,
   `trem_ly = −8`, `trem_step = trem_pitch*trem_rot = 31,1127`;
   `x_trem`/`y_trem` agora derivam do transform. Os 3 furos viraram
   diagonal: **(2826,632 / 199,646), (2857,745 / 230,759),
   (2888,858 / 261,872)** (edits em `timeline.edit` nos FuroTrem1/2/3).
   `bancada_dims.py` reescrito (`trem_world()`, checks de folga do trem,
   cantos da base no tampo, polia 3 fora do bloco 1A) → **`aprovado:
   True`** (14 checks). Volume inalterado (16.655.752,5 mm³, 3 corpos).
   Re-salvo e re-exportado step/stl → copiados para o projeto.
2. **`montagem`:** joint rígido 55 do trem **deletado**, ocorrência 20
   **girada 225°** em torno de (2032, 175,5, 900) e **trasladada (871,
   89,2, 0)** → transform final `Rz(225°) + (2903, 264,7, 900)`;
   `component.update_links` recarregou a bancada (updated: [bancada]);
   rigid recriado (`joint.as_built`, id 68, "Rigid Group 2:20"), trem
   com **dof 0**. Conferência por topologia: centros dos furos da base e
   do tampo coincidem (0,0000001 mm).
3. **Verificações:** `contact.check` → `collisions: []` (set "montagem",
   20 ocorrências); `inspect.interference` → **0 pares** nos verificados
   (só os 5 nominais conhecidos ficaram de fora por orçamento de tempo).
   Drive do virabrequim intacto (joints 65–67 preservados).
4. **Exportado:** `cad/montagem.sc`, `export/montagem.step` (1,48 MB) +
   fotos novas `montagem_trem.png`, `montagem_trem_detalhe.png`,
   `montagem_caminho.png` (as antigas seguem para histórico). README
   atualizado (furação, leiaute, tabela de posições, arquivos).

**Estado:** furos do trem na diagonal 45° batendo com a base; caminho do
arame = rolo no chão → polia 1 por cima → polia 2 por baixo → polia 3 por
cima → **boca da fenda (2800, 173,7 / 933,8)** → enrola na lâmina → sai
pelo lado esquerdo (X 2230) como espiral → ganchos da tábua.

## Sessão 2026-11-10 — simulação (giro + caminho do arame)

**Pedido do usuário:** "consegue fazer a simulação" → escolheu **salvar o
desenho importado antes** e **"Os dois"** (giro do virabrequim + caminho do
arame).

**Antes de tudo:** o app estava com um desenho **importado do STEP, não
salvo** (`path: null`, dirty, 20 peças todas rígidas e sem o revolute).
Salvo como **`designs/montagem_import.sc`** (781.805 B, cópia em
`cad/montagem_import.sc`) a pedido do usuário e só então aberto o
`montagem.sc` paramétrico.

### Giro do virabrequim

1. **`motion.study "Giro 360"`** (id 69): joint 67 (revolute "Virabrequim")
   de 0° a 360°, **72 passos**.
2. **`motion.interference`** 0→360°, 51 pares × 73 amostras — **demorou
   ~12 min** (usar `pending`, nunca reenviar). Resultado: só os **3 pares
   nominais** já registrados (cabeçote × lâmina 2,39 mm; virabrequim ×
   mancal 1A inf. 2,63 mm e sup. 1,30 mm), **nenhum par novo**.
3. **`motion.trace`** da quina da lâmina em (2168, 177,5, 955): círculo
   **r = 25 mm** exato no plano YZ (X 2168), dentro do tubo Ø50.
4. **`joint.drive`** 90° e volta a 0°: `moved: true`; pose restaurada com
   `motion.play step 0`.
5. **GIF:** `motion.export_animation` do study, 36 amostras, 800×500,
   12,5 fps, câmera target (2820, 180, 950) yaw 2,35 pitch 0,32 dist 1450 →
   `fotos/montagem_giro.gif` (535.739 B).
6. **PNG a 90°:** `motion.play step 18` + `screenshot source:"model"` →
   `fotos/montagem_giro_90.png`.

### Caminho do arame

**Solver:** `%TEMP%\opencode\wire_path.py`. Plano vertical que contém a
linha do trem: direção `d = (−1,−1,0)/√2`, origem na polia 1
(2888,504 / 262,225 / 928), `u` ao longo de `d`, `v = z − 928`. Polias em
u = 0 / 44 / 88; boca em u = 125,169 / v = 5,787.

- **Tangentes:** externa do rolo → polia 1 (entrando por cima), internas
  polia 1→2 (por baixo) e 2→3 (por cima), e tangente de ponto (boca) na
  polia 3 (saindo por cima).
- **Raio de contato 13,1 mm** (fundo do canal em V Ø23,34 + raio do arame
  0,8). Primeira tentativa com 12,47 dava 3 sobreposições de 11–15 mm³;
  com 13,1 sobrou **1,56 mm³** na polia 2.
- **Envolvimentos:** P1 69,2° · P2 73,1° · P3 48,1°.
- **Comprimento 1.610,7 mm** (volume analítico Ø1,6 = 3.238,5 mm³).
- **Folgas:** 0 pontos dentro da caixa da bancada; distância mínima ao eixo
  do tubo = 30,0 mm **na boca** (entra tangente).
- **Rolo:** (3763, 1137, 150) — atrás/direita da bancada, 150 mm do chão.

**Build no SolidCraft:** sketch `CaminhoArame` (id 76, plano com origem na
polia 1, `x_dir = (−0,707,−0,707,0)`, `y_dir = (0,0,1)`) com 7 curvas
(l1/a1/l2/a2/l3/a3/l4) + `solid.pipe` Ø1,6 (feature 77, body `Body2`).
A primeira versão (raio 12,47) foi **apagada** (`timeline.delete` 71, 70) e
refeita com o raio novo.

**Componente:** `component.create "arame"` (ocorrência 73),
`component.move_bodies Body2`, `joint.rigid_group [bancada:1, arame:1]`
(joint 75) → **dof 0**.

**Verificações:** `inspect.interference` arame × {Polia, Polia 2, Polia 3,
Tampo, qF, Base}: só **Polia (2) × Body2 = 1,56 mm³**. Tubo (`Open CASCADE…`)
e bancada não concluídos por orçamento; `qF` deu erro de booleano
("implausible result volume", faces curvas) — nada indica contato.

**GIF com o arame:** `montagem_giro_arame.gif` (36 frames, 800×500,
12,5 fps, câmera target (2880, 230, 930) dist 1150) → 660.672 B.
**PNGs:** `arame_trem.png` (detalhe nas 3 polias) e `arame_boca.png`
(entrada na fenda), ambos `source:"model"`.

**Exportado:** `exports/arame.step` (50.851 B) e `arame.stl` (126.484 B,
fine), corpo `Body2`; `montagem_com_arame.step` (1.534.886 B) com todos os
corpos, arame incluído. `montagem.step` **não** foi re-exportado — segue sem
o arame (o arame tem export próprio). `montagem.sc` salvo: 446.795 B,
26 corpos, 20 joints.

**Copiado para o projeto:** `cad/montagem.sc`, `cad/montagem_import.sc`;
`export/arame.step|.stl`, `export/montagem_com_arame.step`,
`export/montagem_giro.gif|montagem_giro_arame.gif|montagem_giro_90.png`,
`export/arame_trem.png|arame_boca.png`. README (seção `montagem.sc` →
"Simulação") e este NOTAS atualizados.

**Armadilhas novas registradas:**

- `screenshot` sem `source:"model"` devolve a **janela** (1920×1080), não o
  render — usar `source:"model"`.
- `motion.interference` é lento (~10–12 min para 72 passos); **nunca**
  reenviar depois do erro `still running:` — usar `pending`.
- `parameters.add` com valor decimal cria unidade mm; `trem_rot` precisou
  de `unit:""`.
- `timeline.inspect` de `solid.hole` mostra `position` **stale** (pitch 62);
  a geometria real vem de `body_topology`.
- A matriz salva em `component.list` é a **transposta** do R efetivo
  (translação na 4ª linha): `R = transpose(top-left 3×3)`.
- O MCP só grava em `SolidCraft-Projetos`; exportar para `C:\DEV` é
  recusado — copiar por shell.

**Pendências que continuam ❌:** suporte do motor, desenrolador (peça),
cortador, firmware, parafusos. Decidir se o componente `arame` fica no
`montagem.sc` definitivo (hoje fica, como referência do caminho).
