---
title: "Guia de Trabalho Multi-Dev · AcademIA"
description: "Convenções obrigatórias para evitar sobrescritas, duplicidades e conflitos entre múltiplos devs/agentes"
tags: [guia, multi-dev, colaboracao, convencoes, governanca, academia]
last_updated: 2026-07-24
---

# 🤝 Guia de Trabalho Multi-Dev · AcademIA

> **LEITURA OBRIGATÓRIA** para todo dev/agente que trabalhar no AcademIA. Estabelece convenções para evitar sobrescritas, duplicidades conflitantes, e perda de trabalho.

## 👥 Devs em Operação Conjunta

Identificados até 2026-07-24:

| Dev/Agente | Branch/Tag | Escopo típico |
|---|---|---|
| **Mavis Agent** | commits `Mavis` (sufixo `-mavis-detalhado` em arquivos) | Slides estendidos, roteiros detalhados, docs de governança |
| **genspark_dev** | commit `d208624` | Geração em massa de materiais de trilhas (slides+roteiros canônicos) |
| **Nexus Deploy Bot** | `feature/*` branches | Infraestrutura, deploy, CI/CD |
| **CEO/AI Nexus** | PRs manuais | Direção estratégica, decisões de alto nível |
| **MMN AI-to-AI Agent** | origem `MMN_AI-to-AI` | Migração inicial de ebooks (já concluída) |
| **Nexus CTO Agent** | reviews | Arquitetura, segurança, compliance |

## ⚠️ Regras de Ouro (NÃO QUEBRAR)

### 1. NUNCA sobrescrever arquivo existente
- Antes de criar ou editar, **SEMPRE** verificar com `git pull` + `git status`.
- Se um arquivo já existe com mesmo nome, **NUNCA** sobrescrever. Em vez disso:
  - **Opção A**: Criar versão alternativa com sufixo (`-mavis-detalhado`, `-extended`, `-v2`)
  - **Opção B**: Abrir PR para discussão antes de modificar
  - **Opção C**: Comentar no CHANGELOG que a versão está sendo atualizada

### 2. SEMPRE fazer `git pull` antes de criar arquivos
```bash
cd /workspace/Academ-IA
git fetch origin
git pull --ff-only origin main  # fast-forward primeiro
# Se der conflito, mover seus arquivos para /tmp/staging e resolver manualmente
```

### 3. SEMPRE verificar se o arquivo já existe no remote
```bash
# Antes de criar
git ls-files | grep "cursos/master/04-"  # vê o que já existe
```

### 4. Convenção de Nomenclatura para Versões Alternativas

| Cenário | Sufixo | Exemplo |
|---|---|---|
| Versão estendida (mais cenas/conteúdo) | `-mavis-detalhado` | `04-rag-roteiro-mavis-detalhado.md` |
| Versão 2 (refatoração) | `-v2` | `05-deploy-slides-v2.md` |
| Rascunho em progresso | `-draft` | `07-novo-curso-draft.md` |
| Backup de migração | `-legacy` | `00-conversao-legacy.md` |

### 5. SEMPRE referenciar a versão canônica no frontmatter
```markdown
---
title: "..."
description: "[VERSÃO ESTENDIDA MAVIS] — complementar ao canônico: 04-rag-roteiro.md"
...
---

> ⚠️ **VERSÃO ESTENDIDA MAVIS** — complementar ao roteiro oficial em `04-rag-roteiro.md` (5 cenas).
```

### 6. CHANGELOG é obrigatório para qualquer commit
Adicionar entrada em `CHANGELOG.md` documentando:
- Arquivos criados/modificados
- Versão (bump minor: 1.6.0 → 1.6.1, 1.6.1 → 1.6.2)
- Conflitos resolvidos (se houve)
- Coordenação com outros devs (se houve)

### 7. Commits com mensagens claras
```bash
# Formato
<tipo>(<escopo>): <descrição curta>

# Exemplos
feat(academia): versão estendida Mavis dos cursos 04, 05, 06
docs(academia): CHANGELOG v1.6.1 — versões estendidas Mavis
fix(academia): corrige ref de áudio no roteiro 04
```

