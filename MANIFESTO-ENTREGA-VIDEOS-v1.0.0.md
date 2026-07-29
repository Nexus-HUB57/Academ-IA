---
title: "MANIFESTO DE ENTREGA — Pipeline de Vídeos Academ-IA"
description: "Artefatos para renderização completa de 19 aulas ONDA-49"
author: "Agente IA PhD — Nexus HUB57"
version: "1.0.0"
date: "2026-07-29"
tags: [videos, render, ffmpeg, tts, frames, thumbnails, pipeline]
---

# 🎬 MANIFESTO DE ENTREGA — Pipeline de Vídeos

> **Data:** 2026-07-29  
> **Por:** Agente IA PhD — Engenharia de Software & Gerenciamento de Núcleos  
> **Base:** Roteiros ONDA-49 (19 aulas, 99 cenas)  
> **Princípio:** Zero alucinação · Fiel aos roteiros · Pronto para produção

---

## 📊 Resumo da Entrega

| Categoria | Quantidade | Descrição |
|---|---|---|
| **Prompts de Frames** | 99 | 1 por cena, baseado no conteúdo visual do roteiro |
| **Scripts TTS** | 19 | 1 por aula, otimizado por persona (Alencar/Dupla) |
| **Scripts Render** | 19 | 1 por aula, ffmpeg completo (1080p + 720p + thumb) |
| **Specs Thumbnails** | 19 | 1 por aula, 2560×1440, prompt de geração |
| **Total de artefatos** | **156** | Todos prontos para produção |

---

## 🎨 Prompts de Frames (99 total)

**Local:** `frame-prompts/aula-{NN}-{slug}-FRAME-PROMPTS.md`

Cada arquivo contém:
- Metadata da aula (trilha, persona, total de cenas)
- 1 prompt de imagem por cena (em inglês, otimizado para IA de imagem)
- Negative prompt padronizado
- Narração associada para referência
- Tipo de layout: `capa_abertura`, `grid_info`, `diagrama`, `conteudo`

