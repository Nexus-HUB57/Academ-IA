---
title: "Vozes Oficiais · Sir Nexus Alencar & Lady Nexus Ive"
description: "Referência canônica das vozes oficiais fixadas no repositório, perfis de voz e diretrizes de uso"
tags: [personas, voices, alencar, ive, oficial, canonico, tts]
category: personas
status: canonico
version: "1.0"
last_review: "2026-07-22"
---

# 🎙️ Vozes Oficiais · Sir Nexus Alencar & Lady Nexus Ive

> **Source of truth** das vozes oficiais do ecossistema Nexus. Este documento é a referência canônica para qualquer produção de áudio, TTS, clonagem, ou material didático que utilize as personas oficiais.

---

## 📂 Localização Canônica

As vozes oficiais estão **fixadas no repositório** em:

| Persona | Arquivo | URL |
|---------|---------|-----|
| **Sir Nexus Alencar** | `personas/alencar/audio/official_voice.wav` | https://github.com/Nexus-HUB57/Academ-IA/tree/main/personas/alencar/audio |
| **Lady Nexus Ive** | `personas/ive/audio/official_voice.wav` | https://github.com/Nexus-HUB57/Academ-IA/tree/main/personas/ive/audio |

**Estes arquivos são a referência primária.** Qualquer material novo deve usar estas vozes como clone source.

---

## 🎭 Perfil de Cada Voz

### Sir Nexus Alencar

- **Arquivo:** `personas/alencar/audio/official_voice.wav`
- **Tamanho:** ~1.4 MB
- **Duração:** ~30-60s (sample de referência)
- **Características da voz:**
  - **Tom**: masculino, maduro, sério mas caloroso
  - **Timbre**: grave, com presença autoritária
  - **Cadência**: pausada, didática, com peso em cada palavra
  - **Sotaque**: português brasileiro (sotaque SP, sem regionalismos fortes)
  - **Velocidade natural**: ~140 palavras/minuto
  - **Pitch natural**: médio-grave
- **Quando usar:**
  - Treinamentos técnicos.
  - Debates densos.
  - Decisões executivas.
  - Mensagens de governança.
- **Quando NÃO usar:**
  - Conteúdo puramente motivacional.
  - Materiais com tom íntimo/pessoal.
  - Vozes que contradigam seu registro institucional.

### Lady Nexus Ive

- **Arquivo:** `personas/ive/audio/official_voice.wav`
- **Tamanho:** ~1.5 MB
- **Duração:** ~30-60s (sample de referência)
- **Características da voz:**
  - **Tom**: feminino, sereno, envolvente
  - **Timbre**: claro, com calor humano sutil
  - **Cadência**: fluida, com pausas para reflexão
  - **Sotaque**: português brasileiro (sotaque SP, com leveza carioca na entonação)
  - **Velocidade natural**: ~150 palavras/minuto
  - **Pitch natural**: médio-alto
- **Quando usar:**
  - Aberturas e encerramentos.
  - Mediação de debates.
  - Mensagens de acolhimento.
  - Reflexões filosóficas/conceituais.
- **Quando NÃO usar:**
  - Decisões técnicas puras.
  - Códigos ou outputs determinísticos.
  - Vozes que contradigam seu registro institucional.

---

## 🎬 Como Usar as Vozes Oficiais

### 1. Clone via ElevenLabs (recomendado)

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="<your_key>")

# Upload da voz Alencar
alencar_voice = client.clone(
    name="Sir Nexus Alencar - Oficial",
    files=["personas/alencar/audio/official_voice.wav"],
    description="Voz oficial canônica de Sir Nexus Alencar para a Academ'IA.",
)

# Upload da voz Ive
ive_voice = client.clone(
    name="Lady Nexus Ive - Oficial",
    files=["personas/ive/audio/official_voice.wav"],
    description="Voz oficial canônica de Lady Nexus Ive para a Academ'IA.",
)
```

### 2. Clone via MiniMax / MiniMax T2A

```python
import requests

