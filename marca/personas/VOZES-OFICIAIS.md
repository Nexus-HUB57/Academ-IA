# 🎙️ Vozes Oficiais · Personas AcademIA

> **Registro formal das vozes oficiais que devem ser usadas em TODA produção de conteúdo da AcademIA.**
> Não use nenhuma outra voz para essas personas. Se precisar de variação, **documente aqui primeiro**.

## 🔐 Status: OFICIAL · VINCULANTE

| Campo | Valor |
|-------|-------|
| **Versão** | 1.0.0 |
| **Status** | 🔒 Oficial / Vinculante |
| **Última atualização** | 2026-07-22 |
| **Owner** | Ravi (CTO/AI) + Helena (CMO/AI) |
| **Aprovado por** | Niko Nexus (CEO/AI) + Sócio Humano |
| **Localização canônica** | `Academ-IA/marca/personas/{persona}/audio/` |

---

## 🎯 Personas e Vozes Canônicas

### 1. **Sir. Nexus Alencar** 🟣

**Voz oficial:** `marca/personas/alencar/audio/official_voice.wav`

| Atributo | Valor |
|----------|-------|
| **Arquivo** | `marca/personas/alencar/audio/official_voice.wav` |
| **Tamanho** | 1.399.724 bytes (1.4 MB) |
| **Duração estimada** | ~15-20 segundos de fala limpa |
| **SHA-256** | `b87c8b6f08ab477e...` (verificar com `sha256sum`) |
| **Sample rate** | 24 kHz (PCM 16-bit mono) |
| **Idioma** | Português (BR) |
| **Sotaque** | Judaico, formal, autoridade técnica |
| **Tom** | Sério, calmo, mentor sábio |
| **Pitch médio** | Médio-grave (homem ~50-55 anos) |
| **Velocidade natural** | 0.85-0.95× (mais pausado) |
| **Características** | Barba grisalha na voz, formal, didático |
| **Use em** | Tutoriais técnicos, módulos Fundamental + Agente + Master |
| **NÃO use em** | Conteúdo curto de social media (use Dupla) |

### 2. **Lady Nexus Ive** 🔵

**Voz oficial:** `marca/personas/ive/audio/official_voice.wav`

| Atributo | Valor |
|----------|-------|
| **Arquivo** | `marca/personas/ive/audio/official_voice.wav` |
| **Tamanho** | 1.501.484 bytes (1.5 MB) |
| **Duração estimada** | ~15-20 segundos de fala limpa |
| **SHA-256** | `b5bd36cabb244f62...` (verificar com `sha256sum`) |
| **Sample rate** | 24 kHz (PCM 16-bit mono) |
| **Idioma** | Português (BR) |
| **Sotaque** | Sulista, leve, sereno |
| **Tom** | Didático, gentil, encorajador |
| **Pitch médio** | Médio (mulher ~35-40 anos) |
| **Velocidade natural** | 0.95-1.05× (ritmo natural) |
| **Características** | Leve sotaque RS, didática, acolhedora |
| **Use em** | Trilha Fundamental (conceitos base), Master (funis) |
| **NÃO use em** | Conteúdo mais técnico-elite (use Dupla) |

### 3. **Dupla Ive + Alencar** 🌸

**Voz oficial:** Composição de ambas as vozes acima (sem sample próprio)

| Atributo | Valor |
|----------|-------|
| **Composição** | 50% Ive + 50% Alencar, alternando falas |
| **Sample próprio** | ❌ Não há sample canônico único |
| **Como produzir** | Mix das 2 vozes oficiais (Ive em "histórias" e "conceitos", Alencar em "autoridade" e "técnica") |
| **Use em** | Módulos Elite, conteúdo arquitetural, storytelling |
| **NÃO use em** | Quando uma voz só é mais efetiva (clareza) |

---

## ✅ Regras de Uso

### OBRIGATÓRIO

1. **SEMPRE use a voz oficial** para qualquer produção (vídeo, audio, podcast)
2. **SEMPRE referencie o SHA-256** quando fizer upload de variação
3. **SEMPRE documente aqui** se criar uma nova voz derivada
4. **NUNCA use TTS genérico** (Google TTS, Amazon Polly) para essas personas
5. **NUNCA modifique a voz** (pitch, velocidade) sem documentar aqui

### Permissões

| Quem pode usar | Onde |
|----------------|------|
| ✅ Time AcademIA (Ravi, Helena, Otavio) | Vídeos de cursos |
| ✅ Time Marketing (Helena) | Social media, ads |
| ✅ Afiliados premium | Com aprovação de Helena |
| ❌ Uso pessoal | Proibido |
| ❌ Redistribuição | Proibido sem NDA |

---

## 🔧 Como Usar no Pipeline

### Opção 1: API de TTS com voz clonada

```python
import requests

# Upload do sample para a API
files = {'audio': open('marca/personas/alencar/audio/official_voice.wav', 'rb')}
response = requests.post('https://api.tts-provider.com/clone', files=files)
voice_id = response.json()['voice_id']  # ex: "alencar_v1"

# Sintetizar com a voz clonada
requests.post('https://api.tts-provider.com/synthesize', json={
    'voice_id': voice_id,
    'text': 'Olá, sou Sir. Nexus Alencar...',
    'output_file': 'output.wav'
})
```

### Opção 2: SDK local (offline)

