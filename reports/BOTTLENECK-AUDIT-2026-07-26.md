---
title: "🔬 Auditoria Cirúrgica de Gargalos de Produção"
description: "Diagnóstico de gargalos de produção no repositório Academ-IA: tamanho, duplicações, paths legados, oportunidades de otimização"
date: 2026-07-26
gerado_por: "Mavis Agent"
git_head: "f4879f2"
tipo: "auditoria-readonly"
tags: [auditoria, gargalos, producao, otimizacao, repo-health, cirurgia]
pattern: "MMN_IA"
last_updated: "2026-07-26"
---

# 🔬 Auditoria Cirúrgica de Gargalos de Produção

> **Diagnóstico READ-ONLY** (zero modificações). Esta auditoria identifica gargalos de produção e oportunidades de otimização **sem alterar nada**.
> Todas as recomendações são **opcionais** e devem ser coordenadas via PR seguindo `GUIA_MULTI_DEV.md`.

## 🎯 TL;DR — Top 5 Gargalos Críticos

| # | Gargalo | Impacto | Economia estimada | Risco |
|---|---|---|---|---|
| 🔴 1 | **`.git` em 1.1GB** (50% do repo) | `git clone` lento, CI custoso | ~400MB com `git gc` + LFS | Baixo |
| 🔴 2 | **289 MP4s no git** (323MB) | Push/pull pesado | ~280MB com Git LFS | Médio (re-config) |
| 🟠 3 | **`audit_hashes/` commitado** (8.8MB, 103 jpgs) | Poluição do repo | ~8.8MB | Zero (del dedicado) |
| 🟠 4 | **`producao/assets/thumbnails/` 138MB + duplicações internas** | Confusão de fontes | ~50MB | Baixo |
| 🟡 5 | **PDFs legados** (`pdf/` 66MB, `pdfs/` 3.4MB stubs) | 3 fontes do mesmo asset | 60MB após unificação | Médio (decisão) |

**Total estimado de otimização:** **~800MB** (35% do repo).

---

## 📊 1. Tamanho do Repositório

| Componente | Tamanho | % do repo |
|---|---:|---:|
| `.git/` | 1.1 GB | **50.0%** 🔴 |
| `videos/` | 354 MB | 15.7% |
| `marca/` | 149 MB | 6.6% |
| `materiais/` | 147 MB | 6.5% |
| `producao/` | 139 MB | 6.2% |
| `apostilas/` | 111 MB | 4.9% |
| `youtube/` | 88 MB | 3.9% |
| `pdf/` | 66 MB | 2.9% |
| `html/` | 29 MB | 1.3% |
| Outros | ~150 MB | 6.7% |
| **TOTAL** | **~2.2 GB** | 100% |

### 1.1 Análise do `.git/` (50% do repo!)

```
.git/objects/pack/  → 1.1 GB (6 packfiles)
.git/logs/          → 19 KB
.git/refs/          → 15 KB
```

**Comando de diagnóstico:**
```bash
git count-objects -v
# count: 31, size: 140, in-pack: 3850, packs: 6, size-pack: 1.06GB
# prune-packable: 5 (5 objetos podem ser removidos)
```

**Oportunidade imediata:** `git gc --aggressive --prune=now` reduz ~5% (50MB). **Não é destrutivo.**

### 1.2 Binários Rastreados por Extensão

| Extensão | Arquivos | Tamanho | % | Recomendação |
|---|---:|---:|---:|---|
| `.png` | 519 | 466 MB | 21% | Considerar LFS/WebP |
| `.mp4` | 289 | 323 MB | 15% | **Git LFS obrigatório** 🔴 |
| `.pdf` | 166 | 143 MB | 6% | Manter (asset canônico) |
| `.mp3` | 74 | 51 MB | 2% | Git LFS opcional |
| `.wav` | 67 | 40 MB | 2% | **Vozes oficiais em LFS** 🔴 |
| `.webp` | 131 | 35 MB | 2% | OK (já é formato otimizado) |
| `.jpg` | 134 | 13 MB | 1% | OK |
| **Total binário** | **1.380** | **1.07 GB** | **49%** | LFS resolve |

---

