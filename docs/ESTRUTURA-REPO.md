---
title: "Estrutura do Repositório Academ'IA"
description: "Mapa canônico de pastas, arquivos, e proveniência. Source of truth para 'onde está X?'"
tags: [docs, estrutura, repo, mapa, organizacao, navegacao, canon]
version: 1.0.0
last_updated: 2026-07-28
pattern: "MMN_IA"
---

# 🗂️ Estrutura do Repositório Academ'IA

> **Mapa canônico** de pastas, arquivos e proveniência. Responde a pergunta **"onde está X?"** de forma definitiva. Atualizado em 2026-07-28 após reorganização v1.7.7 (Mavis Agent).

## 🎯 Filosofia

O repositório segue 5 princípios de organização:

1. **Source of truth explícito** — cada tipo de asset tem um caminho canônico
2. **Convenção sobre configuração** — nomes previsíveis (kebab-case, prefixos por trilha)
3. **Manifest-driven** — manifest.json declara metadados canônicos
4. **Git-tracked quando small, LFS quando grande** — MDs versionados, MP4s grandes em LFS
5. **Multi-dev safe** — sem duplicação, sem sobreposição, com `GUIA_MULTI_DEV.md` como contrato

## 📂 Raiz (4 arquivos canônicos)

| Arquivo | Função | Mantido por |
|---------|--------|-------------|
| `INDEX.md` | Mapa completo do repo (fonte da verdade) | Mavis Agent + multi-dev |
| `README.md` | Overview público da plataforma | Mavis Agent + CTO |
| `CHANGELOG.md` | Histórico de versões semver | Mavis Agent + todos |
| `GUIA_MULTI_DEV.md` | Contrato de colaboração multi-dev | Mavis Agent |

> ⚠️ **Regra:** apenas esses 4 .md devem ficar na raiz. Documentação vai em `docs/`.

## 📚 `docs/` — Documentação geral

| Sub-conjunto | Função | Tamanho típico |
|--------------|--------|----------------|
| `FAQ.md` | Perguntas frequentes | 8.8KB |
| `RESUMO_EXECUTIVO.md` | TL;DR de 1 página | 5.3KB |
| `ANALISE_TECNICA_E_ROADMAP.md` | Auditoria completa + roadmap 90 dias | 14.9KB |
| `ACADEMIA_MANIFEST_OPERACIONAL_*.md` | Manifestos operacionais datados | 3-7KB cada |
| `*_AUDITORIA_*.md` | Relatórios de auditoria (YouTube, capas, voz) | 5-15KB cada |
| `MANIFESTO_REBUILD_*.md` | Manifestos de rebuilds datados | 5-10KB |
| `FILA_YOUTUBE_*.md` | Filas de povoamento do YouTube | 3-5KB |
| `REPO_SPLIT_GOVERNANCA_*.md` | Governança de split de repos | 5KB |
| `MATERIAIS_PENDENTES_*.md` | Listas de materiais pendentes | 3-5KB |
| `ebook/` | Capas de ebooks em webp | ~5MB total |
| `ebooks/` | Capas de ebooks (versão 2) | ~10MB total |
| `reports/` | Relatórios de bottleneck/auditoria | 25KB+ |

## 🎓 Conteúdo Pedagógico (estrutura por tipo)

### `cursos/` — 4 trilhas oficiais
```
cursos/
├── fundamental/    (Trilha F, 6 cursos, iniciante)
├── agente/         (Trilha A, 4 cursos, intermediário)
├── master/         (Trilha M, 7 cursos, avançado)
├── elite/          (Trilha E, 3 cursos, expert)
└── INDEX.md        (panorama das 4 trilhas)
```

**Convenção:** cada curso tem 3 artefatos (cânonicos):
- `XX-nome.md` (descrição + plano)
- `XX-nome-slides.md` (apresentação)
- `XX-nome-roteiro.md` (script de vídeo)

**Versões estendidas:** sufixo `-mavis-detalhado` (convive com canônico).

### `apostilas/` — Material escrito extenso
```
apostilas/
├── NN-titulo.md           (40+ apostilas, 1-43)
├── html/                  (renderizações HTML para web)
├── apostilas_pdf/         (removido v1.7.3 — consolidado em pdfs/)
├── certificacao/          (material de certificação)
├── landing_pages/         (landing pages de venda)
└── imagens/               (assets gráficos)
```

### `tutoriais/` — How-to rápidos (15 min)
```
tutoriais/
├── NN-titulo.md           (38 tutoriais, 01-30+)
├── INDEX.md               (índice navegável)
└── README.md              (visão editorial)
```

### `treinamentos/` — Workshops gravados
```
treinamentos/
├── WS-NN-nome.md          (9+ workshops)
├── treinamento-*.md       (formato alternativo)
├── workshop-*.md
├── INDEX.md
└── README.md
```

### `webinars/` — Sessões ao vivo/sob demanda
```
webinars/
├── WB-AAAA-NN-titulo.md           (20+ webinars)
├── WB-AAAA-NN-titulo-roteiro.md   (roteiro de narração)
└── README.md
```