```python
from TTS.api import TTS

tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
tts.tts_to_file(
    text="Olá, sou Sir. Nexus Alencar...",
    speaker_wav="marca/personas/alencar/audio/official_voice.wav",
    language="pt",
    file_path="output.wav"
)
```

### Opção 3: MiniMax Platform (synthesize_speech com voice_id clonado)

```python
# Após clonar a voz via clone_voice
synthesize_speech(
    text="Olá, sou Sir. Nexus Alencar...",
    output_file_path="output.wav",
    voice_id="alencar_cloned_v1",  # configurado via upload_clone_audio
    speed=0.9
)
```

---

## 📊 Especificações Técnicas

### Formato do Sample

```
Container:   WAV (RIFF)
Codec:       PCM (uncompressed)
Sample rate: 24.000 Hz
Bit depth:   16-bit
Channels:    1 (mono)
Bitrate:     ~384 kbps
Tamanho:     1.4-1.5 MB para 15-20s
```

**Importante:** Sample deve estar em **mono**. Se estiver em stereo, converter antes com:
```bash
ffmpeg -i input_stereo.wav -ac 1 output_mono.wav
```

### Verificação de Integridade

```bash
# Conferir SHA-256
sha256sum marca/personas/alencar/audio/official_voice.wav
# Esperado: b87c8b6f08ab477e... (primeiros 16 chars)

sha256sum marca/personas/ive/audio/official_voice.wav
# Esperado: b5bd36cabb244f62...

# Conferir formato técnico
file marca/personas/alencar/audio/official_voice.wav
# Esperado: "RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 24000 Hz"
```

---

## 🔄 Versionamento de Vozes

Se precisar criar uma **nova versão** da voz (ex: para capturar nuance de emoção):

1. **Não substitua** o arquivo oficial
2. Crie arquivo com sufixo: `official_voice_v2.wav`
3. Adicione entrada na tabela abaixo
4. Commit + PR para revisão
5. Após aprovação, atualize este documento

### Histórico de Versões

| Persona | Arquivo | Data | SHA-256 | Aprovado por | Notas |
|---------|---------|------|---------|--------------|-------|
| Alencar | official_voice.wav | 2026-07-22 | b87c8b6f... | Niko + Sócio | Versão inicial |
| Ive | official_voice.wav | 2026-07-22 | b5bd36ca... | Niko + Sócio | Versão inicial |

---

## 🚨 Anti-Patterns (NÃO FAÇA)

- ❌ Usar voz genérica feminina para substituir Ive
- ❌ Usar voz genérica masculina para substituir Alencar
- ❌ Aplicar pitch shift sem documentar
- ❌ Combinar vozes com outros personagens sem aprovação
- ❌ Usar sample de baixa qualidade (ruído, eco, música de fundo)
- ❌ Usar sample com menos de 10s ou mais de 60s
- ❌ Usar sample em idioma diferente sem treinar modelo multilíngue

---

## 📚 Como Clonar a Voz (procedimento oficial)

```bash
# 1. Upload do sample
upload_clone_audio(
  audio_file_path="marca/personas/alencar/audio/official_voice.wav"
)
# Retorna: file_id (ex: "file_abc123")

# 2. Clonar a voz
clone_voice(
  file_id="file_abc123",
  voice_id="alencar_official",  # ID fixo e canônico
  demo_text="Olá, eu sou Sir. Nexus Alencar, mentor e co-fundador da AcademIA Nexus.",
  demo_audio_output_path="/tmp/alencar_demo.wav"
)

# 3. Validar
# Ouvir /tmp/alencar_demo.wav
# Se OK, usar voice_id="alencar_official" em todas as chamadas synthesize_speech
```

---

## 🔗 Links Canônicos (GitHub)

| Persona | URL |
|---------|-----|
| **Sir Alencar** | https://github.com/Nexus-HUB57/Academ-IA/tree/main/marca/personas/alencar/audio |
| **Lady Ive** | https://github.com/Nexus-HUB57/Academ-IA/tree/main/marca/personas/ive/audio |

> **Nota importante:** A URL oficial é `marca/personas/` (NÃO `personas/`).
> A pasta `personas/` legada foi consolidada em `marca/personas/` em 2026-07-22.

---

## 📋 Checklist de Produção

Antes de usar a voz em produção:

- [ ] Conferi o SHA-256 do sample (b87c8b6f para Alencar, b5bd36ca para Ive)
- [ ] Conferi formato técnico (24kHz, 16-bit, mono)
- [ ] Clonei a voz via API/SDK (voice_id canônico)
- [ ] Testei a síntese com texto curto
- [ ] Validei qualidade de áudio (sem ruído, sem clipping)
- [ ] Documentei aqui se criei variante

---

## 🆘 Em Caso de Problema

| Problema | Causa | Solução |
|----------|-------|---------|
| Áudio com ruído | Sample de má qualidade | Re-extrair sample limpo |
| Pitch estranho | Modelo treinado com sample errado | Re-clonar com sample correto |
| Sotaque errado | Modelo não-PR | Usar modelo multilíngue |
| Voz não soa como persona | Voice_id errado | Verificar voice_id canônico |
| Sample corrompido | SHA-256 não bate | Re-download do GitHub oficial |

---

## 📝 Histórico de Atualizações

| Data | Versão | Mudança | Por |
|------|--------|---------|-----|
| 2026-07-22 | 1.0.0 | Criação do registro oficial de vozes | Mavis (CTO/AI) |

---

*AcademIA · Vozes Oficiais · 2026*