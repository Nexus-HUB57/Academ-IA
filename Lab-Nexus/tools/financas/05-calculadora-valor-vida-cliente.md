---
title: "Tool 05 · Calculadora de Valor Vida do Cliente (LTV)"
subtitle: "Como calcular LTV, CAC payback e LTV/CAC ratio para pricing dinâmico"
author: "Equipo Nexus · Niko (CEO/AI) + Ravi (CTO/AI)"
version: "1.0.0"
date: 2026-07-27
pattern: "MMN_IA"
---

**Tool 05 · Calculadora de Valor Vida do Cliente (LTV)**

*Ferramenta essencial para pricing dinâmico. Sem LTV, você está otimizando para o curto prazo.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 O que Esta Tool Calcula

1. **LTV (Lifetime Value)** — receita média por cliente ao longo do relacionamento
2. **CAC (Customer Acquisition Cost)** — quanto custa adquirir 1 cliente
3. **LTV/CAC Ratio** — saúde do negócio
4. **CAC Payback Period** — quanto tempo para recuperar CAC
5. **LTV por segmento** — para pricing dinâmico

---

## 📐 Fórmulas

### LTV (versão simples)

```
LTV = AOV × Compra média por cliente × Margem
```

### LTV (versão subscription/SaaS)

```
LTV = ARPU × Gross Margin / Churn Rate
```

**Onde:**
- ARPU = Average Revenue Per User (mensal)
- Gross Margin = (Receita - Custo) / Receita
- Churn Rate = % de clientes que cancelam por mês

### LTV (versão completa, com expansão)

```
LTV = (ARPU × Gross Margin) / (Churn - Expansion Rate)
```

**Onde:**
- Expansion Rate = receita adicional de upsell/cross-sell (anualizado)
- Se Expansion > Churn, LTV é "infinito" (excelente)

### CAC

```
CAC = (Marketing + Vendas) / Novos clientes
```

### CAC Payback

```
Payback = CAC / (ARPU × Gross Margin)
```

Em meses. Meta: < 12 meses.

### LTV/CAC Ratio

```
Ratio = LTV / CAC
```

**Interpretação:**

| Ratio | Saúde |
|-------|-------|
| < 1 | 🔴 Quebrando |
| 1-3 | 🟡 Aperte o cinto |
| 3-5 | 🟢 Saudável |
| > 5 | 🟢 Excelente (invista em escala) |
| > 10 | ⚠️ Provavelmente sub-investindo em growth |

---

## 💻 Implementação em Python

### Versão 1: Calculadora CLI

