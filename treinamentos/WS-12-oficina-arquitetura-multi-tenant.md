---
title: "WS-12 · Oficina de Arquitetura Multi-Tenant"
level: elite
duration: 180min
format: workshop
tags: [workshop, multi-tenant, whitelabel, saas, arquitetura, federacao]
last_updated: 2026-07-29
---

# 🎬 WS-12 · Oficina de Arquitetura Multi-Tenant

> **Formato:** Workshop gravado (vídeo + material) · **Duração:** 180 min · **Nível:** Elite

## 🎯 Objetivo

No fim deste workshop, você vai ser capaz de **arquitetar, implementar e operar** uma plataforma multi-tenant com white-label. Vai cobrir os 3 modelos de isolamento (silo, bridge, pool), decisões de banco, governança, e SLA 99.9%.

## 📚 Pré-requisitos

- [x] Nível Master completo
- [x] Curso `cursos/elite/01-multi-tenant-whitelabel.md` (ou vídeos 13)
- [x] Experiência com arquitetura SaaS
- [x] Conhecimento básico de Kubernetes

## 🗓️ Agenda

| Tempo | Bloco | O que você faz |
|---|---|---|
| 00:00–00:15 | **Abertura** | Multi-tenant: por que e quando |
| 00:15–00:45 | **3 modelos** | Silo, Bridge, Pool — comparação |
| 00:45–01:15 | **Decisão** | Como escolher (matriz de decisão) |
| 01:15–01:45 | **Banco** | Schema per-tenant vs DB per-tenant |
| 01:45–02:15 | **White-label** | DNS, certificados, tema, branding |
| 02:15–02:45 | **Governança** | Onboarding, billing, support, audit |
| 02:45–03:00 | **SLA 99.9%** | Estratégia + monitoramento |

## 🛠️ Stack

- PostgreSQL 15+ (com `pg_isolation_level`)
- Redis (cache + sessions)
- Kubernetes (orquestração)
- Terraform (IaC)
- Helm (deploy per-tenant)

## 📂 Arquivos

- `templates/tenant_router.py` — middleware FastAPI
- `templates/rls_policies.sql` — Row Level Security
- `templates/tenant_provisioner.py` — onboarding automatizado
- `templates/whitelabel_dns_setup.sh`
- `templates/sla_dashboard.json`

## 💡 Trade-offs Centrais

| Aspecto | Silo | Bridge | Pool |
|---|---|---|---|
| **Custo** | 3-5x | 2x | 1x |
| **Isolamento** | Total | Médio | Baixo |
| **Compliance** | Fácil (HIPAA, PCI) | Moderado | Complexo |
| **Onboarding** | Lento (minutos) | Médio (seg) | Rápido (ms) |
| **Scaling** | Independente | Parcial | Compartilhado |
| **Customização** | Total | Média | Baixa |

**Recomendação**: começar com **Bridge** (schema per-tenant, DB compartilhado). Escalar para **Silo** quando cliente enterprise exigir (>$5k/mês).

## 🎓 Entregáveis

- ✅ Matriz de decisão impressa
- ✅ Schema de banco multi-tenant com RLS
- ✅ Provisioner automatizado (onboarding < 5min)
- ✅ Whitelabel configurável (DNS + tema)
- ✅ Dashboard de SLA por tenant

---

**Versão 1.0** · 2026-07-29 · Mavis Agent
**Mantido em**: `treinamentos/WS-12-oficina-arquitetura-multi-tenant.md`
