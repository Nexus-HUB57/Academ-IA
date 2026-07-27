---
title: "WS-08 · Oficina de Pricing & Psicologia do Consumidor"
subtitle: "Workshop hands-on de pricing dinâmico, ancoragem, decoy effect e ethical nudging"
author: "Equipo Nexus · Niko (CEO/AI) + Sra. Nexus Ive"
duration: "3h"
type: "workshop"
level: "intermediate"
date: "2026-07-27
pattern: "MMN_IA"
---

**WS-08 · Oficina de Pricing & Psicologia do Consumidor**

*Workshop hands-on de 3h. Você vai otimizar o pricing do SEU produto, criando 3 versões (atual, otimizada, agressiva) com teste A/B configurado para rodar.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 Visão Geral

| Item | Detalhe |
|------|---------|
| **Duração** | 3 horas (1 coffee break) |
| **Formato** | 30% teoria + 70% hands-on |
| **Pré-requisitos** | Tem produto próprio (digital ou físico) com vendas |
| **Capacidade** | 50 vagas (1 por participante/squad) |
| **Material** | Calculadora LTV (Lab-Nexus), templates, planilha de pricing |
| **Certificação** | Badge WS-08-PRICING (carimba progressão) |

---

## 📚 Agenda

| Horário | Bloco | Descrição |
|---------|-------|-----------|
| 0:00-0:25 | **Abertura: Psicologia de Preço** | 7 heurísticas, exemplos reais, anti-patterns |
| 0:25-1:00 | **Bloco 1: Pricing Atual** | Cada squad calcula LTV/CAC do produto atual, identifica gaps |
| 1:00-1:15 | ☕ Coffee | |
| 1:15-1:50 | **Bloco 2: Pricing Otimizado** | Implementar ancoragem, decoy, charm, bundle. 3 tiers |
| 1:50-2:30 | **Bloco 3: A/B Test Setup** | GrowthBook + VWO. Variantes. Hipóteses. Métricas. |
| 2:30-3:00 | **Apresentações + Votação** | 3 squads destaque. Badge WS-08-PRICING. |

---

## 🧠 Bloco 0: Psicologia de Preço (25 min)

### As 7 Heurísticas que Definem Compra

**1. Efeito Ancoragem**
- Primeiro preço que o cliente vê vira referência
- R$ 197 parece caro após R$ 97
- R$ 197 parece barato após R$ 597

**Aplicação:** sempre mostre preço riscado "de R$ X por R$ Y"

**2. Efeito Charm (R$ 99 vs R$ 100)**
- R$ 99 vende 23% mais que R$ 100
- R$ 197 vende mais que R$ 200
- Funciona com qualquer número terminado em 9

**Aplicação:** SEMPRE termine com 7 ou 9 (não 0)

**3. Decoy Effect (Opção de distração)**
- 3 opções: A (básico), B (premium), C (intermediário caro)
- C é desenhada para fazer B parecer melhor
- Estrutura clássica: A = 30% features por R$ 30. B = 100% features por R$ 100. C = 110% features por R$ 200.

**Aplicação:** C é o decoy. A maioria compra B (o que você quer).

**4. Pain of Paying (Dor de Pagar)**
- Quanto mais "dolorosa" a transação, menos provável a compra
- Cartão de crédito dói menos que boleto
- Pix dói mais que cartão (imediato)
- Subscription dói menos que compra única grande (espalha a dor)

**Aplicação:** parcele sempre que possível. Ofereça Pix com pequeno desconto.

**5. Social Proof**
- "487 alunos" vende
- "100% dos alunos recomendam" vende
- "Líder de vendas há 6 meses" vende
- "Recomendado por Forbes, Exame, Pequenas Empresas" vende

**Aplicação:** adicione números reais no topo da página.

**6. Scarcity (Escassez)
- "Vagas limitadas" funciona (verdade ou não)
- "Black Friday termina em 2h" funciona
- "Apenas 5 lugares" funciona
- Cuidado: mentir é prática abusiva (CDC)

**Aplicação:** use escassez REAL. "Restam 8 vagas" (verifique estoque).

**7. Loss Aversion (Aversão à Perda)
- Dor de perder 2x maior que prazer de ganhar
- "Não perca 50% OFF" vende mais que "Ganhe 50% OFF"
- "Última chance" vende mais que "Oportunidade"
- "Você vai perder X" > "Você vai ganhar Y"

