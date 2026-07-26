---
title: "📖 Lib Nexus · Índice Navegável de Referências Canônicas"
description: "Índice navegável das referências canônicas do Lib Nexus (knowledge-base + agents-specs + api-docs + best-practices) com filtros por domínio, audiência e tipo de artefato"
date: 2026-07-26
gerado_por: "Mavis Agent"
version: "1.0.0"
tags: [lib-nexus, indice, navegavel, knowledge-base, agents-specs, api-docs, best-practices, canon]
pattern: "MMN_IA"
last_updated: "2026-07-26"
---

# 📖 Lib Nexus · Índice Navegável de Referências Canônicas

> **Índice navegável** das 26 referências canônicas do Lib Nexus. Complementa o [`README.md`](README.md) (visão editorial + governança) com **filtros práticos** para encontrar o documento de referência certo em <30s.

## 🎯 O que é este índice

O `Lib-Nexus/README.md` documenta a **filosofia, estrutura e governança** da Lib. Este `INDEX.md` é **complementar** e foca em **encontrar a referência canônica certa** rapidamente.

> ⚠️ **REGRA CANÔNICA**: Lib Nexus é **read-mostly** — escrita só via PR + aprovação de contribuidor Elite. Este índice é apenas navegação; **não** modifica a governança.

## 📊 Visão Geral — 26 Referências Canônicas

| Pasta | Documentos | Status |
|---|---:|---|
| 📚 `knowledge-base/` | 9 | 🟢 canônico |
| 🤖 `agents-specs/` | 7 | 🟢 canônico |
| 🔌 `api-docs/` | 5 | 🟢 canônico |
| ⭐ `best-practices/` | 6 | 🟢 canônico |
| **TOTAL** | **27** | 🟢 **100%** |

---

## 📚 `knowledge-base/` (9) — Conceitos, Glossários, Modelos

| Code | Asset | Domínio | Audiência |
|---|---|---|---|
| 00 | `00-glossario.md` | Vocabulário canônico | Todos |
| 01 | `01-modelo-ioaid.md` | Arquitetura IOAID (5 camadas) | Devs + power users |
| 02 | `02-taxonomia-skills.md` | Catálogo de 45 skills | Devs |
| 03 | `03-conformidade-lgpd.md` | LGPD compliance | Devs + jurídico |
| 04 | `04-conformidade-anatel.md` | ANatel compliance | Devs + jurídico |
| 05 | `05-modelo-federation.md` | Federação de agentes | Devs |
| 06 | `06-padroes-seguranca.md` | Padrões de segurança | Devs + SRE |
| 07 | `07-modelo-sho.md` | Self-Healing Orchestrator | Devs |
| 08 | `08-kpis-oficiais-nexus.md` | KPIs oficiais do ecossistema | Estrategistas + devs |

### Quando consultar `knowledge-base/`?

- "O que significa X?" → `00-glossario.md`
- "Como funciona o modelo Y?" → Documentos `01-08`
- "Estou implementando Z, qual a referência canônica?" → Procurar por domínio

---

## 🤖 `agents-specs/` (7) — Contratos de Agentes

| Code | Asset | Agente | Tipo |
|---|---|---|---|
| 00 | `00-base-agent.md` | `baseAgent` | Foundation |
| 01 | `01-marketing-agent.md` | `marketingAgent` | Marketing |
| 02 | `02-judge-revisor.md` | `judgeRevisor` | Governança |
| 03 | `03-federation-gate.md` | `federationGate` | PII Gate |
| 04 | `04-copy-persuasivo-agent.md` | `copyPersuasivoAgent` | Copywriting |
| 05 | `05-analytics-cohort-agent.md` | `analyticsCohortAgent` | Analytics |
| 06 | `06-sho-operator-agent.md` | `shoOperatorAgent` | Orquestração |

### Quando consultar `agents-specs/`?

- "Quais inputs/outputs do agente X?" → `XX-nome-agent.md`
- "Quais erros o agente pode retornar?" → Seção "Errors" do spec
- "Como integrar com o agente Y?" → Seção "Integration" do spec

---

## 🔌 `api-docs/` (5) — APIs Internas e Externas

| Code | Asset | API | Protocolo |
|---|---|---|---|
| 00 | `00-trpc-overview.md` | tRPC (AcademIA) | tRPC |
| 01 | `01-webhooks.md` | Webhooks (Hotmart, Shopee, Stripe) | Webhook |
| 02 | `02-rest-public.md` | REST público | REST |
| 03 | `03-graphql-schema.md` | GraphQL schema | GraphQL |
| 04 | `04-sdk-python-typescript.md` | SDK Python + TypeScript | SDK |

