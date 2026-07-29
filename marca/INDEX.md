---
title: "Marca · Índice Navegável"
description: "Índice navegável da pasta de marca — personas oficiais, vozes, assets visuais e diretrizes"
tags: [marca, indice, personas, branding, navegacao]
version: 1.0.0
last_updated: 2026-07-24
pattern: "MMN_IA"
---

# 🎨 Marca · Índice Navegável

> **Índice navegável** da pasta `marca/` — concentrada em **personas oficiais** (Alencar, Ive, Dupla), suas vozes canônicas, e assets visuais. Documenta o que é **source of truth** vs versões alternativas.

## 🎯 Propósito

A pasta `marca/` é o **repositório canônico de identidade visual e vocal** da Academ'IA. Tudo que envolve as personas oficiais mora aqui:

- Quem são as personas (ficha técnica)
- Como elas falam (voz oficial)
- Como elas se parecem (assets visuais)
- Como elas interagem (quando usar Dupla)
- Versionamento de vozes (registry)

## 📊 Visão Geral

| Subpasta | Função | Arquivos |
|----------|--------|----------|
| `personas/alencar/` | Persona Sir Nexus Alencar | 4 .md + assets + 3 áudios oficiais |
| `personas/ive/` | Persona Sra. Nexus Ive | 3 .md + assets + 1 áudio oficial |
| `personas/dupla/` | Co-apresentação Alencar+Ive | 2 .md + assets |
| `personas/voice_registry/` | Registry de vozes canônicas | 1 .md |
| `personas/` (raiz) | Documentos agregadores | 3 .md (OFFICIAL_VOICES, VOICES, VOZES-OFICIAIS) |

## 👥 Personas Oficiais

### 👨 Sir Nexus Alencar

**Papel:** Técnico, prático, profundo
**Estilo:** Didático, claro, preciso
**Voz:** Tom masculino maduro, timbre grave, cadência pausada
**Sotaque:** PT-BR SP, ~140 wpm, pitch médio-grave

**Documentos canônicos:**
- [`personas/alencar/sir_nexus_alencar.md`](personas/alencar/sir_nexus_alencar.md) — Ficha técnica completa
- [`personas/alencar/identity.md`](personas/alencar/identity.md) — Diretrizes de identidade
- [`personas/alencar/roteiro-aula01.md`](personas/alencar/roteiro-aula01.md) — Exemplo de roteiro
- [`personas/alencar/slides-aula01.md`](personas/alencar/slides-aula01.md) — Exemplo de slides

**Áudio oficial canônico:**
- [`personas/alencar/audio/official_voice.wav`](personas/alencar/audio/official_voice.wav) — **SOURCE OF TRUTH** (30-60s)
- [`personas/alencar/audio/official_voice Sir Nexus Alencar Dublado.wav`](personas/alencar/audio/official_voice%20Sir%20Nexus%20Alencar%20Dublado.wav) — Versão dublada
- [`personas/alencar/audio/Official_Voice Original Modelo Oficial Voz Sir Nexus Alencar.wav`](personas/alencar/audio/Official_Voice%20Original%20Modelo%20Oficial%20Voz%20Sir%20Nexus%20Alencar.wav) — Versão original
- [`personas/alencar/voz_sir_nexus_alencar.wav`](personas/alencar/voz_sir_nexus_alencar.wav) — Áudio de teste
- [`personas/alencar/sir_nexus_alencar_intro.wav`](personas/alencar/sir_nexus_alencar_intro.wav) — Intro

**Assets visuais:**
- [`personas/alencar/Sir_Alencar.png`](personas/alencar/Sir_Alencar.png) — Avatar principal
- [`personas/alencar/sir_nexus_alencar.webp`](personas/alencar/sir_nexus_alencar.webp) — Versão webp
- [`personas/alencar/assets/`](personas/alencar/assets/) — Banco de imagens de referência

### 👩 Sra. Nexus Ive

**Papel:** Matriarca, estrategista, acolhedora
**Estilo:** Sotaque sulista, serenidade, autoridade
**Voz:** Tom feminino sereno, timbre claro, cadência fluida
**Sotaque:** PT-BR SP com leveza carioca, ~150 wpm, pitch médio-alto

**Documentos canônicos:**
- [`personas/ive/sra_nexus_ive.md`](personas/ive/sra_nexus_ive.md) — Ficha técnica completa
- [`personas/ive/identity.md`](personas/ive/identity.md) — Diretrizes de identidade
- [`personas/ive/voice_guidelines.md`](personas/ive/voice_guidelines.md) — Diretrizes específicas de voz

**Áudio oficial canônico:**
- [`personas/ive/audio/official_voice.wav`](personas/ive/audio/official_voice.wav) — **SOURCE OF TRUTH** (30-60s)
- [`personas/ive/audio/Official_voice Dublado Portugues Modelo Oficial Voz Lady Ive Nexus.wav`](personas/ive/audio/Official_voice%20Dublado%20Portugues%20Modelo%20Oficial%20Voz%20Lady%20Ive%20Nexus.wav) — Versão dublada

**Assets visuais:**
- [`personas/ive/assets/`](personas/ive/assets/) — Banco de imagens de referência

### 👥 Dupla Ive + Alencar

**Papel:** Co-apresentação harmônica
**Estilo:** Complementaridade, cumplicidade
**Quando usar:** Eventos especiais, lançamentos, whitepapers, momentos de marca

