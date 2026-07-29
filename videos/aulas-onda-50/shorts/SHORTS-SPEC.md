---
title: "ONDA-50 · YouTube Shorts Spec para aulas 15-33"
version: "1.0"
date: "2026-07-23"
status: "spec-only (não geradas nesta sessão)"
---

# 📱 Especificação YouTube Shorts (1080×1920)

> Versão vertical (9:16) das capas YouTube 16:9 da ONDA-50. Adaptar layout
> mantém a persona canônica mas reorganiza composição para preencher o canvas
> vertical do TikTok / Reels / Shorts.

## 🎨 Especificações técnicas

| Item | Valor |
|---|---|
| Resolução | 1080 × 1920 px |
| Aspect | 9:16 vertical |
| Formato | PNG lossless |
| Modelo | `nano-banana-2` ou `gpt-image-2` |
| Referências visuais | Persona canônica de `/s/PI8rS0VM` (Alencar) + `/s/VEcRp6sP` (Ive) + `/s/IfqERhh1` (Dupla) |
| Texto overlay | Topo 1/3 do canvas, badge ACADEMIA NEXUS no rodapé |
| Background | Heroic/dark com gradiente vertical navy → gold |

## 🧠 Layout vertical (3 faixas)

1. **Topo (0-30%)** → texto temático (visível mesmo em thumbnail pequeno)
2. **Centro (30-70%)** → persona em pose didática
3. **Rodapé (70-100%)** → ícone temático + roadmap visual + badge ACADEMIA NEXUS

## ⏭️ Próxima ação (quando uma janela de budget permitir)

Gerar 19 capas verticais — uma por aula — usando `image_generation` com `aspect_ratio="9:16"` e `image_urls=[referência canônica da persona apropriada]`.

Filenames seriam: `capa-NN-SLUG-PERSONA-shorts.png` em `../aulas-onda-49/thumbnails/`.

## 🚫 Bloqueio atual

Conter o uso de `image_generation` mantendo-se dentro do budget mensal. Esta
spec fica como blueprint — execução é feita em uma rodada posterior a pedido.
