---
title: "Vozes Oficiais · Personas AcademIA"
description: "Guia canônico das vozes oficiais das personas — Alencar e Ive"
tags: [personas, vozes, audio, tts, oficial]
version: "1.0.0"
last_updated: "2026-07-22"
---

# 🎙️ Vozes Oficiais · Personas AcademIA

> **Este é o registro canônico das vozes oficiais das personas.** Todos os vídeos, áudios, podcasts, treinamentos e materiais da AcademIA DEVEM usar essas vozes como referência.

## 📍 Localização no Repo

| Persona | Caminho | Arquivo | Tamanho | Duração |
|---------|---------|---------|---------|---------|
| **Sir Nexus Alencar** | `marca/personas/alencar/audio/` | `official_voice.wav` | 1.4MB | 29.16s |
| **Lady Nexus Ive** | `marca/personas/ive/audio/` | `official_voice.wav` | 1.5MB | 31.28s |

**URL pública:** [github.com/Nexus-HUB57/Academ-IA/tree/main/marca/personas](https://github.com/Nexus-HUB57/Academ-IA/tree/main/marca/personas)

## 🔧 Especificações Técnicas

| Parâmetro | Valor |
|-----------|-------|
| **Codec** | PCM 16-bit (pcm_s16le) |
| **Sample rate** | 24.000 Hz |
| **Canais** | 1 (mono) |
| **Bit depth** | 16-bit |
| **Bit rate** | 384 kbps |
| **Formato** | WAV (PCM) |
| **Tamanho** | ~1.4-1.5 MB |
| **Duração da amostra** | 29-31 segundos |

## 🎭 Personas

### 🎩 Sir Nexus Alencar
**Arquivo:** `marca/personas/alencar/audio/official_voice.wav`

- **Voz:** Masculina, grave, didática
- **Trilhas:** Fundamental + Agente (8 roteiros)
- **Tom:** Técnico, autoritário, com pausas em conceitos-chave
- **Uso:** Vídeos-aula, narração de cursos técnicos, apresentações, treinamentos
- **Velocidade recomendada:** 0.95x (mais pausado, didático)
- **Volume:** -3 dB a 0 dB

### 👑 Lady Nexus Ive
**Arquivo:** `marca/personas/ive/audio/official_voice.wav`

- **Voz:** Feminina, acolhedora, sensual sutil
- **Trilhas:** Master + Elite (7 roteiros, em dupla)
- **Tom:** Acolhedor, empoderador, humano
- **Uso:** Aberturas, fechamentos, conteúdo emocional, CTA
- **Velocidade recomendada:** 1.0x (ritmo natural)
- **Volume:** -3 dB a 0 dB

### 👥 Dupla (Ive + Alencar)
- **Aparece em:** Trilha Master + Elite (7 vídeos)
- **Formato:** Tela dividida. Ive abre, Alencar aprofunda, Ive contextualiza, Alencar fecha
- **Tom:** Estratégico, com tensão intelectual produtiva

## 🔄 Mapeamento para TTS Público

Quando usar **APIs públicas de TTS** (ElevenLabs, MiniMax Speech, Google TTS, etc.), mapear para as vozes mais próximas:

| Persona | TTS ElevenLabs (português) | TTS MiniMax Speech (português) | Características |
|---------|---------------------------|-------------------------------|-----------------|
| **Sir Nexus Alencar** | `Portuguese_Deep-VoicedGentleman` | `male-qn-qingse` (v1) ou `male-qn-jingying` | Voz masculina, grave, didática |
| **Lady Nexus Ive** | `Portuguese_Kind-heartedGirl` | `female-shaonv` (v1) ou `female-yujie` | Voz feminina, acolhedora, calorosa |

**⚠️ IMPORTANTE:** O mapeamento é uma aproximação. Para uso crítico (lançamento, comunicação oficial), usar **as amostras oficiais gravadas em estúdio** acima, e fazer **clonagem de voz via ElevenLabs Voice Cloning API** (a partir do `official_voice.wav`), preservando a identidade sonora exata.

## 🎬 Uso em Produção

### Cenário 1: Vídeo-aula (narração completa)
```bash
# Exemplo: vídeo 01-IOAID com voz do Alencar
synthesize_speech(
  text="Olá. Eu sou Sir Nexus Alencar...",
  voice_id="Portuguese_Deep-VoicedGentleman",
  speed=0.95
)
```

### Cenário 2: Dupla (Master/Elite)
- **Cena de abertura:** `voice_id="Portuguese_Kind-heartedGirl"` (Ive)
- **Cena técnica:** `voice_id="Portuguese_Deep-VoicedGentleman"` (Alencar)
- **Cena de fechamento:** `voice_id="Portuguese_Kind-heartedGirl"` (Ive)

### Cenário 3: Áudio oficial (clone de voz)
Para preservar a voz exata do estúdio:
1. Usar o `official_voice.wav` como sample para **ElevenLabs Voice Cloning**
2. Clonar a voz (1-3 minutos de áudio)
3. Usar a voz clonada em todas as gerações
4. Manter o `official_voice.wav` como **referência canônica** do repo

## 🚫 Restrições de Uso

- ✅ **Pode usar em:** vídeos-aula, treinamentos, podcasts, webinars, demos, materiais internos
- ✅ **Pode clonar via API** (com credenciais válidas) para escalar produção
- ❌ **NÃO pode:** redistribuir o `official_voice.wav` como se fosse do próprio usuário
- ❌ **NÃO pode:** modificar o arquivo original
- ❌ **NÃO pode:** usar a voz oficial para conteúdo que viole LGPD, promova discurso de ódio, ou viole ética profissional

## 📋 Checklist para Novo Material

Ao criar qualquer áudio/vídeo com persona, verificar:

- [ ] A persona correta foi usada (Alencar OU Ive OU Dupla)
- [ ] O `voice_id` TTS corresponde ao mapeamento oficial
- [ ] Velocidade adequada (0.95x Alencar, 1.0x Ive)
- [ ] Tom alinhado com as diretrizes da persona (ver `marca/personas/{persona}/identity.md`)
- [ ] Volume normalizado (-3 a 0 dB)
- [ ] Saída validada com `ffprobe` (24kHz, mono, PCM 16-bit)

## 🔗 Links Relacionados

- `marca/personas/alencar/identity.md` — Diretrizes de Alencar
- `marca/personas/ive/identity.md` — Diretrizes de Ive
- `marca/personas/ive/voice_guidelines.md` — Guia de voz detalhado da Ive
- `marca/personas/dupla/` — Diretrizes de co-atuação
- `videos/RENDER_PIPELINE.md` — Pipeline de renderização
- `videos/roteiros/` — Roteiros dos vídeos

---

**Mantido por:** MMN AI-to-AI
**Última atualização:** 2026-07-22 · v1.0.0
