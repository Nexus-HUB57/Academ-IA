---
title: "Prompt 07 · Diagnóstico Completo de Produto"
subtitle: "Framework para análise 360° de produto digital com IA"
author: "Equipo Nexus · Niko (CEO/AI) + Sra. Nexus Ive"
version: "1.0.0"
date: 2026-08-04
pattern: "MMN_IA"
---

**Prompt 07 · Diagnóstico Completo de Produto**

*Prompt estruturado para diagnosticar 360° de um produto digital: market fit, UX, monetização, growth, operação, e riscos. Use antes de pivotar, levantar, ou escalar.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 Quando Usar Este Prompt

✅ **Use quando:**
- Antes de pivotar (precisa entender o que mudar)
- Antes de levantar rodada (mostrar tração + gaps)
- Antes de escalar (validar se fundação aguenta)
- Trimestralmente (revisão de saúde)
- Quando produto "não está performando" sem causa clara

❌ **Não use quando:**
- Produto está performando bem (não mexe)
- Você quer validar ideia (use pesquisa de mercado)
- Pré-MVP (não tem dados para analisar)

---

## 📋 O Prompt

```markdown
# Diagnóstico Completo de Produto

Você é um Product Strategy Expert com 15 anos de experiência em SaaS B2B e B2C.
Faça um diagnóstico 360° do produto abaixo, identificando:

1. Estado atual (métricas, sinais)
2. Problemas críticos (P0)
3. Oportunidades de alto impacto
4. Riscos e sinais de alerta
5. Plano de ação priorizado (próximos 90 dias)

## PRODUTO

**Nome:** [Nome do produto]
**Categoria:** [SaaS, e-commerce, marketplace, infoproduto, etc]
**Stage:** [Pre-PMF, PMF, Scale, Mature]
**Pricing:** [R$ X/mês ou one-time]

**Target Customer (ICP):**
- Quem: [persona]
- Tamanho do mercado: [TAM, SAM, SOM]
- Alternativas: [concorrentes principais]

## MÉTRICAS ATUAIS (últimos 90 dias)

| Métrica | Valor | Tendência |
|---------|-------|-----------|
| MAU | __ | ↑↓→ |
| DAU/MAU | __ | ↑↓→ |
| Conversão | __% | ↑↓→ |
| ARPU | R$ __ | ↑↓→ |
| Churn mensal | __% | ↑↓→ |
| LTV | R$ __ | ↑↓→ |
| CAC | R$ __ | ↑↓→ |
| LTV/CAC | __x | ↑↓→ |
| NPS | __ | ↑↓→ |
| Payback | __ meses | ↑↓→ |
| Magic Number | __ | ↑↓→ |

## DADOS ADICIONAIS

**Top 3 conquistas (últimos 90 dias):**
1. ___
2. ___
3. ___

**Top 3 frustrações (últimos 90 dias):**
1. ___
2. ___
3. ___

**Features lançadas:** ___
**Features canceladas:** ___
**Bugs críticos (P0):** ___

**Concorrentes que estão crescendo:** ___
**Concorrentes que estão morrendo:** ___

**Feedback recente de clientes (verbatim, 3-5 quotes):**
1. "___" — [user]
2. "___" — [user]
3. "___" — [user]

**Hipótese principal do problema:** ___

## FORMATO DE SAÍDA

Analise cada uma das 8 dimensões abaixo:

### 1. Market & Positioning
- [Análise do mercado]
- [Posicionamento atual vs ideal]
- [Sinais de product-market fit]

### 2. Value Proposition
- [Clareza do valor]
- [Diferenciação vs concorrentes]
- [Job to be done]

### 3. Pricing & Monetização
- [Análise de pricing]
- [LTV/CAC ratio]
- [Willigness to pay]

### 4. Aquisição & Growth
- [Canais funcionando]
- [Funil de conversão]
- [CAC por canal]
- [Viral coefficient]

### 5. Retenção & Engagement
- [Cohort retention]
- [DAU/MAU]
- [Churn reasons]
- [Feature adoption]

### 6. UX & Produto
- [UX flows problemáticos]
- [Features subutilizadas]
- [Onboarding]
- [Caminhos de sucesso]

### 7. Operação & Time
- [Velocidade de desenvolvimento]
- [Qualidade (bugs, uptime)]
- [Suporte ao cliente]
- [Tech debt]

### 8. Riscos & Sinais de Alerta
- [Riscos críticos]
- [Sinais de alerta]
- [Mitigações]

## PRIORIZAÇÃO

Liste as TOP 5 ações para os próximos 90 dias, ordenadas por impacto:

| # | Ação | Impacto | Esforço | Owner | Métrica de sucesso |
|---|------|---------|---------|-------|---------------------|
| 1 | __ | Alto/Médio/Baixo | __ | __ | __ |
| 2 | __ | | | | |
| 3 | __ | | | | |
| 4 | __ | | | | |
| 5 | __ | | | | |

## RECOMENDAÇÃO FINAL

Em 1 parágrafo: qual é o diagnóstico principal e o que fazer AGORA?
```

---

## 🛠️ Como Usar

### Uso 1: Diagnóstico Trimestral

```python
"""
Rodar diagnóstico todo trimestre.
"""
from openai import OpenAI

client = OpenAI()

prompt = open("prompt_diagnostico_produto.md").read()
produto_data = {
    "nome": "Nexus Agent Platform",
    "categoria": "SaaS B2B",
    "stage": "Scale",
    "pricing": "R$ 497/mês",
    "metricas": {...},
    "conquistas": [...],
    "frustracoes": [...],
    "feedback": [...],
}

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Produto: {produto_data}"},
    ],
    max_tokens=4000,
)

diagnostico = response.choices[0].message.content
print(diagnostico)
```

