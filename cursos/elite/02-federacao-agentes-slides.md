---
title: "Módulo Elite-02 · Slides · Federação de Agentes"
description: "Slides visuais para acompanhar o módulo 02 da Trilha Elite"
tags: [slides, elite, modulo-02]
modulo: elite-02
trilha: Elite
ordem: 2
total_slides: 9
pattern: "MMN_IA"
---

# 📊 Slides · Elite 02 · Federação de Agentes

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

**Título:** Federação de Agentes
**Subtítulo:** Trilha Elite · Módulo 02
**Persona-guia:** Sra. Nexus Ive e Sir. Nexus Alencar

---

## 📍 SLIDE 02 — Objetivo do módulo

**Título:** O que você vai dominar neste módulo
- Federação = agentes em máquinas diferentes (ou regiões diferentes) que se autenticam mutuamente, trocam tarefas e constroem confiança ao longo do tempo.
- No Nexus, a federação herda o design do Ruflo Agent Federation (referência: docs da Ruflo/Claude-Flow):

---

## 📍 SLIDE 03 — O que é federação

**Título:** O que é federação
- Federação = agentes em máquinas diferentes (ou regiões diferentes) que se autenticam mutuamente, trocam tarefas e constroem confiança ao longo do tempo.
- No Nexus, a federação herda o design do Ruflo Agent Federation (referência: docs da Ruflo/Claude-Flow):

---

## 📍 SLIDE 04 — Como iniciar uma federação

**Título:** Como iniciar uma federação
- ### Passo 1 — Inicializar ### Passo 2 — Conectar a outro nó ### Passo 3 — Enviar primeira tarefa

---

## 📍 SLIDE 05 — Trust levels (5 estágios)

**Título:** Trust levels (5 estágios)
- Upgrade requer histórico (mínimo 30 dias, success rate > 90%).
- Downgrade é instantâneo em caso de mau comportamento.

---

## 📍 SLIDE 06 — PII-gating em ação

**Título:** PII-gating em ação
- Quando você envia uma tarefa federada, antes de sair do seu nó: Configuração por trust level:

---

## 📍 SLIDE 07 — Auditoria

**Título:** Auditoria
- A trilha é buscável via HNSW (RAG semântico).
- Toda mensagem federada gera um registro imutável:

---

## 📍 SLIDE 08 — Exercício

**Título:** Exercício
- Levante 2 nós Nexus locais (containers Docker)
- federation init em cada um
- Conecte um ao outro
- Envie uma tarefa simples: "qual a data atual?"

---

## 📍 SLIDE 09 — Checklist e próximos passos

**Título:** O que precisa sair pronto daqui
- Revisar os conceitos centrais apresentados neste módulo
- Transformar os exemplos em configuração real no ecossistema Nexus
- Pré-requisito relacionado: ["elite/01-multi-tenant-whitelabel"]
- Seguir para o próximo módulo com base documentada e operacional

