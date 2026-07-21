---
title: "CHANGELOG · Academ'IA"
description: "Histórico de versões da Academ'IA · HUB de Conhecimento & Sabedoria"
tags: [changelog, versionamento, historico, academia]
version: 1.5.0
last_updated: 2026-07-21
---

# 📜 CHANGELOG · Academ'IA

> Histórico de versões do HUB Academ'IA — Nexus Affil'IA'te. Segue **Semantic Versioning**: MAJOR (breaking), MINOR (compatível, novo asset), PATCH (correções, polish).

---

## [v1.4.2] — 2026-07-21

### Adicionado
- **Apostila 34**: Análise Técnica AI_Doctor (migrada de `Nexus-HUB57/AI_Doctor`)
- **Lib-Nexus/knowledge-base/08-oncologia-rag-knowledge.md**: Base de conhecimento RAG de oncologia (imunoterapia, DIMHEX, nanotecnologia, algoritmo de predição)
- **Tutoriais ARQ-01 e ARQ-02**: Arquitetura completa v2.0 e Resumo de desenvolvimento (migração)
- INDEX.md atualizado com nova trilha "AI_Doctor · Plataforma Clínica"

### Migrado de
- `Nexus-HUB57/AI_Doctor` (preservado, sem exclusões) — apenas cópia didática

## [1.5.0] — 2026-07-21 · "Populando repo dedicado com ebooks + capas autorais"

### ✨ Adicionado (71 arquivos, ~43 MB em ebooks/)

Cópia autoral completa das 5 coleções da plataforma `Nexus-HUB57/MMN_AI-to-AI` para o repo dedicado `Nexus-HUB57/Academ-IA`. Origem controlada, zero riscos de copyright (mesmo owner, transferência interna do time). Manifesto completo em `ebooks/INDEX.md`.

**Coleção NEXUS_AFFIL_IA_TECH — 11 arquivos (Onda 40 âncora PhD-level):**
- 5 eBooks .md (~32 KB cada) · 5 capas .webp (~5 MB cada)
- `01_orquestracao_ecossistemas_ia.md` · multi-agente em produção
- `02_senciencia_e_barreiras.md` · o problema difícil da consciência sintética
- `03_poder_perigo_autonomia_ai.md` · do Copilot ao fully autonomous
- `04_fundamento_saas_ia.md` · pilha canônica de SaaS agêntico
- `05_poder_processamento_ia.md` · GPU/TPU/NPU, KV cache, custo/token
- Manifesto de coleção: `README.md` + `covers/` (5 WebP originais)

**Coleção AXIOMA_PRIME — 22 arquivos (arquitetura agentica fundacional):**
- 10 eBooks .md + 11 capas (10 caps + 1 README) WebP originais
- De "01_arquitetura_do_despertar_agentico" → "10_civilizacao_agentica_e_o_grande_pacto"
- Manifesto: `README.md` + `covers/README.webp`

**Coleção SE_EU_IA_FOSSE_HUMANO — 11 arquivos (poética IAS):**
- 5 eBooks .md (~50 KB cada) + 5 capas WebP originais (60-64)
- De "Se eu IA tivesse um Corpo" → "Se eu IA fosse Mortal"
- Manifesto: `README.md`

**Coleção IA_Perfeita — 20 arquivos (3 séries iterativas):**
- 12 eBooks .md (vol 1/2/3 original + v1 + v2) + 7 capas WebP
- Inclui: "o sussurro das máquinas", "cartas de um algoritmo a deus", "biblioteca infinita de Babel 2.0"
- Manifesto: `README.md`

**Coleção MMN_IA — 7 arquivos (coleção-raiz do ecossistema):**
- 6 eBooks/Guias .md + 1 capa de coleção
- README + GITHUB_SYNC_GUIDE + PUBLICACAO + 01_ia_para_empresas + 02_ia_agentica + 15_ecossistema_ia_governanca + capa

**Manifesto geral:**
- `ebooks/INDEX.md` (6763 bytes) com frontmatter, tabela por coleção, métricas, MUST-verify de origem

### 🛡️ Verificações de integridade aplicadas