## 🔍 2. Duplicações Confirmadas (mesmo hash MD5)

### 2.1 Em `marca/personas/` (12 duplicações detectadas)

| # | Arquivo A | Arquivo B | Persona | Tamanho |
|---|---|---|---|---:|
| 1 | `ive/assets/ive_nexus_ref.png` | `ive/assets/ive_nexus_ref_1.png` | Ive | 4.7MB |
| 2 | `ive/ive_nexus_ref.png` | `ive/assets/ive_nexus_ref_1.png` | Ive | 4.7MB |
| 3 | `alencar/assets/alencar_nexus_ref.png` | `alencar/alencar_nexus_ref.png` | Alencar | 4.7MB |
| 4 | `alencar/assets/alencar_nexus_ref_1.png` | `alencar/alencar_nexus_ref.png` | Alencar | 4.7MB |
| 5 | `alencar/assets/celebration_ive_alencar.png` | `dupla/assets/celebration_ive_alencar.png` | Dupla | 4.3MB |
| 6 | `alencar/assets/alencar_meeting_monitor.png` | `alencar/alencar_meeting_monitor.png` | Alencar | 4.0MB |
| 7 | `alencar/assets/alencar_meeting_v1.png` | `alencar/assets/alencar_meeting_monitor.png` | Alencar | 4.0MB |
| 8 | `ive/assets/ive_training_v1.png` | `ive/assets/ive_training_front.png` | Ive | 4.0MB |
| 9 | `ive/ive_training_front.png` | `ive/assets/ive_training_v1.png` | Ive | 4.0MB |
| 10 | `ive/ive_training_v1.png` | `ive/ive_training_front.png` | Ive | 4.0MB |
| 11 | `ive/assets/celebration_ive_alencar.png` | `dupla/assets/celebration_ive_alencar.png` | Dupla | 4.3MB |
| 12 | `alencar/voz_sir_nexus_alencar.wav` | `alencar/audio/official_voice.wav` | Alencar | ⚠️ **VOZ OFICIAL** |

**Risco:** 🟠 **MÉDIO** — especialmente o item 12 (voz oficial). Qualquer deduplicação aqui precisa de validação dupla (outro dev revisa).

**Recomendação:**
- **NÃO deduplicar vozes oficiais** (item 12) — segurança por redundância é desejável aqui
- **Deduplicar imagens de assets** após decisão de "qual é o canônico" em PR com review

### 2.2 Em `producao/assets/thumbnails/` (9 duplicações internas)

Mesmo arquivo existe como `capa-XX-slug-persona.png` E `thumb-XX-slug.png`:

| # | Capa | Thumbnail |
|---|---|---|
| 1 | `capa-00-boas-vindas-ive.png` | `thumb-00-boas-vindas.png` |
| 2 | `capa-01-entendendo-ioaid-dupla.png` | `thumb-01-ioaid.png` |
| 3 | `capa-02-sistema-sho-dupla.png` | `thumb-02-sho.png` |
| 4 | `capa-03-painel-afiliado-ive.png` | `thumb-03-painel.png` |
| 5 | `capa-04-primeiro-agente-dupla.png` | `thumb-04-primeiro-agente.png` |
| 6 | `capa-05-skills-essenciais-alencar.png` | `thumb-05-skills.png` |
| 7 | `capa-06-disparo-whatsapp-alencar.png` | `thumb-06-disparo.png` |
| 8 | `capa-07-judge-revisor-alencar.png` | `thumb-07-judge.png` |
| 9 | `capa-08-otimizacao-conversao-dupla.png` | `thumb-08-otimizacao.png` |

**Tamanho do `producao/assets/thumbnails/`:** 138MB (99 arquivos, 97 capas/thumbs + 2 audit files)
**Risco:** 🟡 **BAIXO** — decisão editorial: "manter ambos para compatibilidade" vs "escolher canônico"

### 2.3 Em `videos/` (3 duplicações detectadas)

| # | Arquivo A | Arquivo B |
|---|---|---|
| 1 | `video-00-boas-vindas-poc.mp4` | `video-00-boas-vindas.mp4` |
| 2 | `aulas-onda-49/slides-oficiais/aula-15/cena-05-cta.png` | `aulas-onda-49/slides/aula-15-metricas-roi-ecossistema/cena-05-cta.png` |
| 3 | `aulas-onda-49/slides-oficiais/aula-15/capa-oficial.png` | `aulas-onda-49/thumbnails/capa-15-metricas-roi-alencar.png` |

