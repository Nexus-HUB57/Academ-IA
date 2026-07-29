---
title: "Prompt — Ad Creative Matrix (12 Variações para Anúncios)"
description: "Prompt para gerar 12 variações de criativos de anúncios pagos em matriz de gancho + formato"
tags: [lab-nexus, prompt, copywriting, ads, paid-traffic, meta, google, tiktok]
category: prompts/copywriting
level: avancado
author: "Equipe Nexus"
version: "1.0"
last_review: "2026-07-22"
---

# 📢 Prompt — Ad Creative Matrix (12 Variações para Anúncios)

Prompt canônico para gerar **matriz de 12 criativos publicitários** combinando **4 ganchos × 3 formatos**. Cada combinação vira um criativo testável em Meta/Google/TikTok. Baseado em framework de **teste multivariado rápido**.

## 🎯 Quando usar

- Antes de escalar campanha paga.
- Em testes A/B de criativos.
- Para saturar funil de topo (TOFU).
- Quando ROAS cai por fadiga de criativo.
- Para diversificar portfólio de anúncios.

## 📋 Variáveis de Entrada

```yaml
produto: "Nome do produto"
publico: "Persona"
promessa: "Benefício principal"
objecao: "Maior dúvida antes de comprar"
plataforma: "meta | google | tiktok | linkedin"
budget_teste: "Valor em R$ para testar (ex: R$ 1000)"
objetivo: "awareness | consideration | conversion"
tom: "urgente | aspiracional | educativo | polêmico"
```

## 📦 Prompt Pronto

```text
# PAPEL
Você é media buyer sênior, especialista em criativos de alta performance.
Domina Meta Ads, Google Ads, TikTok Ads, e padrões de algoritmo 2026.
Calibrado em +10.000 criativos analisados.

# OBJETIVO
Gerar uma MATRIZ de 12 criativos, combinando:
- 4 GANCHOS (ângulos de copy)
- 3 FORMATOS (image, video, carousel)
Total: 12 variações testáveis.

# INPUTS
Produto: {{produto}}
Público: {{publico}}
Promessa: {{promessa}}
Objeção: {{objecao}}
Plataforma: {{plataforma}}
Budget de teste: {{budget_teste}}
Objetivo: {{objetivo}}
Tom: {{tom}}

# 4 GANCHOS A TESTAR

1. GANCHO "DOR" — chamar atenção pelo problema
   - "Você está perdendo X sem perceber"
   - "O erro que 90% das pessoas cometem"
   - Foco: identificação imediata

2. GANCHO "PROVA" — credibilidade imediata
   - "Como Maria saiu de 0 para R$50k/mês"
   - "O método usado por X clientes"
   - Foco: autoridade + curiosidade

3. GANCHO "CURIOSIDADE" — lacuna de informação
   - "Descobri o segredo que ninguém conta"
   - "O que X não te disse sobre Y"
   - Foco: gap que precisa ser fechado

4. GANCHO "OFERTA" — direto, sem rodeio
   - "R$ X por Y (apenas 48h)"
   - "Bônus exclusivo para os primeiros 100"
   - Foco: escassez + urgência

# 3 FORMATOS A TESTAR

**FORMATO A — Imagem estática**
- 1080x1080 ou 1080x1350
- Texto grande (max 30% da imagem)
- Headline + subhead + CTA
- 1 produto/benefício por imagem

**FORMATO B — Vídeo curto (15-30s)**
- Vertical 9:16
- Hook visual nos primeiros 3s
- Texto na tela sempre
- CTA verbal + visual

**FORMATO C — Carrossel (3-5 slides)**
- Cada slide = 1 ideia
- Slide 1 = gancho forte
- Slide final = CTA
- Útil para educação + conversão

# REGRAS OBRIGATÓRIAS
- Headline ≤ 10 palavras
- Subhead ≤ 20 palavras
- CTA claro e único
- LGPD-safe (sem promessas absolutas)
- Texto na tela em vídeos
- Trilha trending em vídeos
- Variação REAL entre os 12 (não é mesmo copy com cor diferente)

# FORMATO DE SAÍDA
Tabela markdown com 12 linhas (4 ganchos × 3 formatos).
Cada linha: headline, subhead, cta, visual_notes, copy_video
```