### `playbooks/` — Manuais operacionais
```
playbooks/
├── PB-*.md                (15 playbooks)
├── INDEX.md
└── README.md
```

### `certificacoes/` — 5 certificações
```
certificacoes/
├── CEN-*.md
├── CEN-plus-*.md
├── CON-*.md
├── CNX-*.md
├── MAS-plus-*.md
├── banco-questoes-*.md
├── simulado-*.md
└── README.md
```

## 🤖 Tecnologia de Agentes

### `Lib-Nexus/` — Biblioteca de referência
```
Lib-Nexus/
├── knowledge-base/        (conceitos, glossário, taxonomias — 9 docs)
├── agents-specs/          (contratos de agentes — 7 docs)
├── api-docs/              (documentação de APIs — 5 docs)
├── best-practices/        (padrões recomendados — 6 docs)
├── INDEX.md
└── README.md
```

### `Lab-Nexus/` — Bancada prática
```
Lab-Nexus/
├── prompts/
│   ├── copywriting/       (12 prompts)
│   ├── analise/           (6 prompts)
│   ├── estrategia/        (5 prompts)
│   └── governanca/        (4 prompts)
├── templates/             (HTML email, landing, social)
├── tools/                 (analytics, automation, copy, design, financas, marketing)
├── workflows/n8n/         (workflows N8N)
├── INDEX.md
└── README.md
```

### `governanca/` — Governança editorial/ética
```
governanca/
├── 04-politica-ia-responsavel.md
├── 05-ai-act-eu-compliance.md
├── C-SUITE-AI.md
├── PB-GOVERN-postmortem-blame-free.md
└── RATIFICACAO-LOOP-M4-M5-M7.md
```

## 🎬 Produção Audiovisual

### `materiais/video-aulas/` — Workspace canônico de vídeo-aulas
```
materiais/video-aulas/
├── fundamental/   (4 vídeo-aulas, codes 00-03)
├── agente/        (4 vídeo-aulas, codes 04-07)
├── master/        (4 vídeo-aulas, codes 08-11)
├── elite/         (3 vídeo-aulas, codes 12-14)
└── INDEX.md
```

**Estrutura de cada vídeo-aula:**
```
NN-nome/
├── manifest.json       ← declaração canônica
├── slides/             ← slides finais aprovados
├── roteiros/           ← roteiros canônicos
├── audios/             ← áudios narrados
├── capas/              ← capa + thumbnail
├── videos/             ← vídeo final renderizado
├── curso/              ← HTML + PDF de material de apoio
├── publicacao/         ← thumb YouTube + descrição TXT
└── rebuild/            ← re-renders com masters
```

### `producao/` — Pipeline de produção
```
producao/
├── assets/thumbnails/        (138MB — capas e thumbs)
├── catalog/                  (catálogo de módulos)
├── pipeline/                 (PIPELINE_PRODUCAO.md)
├── playbooks/                (playbooks de produção)
├── quality/                  (checklists de qualidade)
├── roteiros/                 (38 roteiros canônicos)
├── scripts/                  (scripts de produção)
├── templates/                (templates por persona)
├── AUDITORIA_CONSOLIDACAO.md
├── GO-LIVE-CHECKLIST.md
├── INCIDENT-RESPONSE-RUNBOOK.md
├── NGINX-CDN-CONFIG.md
├── PADRAO_VIDEOS_ACADEMIA.md
├── README.md
├── RENDER-PIPELINE.md
└── STATUS.md
```

### `videos/` — Histórico de ondas (v1.0)
```
videos/
├── roteiros/         (44 roteiros históricos, codes 00-19)
├── aulas-onda-47/    (audios, manifest, roteiros, thumbs)
├── aulas-onda-49/    (audios, manifest, piloto, renders, roteiros, scripts, slides, thumbnails, v2)
├── aulas-onda-50/    (em produção)
├── audio/            (áudios extras)
├── frames/           (frames extraídos)
├── scripts/          (scripts de produção)
├── thumbnails/       (thumbnails)
└── README.md
```

> ⚠️ `videos/` é o **histórico das ondas** (v1.0). Para novos vídeos, usar `materiais/video-aulas/`.

### `youtube/` — Operação do canal
```
youtube/
├── OPERACAO-CANAL.md                (Mavis Agent)
├── RUNBOOK-POVOAR-CANAL.md          (Mavis Agent)
├── publish_plan.json                (plano canônico)
├── publish_plan.csv                 (CSV)
├── upload_batch_ready.json          (fila de upload)
├── upload_queue_repovoamento_*.json (fila rebuild)
├── upload_results.json              (resultados de upload)
├── descriptions/                    (15 .txt)
├── thumbnails/                      (15 .png)
├── thumbnails_yt/                   (15 .jpg)
├── videos_teaser/                   (13 .mp4)
├── teaser_aliases.json
├── README.md
└── .gitignore                       (credenciais OAuth2)
```

### `html/` — Renderizações HTML
```
html/
├── index.html
├── admin.html
├── busca.html
├── mapa-academia.html
├── glossario.html
├── enhance.js
├── acad-style.css
├── apostilas/
├── cursos/
└── webinars/
```