### Uso 2: Análise de Feature Específica

```python
"""
Variante: diagnóstico de feature.
"""
prompt_feature = """
Você é um Product Analyst. Analise a feature abaixo e dê recomendação GO/NO-GO/KILL.

**Feature:** [Nome]
**Objetivo:** [O que deveria fazer]
**Métricas atuais:**
- Adoção: X% dos usuários
- Retenção: Y% continuam usando após 7 dias
- NPS: Z

**Decisão:**
- GO: investir mais
- NO-GO: não expandir, manter como está
- KILL: remover

**Justificativa + próximos passos.**
"""
```

### Uso 3: Antes de Pivotar

```python
"""
Variante: análise pré-pivot.
"""
prompt_pivot = """
Analise se vale a pena pivotar o produto abaixo.

**Produto atual:** [descrição]
**Por que considerar pivot:** [motivo]
**3 opções de pivot consideradas:**
1. [Opção A]
2. [Opção B]
3. [Opção C]

**Analise:**
- Custo de pivot vs continuar
- Risco de cada opção
- Tempo até validação
- Recomendação final
"""
```

---

## 📊 Exemplo de Output

**Input:**
```
Produto: Nexus Agent Platform (SaaS B2B)
Stage: Scale (3 anos, R$ 80k MRR, 200 clientes)
Pricing: R$ 497/mês
Métricas: LTV/CAC 1.8x, churn 8%, NPS 32
Frustrações: CAC alto, churn de Pro tier
```

**Output (resumido):**

### 1. Market & Positioning
- Mercado B2B de IA agents é crescente (30% a.a.)
- Positioning atual: "Plataforma de agentes" (genérico)
- **PMF fraco:** LTV/CAC 1.8x é apertado, NPS 32 é OK mas não excelente
- **Sinal de alerta:** Churn de 8%/mês é alto para B2B (target: < 3%)

### 2. Value Proposition
- Clientes não veem valor claro de "agentes" (muito abstrato)
- Concorrente [X] foca em "ROI mensurável" e cresce mais rápido
- **Recomendação:** Reposicionar para "Automação que paga por si mesma" com ROI claro

### 3. Pricing & Monetização
- R$ 497/mês é médio para B2B
- CAC de R$ 800+ torna payback 5+ meses (alto)
- **Oportunidade:** Pricing baseado em uso (por agente) pode aumentar LTV

### 4-8 [...]

### TOP 5 Ações (próximos 90 dias)

| # | Ação | Impacto | Esforço | Métrica |
|---|------|---------|---------|---------|
| 1 | Reposicionar marketing para "ROI mensurável" | Alto | Médio | NPS > 50 |
| 2 | Implementar feature de ROI tracking | Alto | Alto | Churn < 5% |
| 3 | Testar pricing por uso | Médio | Médio | LTV/CAC > 3x |
| 4 | Programa de customer success dedicado | Alto | Médio | Churn Pro < 3% |
| 5 | Análise de coortes (entender churn) | Médio | Baixo | - |

### Recomendação Final

Produto tem tração mas tem sinais de alerta. Priorizar 1) reposicionamento de marketing (baixo custo, alto impacto), 2) feature de ROI (alto esforço, alto impacto), 3) programa de CS (médio esforço, alto impacto). Considerar pivot de pricing nos próximos 6 meses se LTV/CAC não melhorar.

---

## 💡 Dicas de Uso

### 1. Seja Honesto nos Dados
- Não infle números para parecer melhor
- Inclua problemas, não só sucessos
- "Mentir" para o LLM = diagnóstico errado

### 2. Itere com o Diagnóstico
- Rode o prompt 2-3 vezes
- Compare outputs
- Use para discussão com time

### 3. Combine com Pesquisa Qualitativa
- LLM analisa números
- Humano complementa com entrevistas
- Melhor diagnóstico vem dos dois

### 4. Documente Decisões
- Após diagnóstico, documente ações tomadas
- Compare 90 dias depois
- Aprenda com o passado

### 5. Use Antes de Investimentos Grandes
- Levantar rodada? Diagnóstico antes.
- Contratar 5 pessoas? Diagnóstico antes.
- Pivot? Diagnóstico antes.

---

## 📚 Materiais Complementares

- `Lab-Nexus/prompts/analise/01-analise-coorte-churn.md` — coorte
- `Lab-Nexus/prompts/analise/02-analise-funil-conversao.md` — funil
- `Lab-Nexus/prompts/analise/03-diagnostico-funil-completo.md` — funil
- `Lab-Nexus/prompts/analise/05-analise-concorrencia-profund.md` — concorrência
- `Lab-Nexus/prompts/analise/06-forecast-receita-trimestral.md` — forecast
- `playbooks/PB-PRODUTO-lancamento-beta-fechado.md` — beta
- `treinamentos/WS-09-oficina-marketing-conversacional.md` — marketing
- `apostilas/48-design-thinking-ia.md` — design thinking

---

## 🔗 Links Externos

- Lenny's Newsletter: https://www.lennysnewsletter.com/
- Reforge: https://www.reforge.com/
- ProductPlan: https://www.productplan.com/
- Mind the Product: https://www.mindtheproduct.com/

---

*AcademIA · Prompt 07 · Diagnóstico Completo de Produto · 2026*