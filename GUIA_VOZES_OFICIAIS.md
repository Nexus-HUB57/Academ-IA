---
title: "Guia Rápido das Vozes Oficiais · AcademIA"
description: "Ponto de entrada rápido para uso das vozes oficiais. Detalhes em personas/voice_registry/"
tags: [vozes, tts, audio, personas, alencar, ive, narração, voice-cloning, guia]
last_updated: 2026-07-22
---

# 🎙️ Guia Rápido das Vozes Oficiais · AcademIA

> ⚠️ **DOCUMENTO SECUNDÁRIO** — A fonte canônica é `personas/voice_registry/OFFICIAL_VOICES_REGISTRY.md`. Este guia é um **resumo de uso rápido** para devs que só precisam saber qual arquivo usar.

---

## 👥 As Duas Vozes Oficiais

### 1. **Sir Nexus Alencar** — Mentor Técnico

- 📁 **Arquivo canônico**: `personas/alencar/audio/official_voice.wav`
- 🌐 **URL**: https://github.com/Nexus-HUB57/Academ-IA/tree/main/personas/alencar/audio
- 🎭 **Papel**: Sábio, sereno, autoridade intelectual
- 🗣️ **Voz**: Madura, controlada, didática
- 📚 **Quando usar**: Aulas técnicas, código, arquitetura, exemplos práticos
- 📋 **Detalhes**: `personas/alencar/identity.md`

### 2. **Lady Nexus Ive** — Estrategista de Marca

- 📁 **Arquivo canônico**: `personas/ive/audio/official_voice.wav`
- 🌐 **URL**: https://github.com/Nexus-HUB57/Academ-IA/tree/main/personas/ive/audio
- 🎭 **Papel**: Acolhedora, empoderadora, envolvente
- 🗣️ **Voz**: Leve rouquidão, sotaque sulista elegante
- 📚 **Quando usar**: Aulas estratégicas, aberturas, enceramentos, calls-to-action
- 📋 **Detalhes**: `personas/ive/identity.md` + `personas/ive/voice_guidelines.md`

---

## 🎯 Mapa de Uso Rápido

| Material | Voz | Arquivo |
|---|---|---|
| Curso técnico (código, RAG, deploy) | **Alencar** | `personas/alencar/audio/official_voice.wav` |
| Curso estratégico (vendas, marketing) | **Ive** | `personas/ive/audio/official_voice.wav` |
| Abertura de curso | **Ive** | `personas/ive/audio/official_voice.wav` |
| Encerramento de curso | **Alencar** | `personas/alencar/audio/official_voice.wav` |
| Treinamento (WS) — bloco técnico | **Alencar** | `personas/alencar/audio/official_voice.wav` |
| Treinamento (WS) — bloco estratégico | **Ive** | `personas/ive/audio/official_voice.wav` |
| Webinar — abertura/mestrado | **Ive** | `personas/ive/audio/official_voice.wav` |
| Webinar — técnico | **Alencar** | `personas/alencar/audio/official_voice.wav` |
| Playbook de crise | **Alencar** | `personas/alencar/audio/official_voice.wav` |
| Onboarding | **Ive** | `personas/ive/audio/official_voice.wav` |
| Alerta/notificação curta | **Alencar** | `personas/alencar/audio/official_voice.wav` |

---

## 🛠️ Como Usar em Código

### Voice Cloning (ElevenLabs)

```python
from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key="...")

# Alencar
audio = client.clone(
    name="Sir Nexus Alencar - Official",
    files=["personas/alencar/audio/official_voice.wav"],
    description="Voz PT-BR masculina, meia-idade, erudição sutil"
)

# Ive
audio = client.clone(
    name="Lady Nexus Ive - Official",
    files=["personas/ive/audio/official_voice.wav"],
    description="Voz PT-BR feminina, sotaque sulista elegante"
)
```

### OpenAI TTS (sem clone)

```python
from openai import OpenAI

client = OpenAI()

# Para Alencar (voz grave madura)
speech = client.audio.speech.create(
    model="tts-1-hd",
    voice="onyx",
    input="Bem-vindo à AcademIA. Eu sou Sir Nexus Alencar.",
)
```

### Voice Resolver (oficial no projeto)

```python
# Script oficial: personas/voice_registry/voice_resolver.py
from voice_resolver import resolve_voice

audio_alencar = resolve_voice("alencar")
audio_ive = resolve_voice("ive")
```

---

## 🚨 Regras de Ouro

1. **NUNCA** use voz genérica de TTS em produto final — sempre clone dos arquivos `.wav` oficiais
2. **NUNCA** misture as duas vozes na mesma frase (cada persona fala a sua vez)
3. **NUNCA** use voice IDs genéricos do ElevenLabs (`Portuguese_CharmingQueen`, etc.) em produção
4. **NUNCA** edite, normalize ou regrave os arquivos `.wav` originais
5. **SEMPRE** referencie o **registro canônico** em `personas/voice_registry/OFFICIAL_VOICES_REGISTRY.md`
6. **SEMPRE** use proporção 60% Alencar (técnico) / 40% Ive (estratégico) em materiais longos
7. **SEMPRE** mantenha 24kHz, mono, 16-bit PCM, sem ruído de fundo

---

## 📚 Documentação Completa

| Documento | Propósito |
|---|---|
| `personas/voice_registry/OFFICIAL_VOICES_REGISTRY.md` | **REGISTRO CANÔNICO** — referência oficial completa |
| `personas/voice_registry/voice_resolver.py` | Script oficial de resolução de voz |
| `personas/alencar/identity.md` | Identidade visual + textual do Alencar |
| `personas/ive/identity.md` | Identidade visual + textual da Ive |
| `personas/ive/voice_guidelines.md` | Diretrizes detalhadas de voz da Ive |
| `personas/dupla/interaction_guidelines.md` | Como Alencar e Ive interagem |
| `personas/dupla/guia-dupla-nexus.md` | Guia completo da dupla |
| `producao/PADRAO_VIDEOS_ACADEMIA.md` | Padrão de produção de vídeos |
| `producao/catalog/CATALOGO_MODULOS.md` | Catálogo de módulos |

---

## 🔗 Links Externos

- 📁 Repositório: https://github.com/Nexus-HUB57/Academ-IA
- 🎙️ Vozes Alencar: https://github.com/Nexus-HUB57/Academ-IA/tree/main/personas/alencar/audio
- 🎙️ Vozes Ive: https://github.com/Nexus-HUB57/Academ-IA/tree/main/personas/ive/audio
- 📜 Registro canônico: https://github.com/Nexus-HUB57/Academ-IA/blob/main/personas/voice_registry/OFFICIAL_VOICES_REGISTRY.md

---

**Versão 1.0** · Criado em 2026-07-22 · Mavis Agent
