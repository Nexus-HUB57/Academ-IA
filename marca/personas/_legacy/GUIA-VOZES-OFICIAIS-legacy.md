# 🎙️ Guia das Vozes Oficiais · AcademIA

> ⚠️ **DOCUMENTO DE ENTRADA RÁPIDA** — Para detalhes completos, consulte:
> - `marca/personas/VOZES-OFICIAIS.md` (guia operacional)
> - `marca/personas/OFFICIAL_VOICES.md` (descrição detalhada)
> - `marca/personas/voice_registry/OFFICIAL_VOICES_REGISTRY.md` (contrato)
> - `marca/personas/voice_registry/voice_resolver.py` (script Python)

---

## 🎯 TL;DR

**As vozes oficiais são IMUTÁVEIS e devem ser usadas em TODA produção de áudio/vídeo.**

| Persona | Arquivo canônico | URL GitHub |
|---------|------------------|------------|
| **Sir Nexus Alencar** | `marca/personas/alencar/audio/official_voice.wav` | [link](https://github.com/Nexus-HUB57/Academ-IA/tree/main/marca/personas/alencar/audio) |
| **Lady Nexus Ive** | `marca/personas/ive/audio/official_voice.wav` | [link](https://github.com/Nexus-HUB57/Academ-IA/tree/main/marca/personas/ive/audio) |

**MD5 canônico (validar antes de usar):**
- Alencar: `9f1cbd7aaef82b70f8972e4dc7374eba`
- Ive: `073d4964d3de3713f0349731dd3bf683`

---

## 🚀 Como Usar em 30 Segundos

### Python (resolver dinâmico)

```python
import sys
sys.path.insert(0, '/workspace/Academ-IA/marca/personas/voice_registry')
from voice_resolver import get_voice_id, verify_official_wavs

# Verificar integridade dos WAVs
status = verify_official_wavs()
print(status['ive']['ok'])     # True
print(status['alencar']['ok']) # True

# Obter voice_id (após configurar CLONE_IDs)
import os
os.environ['IVE_CLONE_ID'] = 'sua_ive_clone_id'
os.environ['ALENCAR_CLONE_ID'] = 'sua_alencar_clone_id'
voice_id = get_voice_id('alencar')
```

### TTS direto (MiniMax Platform)

```python
synthesize_speech(
    text="Olá, eu sou Sir. Nexus Alencar...",
    output_file_path="output.wav",
    voice_id="alencar_cloned_v1",  # configurado via clone_voice
    speed=0.9  # Alencar fala mais pausado
)
```

### Verificação manual

```bash
# Validar integridade
cd /workspace/Academ-IA
md5sum marca/personas/alencar/audio/official_voice.wav
# Esperado: 9f1cbd7aaef82b70f8972e4dc7374eba

md5sum marca/personas/ive/audio/official_voice.wav
# Esperado: 073d4964d3de3713f0349731dd3bf683
```

---

## 📂 Onde Está Cada Coisa

```
Academ-IA/
├── GUIA-VOZES-OFICIAIS.md                ← ESTE ARQUIVO (entrada rápida)
│
├── marca/personas/
│   ├── VOZES-OFICIAIS.md                  ← Guia operacional (procedimentos)
│   ├── OFFICIAL_VOICES.md                 ← Descrição detalhada das vozes
│   │
│   ├── alencar/
│   │   ├── identity.md
│   │   ├── sir_nexus_alencar.md           ← Ficha canônica
│   │   ├── sir_nexus_alencar_intro.wav
│   │   └── audio/
│   │       ├── official_voice.wav         ← 🎙️ VOZ OFICIAL PRINCIPAL
│   │       ├── "Official_Voice Original Modelo Oficial Voz Sir Nexus Alencar.wav"
│   │       └── "official_voice Sir Nexus Alencar Dublado.wav"
│   │
│   ├── ive/
│   │   ├── identity.md
│   │   ├── voice_guidelines.md
│   │   └── audio/
│   │       ├── official_voice.wav         ← 🎙️ VOZ OFICIAL PRINCIPAL
│   │       └── "Official_voice Dublado Portugues Modelo Oficial Voz Lady Ive Nexus.wav"
│   │
│   ├── dupla/
│   │   ├── interaction_guidelines.md
│   │   └── guia-dupla-nexus.md
│   │
│   └── voice_registry/
│       ├── OFFICIAL_VOICES_REGISTRY.md    ← Contrato permanente
│       └── voice_resolver.py              ← Script Python para resolver
│
└── (antigamente em personas/ — MOVIDO para marca/personas/)
```

---

## ✅ Regras de Ouro

1. **SEMPRE use `marca/personas/{persona}/audio/official_voice.wav`** como sample
2. **NUNCA use voz genérica** (Google TTS, Polly, etc) para essas personas
3. **SEMPRE valide o MD5** antes de clonar (verificar integridade)
4. **SEMPRE documente** no `VOZES-OFICIAIS.md` se criar nova versão
5. **NUNCA modifique** pitch/velocidade sem documentar
6. **SEMPRE referencie** este guia em PRs de produção de áudio/vídeo

---

## 🔄 Pipeline Típico

```
1. Conferir MD5 dos samples oficiais
        ↓
2. Upload via upload_clone_audio()
        ↓
3. clone_voice(file_id, voice_id="alencar_v1")
        ↓
4. Configurar env var: ALENCAR_CLONE_ID=sua_id
        ↓
5. Usar get_voice_id("alencar") em todo synthesize_speech
        ↓
6. Validar qualidade do áudio gerado (teste manual)
        ↓
7. Documentar em changelog + CHANGELOG.md
```

---

## 🆘 Problemas Comuns

| Problema | Solução |
|----------|---------|
| MD5 não bate | `git pull` para garantir WAVs atualizados |
| Voice ID retorna fallback | Configurar env vars `IVE_CLONE_ID` e `ALENCAR_CLONE_ID` |
| Voz soa robótica | Sample tem ruído — re-extrair limpo |
| Pitch estranho | Modelo treinado com sample errado |
| Sotaque gringo | Usar modelo multilíngue (XTTS v2) |

---

## 📜 Histórico de Migração

| Data | Evento |
|------|--------|
| 2026-07-22 | Registro canônico criado em `personas/voice_registry/` |
| 2026-07-23 | Migração: `personas/` → `marca/personas/` (consolidação) |
| 2026-07-23 | VOZES-OFICIAIS.md criado em `marca/personas/` |
| 2026-07-23 | voice_resolver.py atualizado para apontar `marca/personas/` |
| 2026-07-23 | MD5 dos WAVs validados: Alencar OK + Ive OK |

---

*AcademIA · Guia Vozes Oficiais · v1.0 · 2026*