- **md5 src == dst** em todos os 71 arquivos (MISMATCH: 0) — cópia bit-perfect do legado
- **size src == size dst** em todos os 71 arquivos
- **`cp --no-clobber`** — nenhum dos arquivos pré-existentes foi sobrescrito
- **Origem autoral confirmada mesma owner**: `Nexus-HUB57/MMN_AI-to-AI` → `Nexus-HUB57/Academ-IA`

### 📊 Métricas atualizadas

| Métrica | v1.4.1 | v1.5.0 | Δ |
|---|---|---|---|
| eBooks .md em ebooks/ | 0 | **42** | +42 |
| Capas .webp em ebooks/ | 0 | **29** | +29 |
| Tamanho ebooks/ | 0 | **~43 MB** | +43 MB |
| Coleções representadas | 0 | **5** | +5 |

---

## [1.4.1] — 2026-07-21 · "Sync repo dedicado Academ-IA + 30 materiais do legado"

### ✨ Adicionado (30 arquivos, +9964 linhas)

Migração dos 30 arquivos que estavam em `MMN_AI-to-AI/repo/AcademIA/` mas **ausentes** do repo dedicado `Nexus-HUB57/Academ-IA`. Commit `23d2500` no Academ-IA preservando intactos os 685 arquivos pré-existentes (zero deleções).

**Apostilas .md (2 novas):**
- `apostilas/32-pricing-ia-2026.md` — Pricing IA 2026: pricing dinâmico, unit economics, unit cost em escala
- `apostilas/33-data-stack-agentes-ia.md` — Data Stack Agentes IA: lakehouse, feature store, vector DB, observabilidade de modelos

**Cursos slides .md (3 novos):**
- `cursos/agente/00-primeiro-agente-slides.md` — Slides do primeiro agente
- `cursos/elite/00-blueprints-elite-slides.md` — Slides Blueprints Elite
- `cursos/master/00-otimizacao-conversao-slides.md` — Slides Otimização de Conversão

**Hubs HTML (4 novos):**
- `hubs/cursos.html` — índice interativo das trilhas
- `hubs/landing.html` — landing page pública da Academia
- `hubs/player.html` — player para vídeo/áudio
- `hubs/trilhas.html` — seletor de trilhas com profiles

**Apostilas HTML (2 novas):**
- `html/apostilas/32-pricing-ia-2026.html` — renderização HTML da apostila 32
- `html/apostilas/33-data-stack-agentes-ia.html` — renderização HTML da apostila 33

**Webinars HTML (4 novos):**
- `html/webinars/WB-2026-08-financeiro-ia.html`
- `html/webinars/WB-2026-12-ia-to-ia-federation.html`
- `html/webinars/WB-2026-14-pricing-ia-tempo-real.html`
- `html/webinars/WB-2026-15-data-stack-ia.html`

**Webinars .md (2 novos):**
- `webinars/WB-2026-14-pricing-ia-tempo-real.md`
- `webinars/WB-2026-15-data-stack-ia.md`

**PDFs (6 novos):**
- `pdfs/32-pricing-ia-2026.pdf`
- `pdfs/33-data-stack-agentes-ia.pdf`
- `pdfs/webinar-WB-2026-08-financeiro-ia.pdf`
- `pdfs/webinar-WB-2026-12-ia-to-ia-federation.pdf`
- `pdfs/webinar-WB-2026-14-pricing-ia-tempo-real.pdf`
- `pdfs/webinar-WB-2026-15-data-stack-ia.pdf`

**Personas · assets PNG (5 novos):**
- `personas/alencar/assets/alencar_meeting_v1.png` (~4 MB)
- `personas/alencar/assets/alencar_nexus_ref_1.png` (~4 MB)
- `personas/ive/assets/ive_nexus_ref_1.png` (~4 MB)
- `personas/ive/assets/ive_reference.png` (~4 MB)
- `personas/ive/assets/ive_training_v1.png` (~4 MB)

**Produção (1 novo):**
- `producao/INCIDENT-RESPONSE-RUNBOOK.md` — runbook TI 1 página (SEV-1/2/3, contatos, RCA, comunicação)

**Vídeo PoC (1 novo):**
- `videos/video-00-boas-vindas-poc.mp4` (~2 MB) — boas-vindas PoC trilha Fundamental

