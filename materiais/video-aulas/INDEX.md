---
title: "Materiais · Vídeo-Aulas — Índice Navegável"
description: "Índice das 15 vídeo-aulas canônicas (4 fundamental + 4 agente + 4 master + 3 elite) com metadados, persona e status de produção"
tags: [materiais, video-aulas, indice, trilhas, canon, navegacao]
version: 1.0.0
last_updated: 2026-07-25
pattern: "MMN_IA"
---

# 🎬 Materiais · Vídeo-Aulas — Índice Navegável

> **Índice navegável** das 15 vídeo-aulas canônicas. Cada vídeo-aula é um **workspace autocontido** com `manifest.json` declarativo, slides, roteiros, áudios, capas, vídeo final e artefatos de publicação. Para o manifesto canônico completo, ver [`../../docs/MANIFESTO_REBUILD_VIDEO_AULAS_00_14_2026-07-24.md`](../../docs/MANIFESTO_REBUILD_VIDEO_AULAS_00_14_2026-07-24.md).

## 🎯 O que é esta pasta

`materiais/video-aulas/` é o **workspace canônico de produção** de vídeo-aulas. Diferente de `cursos/` (que tem a estrutura pedagógica), esta pasta tem o **produto final** de cada vídeo — slides finais, roteiro canônico, áudio narrado, capa aprovada, vídeo renderizado, e metadados de publicação.

Cada vídeo-aula mora em sua própria pasta com estrutura fixa:

```
materiais/video-aulas/{trilha}/{NN-nome}/
├── manifest.json           ← declaração canônica
├── slides/                 ← slides finais aprovados
├── roteiros/               ← roteiros canônicos (legado + canônico)
├── audios/                 ← áudios narrados (legado + PT-BR)
├── capas/                  ← capa principal + thumbnail
├── videos/                 ← vídeo final renderizado
├── curso/                  ← HTML + PDF de material de apoio
└── publicacao/             ← thumbnail YouTube + descrição TXT
```

## 📊 Visão Geral

| Trilha | Vídeos | Codes | Duração total | Status |
|--------|--------|-------|---------------|--------|
| 🥉 **Fundamental** | 4 | 00-03 | ~6 min | 🟢 pronto_para_rebuild |
| 🥈 **Agente** | 4 | 04-07 | ~7 min | 🟢 pronto_para_rebuild |
| 🥇 **Master** | 4 | 08-11 | ~10 min | 🟢 pronto_para_rebuild |
| 💎 **Elite** | 3 | 12-14 | ~8 min | 🟢 pronto_para_rebuild |
| **TOTAL** | **15** | **00-14** | **~31 min** | 🟢 **100%** |

## 🥉 Trilha Fundamental (4 vídeos)

> Conceitos-base da Academ'IA. Para quem está começando.

| Code | Título | Persona | Duração | Status |
|------|--------|---------|---------|--------|
| [00](fundamental/00-boas-vindas/) | Boas-vindas à AcademIA Nexus | 👨 Alencar | 75s | 🟢 |
| [01](fundamental/01-entendendo-ioaid/) | Entendendo o IOAID | 👩 Ive | 90s | 🟢 |
| [02](fundamental/02-sistema-sho/) | O Sistema SHO (Self-Healing Orchestrator) | 👨 Alencar | 95s | 🟢 |
| [03](fundamental/03-painel-afiliado/) | Painel do Afiliado — Visão Geral da Operação | 👥 Dupla | 105s | 🟢 |

## 🥈 Trilha Agente (4 vídeos)

> Construção e operação de agentes. Hands-on.

| Code | Título | Persona | Duração | Status |
|------|--------|---------|---------|--------|
| [04](agente/00-primeiro-agente/) | Construindo Seu Primeiro Agente em 4 Minutos | 👨 Alencar | 90s | 🟢 |
| [05](agente/01-skills-essenciais/) | Skills Essenciais — Copywriter + Audience-Segmenter | 👨 Alencar | 95s | 🟢 |
| [06](agente/02-disparo-whatsapp/) | Disparando no WhatsApp em Escala | 👨 Alencar | 100s | 🟢 |
| [07](agente/03-judge-revisor/) | Judge Revisor — A IA que Decide por Você | 👨 Alencar | 105s | 🟢 |

## 🥇 Trilha Master (4 vídeos)

> Otimização avançada e estratégia.

| Code | Título | Persona | Duração | Status |
|------|--------|---------|---------|--------|
| [08](master/00-otimizacao-conversao/) | Otimização de Conversão — A Matemática da Receita | 👥 Dupla | 135s | 🟢 |
| [09](master/01-funis-lifecycle/) | Funis e Lifecycle — O Sistema Completo | 👥 Dupla | 145s | 🟢 |
| [10](master/02-ab-test-judge/) | A/B Testing com Judge — Ciência da Experimentação | 👥 Dupla | 145s | 🟢 |
| [11](master/03-coortes-churn/) | Análise de Coortes e Churn — A Arte de Reter | 👥 Dupla | 150s | 🟢 |

## 💎 Trilha Elite (3 vídeos)

> Tópicos avançados para top 5% da rede.

| Code | Título | Persona | Duração | Status |
|------|--------|---------|---------|--------|
| [12](elite/00-blueprints-elite/) | Blueprints Elite — O Jogo do Top 10% | 👥 Dupla | 155s | 🟢 |
| [13](elite/01-multi-tenant-whitelabel/) | Multi-Tenant e White-Label na Prática | 👨 Alencar | 160s | 🟢 |
| [14](elite/02-federacao-agentes/) | Federação de Agentes Zero-Trust | 👥 Dupla | 165s | 🟢 |