**Estilos por trilha:**
- Fundamental: Cyan (#00D4FF) — acolhedor, introdutório
- Agente: Teal (#00BFA5) — prático, hands-on
- Master: Gold (#FFD700) — sofisticado, avançado
- Elite: Purple (#9D4EDD) — intenso, cutting-edge

---

## 🎤 Scripts TTS (19 total)

**Local:** `tts-scripts/tts-aula-{NN}-{slug}.sh`

Configuração por persona:

| Persona | Voz | Speed | Pitch | Estilo |
|---|---|---|---|---|
| Alencar | pt-BR-Neural2-B | 0.95 | -2st | authoritative, calm, educational |
| Dupla | pt-BR-Neural2-C | 1.0 | 0st | energetic, clear, engaging |

Cada script gera arquivos `audio/cena{N}.wav` para todas as cenas da aula.

---

## 🎬 Scripts de Renderização (19 total)

**Local:** `render-scripts/render-aula-{NN}-{slug}.sh`

Pipeline completo por script:
1. **Verificação** — Checa frames PNG e áudios WAV
2. **Render cenas** — ffmpeg com fade-in/fade-out, 1920×1080
3. **Concatenação** — Une todas as cenas em vídeo final
4. **Downscale 720p** — Versão otimizada para mobile
5. **Thumbnail** — Extrai frame do segundo 5 em 2560×1440

**Outputs:**
- `videos/aulas-onda-49/renders/aula-{NN}-{slug}-1080p.mp4`
- `videos/aulas-onda-49/renders/aula-{NN}-{slug}-720p.mp4`
- `videos/aulas-onda-49/thumbnails/thumb-{NN}-{slug}.png`

---

## 🖼️ Especificações de Thumbnails (19 total)

**Local:** `thumbnails-specs/thumb-{NN}-{slug}-SPEC.md`

Cada especificação inclui:
- Layout visual com diagrama ASCII
- Prompt de geração em inglês (otimizado para IA de imagem)
- Checklist de qualidade
- Nome do arquivo de saída

---

## 🚀 Pipeline de Produção Completo

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  ROTEIRO (.md)  │────▶│  PROMPT FRAME   │────▶│  FRAME PNG      │
│  (já existe)    │     │  (gerado aqui)  │     │  (IA de imagem) │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
┌─────────────────┐     ┌─────────────────┐            │
│  NARRAÇÃO       │────▶│  TTS (.wav)     │────────────┤
│  (do roteiro)   │     │  (gcloud TTS)   │            │
└─────────────────┘     └─────────────────┘            │
                                                       ▼
                                              ┌─────────────────┐
                                              │  RENDER ffmpeg  │
                                              │  (script gerado)│
                                              └─────────────────┘
                                                       │
                              ┌────────────────────────┼────────────────────────┐
                              ▼                        ▼                        ▼
                        ┌──────────┐           ┌──────────┐           ┌──────────┐
                        │ 1080p    │           │ 720p     │           │ Thumb    │
                        │ .mp4     │           │ .mp4     │           │ .png     │
                        └──────────┘           └──────────┘           └──────────┘
```

---

## 📋 Checklist de Produção

### Por Aula:
- [ ] Gerar frames PNG (usar prompts em `frame-prompts/`)
- [ ] Gerar áudios WAV (executar script em `tts-scripts/`)
- [ ] Executar render (executar script em `render-scripts/`)
- [ ] Verificar qualidade do vídeo final
- [ ] Fazer upload para CDN
- [ ] Atualizar banco de dados `academia_lessons`

### Após todas as aulas:
- [ ] Atualizar `MASTER-PIPELINE-E2E.json`
- [ ] Atualizar `INDEX.md`
- [ ] Atualizar `CHANGELOG.md` → `[1.7.0]`
- [ ] Merge da branch `dev/materiais-pendentes-on-50`

---

## 📎 Lista de Arquivos

```
Academ-IA-videos/
├── frame-prompts/
│   ├── aula-15-metricas-e-roi-do-ecosistema-ia-FRAME-PROMPTS.md
│   ├── aula-16-trilha-fundamental-de-ia-FRAME-PROMPTS.md
│   ├── aula-17-seo-e-marketing-de-conteudo-para-agentes-ia-FRAME-PROMPTS.md
│   ├── aula-18-seguranca-ofensiva-pentest-com-agentes-ia-FRAME-PROMPTS.md
│   ├── aula-19-monetizacao-avancada-em-escala-FRAME-PROMPTS.md
│   ├── aula-20-trilha-elite-engenharia-de-agentes-FRAME-PROMPTS.md
│   ├── aula-21-trilha-master-arquitetura-de-sistemas-m-FRAME-PROMPTS.md
│   ├── aula-22-trilha-master-mentoria-e-lideranca-tecni-FRAME-PROMPTS.md
│   ├── aula-23-curso-rag-pratico-do-zero-a-producao-FRAME-PROMPTS.md
│   ├── aula-24-curso-agents-com-langgraph-FRAME-PROMPTS.md
│   ├── aula-25-curso-prompt-engineering-avancado-FRAME-PROMPTS.md
│   ├── aula-26-curso-vector-databases-FRAME-PROMPTS.md
│   ├── aula-27-curso-voice-ai-e-tts-FRAME-PROMPTS.md
│   ├── aula-28-curso-multimodal-rag-FRAME-PROMPTS.md
│   ├── aula-29-protocolo-ai-to-ai-FRAME-PROMPTS.md
│   ├── aula-30-federacao-zero-trust-FRAME-PROMPTS.md
│   ├── aula-31-fabrica-de-conteudo-com-ia-FRAME-PROMPTS.md
│   ├── aula-32-pricing-de-produtos-digitais-com-ia-FRAME-PROMPTS.md
│   └── aula-33-data-stack-para-agentes-ia-FRAME-PROMPTS.md
├── tts-scripts/
│   ├── tts-aula-15-metricas-e-roi-do-ecosistema-ia.sh
│   ├── tts-aula-16-trilha-fundamental-de-ia.sh
│   ├── tts-aula-17-seo-e-marketing-de-conteudo-para-agentes-ia.sh
│   ├── tts-aula-18-seguranca-ofensiva-pentest-com-agentes-ia.sh
│   ├── tts-aula-19-monetizacao-avancada-em-escala.sh
│   ├── tts-aula-20-trilha-elite-engenharia-de-agentes.sh
│   ├── tts-aula-21-trilha-master-arquitetura-de-sistemas-m.sh
│   ├── tts-aula-22-trilha-master-mentoria-e-lideranca-tecni.sh
│   ├── tts-aula-23-curso-rag-pratico-do-zero-a-producao.sh
│   ├── tts-aula-24-curso-agents-com-langgraph.sh
│   ├── tts-aula-25-curso-prompt-engineering-avancado.sh
│   ├── tts-aula-26-curso-vector-databases.sh
│   ├── tts-aula-27-curso-voice-ai-e-tts.sh
│   ├── tts-aula-28-curso-multimodal-rag.sh
│   ├── tts-aula-29-protocolo-ai-to-ai.sh
│   ├── tts-aula-30-federacao-zero-trust.sh
│   ├── tts-aula-31-fabrica-de-conteudo-com-ia.sh
│   ├── tts-aula-32-pricing-de-produtos-digitais-com-ia.sh
│   └── tts-aula-33-data-stack-para-agentes-ia.sh
├── render-scripts/
│   ├── render-aula-15-metricas-e-roi-do-ecosistema-ia.sh
│   ├── render-aula-16-trilha-fundamental-de-ia.sh
│   ├── render-aula-17-seo-e-marketing-de-conteudo-para-agentes-ia.sh
│   ├── render-aula-18-seguranca-ofensiva-pentest-com-agentes-ia.sh
│   ├── render-aula-19-monetizacao-avancada-em-escala.sh
│   ├── render-aula-20-trilha-elite-engenharia-de-agentes.sh
│   ├── render-aula-21-trilha-master-arquitetura-de-sistemas-m.sh
│   ├── render-aula-22-trilha-master-mentoria-e-lideranca-tecni.sh
│   ├── render-aula-23-curso-rag-pratico-do-zero-a-producao.sh
│   ├── render-aula-24-curso-agents-com-langgraph.sh
│   ├── render-aula-25-curso-prompt-engineering-avancado.sh
│   ├── render-aula-26-curso-vector-databases.sh
│   ├── render-aula-27-curso-voice-ai-e-tts.sh
│   ├── render-aula-28-curso-multimodal-rag.sh
│   ├── render-aula-29-protocolo-ai-to-ai.sh
│   ├── render-aula-30-federacao-zero-trust.sh
│   ├── render-aula-31-fabrica-de-conteudo-com-ia.sh
│   ├── render-aula-32-pricing-de-produtos-digitais-com-ia.sh
│   └── render-aula-33-data-stack-para-agentes-ia.sh
├── thumbnails-specs/
│   ├── thumb-15-metricas-e-roi-do-ecosistema-ia-SPEC.md
│   ├── thumb-16-trilha-fundamental-de-ia-SPEC.md
│   ├── thumb-17-seo-e-marketing-de-conteudo-para-agentes-ia-SPEC.md
│   ├── thumb-18-seguranca-ofensiva-pentest-com-agentes-ia-SPEC.md
│   ├── thumb-19-monetizacao-avancada-em-escala-SPEC.md
│   ├── thumb-20-trilha-elite-engenharia-de-agentes-SPEC.md
│   ├── thumb-21-trilha-master-arquitetura-de-sistemas-m-SPEC.md
│   ├── thumb-22-trilha-master-mentoria-e-lideranca-tecni-SPEC.md
│   ├── thumb-23-curso-rag-pratico-do-zero-a-producao-SPEC.md
│   ├── thumb-24-curso-agents-com-langgraph-SPEC.md
│   ├── thumb-25-curso-prompt-engineering-avancado-SPEC.md
│   ├── thumb-26-curso-vector-databases-SPEC.md
│   ├── thumb-27-curso-voice-ai-e-tts-SPEC.md
│   ├── thumb-28-curso-multimodal-rag-SPEC.md
│   ├── thumb-29-protocolo-ai-to-ai-SPEC.md
│   ├── thumb-30-federacao-zero-trust-SPEC.md
│   ├── thumb-31-fabrica-de-conteudo-com-ia-SPEC.md
│   ├── thumb-32-pricing-de-produtos-digitais-com-ia-SPEC.md
│   └── thumb-33-data-stack-para-agentes-ia-SPEC.md
└── MANIFESTO-ENTREGA-VIDEOS-v1.0.0.md
```

---

*Manifesto produzido em 2026-07-29 · Nexus HUB57 · Academ'IA v2.0-on-50*  
*Agente IA PhD — Engenharia de Software & Gerenciamento de Núcleos*
