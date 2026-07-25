# Manifesto Operacional do Rebuild — Vídeo-Aulas 00-14

**Data:** 2026-07-24

## Estrutura canônica criada
- Workspace principal: `materiais/video-aulas`
- Organização por trilha > módulo > tipos de material (capas, slides, roteiros, áudios, vídeos, publicação, curso).
- Cada pasta de módulo contém links canônicos para os arquivos reais já existentes no repositório.

## Modelos aprovados
- Abertura visual: `kling/v3`
- Narração: `fal-ai/minimax/speech-2.8-hd`

## Duração-alvo por vídeo
- **00 · Boas-vindas à AcademIA Nexus** → **75s** · persona `alencar`
- **01 · Entendendo o IOAID** → **90s** · persona `ive`
- **02 · O Sistema SHO (Self-Healing Orchestrator)** → **95s** · persona `alencar`
- **03 · Painel do Afiliado — Visão Geral da Operação** → **105s** · persona `dupla`
- **04 · Construindo Seu Primeiro Agente em 4 Minutos** → **90s** · persona `alencar`
- **05 · Skills Essenciais — Copywriter + Audience-Segmenter** → **95s** · persona `alencar`
- **06 · Disparando no WhatsApp em Escala** → **100s** · persona `alencar`
- **07 · Judge Revisor — A IA que Decide por Você** → **105s** · persona `alencar`
- **08 · Otimização de Conversão — A Matemática da Receita** → **135s** · persona `dupla`
- **09 · Funis e Lifecycle — O Sistema Completo** → **145s** · persona `dupla`
- **10 · A/B Testing com Judge — Ciência da Experimentação** → **145s** · persona `dupla`
- **11 · Análise de Coortes e Churn — A Arte de Reter** → **150s** · persona `dupla`
- **12 · Blueprints Elite — O Jogo do Top 10%** → **155s** · persona `dupla`
- **13 · Multi-Tenant e White-Label na Prática** → **160s** · persona `alencar`
- **14 · Federação de Agentes Zero-Trust** → **165s** · persona `dupla`

## Naming final
- Áudio novo: `rebuild_{code}_narracao_ptbr.wav`
- Abertura: `video-{code}-opening.mp4`
- Master final: `video-{code}-{slug}-master.mp4`

## Handoff operacional
- Reusar capa oficial e thumb aprovados a partir de `producao/assets/thumbnails`.
- Reusar slides e roteiros já existentes como base do rebuild.
- Gerar nova narração na duração-alvo e sincronizar com 5-10 slides.
- Publicação só após aprovação humana do novo master.