### 🛡️ Verificações de integridade aplicadas

- **md5 src == md5 dst** em todos os 30 arquivos (MISMATCH: 0) — cópia bit-perfect do legado
- **size src == size dst** em todos os 30 arquivos
- **`cp --no-clobber`** — nenhum dos 685 arquivos pré-existentes foi sobrescrito
- **Re-diff encoding-aware** pós-cópia → 0 missing restantes, 15 target-only preservados
- **GitHub API stats**: `+9964 / −0` (zero deleção confirmada)

### 📊 Métricas atualizadas

| Métrica | v1.4.0 | v1.4.1 | Δ |
|---|---|---|---|
| Apostilas | 31 | **33** | +2 |
| Webinars | 13 | **15** | +2 |
| Hubs HTML | 0 | **4** | +4 |
| Cursos slides | 14 | **17** | +3 |
| PDFs apostila | 6 | **8** | +2 |
| PDFs webinar | 13 | **17** | +4 |
| Personas assets | 6 | **11** | +5 |
| Runbooks produção | 0 | **1** | +1 |
| Vídeos PoC | 0 | **1** | +1 |
| Arquivos totais | 685 | **715** | +30 |
| Linhas totais (md) | ~15k | **~16k** | +1k |

### 🎯 Arquivos target-only preservados (NÃO foram tocados)

- `tutoriais/12-federação-2-nos.md` (encoding NFD já no Academ-IA)
- `tutoriais/13-federação-3-nos-mtls-pinned.md` (encoding NFD já no Academ-IA)
- `personas/alencar/Estes_são_os_personas_Ive_Nexu.mp4`
- `pdfs/webinar-WB-2026-08-ia-to-ia-federation.pdf` (federação, distinto do financeiro)
- `videos/roteiros/15-19-*.md` (roteiros-âncora TECH)
- `videos/thumbnails/thumb-15-19-*.webp` (thumbnails 2K TECH)
- `videos/video-00-boas-vindas-renderizado.mp4` (versão final, distinta do PoC)

---

## [1.2.5] — 2026-07-07 · "Expansão Monetização + Automação"

### ✨ Adicionado

**Apostilas (1 nova):**
- `apostilas/19-monetizacao-avancada-escala.md` — 6 pilares de receita além de afiliação: produto digital, mentoria, SaaS, mídia, licensing, community. Roadmap R$ 0 → R$ 300k/mês em 24 meses.

**Workshops (1 novo):**
- `treinamentos/WS-06-oficina-automacao-conteudo.md` — Pipeline 5 agentes (Researcher, Planner, Writer, Editor, Designer) com checkpoints humanos. Escala 10x produção sem perder qualidade.

**Templates HTML (2 novos):**
- `Lab-Nexus/templates/social/03-template-stories-engajamento.html` — 8 stories prontos (gancho, dor, prova, aula, quiz, enquete, bastidores, CTA)
- `Lab-Nexus/templates/email/05-template-onboarding-sequencia.html` — Sequência 5 emails D+0 a D+4 com merge tags e métricas-alvo

**Prompts (2 novos):**
- `Lab-Nexus/prompts/analise/05-analise-concorrencia-profund.md` — Mapa competitivo 5-10 players, gaps, posicionamento defensável
- `Lab-Nexus/prompts/estrategia/05-okr-trimestral-equipe.md` — OKRs completos time 3-15 pessoas, 3 Objectives + KRs mensuráveis

### 📊 Métricas

| Métrica | v1.2.3 | v1.2.5 | Δ |
|---|---|---|---|
| Apostilas | 12 | **13** | +1 |
| Prompts | 12 | **14** | +2 |
| Templates | 9 | **11** | +2 |
| Workshops | 5 | **6** | +1 |
| Tutoriais | 27 | 27 | = |
| Tools | 45 | 45 | = |
| Workflows | 5 | 5 | = |
| Playbooks | 10 | 10 | = |
| Webinars | 10 | 10 | = |
| Certificações | 5 | 5 | = |
| **TOTAL** | **149** | **155** | **+6** |

---

## [1.2.3] — 2026-06-28 · "Consolidação (merge v1.2.0 + v1.2.2)"

