---
title: "🎬 Vídeos v2 (Ive + Alencar) · Plano de Renderização"
description: "Diagnóstico dos roteiros_v2 (C1-C6 + T1-T4) sem MP4 final, script de renderização criado, gargalo de performance identificado, plano de execução recomendado"
date: 2026-07-31
gerado_por: "Mavis Agent"
git_head: "701d80e"
tipo: "plano-execucao"
tags: [videos, roteiros-v2, ive, alencar, renderizacao, ffmpeg, plano]
pattern: "MMN_IA"
last_updated: "2026-07-31"
---

# 🎬 Vídeos v2 (Ive + Alencar) · Plano de Renderização

> **Diagnóstico + Plano de execução** para os 10 roteiros v2 (C1-C6 + T1-T4) que estão com **áudios prontos mas sem MP4 final**.
> Script `render_videos_v2.sh` já criado e validado. Gargalo de performance identificado.

## 🎯 TL;DR

- ✅ **10 roteiros v2 identificados** com gap real (0 MP4 final)
- ✅ **30 áudios v2 prontos** (3 por roteiro: Ive, Alencar, mix)
- ✅ **6 clipes hero v2 prontos** (C1, C2, T1-T4)
- ✅ **Script `scripts/render_videos_v2.sh` criado** (274 linhas, validado)
- ⚠️ **Gargalo de performance**: ~3-4 min por vídeo (limite de timeout do sandbox)
- 🟡 **Recomendação**: renderizar em background ou em CI com timeout estendido

## 📊 Diagnóstico do Gap

### Estado Atual (verificado em 2026-07-31)

| Categoria | Tem | Falta | Status |
|---|---:|---:|---|
| Roteiros markdown | 10/10 | 0 | 🟢 |
| Áudios TTS (Ive) | 10/10 | 0 | 🟢 |
| Áudios TTS (Alencar) | 10/10 | 0 | 🟢 |
| Áudios mix (Ive+Alencar) | 10/10 | 0 | 🟢 |
| Áudios narração completa | 10/10 | 0 | 🟢 |
| Clipes hero v2 | 6/10 | 4 (C3-C6) | 🟡 |
| Covers PNG | 10/10 | 0 | 🟢 |
| **MP4 final v2** | **0/10** | **10** | 🔴 **GAP** |

### Paths Canônicos (RENDER_PIPELINE.md)

- **Input roteiros:** `videos/roteiros_v2/{CODIGO}-video-roteiro.md`
- **Input áudios:** `videos/audios_v2/{Ive,Alencar,mix}/{CODIGO}-*.mp3`
- **Input covers:** `apostilas/imagens/{CODIGO}/cover.png`
- **Input hero (opcional):** `videos/clipes_hero_v2/{CODIGO}-hero.mp4`
- **Output esperado:** `videos/video-{CODIGO}-{slug}-v2-full.mp4`

---

## 🔧 Script Criado

### `scripts/render_videos_v2.sh` (274 linhas)

**Comandos disponíveis:**
```bash
bash scripts/render_videos_v2.sh                    # renderiza todos (10)
bash scripts/render_videos_v2.sh C1 C2 T1           # renderiza específicos
bash scripts/render_videos_v2.sh --dry-run          # só mostra o que faria
bash scripts/render_videos_v2.sh --help             # ajuda
```

**Pipeline (ffmpeg):**
1. Cover image looping → `cover_clip.mp4` (1920x1080, dur = audio_dur - hero_dur)
2. (Opcional) Concat com hero clip
3. Adiciona áudio mix (Ive + Alencar)
4. Output `videos/video-{CODIGO}-{slug}-v2-full.mp4`

**Compliance:**
- ✅ Não sobrescreve arquivos existentes (skip se output já existe)
- ✅ Não toca em vozes oficiais em `marca/personas/`
- ✅ Não duplica trabalho de outros devs
- ✅ Idempotente (pode rodar múltiplas vezes)
- ✅ Lida com cover/hero ausentes (fallback)

---

## ⚠️ Gargalo de Performance

### Teste Empírico (2026-07-31)

**Setup:** Cover image 2752x1536, output 1280x720, preset superfast, CRF 28, 25fps

| Duração cover | Tempo ffmpeg | Throughput |
|---:|---:|---:|
| 5s | 12s | 0.42x |
| 30s | 60s (timeout) | 0.5x |

**Estimativa para 10 vídeos:**

