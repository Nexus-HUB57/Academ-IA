---
title: "Módulo Elite-01 · Slides · Multi-tenant e White-label"
description: "Slides visuais para acompanhar o módulo 01 da Trilha Elite"
tags: [slides, elite, modulo-01]
modulo: elite-01
trilha: Elite
ordem: 1
total_slides: 9
pattern: "MMN_IA"
---

# 📊 Slides · Elite 01 · Multi-tenant e White-label

> Material visual de apoio para acompanhar o vídeo e a leitura do módulo.

## 🎨 Paleta de Cores

```
Primary:    #facc15
Secondary:  #b78cff
Accent:     #ff7eb6
Background: #0a0e1a
```

---

## 📍 SLIDE 01 — Abertura

**Título:** Multi-tenant e White-label
**Subtítulo:** Trilha Elite · Módulo 01
**Persona-guia:** Sra. Nexus Ive e Sir. Nexus Alencar

---

## 📍 SLIDE 02 — Objetivo do módulo

**Título:** O que você vai dominar neste módulo
- Multi-tenant = uma única instância do Nexus serve múltiplos clientes (tenants), cada um com dados isolados.
- White-label = o tenant pode customizar marca, domínio e cores.
- Instance Management (CRUD, API key, rate limit)
- Branding Engine (logos, cores, fontes, domínio)

---

## 📍 SLIDE 03 — Conceito

**Título:** Conceito
- Multi-tenant = uma única instância do Nexus serve múltiplos clientes (tenants), cada um com dados isolados.
- White-label = o tenant pode customizar marca, domínio e cores.
- Instance Management (CRUD, API key, rate limit)
- Branding Engine (logos, cores, fontes, domínio)

---

## 📍 SLIDE 04 — Isolamento: 3 estratégias

**Título:** Isolamento: 3 estratégias
- Nexus default: row-level-security com RLS ativo em todas as tabelas (backend/src/db/rls/).

---

## 📍 SLIDE 05 — Como configurar (passo a passo)

**Título:** Como configurar (passo a passo)
- ### 1.
- Criar a instância ### 2.
- Configurar DNS ### 3.
- Provisionar SSL (automático via Caddy/Traefik) ### 4.

---

## 📍 SLIDE 06 — API key e rate limit

**Título:** API key e rate limit
- X-API-Key: chave de 32 chars para integrações
- X-Tenant-ID: header obrigatório em todas as requests
- Rate limit padrão: 1000 req/min (plano Pro), 10000 (Enterprise)
- Cada tenant recebe:

---

## 📍 SLIDE 07 — Billing por tenant

**Título:** Billing por tenant
- Cobrança via Stripe Connect (split entre Nexus e o tenant)
- Planos: Starter / Pro / Enterprise
- Métricas de billing: contatos armazenados, mensagens enviadas, skills ativas

---

## 📍 SLIDE 08 — Exercício

**Título:** Exercício
- Crie 1 instância de teste no painel
- Configure branding (cor + logo)
- Suba 1 subdomínio (use *.localhost se não tiver DNS)
- Crie 1 afiliado dentro do tenant

---

## 📍 SLIDE 09 — Checklist e próximos passos

**Título:** O que precisa sair pronto daqui
- Revisar os conceitos centrais apresentados neste módulo
- Transformar os exemplos em configuração real no ecossistema Nexus
- Pré-requisito relacionado: ["elite/00-blueprints-elite"]
- Seguir para o próximo módulo com base documentada e operacional