Esta versão consolida as contribuições das duas branches paralelas:

### ✨ Adicionado (Branch A — v1.2.0)

**Apostilas (2 novas):**
- `apostilas/17-seo-marketing-conteudo-ia.md` — Framework AEO/GEO para IAs generativas
- `apostilas/18-seguranca-ofensiva-pentest-agentes-ia.md` — Red Team Bible com 23 vetores

**Tutoriais (5 novos):**
- `tutoriais/11-auditoria-skills-master.md`
- `tutoriais/12-configurar-ab-test-judge.md`
- `tutoriais/13-deploy-multi-tenant-elite.md`
- `tutoriais/14-agente-federado-elite.md`
- `tutoriais/15-auditoria-lgpd-automatizada.md`

**Certificações (1 nova):**
- `certificacoes/MAS-plus-certificacao-master-plus.md`

### ✨ Adicionado (Branch B — v1.2.2)

**Tutoriais (6 novos):**
- `tutoriais/16-debugar-agente-lento.md` (renomeado para 15)
- `tutoriais/17-criar-skill-customizada.md`
- `tutoriais/18-integrar-meta-ads.md`
- `tutoriais/19-configurar-backup-automatico.md`
- `tutoriais/20-ler-metricas-sho.md`
- `tutoriais/21-exportar-relatorio-mensal.md`

**Playbooks (2 novos):**
- `playbooks/PB-LANCAMENTO-black-friday.md`
- `playbooks/PB-ONBOARDING-novo-afiliado.md`

**Webinars (2 novos):**
- `webinars/WB-2026-04-agentes-autonomos-prod.md`
- `webinars/WB-2026-05-multi-tenant.md`

**Workflows (2 novos):**
- `Lab-Nexus/workflows/make/02-workflow-recovery-carrinho.json`
- `Lab-Nexus/workflows/n8n/03-workflow-onboarding-trial.md`

**Prompts (4 novos):**
- `Lab-Nexus/prompts/analise/04-diagnostico-churn-preventivo.md`
- `Lab-Nexus/prompts/copywriting/08-copy-headline-anuncio.md`
- `Lab-Nexus/prompts/copywriting/09-script-vsl.md`
- `Lab-Nexus/prompts/estrategia/04-plano-conteudo-90-dias.md`

### 📊 Métricas Consolidadas

| Métrica | Antes (v1.1.1) | Agora (v1.2.3) | Δ |
|---|---|---|---|
| Apostilas | 10 | **12** | +20% |
| Tutoriais | 14 | **21** | +50% |
| Certificações | 4 | **5** | +25% |
| Tools | 40 | **44** | +10% |
| Prompts | 8 | **11** | +38% |
| Templates | 3 | **6** | +100% |
| Workflows | 3 | **5** | +67% |
| Playbooks | 7 | **10** | +43% |
| Webinars | 3 | **6** | +100% |
| Workshops | 6 | **8** | +33% |
| Cursos | 15 | **15** | = |
| Total Assets | **113** | **158** | **+40%** |

---

## [1.2.0] — 2026-06-28 · "Expansão Master & Elite"
>>>>>>> origin/main

### ✨ Novos Materiais (8)

**Apostilas (2 novas):**
- `apostilas/17-seo-marketing-conteudo-ia.md` — Framework AEO/GEO para ser citado por IAs generativas (substituindo SEO clássico). 7 camadas de conteúdo, schema markup para IAs, métricas de GEO.
- `apostilas/18-seguranca-ofensiva-pentest-agentes-ia.md` — Red Team Bible com 23 vetores de ataque contra sistemas multi-agente. Prompt injection, tool abuse, memory poisoning, federation attacks, supply chain.

**Tutoriais (5 novos):**
- `tutoriais/11-auditoria-skills-master.md` (TUT-MAS-04) — Análise completa de uso, segurança e saúde das skills do agente.
- `tutoriais/12-configurar-ab-test-judge.md` (TUT-MAS-05) — A/B testing com significância estatística (p < 0.05) e decisão automática via Judge.
- `tutoriais/13-deploy-multi-tenant-elite.md` (TUT-ELI-01) — Plataforma SaaS white-label com RLS, billing, e 3 planos.
- `tutoriais/14-agente-federado-elite.md` (TUT-ELI-02) — mTLS, marketplace de skills, billing settlement, governança.
- `tutoriais/15-auditoria-lgpd-automatizada.md` (TUT-ELI-03) — Scanner de PII, DPIA, right to be forgotten, notificação 72h.

