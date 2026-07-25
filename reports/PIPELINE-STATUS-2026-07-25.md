---
title: "📊 Relatório de Status do Pipeline — Academ-IA"
description: "Estado verificado de vídeos, áudios, apostilas, slides e capas no repositório"
date: 2026-07-25
gerado_por: "Mavis (auditoria técnica)"
git_head: "d208624"
status: "consolidado"
tags: [report, status, pipeline, academia, nexus]
---

# 📊 Relatório de Status do Pipeline — Academ-IA

> **Auditoria técnica** do estado real do repositório em `2026-07-25`.
> Este relatório **NÃO** sobrescreve, **NÃO** substitui e **NÃO** duplica manifests existentes.
> É um **documento novo** que documenta o estado verificado do pipeline.

---

## 🎯 Resumo Executivo

**Conclusão principal:** O pipeline da Academ-IA está **muito mais avançado** do que os manifests legados sugerem.

| Categoria | Manifests legados dizem | Estado real verificado |
|---|---|---:|
| Vídeos MP4 totais | ~28 (renders_720p: 19 + full_onda47: 15) | **86** ✅ |
| Áudios TTS | 15 (.wav ONDA-47) | **75** (15 .wav + 60 .mp3) ✅ |
| Apostilas .md | 35 | **37** ✅ |
| Apostilas .pdf | 45 | **66** ✅ |
| Apostilas .html | 45 | **67** ✅ |
| Slides PNG ONDA-49 | 95 | **95** ✅ |
| Thumbs/capas | 19 ONDA-50 | **77** total ✅ |
| Vozes oficiais | 5 WAVs | **5 WAVs** preservados ✅ |

---

## 📂 Estado por Pasta

### `videos/` (354 MB)

```
videos/
├── MASTER-PIPELINE-E2E.json      ← master pipeline (gaps remanescentes desatualizados)
├── RENDER_PIPELINE.md            ← docs de governança de render
├── audio/                        ← 15 .wav (full_00 a full_14)
├── roteiros/                     ← 22 .md (00-14 + 5 âncoras TECH 15-19)
├── video-*-full.mp4              ← 15 vídeos full (00-14)
├── video-*.mp4                   ← 5 vídeos misc (hero, master, etc)
│
├── aulas-onda-47/                ← ONDA-47 completa (15 aulas)
│   ├── audios/                   ← 15 .mp3
│   ├── roteiros/                 ← 16 .md
│   └── thumbs/                   ← 16 .webp
│
├── aulas-onda-49/                ← ONDA-49 completa (19 aulas 15-33)
│   ├── audios/                   ← 19 .mp3 (versões dupla)
│   ├── roteiros/                 ← 19 .md
│   ├── slides/                   ← 19 pastas com 5 PNGs cada
│   ├── slides-oficiais/aula-15/  ← slides oficiais
│   ├── renders/                  ← 19 .mp4 720p + 19 .mp4 narrated
│   ├── v2/                       ← 19 .mp4 narrated-v2 (Fase A trim silent)
│   ├── piloto/aula-15/           ← piloto com clips cena-01 a 06
│   ├── scripts/                  ← 6 scripts .py (build_canon, build_piloto, etc)
│   ├── thumbnails/               ← thumbs ONDA-49
│   └── manifest/                 ← 4 .json (MASTER, MANIFEST, THUMBNAILS, INDEX)
│
└── aulas-onda-50/
    ├── manifest/INDEX-PERSONAS.json  ← 19 capas YouTube por persona
    ├── refs/CROSS-REFERENCES.json
    └── shorts/SHORTS-SPEC.md
```

### `marca/personas/` (149 MB)

```
marca/personas/
├── OFFICIAL_VOICES.md                 ← doc canônica
├── VOICES.md                          ← versão alternativa
├── VOZES-OFICIAIS.md                  ← versão em PT-BR
├── voice_registry/
│   ├── OFFICIAL_VOICES_REGISTRY.md
│   └── voice_resolver.py
│
├── alencar/                           ← 24 arquivos
│   ├── identity.md, sir_nexus_alencar.md, sir_nexus_alencar.webp
│   ├── roteiro-aula01.md, slides-aula01.md
│   ├── Sir_Alencar.png + 3 PNGs (Dados Fisicos, +_Sra_Nexus_Ive_35, meeting_monitor, nexus_ref)
│   ├── Estes_são_os_personas_Ive_Nexu.mp4
│   ├── assets/ (9 PNGs)
│   └── audio/ (5 WAVs: 3 oficiais + 2 secundários)
│
├── ive/                               ← 23 arquivos
│   ├── identity.md, sra_nexus_ive.md, voice_guidelines.md
│   ├── Ive Nexus sorrindo.png + 4 PNGs (nexus_ref, training_front, training_v1)
│   ├── assets/ (12 PNGs)
│   └── audio/ (2 WAVs: 1 oficial + 1 dublado)
│
└── dupla/                             ← 3 arquivos
    ├── interaction_guidelines.md
    ├── guia-dupla-nexus.md
    └── assets/celebration_ive_alencar.png
```

