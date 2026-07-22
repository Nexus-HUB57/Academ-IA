---
title: "KPIs Oficiais Nexus · Catálogo Canônico"
description: "Catálogo das métricas oficiais, fórmulas de cálculo, owners e targets para o ecossistema Nexus"
tags: [lib-nexus, knowledge-base, kpi, metricas, canonico, sla]
category: knowledge-base
version: "1.0"
last_review: "2026-07-21"
status: canonico
---

# 📊 KPIs Oficiais Nexus · Catálogo Canônico

> **Source of truth** das métricas oficiais reportadas pelo ecossistema Nexus. Este documento define cada KPI, fórmula de cálculo, owner accountable, target e cadência de revisão.

---

## 🎯 Definição Canônica

Um **KPI (Key Performance Indicator)** é uma métrica que:

1. **Reflete objetivo de negócio** (não apenas atividade).
2. **É quantificável** (número, percentual, índice).
3. **É comparável** ao longo do tempo.
4. **Tem owner accountable** (humano ou sistema).
5. **Tem target** definido e revisado.

**Anti-KPI** (não deve ser reportado): vanity metrics, métricas de proxy ruins, métricas que otimizam o sistema no lugar do objetivo.

---

## 📋 Catálogo Oficial

### Categoria 1 — Plataforma (Nível 0)

| KPI | Fórmula | Owner | Target | Cadência |
|-----|---------|-------|--------|----------|
| **MRR** (Monthly Recurring Revenue) | soma de mensalidades ativas × 1 mês | Head de Operações | crescente 5%/mês | Mensal |
| **ARR** (Annual Recurring Revenue) | MRR × 12 | Head de Operações | crescente 50%/ano | Trimestral |
| **Tenants ativos** | tenants com >1 ação/mês | Head de Operações | >13.000 | Mensal |
| **GMV Marketplace** | soma de transações marketplace | Head de Marketplace | >R$5M/mês | Mensal |
| **Churn mensal** | tenants que saíram / total | Head de Operações | <2% | Mensal |
| **NPS** | Net Promoter Score | Head de CX | >50 | Trimestral |

### Categoria 2 — Performance Técnica (Nível 1)

| KPI | Fórmula | Owner | Target | Cadência |
|-----|---------|-------|--------|----------|
| **Disponibilidade** | (tempo_up / tempo_total) × 100 | SRE | >99.95% | Contínua |
| **Latência p50** | mediana de latência | SRE | <100ms | Contínua |
| **Latência p99** | percentil 99 | SRE | <200ms | Contínua |
| **Latência p99.9** | percentil 99.9 | SRE | <500ms | Contínua |
| **Error rate (5xx)** | 5xx / total_requests | SRE | <0.1% | Contínua |
| **MTTR** (Mean Time To Recover) | média de tempo de recuperação | SRE | <15min | Por incidente |
| **MTBF** (Mean Time Between Failures) | uptime / # de incidents | SRE | >720h | Mensal |

### Categoria 3 — SHO (Nível 2)

| KPI | Fórmula | Owner | Target | Cadência |
|-----|---------|-------|--------|----------|
| **Detecção latency SEV-3** | ts_detecção - ts_incidente | SHO Lead | <90s | Por evento |
| **FPR** (False Positive Rate) | alertas errados / total alertas | SHO Lead | <5% | Mensal |
| **FNR** (False Negative Rate) | incidents não detectados / total | SHO Lead | <1% | Mensal |
| **Playbook coverage** | incidents com playbook / total | SHO Lead | >90% | Mensal |
| **Auto-resolution rate** | incidents resolvidos por SHO / total | SHO Lead | >60% | Mensal |

### Categoria 4 — Marketplace (Nível 3)