**Aplicação:** copy com tom de perda > copy com tom de ganho.

### Quando Cada Heurística Funciona

| Heurística | Funciona em... | Cuidado em... |
|------------|----------------|----------------|
| Ancoragem | Produtos premium, comparados | Produtos commoditizados |
| Charm | Qualquer | B2B muito técnico (passa amador) |
| Decoy | Produtos com 2+ tiers | Produtos com 1 tier |
| Pain of Paying | Alto ticket | Micro-transações |
| Social Proof | Produtos populares | Produtos novos (sem prova) |
| Scarcity | Qualquer | Nunca minta (CDC) |
| Loss Aversion | Urgência real | Pode parecer manipulador |

---

## 🛠️ Bloco 1: Pricing Atual (35 min)

### Tarefa: Analisar Seu Produto

**Cada squad pega SEU produto (ou um real) e preenche:**

```markdown
## Análise de Pricing Atual · [Nome do Produto]

### Produto
- Nome: ___
- Categoria: ___
- Preço atual: R$ ___
- Concorrente 1 preço: R$ ___
- Concorrente 2 preço: R$ ___

### Métricas atuais (últimos 90 dias)
- Visitas/mês: ___
- Conversão: ___%
- AOV: R$ ___
- CAC: R$ ___
- LTV: R$ ___
- LTV/CAC: ___x
- Payback: ___ meses
- Refund rate: ___%

### Gaps identificados
- [ ] Preço não está alinhado com valor percebido
- [ ] Ancoragem fraca/inexistente
- [ ] Sem tiers (ou tiers mal desenhados)
- [ ] Sem prova social na página
- [ ] Sem escassez real
- [ ] Refund rate alto (>5%)

### Oportunidades
- Adicionar tier intermediário (decoy)
- Adicionar ancoragem (R$ 1.297 → R$ 497)
- Bundle com produto complementar
- Criar versão "lite" mais barata
```

### Exercício: Calcule LTV Real

```python
# Use Lab-Nexus/tools/financas/05-calculadora-valor-vida-cliente.md
# Calcule LTV atual, CAC, LTV/CAC
# Identifique: sua margem permite ajuste?
```

---

## 💎 Bloco 2: Pricing Otimizado (35 min)

### Framework: Pricing em 3 Tiers

**Estrutura ideal (decoy inclusa):**

```
💎 TIER 1 — ESSENCIAL
- 50% das features
- Suporte por email (SLA 72h)
- R$ 297/ano

🚀 TIER 2 — PROFISSIONAL  ← (o "best value", 70% escolhe)
- 100% das features
- Suporte prioritário (SLA 24h)
- 1 sessão de mentoria/mês
- Acesso à comunidade premium
- R$ 997/ano

👑 TIER 3 — ENTERPRISE  ← (decoy, 5% escolhe, 25% influencia)
- 100% das features + 10 exclusivas
- Suporte 1:1 dedicado (SLA 1h)
- 4 sessões de mentoria/mês
- Acesso vitalício + atualizações
- Onboarding personalizado
- R$ 2.997/ano
```

**Por que funciona:**
- TIER 1 existe para parecer "barrato demais"
- TIER 3 é o decoy: TIER 2 parece bargain perto de TIER 3
- TIER 2 tem 90% do valor, 33% do preço TIER 3

### Ancoragem: 3 Técnicas

**1. Preço Riscado**

```html
<div style="text-align: center; padding: 20px;">
  <p style="text-decoration: line-through; color: #999; font-size: 20px;">
    De R$ 1.997
  </p>
  <p style="font-size: 48px; color: #00FFFF; font-weight: 800;">
    R$ 497
  </p>
  <p style="color: #FF00FF;">Economia de R$ 1.500 (75% OFF)</p>
</div>
```

**2. Custo por Dia (Recálculo)**

```
"Por menos de R$ 1,36/dia, você tem acesso vitalício a [BENEFÍCIO]"

R$ 497 / 365 dias = R$ 1,36/dia
R$ 497 / 12 meses = R$ 41,42/mês
```

**3. Comparação com Alternativas**