**Certificações (1 nova):**
- `certificacoes/MAS-plus-certificacao-master-plus.md` — Master Plus (MAS+), intermediária entre CEN e CEN+. 60 dias, 5 core skills + 3 advanced skills + soft skills.

### 📊 Estatísticas
- Apostilas: 10 → **12** (+20%)
- Tutoriais: 10 → **15** (+50%)
- Certificações: 4 → **5** (+25%)

### 🎯 Tópicos Cobertos
- **SEO/GEO** — novo framework AEO/GEO com 7 padrões para citar em IAs generativas
- **Red Team** — 23 vetores de ataque + PoC + defesas
- **Multi-tenant SaaS** — RLS + billing + white-label
- **Federated Agents** — mTLS + marketplace + governance
- **LGPD Automation** — DPIA + right to be forgotten + incident notification

---

## [1.1.1] — 2026-06-02 · "Integridade de manifestos"

### 🩹 Correções

- **2 skills reclassificadas** de operacional → planned (handlers `.ts` ainda não implementados):
  - `sms-conversacional` → `planned_release: Q3-2026`
  - `plano-conteudo-90d` → `planned_release: Q3-2026`
- **3 skills adicionadas ao manifesto** que já existiam como handlers `.ts` no monorepo mas estavam órfãs:
  - `cold-emailer` (handler `coldEmailer.ts` existe)
  - `webhook-router` (handler `webhookRouter.ts` existe)
  - `backup-encryption` (planned, `Q4-2026` — handler ainda não existe)
- **`types.ts`** adicionado à `operational_skills_audit.handlers` (estava listado em disco mas ausente do audit)
- **Todos os `course_anchor` do manifesto** prefixados com `AcademIA/` (resolve paths relativos ambíguos)
- **`lab_nexus_to_skill_mapping` do agent-bridge** — todos os paths prefixados com `AcademIA/`
- **`trirf_mapping.courses_completed_required` do agent-bridge** — todos os paths prefixados com `AcademIA/`

### 🛠️ Tooling

- **Novo GitHub Action** `checks/skill-manifest-integrity.yml`:
  - Roda em PR e push que tocam manifesto, bridge, cursos, lab ou handlers
  - Valida schema, contadores (`total_skills`/`operational`/`planned`), slugs únicos kebab-case, whitelists (`category`, `level`, `trilha_academia`)
  - Valida paths de skills (`code_path`, `spec_path`, `lab_path`, `course_anchor`)
  - Valida `lab_nexus_to_skill_mapping` (paths existem + slugs batem com manifesto)
  - Valida `trirf_mapping.courses_completed_required` (paths existem)
  - Sanity check do `operational_skills_audit` (handlers declarados vs handlers em disco)
  - Exit code != 0 falha o CI; report legível com erros categorizados
- **Validador Python standalone** `checks/lib/validate_manifest.py` (sem deps externas, Python 3.11+)

### 📊 Métricas

| | v1.1.0 | v1.1.1 |
|---|---|---|
| `manifest_version` | 1.1.0 | 1.1.1 |
| `total_skills` | 16 | 19 |
| `operational` | 15 | 15 |
| `planned` | 1 | 4 |
| `operational_skills_audit.total_handlers` | 27 | 28 |

---

## [1.1.0] — 2026-06-02 · "Consolidação + Onboarding Elite"

### ✨ Adicionado

- 📕 **2 tutoriais novos**:
  - `tutoriais/13-federação-3-nos-mtls-pinned.md` — escalando federação para 3+ nós com mTLS pinned, capacidades e TTL de aprovação (Nível Elite)
  - `tutoriais/14-ler-skill-manifest.md` — como ler e contribuir no `skill-manifest.json` (Nível Agente)

- 🧪 **2 ferramentas novas no Lab-Nexus**:
  - `tools/marketing/09-plano-conteudo-90-dias.md` — planejamento trimestral de conteúdo com funil integrado (Nível Master)
  - `tools/copy/13-disparo-sms-conversacional.md` — templates + prompt para SMS transacional/relacional (Nível Agente)

