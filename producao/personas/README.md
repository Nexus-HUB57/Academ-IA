---
title: "Personas · Produção · AcademIA"
description: "Documentação canônica das personas (Alencar + Ive) para uso em produção"
tags: [personas, producao, alencar, ive, oficial, canon]
last_updated: 2026-07-26
---

# 🎙️ Personas · Produção · AcademIA

> **Documentação canônica** das personas oficiais para uso em produção (vídeos, TTS, voice-cloning, narrações).

## 📍 Fonte Canônica

A documentação canônica das personas **NÃO está aqui**. Está em `marca/personas/`:

- **Alencar**: `marca/personas/alencar/sir_nexus_alencar.md`
- **Ive**: `marca/personas/ive/sra_nexus_ive.md`

Este diretório `producao/personas/` é um **mirror via symlinks** para preservar a referência histórica do antigo `MMN_AI-to-AI/AcademIA/producao/personas/`.

## 🔗 Symlinks

| Arquivo (este dir) | Aponta para |
|---|---|
| `sir_nexus_alencar.md` | `marca/personas/alencar/sir_nexus_alencar.md` |
| `sra_nexus_ive.md` | `marca/personas/ive/sra_nexus_ive.md` |

## 🎯 Estrutura de Personas (Localização Final)

```
Academ-IA/marca/personas/
├── OFFICIAL_VOICES.md            # Sumário de vozes oficiais
├── VOICES.md                     # Detalhamento de vozes
├── VOZES-OFICIAIS.md             # PT-BR
├── alencar/                      # Persona Sir Nexus Alencar
│   ├── identity.md
│   ├── sir_nexus_alencar.md      # Ficha técnica completa
│   ├── roteiro-aula01.md
│   ├── slides-aula01.md
│   ├── audio/                    # Arquivos WAV oficiais
│   └── assets/                   # Imagens de referência
├── ive/                          # Persona Lady Nexus Ive
│   ├── identity.md
│   ├── sra_nexus_ive.md          # Ficha técnica completa
│   ├── voice_guidelines.md
│   ├── audio/                    # Arquivos WAV oficiais
│   └── assets/
├── dupla/                        # Interação entre Alencar + Ive
│   ├── guia-dupla-nexus.md
│   └── interaction_guidelines.md
└── voice_registry/               # Registro canônico de vozes
    ├── OFFICIAL_VOICES_REGISTRY.md
    └── voice_resolver.py
```

## 📝 Histórico de Migração

- **2026-06-15**: Arquivos originais em `MMN_AI-to-AI/AcademIA/producao/personas/`
- **2026-07-22**: Migração para `Academ-IA/marca/personas/` (consolidação com marca)
- **2026-07-26**: Symlinks criados em `producao/personas/` para preservar referência histórica

## ✅ Por que symlinks e não duplicação?

1. **Single source of truth**: atualização em `marca/personas/` propaga automaticamente
2. **Zero duplicação**: evita inconsistências entre versões
3. **Compatibilidade**: links antigos `producao/personas/sir_nexus_alencar.md` continuam funcionando
4. **Auditoria**: caminho de referência preservado para git blame e diff histórico

---

**Versão 1.0** · Criado em 2026-07-26 · Mavis Agent