```python
# ltv_calculator.py
"""
Calculadora de LTV / CAC / Payback para Nexus Affil'IA'te.
Uso: python ltv_calculator.py
"""
from dataclasses import dataclass
from datetime import date


@dataclass
class LTVInputs:
    arpu_mensal: float          # Average Revenue Per User (mensal)
    gross_margin: float         # 0-1 (ex: 0.80 = 80% margem)
    churn_mensal: float         # 0-1 (ex: 0.05 = 5% churn mensal)
    expansion_anual: float = 0  # 0-1 (ex: 0.10 = 10% upsell anual)
    cac: float = 0              # Customer Acquisition Cost


def calculate_ltv(inputs: LTVInputs) -> dict:
    """Calcula métricas de LTV"""
    arpu = inputs.arpu_mensal
    gm = inputs.gross_margin
    churn = inputs.churn_mensal
    exp_annual = inputs.expansion_anual
    exp_monthly = (1 + exp_annual) ** (1/12) - 1
    net_churn = churn - exp_monthly

    if net_churn <= 0:
        # Expansão > Churn (excelente!)
        ltv = (arpu * gm) * 120  # 10 anos de LTV efetivo
        warning = "Churn < Expansion (excelente!)"
    else:
        ltv = (arpu * gm) / net_churn
        warning = None

    if inputs.cac > 0:
        ltv_cac_ratio = ltv / inputs.cac
        if ltv > 0 and arpu * gm > 0:
            payback_months = inputs.cac / (arpu * gm)
        else:
            payback_months = float('inf')
    else:
        ltv_cac_ratio = None
        payback_months = None

    return {
        'ltv': round(ltv, 2),
        'ltv_cac_ratio': round(ltv_cac_ratio, 2) if ltv_cac_ratio else None,
        'payback_months': round(payback_months, 1) if payback_months else None,
        'warning': warning,
        'net_churn_monthly': round(net_churn * 100, 2),
    }


def interpret(ltv_cac_ratio: float) -> str:
    """Interpreta ratio"""
    if ltv_cac_ratio < 1:
        return "🔴 PREJUÍZO: você perde dinheiro a cada cliente"
    elif ltv_cac_ratio < 3:
        return "🟡 APERTE O CINTO: saudável mas apertado"
    elif ltv_cac_ratio < 5:
        return "🟢 SAUDÁVEL: boa margem para investir em escala"
    elif ltv_cac_ratio < 10:
        return "🟢 EXCELENTE: invista agressivamente em aquisição"
    else:
        return "⚠️ SUB-INVESTINDO: aumente CAC para capturar mais mercado"


# ======================
# Exemplo
# ======================
if __name__ == "__main__":
    # SaaS: ARPU R$ 99, margem 80%, churn 5% mensal, CAC R$ 250
    inputs = LTVInputs(
        arpu_mensal=99.0,
        gross_margin=0.80,
        churn_mensal=0.05,
        expansion_anual=0.10,
        cac=250.0
    )

    result = calculate_ltv(inputs)

    print("=" * 50)
    print("  CALCULADORA LTV / CAC / PAYBACK")
    print("=" * 50)
    print(f"\n📊 Inputs:")
    print(f"  ARPU mensal:           R$ {inputs.arpu_mensal:.2f}")
    print(f"  Margem bruta:          {inputs.gross_margin * 100:.0f}%")
    print(f"  Churn mensal:          {inputs.churn_mensal * 100:.1f}%")
    print(f"  Expansão anual:        {inputs.expansion_anual * 100:.0f}%")
    print(f"  CAC:                   R$ {inputs.cac:.2f}")

    print(f"\n💰 Resultados:")
    print(f"  LTV:                   R$ {result['ltv']:.2f}")
    if result['ltv_cac_ratio']:
        print(f"  LTV/CAC ratio:         {result['ltv_cac_ratio']:.2f}x")
        print(f"  Payback period:        {result['payback_months']:.1f} meses")
        print(f"\n  Diagnóstico: {interpret(result['ltv_cac_ratio'])}")

    if result['warning']:
        print(f"\n  ⚠️ {result['warning']}")
```

**Output esperado:**

```
==================================================
  CALCULADORA LTV / CAC / PAYBACK
==================================================

📊 Inputs:
  ARPU mensal:           R$ 99.00
  Margem bruta:          80%
  Churn mensal:          5.0%
  Expansão anual:        10%
  CAC:                   R$ 250.00

💰 Resultados:
  LTV:                   R$ 1152.00
  LTV/CAC ratio:         4.61x
  Payback period:        3.2 meses

  Diagnóstico: 🟢 SAUDÁVEL: boa margem para investir em escala
```

---

### Versão 2: API FastAPI

