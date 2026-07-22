---
title: "Guia das Vozes Oficiais · AcademIA"
description: "Referência obrigatória para TTS, vídeos, audiobooks e narrações da AcademIA"
tags: [vozes, tts, audio, personas, alencar, ive, narração, voice-cloning]
last_updated: 2026-07-22
---

# 🎙️ Guia das Vozes Oficiais · AcademIA

> **Documento canônico.** Toda narração em áudio da AcademIA **DEVE** usar exclusivamente estas duas vozes oficiais. Qualquer TTS, voice-clone, audiobook ou vídeo-aula deve referenciar os arquivos abaixo.

---

## 👥 Os Dois Personas Oficiais

### 1. **Sir Nexus Alencar** — Mentor Técnico

| Atributo | Detalhe |
|---|---|
| **Papel** | Mentor técnico e rosto da marca |
| **Arquétipo** | Sábio, sereno, autoridade intelectual, acolhedor |
| **Visual** | Homem de meia-idade, traços judaicos, Kippah, olhos azuis, barba grisalha, social azul |
| **Voz** | Madura, serena, acolhedora |
| **Áudio oficial** | `personas/alencar/audio/official_voice.wav` |
| **Sotaque** | Português brasileiro neutro com leve erudição |
| **Cadência** | Controlada, pausada, explicativa |
| **Uso em roteiros** | Explicações técnicas profundas, exemplos práticos, demonstrações de código |
| **Personas complementares** | Atua em dupla com Sra. Ive |

**Fonte no repositório:**
- Áudio: https://github.com/Nexus-HUB57/Academ-IA/tree/main/personas/alencar/audio
- Identidade completa: `personas/alencar/identity.md`
- Diretrizes visuais: `personas/alencar/assets/`

---

### 2. **Lady Nexus Ive** — Estrategista de Marca

| Atributo | Detalhe |
|---|---|
| **Papel** | Estrategista de marca, anfitriã, instrutora principal |
| **Arquétipo** | Acolhedora, empoderadora, serena, sensual sutil |
| **Visual** | Mulher, sorriso marcante, presença sofisticada |
| **Voz** | Leve rouquidão, suave, sotaque sulista sutil |
| **Áudio oficial** | `personas/ive/audio/official_voice.wav` |
| **Sotaque** | Português brasileiro com sotaque sulista elegante (R marcado, vogais abertas) |
| **Cadência** | Controlada mas envolvente, "magnetismo" |
| **Uso em roteiros** | Abertura/encerramento, calls-to-action, visão estratégica |
| **Personas complementares** | Atua em dupla com Sr. Alencar |

**Fonte no repositório:**
- Áudio: https://github.com/Nexus-HUB57/Academ-IA/tree/main/personas/ive/audio
- Identidade completa: `personas/ive/identity.md`
- Diretrizes de voz: `personas/ive/voice_guidelines.md`
- Assets visuais: `personas/ive/assets/`

---

## 🎬 Onde Usar Cada Voz

| Material | Voz Preferencial | Por quê |
|---|---|---|
| **Aulas técnicas** (código, arquitetura) | **Alencar** | Tom sério, didático |
| **Aulas estratégicas** (negócios, vendas) | **Ive** | Empoderamento,CTA |
| **Aberturas de curso** (intro do módulo) | **Ive** | Acolhimento, contexto |
| **Encerramentos** (conclusão do módulo) | **Alencar** | Síntese, firmeza |
| **Treinamentos/workshops** (WS-*) | **Ambos alternados** | Dupla didática |
| **Webinars** (WB-*) | **Ive (mestre) + Alencar (técnico)** | Dinâmica de palco |
| **Playbooks de crise** (PB-CRISES-*) | **Alencar** | Comando assertivo |
| **Apostilas narradas** (audiobook) | **Ive** | Leitura envolvente |
| **Alertas / notificações curtas** | **Alencar** | Autoridade rápida |
| **Onboarding novos afiliados** | **Ive** | Acolhimento, bem-vinda |

---

## 🛠️ Como Usar os Áudios Oficiais

### 1. Voice Cloning (ElevenLabs / OpenAI Voice Engine)