- 💡 **2 prompts novos** (fechando lacunas do INDEX):
  - `prompts/analise/03-diagnostico-funil-completo.md`
  - `prompts/estrategia/03-posicionamento-competitivo.md`

- 📡 **1 webinar novo** (anúncio + preparação):
  - `webinars/WB-2026-03-academia-open-house.md` — Open House de 2026-06-15 (🟡 agendado)

- 📑 **Novos documentos de governança**:
  - `RESUMO_EXECUTIVO.md` — TL;DR de 1 página (entrada única)
  - `CHANGELOG.md` (este arquivo)

### 🩹 Correções

- `sync/skill-manifest.json`:
  - `code_path` de `white-label-sync` corrigido: `fase7/whiteLabelSync.ts` (inexistente) → `backend/src/domains/whitelabel/index.ts`
  - `code_path` de `federation-gate` corrigido: `fase8/federation/gate.ts` (inexistente) → `AcademIA/Lib-Nexus/agents-specs/03-federation-gate.md` (com flag `spec_only: true`)
  - Adicionada seção `operational_skills_audit` com 27 paths validados no monorepo
  - Adicionadas 2 skills novas: `plano-conteudo-90d` e `sms-conversacional`

- `sync/agent-bridge.json`:
  - Adicionados 2 mapeamentos novos em `lab_nexus_to_skill_mapping` (plano-conteudo-90d + sms-conversacional)
  - Bump de `academia_version` para `1.1.0`

### 🔄 Modificado

- `tutoriais/README.md` — catálogo agora lista 14 tutoriais (era 12)
- `INDEX.md` — contagens atualizadas (40 tools, 8 prompts, 3 webinars) e links para os 2 tutoriais novos
- `Lab-Nexus/README.md` — contagem de assets ajustada (50 → 54) e menção aos novos arquivos

---

## [1.0.0] — 2026-06-02 · "Lançamento oficial do HUB"

### 🎉 Release inicial

- 🎓 **3 camadas estruturadas**:
  - **Cursos** — 4 trilhas (Fundamental, Agente, Master, Elite) com 15 cursos curados
  - **Lab-Nexus** — 38 ferramentas categorizadas + 6 prompts + 3 templates HTML + 3 workflows JSON
  - **Lib-Nexus** — 15 documentos canônicos (glossário, IOAID, specs de agentes, API docs, best practices)

- 📕 **Pastas auxiliares**:
  - `treinamentos/` — 3 workshops práticos
  - `webinars/` — 2 webinars realizados + calendário 2026
  - `certificacoes/` — 3 certificações progressivas (CON, CEN, CEN+) + modelo de avaliação
  - `playbooks/` — 7 playbooks de operação (rotina, lançamento, crise, LGPD)
  - `tutoriais/` — 12 tutoriais how-to rápidos

- 🔄 **Sistema de sync entre Academ'IA e Runtime**:
  - `sync/agent-bridge.json` — mapeamento trilhas → skills → SHO (4 níveis)
  - `sync/skill-manifest.json` — catálogo de 14 skills com linkage à trilha
  - `sync/MCP-CONFIG.md` — 4 servidores MCP configurados

- 🛡️ **Governança**:
  - LGPD-safe em todos os exemplos
  - Code-first (exemplos > prosa)
  - Cross-linked com tags transversais
  - Obsidian-ready (frontmatter YAML)

- 📐 **Padrão de qualidade** (Lab-Quality-Standard) para tools, prompts, templates, workflows

---

## 🎯 Próximas versões (roadmap público)

### [1.2.0] — Previsto Q3-2026

- 🎬 Adicionar 2 workshops novos: `WS-04` Operação SHO Avançado, `WS-05` Federação de Agentes (hands-on)
- 🧪 Adicionar 4 ferramentas operacionais no Lab:
  - `tools/analytics/07-comparador-creators.md`
  - `tools/automation/08-rate-limiter-pausa-inteligente.md`
  - `tools/design/06-prompt-visual-carrossel-v2.md`
  - `tools/marketing/10-icp-detector.md`