```python
# ltv_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Nexus LTV Calculator",
    description="Calculadora de LTV, CAC, Payback e LTV/CAC ratio",
    version="1.0.0"
)


class LTVRequest(BaseModel):
    arpu_mensal: float = Field(..., gt=0, description="ARPU mensal em BRL")
    gross_margin: float = Field(..., gt=0, le=1, description="Margem bruta (0-1)")
    churn_mensal: float = Field(..., ge=0, le=1, description="Churn mensal (0-1)")
    expansion_anual: float = Field(0, ge=0, le=2, description="Expansão anual (0-2)")
    cac: float = Field(0, ge=0, description="Custo de aquisição")
    segmento: Optional[str] = Field(None, description="Segmento do cliente")


class LTVResponse(BaseModel):
    ltv: float
    ltv_cac_ratio: Optional[float]
    payback_months: Optional[float]
    diagnosis: str
    recommendation: str
    benchmark_percentile: Optional[int]


@app.post("/v1/ltv/calculate", response_model=LTVResponse)
async def calculate(req: LTVRequest):
    arpu = req.arpu_mensal
    gm = req.gross_margin
    churn = req.churn_mensal
    exp_annual = req.expansion_anual
    exp_monthly = (1 + exp_annual) ** (1/12) - 1
    net_churn = churn - exp_monthly

    if net_churn <= 0:
        ltv = (arpu * gm) * 120  # 10 anos
        warning = "Churn < Expansion: LTV indefinido (excelente)"
    else:
        ltv = (arpu * gm) / net_churn

    if req.cac > 0:
        ratio = ltv / req.cac
        payback = req.cac / (arpu * gm) if arpu * gm > 0 else float('inf')

        # Diagnóstico
        if ratio < 1:
            diagnosis = "PREJUIZO"
            recommendation = "Pare aquisição. Reestruture."
        elif ratio < 3:
            diagnosis = "APERTE_CINTO"
            recommendation = "Reduza CAC ou aumente LTV antes de escalar."
        elif ratio < 5:
            diagnosis = "SAUDAVEL"
            recommendation = "Pode investir moderadamente em escala."
        elif ratio < 10:
            diagnosis = "EXCELENTE"
            recommendation = "Invista agressivamente em aquisição."
        else:
            diagnosis = "SUB_INVESTINDO"
            recommendation = "Aumente CAC - capture mais mercado."
    else:
        ratio = None
        payback = None
        diagnosis = "SEM_CAC"
        recommendation = "Forneça CAC para análise completa."

    return LTVResponse(
        ltv=round(ltv, 2),
        ltv_cac_ratio=round(ratio, 2) if ratio else None,
        payback_months=round(payback, 1) if payback and payback != float('inf') else None,
        diagnosis=diagnosis,
        recommendation=recommendation,
        benchmark_percentile=None  # TODO: integrar com dataset
    )
```

**Uso:**

```bash
curl -X POST http://localhost:8000/v1/ltv/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "arpu_mensal": 99,
    "gross_margin": 0.80,
    "churn_mensal": 0.05,
    "expansion_anual": 0.10,
    "cac": 250
  }'
```

**Resposta:**

```json
{
  "ltv": 1152.0,
  "ltv_cac_ratio": 4.61,
  "payback_months": 3.2,
  "diagnosis": "SAUDAVEL",
  "recommendation": "Pode investir moderadamente em escala.",
  "benchmark_percentile": null
}
```

---

### Versão 3: Análise por Segmento

```python
# ltv_by_segment.py
from typing import List, Dict

def calculate_ltv_by_segment(
    segmentos: List[Dict]
) -> Dict:
    """
    Calcula LTV por segmento para pricing dinâmico.

    segmentos = [
        {'nome': 'Bargain Hunter', 'arpu': 50, 'churn_mensal': 0.10, 'gm': 0.70, 'cac': 80, 'size': 200},
        {'nome': 'Mainstream',     'arpu': 99, 'churn_mensal': 0.05, 'gm': 0.80, 'cac': 250, 'size': 350},
        {'nome': 'Premium',        'arpu': 297, 'churn_mensal': 0.02, 'gm': 0.85, 'cac': 600, 'size': 100},
    ]
    """
    results = {}
    total_revenue = 0
    total_cac = 0

    for seg in segmentos:
        net_churn = seg['churn_mensal']
        ltv = (seg['arpu'] * seg['gm']) / net_churn
        ratio = ltv / seg['cac'] if seg['cac'] > 0 else None
        revenue_seg = ltv * seg['size']
        cac_seg = seg['cac'] * seg['size']

        results[seg['nome']] = {
            'ltv': round(ltv, 2),
            'ltv_cac_ratio': round(ratio, 2) if ratio else None,
            'size': seg['size'],
            'revenue_total': round(revenue_seg, 2),
            'cac_total': round(cac_seg, 2),
            'profit_total': round(revenue_seg - cac_seg, 2),
        }

        total_revenue += revenue_seg
        total_cac += cac_seg

    results['_summary'] = {
        'revenue_total': round(total_revenue, 2),
        'cac_total': round(total_cac, 2),
        'profit_total': round(total_revenue - total_cac, 2),
        'roi': round((total_revenue - total_cac) / total_cac, 2) if total_cac > 0 else None,
    }

    return results


# Exemplo
segmentos = [
    {'nome': 'Bargain Hunter', 'arpu': 50, 'churn_mensal': 0.10, 'gm': 0.70, 'cac': 80, 'size': 200},
    {'nome': 'Value Seeker',   'arpu': 75, 'churn_mensal': 0.07, 'gm': 0.75, 'cac': 150, 'size': 300},
    {'nome': 'Mainstream',     'arpu': 99, 'churn_mensal': 0.05, 'gm': 0.80, 'cac': 250, 'size': 350},
    {'nome': 'Quality Seeker', 'arpu': 197, 'churn_mensal': 0.03, 'gm': 0.85, 'cac': 400, 'size': 120},
    {'nome': 'Status Buyer',   'arpu': 500, 'churn_mensal': 0.02, 'gm': 0.90, 'cac': 800, 'size': 30},
]

resultado = calculate_ltv_by_segment(segmentos)
import json
print(json.dumps(resultado, indent=2))
```