### Quando consultar `api-docs/`?

- "Como autenticar na API X?" → `XX-nome-api.md` (seção Auth)
- "Quais endpoints estão disponíveis?" → `00-trpc-overview.md` ou `02-rest-public.md`
- "Como receber webhooks do Hotmart?" → `01-webhooks.md`

---

## ⭐ `best-practices/` (6) — Padrões Recomendados

| Code | Asset | Domínio | Audiência |
|---|---|---|---|
| 00 | `00-prompt-engineering.md` | Prompt engineering | Todos os agentes |
| 01 | `01-error-handling.md` | Tratamento de erros | Devs |
| 02 | `02-performance.md` | Performance e otimização | Devs + SRE |
| 03 | `03-seguranca-confianca.md` | Segurança e confiança | Devs + SRE + jurídico |
| 04 | `04-seguranca-agentes.md` | Segurança específica de agentes | Devs de agentes |
| 05 | `05-sre-observability.md` | SRE e observabilidade | SRE + Devs |

### Quando consultar `best-practices/`?

- "Como devo tratar erros X?" → `01-error-handling.md`
- "Como otimizar performance de Y?" → `02-performance.md`
- "Como garantir segurança de Z?" → `03-seguranca-confianca.md` ou `04-seguranca-agentes.md`

---

## 🔀 Filtros Rápidos por Persona

### 👨‍💻 "Sou dev implementando um agente"

1. `agents-specs/00-base-agent.md` (foundation obrigatória)
2. `agents-specs/XX-seu-agente.md` (spec específica)
3. `best-practices/00-prompt-engineering.md`
4. `best-practices/01-error-handling.md`
5. `knowledge-base/02-taxonomia-skills.md`

### 🎯 "Sou dev integrando com APIs"

1. `api-docs/00-trpc-overview.md` (entry point)
2. `api-docs/02-rest-public.md` (se preferir REST)
3. `api-docs/01-webhooks.md` (se recebe webhooks)
4. `best-practices/02-performance.md`

### 🔒 "Preciso garantir compliance/segurança"

1. `knowledge-base/03-conformidade-lgpd.md`
2. `knowledge-base/04-conformidade-anatel.md`
3. `knowledge-base/06-padroes-seguranca.md`
4. `best-practices/03-seguranca-confianca.md`
5. `best-practices/04-seguranca-agentes.md`

### 📊 "Sou Estrategista e quero entender o modelo de negócio"

1. `knowledge-base/00-glossario.md` (vocabulário)
2. `knowledge-base/01-modelo-ioaid.md` (arquitetura)
3. `knowledge-base/08-kpis-oficiais-nexus.md` (KPIs oficiais)
4. `knowledge-base/05-modelo-federation.md` (federação de agentes)

### 🛠️ "Sou SRE/Observability"

1. `best-practices/05-sre-observability.md`
2. `best-practices/02-performance.md`
3. `knowledge-base/07-modelo-sho.md` (Self-Healing)

---

## 🔗 Links Cruzados

- **Manifest canônico do repo:** [`../INDEX.md`](../INDEX.md)
- **Source of truth de vozes:** [`../marca/personas/voice_registry/`](../marca/personas/voice_registry/)
- **Skills correspondentes:** [`../sync/skill-manifest.json`](../sync/skill-manifest.json)
- **CHANGELOG:** [`../CHANGELOG.md`](../CHANGELOG.md)
- **Multi-dev guide:** [`../GUIA_MULTI_DEV.md`](../GUIA_MULTI_DEV.md)

---

## ⚖️ Compliance & Governança

- ✅ **Read-mostly:** este índice não altera a governança
- ✅ **Sem sobrescrita:** adição pura de `INDEX.md` (não toca em `README.md` ou specs)
- ✅ **LGPD-safe:** nenhum dado pessoal neste índice
- ✅ **Code-first:** apenas navegação + referências
- ✅ **Versionado:** controlado por CHANGELOG

---

**Gerado por:** Mavis Agent · **Data:** 2026-07-26 · **Versão:** 1.0.0
**Compliance:** [GUIA_MULTI_DEV.md](../GUIA_MULTI_DEV.md) · Nenhuma sobrescrita, adição pura.
