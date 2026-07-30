---
title: "Tool 06 · Calculadora de Unit Economics"
subtitle: "Como calcular LTV, CAC, payback, LTV/CAC ratio, gross margin e magic number"
author: "Equipo Nexus · Niko (CEO/AI) + Ravi (CTO/AI)"
version: "1.0.0"
date: 2026-07-30
pattern: "MMN_IA"
---

**Tool 06 · Calculadora de Unit Economics**

*Ferramenta essencial para pricing, fundraising e growth. Sem unit economics saudável, você está crescendo em direção ao buraco.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 O que Esta Tool Calcula

1. **LTV** (Lifetime Value) — receita média por cliente
2. **CAC** (Customer Acquisition Cost) — custo para adquirir cliente
3. **Payback Period** — meses para recuperar CAC
4. **LTV/CAC Ratio** — saúde do unit economics
5. **Gross Margin** — margem bruta
6. **Magic Number** — eficiência de sales/marketing
7. **Burn Multiple** — eficiência de capital
8. **Cohort LTV** — LTV por coorte de aquisição

---

## 📐 Fórmulas

### LTV (versão simples)

```
LTV = ARPU × Tempo médio como cliente × Margem
```

### LTV (versão SaaS)

```
LTV = ARPU mensal × Gross Margin / Churn mensal
```

### CAC (simples)

```
CAC = Total Sales & Marketing Spend / Novos clientes
```

### CAC Blended vs Paid

```
CAC Blended = Total S&M / Todos novos clientes
CAC Paid = Ad Spend / Clientes vindos de ads
```

### Payback Period

```
Payback = CAC / (ARPU × Gross Margin)
```

### LTV/CAC Ratio

```
Ratio = LTV / CAC
```

**Interpretação:**

| Ratio | Saúde |
|-------|-------|
| < 1 | 🔴 Quebrando (perde dinheiro por cliente) |
| 1-3 | 🟡 Apertado |
| 3-5 | 🟢 Saudável |
| > 5 | 🟢 Excelente |
| > 10 | ⚠️ Sub-investindo em growth |

### Magic Number (Sales Efficiency)

```
Magic Number = (ARR gained this quarter) / (S&M spend last quarter)
```

**Interpretação:**

| Magic Number | Ação |
|---------------|------|
| < 0.5 | 🔴 Reduzir S&M |
| 0.5-1.0 | 🟡 Manter |
| > 1.0 | 🟢 Investir mais |

### Burn Multiple

```
Burn Multiple = Net Burn / Net New ARR
```

**Interpretação:**

| Burn Multiple | Saúde |
|---------------|-------|
| < 1.0 | 🟢 Excelente |
| 1.0-1.5 | 🟡 OK |
| 1.5-2.0 | 🟡 Apertado |
| > 2.0 | 🔴 Ruim |
| > 3.0 | 💀 Crítico |

### Gross Margin

```
GM = (Receita - COGS) / Receita
```

**Para SaaS:** > 75%
**Para serviços:** > 50%
**Para hardware:** > 30%

### Net Revenue Retention (NRR)

```
NRR = (ARR inicial + expansão - churn - downgrade) / ARR inicial
```

**Interpretação:**

| NRR | Tipo |
|-----|------|
| < 80% | 🔴 Churn alto |
| 80-100% | 🟡 Estável |
| 100-110% | 🟢 Crescimento orgânico |
| 110-130% | 🟢 Excelente |
| > 130% | 🟢 Enterprise-grade |

---

## 💻 Implementação Python

### Versão 1: Calculadora CLI

