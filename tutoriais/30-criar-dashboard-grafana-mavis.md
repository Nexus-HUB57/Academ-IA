---
version: "1.0-mavis-recovery"
recovery_note: "Versão recuperada após force-push de 2026-07-29. Coexiste com o canônico em tutoriais/(sem equivalente canônico).md"
title: "Tutorial 30 · Criar Dashboard Grafana para Métricas de Negócio"
description: "Como construir dashboard de métricas de negócio (MRR, LTV, conversão) com Grafana + PostgreSQL"
tags: [tutorial, 30, grafana, dashboard, metricas, postgres, business-intelligence]
tier: "Master"
duracao_estimada: "30 min"
pre_requisitos: ["tutoriais/23-deploy-monitoramento-prometheus.md"]
ultima_atualizacao: 2026-07-27
---

# Tutorial 30 · Criar Dashboard Grafana para Métricas de Negócio

> **Por que importa**: Prometheus é ótimo para métricas técnicas (latência, errors). Para métricas de NEGÓCIO (MRR, LTV, conversão), use Grafana + PostgreSQL direto. Decisões de negócio devem ser data-driven.

## 🎯 O que você vai aprender

- Conectar Grafana ao PostgreSQL de produção
- Criar 5 painéis essenciais: MRR, novos clientes, churn, conversão, LTV
- Configurar alertas de negócio no Slack
- Compartilhar dashboard com a equipe

## ⏱️ Duração: 30 minutos

---

## 📋 Passo 1: Provisionar Grafana (Docker)

```yaml
# docker-compose.grafana.yml
version: '3.8'

services:
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASS}
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_AUTH_ANONYMOUS_ENABLED=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
      - ./grafana/dashboards:/var/lib/grafana/dashboards
    restart: unless-stopped

volumes:
  grafana_data:
```

```bash
docker compose -f docker-compose.grafana.yml up -d
# Acessar: http://localhost:3000 (admin / senha do .env)
```

## 📋 Passo 2: Adicionar PostgreSQL como Data Source

Via UI: **Configuration → Data Sources → Add data source → PostgreSQL**

```yaml
# Ou via provisioning: grafana/provisioning/datasources/postgres.yml
apiVersion: 1

datasources:
  - name: PostgreSQL-Academ
    type: postgres
    access: proxy
    url: postgres:5432
    database: nexus_prod
    user: grafana_ro
    secureJsonData:
      password: ${DB_RO_PASSWORD}
    jsonData:
      sslmode: require
      maxOpenConns: 10
      maxIdleConns: 2
      connMaxLifetime: 600
    isDefault: true
```

## 📋 Passo 3: Schema de Banco (exemplo)

```sql
-- migrations/001_create_business_metrics.sql
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  plan VARCHAR(50) NOT NULL,  -- 'basic', 'pro', 'enterprise'
  mrr_cents INT NOT NULL,     -- Monthly Recurring Revenue em centavos
  status VARCHAR(20) NOT NULL, -- 'active', 'canceled', 'past_due'
  started_at TIMESTAMPTZ NOT NULL,
  canceled_at TIMESTAMPTZ
);

CREATE TABLE payments (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  amount_cents INT NOT NULL,
  status VARCHAR(20) NOT NULL, -- 'succeeded', 'failed', 'refunded'
  created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE conversions (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  funnel_step VARCHAR(50) NOT NULL, -- 'landing', 'signup', 'trial', 'paid'
  created_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX idx_subscriptions_status_started ON subscriptions(status, started_at);
CREATE INDEX idx_payments_status_created ON payments(status, created_at);
CREATE INDEX idx_conversions_funnel_created ON conversions(funnel_step, created_at);
```

## 📋 Passo 4: Dashboard — 5 Painéis Essenciais

### 4.1 MRR ao Longo do Tempo

```sql
-- Query
SELECT
  date_trunc('day', started_at) AS time,
  SUM(mrr_cents) / 100.0 AS mrr_brl
FROM subscriptions
WHERE status = 'active'
  AND started_at >= $__timeFrom()
  AND started_at <= $__timeTo()
GROUP BY time
ORDER BY time;
```

**Tipo de painel**: Time Series
**Unit**: BRL (R$)
**Config**: 
- Thresholds: 0 (red), 50k (yellow), 100k (green)
- Display: linha + área

### 4.2 Novos Clientes vs Churn

```sql
-- Novos clientes (paid conversions)
SELECT
  date_trunc('day', p.created_at) AS time,
  COUNT(DISTINCT p.user_id) AS new_customers
FROM payments p
WHERE p.status = 'succeeded'
  AND p.amount_cents > 0
  AND p.created_at >= $__timeFrom()
  AND p.created_at <= $__timeTo()
GROUP BY time
ORDER BY time;
```

```sql
-- Churn
SELECT
  date_trunc('day', canceled_at) AS time,
  COUNT(DISTINCT user_id) AS churned_customers
FROM subscriptions
WHERE status = 'canceled'
  AND canceled_at >= $__timeFrom()
  AND canceled_at <= $__timeTo()
GROUP BY time
ORDER BY time;
```