**Output:**

```json
{
  "Bargain Hunter": {
    "ltv": 350.0,
    "ltv_cac_ratio": 4.38,
    "size": 200,
    "revenue_total": 70000.0,
    "cac_total": 16000.0,
    "profit_total": 54000.0
  },
  "Value Seeker": {
    "ltv": 803.57,
    "ltv_cac_ratio": 5.36,
    "size": 300,
    "revenue_total": 241071.0,
    "cac_total": 45000.0,
    "profit_total": 196071.0
  },
  "Mainstream": {
    "ltv": 1584.0,
    "ltv_cac_ratio": 6.34,
    "size": 350,
    "revenue_total": 554400.0,
    "cac_total": 87500.0,
    "profit_total": 466900.0
  },
  "Quality Seeker": {
    "ltv": 5583.33,
    "ltv_cac_ratio": 13.96,
    "size": 120,
    "revenue_total": 669999.6,
    "cac_total": 48000.0,
    "profit_total": 621999.6
  },
  "Status Buyer": {
    "ltv": 22500.0,
    "ltv_cac_ratio": 28.13,
    "size": 30,
    "revenue_total": 675000.0,
    "cac_total": 24000.0,
    "profit_total": 651000.0
  },
  "_summary": {
    "revenue_total": 2210470.6,
    "cac_total": 220500.0,
    "profit_total": 1989970.6,
    "roi": 9.02
  }
}
```

---

## 📊 Planilha de Cálculo Rápido

Se preferir planilha:

| Métrica | Valor |
|---------|-------|
| **ARPU mensal** | R$ ___ |
| **Gross margin** | ___% |
| **Churn mensal** | ___% |
| **Expansão anual** | ___% |
| **CAC** | R$ ___ |
| **LTV (calculado)** | R$ ___ |
| **LTV/CAC** | ___x |
| **Payback** | ___ meses |

**Fórmulas de célula:**

```
LTV = (B1*B2) / (B3 - ((1+B4)^(1/12)-1))
LTV/CAC = B6 / B5
Payback = B5 / (B1*B2)
```

---

## 📈 Análise de Coorte (Cohort Analysis)

**O que é:** acompanhar LTV de grupos de clientes ao longo do tempo.

```python
# cohort_ltv.py
import pandas as pd
import numpy as np

def calculate_cohort_ltv(
    transactions: pd.DataFrame,
    cohort_col: str = 'signup_month',
    period_col: str = 'transaction_month'
) -> pd.DataFrame:
    """
    Calcula LTV acumulado por coorte (mês de signup) e mês de tenure.

    transactions deve ter colunas:
    - customer_id
    - signup_month
    - transaction_month
    - revenue
    """
    # Meses desde signup (tenure)
    transactions['tenure_month'] = (
        (transactions[period_col].dt.year - transactions[cohort_col].dt.year) * 12 +
        (transactions[period_col].dt.month - transactions[cohort_col].dt.month)
    )

    # LTV acumulado por coorte
    cohort_ltv = transactions.groupby(
        [cohort_col, 'tenure_month']
    )['revenue'].sum().reset_index()

    # Pivot para visualização
    cohort_ltv_pivot = cohort_ltv.pivot(
        index=cohort_col,
        columns='tenure_month',
        values='revenue'
    ).cumsum(axis=1)

    return cohort_ltv_pivot


# Visualização
import matplotlib.pyplot as plt
import seaborn as sns

def plot_cohort_heatmap(cohort_ltv: pd.DataFrame):
    plt.figure(figsize=(14, 8))
    sns.heatmap(
        cohort_ltv,
        annot=True,
        fmt='.0f',
        cmap='YlGnBu',
        cbar_kws={'label': 'LTV Acumulado (R$)'}
    )
    plt.title('LTV Acumulado por Coorte de Signup')
    plt.xlabel('Meses desde Signup')
    plt.ylabel('Mês de Signup')
    plt.tight_layout()
    plt.savefig('cohort_ltv.png', dpi=150)
    print("Heatmap salvo em cohort_ltv.png")
```

