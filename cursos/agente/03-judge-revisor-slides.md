---
title: "Módulo Agente-03 · Slides · Lendo o Judge Revisor"
description: "Slides visuais para acompanhar o módulo 03 da Trilha Agente"
tags: [slides, agente, modulo-03]
modulo: agent-03
trilha: Agente
ordem: 3
total_slides: 9
pattern: "MMN_IA"
---

# 📊 Slides · Agente 03 · Lendo o Judge Revisor

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

**Título:** Lendo o Judge Revisor
**Subtítulo:** Trilha Agente · Módulo 03
**Persona-guia:** Sra. Nexus Ive e Sir. Nexus Alencar

---

## 📍 SLIDE 02 — Objetivo do módulo

**Título:** O que você vai dominar neste módulo
- Arquivo: backend/src/agentic/skills/judgeRevisor.ts + judge/judgeRevisor.ts
- O Judge Revisor é um LLM secundário que avalia a saída do LLM primário antes de qualquer ação ser tomada.
- É a implementação prática de LLM-as-a-Judge no Nexus.

---

## 📍 SLIDE 03 — O que é o Judge?

**Título:** O que é o Judge?
- Arquivo: backend/src/agentic/skills/judgeRevisor.ts + judge/judgeRevisor.ts
- O Judge Revisor é um LLM secundário que avalia a saída do LLM primário antes de qualquer ação ser tomada.
- É a implementação prática de LLM-as-a-Judge no Nexus.

---

## 📍 SLIDE 04 — Por que o Judge existe

**Título:** Por que o Judge existe
- ✅ Detectar claims publicitários sem prova
- ✅ Sinalizar tom inadequado (agressivo, promessas irreais)
- ✅ Avaliar clareza e persuasão
- ✅ Classificar risco regulatório (CONAR, LGPD, CDC)

---

## 📍 SLIDE 05 — Como o Judge pontua

**Título:** Como o Judge pontua
- Threshold padrão: 0.75 (configurável no SHO).

---

## 📍 SLIDE 06 — Lendo a fila do Judge

**Título:** Lendo a fila do Judge
- 📝 Trecho da copy
- ⚠️ risk_flags (3-5 chips clicáveis)
- 💡 suggestions (1-3 melhorias sugeridas)
- ⏱️ Idade na fila (velho = prioridade)

---

## 📍 SLIDE 07 — Quando aprovar mesmo com nota baixa

**Título:** Quando aprovar mesmo com nota baixa
- Você conhece o segmento melhor que o Judge
- A campanha é de reativação (tom agressivo é OK)
- É um teste A/B explícito (você quer ver a resposta real)

---

## 📍 SLIDE 08 — Quando bloquear (mesmo com nota alta)

**Título:** Quando bloquear (mesmo com nota alta)
- Detectou claim_subjetivo com número específico
- A copy promete resultado sem disclaimer
- Tom pode ser interpretado como spam
- Fere uma regra do CONAR para seu nicho

---

## 📍 SLIDE 09 — Checklist e próximos passos

**Título:** O que precisa sair pronto daqui
- Revisar os conceitos centrais apresentados neste módulo
- Transformar os exemplos em configuração real no ecossistema Nexus
- Pré-requisito relacionado: ["agente/02-disparo-whatsapp"]
- Seguir para o próximo módulo com base documentada e operacional