### `pdfs/` — PDFs publicados (canônico único desde v1.7.3)
```
pdfs/        (81 PDFs, 70MB — apostilas + webinars + cursos)
```

> ⚠️ `pdf/` e `apostilas/apostilas_pdf/` foram **removidos** em v1.7.3 (consolidados em `pdfs/`).

### `marca/` — Identidade visual e vocal
```
marca/
├── personas/
│   ├── OFFICIAL_VOICES.md              (canônico)
│   ├── VOICES.md                       (legacy)
│   ├── VOZES-OFICIAIS.md               (legacy)
│   ├── alencar/                        (persona + assets + áudios)
│   ├── ive/                            (persona + assets + áudios)
│   ├── dupla/                          (co-apresentação)
│   ├── voice_registry/                 (registry de vozes)
│   └── _legacy/                        (versões deprecated — v1.7.7)
│       ├── GUIA_VOZES_OFICIAIS-legacy.md
│       └── GUIA-VOZES-OFICIAIS-legacy.md
└── INDEX.md                            (índice da marca)
```

### `producao/assets/` — Assets visuais
```
producao/assets/
├── thumbnails/         (138MB capas + thumbs de YouTube)
└── ...                  (outros assets)
```

## 🛠️ Operacional

### `scripts/` — Scripts Python/Bash
```
scripts/   (23 scripts — auditoria, sync, build, render, YouTube)
```

### `sync/` — Sincronização Academ'IA ↔ runtime
```
sync/
├── agent-bridge.json
├── skill-manifest.json
├── audit-log-schema.md
├── MCP-CONFIG.md
└── INDEX.md
```

### `hubs/` — Landing pages HTML estáticas
```
hubs/   (14 HTMLs — index, cursos, trilhas, apostilas, lib, lab, playbooks, webinars, tutoriais, certificacoes, comunidade, landing, player)
```

### `agent-sessions/` — Histórico de sessões de agentes
```
agent-sessions/
├── README.md
├── INDEX.md
└── 2026-06-03-mavis/    (sessão de auditoria histórica)
    ├── 00-README.md
    ├── 01-ANALISE_CRITICA_NEXUS.md
    ├── 02-REVISAO_DOCUMENTAL_NEXUS.md
    ├── 03-MAPEAMENTO_AI_VS_HUMANO.md
    ├── 04-ATUALIZACAO_LOCALIZACAO_DOC3.md
    └── 05-AUDITORIA_VOZES_OFICIAIS.md
```

### `reports/` — Relatórios de auditoria/bottleneck
```
reports/
├── BOTTLENECK-AUDIT-2026-07-26.md
└── PIPELINE-STATUS-2026-07-25.md
```

## 🔄 Histórico de Reorganizações

| Versão | Data | Ação | Por quê |
|--------|------|------|---------|
| 1.7.3 | 2026-07-27 | Consolidação de 3 fontes de PDF em `pdfs/` | GAP-03 do BOTTLENECK-AUDIT |
| 1.7.3 | 2026-07-27 | Remoção de `audit_hashes/` (8.8MB) | P0 do BOTTLENECK-AUDIT |
| 1.7.7 | 2026-07-28 | Movidos 3 docs da raiz para `docs/` | Limpeza de raiz |
| 1.7.7 | 2026-07-28 | Movidos 2 GUIAs legacy para `marca/personas/_legacy/` | Resolver duplicação |
| 1.7.7 | 2026-07-28 | Movido `roteiros_gerados.md` para `cursos/` | Era temporário, 0 refs |

## 📋 Onde está X? (referência rápida)

| Procurando | Onde está |
|------------|-----------|
| Como começar a usar a Academ'IA | `README.md` |
| Visão geral do repo | `INDEX.md` (raiz) |
| Histórico de mudanças | `CHANGELOG.md` (raiz) |
| Regras multi-dev | `GUIA_MULTI_DEV.md` (raiz) |
| FAQ | `docs/FAQ.md` |
| Resumo executivo | `docs/RESUMO_EXECUTIVO.md` |
| Roadmap | `docs/ANALISE_TECNICA_E_ROADMAP.md` |
| Vídeo-aulas | `materiais/video-aulas/INDEX.md` |
| Cursos | `cursos/INDEX.md` |
| Roteiros | `producao/roteiros/INDEX.md` |
| Playbooks | `playbooks/INDEX.md` |
| Tutoriais | `tutoriais/INDEX.md` |
| Treinamentos | `treinamentos/INDEX.md` |
| Personas | `marca/INDEX.md` |
| Agentes IA | `Lib-Nexus/agents-specs/` |
| API docs | `Lib-Nexus/api-docs/` |
| Prompts | `Lab-Nexus/prompts/` |
| YouTube | `youtube/OPERACAO-CANAL.md` |
| Personas legacy | `marca/personas/_legacy/` |

## 👥 Ownership

- **Owner:** Head de Operações + Head de Arquitetura
- **Mantenedor:** Equipe multi-dev
- **Cadência de revisão:** Trimestral

---

*Nexus Affil'IA'te · docs/ESTRUTURA-REPO.md · v1.0.0 · Julho 2026*