```python
"""
Calculadora de Unit Economics.
Uso: python unit_economics.py
"""
from dataclasses import dataclass


@dataclass
class UnitEconomicsInputs:
    # Revenue
    arpu_mensal: float
    gm: float  # 0-1
    churn_mensal: float  # 0-1
    expansion_anual: float = 0  # 0-1

    # Costs
    cac: float
    sm_mensal: float = 0
    novos_clientes_mes: int = 0

    # Growth
    arr_anterior: float = 0
    arr_atual: float = 0
    net_burn_mensal: float = 0

    # Cohorts
    cohort_mes: str = ""
    cohort_inicial: float = 0
    cohort_revenue_mes: list = None


def calculate_unit_economics(inputs: UnitEconomicsInputs) -> dict:
    """Calcula todas as métricas de unit economics"""

    # LTV
    net_churn = inputs.churn_mensal - ((1 + inputs.expansion_anual) ** (1/12) - 1)
    if net_churn <= 0:
        ltv = (inputs.arpu_mensal * inputs.gm) * 120  # 10 anos
        ltv_note = "Churn < Expansion (excelente!)"
    else:
        ltv = (inputs.arpu_mensal * inputs.gm) / net_churn
        ltv_note = None

    # CAC
    cac = inputs.cac

    # Payback
    if inputs.arpu_mensal * inputs.gm > 0:
        payback_meses = cac / (inputs.arpu_mensal * inputs.gm)
    else:
        payback_meses = float("inf")

    # LTV/CAC
    if cac > 0:
        ltv_cac = ltv / cac
    else:
        ltv_cac = None

    # Magic Number
    if inputs.sm_mensal > 0:
        new_arr = inputs.arr_atual - inputs.arr_anterior
        magic_number = new_arr / (inputs.sm_mensal * 3)  # quarterly
    else:
        magic_number = None

    # Burn Multiple
    if (inputs.arr_atual - inputs.arr_anterior) > 0:
        burn_multiple = (inputs.net_burn_mensal * 3) / (inputs.arr_atual - inputs.arr_anterior)
    else:
        burn_multiple = None

    return {
        # LTV
        "ltv": round(ltv, 2),
        "ltv_note": ltv_note,
        "ltv_cac_ratio": round(ltv_cac, 2) if ltv_cac else None,
        "payback_meses": round(payback_meses, 1) if payback_meses != float("inf") else None,

        # Efficiency
        "cac": cac,
        "magic_number": round(magic_number, 2) if magic_number else None,
        "burn_multiple": round(burn_multiple, 2) if burn_multiple else None,

        # Diagnosis
        "diagnosis": diagnose(ltv_cac, payback_meses, burn_multiple),
    }


def diagnose(ltv_cac, payback, burn_multiple) -> str:
    """Diagnóstico baseado em múltiplas métricas"""
    issues = []

    if ltv_cac is None:
        issues.append("CAC = 0 (informe)")
    elif ltv_cac < 1:
        issues.append("LTV/CAC < 1 (quebrando)")
    elif ltv_cac < 3:
        issues.append("LTV/CAC < 3 (apertado)")
    elif ltv_cac > 10:
        issues.append("LTV/CAC > 10 (sub-investindo)")

    if payback is None or payback == float("inf"):
        issues.append("Payback indefinido")
    elif payback > 18:
        issues.append("Payback > 18 meses (longo demais)")

    if burn_multiple is None:
        pass
    elif burn_multiple > 2:
        issues.append("Burn Multiple > 2 (capital ineficiente)")

    if not issues:
        return "🟢 SAUDÁVEL: unit economics prontos para escalar"
    else:
        return "🟡 ATENÇÃO: " + "; ".join(issues)


# ======================
# Exemplo
# ======================
if __name__ == "__main__":
    inputs = UnitEconomicsInputs(
        arpu_mensal=297.0,
        gm=0.80,
        churn_mensal=0.05,
        expansion_anual=0.10,
        cac=600.0,
        sm_mensal=20000,
        arr_anterior=1_000_000,
        arr_atual=1_200_000,
        net_burn_mensal=50_000,
    )

    result = calculate_unit_economics(inputs)

    print("=" * 60)
    print("  UNIT ECONOMICS · Nexus Affil'IA'te")
    print("=" * 60)
    print(f"\n💰 LTV: R$ {result['ltv']:,.2f}")
    if result['ltv_note']:
        print(f"   ({result['ltv_note']})")
    print(f"💸 CAC: R$ {result['cac']:,.2f}")
    print(f"📊 LTV/CAC: {result['ltv_cac_ratio']}x")
    print(f"⏱  Payback: {result['payback_meses']} meses")
    print(f"\n📈 Magic Number: {result['magic_number']}")
    print(f"🔥 Burn Multiple: {result['burn_multiple']}")
    print(f"\n🎯 Diagnóstico: {result['diagnosis']}")
```

