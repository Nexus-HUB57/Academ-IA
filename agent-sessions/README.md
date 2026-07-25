---
gerado_por: IA (modelo MiniMax-M3)
contexto: README da pasta agent-sessions/ no repo canônico Academ-IA
data: 2026-07-24 (revisado pós GUIA_MULTI_DEV.md)
versao: 2.0
referencias_canonicas:
  - GUIA_MULTI_DEV.md (convenções obrigatórias multi-dev, criado 2026-07-24)
  - CHANGELOG.md (v1.6.3, 2026-07-24)
  - INDEX.md (fonte da verdade do repo)
---

# agent-sessions/

Esta pasta contém **artefatos gerados por agentes de IA** que trabalharam neste repositório em sessões específicas de chat, sob autorização do owner.

> ⚠️ **REGRA MULTI-DEV**: Este diretório segue as convenções do [`GUIA_MULTI_DEV.md`](../GUIA_MULTI_DEV.md) (criado 2026-07-24, Mavis Agent, pós-resolução de conflito Mavis × genspark_dev). Em particular:
> - Pasta `agent-sessions/` é dedicada a **artefatos de auditoria/análise** de IAs, não a materiais didáticos.
> - Materiais didáticos (slides, roteiros, apostilas) usam sufixo `-mavis-detalhado` em pastas próprias.
> - Nunca sobrescrever arquivo existente — sempre criar nova versão.
> - CHANGELOG.md é obrigatório para qualquer commit.

## Convenção de nomenclatura

```
agent-sessions/
└── YYYY-MM-DD-<nome-do-agente>/
    ├── 00-README.md                          (índice da sessão)
    ├── 01-...md                              (artefato 1)
    ├── 02-...md                              (artefato 2)
    └── ...
```

- `YYYY-MM-DD` = data de início da sessão
- `<nome-do-agente>` = identificador do agente (ex: `mavis`, `genspark`, `nexus-agente-ia`)

## Header obrigatório em cada artefato

Todo arquivo `.md` nesta pasta **deve** começar com YAML frontmatter incluindo pelo menos:

```yaml
---
session_id: <string>
agent: <nome-do-agente> (<modelo>)
data_sessao: <ISO 8601 start - end>
gerado_por: IA / humano / pipeline
contexto_sessao: <descrição em 1-2 frases>
nota_proveniencia: <aviso de proveniência IA se aplicável>
categoria: <analise|revisao|governanca|errata|...>
versao: <semver>
conflito_multi_dev: NENHUM | <descrição do conflito>
---
```

Adicione `conflito_multi_dev: NENHUM` se a criação do arquivo **não** sobrescreve nem duplica nada existente no remote. Caso contrário, descreva o conflito e a resolução.

## Lista de sessões registradas

| Sessão | Data | Agente | Modelo | Artefatos | Status |
|--------|------|--------|--------|-----------|--------|
| 2026-06-03-mavis | 2026-06-02 → 2026-06-03 | Mavis | MiniMax-M3 | [5 docs](./2026-06-03-mavis/) | re-migrado do repo legado em 2026-07-23 |
| 2026-07-22-mavis | 2026-07-22 | Mavis | MiniMax-M3 | 1 doc na raiz (`../GUIA_VOZES_OFICIAIS.md`) | commit `9886e5b` (no legado) / trabalho continuou no canônico |
| 2026-07-24-mavis | 2026-07-24 | Mavis | MiniMax-M3 | 1 doc aqui (`./2026-06-03-mavis/05-AUDITORIA_VOZES_OFICIAIS.md`) | esta sessão, v2.0 da auditoria |

## Política de retenção

- Artefatos nesta pasta **não são** documentação oficial do produto.
- Artefatos podem ser **movidos para `archive/`** após 90 dias, a critério do owner.
- Artefatos podem ser **deletados** se o owner decidir, mas o histórico fica no `git log`.
- Auditorias devem ser **versionadas** quando dados de base mudam (ex: minha auditoria de vozes passou de v1.0 → v2.0 quando os arquivos de áudio foram atualizados).

## Relação com outros diretórios

| Pasta | Conteúdo | Relação |
|-------|----------|---------|
| `governanca/` | Decisões editoriais, regras de produção | agent-sessions é fonte de **uma** decisão; governanca é o **acumulado** |
| `producao/` | Pipeline de produção de conteúdo | agent-sessions pode gerar specs que vão para `producao/` |
| `marca/personas/` | Identidade das personas (Ive, Alencar) | agent-sessions pode auditar consistência |
| `GUIA_MULTI_DEV.md` (raiz) | Convenções multi-dev | **OBRIGATÓRIO** ler antes de criar/modificar arquivos |

## Onde reportar problema

Se um artefato em `agent-sessions/` estiver incorreto, desatualizado ou problemático:
1. Abrir issue no GitHub
2. Mencionar `session_id` e `data_sessao`
3. Citar a fonte canônica que conflita (ex: REGISTRY, INDEX, CHANGELOG)

## Histórico desta pasta

- **2026-07-23**: primeira entrada (sessão 2026-06-03-mavis re-migrada do repo legado)
- **2026-07-24**: revisão pós GUIA_MULTI_DEV.md; auditoria de vozes atualizada para v2.0

---

**Mantido por:** owner + agentes de IA autorizados.
**Versão deste README:** 2.0 (2026-07-24).