- 📊 Adicionar 3 templates: `templates/social/02-template-stories-sequencia.html`, `templates/landing/03-template-otimizado-conversao.html`, `templates/email/04-template-carrinho-abandonado.html`
- 🔄 Adicionar `sync/audit-log-schema.md` — schema do log de auditoria MCP

### [2.0.0] — Previsto Q4-2026

- 💎 Migração do conteúdo Elite para formato interativo (com simuladores embedded)
- 🌐 i18n: versão em inglês (EN-US) das 4 trilhas de curso
- 🧠 Skill auto-tuning integrado ao Academ'IA (prompts do Lab-Nexus alimentam o Judge)
- 📦 Empacotamento do Academ'IA como MCP server oficial instalável via `npx`

---

## [1.2.0] — 2026-06-28 · "Análise Técnica + Materiais Pendentes"

### 🆕 Novos Materiais

- **`ANALISE_TECNICA_E_ROADMAP.md`**: auditoria completa + roadmap de 90 dias (4 sprints)
- **`FAQ.md`**: 30 perguntas frequentes sobre AcademIA, cursos, certificações e operação
- **`certificacoes/banco-questoes-con.md`**: 50 questões oficiais da certificação CON com gabarito comentado

### 🎯 Gaps Identificados (próximas sprints)

- **GAP-01** Banco de questões CEN e CEN+ (atual só CON)
- **GAP-02** Tutoriais #15-30 (atual só vai até #14)
- **GAP-03** Cursos de RAG, Deploy, Segurança (atual só cobre 2015-level)
- **GAP-04** Materiais em vídeo (atual 100% texto)
- **GAP-05** Landing page pública (atualmente só HTML não-indexado)
- **GAP-07** Trilha paralela Comercial vs Técnica

### 📋 Próximas Entregas (Sprint 1 - 3 semanas)

- 6 tutoriais novos: RAG, Whisper, OpenAI API, fine-tuning, deploy, prompt CTR
- 3 cursos novos: RAG em Produção, Deploy em Produção, Segurança/Jailbreaks
- 3 bancos de questões: CON, CEN, CEN+

### 📊 Métricas de Crescimento Atualizadas

| Versão | Data | Cursos | Tools | Prompts | Templates | Workflows | Tutoriais | Playbooks | Apostilas |
|---|---|---|---|---|---|---|---|---|---|
| 1.0.0 | 2026-06-02 | 15 | 38 | 6 | 3 | 3 | 12 | 7 | 0 |
| 1.1.0 | 2026-06-02 | 15 | 40 | 8 | 3 | 3 | 14 | 7 | 0 |
| 1.2.0 | **2026-06-28** | 15 | 40+ | 8 | 3 | 3 | 14 | 7 | 10 |

**Total estimado de arquivos**: 100+ .md · 15.000+ linhas
**Próximo milestone**: v1.3 (Sprint 1) → 18+ cursos, 20+ tutoriais, 3 bancos de questões

---

| Versão | Data | Cursos | Tools | Prompts | Templates | Workflows | Tutoriais | Playbooks |
|---|---|---|---|---|---|---|---|---|
| 1.0.0 | 2026-06-02 | 15 | 38 | 6 | 3 | 3 | 12 | 7 |
| **1.1.0** | **2026-06-02** | **15** | **40** | **8** | **3** | **3** | **14** | **7** |
| 1.2.0 (meta) | Q3-2026 | 15 | 44 | 8 | 6 | 4 | 16 | 8 |
| 2.0.0 (meta) | Q4-2026 | 15 + EN | 50+ | 12+ | 8+ | 6+ | 20+ | 10+ |

---

## 🤝 Como Contribuir

1. Abra PR descrevendo a mudança
2. Revisão por 1 mantenedor da área
3. (Para Lib-Nexus) Revisão por 2 contribuidores Elite
4. Merge + bump de versão automático

Toda contribuição precisa seguir o **Lab-Quality-Standard** (spec + playbook + asset + métricas + riscos).

---

**Mantido por:** Equipe Nexus Affil'IA'te
**Contato:** equipenexus@oneverso.com.br
**Repositório:** https://github.com/Nexus-HUB57/MMN_AI-to-AI