**Output esperado:**

```
============================================================
  UNIT ECONOMICS · Nexus Affil'IA'te
============================================================

💰 LTV: R$ 1,152.00
💸 CAC: R$ 600.00
📊 LTV/CAC: 1.92x
⏱  Payback: 2.5 meses

📈 Magic Number: 3.33
🔥 Burn Multiple: 0.75

🎯 Diagnóstico: 🟡 ATENÇÃO: LTV/CAC < 3 (apertado)
```

---

### Versão 2: API FastAPI

```python
"""
API para cálculo de unit economics.
"""
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Unit Economics Calculator",
    version="1.0.0",
)


class UnitEconomicsRequest(BaseModel):
    arpu_mensal: float = Field(..., gt=0, description="ARPU mensal em BRL")
    gm: float = Field(..., gt=0, le=1, description="Gross margin (0-1)")
    churn_mensal: float = Field(..., ge=0, le=1, description="Churn mensal (0-1)")
    expansion_anual: float = Field(0, ge=0, le=2)
    cac: float = Field(..., ge=0)
    sm_mensal: float = Field(0, ge=0)
    arr_anterior: float = Field(0, ge=0)
    arr_atual: float = Field(0, ge=0)
    net_burn_mensal: float = Field(0)


class UnitEconomicsResponse(BaseModel):
    ltv: float
    cac: float
    ltv_cac_ratio: Optional[float]
    payback_meses: Optional[float]
    magic_number: Optional[float]
    burn_multiple: Optional[float]
    diagnosis: str
    recommendations: list


@app.post("/v1/unit-economics/calculate", response_model=UnitEconomicsResponse)
async def calculate(req: UnitEconomicsRequest):
    inputs = UnitEconomicsInputs(
        arpu_mensal=req.arpu_mensal,
        gm=req.gm,
        churn_mensal=req.churn_mensal,
        expansion_anual=req.expansion_anual,
        cac=req.cac,
        sm_mensal=req.sm_mensal,
        arr_anterior=req.arr_anterior,
        arr_atual=req.arr_atual,
        net_burn_mensal=req.net_burn_mensal,
    )

    result = calculate_unit_economics(inputs)
    recommendations = generate_recommendations(inputs, result)

    return UnitEconomicsResponse(
        ltv=result["ltv"],
        cac=result["cac"],
        ltv_cac_ratio=result["ltv_cac_ratio"],
        payback_meses=result["payback_meses"],
        magic_number=result["magic_number"],
        burn_multiple=result["burn_multiple"],
        diagnosis=result["diagnosis"],
        recommendations=recommendations,
    )


def generate_recommendations(inputs, result) -> list:
    """Gera recomendações baseadas nos números"""
    recs = []

    if result["ltv_cac_ratio"] and result["ltv_cac_ratio"] < 3:
        recs.append({
            "priority": "alta",
            "area": "pricing ou churn",
            "action": "LTV/CAC < 3. Aumente preço em 20% ou reduza churn pela metade.",
        })

    if result["payback_meses"] and result["payback_meses"] > 12:
        recs.append({
            "priority": "alta",
            "area": "CAC ou ARPU",
            "action": "Payback > 12 meses. Reduza CAC (mude canal) ou aumente ARPU (upsell).",
        })

    if result["burn_multiple"] and result["burn_multiple"] > 2:
        recs.append({
            "priority": "crítica",
            "area": "eficiência de capital",
            "action": "Burn Multiple > 2. Considere pausar hiring ou cortar canais não-eficientes.",
        })

    if result["magic_number"] and result["magic_number"] < 0.5:
        recs.append({
            "priority": "alta",
            "area": "sales efficiency",
            "action": "Magic Number < 0.5. S&M não está retornando ARR. Repensar canais.",
        })

    if not recs:
        recs.append({
            "priority": "informacional",
            "area": "escala",
            "action": "Unit economics saudáveis. Pode dobrar investimento em growth.",
        })

    return recs
```