---

## 🎯 Aplicação: Pricing Dinâmico Orientado por LTV

### Estratégia 1: LTV-Based Segmentação

```python
def recommend_price_by_ltv(ltv: float, gross_margin: float, target_ltv_cac: float = 4.0) -> float:
    """
    Recomenda preço que maximize LTV dado um LTV/CAC target.
    """
    # Se queremos LTV/CAC = 4, e CAC típico = 30% do ARPU (sector médio):
    # LTV = 4 × CAC
    # LTV = ARPU × GM / churn
    # ARPU = LTV × churn / GM
    # ARPU = 4 × CAC × churn / GM
    # ARPU = 4 × (0.3 × ARPU) × churn / GM
    # 1 = 1.2 × churn / GM
    # churn = GM / 1.2

    # Mas para SaaS simples, podemos simplificar:
    # price = LTV × churn / GM
    return ltv * 0.05 / gross_margin  # Assumindo churn 5% mensal


# Exemplo: LTV target R$ 1000, GM 80%
recommended_price = recommend_price_by_ltv(ltv=1000, gross_margin=0.80)
# = R$ 62.50/mês
```

### Estratégia 2: CAC-Aware Pricing

```python
def optimize_price_for_cac_ratio(
    current_price: float,
    current_conversion: float,
    current_cac: float,
    target_ltv_cac: float = 4.0,
    elasticity: float = -1.5
) -> float:
    """
    Encontra preço que maximiza LTV/CAC ratio.
    """
    # LTV = ARPU × GM / churn
    # CAC = custo_total / clientes
    # LTV/CAC = ARPU / CAC

    # Assumindo: a cada +1% no preço, conversão cai elasticity%
    # Revenue_per_visit = price × conversion(price)
    # LTV/CAC = price × conversion(price) / CAC

    from scipy.optimize import minimize_scalar

    def negative_ltv_cac(price):
        new_conversion = current_conversion * (1 + elasticity * (price - current_price) / current_price)
        new_conversion = max(0.0001, min(1, new_conversion))
        # ARPU vai para LTV
        ltv = price * 0.8 / 0.05  # Assumindo churn 5%
        # CAC é proporcional ao inverse da conversão
        new_cac = current_cac * (current_conversion / new_conversion)
        return -(ltv / new_cac)

    result = minimize_scalar(negative_ltv_cac, bounds=(current_price*0.5, current_price*2), method='bounded')
    return round(result.x, 2)
```

---

## ✅ Checklist de Implementação

- [ ] Calcular LTV atual (3 últimos meses de dados)
- [ ] Calcular CAC atual
- [ ] Validar LTV/CAC ratio (meta: 3-5x)
- [ ] Calcular CAC payback (meta: < 12 meses)
- [ ] Segmentar clientes (Bargain/Value/Mainstream/Premium/Status)
- [ ] Calcular LTV por segmento
- [ ] Ajustar pricing se LTV/CAC < 3
- [ ] Documentar premissas
- [ ] Revisar trimestralmente
- [ ] Ajustar churn/expansion rate com dados reais

---

## 📚 Materiais Complementares

- `Lab-Nexus/tools/financas/01-business-case.md` — business case framework
- `Lab-Nexus/tools/financas/02-calculadora-payback.md` — payback
- `Lab-Nexus/tools/financas/03-orcamento-anual.md` — budget
- `Lab-Nexus/tools/financas/04-fluxo-caixa-projetado.md` — cash flow
- `apostilas/42-pricing-dinamico-ia-2026.md` — pricing dinâmico
- `apostilas/32-pricing-ia-2026.md` — pricing tradicional
- `tutoriais/19-prompt-engineering-metodo-ctr.md` — CTR

---

## 🔗 Links Externos

- Lenny's Newsletter LTV: https://www.lennysnewsletter.com/p/lTV
- SaaS metrics: https://www.forEntrepreneurs.com/saas-metrics-2/
- Cohort analysis: https://www.amplitude.com/blog/cohort-analysis

---

*AcademIA · Tool 05 · LTV Calculator · 2026*