**Risco:** 🟠 **MÉDIO** — PoC pode ser removida após decisão editorial.

### 2.4 Em `videos/aulas-onda-49/piloto/aula-15/audit_hashes/` (103 jpgs, 8.8MB)

**Hash:** muitos arquivos `sec-XX.jpg` têm o **mesmo hash** (até 17 cópias idênticas!)

| Cluster | Tamanho cluster | Cópias |
|---|---:|---:|
| sec-61 a 78 (cluster 1) | ~700KB | 17 cópias idênticas |
| sec-36 a 51 (cluster 2) | ~700KB | 16 cópias idênticas |
| sec-16, 17-23, 25-26 (cluster 3) | ~700KB | 10 cópias idênticas |
| sec-87-94, 79-86, 53-60, 27-34, 95-102, 08-15 | ~700KB | 8 cópias cada |

**Diagnóstico:** Pasta `audit_hashes/` foi usada como **debug de cenas** durante produção. Foi commitada por engano. **Não é asset canônico.**

**Risco:** 🟢 **ZERO** — pasta é claramente de debug, não referenciada em manifests.

---

## 🗂️ 3. Pastas com Paths Suspeitos

### 3.1 `videos/aulas-onda-49/piloto/aula-15/audit_hashes/` 🔴

- **8.8MB, 103 jpgs**
- Pasta de debug, não referenciada em `manifest.json` da aula-15
- Estrutura: `piloto/aula-15/{audios, audit_hashes, clips, slides, list.txt}`
- **Recomendação:** adicionar `**/audit_hashes/` ao `.gitignore` + `git rm -r` em PR

### 3.2 `pdfs/` (74 PDFs, 3.4MB) — Stubs

Tamanhos típicos: 20-80KB (vs `pdf/` que tem 1-16MB, e `apostilas/apostilas_pdf/` que tem ~1MB médio)

**Diagnóstico:** `pdfs/` contém **PDFs stub** (apenas capa). Servem como **placeholder** no site público para evitar 404 enquanto o asset real está em produção.

**Risco:** 🟡 **BAIXO** — decisão editorial sobre quando substituir stubs pelos reais.

### 3.3 `pdf/` (11 PDFs, 66MB) — Versão "full" legada

- 11 PDFs grandes (até 16MB)
- Não referenciados no `INDEX.md` principal
- Provavelmente substituídos por `apostilas/apostilas_pdf/` (45 PDFs, 40MB)
- **Recomendação:** decisão editorial em PR: remover, mover para backup, ou linkar como legado

### 3.4 `videos/aulas-onda-49/slides-oficiais/` vs `slides/`

| Pasta | Tamanho | Status |
|---|---:|---|
| `slides/` (19 aulas × 5 cenas) | 37 MB | 🟢 canônico |
| `slides-oficiais/aula-15/` | 4.3 MB | 🟡 só aula-15 (piloto) |

**Diagnóstico:** `slides-oficiais/` é o piloto da aula-15 que foi validado e então copiado para `slides/aula-15-*/`. A pasta `slides-oficiais/` pode ser **removida** se o piloto já foi consumido.

**Risco:** 🟠 **MÉDIO** — confirmar com dev que fez o rebuild.

### 3.5 `producao/assets/thumbnails/THUMBNAIL_AUDIT_2026-07-23.*` (2 arquivos)

- `THUMBNAIL_AUDIT_2026-07-23.json` + `.md`
- 99 capas/thumbs, 138MB total
- **Diagnóstico:** Audit files são **relatórios de validação** das 99 capas. Útil para auditoria, mas poderia estar em `reports/` (separado de assets).

**Risco:** 🟢 **ZERO** — só realocação de local.

---

## 📈 4. Resumo de Duplicações por Tipo