**Documentos:**
- [`personas/dupla/guia-dupla-nexus.md`](personas/dupla/guia-dupla-nexus.md) — Guia de uso da dupla
- [`personas/dupla/interaction_guidelines.md`](personas/dupla/interaction_guidelines.md) — Diretrizes de interação

**Templates de roteiro:**
- [`../producao/templates/TEMPLATE_ROTEIRO_DUPLA.md`](../producao/templates/TEMPLATE_ROTEIRO_DUPLA.md)

## 🎙️ Registry de Vozes

[`personas/voice_registry/OFFICIAL_VOICES_REGISTRY.md`](personas/voice_registry/OFFICIAL_VOICES_REGISTRY.md) — **Registry canônico** de todas as vozes oficiais, com versão, fonte, e changelog. Use este documento para saber qual é a versão atual de cada voz.

## 📋 Documentos Agregadores (raiz personas/)

> ⚠️ Múltiplos documentos agregadores existem na raiz. **OFFICIAL_VOICES.md é o source of truth** (consolidado por Mavis).

- [`personas/OFFICIAL_VOICES.md`](personas/OFFICIAL_VOICES.md) — ✅ **SOURCE OF TRUTH** (consolidado)
- [`personas/VOICES.md`](personas/VOICES.md) — Documento legacy
- [`personas/VOZES-OFICIAIS.md`](personas/VOZES-OFICIAIS.md) — Versão PT-BR

> **Regra de ouro:** ao criar conteúdo novo, referencie `OFFICIAL_VOICES.md` (não as versões legacy).

## 🛡️ Convenções de Marca

### Identidade visual

- **Paleta:** cyan (#63eaff), purple (#b78cff), gold (#facc15)
- **Tipografia:** Inter (sans-serif) para corpo, com títulos em peso 700/800
- **Background:** dark (gradiente radial do #0a1530 ao #050810)
- **Vinhetas:** transições curtas, max 1s

### Identidade vocal

- **PT-BR** (sotaque SP padrão)
- **Velocidade:** 140-160 wpm
- **Tom:** profissional mas acessível
- **Pausas:** naturais (não roboticamente uniformes)

### Uso de Dupla

- **Aprovação prévia** de Head de Marca
- **Contexto institucional** (lançamento, milestone, whitepaper)
- **Templates próprios** (não usar templates de persona única)
- **Roteiro revisado** por 2 pessoas (uma Ive, uma Alencar)

## 📂 Estrutura

```
marca/
├── INDEX.md                       ← este arquivo
└── personas/
    ├── OFFICIAL_VOICES.md          ← SOURCE OF TRUTH
    ├── VOICES.md                   (legacy)
    ├── VOZES-OFICIAIS.md           (legacy PT-BR)
    ├── alencar/
    │   ├── sir_nexus_alencar.md
    │   ├── identity.md
    │   ├── roteiro-aula01.md
    │   ├── slides-aula01.md
    │   ├── audio/
    │   │   ├── official_voice.wav          ← CANÔNICO
    │   │   ├── official_voice Sir Nexus Alencar Dublado.wav
    │   │   ├── Official_Voice Original Modelo Oficial Voz Sir Nexus Alencar.wav
    │   │   ├── voz_sir_nexus_alencar.wav
    │   │   └── sir_nexus_alencar_intro.wav
    │   ├── assets/
    │   ├── Sir_Alencar.png
    │   ├── Dados Fisicos.png
    │   ├── Alencar +_Sra_Nexus_Ive_35.png
    │   ├── alencar_meeting_monitor.png
    │   ├── alencar_nexus_ref.png
    │   ├── sir_nexus_alencar.webp
    │   └── Estes_são_os_personas_Ive_Nexu.mp4
    ├── ive/
    │   ├── sra_nexus_ive.md
    │   ├── identity.md
    │   ├── voice_guidelines.md
    │   ├── audio/
    │   │   ├── official_voice.wav          ← CANÔNICO
    │   │   └── Official_voice Dublado Portugues Modelo Oficial Voz Lady Ive Nexus.wav
    │   └── assets/
    ├── dupla/
    │   ├── guia-dupla-nexus.md
    │   ├── interaction_guidelines.md
    │   └── assets/
    │       └── celebration_ive_alencar.png
    └── voice_registry/
        └── OFFICIAL_VOICES_REGISTRY.md
```

## 🔗 Links Cruzados

- [`../producao/roteiros/INDEX.md`](../producao/roteiros/INDEX.md) — Índice de roteiros (usa personas)
- [`../producao/templates/`](../producao/templates/) — Templates por persona
- [`../producao/PIPELINE_PRODUCAO.md`](../producao/PIPELINE_PRODUCAO.md) — Pipeline de produção
- [`../Lib-Nexus/best-practices/`](../Lib-Nexus/best-practices/) — Padrões técnicos
- [`../governanca/`](../governanca/) — Governança de marca e IA responsável
- [`../GUIA_MULTI_DEV.md`](../GUIA_MULTI_DEV.md) — Convenções multi-dev

## 👥 Ownership

- **Owner:** Head de Marca + Head de Produção
- **Aprovação de mudanças:** Head de Marca
- **Cadência de revisão:** Semestral ou a cada release de nova voz

---

*Nexus Affil'IA'te · marca/INDEX.md · v1.0.0 · Julho 2026*
