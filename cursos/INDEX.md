---
title: "Cursos · Panorama das 4 Trilhas"
description: "Índice panorâmico das 4 trilhas de cursos da Academ'IA — Fundamental, Agente, Master, Elite"
tags: [cursos, indice, trilhas, fundamental, agente, master, elite, panorama]
version: 1.0.0
last_updated: 2026-07-24
pattern: "MMN_IA"
---

# 🎓 Cursos · Panorama das 4 Trilhas

> **Índice panorâmico** das 4 trilhas de cursos estruturados da Academ'IA. Para detalhes por curso, consulte o README da trilha correspondente. Este documento dá **visão de pássaro** e orientação de progressão de carreira.

## 🎯 Filosofia dos Cursos

Cada curso tem **3 artefatos canônicos** (3-camada):

| Artefato | Função | Quem usa |
|----------|--------|----------|
| `XX-nome.md` | Descrição completa, objetivos, pré-requisitos, plano | Aluno (estudar) |
| `XX-nome-slides.md` | Apresentação (PPT-equivalente em MD) | Professor / Aluno (visualizar) |
| `XX-nome-roteiro.md` | Roteiro do vídeo-aula (script detalhado) | Produção / Aluno (assistir) |

> **Versões estendidas** usam sufixo `-mavis-detalhado` (mais cenas, mais profundidade). Convive com versão canônica sem sobrescrita.

## 📊 Visão Geral das 4 Trilhas

| Trilha | Carga | Cursos | Dificuldade | Perfil |
|--------|-------|--------|-------------|--------|
| 🥉 **Fundamental** | ~6h | 6 (00-02) | ⭐ | Quem está começando |
| 🥈 **Agente** | ~8h | 4 (00-03) | ⭐⭐ | Operador de agentes |
| 🥇 **Master** | ~16h | 7 (00-06) | ⭐⭐⭐ | Estrategista |
| 💎 **Elite** | ~6h | 3 (00-02) | ⭐⭐⭐⭐ | Top 5% da rede |
| **TOTAL** | **~36h** | **20 cursos** | — | — |

## 🥉 Trilha Fundamental (6 cursos)

Para **quem está começando do zero** — configuração inicial, primeiros conceitos, primeira persona.

| # | Curso | Versão canônica | Versões alternativas |
|---|-------|-----------------|----------------------|
| 00 | Boas-vindas | [00-boas-vindas.md](fundamental/00-boas-vindas.md) | slides · roteiro |
| 01 | Introdução Sra. Nexus Ive | [01-introducao-sra-nexus-ive.md](fundamental/01-introducao-sra-nexus-ive.md) | slides · roteiro |
| 01 | Entendendo IOAID | [01-entendendo-ioaid.md](fundamental/01-entendendo-ioaid.md) | slides · roteiro |
| 02 | Sistema SHO | [02-sistema-sho.md](fundamental/02-sistema-sho.md) | slides · roteiro |
| 02 | LGPD para afiliados | [02-lgpd-afiliados.md](fundamental/02-lgpd-afiliados.md) | slides · roteiro |
| 02 | Multi-tenant básico | [02-multi-tenant-basico.md](fundamental/02-multi-tenant-basico.md) | slides · roteiro |

### Estrutura detalhada

```
cursos/fundamental/
├── 00-boas-vindas.md + slides + roteiro (+ 7 arquivos .wav de cenas)
├── 01-introducao-sra-nexus-ive.md + slides + roteiro
├── 01-entendendo-ioaid.md + slides + roteiro
├── 02-sistema-sho.md + slides + roteiro
├── 02-lgpd-afiliados.md + slides + roteiro
├── 02-multi-tenant-basico.md + slides + roteiro
└── aula01/, aula02/   (subpastas de exercícios)
```

## 🥈 Trilha Agente (4 cursos)

Para **operadores de agentes** — primeiro agente, skills, disparos, judge.

| # | Curso | Versão canônica | Versões alternativas |
|---|-------|-----------------|----------------------|
| 00 | Primeiro Agente | [00-primeiro-agente.md](agente/00-primeiro-agente.md) | slides · roteiro |
| 01 | Skills Essenciais | [01-skills-essenciais.md](agente/01-skills-essenciais.md) | slides · roteiro |
| 02 | Disparo WhatsApp | [02-disparo-whatsapp.md](agente/02-disparo-whatsapp.md) | slides · roteiro |
| 03 | Judge Revisor | [03-judge-revisor.md](agente/03-judge-revisor.md) | slides · roteiro |

### Estrutura detalhada

```
cursos/agente/
├── 00-primeiro-agente.md + slides + roteiro
├── 01-skills-essenciais.md + slides + roteiro
├── 02-disparo-whatsapp.md + slides + roteiro
└── 03-judge-revisor.md + slides + roteiro
```

## 🥇 Trilha Master (7 cursos)

Para **estrategistas** — funis, A/B testing, coortes, RAG, deploy, segurança.

