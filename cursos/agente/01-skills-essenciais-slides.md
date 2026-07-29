---
title: "Módulo Agente-01 · Slides · Skills essenciais: copywriter + audience-segmenter"
description: "Slides visuais para acompanhar o módulo 01 da Trilha Agente"
tags: [slides, agente, modulo-01]
modulo: agent-01
trilha: Agente
ordem: 1
total_slides: 8
pattern: "MMN_IA"
---

# 📊 Slides · Agente 01 · Skills essenciais: copywriter + audience-segmenter

> Material visual de apoio para acompanhar o vídeo e a leitura do módulo.

## 🎨 Paleta de Cores

```
Primary:    #63eaff
Secondary:  #b78cff
Accent:     #ff7eb6
Background: #0a0e1a
```

---

## 📍 SLIDE 01 — Abertura

**Título:** Skills essenciais: copywriter + audience-segmenter
**Subtítulo:** Trilha Agente · Módulo 01
**Persona-guia:** Sra. Nexus Ive e Sir. Nexus Alencar

---

## 📍 SLIDE 02 — Objetivo do módulo

**Título:** O que você vai dominar neste módulo
- Hoje o sistema tem 27 skills operacionais + 18 planejadas (roadmap) = 45 totais.
- Uma Skill é uma capacidade atômica do agente.
- Cada skill é um arquivo TypeScript em backend/src/agentic/skills/ que implementa o contrato SkillHandler:

---

## 📍 SLIDE 03 — O que é uma Skill?

**Título:** O que é uma Skill?
- Hoje o sistema tem 27 skills operacionais + 18 planejadas (roadmap) = 45 totais.
- Uma Skill é uma capacidade atômica do agente.
- Cada skill é um arquivo TypeScript em backend/src/agentic/skills/ que implementa o contrato SkillHandler:

---

## 📍 SLIDE 04 — As 2 skills que você vai usar TODO dia

**Título:** As 2 skills que você vai usar TODO dia
- 📂 Onde usar: Lab-Nexus/tools/copy/ tem 12 templates prontos.
- ### ✍️ copywriter-persuasivo O que faz: gera copy pronto para publicação (headline, sub, 3 hooks A/B, CTA + flags de risco).
- Input mínimo: Output típico: ### 🎯 audience-segmenter O que faz: divide uma lista de contatos em segmentos acionáveis (ex: lead frio, lead quente, cliente ativo, inativo 30d+).
- Input: Output:

---

## 📍 SLIDE 05 — Padrão recomendado (use sempre)

**Título:** Padrão recomendado (use sempre)
- Segmentar primeiro — nunca disparar para a lista cheia.
- Escolher o segmento mais quente — começa por quem tem maior propensão.
- Gerar copy com 3 hooks A/B — o Judge vai ranquear.
- Disparar e medir — 24h depois, ver CTR por hook.

---

## 📍 SLIDE 06 — Exercício

**Título:** Exercício
- Pegue sua lista de 1.000 contatos
- Rode audience-segmenter com critério engagement_score
- Identifique o top 20% (segmento quente)
- Rode copywriter-persuasivo com 3 hooks diferentes para esse segmento

---

## 📍 SLIDE 07 — Próximo passo

**Título:** Próximo passo
- 👉 02 · Disparando no WhatsApp --- Versão 1.0 · Atualizado 2026-06-02 · Fonte: backend/src/agentic/skills/copywriterPersuasivo.ts + audienceSegmenter.ts

---

## 📍 SLIDE 08 — Checklist e próximos passos

**Título:** O que precisa sair pronto daqui
- Revisar os conceitos centrais apresentados neste módulo
- Transformar os exemplos em configuração real no ecossistema Nexus
- Pré-requisito relacionado: ["agente/00-primeiro-agente"]
- Seguir para o próximo módulo com base documentada e operacional