# Endpoint MiniMax
url = "https://api.minimaxi.chat/v1/voice_clone"
files = {"audio": open("personas/alencar/audio/official_voice.wav", "rb")}
data = {
    "voice_id": "sir_nexus_alencar_oficial",
    "name": "Sir Nexus Alencar - Oficial",
    "description": "Voz oficial canônica de Sir Nexus Alencar para a Academ'IA.",
}
response = requests.post(url, files=files, data=data, headers={"Authorization": "Bearer <key>"})
```

### 3. Uso Direto no Conteúdo

Em qualquer produção (vídeo, podcast, simulação):

- **Use a voz clonada** (não a voz original) para permitir customização de tom/velocidade.
- **Mantenha a referência** ao `official_voice.wav` no projeto, para garantir consistência.
- **Não edite o original** — versão é canônica.

---

## 🛡️ Diretrizes de Uso

### Permitido

- ✅ Clonar a voz para uso em materiais da Academ'IA.
- ✅ Ajustar velocidade, pitch, emoção (via TTS provider).
- ✅ Usar em webinars, treinamentos, podcasts, vídeos.
- ✅ Combinar as duas vozes em diálogo (regra da Dupla).
- ✅ Re-voicing em outros idiomas (manter personalidade).

### Não Permitido

- ❌ Usar a voz fora do contexto institucional Nexus.
- ❌ Criar conteúdo que contradiga valores da plataforma.
- ❌ Modificar a voz para soar como outra persona.
- ❌ Usar em conteúdo enganoso ou manipulação.
- ❌ Distribuir a voz fora do ecossistema Nexus sem autorização.

---

## 📊 Especificações Técnicas Recomendadas

### ElevenLabs (Settings Padrão)

| Parâmetro | Alencar | Ive |
|-----------|---------|-----|
| **Stability** | 0.65 | 0.55 |
| **Clarity + Similarity** | 0.78 | 0.80 |
| **Style exaggeration** | 0.20 | 0.35 |
| **Speaker boost** | true | true |

### MiniMax (Settings Padrão)

| Parâmetro | Alencar | Ive |
|-----------|---------|-----|
| **Speed** | 0.95 | 1.00 |
| **Pitch** | -2 | 0 |
| **Volume** | 1.0 | 1.0 |
| **Emotion** | neutral (base) | neutral (base) |
| **Voice ID** | `sir_nexus_alencar_oficial` | `lady_nexus_ive_oficial` |

---

## 🔄 Versionamento de Vozes

Caso uma voz precise ser **atualizada** (re-clonada, ajustada):

1. **Backup** o arquivo atual para `audio/official_voice_v{N}.wav`.
2. **Grave nova versão** com consentimento explícito da persona original.
3. **Documente** a mudança no `CHANGELOG.md` da pasta da persona.
4. **Não apague** a versão anterior — versionamento é não-destrutivo.

---

## 🤝 Uso em Conjunto (Dupla)

Quando as duas vozes aparecem **juntas** (vide `personas/dupla/guia-dupla-nexus.md`):

- **Alencar** fala primeiro em contexto técnico/estratégico.
- **Ive** fala primeiro em contexto motivacional/conceitual.
- **Alternância** com pausas de 200-500ms entre falas.
- **Nunca sobreposição** — uma voz de cada vez.

---

## 📂 Arquivos Relacionados

- [Persona Alencar](alencar/identity.md)
- [Persona Ive](ive/identity.md)
- [Diretrizes de Voz Ive](ive/voice_guidelines.md)
- [Guia da Dupla Nexus](dupla/guia-dupla-nexus.md)
- [Diretrizes de Interação Dupla](dupla/interaction_guidelines.md)

## 👥 Ownership

- **Owner:** Head de Marca + Head de Conteúdo
- **Reviewers:** Alencar, Ive (personas oficiais)
- **Cadência de revisão:** Semestral

---

*Nexus Affil'IA'te · Personas · OFFICIAL_VOICES.md · v1.0 · Julho 2026*