| KPI | Fórmula | Owner | Target | Cadência |
|-----|---------|-------|--------|----------|
| **Skills publicadas** | count skills ativas | Marketplace Lead | >800 | Mensal |
| **Autores ativos** | autores com ≥1 venda últimos 30d | Marketplace Lead | >200 | Mensal |
| **Review médio** | média de ratings | Marketplace Lead | >4.3 | Mensal |
| **Retenção 30d** | % skills ativas após 30d da compra | Marketplace Lead | >80% | Mensal |
| **Revenue share Nexus** | % que Nexus fica | Head de Marketplace | 20% | Mensal |

### Categoria 5 — Afiliado (Nível 4 — Individual)

| KPI | Fórmula | Owner (afiliado) | Target | Cadência |
|-----|---------|-------------------|--------|----------|
| **Receita mensal** | receita atribuível ao afiliado | afiliado | crescente | Mensal |
| **ROI Direto** | (receita - custo) / custo | afiliado | >500% | Mensal |
| **Horas economizadas** | soma de tempo economizado pela IA | afiliado | >15h/mês | Mensal |
| **Skills ativas** | skills instaladas em uso | afiliado | ≥3 | Mensal |
| **Coorte quente** | % base engajada últimos 7d | afiliado | >30% | Semanal |

### Categoria 6 — White-Label (Nível 5)

| KPI | Fórmula | Owner | Target | Cadência |
|-----|---------|-------|--------|----------|
| **GMV do parceiro** | receita transacionada via WL | WL Account | crescente | Mensal |
| **Tenants do parceiro** | sub-clientes ativos | WL Account | >100 | Mensal |
| **Health score** | score composto (uso + satisfação + pagamento) | WL Account | >0.7 | Trimestral |
| **NPS do parceiro** | NPS medido | WL Account | >55 | Trimestral |
| **Custo por tenant ativo** | custo total / tenants ativos | WL Account | <R$50 | Mensal |

---

## 📐 Fórmulas Auxiliares

### ROI Nexus (4 dimensões)

```
ROI Nexus = Direto + Produtividade + Estratégico + Sistêmico
```

**ROI Direto:**
```
(receita_atribuível - custo_total) / custo_total × 100%
```

**ROI Produtividade:**
```
(horas_economizadas × valor_hora) / custo_ia × 100%
```

**ROI Estratégico:**
```
opções_criadas × valor_opcional / custo_investimento
```

**ROI Sistêmico:**
```
externalidades_positivas / custo_participacao
```

### Calibração (Expected Calibration Error)

```
ECE = Σ |confiança_predita - acurácia_real| × n_bucket / N_total
```

Target: ECE ≤ 0.05.

### Health Score de White-Label

```
health_score = 0.4 × uso + 0.3 × satisfação + 0.3 × pagamento
```

Cada componente normalizado [0, 1].

---

## 📊 Reporting Cadence

| Cadência | KPIs | Audiência |
|----------|------|-----------|
| **Tempo real** | Latência, erro, throughput | SRE |
| **Diário** | Receita, MAU, conversion | Head de Operações |
| **Semanal** | Coorte, funil, campanha | Head de Marketing |
| **Mensal** | MRR, churn, NPS, marketplace | C-Suite |
| **Trimestral** | ROI, estratégia, roadmaps | Conselho |
| **Anual** | LTV, CAC, ROI anual | Board / Investidores |

---

## 📚 Documentos Relacionados

- [Knowledge-base: `01-modelo-ioaid.md`](01-modelo-ioaid.md)
- [Knowledge-base: `04-conformidade-anatel.md`](04-conformidade-anatel.md)
- [Knowledge-base: `07-modelo-sho.md`](07-modelo-sho.md)
- [Apostila 15 — Métricas & ROI do Ecossistema](../../apostilas/15-metricas-roi-ecossistema.md)
- [Best-practice: `01-error-handling.md`](../best-practices/01-error-handling.md)

## 👥 Ownership

- **Owner:** Head de Operações + Head de Dados
- **Reviewers:** C-Suite, Conselho Técnico
- **Cadência de revisão:** Trimestral

---

*Nexus Affil'IA'te · Lib-Nexus · knowledge-base/08-kpis-oficiais-nexus.md · v1.0 · Julho 2026*