**Tipo**: Time Series (2 séries no mesmo gráfico)
**Display**: Bar + line (novos em verde, churn em vermelho)

### 4.3 Funil de Conversão

```sql
SELECT
  funnel_step,
  COUNT(DISTINCT user_id) AS users
FROM conversions
WHERE created_at >= $__timeFrom()
  AND created_at <= $__timeTo()
GROUP BY funnel_step
ORDER BY CASE funnel_step
  WHEN 'landing' THEN 1
  WHEN 'signup' THEN 2
  WHEN 'trial' THEN 3
  WHEN 'paid' THEN 4
END;
```

**Tipo**: Bar Gauge
**Config**: Color thresholds por etapa

### 4.4 LTV por Cohort

```sql
WITH cohorts AS (
  SELECT
    user_id,
    date_trunc('month', started_at) AS cohort_month
  FROM subscriptions
  WHERE status IN ('active', 'canceled')
),
revenue_per_user AS (
  SELECT
    c.cohort_month,
    s.user_id,
    SUM(p.amount_cents) / 100.0 AS total_revenue
  FROM cohorts c
  JOIN payments p ON p.user_id = c.user_id AND p.status = 'succeeded'
  JOIN subscriptions s ON s.user_id = c.user_id
  GROUP BY c.cohort_month, s.user_id
)
SELECT
  cohort_month AS time,
  AVG(total_revenue) AS avg_ltv
FROM revenue_per_user
WHERE cohort_month >= $__timeFrom()
GROUP BY cohort_month
ORDER BY cohort_month;
```

**Tipo**: Bar Chart (horizontal)
**Config**: Stacked por mês de cohort

### 4.5 Top 10 Clientes por MRR

```sql
SELECT
  u.email,
  s.mrr_cents / 100.0 AS mrr_brl,
  s.plan
FROM subscriptions s
JOIN users u ON u.id = s.user_id
WHERE s.status = 'active'
ORDER BY s.mrr_cents DESC
LIMIT 10;
```

**Tipo**: Table
**Colunas**: email, plan, mrr_brl
**Color**: mrr_brl gradient

## 📋 Passo 5: Provisionar Dashboard Automaticamente

```yaml
# grafana/provisioning/dashboards/business.yml
apiVersion: 1

providers:
  - name: 'Business Metrics'
    orgId: 1
    folder: 'AcademIA'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 30
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards
```

```bash
# Exportar dashboard criado via UI para JSON
# UI → Dashboard → Share → Export → Save to file

# Salvar em grafana/dashboards/business-metrics.json
```

## 📋 Passo 6: Alertas no Slack

```yaml
# grafana/provisioning/alerting/business.yml
apiVersion: 1

groups:
  - orgId: 1
    name: business-metrics
    folder: AcademIA
    interval: 5m
    rules:
      - uid: mrr-drop
        title: "MRR caindo mais de 10% em 7 dias"
        condition: C
        data:
          - refId: A
            datasourceUid: PostgreSQL-Academ
            relativeTimeRange:
              from: 604800  # 7 dias
              to: 0
            model:
              rawSql: |
                WITH current_mrr AS (
                  SELECT SUM(mrr_cents) AS mrr
                  FROM subscriptions
                  WHERE status = 'active' AND started_at <= NOW()
                ),
                past_mrr AS (
                  SELECT SUM(mrr_cents) AS mrr
                  FROM subscriptions
                  WHERE status = 'active' AND started_at <= NOW() - INTERVAL '7 days'
                )
                SELECT
                  ((SELECT mrr FROM current_mrr) - (SELECT mrr FROM past_mrr))::float
                  / NULLIF((SELECT mrr FROM past_mrr), 0) AS mrr_change_pct
          - refId: C
            datasourceUid: __expr__
            model:
              type: threshold
              conditions:
                - evaluator:
                    type: lt
                    params: [-0.10]
        noDataState: OK
        execErrState: Alerting
        for: 5m
        annotations:
          summary: "MRR caindo {{ printf \"%.1f%%\" (mul $values.A.Value -1) }}"
        labels:
          severity: critical
          channel: slack-business
        # Configurar contact point no Slack via UI
```

## 📋 Passo 7: Compartilhar com Equipe

```bash
# 1. Criar API key para embed
# UI → Configuration → API Keys → New API Key (Viewer role)

# 2. Link compartilhável
http://localhost:3000/d/abc123/business-metrics?orgId=1&from=now-30d&to=now

# 3. Snapshot para relatório
# UI → Dashboard → Share → Snapshot
# Gera URL pública com data específica
```

## 🎓 Próximo Passo

- **Tutoriais relacionados**:
  - `tutoriais/23-deploy-monitoramento-prometheus.md` (métricas técnicas)
  - `tutoriais/26-monitorar-com-sentry.md` (error tracking)
  - `tutoriais/08-primeiro-ab-test.md` (análise estatística)
- **Curso**: `cursos/master/00-otimizacao-conversao.md` (CRO)
- **Apostila**: `apostilas/15-metricas-roi-ecossistema.md`

---

**Tutorial criado em 2026-07-27** · Mavis Agent
**Versão 1.0** · Mantido em `tutoriais/30-criar-dashboard-grafana.md`
