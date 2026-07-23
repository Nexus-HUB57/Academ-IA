---
title: "ONDA-49 · Videoaulas 15-33 · Slides B2 + Renders MP4"
version: "1.0"
date: "2026-07-23"
persona: "dupla (Alencar + Ive)"
hub: "MMN AI-to-AI"
pattern: "MMN_IA · AcademIA · Videoaulas"
---

# 🌊 ONDA-49 · Videoaulas 15-33

**19 videoaulas cobrindo trilhas Fundamental → Master → Elite → Cursos especializados**

> Sucessora natural das Ondas 47/48 (audio-aulas 01-16 do "Curso Universo IA"),
> esta onda adiciona 19 videoaulas visuais premium com slides B2 (1920×1080)
> em navy+gold e renders MP4 720p sincronizados com áudio TTS.

## 📊 Deliverables

| Categoria | Quantidade | Local |
|---|---|---|
| **Roteiros MD** | 19 (aulas 15-33) | `roteiros/aula-NN-SLUG.md` |
| **Slides B2 PNG** | 95 (19 × 5 cenas) | `slides/aula-NN-SLUG/cena-*.png` |
| **Vídeos MP4 720p** | 9 (aulas 17, 26-33) | `renders/aula-NN-SLUG-720p.mp4` |
| **Manifest** | 1 | `manifest/MANIFEST-ONDA-49.json` |
| **Script gerador** | 1 (`gen_slides_b2.py`) | `scripts/` |

## 🎨 Design System

- **Paleta**: Navy `#0A1628` · Gold `#D4AF37` · Cyan `#22D3EE`
- **Fontes**: Inter (900/800/600/400) · JetBrains Mono (700)
- **Slides**: 1920×1080 PNG lossless
- **Vídeos**: 1280×720 @ 25 fps · libx264 crf24 · AAC 96 k

## 🎭 5 cenas por aula

1. **Hero** (10s) — Título grande + ícone temático + trilha + progress bar
2. **Stats** (15s) — 3 cards com números-chave da aula
3. **Cards Framework** (15s) — 4 pilares/conceitos em grid 2×2
4. **Pyramid** (15s) — Hierarquia de maturidade (5 níveis)
5. **CTA** (15s) — Chamada para `oneverso.com.br/academia`

## 📚 Índice das 19 videoaulas

| # | Título | Trilha | Slides | MP4 |
|---|---|---|---|---|
| 15 | Métricas & ROI do Ecossistema | Fundamental | ✅ | ⏳ |
| 16 | Trilha Fundamental IA | Fundamental | ✅ | ⏳ |
| 17 | SEO & Marketing de Conteúdo para IA | Master | ✅ | **✅** |
| 18 | Segurança Ofensiva & Pentest de Agentes | Elite | ✅ | ⏳ |
| 19 | Monetização Avançada em Escala | Master | ✅ | ⏳ |
| 20 | Trilha Elite Engenharia | Elite | ✅ | ⏳ |
| 21 | Trilha Master Arquitetura | Master | ✅ | ⏳ |
| 22 | Trilha Master Mentoria | Master | ✅ | ⏳ |
| 23 | Curso RAG Prático | Curso | ✅ | ⏳ |
| 24 | Curso Agents LangGraph | Curso | ✅ | ⏳ |
| 25 | Curso Prompt Engineering | Curso | ✅ | ⏳ |
| 26 | Curso Vector DB | Curso | ✅ | **✅** |
| 27 | Curso Voice AI | Curso | ✅ | **✅** |
| 28 | Curso Multimodal RAG | Curso | ✅ | **✅** |
| 29 | AI-to-AI Protocol | Fundamental | ✅ | **✅** |
| 30 | Federação Zero-Trust | Fundamental | ✅ | **✅** |
| 31 | Fábrica de Conteúdo IA | Elite | ✅ | **✅** |
| 32 | Pricing IA 2026 | Elite | ✅ | **✅** |
| 33 | Data Stack de Agentes IA | Elite | ✅ | **✅** |

**Total renders prontos**: 9/19 (47%)

## 🎙️ Vozes oficiais

- **Sir Nexus Alencar** → `personas/alencar/audio/official_voice.wav` (masculina, técnica, didática)
- **Lady Nexus Ive** → `personas/ive/audio/official_voice.wav` (feminina, estratégica, acolhedora)

Todos os áudios TTS deste lote foram gerados com essas referências canônicas.
Os áudios das aulas 26-33 usaram MiniMax speech-2.8-hd com pitch-shift no chunk Ive
(voz feminina sintética +6 semitons) — status conhecido, será regenerado com voice-clone
oficial na ONDA-50.

## 📂 Estrutura

```
videos/aulas-onda-49/
├── README.md                         ← este arquivo
├── manifest/
│   └── MANIFEST-ONDA-49.json         ← índice completo com status por aula
├── roteiros/                         ← 19 roteiros MD
│   ├── aula-15-metricas-roi-ecossistema.md
│   └── ... aula-33-data-stack-agentes-ia.md
├── slides/                           ← 19 pastas com 5 slides cada
│   ├── aula-15-metricas-roi-ecossistema/
│   │   ├── cena-01-hero.png
│   │   ├── cena-02-stats.png
│   │   ├── cena-03-cards.png
│   │   ├── cena-04-pyramid.png
│   │   └── cena-05-cta.png
│   └── ...
├── renders/                          ← 9 MP4 720p com áudio TTS
│   ├── aula-17-seo-marketing-conteudo-ia-720p.mp4
│   ├── aula-26-curso-vector-db-720p.mp4
│   └── ...
└── scripts/
    └── gen_slides_b2.py              ← Regenerador Playwright+CSS
```

## 🚀 Regenerar slides do zero

```bash
cd videos/aulas-onda-49/scripts
pip install playwright
python3 -m playwright install chromium
python3 gen_slides_b2.py
```

## ⚠️ Pendências ONDA-50

| Item | Bloqueio | Solução |
|---|---|---|
| 10 renders MP4 restantes | Áudio TTS voice-clone rejeitou schema | `fal-client` Python direto com `FAL_KEY` |
| Capas YouTube 16:9 personalizadas | — | Fluxo `image_generation → UploadFileWrapper` (validado) |
| Voz Ive canônica nos 8 MP4 (#26-33) | Pitch-shift +6 semitons sintético | Voice-clone com sample oficial 2:21 |

---

**Autor**: Nexus AI-to-AI Pipeline · **Hub**: MMN AI-to-AI · **Data**: 2026-07-23
