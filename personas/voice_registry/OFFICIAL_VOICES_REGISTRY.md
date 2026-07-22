# 🎙️ Registro Canônico de Vozes Oficiais — AcademIA Nexus

**Nexus Affil'IA'te · MMN_IA · 2026**
**Status:** Onda 50 (2026-07-22)
**Mantido em:** `personas/voice_registry/`

Este é o **contrato permanente de voz** dos personas da AcademIA. Todos os scripts TTS, pipelines de áudio e gerações de vídeo DEVEM referenciar estes arquivos canônicos em vez de voice IDs genéricos.

---

## 🎭 Personas e Vozes Oficiais

### Sra. Nexus Ive (Matriarca, Estrategista)

| Atributo | Valor |
|----------|-------|
| **Arquivo canônico** | `personas/ive/audio/official_voice.wav` |
| **Caminho absoluto (repo)** | `AcademIA/personas/ive/audio/official_voice.wav` |
| **URL GitHub** | https://github.com/Nexus-HUB57/Academ-IA/tree/main/personas/ive/audio |
| **Duração** | 31.28s |
| **Sample rate** | 24000 Hz |
| **Canais** | 1 (mono) |
| **Bit depth** | 16-bit PCM |
| **Codec** | pcm_s16le (WAV) |
| **Tamanho** | 1.5 MB (1,501,484 bytes) |
| **MD5** | `073d4964d3de3713f0349731dd3bf683` |
| **Alias fonte** | `ive_amostra_1.wav` (conforme `identity.md`) |
| **Tom** | Serena, articulada, sotaque sulista leve, rouquidão suave |
| **Trilhas** | Fundamental (acolhedora) · Agente (instrutiva) · Master (estratégica) · Elite (parceria) |

### Sir. Nexus Alencar (Mentor Técnico)

| Atributo | Valor |
|----------|-------|
| **Arquivo canônico** | `personas/alencar/audio/official_voice.wav` |
| **Caminho absoluto (repo)** | `AcademIA/personas/alencar/audio/official_voice.wav` |
| **URL GitHub** | https://github.com/Nexus-HUB57/Academ-IA/tree/main/personas/alencar/audio |
| **Alias histórico (mesmo conteúdo)** | `personas/alencar/voz_sir_nexus_alencar.wav` |
| **Duração** | 29.16s |
| **Sample rate** | 24000 Hz |
| **Canais** | 1 (mono) |
| **Bit depth** | 16-bit PCM |
| **Codec** | pcm_s16le (WAV) |
| **Tamanho** | 1.4 MB (1,399,724 bytes) |
| **MD5** | `9f1cbd7aaef82b70f8972e4dc7374eba` |
| **Alias fonte** | `alencar_amostra_1.wav` (conforme `identity.md`) |
| **Tom** | Maduro, sereno, didático, autoridade intelectual, judaico sereno |
| **Trilhas** | Fundamental (passo a passo) · Agente (direto) · Master (analítico) · Elite (técnico profundo) |

### Dupla (Ive + Alencar)

| Atributo | Valor |
|----------|-------|
| **Voz Ive** | `personas/ive/audio/official_voice.wav` |
| **Voz Alencar** | `personas/alencar/audio/official_voice.wav` |
| **Diretrizes** | `personas/dupla/interaction_guidelines.md` |
| **Guia** | `personas/dupla/guia-dupla-nexus.md` |
| **Módulos onde atua** | 00 (boas-vindas) · 03 (painel) · 08 (otimização) · 09 (funis) · 12 (blueprints) · 14 (federação) |

---

## 🚫 Vozes Genéricas Proibidas em Produção

Até que a clonagem oficial de voz esteja validada em CI, **NÃO** usar:

| Voice ID Genérico | Motivo |
|-------------------|--------|
| `Portuguese_CharmingQueen` | Voz pública genérica, sem assinatura das personas |
| `Portuguese_Steadymentor` | Voz pública genérica, sem assinatura das personas |