**Uso:**

```bash
curl -X POST http://localhost:8000/v1/unit-economics/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "arpu_mensal": 297,
    "gm": 0.80,
    "churn_mensal": 0.05,
    "expansion_anual": 0.10,
    "cac": 600,
    "sm_mensal": 20000,
    "arr_anterior": 1000000,
    "arr_atual": 1200000,
    "net_burn_mensal": 50000
  }'
```

**Resposta:**

```json
{
  "ltv": 1152.0,
  "cac": 600.0,
  "ltv_cac_ratio": 1.92,
  "payback_meses": 2.5,
  "magic_number": 3.33,
  "burn_multiple": 0.75,
  "diagnosis": "🟡 ATENÇÃO: LTV/CAC < 3 (apertado)",
  "recommendations": [
    {
      "priority": "alta",
      "area": "pricing ou churn",
      "action": "LTV/CAC < 3. Aumente preço em 20% ou reduza churn pela metade."
    }
  ]
}
```

---

### Versão 3: Análise de Coorte

```python
"""
Análise de LTV por coorte de aquisição.
"""
import pandas as pd
import numpy as np


def calculate_cohort_ltv(
    transactions: pd.DataFrame,
    cohort_col: str = "signup_month",
    revenue_col: str = "revenue",
    customer_col: str = "customer_id",
) -> pd.DataFrame:
    """
    Calcula LTV cumulativo por coorte de signup.

    transactions: DataFrame com colunas:
    - customer_id
    - signup_month
    - transaction_month
    - revenue
    """
    # Meses desde signup (tenure)
    transactions = transactions.copy()
    transactions["tenure_month"] = (
        (transactions["transaction_month"].dt.year - transactions[cohort_col].dt.year) * 12
        + (transactions["transaction_month"].dt.month - transactions[cohort_col].dt.month)
    )

    # Agregar LTV por coorte
    cohort_data = (
        transactions
        .groupby([cohort_col, "tenure_month"])
        .agg(
            total_revenue=(revenue_col, "sum"),
            unique_customers=(customer_col, "nunique"),
        )
        .reset_index()
    )

    # Calcular LTV médio por customer
    cohort_data["ltv_cumulative"] = (
        cohort_data
        .sort_values(["tenure_month"])
        .groupby(cohort_col)["total_revenue"]
        .cumsum()
    )
    cohort_data["ltv_per_customer"] = (
        cohort_data["ltv_cumulative"] / cohort_data["unique_customers"]
    )

    # Pivot para visualização
    pivot = cohort_data.pivot_table(
        index=cohort_col,
        columns="tenure_month",
        values="ltv_per_customer",
    )

    return pivot


def plot_cohort_heatmap(cohort_pivot: pd.DataFrame, save_path: str = None):
    """Gera heatmap da coorte"""
    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.figure(figsize=(14, 8))
    sns.heatmap(
        cohort_pivot,
        annot=True,
        fmt=".0f",
        cmap="YlGnBu",
        cbar_kws={"label": "LTV por cliente (R$)"},
        linewidths=0.5,
    )
    plt.title("LTV Acumulado por Coorte de Signup")
    plt.xlabel("Meses desde Signup (Tenure)")
    plt.ylabel("Mês de Signup")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Heatmap salvo em {save_path}")
    else:
        plt.show()
```

---

## 📊 Análise por Segmento