```python
# ElevenLabs exemplo
from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key="...")

# Para Alencar (voz masculina madura)
audio_alencar = client.clone(
    name="Sir Nexus Alencar - Official",
    files=["personas/alencar/audio/official_voice.wav"],
    description="Voz masculina PT-BR, meia-idade, erudição sutil, didática"
)

# Para Ive (voz feminina acolhedora)
audio_ive = client.clone(
    name="Lady Nexus Ive - Official",
    files=["personas/ive/audio/official_voice.wav"],
    description="Voz feminina PT-BR, sotaque sulista, envolvente"
)
```

### 2. OpenAI TTS com Voice Embedding

```python
from openai import OpenAI

client = OpenAI()

# OpenAI TTS-1-HD (não clona, mas gera voz PT-BR de alta qualidade)
speech = client.audio.speech.create(
    model="tts-1-hd",
    voice="onyx",  # voz masculina grave (similar a Alencar)
    input="Bem-vindo à AcademIA. Eu sou Sir Nexus Alencar, seu mentor técnico.",
    language="pt-BR",
)
speech.stream_to_file("audio_alencar.mp3")
```

### 3. Edge TTS (gratuito, sem clonagem)

```python
import edge_tts

# Voz masculina PT-BR mais próxima de Alencar
communicate = edge_tts.Communicate(
    text="Bem-vindo à AcademIA. Eu sou Sir Nexus Alencar.",
    voice="pt-BR-AntonioNeural",  # masculina, meia-idade
)
communicate.save("alencar_edge.mp3")
```

---

## 🎯 Regras de Ouro (NÃO QUEBRAR)

1. **NUNCA** use voz genérica de TTS em produto final — sempre clonar das oficiais
2. **NUNCA** misture as duas vozes em uma mesma frase (cada persona fala a vez dele)
3. **NUNCA** altere tom de voz sem aprovação (afeta identidade da marca)
4. **SEMPRE** referencie `GUIA_VOZES_OFICIAIS.md` antes de criar áudio
5. **SEMPRE** use os arquivos `.wav` da pasta `audio/` (nunca regrave ou edite)
6. **SEMPRE** mantenha a proporção 60% Alencar (técnico) / 40% Ive (estratégico) em materiais longos
7. **SEMPRE** atualize este guia se novas vozes oficiais forem adicionadas

---

## 📋 Checklist de Áudio (TTS/Clone)

Antes de publicar qualquer áudio:

- [ ] Voz é Alencar ou Ive (nenhuma outra)
- [ ] Arquivo fonte é `personas/{alencar,ive}/audio/official_voice.wav`
- [ ] Sotaque preservado (Alencar: neutro-erudito / Ive: sulista-elegante)
- [ ] Cadência compatível (Alencar: pausada / Ive: envolvente)
- [ ] Metadata do arquivo inclui: `voice="Sir Nexus Alencar" ou "Lady Nexus Ive"`
- [ ] Frontmatter do roteiro indica qual persona narra
- [ ] Não há mistura de vozes na mesma faixa
- [ ] Volume normalizado (-3dB padrão)
- [ ] Sample rate 48kHz (padrão vídeo) ou 24kHz (padrão podcast)

---

## 📚 Documentação Complementar

- `personas/alencar/identity.md` — Identidade visual + textual do Alencar
- `personas/alencar/roteiro-aula01.md` — Roteiro de exemplo com Alencar
- `personas/ive/identity.md` — Identidade visual + textual da Ive
- `personas/ive/voice_guidelines.md` — Diretrizes detalhadas de voz
- `personas/dupla/interaction_guidelines.md` — Como Alencar e Ive interagem

---

## 🔗 Links Úteis

- Repositório: https://github.com/Nexus-HUB57/Academ-IA
- Áudio Alencar: https://github.com/Nexus-HUB57/Academ-IA/tree/main/personas/alencar/audio
- Áudio Ive: https://github.com/Nexus-HUB57/Academ-IA/tree/main/personas/ive/audio

---

**Versão 1.0** · Criado em 2026-07-22 · Mavis Agent
