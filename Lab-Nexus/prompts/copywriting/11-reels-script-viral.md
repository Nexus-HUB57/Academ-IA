---
title: "Prompt — Reels Script Viral (60 segundos)"
description: "Prompt para gerar scripts de Reels/TikTok otimizados para retenção e viralização"
tags: [lab-nexus, prompt, copywriting, reels, tiktok, instagram, viral]
category: prompts/copywriting
level: intermediario
author: "Equipe Nexus"
version: "1.0"
last_review: "2026-07-22"
---

# 🎬 Prompt — Reels Script Viral (60 segundos)

Prompt canônico para gerar **scripts de Reels/TikTok/Shorts de 60 segundos** com estrutura de **retenção progressiva** (gancho, tensão, virada, CTA). Baseado em benchmark de 1.000+ vídeos com >100k views.

## 🎯 Quando usar

- Antes de gravar Reels/TikTok/Shorts.
- Em testes A/B de ganchos (hook).
- Para produtos com público jovem (18-35).
- Para conteúdo viral/awareness.
- Em trends (adaptando para o produto).

## 📋 Variáveis de Entrada

```yaml
produto: "Nome do produto"
publico: "Persona (idade, interesse, dor)"
promessa: "Benefício principal em 1 frase"
objecao: "Maior dúvida antes de comprar"
plataforma: "instagram | tiktok | youtube_shorts | kwai"
tom: "humor | polêmica | curiosidade | inspirador | direto"
duracao: 60  # segundos
tendência_atual: "Trend do momento (opcional)"
```

## 📦 Prompt Pronto

```text
# PAPEL
Você é roteirista especialista em vídeos curtos virais, com benchmark em
1.000+ vídeos de >100k views. Domina estrutura de retenção, ganchos
psicológicos, e padrões de algoritmo Instagram/TikTok.

# OBJETIVO
Gerar 3 variantes de script para Reels de 60 segundos, cada uma com
estrutura de retenção progressiva: gancho (0-3s) → tensão (3-45s) →
virada (45-55s) → CTA (55-60s).

# INPUTS
Produto: {{produto}}
Público: {{publico}}
Promessa: {{promessa}}
Objeção: {{objecao}}
Plataforma: {{plataforma}}
Tom: {{tom}}
Duração: {{duracao}}s
Tendência: {{tendencia_atual}}

# ESTRUTURA — 60 SEGUNDOS

**FASE 1 — GANCHO (0-3 segundos)**
- Primeira frase visual + sonora
- Estratégia: interrupção de padrão, pergunta provocativa, ou afirmação absurda
- Retenção alvo: 70% dos viewers passam dos 3s
- Use CAPS para ênfase visual
- 1 frase apenas, max 15 palavras

**FASE 2 — TENSÃO (3-45 segundos)**
- Setup do problema / curiosidade
- 3-5 frases curtas (max 10 palavras cada)
- Visual: cortes rápidos, texto na tela, mudança de ângulo a cada 5-7s
- Trilha: trending sound ou música com batida
- Use "você" para falar diretamente com o viewer

**FASE 3 — VIRADA (45-55 segundos)**
- O momento de revelação / quebra de expectativa
- 2-3 frases
- Visual: zoom in, mudança de iluminação, ênfase
- Prova concreta (número, nome, demonstração)

**FASE 4 — CTA (55-60 segundos)**
- Chamada à ação clara
- "Link na bio", "Comenta X", "Salva esse post"
- 1 frase, max 10 palavras
- Sempre entregar valor ANTES de pedir ação

# REGRAS OBRIGATÓRIAS
- Texto na tela em TODAS as frases (acessibilidade + retenção)
- Cortes a cada 3-7 segundos (ritmo)
- Trilha SEMPRE trending ou original
- Legenda embutida no vídeo
- LGPD-safe (sem promessas absolutas)
- Zero "compre agora" agressivo
- Valor ANTES de CTA

# FORMATO DE SAÍDA
Markdown estruturado por variante, com marcações de tempo e visual.
```

## 💡 Exemplo de Saída

**Input:**
```
Produto: Curso "Corte Viral"
Público: afiliada iniciante, 25-35
Promessa: Vídeos que viralizam em 7 dias
Objeção: "Não tenho tempo de gravar"
Plataforma: instagram
Tom: curiosidade
```

**Output (Variante 1):**

```markdown
## Variante 1 — "O Erro de 3 Segundos"

### FASE 1 — GANCHO (0-3s)
🎥 VISUAL: Close no rosto, olhos arregalados, texto: "VOCÊ PERDE 70% DOS VIEWERS EM 3 SEGUNDOS"
🎙️ VOZ: "Se você tá perdendo gente no primeiro segundo do seu Reels, é por causa disso."

### FASE 2 — TENSÃO (3-45s)
🎥 VISUAL: Cortes rápidos, mostrando exemplos de hooks bons vs ruins
🎙️ VOZ: "Eu analisei 500 Reels. 70% cometem o MESMO erro no gancho. Começam com 'Oi gente, eu sou a Maria'. EM 1.5 SEGUNDOS, a pessoa já saiu. Sabe por quê? Porque ninguém liga pra você em 1.5s. As pessoas ligam pra ELAS MESMAS. Então o gancho tem que ser sobre o VIEWER, não sobre você. 'Você tá perdendo dinheiro sem saber'. ISSO é um gancho. 'Descobri o segredo que ninguém te conta'. ISSO é um gancho. Você tem 3 segundos pra fazer a pessoa ficar OU sair pra sempre."

### FASE 3 — VIRADA (45-55s)
🎥 VISUAL: Zoom in, mostrando a tela com 1M de views
🎙️ VOZ: "Apliquei isso num Reels semana passada. 1.2 milhão de views. Em 7 dias. Sem gastar 1 real com ads."

### FASE 4 — CTA (55-60s)
🎥 VISUAL: Tela final com o nome do curso
🎙️ VOZ: "Quer os 7 hooks que eu uso? Comenta 'HOOK' aqui que eu mando no privado."
```

## 📊 Métricas Esperadas

| Métrica | Target |
|---------|--------|
| **Retenção 3s** | >70% |
| **Retenção 50%** | >35% |
| **Watch time médio** | >40s |
| **Engagement rate** | >5% |
| **Shares** | >2% dos views |

## ⚠️ Erros Comuns

- ❌ Gancho fraco (cumprimento, saudação longa, "oi gente")
- ❌ Visual estático (sem cortes)
- ❌ Sem texto na tela (perde 80% dos viewers sem som)
- ❌ Trilha genérica (não trending)
- ❌ CTA agressivo ("COMPRA AGORA!")
- ❌ Sem virada clara (apenas setup sem payoff)

## 🔗 Próximos Prompts

- → `10-sequencia-email-nurture.md` — converter Reels em sequência de e-mail
- → `08-copy-headline-anuncio.md` — testar Reels como ads

---

*Versão 1.0 · Atualizado 2026-07-22 · Mantido pela Equipe Nexus*