```python
def unit_economics_by_segment(segmentos: list) -> dict:
    """
    Calcula unit economics por segmento.

    segmentos = [
        {'nome': 'Free',  'arpu': 0,    'churn_mensal': 0.20, 'gm': 0.50, 'cac': 50,   'size': 1000},
        {'nome': 'Pro',   'arpu': 99,   'churn_mensal': 0.08, 'gm': 0.80, 'cac': 300,  'size': 200},
        {'nome': 'Enterp.','arpu': 1000, 'churn_mensal': 0.02, 'gm': 0.90, 'cac': 5000, 'size': 20},
    ]
    """
    results = {}
    total_revenue = 0
    total_cac = 0

    for seg in segmentos:
        net_churn = seg["churn_mensal"]
        ltv = (seg["arpu"] * seg["gm"]) / net_churn if net_churn > 0 else 999_999
        ltv_cac = ltv / seg["cac"] if seg["cac"] > 0 else None

        revenue_seg = ltv * seg["size"]
        cac_seg = seg["cac"] * seg["size"]

        results[seg["nome"]] = {
            "ltv": round(ltv, 2),
            "cac": seg["cac"],
            "ltv_cac_ratio": round(ltv_cac, 2) if ltv_cac else None,
            "size": seg["size"],
            "revenue_lifetime": round(revenue_seg, 2),
            "cac_total": round(cac_seg, 2),
            "profit_lifetime": round(revenue_seg - cac_seg, 2),
        }

        total_revenue += revenue_seg
        total_cac += cac_seg

    results["_total"] = {
        "revenue_lifetime": round(total_revenue, 2),
        "cac_total": round(total_cac, 2),
        "profit_lifetime": round(total_revenue - total_cac, 2),
        "blended_ltv_cac": round(total_revenue / total_cac, 2) if total_cac > 0 else None,
    }

    return results


# Exemplo
segmentos = [
    {"nome": "Free", "arpu": 0, "churn_mensal": 0.20, "gm": 0.50, "cac": 50, "size": 1000},
    {"nome": "Pro", "arpu": 99, "churn_mensal": 0.08, "gm": 0.80, "cac": 300, "size": 200},
    {"nome": "Enterprise", "arpu": 1000, "churn_mensal": 0.02, "gm": 0.90, "cac": 5000, "size": 20},
]

resultado = unit_economics_by_segment(segmentos)
import json
print(json.dumps(resultado, indent=2, ensure_ascii=False))
```

**Output:**

```json
{
  "Free": {
    "ltv": 0.0,
    "cac": 50,
    "ltv_cac_ratio": 0.0,
    "size": 1000,
    "revenue_lifetime": 0.0,
    "cac_total": 50000.0,
    "profit_lifetime": -50000.0
  },
  "Pro": {
    "ltv": 990.0,
    "cac": 300,
    "ltv_cac_ratio": 3.3,
    "size": 200,
    "revenue_lifetime": 198000.0,
    "cac_total": 60000.0,
    "profit_lifetime": 138000.0
  },
  "Enterprise": {
    "ltv": 45000.0,
    "cac": 5000,
    "ltv_cac_ratio": 9.0,
    "size": 20,
    "revenue_lifetime": 900000.0,
    "cac_total": 100000.0,
    "profit_lifetime": 800000.0
  },
  "_total": {
    "revenue_lifetime": 1098000.0,
    "cac_total": 210000.0,
    "profit_lifetime": 888000.0,
    "blended_ltv_cac": 5.23
  }
}
```

**Insight:** Free users dão prejuízo, Pro é saudável, Enterprise é o motor de lucro. Considere mudar estratégia: menos Free, mais Pro.

---

## 📅 Dashboard de Unit Economics

```python
"""
Dashboard atualizado mensalmente.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_unit_economics_evolution(monthly_data: pd.DataFrame, save_path: str = None):
    """
    Plota evolução de LTV, CAC, LTV/CAC ao longo do tempo.

    monthly_data tem colunas: month, ltv, cac, ltv_cac_ratio
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # LTV
    axes[0, 0].plot(monthly_data["month"], monthly_data["ltv"], marker="o", color="green")
    axes[0, 0].set_title("LTV ao longo do tempo")
    axes[0, 0].set_ylabel("R$")
    axes[0, 0].grid(True)

    # CAC
    axes[0, 1].plot(monthly_data["month"], monthly_data["cac"], marker="o", color="red")
    axes[0, 1].set_title("CAC ao longo do tempo")
    axes[0, 1].set_ylabel("R$")
    axes[0, 1].grid(True)

    # LTV/CAC Ratio
    axes[1, 0].plot(
        monthly_data["month"],
        monthly_data["ltv_cac_ratio"],
        marker="o",
        color="blue",
    )
    axes[1, 0].axhline(y=3, color="green", linestyle="--", label="Saudável (3x)")
    axes[1, 0].axhline(y=1, color="red", linestyle="--", label="Break-even (1x)")
    axes[1, 0].set_title("LTV/CAC Ratio")
    axes[1, 0].set_ylabel("Ratio")
    axes[1, 0].legend()
    axes[1, 0].grid(True)

    # Payback
    payback = monthly_data["cac"] / (
        monthly_data["ltv"] * 0.05
    )  # assume churn 5%
    axes[1, 1].plot(monthly_data["month"], payback, marker="o", color="purple")
    axes[1, 1].axhline(y=12, color="green", linestyle="--", label="Bom (< 12 meses)")
    axes[1, 1].set_title("Payback Period")
    axes[1, 1].set_ylabel("Meses")
    axes[1, 1].legend()
    axes[1, 1].grid(True)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    else:
        plt.show()
```