> **Histórico:** A Onda 49 usou estas vozes genéricas como fallback. A Onda 50+ deve usar exclusivamente as vozes oficiais clonadas a partir dos WAVs acima (ou voice IDs clonados via `clone_voice` quando disponível).

---

## 🔄 Pipeline de Uso

### 1. Clonagem (executar uma vez)

```bash
# Upload do WAV oficial
file_id_ive=$(upload_clone_audio("personas/ive/audio/official_voice.wav"))
file_id_alencar=$(upload_clone_audio("personas/alencar/audio/official_voice.wav"))

# Clone (gera voice_id custom + preview)
voice_id_ive=$(clone_voice(file_id_ive, voice_id="sra_nexus_ive_v1"))
voice_id_alencar=$(clone_voice(file_id_alencar, voice_id="sir_nexus_alencar_v1"))
```

> **Status atual (2026-07-22):** O serviço `clone_voice` está retornando `voice_id=(empty)`. Pivô pendente até normalização. Em Onda 50, registrar IDs clonados aqui.

### 2. Geração de áudio TTS

```python
# Em vídeos/scripts/roteiros_parsed.json
"voice_ive": "sra_nexus_ive_v1"        # ou Portuguese_CharmingQueen (fallback)
"voice_alencar": "sir_nexus_alencar_v1"  # ou Portuguese_Steadymentor (fallback)
```

```python
# Em batch_synthesize_speech
requests = [
  {"text": "...", "output_file_path": "...", "voice_id": voice_ive},
  {"text": "...", "output_file_path": "...", "voice_id": voice_alencar},
]
```

### 3. Renderização de vídeo

```bash
ffmpeg -y \
  -f concat -safe 0 -i videos/frames/full_XX_list.txt \
  -i videos/audio/full_XX_persona.wav \
  -c:v libx264 -preset ultrafast -crf 23 \
  -pix_fmt yuv420p -r 25 \
  -c:a aac -b:a 192k \
  -shortest -movflags +faststart \
  videos/video-XX-{slug}-full.mp4
```

---

## 📋 Checklist de Validação por Voz

Ao produzir novo material de áudio, validar:

- [ ] `voice_id` é uma das vozes oficiais clonadas (ou fallback documentado)
- [ ] Arquivo gerado tem 24 kHz, mono, 16-bit PCM
- [ ] Duração coerente com tamanho do texto (~150-200 chars/min para PT-BR)
- [ ] Tom da persona respeitado (ver `voice_guidelines.md` da persona)
- [ ] Sem ruído de fundo, sem clipping, sem cortes abruptos
- [ ] Áudio referenciado em `videos/audio/full_XX_persona.wav`

---

## 🔗 Referências Cruzadas

| Documento | Caminho |
|-----------|---------|
| Identity Ive | `personas/ive/identity.md` |
| Identity Alencar | `personas/alencar/identity.md` |
| Diretrizes de voz Ive | `personas/ive/voice_guidelines.md` |
| Diretrizes de interação Dupla | `personas/dupla/interaction_guidelines.md` |
| Guia Dupla | `personas/dupla/guia-dupla-nexus.md` |
| Padrão de produção de vídeos | `producao/PADRAO_VIDEOS_ACADEMIA.md` |
| Catálogo de módulos | `producao/catalog/CATALOGO_MODULOS.md` |

---

## 📊 Histórico de Versões

| Versão | Data | Mudança |
|--------|------|---------|
| **1.0.0** | 2026-07-22 | Criação do registro. Documenta WAVs oficiais Ive + Alencar. Marca `Portuguese_CharmingQueen`/`Portuguese_Steadymentor` como proibidos em produção. Pivô: aguardar normalização de `clone_voice`. |

---

*Academ-IA · MMN AI-to-AI · Nexus HUB57 · 2026 · Onda 50*