## 🔄 Workflow Recomendado (sem sobrescritas)

```bash
# 1. Sync com remote
cd /workspace/Academ-IA
git fetch origin
git status  # ver se tem mudanças locais não commitadas
git pull --ff-only origin main  # fast-forward

# 2. Antes de criar qualquer arquivo, verificar duplicidade
git ls-files | grep "caminho/proposto/"

# 3. Criar arquivo (com sufixo se já houver versão canônica)
echo "conteúdo..." > "caminho/novo-mavis-detalhado.md"

# 4. Verificar estado
git status

# 5. Adicionar APENAS arquivos novos (não modificados pelo remote)
git add caminho/novo-mavis-detalhado.md

# 6. Atualizar CHANGELOG.md
# Editar CHANGELOG.md com entrada v1.6.X

# 7. Commit
git commit -m "feat(academia): descrição clara"

# 8. Push
git push origin main
```

## 🛡️ Em Caso de Conflito Detectado

```bash
# SINTOMA: "These files would be overwritten by merge"
# 1. NÃO usar --force nem --delete
# 2. Mover seus arquivos para /tmp/staging/
mkdir -p /tmp/staging_mavis
mv "seu/arquivo.md" "/tmp/staging_mavis/seu_arquivo_MAVIS.md"

# 3. Agora faça o pull (deve passar)
git pull --ff-only origin main

# 4. Compare: o que tem no remote vs o que você tinha
diff "/tmp/staging_mavis/seu_arquivo_MAVIS.md" "seu/arquivo.md"

# 5. Decida: merge, sobrescrever (com sufixo), ou descartar
# Recomendado: sufixo para coexistir

# 6. Commit + push normalmente
```

## 📋 Convenções por Tipo de Material

### Slides de Curso
- Canônico: `cursos/{trilha}/NN-nome-slides.md` (genspark_dev gera padrão)
- Estendido: `cursos/{trilha}/NN-nome-slides-mavis-detalhado.md` (Mavis)
- Draft: `cursos/{trilha}/NN-nome-slides-draft.md`

### Roteiros de Vídeo
- Canônico: `cursos/{trilha}/NN-nome-roteiro.md`
- Estendido: `cursos/{trilha}/NN-nome-roteiro-mavis-detalhado.md`

### Tutoriais
- Numerados: `tutoriais/NN-titulo.md` (01-99)
- Séries especiais: `tutoriais/series-{nome}/NN-titulo.md`

### Documentação Raiz
- `README.md` — Apresentação
- `INDEX.md` — Índice geral
- `CHANGELOG.md` — Histórico
- `GUIA_*.md` — Guias de processo
- `RESUMO_*.md` — Resumos executivos
- `ROADMAP_*.md` — Planejamento

## 🎯 Quando Oficializar Versão Estendida

Uma versão `-mavis-detalhado` vira **canônica** quando:
1. Time de produção revisa e aprova
2. PR de consolidação é aberto (mesclando canônico + estendido)
3. Versão canônica antiga é movida para `_archive/` ou deletada com aviso

**ATENÇÃO**: não deletar arquivos sem aviso no CHANGELOG. Mover para `_archive/` é mais seguro.

## 📚 Documentos de Referência

- `governanca/C-SUITE-AI.md` — Governança executiva
- `governanca/PB-GOVERN-postmortem-blame-free.md` — Cultura de post-mortem
- `governanca/RATIFICACAO-LOOP-M4-M5-M7.md` — Ratificação de decisões
- `producao/GO-LIVE-CHECKLIST.md` — Checklist pré-deploy
- `producao/INCIDENT-RESPONSE-RUNBOOK.md` — Runbook de incidentes

---

**Versão 1.0** · Criado em 2026-07-24 · Mavis Agent · Pós-resolução de conflito com genspark_dev