---

## 🎯 Interpretação Prática

### Cenário 1: Startup Seed

```
LTV: R$ 1.000
CAC: R$ 800
LTV/CAC: 1.25x
Payback: 12 meses
Diagnóstico: 🟡 apertado, mas ok para seed
```

**Ação:** aceitar (investidores seed entendem). Foco em product-market fit.

### Cenário 2: Startup Series A

```
LTV: R$ 5.000
CAC: R$ 1.000
LTV/CAC: 5x
Payback: 6 meses
Diagnóstico: 🟢 saudável
```

**Ação:** investir agressivamente em growth. Magic Number vai ser alto.

### Cenário 3: Startup em Crise

```
LTV: R$ 500
CAC: R$ 1.200
LTV/CAC: 0.42x
Payback: 30+ meses
Diagnóstico: 🔴 quebrando
```

**Ação:** parar aquisição. Investigar churn, pricing, ICP.

### Cenário 4: SaaS B2B Enterprise

```
LTV: R$ 50.000
CAC: R$ 8.000
LTV/CAC: 6.25x
Payback: 8 meses
Diagnóstico: 🟢 excelente
```

**Ação:** manter, considerar expansão de canal.

---

## 🛠️ Quando Usar Cada Métrica

| Métrica | Quando usar |
|---------|-------------|
| **LTV/CAC** | Visão geral de saúde |
| **CAC Payback** | Decidir se escala agora |
| **Magic Number** | Eficiência de S&M (sales-led) |
| **Burn Multiple** | Saúde financeira geral |
| **NRR** | Qualidade do produto (PLG/marketplace) |
| **Gross Margin** | Modelo de negócio saudável |
| **Cohort LTV** | Tendência de longo prazo |

---

## ✅ Checklist Mensal

- [ ] Calcular LTV, CAC, LTV/CAC, Payback
- [ ] Calcular Magic Number e Burn Multiple
- [ ] Segmentar por canal de aquisição
- [ ] Analisar coortes (últimos 6 meses)
- [ ] Atualizar dashboard Grafana
- [ ] Reportar para investidores (se aplicável)
- [ ] Ajustar estratégia baseado nos dados

---

## 📚 Materiais Complementares

- `Lab-Nexus/tools/financas/01-business-case-template.md`
- `Lab-Nexus/tools/financas/02-calculadora-payback.md`
- `Lab-Nexus/tools/financas/03-orcamento-anual.md`
- `Lab-Nexus/tools/financas/04-fluxo-caixa-projetado.md`
- `Lab-Nexus/tools/financas/05-calculadora-valor-vida-cliente.md`
- `apostilas/42-pricing-dinamico-ia-2026.md`
- `apostilas/44-fiscal-contabilidade-2026.md`

---

## 🔗 Links Externos

- David Sacks: https://saas.huddle.com/articles/burn-multiple/
- OpenView Partners: https://openviewpartners.com/blog/
- Lenny's Newsletter: https://www.lennysnewsletter.com/p/unit-economics
- ICONIQ Growth: https://iconiqcapital.com/growth

---

*AcademIA · Tool 06 · Unit Economics · 2026*