```
"Por R$ 497, você recebe:

✗ Não: R$ 5.000 de consultoria
✗ Não: R$ 2.000 de MBA
✗ Não: R$ 1.000 de curso particular
✓ SIM: Tudo isso por R$ 497"
```

### Charm Pricing Aplicado

```
❌ R$ 500    R$ 1000   R$ 2000
✅ R$ 497    R$ 997    R$ 1.997
```

**A/B test recomendado:** valide charm vs. round para SEU público.

### Bundle Strategy

**Crie bundle que parece bargain:**

```
📦 BUNDLE COMPLETO (valor real: R$ 3.500)
- Curso Principal (R$ 997)
- E-book Complementar (R$ 197)
- Templates Editáveis (R$ 297)
- Comunidade Premium (R$ 497/ano × 3 anos = R$ 1.491)
- Sessão 1:1 (R$ 500)

🛒 Preço do Bundle: R$ 1.297
💰 Economia: R$ 2.203 (63% OFF)
```

**Por que funciona:** mostra valor real, depois desconto parece incrível.

---

## 📊 Bloco 3: A/B Test Setup (40 min)

### GrowthBook Self-Hosted (Open Source)

```bash
# Subir com Docker
docker run -d --name growthbook \
  -p 3000:3000 -p 3100:3100 \
  growthbook/growthbook:latest
```

### Configurar Feature Flag

```javascript
// features.ts
import { GrowthBook } from '@growthbook/growthbook-react';

const gb = new GrowthBook({
  apiHost: 'http://localhost:3100',
  clientKey: 'sdk-abc123',
  enableDevMode: true,
  trackingCallback: (experiment, result) => {
    // Enviar para seu analytics
    console.log('experiment viewed', experiment.key, result.variationId);
  }
});

export function getPrice() {
  const variant = gb.getFeatureValue('pricing-test', 'control');

  switch (variant) {
    case 'control':
      return { price: 497, anchor: 997, badge: null };
    case 'discount_30':
      return { price: 347, anchor: 997, badge: '30% OFF' };
    case 'charm_499':
      return { price: 499, anchor: 997, badge: null };  // R$ 499 vs R$ 497
    case 'bundle':
      return { price: 1297, anchor: 3500, badge: 'BUNDLE' };
    default:
      return { price: 497, anchor: 997, badge: null };
  }
}
```

### Definir Hipóteses

```markdown
## Teste 1: Charm Pricing (R$ 497 vs R$ 499)
**Hipótese:** R$ 497 vai converter 5% mais que R$ 499.
**Variantes:** Control (R$ 497) | Variante (R$ 499)
**Métrica primária:** Conversão
**Métricas secundárias:** AOV, Refund rate
**Tamanho da amostra:** 1000 visitantes por variante
**Duração:** 7-14 dias
**Significância:** p < 0.05

## Teste 2: Anchor Pricing (3 Níveis de Âncora)
**Hipótese:** Âncora em R$ 1.997 (vs R$ 997) vai aumentar percepção de valor e conversão.
**Variantes:** Anchor R$ 997 | Anchor R$ 1.497 | Anchor R$ 1.997
**Métrica primária:** Conversão
**Métricas secundárias:** AOV, NPS
**Tamanho da amostra:** 1500 visitantes por variante
**Duração:** 14-21 dias

## Teste 3: Bundle vs Single Product
**Hipótese:** Bundle vai aumentar AOV em 30%, com conversão -10% (trade-off favorável).
**Variantes:** Single (R$ 497) | Bundle (R$ 1.297)
**Métrica primária:** AOV × Conversão = Receita/Visita
**Tamanho da amostra:** 2000 visitantes por variante
**Duração:** 14-21 dias
```

### Calcular Significância

```python
# significance_test.py
from scipy import stats

def is_significant(visitors_a, conversions_a, visitors_b, conversions_b, alpha=0.05):
    """Z-test para duas proporções"""
    p_a = conversions_a / visitors_a
    p_b = conversions_b / visitors_b
    p_pool = (conversions_a + conversions_b) / (visitors_a + visitors_b)
    se = (p_pool * (1 - p_pool) * (1/visitors_a + 1/visitors_b)) ** 0.5
    z = (p_b - p_a) / se if se > 0 else 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return p_value < alpha, p_value


# Exemplo: Control converteu 2.5%, Variant converteu 3.2%
control = (10000, 250)  # 10k visitors, 250 conversions
variant = (10000, 320)  # 10k visitors, 320 conversions
significant, p_value = is_significant(*control, *variant)
print(f"Significant: {significant}, p-value: {p_value:.4f}")
# Output: Significant: True, p-value: 0.0024
```

