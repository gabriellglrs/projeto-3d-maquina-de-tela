# Índice das figuras — VITA Technical Bulletin 51025-BK

Origem: `https://www.cd3wdproject.org/new/VITAHTML/SUBLEV/EN1/CLFENCE.HTM`
(texto) e `.../new/VITAHTML/SUBLEV/GIF/` (imagens).

**O HTML público só embute 11 imagens** (figs. 1–5, 11–15 e 18). O texto
cita as figs. 6–10, 16 e 17, que ficaram de fora da conversão. Elas existem
no mesmo servidor com o padrão `CLF<fig>X<página do folheto original>` — e a
**fig. 16 está dentro do mesmo GIF da fig. 15**. Com isso o acervo está
completo: **18/18 figuras**.

| Fig. | Arquivo | Conteúdo |
|---|---|---|
| 1 | `CLF1X1.gif` | bloco **1A**: 2 furos verticais 1/4", furo horizontal 1" |
| 2 | `CLF2X1.gif` | bloco **1B**: 2× 1/4" + 1× 2¼", contra-furo 1/2" × 1/4" |
| 3 | `CLF3X1.gif` | **lâmina 4**: furo 1/4", quinas arredondadas |
| 4 | `CLF4X5.gif` | **virabrequim 5** (desenho cotado D…M) |
| 5 | `CLF5X5.gif` | tubo **7**: fenda helicoidal 3/16" + furo 1/4" no topo |
| 6 | `clf6x7.gif` | **braço 8**: 3 furos 1/4" com passo **N = 5 cm** |
| 7 | `clf7x7.gif` | **gancho 11**: olho 1/8", **R 8,9 / S 5 / T 2,5 cm** |
| 8 | `clf8x7.gif` | **base 6** do trem de tensão: **U 4,4 / V 1,6 / W 3,5 / X 1,2** |
| 9 | `clf9x8.gif` | **polia 10** (torno): **O 3,2 / P 1,7 / Q 0,6** + ângulo Q° |
| 10 | `clf10x8.gif` | **tabela de cotas N–X** + montagem 9A/9B/9C (arruelas/rolamentos) |
| 11 | `CLF11X20.gif` | seção da polia no eixo (cantoneira em L) |
| 12 | `CLF12X2.gif` | polias nos tubos-rolamento |
| 13 | `CLF13X3.gif` | montagem do cabeçote de dobra |
| 14 | `CLF14X2.gif` | montagem do trem de tensão (3 polias) |
| 15 | `CLF15X3.gif` | vista de **topo** da máquina montada — **Y 2,2 / Z 12,4 cm** |
| 16 | *(no `CLF15X3.gif`)* | vista **lateral** da máquina montada |
| 17 | `clf17x9.gif` | **operação**: rolo de arame, tela pronta, manivela, ganchos |
| 18 | `CLF18X4.gif` | vistas de topo e lateral da montagem na bancada |

**Única imagem ainda ausente:** a ilustração do resumo *"World Neighbors in
Action"* (peças rotuladas A–F: tubo, lâmina, blocos C/D, manivela E, polias
F). O HTML perdeu o `<IMG>` nesse ponto e o arquivo não existe no servidor
(testados `CLF19…27` × páginas 1–30 e nomes alternativos). É um resumo de
outra publicação, não uma figura numerada do boletim — não bloqueia nada.

## Tabela de cotas N–X (fig. 10) — cm / polegadas

| Letra | cm | in | Uso |
|---|---|---|---|
| N | 5 | 2 | passo dos 3 furos do braço 8 |
| O | 3,2 | 1¼ | diâmetro da polia 10 |
| P | 1,7 | 43/64 | largura da polia 10 |
| Q | 0,6 | 1/4 | profundidade do canal (e Q° o ângulo) |
| R | 8,9 | 3½ | gancho 11 — alcance horizontal |
| S | 5 | 2 | gancho 11 — queda vertical |
| T | 2,5 | 1 | gancho 11 — altura da ponta virada |
| U | 4,4 | 1¾ | base 6 — passo dos furos |
| V | 1,6 | 5/8 | base 6 — aba |
| W | 3,5 | 1⅜ | base 6 — largura |
| X | 1,2 | 1/2 | base 6 — espessura/aba menor |

Leiaute (fig. 15/16): **Y = 22 mm** e **Z = 124 mm** — posição do trem e do
eixo do cabeçote em relação à borda de trás da bancada. **Decisão
2026-11-08: manter o leiaute central** (Y 152,5) como base da montagem 3D;
a cota da fig. 15/16 fica registrada para uma eventual migração (Z 124 pode
ser até a face do bloco 1B ou até o eixo do tubo — a decidir quando for
migrar).

## Impacto nos modelos já feitos (conferência fechada 2026-11-08)

Estes modelos foram feitos **antes** de as figuras aparecerem, derivados da
função/texto. Foram conferidos e corrigidos:

| Modelo | Cota nova | Situação |
|---|---|---|
| `gancho_tela` (11) | R 89 / S 50 / T 25 | ✅ **reworkado** (17:39) — olho Ø3,2 + corpo com dobra 45°, U r10, perna T; bbox 95,475 × 3,25 × 56,475; V 1.248,015 mm³ |
| `trem_tensao` base (6) | U 44 / V 16 / W 35 / X 12 | ✅ **reworkado** (17:50) — chapa em L 112 × 16/35 × 4,8 (não mais cantoneira 70×190×6); furação U 44 aplicada **e propagada à bancada** (trem_pitch 62 → 44, furos 2044/2088/2132 — depois
reposicionados na diagonal 45° em 2026-11-09: 2826,6/199,6 · 2857,7/230,8 ·
2888,9/261,9, ver NOTAS) |
| `trem_tensao` polias (10) | O 32 / P 17 / Q 6 | ✅ **reworkado** — Ø32 × 17, canal V boca 5 a 60°; **venceu a fig. 9** (o texto 1½–2" é recomendação genérica) |
| `bancada` leiaute | Y 22 / Z 124 | ⏸ **decisão: manter central** (Y 152,5) — fig. 15/16 registrada para migração futura |
| `bancada` furação 1A | — | ✅ **corrigido**: 2880 → **2952** (bloco 72 mm fora do fim do tubo, folga 10 mm p/ lâmina que chega a 2912) |

Volumes conferidos (analítico × B-rep): gancho 1.248,015 × 1.248,0;
trem 58.900,461 × 58.900,311 — ambos dentro de 0,01%.