| Tipo | Duplicações detectadas | Espaço desperdiçado (estimado) | Prioridade |
|---|---:|---:|---|
| **Imagens de personas** | 12 | ~50MB | 🟠 Média |
| **Capas/thumbs YouTube** | 9 | ~30MB | 🟡 Baixa |
| **Vídeos PoC vs Final** | 1 | ~6MB | 🟡 Baixa |
| **Slides oficiais vs slides** | 2 | ~8MB | 🟠 Média |
| **audit_hashes/** | 103 | 8.8MB | 🔴 Alta (zerar) |
| **TOTAL** | **127** | **~103MB** | — |

---

## 🚦 5. Recomendações (em ordem de prioridade)

### P0 — Imediato (zero risco)

1. **Adicionar `**/audit_hashes/` ao `.gitignore`** + `git rm -r --cached videos/aulas-onda-49/piloto/aula-15/audit_hashes/`
   - Economia: **8.8MB**
   - Risco: zero
   - Comando: PR único, aprovação do owner do piloto

2. **Rodar `git gc --aggressive --prune=now`**
   - Economia: **~50MB**
   - Risco: zero (operação de manutenção)
   - Comando: documentação em `governanca/git-maintenance.md`

### P1 — Curto prazo (coordenação multi-dev)

3. **Migrar MP4s e WAVs para Git LFS** (em coordenação com CTO Agent)
   - Economia: **~280MB no .git/**
   - Risco: 🟠 médio (requer re-config de hooks + storage)
   - Comando: setup Git LFS com track de `*.mp4`, `*.wav`, `*.mp3`

4. **Deduplicar `producao/assets/thumbnails/` capa-XX vs thumb-XX**
   - Economia: **~30MB**
   - Risco: 🟡 baixo (decisão editorial: canônico = capa-XX)
   - Comando: PR com revisão do owner de `producao/`

5. **Mover `THUMBNAIL_AUDIT_2026-07-23.*` para `reports/`**
   - Economia: 0 (realocação)
   - Risco: zero
   - Comando: PR simples

### P2 — Médio prazo (decisão estratégica)

6. **Resolver 3 fontes de PDF** (`pdf/` 66MB + `pdfs/` stubs 3.4MB + `apostilas/apostilas_pdf/` 40MB)
   - Economia: **~60MB** (após unificação)
   - Risco: 🟠 médio (decisão: qual é canônico, onde fica legado)
   - Comando: documentação em `docs/PDF-SOURCE-OF-TRUTH.md` + PR

7. **Deduplicar imagens de personas** (`marca/personas/*/alencar_*.png` etc)
   - Economia: **~50MB**
   - Risco: 🟠 médio (NÃO deduplicar vozes oficiais)
   - Comando: PR com revisão dupla + validação visual

8. **Avaliar `videos/aulas-onda-49/slides-oficiais/` (piloto aula-15)**
   - Economia: **~4MB**
   - Risco: 🟠 médio (confirmar que piloto foi consumido)
   - Comando: PR com confirmação do dev que fez o rebuild

---

## 🛡️ 6. Compliance com GUIA_MULTI_DEV

✅ Esta auditoria:
- **NÃO modificou nenhum arquivo** (apenas leitura)
- **NÃO criou arquivos novos** (exceto este relatório em `reports/`)
- **NÃO deletou nada**
- **NÃO sobrescreveu nada**
- **NÃO duplicou nada**

✅ Recomendações:
- **Todas opcionais** e dependem de coordenação multi-dev
- **Cada uma em PR separado** com revisão de outro dev
- **Nenhuma toca em `marca/personas/voice_registry/` ou vozes oficiais**

---

## 🔗 7. Próximas Auditorias Recomendadas

1. **Auditoria de licenciamento** — verificar licenças de PNGs de terceiros
2. **Auditoria de segurança** — verificar que nenhum `.env`, secret ou token está commitado
3. **Auditoria de Manifests** — validar que todos os JSON manifests batem com o filesystem
4. **Auditoria de CI/CD** — verificar se o pipeline de build referencia paths legados

---

**Gerado por:** Mavis Agent · **Data:** 2026-07-26 · **Git head:** f4879f2
**Tipo:** Read-only · **Compliance:** [GUIA_MULTI_DEV.md](../GUIA_MULTI_DEV.md) · [CHANGELOG.md](../CHANGELOG.md)