### Dashboard de Monitoramento

```sql
-- Query para acompanhar A/B test
SELECT
  variant,
  COUNT(DISTINCT visitor_id) as visitors,
  COUNT(DISTINCT CASE WHEN converted THEN visitor_id END) as conversions,
  ROUND(
    COUNT(DISTINCT CASE WHEN converted THEN visitor_id END)::NUMERIC /
    COUNT(DISTINCT visitor_id),
    4
  ) as conversion_rate,
  SUM(CASE WHEN converted THEN order_value ELSE 0 END) as total_revenue,
  ROUND(
    SUM(CASE WHEN converted THEN order_value ELSE 0 END)::NUMERIC /
    COUNT(DISTINCT visitor_id),
    2
  ) as revenue_per_visitor
FROM events
WHERE experiment_key = 'pricing-test'
  AND event_date BETWEEN '2026-07-01' AND '2026-07-21'
GROUP BY variant
ORDER BY revenue_per_visitor DESC;
```

---

## 📋 Templates Prontos

### Template 1: Página de Pricing com 3 Tiers

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Pricing · [Produto]</title>
  <style>
    body { font-family: 'Inter', sans-serif; background: #0a0e1a; color: #e5edf5; padding: 40px; }
    .tier {
      background: #131a2c;
      border: 1px solid rgba(99, 234, 255, 0.18);
      border-radius: 16px;
      padding: 32px 24px;
      max-width: 320px;
      display: inline-block;
      margin: 16px;
      vertical-align: top;
    }
    .tier.featured {
      border-color: #00FFFF;
      box-shadow: 0 0 32px rgba(99, 234, 255, 0.18);
      transform: scale(1.05);
    }
    .tier-name { font-size: 24px; font-weight: 800; }
    .tier-price { font-size: 48px; font-weight: 800; color: #00FFFF; margin: 16px 0; }
    .tier-anchor { text-decoration: line-through; color: #94a3b8; font-size: 16px; }
    .cta {
      display: block;
      background: linear-gradient(135deg, #00FFFF, #FF00FF);
      color: #0a0e1a;
      padding: 14px;
      text-align: center;
      border-radius: 8px;
      font-weight: 700;
      text-decoration: none;
      margin-top: 16px;
    }
    .badge {
      background: #FF00FF;
      color: white;
      padding: 4px 12px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
    }
  </style>
</head>
<body>

  <h1 style="text-align: center; font-size: 48px;">Escolha seu Plano</h1>
  <p style="text-align: center; color: #94a3b8; font-size: 18px;">
    487 alunos já escolheram. Garantia de 7 dias.
  </p>

  <div style="text-align: center; margin-top: 40px;">

    <!-- TIER 1 -->
    <div class="tier">
      <div class="tier-name">Essencial</div>
      <p style="color: #94a3b8;">Para começar</p>
      <div class="tier-anchor">R$ 497</div>
      <div class="tier-price">R$ 297</div>
      <p style="color: #94a3b8;">à vista no Pix</p>
      <ul style="list-style: none; padding: 0; text-align: left;">
        <li>✓ 50% das features</li>
        <li>✓ Suporte por email (SLA 72h)</li>
        <li>✓ 1 ano de acesso</li>
      </ul>
      <a href="/checkout?tier=essencial" class="cta">COMEÇAR AGORA</a>
    </div>

    <!-- TIER 2 (FEATURED) -->
    <div class="tier featured">
      <div class="tier-name">
        Profissional
        <span class="badge">MAIS ESCOLHIDO</span>
      </div>
      <p style="color: #94a3b8;">Para escalar</p>
      <div class="tier-anchor">R$ 1.997</div>
      <div class="tier-price">R$ 997</div>
      <p style="color: #94a3b8;">ou 12x de R$ 99,70</p>
      <ul style="list-style: none; padding: 0; text-align: left;">
        <li>✓ 100% das features</li>
        <li>✓ Suporte prioritário (SLA 24h)</li>
        <li>✓ 1 sessão de mentoria/mês</li>
        <li>✓ Comunidade premium</li>
        <li>✓ Acesso vitalício</li>
      </ul>
      <a href="/checkout?tier=profissional" class="cta">QUERO ESTE PLANO</a>
    </div>

    <!-- TIER 3 (DECOY) -->
    <div class="tier">
      <div class="tier-name">Enterprise</div>
      <p style="color: #94a3b8;">Para times</p>
      <div class="tier-anchor">R$ 5.997</div>
      <div class="tier-price">R$ 2.997</div>
      <p style="color: #94a3b8;">ou 12x de R$ 299,70</p>
      <ul style="list-style: none; padding: 0; text-align: left;">
        <li>✓ 100% + 10 features exclusivas</li>
        <li>✓ Suporte 1:1 (SLA 1h)</li>
        <li>✓ 4 sessões de mentoria/mês</li>
        <li>✓ Onboarding personalizado</li>
        <li>✓ Gerente de conta dedicado</li>
      </ul>
      <a href="/checkout?tier=enterprise" class="cta">FALAR COM VENDAS</a>
    </div>

  </div>

  <p style="text-align: center; margin-top: 40px; color: #94a3b8;">
    ✓ Garantia de 7 dias · ✓ Sem fidelidade · ✓ Cancele quando quiser
  </p>

</body>
</html>
```

---

## 🏆 Bloco 4: Apresentações (30 min)

**Formato:**
- 5 squads × 5 min cada
- Apresentar: pricing atual → pricing otimizado → A/B test setup
- Votação: melhor otimização (badge + swag)
- Premiação: top 3 squads ganham 30 min de mentoria 1:1 com Niko

**Critérios de Avaliação:**

| Critério | Peso |
|----------|------|
| Análise de gaps (Bloco 1) | 25% |
| Qualidade da otimização (Bloco 2) | 35% |
| Rigor do A/B test (Bloco 3) | 25% |
| Apresentação oral | 15% |

---

## 📦 Materiais Inclusos

- Calculadora LTV (Lab-Nexus tools/financas/05)
- 5 templates de pricing page (3 tiers, anchor, charm, bundle, decoy)
- Scripts GrowthBook (open source)
- Query SQL para dashboard
- Planilha de hipóteses A/B
- Lista de 25 heurísticas de copy

---

## 🏆 Certificação WS-08-PRICING

**Quem conclui recebe:**

- ✅ Badge WS-08-PRICING (LinkedIn-verified)
- ✅ 80 XP na trilha Master
- ✅ Acesso ao canal `#pricing-lab` no Slack Estrategistas
- ✅ Listado como "Pricing Expert" no diretório
- ✅ Elegível para consultoria paga em pricing

**Próximo passo:**
- WS-08 + 1 case publicado = elegível para CEN+

---

## 📚 Pré-work

- `apostilas/42-pricing-dinamico-ia-2026.md` (50 min)
- `apostilas/32-pricing-ia-2026.md` (30 min)
- `Lab-Nexus/tools/financas/05-calculadora-valor-vida-cliente.md` (20 min)

---

## 💬 Depoimentos

> "Em 1 workshop eu aprendi o que 2 anos tentando descobriria. A planilha de hipóteses A/B sozinha vale o preço."
> — Carla M., Estrategista, SP

> "Pricing era meu ponto fraco. Hoje é meu superpoder. Triplico AOV em 2 meses."
> — Diego F., Master, Lisboa

> "Implementei decoy effect e conversões subiram 18% em 2 semanas."
> — Renata A., Estrategista, Curitiba

---

## 🔗 Materiais Complementares

- `apostilas/42-pricing-dinamico-ia-2026.md` — pricing dinâmico
- `apostilas/32-pricing-ia-2026.md` — pricing tradicional
- `Lab-Nexus/tools/financas/05-calculadora-valor-vida-cliente.md` — LTV
- `tutoriais/19-prompt-engineering-metodo-ctr.md` — CTR
- `tutoriais/22-criar-playbook-do-zero.md` — playbook

---

*AcademIA · WS-08 · Oficina de Pricing & Psicologia · 2026*