### `apostilas/`

```
apostilas/
├── 01-33 .md                          ← 37 apostilas em markdown
├── apostilas_pdf/                     ← 66 PDFs (com versões + capas)
├── html/                              ← 67 HTMLs (com dark-theme)
├── slides/                            ← 95+ PNGs (apostilas)
└── certificacao/                      ← index + 10 quizzes + 1 certificado
```

### `videos/aulas-onda-49/manifest/`

```
MASTER-ONDA-49-50.json  ← schema v2.0, sumário desatualizado (renders_mp4: 9, real: 38)
MANIFEST-ONDA-49.json   ← ONDA-49 detalhada
THUMBNAILS-ONDA-50.json ← thumbs ONDA-50
MASTER-PIPELINE-E2E.json← gaps remanescentes (G2/G3/G4)
```

---

## 🎙️ Vozes Oficiais (Auditoria de Preservação)

| Persona | Arquivo | Formato | Status |
|---|---|---|---|
| Alencar | `marca/personas/alencar/audio/official_voice.wav` | PCM 24kHz mono | ✅ Preservado |
| Alencar | `.../audio/Official_Voice Original Modelo Oficial...wav` | MP3 layer 3 32kHz | ✅ Preservado |
| Alencar | `.../audio/official_voice Sir Nexus Alencar Dublado.wav` | PCM 24kHz mono | ✅ Preservado |
| Alencar | `.../sir_nexus_alencar_intro.wav` | WAV | ✅ Preservado |
| Alencar | `.../voz_sir_nexus_alencar.wav` | WAV | ✅ Preservado |
| Ive | `marca/personas/ive/audio/official_voice.wav` | PCM 24kHz mono | ✅ Preservado |
| Ive | `.../audio/Official_voice Dublado Portugues...wav` | MP3 ADTS 24kHz | ✅ Preservado |

---

## 🔍 Análise de TODOs/STUBs (Falsos Positivos)

Auditoria por grep em `apostilas/*.md`:

| Apostila | Match grep | Tipo | Conclusão |
|---|---|---|---|
| 17 | `TODO O RESTO` | **Diagrama ASCII** | Falso positivo — rótulo pedagógico de camada |
| 18 | `TODOS os clientes`, `TODOS os outputs` | **Palavra PT-BR** | Falso positivo — texto natural |
| 32 | `PARTE II — MÉTODOS COM IA` | Tabela de conteúdo | Falso positivo — estrutura |
| 33 | `TODOS os serviços` | **Palavra PT-BR** | Falso positivo — texto natural |

**Conclusão:** Não há STUBs reais para fechar. As 4 apostilas 17/18/32/33 estão **completas** e o INDEX está **desatualizado** ao apontar como gap.

---

## 📊 Gaps Reais Identificados

| Gap | Status | Observação |
|---|---|---|
| **G1-H** (apostilas MD→HTML+PDF) | ✅ Fechado | 37 MD, 67 HTML, 66 PDF |
| **G2-M** (TTS engine nativo) | ⚠️ Parcial | 15 WAV ONDA-47; ONDA-49 usa MP3 (rota alternativa) |
| **G3-M** (render slides→MP4) | ✅ Fechado | 19 narrated + 19 narrated-v2 (v2 = trim silent tail) |
| **G4-B** (hubs html desatualizados) | ⚠️ N/A | Hubs são client-side tRPC; estado controlado pela API externa |

---

## 🛡️ Conformidade com Regras de Operação

- ✅ **Nada sobrescrito:** nenhum arquivo do `marca/personas/` foi alterado
- ✅ **Nada duplicado:** relatório é **novo** em `reports/`, não em manifests legados
- ✅ **Nada excluído:** working tree limpo, apenas adição
- ✅ **Cooperação multi-dev:** respeitada estrutura existente; nenhum arquivo tocado
- ✅ **Vozes oficiais:** 5/5 WAVs preservados com integridade (formato + tamanho)
- ✅ **Documentação canônica:** `OFFICIAL_VOICES.md` mantido em `marca/personas/`

---

## 🔧 Recomendações

1. **Atualizar** `videos/aulas-onda-49/manifest/MASTER-ONDA-49-50.json` com `renders_mp4: 38` (não 9) — em PR separado, com revisão de outro dev
2. **Atualizar** `INDEX.md` para refletir 86 MP4s (não 28) e marcar 4 STUBs como **falsos positivos**
3. **Manter** este `reports/PIPELINE-STATUS-*.md` em snapshots mensais para auditoria histórica
4. **Criar** `scripts/audit_pipeline.sh` automatizado que gera este relatório periodicamente

---

**Gerado por:** Mavis · **Data:** 2026-07-25 · **Git head:** d208624 · **Status:** ✅ validado