## 👥 Por Persona Apresentadora

### 👨 Sir Nexus Alencar (técnico, profundo) — 8 vídeos
- Fundamental 00, 02
- Agente 04, 05, 06, 07
- Elite 13

### 👩 Sra. Nexus Ive (matriarca, estratégica) — 1 vídeo
- Fundamental 01

### 👥 Dupla (Ive + Alencar) — 6 vídeos
- Fundamental 03
- Master 08, 09, 10, 11
- Elite 12, 14

## 🎯 Por Caso de Uso

### "Quero entender o que é a Academ'IA"
→ [00 Boas-vindas](fundamental/00-boas-vindas/) (75s)

### "Quero entender o modelo de operação (IOAID)"
→ [01 Entendendo o IOAID](fundamental/01-entendendo-ioaid/) (90s)

### "Quero entender o sistema de auto-cura (SHO)"
→ [02 O Sistema SHO](fundamental/02-sistema-sho/) (95s)

### "Quero ver o painel de afiliado"
→ [03 Painel do Afiliado](fundamental/03-painel-afiliado/) (105s)

### "Quero criar meu primeiro agente"
→ [04 Construindo Seu Primeiro Agente](agente/00-primeiro-agente/) (90s)

### "Quero entender skills essenciais"
→ [05 Skills Essenciais](agente/01-skills-essenciais/) (95s)

### "Quero disparar no WhatsApp em escala"
→ [06 Disparando no WhatsApp em Escala](agente/02-disparo-whatsapp/) (100s)

### "Quero entender o Judge Revisor"
→ [07 Judge Revisor](agente/03-judge-revisor/) (105s)

### "Quero otimizar conversão"
→ [08 Otimização de Conversão](master/00-otimizacao-conversao/) (135s)

### "Quero montar funis"
→ [09 Funis e Lifecycle](master/01-funis-lifecycle/) (145s)

### "Quero fazer A/B testing"
→ [10 A/B Testing com Judge](master/02-ab-test-judge/) (145s)

### "Quero analisar coortes e churn"
→ [11 Análise de Coortes e Churn](master/03-coortes-churn/) (150s)

### "Quero ser top 10%"
→ [12 Blueprints Elite](elite/00-blueprints-elite/) (155s)

### "Quero lançar multi-tenant white-label"
→ [13 Multi-Tenant e White-Label](elite/01-multi-tenant-whitelabel/) (160s)

### "Quero entender federação zero-trust"
→ [14 Federação de Agentes](elite/02-federacao-agentes/) (165s)

## 🔄 Status de Produção

Todos os 15 vídeos estão com status `pronto_para_rebuild` — significa que a estrutura canônica foi montada e estão prontos para entrar em produção (rebuild do vídeo final, narração PT-BR, publicação).

### Pipeline de Produção

1. **Manifest** declarado e validado.
2. **Slides** finais aprovados.
3. **Roteiro** canônico escrito.
4. **Áudio PT-BR** gerado via TTS.
5. **Capa + Thumb** aprovados pelo Head de Marca.
6. **Vídeo** renderizado (avatar + slides + áudio).
7. **Publicação** no YouTube (descrição + thumbnail).

> Para detalhes do pipeline: [`../../producao/PIPELINE_PRODUCAO.md`](../../producao/PIPELINE_PRODUCAO.md)

## 📂 Estrutura

```
materiais/video-aulas/
├── INDEX.md                       ← este arquivo
├── fundamental/                   (4 vídeo-aulas)
│   ├── 00-boas-vindas/
│   ├── 01-entendendo-ioaid/
│   ├── 02-sistema-sho/
│   └── 03-painel-afiliado/
├── agente/                        (4 vídeo-aulas)
│   ├── 00-primeiro-agente/
│   ├── 01-skills-essenciais/
│   ├── 02-disparo-whatsapp/
│   └── 03-judge-revisor/
├── master/                        (4 vídeo-aulas)
│   ├── 00-otimizacao-conversao/
│   ├── 01-funis-lifecycle/
│   ├── 02-ab-test-judge/
│   └── 03-coortes-churn/
└── elite/                         (3 vídeo-aulas)
    ├── 00-blueprints-elite/
    ├── 01-multi-tenant-whitelabel/
    └── 02-federacao-agentes/
```

## 🔗 Links Cruzados

- [`../../docs/MANIFESTO_REBUILD_VIDEO_AULAS_00_14_2026-07-24.md`](../../docs/MANIFESTO_REBUILD_VIDEO_AULAS_00_14_2026-07-24.md) — Manifesto canônico do rebuild
- [`../../cursos/INDEX.md`](../../cursos/INDEX.md) — Cursos (origem pedagógica)
- [`../../producao/roteiros/INDEX.md`](../../producao/roteiros/INDEX.md) — Roteiros canônicos
- [`../../marca/INDEX.md`](../../marca/INDEX.md) — Personas oficiais
- [`../../producao/PIPELINE_PRODUCAO.md`](../../producao/PIPELINE_PRODUCAO.md) — Pipeline
- [`../../GUIA_MULTI_DEV.md`](../../GUIA_MULTI_DEV.md) — Convenções multi-dev

## 👥 Ownership

- **Owner:** Head de Produção + Head de Marca
- **Mantenedor:** Equipe de produção multi-dev
- **Cadência de revisão:** Semanal (status) / Trimestral (qualidade)

---

*Nexus Affil'IA'te · materiais/video-aulas/INDEX.md · v1.0.0 · Julho 2026*