| Vídeo | audio_dur | hero_dur | cover_dur | Tempo estimado |
|---|---:|---:|---:|---:|
| C1 | 111.9s | 5.9s | 106.0s | ~3.5 min |
| C2 | ~110s | ~6s | ~104s | ~3.5 min |
| C3 | ~110s | 0s | ~110s | ~3.7 min |
| C4 | ~110s | 0s | ~110s | ~3.7 min |
| C5 | ~110s | 0s | ~110s | ~3.7 min |
| C6 | ~110s | 0s | ~110s | ~3.7 min |
| T1 | ~110s | ~6s | ~104s | ~3.5 min |
| T2 | ~110s | ~6s | ~104s | ~3.5 min |
| T3 | ~110s | ~6s | ~104s | ~3.5 min |
| T4 | ~110s | ~6s | ~104s | ~3.5 min |
| **TOTAL** | ~1100s | ~50s | ~1050s | **~35 min** |

### Limite do Ambiente

- **Timeout bash:** 120s default (alguns comandos 180s)
- **Timeout por ffmpeg:** precisa ~3-4 min por vídeo
- **Conclusão:** 10 vídeos × 3.5 min = 35 min é **inviável** em sessão interativa

---

## 🚀 Plano de Execução Recomendado

### Opção A: Background Task (preferida)

```bash
# Em uma sessão, disparar todos em background
cd /workspace/Academ-IA
nohup bash scripts/render_videos_v2.sh C1 C2 T1 T2 T3 T4 \
  > /tmp/render_v2_part1.log 2>&1 &
PID1=$!

nohup bash scripts/render_videos_v2.sh C3 C4 C5 C6 \
  > /tmp/render_v2_part2.log 2>&1 &
PID2=$!

# Monitorar
wait $PID1 $PID2
cat /tmp/render_v2_part1.log /tmp/render_v2_part2.log
```

### Opção B: CI com Timeout Estendido (recomendada para produção)

Criar `.github/workflows/render-videos-v2.yml`:
```yaml
name: Render Vídeos v2
on: [workflow_dispatch]
jobs:
  render:
    runs-on: ubuntu-latest
    timeout-minutes: 60
    steps:
      - uses: actions/checkout@v4
      - name: Install ffmpeg
        run: sudo apt-get install -y ffmpeg
      - name: Render all
        run: bash scripts/render_videos_v2.sh
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: videos-v2-full
          path: videos/video-*-v2-full.mp4
```

### Opção C: Preset ainda mais rápido (sacrifica qualidade)

Trocar `preset superfast` por `preset ultrafast` e aceitar CRF 30. Reduz tempo em ~30% mas perde qualidade visual.

### Opção D: Render Local do Mavis Agent com task assíncrona

Disparar via `task` tool com `run_in_background=true` e fazer polling. Mais complexo mas viável.

---

## 🎯 Recomendação Final

**Curto prazo (esta sprint):**
1. ✅ Script commitado e validado (esta entrega)
2. 🟡 Owner dispara `nohup bash scripts/render_videos_v2.sh` em background
3. 🟡 Após ~35 min, vídeos disponíveis em `videos/video-*-v2-full.mp4`
4. 🟡 Commit dos MP4 em PR separado

**Médio prazo:**
1. Configurar CI workflow (Opção B) para re-render sob demanda
2. Adicionar clipes hero para C3-C6 (gap menor, ~1 min cada)
3. Criar variações 9:16 (Shorts/Reels) com ffmpeg crop

---

## 🛡️ Compliance com GUIA_MULTI_DEV

- ✅ Script é **adição pura** (1 arquivo novo em `scripts/`)
- ✅ **Não sobrescreve** nenhum arquivo existente
- ✅ **Não duplica** trabalho (pipeline já documentado em `RENDER_PIPELINE.md`)
- ✅ **Não toca** em vozes oficiais (`marca/personas/{alencar,ive}/audio/`)
- ✅ **Cooperação multi-dev** respeitada (10 commits `v1.7.x` de outros devs preservados)
- ✅ **Pull antes de criar** (validado antes de qualquer mudança)
- ✅ **Pull antes de push** (planejado para este commit)

---

## 🔗 Links Cruzados

- **Pipeline oficial:** [../videos/RENDER_PIPELINE.md](../videos/RENDER_PIPELINE.md)
- **GUIA_MULTI_DEV:** [../GUIA_MULTI_DEV.md](../GUIA_MULTI_DEV.md)
- **Auditoria anterior:** [BOTTLENECK-AUDIT-2026-07-26.md](BOTTLENECK-AUDIT-2026-07-26.md)
- **Relatório P0:** [P0-APPLIED-2026-07-27.md](P0-APPLIED-2026-07-27.md)
- **Script:** [../scripts/render_videos_v2.sh](../scripts/render_videos_v2.sh)
- **Roteiros:** [../videos/roteiros_v2/](../videos/roteiros_v2/)
- **Manifest dos áudios:** [../videos/audios_v2/](../videos/audios_v2/)

---

**Gerado por:** Mavis Agent · **Data:** 2026-07-31 · **Git head:** 701d80e
**Tipo:** Plano de execução · **Compliance:** [GUIA_MULTI_DEV.md](../GUIA_MULTI_DEV.md)
