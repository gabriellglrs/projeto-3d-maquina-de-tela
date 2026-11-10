# Referências — SolidCraft + OpenCode

## Como está montado aqui

| O quê | Onde |
|---|---|
| Config global (MCP `solidcraft` headless + `solidcraft-live`) | `C:\Users\gabri\.config\opencode\opencode.json` |
| Skills oficiais do SolidCraft | `C:\Users\gabri\.config\opencode\skills\solidcraft-*\` |
| Skills do nicho (fluxo-projeto-3d, serralheria, imp3d) | `C:\Users\gabri\.config\opencode\skills\` |
| Comandos rápidos `/novo-projeto` `/verificar` `/exportar` `/montagem` | `C:\Users\gabri\.config\opencode\commands\` |
| Projeto (designs, scripts, exports, fotos) | `C:\Users\gabri\SolidCraft-Projetos\` |

## Comandos úteis do terminal

```sh
solidcraft-cli mcp setup --client opencode   # regravar a config MCP após atualizar o SolidCraft
solidcraft-cli mcp setup --dry-run           # ver o que seria escrito, sem mudar nada
opencode mcp list                            # estado das conexões
solidcraft-cli run script.json --out p.part  # rodar um script JSON de comandos
solidcraft-cli commands                      # catálogo de comandos do CAD
```

## Links oficiais

- Site: https://solidcraft.io · Docs: https://docs.solidcraft.io · Guia MCP: https://docs.solidcraft.io/guide/mcp.html
- Repo: https://github.com/tangency-labs/solidcraft (docs em `docs/`, skills em `skills/`)
- Skills de modelagem: `docs/mcp.md`, `skills/solidcraft-modeling/reference.md`
- Comandos e capacidades: `docs/capabilities.md`, `docs/features.md`, `docs/scripts.md`
- Discord: https://discord.gg/FtU4NQNVDH

## Dicas de trabalho

- O servidor `solidcraft` roda **headless** (constrói em segundo plano). O `solidcraft-live` pega o app aberto — abra o SolidCraft para assistir a peça ser modelada.
- MCP só grava em `C:\Users\gabri\SolidCraft-Projetos` (allow-path). Para outra pasta, adicione `--allow-path` no `opencode.json`.
- Depois de atualizar o SolidCraft, rode de novo `solidcraft-cli mcp setup --client opencode --dry-run` para conferir o caminho do executável.