| # | Curso | Versão canônica | Versões alternativas |
|---|-------|-----------------|----------------------|
| 00 | Otimização de Conversão | [00-otimizacao-conversao.md](master/00-otimizacao-conversao.md) | slides · roteiro |
| 01 | Funis & Lifecycle | [01-funis-lifecycle.md](master/01-funis-lifecycle.md) | slides · roteiro |
| 02 | A/B Test com Judge | [02-ab-test-judge.md](master/02-ab-test-judge.md) | slides · roteiro |
| 03 | Coortes & Churn | [03-coortes-churn.md](master/03-coortes-churn.md) | slides · roteiro |
| 04 | RAG em Produção ⭐ | [04-rag-em-producao.md](master/04-rag-em-producao.md) | slides · roteiro · `-mavis-detalhado` |
| 05 | Deploy em Produção ⭐ | [05-deploy-em-producao.md](master/05-deploy-em-producao.md) | slides · roteiro · `-mavis-detalhado` |
| 06 | Segurança & Jailbreaks & LGPD ⭐ | [06-seguranca-jailbreaks-lgpd.md](master/06-seguranca-jailbreaks-lgpd.md) | slides · roteiro · `-mavis-detalhado` |

> ⭐ = cursos com **versão estendida Mavis** (mais cenas, mais profundidade)

### Estrutura detalhada

```
cursos/master/
├── 00-otimizacao-conversao.md + slides + roteiro
├── 01-funis-lifecycle.md + slides + roteiro
├── 02-ab-test-judge.md + slides + roteiro
├── 03-coortes-churn.md + slides + roteiro
├── 04-rag-em-producao.md + slides + roteiro + 04-rag-em-producao-*-mavis-detalhado.md
├── 05-deploy-em-producao.md + slides + roteiro + 05-deploy-em-producao-*-mavis-detalhado.md
├── 06-seguranca-jailbreaks-lgpd.md + slides + roteiro + 06-seguranca-jailbreaks-lgpd-*-mavis-detalhado.md
└── README.md  (panorama da trilha)
```

## 💎 Trilha Elite (3 cursos)

Para **top 5% da rede** — blueprints elite, multi-tenant white-label, federação.

| # | Curso | Versão canônica | Versões alternativas |
|---|-------|-----------------|----------------------|
| 00 | Blueprints Elite | [00-blueprints-elite.md](elite/00-blueprints-elite.md) | slides · roteiro |
| 01 | Multi-Tenant White-Label | [01-multi-tenant-whitelabel.md](elite/01-multi-tenant-whitelabel.md) | slides · roteiro |
| 02 | Federação de Agentes | [02-federacao-agentes.md](elite/02-federacao-agentes.md) | slides · roteiro |

### Estrutura detalhada

```
cursos/elite/
├── 00-blueprints-elite.md + slides + roteiro
├── 01-multi-tenant-whitelabel.md + slides + roteiro
└── 02-federacao-agentes.md + slides + roteiro
```

## 🗺️ Trilha de Progressão Recomendada

```
   🥉 Fundamental
        │ (1-2 meses)
        ↓
   🥈 Agente
        │ (2-3 meses, primeiro agente em produção)
        ↓
   🥇 Master
        │ (3-4 meses, otimização contínua)
        ↓
   💎 Elite
        │ (1-2 meses, top 5% da rede)
        ↓
   🏆 Certificação Nexus (CON → CEN → CEN+ → MAS+ → CNX)
```

## 🎯 Por Caso de Uso / Necessidade

### "Quero aprender a operar a plataforma"
→ Trilha **Fundamental** (00-02)

### "Quero criar e manter agentes em produção"
→ Trilha **Agente** (00-03)

### "Quero otimizar conversão e fazer estratégia"
→ Trilha **Master** (00-03)

### "Quero construir features avançadas (RAG, deploy, segurança)"
→ Trilha **Master** (04-06)

### "Quero ser top 5% e ganhar mais"
→ Trilha **Elite** completa

### "Quero virar um arquiteto de plataforma white-label"
→ Trilha **Elite** 01-02

### "Quero entender a visão macro do ecossistema"
→ Cursos 00 de cada trilha (00-boas-vindas, 00-primeiro-agente, 00-otimizacao-conversao, 00-blueprints-elite)

## 🎓 Certificação

Cada trilha prepara para um nível de certificação:
- **Fundamental** → base para **CON** (Operador Nexus)
- **Agente** → base para **CEN** (Estrategista Nexus)
- **Master** → base para **CEN+** (Elite Nexus) e **MAS+** (Master Plus)
- **Elite** → base para **CNX** (Nexus Master)

Veja [`../certificacoes/`](../certificacoes/) para simulados e detalhes.

## 📂 Estrutura

```
cursos/
├── INDEX.md                       ← este arquivo
├── fundamental/                   (6 cursos + subpastas)
│   ├── 00-boas-vindas*
│   ├── 01-*
│   └── 02-*
├── agente/                        (4 cursos)
├── master/                        (7 cursos + README)
└── elite/                         (3 cursos)
```

## 🔗 Links Cruzados

- [`../apostilas/`](../apostilas/) — Material escrito complementar (37 apostilas)
- [`../treinamentos/`](../treinamentos/) — Workshops práticos (9 treinamentos)
- [`../tutoriais/`](../tutoriais/) — How-to rápidos (36 tutoriais)
- [`../webinars/`](../webinars/) — Webinars ao vivo/sob demanda
- [`../certificacoes/`](../certificacoes/) — Simulados e estrutura de certificação
- [`../Lib-Nexus/`](../Lib-Nexus/) — Biblioteca de referência técnica
- [`../Lab-Nexus/`](../Lab-Nexus/) — Ferramentas práticas

## 👥 Ownership

- **Owner:** Head de Curadoria Pedagógica
- **Mantenedor:** Equipe Multi-Dev (Mavis, genspark_dev, etc.)
- **Cadência de revisão:** Mensal

---

*Nexus Affil'IA'te · cursos/INDEX.md · v1.0.0 · Julho 2026*