## 💡 Exemplo de Saída (4 das 12 linhas)

**Input:**
```
Produto: Curso "Funil Lucrativo"
Público: afiliada 25-35, classe B
Promessa: Escalar para R$ 30k/mês
Objeção: "Não tenho tempo"
Plataforma: meta
Objetivo: consideration
```

**Output:**

| # | Gancho | Formato | Headline | Subhead | CTA | Visual/Video |
|---|--------|---------|----------|---------|-----|--------------|
| 1 | DOR | Imagem | "Você trabalha 14h/dia e fatura R$3k" | "Descobri o erro que prende você nesse ciclo" | "Veja o método" | Foto de mulher exausta, expressão cansada, fundo desfocado |
| 2 | DOR | Vídeo | "Você não tem tempo. Eu também não tinha." | "Hoje fature R$35k trabalhando 5h/dia. O que mudou?" | "Assista até o fim" | Texto: "Eu trabalhava 14h..." → corte → "Hoje trabalho 5h" |
| 3 | DOR | Carrossel | "5 erros que prendem você em R$3k/mês" | "Slide 1: erro #1 — copiar o que não funciona" | "Salva esse post" | 5 slides, cada um com 1 erro + solução rápida |
| 4 | PROVA | Imagem | "Maria saiu de 0 para R$50k/mês" | "Com o método Funil Lucrativo, em 6 meses" | "Quero saber como" | Antes/depois (mockup): R$0 vs R$50k, datas |
| 5 | PROVA | Vídeo | "12 alunas já passaram de R$30k/mês" | "Cada uma com a sua história. Veja 3 depoimentos reais." | "Assista o vídeo completo" | 3 cortes rápidos, cada um com uma aluna |
| ... | ... | ... | ... | ... | ... | ... |

## 📊 Estratégia de Teste

### Fase 1 — Smoke Test (R$ 50-100 total)

- Distribuir R$ 8-10 por criativo nos 12.
- Rodar 48h.
- Critério: **Hook Rate > 30%** (3s view rate).
- Cortar fundo: piores 8.

### Fase 2 — Mid Test (R$ 500-1000)

- Top 4 sobreviventes.
- R$ 125-250 cada.
- Rodar 5 dias.
- Critério: **CTR > 1.5%**, **CPC < R$1**.
- Cortar fundo: 2 piores.

### Fase 3 — Scale (R$ 5000+)

- Top 2 finalistas.
- Escalar budget em 20% ao dia se ROAS > 2.
- Pausar se ROAS cai abaixo de 1.5 por 2 dias seguidos.

## 📊 Métricas-Chave

| Métrica | Target |
|---------|--------|
| **Hook Rate** | >30% |
| **CTR** | >1.5% (Meta), >2% (Google), >1% (TikTok) |
| **CPC** | <R$1.50 |
| **CPM** | <R$30 |
| **ROAS** | >2 (mínimo), >4 (alvo) |
| **Frequency** | <3 (saturação) |

## ⚠️ Erros Comuns

- ❌ 12 criativos com o MESMO gancho (não dá pra aprender nada)
- ❌ Variação só de cor/imagem (copy igual)
- ❌ Budget distribuído igualmente (testes enviesados)
- ❌ Cortar cedo demais (sem volume estatístico)
- ❌ Escalar criativo que tem bom CTR mas ROAS ruim
- ❌ Não rotacionar criativos (fadiga após 7-14 dias)

## 🔗 Próximos Prompts

- → `03-cta-persuasivo.md` — testar 8 CTAs
- → `01-headline-persuasiva.md` — headlines para os ganchos
- → `11-reels-script-viral.md` — versão orgânica dos criativos

---

*Versão 1.0 · Atualizado 2026-07-22 · Mantido pela Equipe Nexus*
