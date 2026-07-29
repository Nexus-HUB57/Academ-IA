---
title: "Módulo Agente-02 · Slides · Disparando no WhatsApp"
description: "Slides visuais para acompanhar o módulo 02 da Trilha Agente"
tags: [slides, agente, modulo-02]
modulo: agent-02
trilha: Agente
ordem: 2
total_slides: 8
pattern: "MMN_IA"
---

# 📊 Slides · Agente 02 · Disparando no WhatsApp

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

**Título:** Disparando no WhatsApp
**Subtítulo:** Trilha Agente · Módulo 02
**Persona-guia:** Sra. Nexus Ive e Sir. Nexus Alencar

---

## 📍 SLIDE 02 — Objetivo do módulo

**Título:** O que você vai dominar neste módulo
- Regra de ouro do Nexus: toda mensagem no WhatsApp passa por template approval + opt-in verificado.
- Quebrar isso = ban permanente do número.
- [ ] Cada contato tem opted_in: true e opted_in_at < 12 meses
- [ ] O template foi aprovado pelo WhatsApp Business

---

## 📍 SLIDE 03 — Antes de tudo: LGPD e Template Approval

**Título:** Antes de tudo: LGPD e Template Approval
- Regra de ouro do Nexus: toda mensagem no WhatsApp passa por template approval + opt-in verificado.
- Quebrar isso = ban permanente do número.
- [ ] Cada contato tem opted_in: true e opted_in_at < 12 meses
- [ ] O template foi aprovado pelo WhatsApp Business

---

## 📍 SLIDE 04 — Passo a passo — primeiro disparo

**Título:** Passo a passo — primeiro disparo
- ### 1.
- Conecte o WhatsApp Business ### 2.
- Crie o template (se ainda não tem) Exemplo de template aprovado: Categorias aceitas: marketing (com opt-in) ou utility (transacional).
- ### 3.

---

## 📍 SLIDE 05 — Red flags (pause e investigue)

**Título:** Red flags (pause e investigue)
- Block rate > 2% por dia
- Read rate < 30%
- Templates reprovados pela Meta
- Pico de whatsapp.opt_out (pessoas saindo)

---

## 📍 SLIDE 06 — Exercício

**Título:** Exercício
- Configure o dispatcher WhatsApp
- Crie 1 template promo_especial_v1
- Envie para 20 contatos do segmento quentes_30d
- Aguarde 48h

---

## 📍 SLIDE 07 — Próximo passo

**Título:** Próximo passo
- 👉 03 · Lendo o Judge Revisor --- Versão 1.0 · Atualizado 2026-06-02 · Fonte: backend/src/agentic/skills/dispatcher.ts + autoPublisher.ts

---

## 📍 SLIDE 08 — Checklist e próximos passos

**Título:** O que precisa sair pronto daqui
- Revisar os conceitos centrais apresentados neste módulo
- Transformar os exemplos em configuração real no ecossistema Nexus
- Pré-requisito relacionado: ["agente/01-skills-essenciais"]
- Seguir para o próximo módulo com base documentada e operacional

