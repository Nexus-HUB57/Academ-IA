---
title: "Tutorial 23 · Deploy de Agentes IA com Monitoramento Prometheus + Grafana"
subtitle: "Como colocar agentes em produção com observabilidade nativa"
author: "Equipo Nexus · Ravi (CTO/AI)"
version: "1.0.0"
date: 2026-07-26
pattern: "MMN_IA"
---

**Tutorial 23 · Deploy de Agentes IA com Monitoramento Prometheus + Grafana**

*Como colocar agentes em produção com métricas, traces, logs e alertas. Stack completa de observabilidade para sistemas de IA multi-tenant.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 O que Você Vai Conquistar

Em 1h30, você vai:

1. Fazer deploy de um agente IA em container
2. Instalar Prometheus + Grafana + Loki
3. Expor métricas nativas (latência, tokens, custo, erros)
4. Criar dashboards prontos
5. Configurar alertas Slack/PagerDuty

**Pré-requisitos:**
- Docker + Docker Compose
- Conta em cloud (GCP, AWS, DigitalOcean, etc)
- Conhecimento básico de Linux
- Agente Nexus Affil'IA'te já configurado localmente

---

## 🏗️ Arquitetura do Stack

```
┌─────────────────┐     ┌─────────────────┐
│  Agent Service  │────▶│   Prometheus    │──▶┌──────────┐
│   (FastAPI)     │     │   (scrape)      │   │ Grafana  │
│  /metrics       │     └─────────────────┘   │  (UI)    │
└────────┬────────┘            │               └──────────┘
         │                     ▼
         │            ┌─────────────────┐
         └───────────▶│      Loki       │──▶┌──────────┐
                      │  (logs agreg)   │   │  Grafana │
                      └─────────────────┘   └──────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │  Alertmanager   │──▶ Slack / PagerDuty
                     └─────────────────┘
```

---

## 📦 Stack de Arquivos

```
nexus-agent-stack/
├── docker-compose.yml
├── .env
├── prometheus/
│   ├── prometheus.yml
│   └── alerts/
│       └── agent_alerts.yml
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── datasources.yml
│   │   └── dashboards/
│   │       └── dashboards.yml
│   └── dashboards/
│       ├── agent_overview.json
│       └── cost_per_tenant.json
├── loki/
│   └── loki-config.yml
├── alertmanager/
│   └── alertmanager.yml
└── agent/
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py
    ├── metrics.py
    └── tenants/
        └── config_default.yaml
```

---

## 🐍 Passo 1: Agente com Métricas (FastAPI + prometheus-client)

### `agent/requirements.txt`

```
fastapi==0.115.0
uvicorn[standard]==0.32.0
prometheus-client==0.21.0
python-multipart==0.0.12
pydantic==2.9.2
structlog==24.4.0
httpx==0.27.2
tenacity==9.0.0
nexus-affil-IA-sdk==1.3.2
```

### `agent/metrics.py`

```python
"""
Métricas Prometheus nativas para o agente.
"""
from prometheus_client import (
    Counter, Histogram, Gauge, Summary,
    CollectorRegistry, generate_latest,
    CONTENT_TYPE_LATEST
)
import time
from functools import wraps

REGISTRY = CollectorRegistry()

# === Métricas de Negócio ===
REQUEST_COUNT = Counter(
    'nexus_agent_requests_total',
    'Total de requests recebidos',
    labelnames=['tenant_id', 'endpoint', 'status'],
    registry=REGISTRY
)

REQUEST_LATENCY = Histogram(
    'nexus_agent_request_latency_seconds',
    'Latência de requests',
    labelnames=['tenant_id', 'endpoint'],
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0),
    registry=REGISTRY
)

TOKENS_USED = Counter(
    'nexus_agent_tokens_total',
    'Tokens consumidos',
    labelnames=['tenant_id', 'model', 'direction'],
    registry=REGISTRY
)

COST_USD = Counter(
    'nexus_agent_cost_usd_total',
    'Custo em USD',
    labelnames=['tenant_id', 'model'],
    registry=REGISTRY
)

ACTIVE_USERS = Gauge(
    'nexus_agent_active_users',
    'Usuários ativos (últimos 5 min)',
    labelnames=['tenant_id'],
    registry=REGISTRY
)

# === Métricas de Saúde ===
AGENT_UP = Gauge(
    'nexus_agent_up',
    '1 se agente está respondendo health check',
    registry=REGISTRY
)

DEPENDENCIES_UP = Gauge(
    'nexus_agent_dependencies_up',
    '1 se dependência está OK',
    labelnames=['dependency'],
    registry=REGISTRY
)

# === Métricas de Erro ===
ERROR_COUNT = Counter(
    'nexus_agent_errors_total',
    'Total de erros',
    labelnames=['tenant_id', 'error_type'],
    registry=REGISTRY
)

# === Métricas de Judge Revisor ===
JUDGE_REVISIONS = Counter(
    'nexus_agent_judge_revisions_total',
    'Revisões do Judge',
    labelnames=['tenant_id', 'verdict'],
    registry=REGISTRY
)

# === Decorador para instrumentação automática ===
def track_request(tenant_id: str, endpoint: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.time()
            status = "success"
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status = "error"
                ERROR_COUNT.labels(
                    tenant_id=tenant_id,
                    error_type=type(e).__name__
                ).inc()
                raise
            finally:
                duration = time.time() - start
                REQUEST_LATENCY.labels(
                    tenant_id=tenant_id,
                    endpoint=endpoint
                ).observe(duration)
                REQUEST_COUNT.labels(
                    tenant_id=tenant_id,
                    endpoint=endpoint,
                    status=status
                ).inc()
        return wrapper
    return decorator


def render_metrics():
    """Renderiza métricas para endpoint /metrics"""
    return generate_latest(REGISTRY), CONTENT_TYPE_LATEST
```

### `agent/main.py`

```python
"""
Agente Nexus com métricas nativas.
"""
import os
import time
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response, JSONResponse
from contextlib import asynccontextmanager
import structlog

from metrics import (
    track_request, render_metrics,
    AGENT_UP, DEPENDENCIES_UP,
    TOKENS_USED, COST_USD, ACTIVE_USERS,
    JUDGE_REVISIONS
)

logger = structlog.get_logger()
app = FastAPI(
    title="Nexus Agent",
    version="1.3.0",
    description="Agente de afiliação com observabilidade nativa"
)

# Custos por modelo (USD por 1k tokens)
COST_TABLE = {
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "claude-sonnet-4-5": {"input": 0.003, "output": 0.015},
    "claude-haiku-4-5": {"input": 0.0008, "output": 0.004},
}

# Usuários ativos (em memória, simples)
active_users = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown hooks"""
    AGENT_UP.set(1)
    DEPENDENCIES_UP.labels(dependency="openai").set(1)
    DEPENDENCIES_UP.labels(dependency="anthropic").set(1)
    DEPENDENCIES_UP.labels(dependency="redis").set(1)
    logger.info("agent_started", version="1.3.0")
    yield
    AGENT_UP.set(0)
    logger.info("agent_stopped")


@app.get("/health")
async def health():
    return {"status": "ok", "uptime_seconds": time.time()}


@app.get("/ready")
async def ready():
    """Readiness check para k8s"""
    deps_ok = all(
        DEPENDENCIES_UP.labels(dependency=d)._value.get() == 1
        for d in ["openai", "anthropic", "redis"]
    )
    if not deps_ok:
        raise HTTPException(status_code=503, detail="dependencies not ready")
    return {"status": "ready"}


@app.get("/metrics")
async def metrics():
    """Endpoint Prometheus"""
    data, content_type = render_metrics()
    return Response(content=data, media_type=content_type)


@app.post("/v1/agent/invoke")
@track_request(tenant_id="demo", endpoint="invoke")
async def invoke(request: Request):
    """Endpoint principal do agente"""
    body = await request.json()
    tenant_id = body.get("tenant_id", "demo")
    user_id = body.get("user_id", "anonymous")
    message = body.get("message", "")

    # Marcar usuário como ativo
    active_users[user_id] = time.time()
    ACTIVE_USERS.labels(tenant_id=tenant_id).set(
        len([t for t in active_users.values() if time.time() - t < 300])
    )

    # Chamar LLM (mock para o exemplo)
    model = "gpt-4o-mini"
    input_tokens = len(message.split()) * 1.3
    output_tokens = 150

    # Métricas de tokens
    TOKENS_USED.labels(
        tenant_id=tenant_id,
        model=model,
        direction="input"
    ).inc(input_tokens)
    TOKENS_USED.labels(
        tenant_id=tenant_id,
        model=model,
        direction="output"
    ).inc(output_tokens)

    # Métricas de custo
    cost = (
        (input_tokens / 1000) * COST_TABLE[model]["input"] +
        (output_tokens / 1000) * COST_TABLE[model]["output"]
    )
    COST_USD.labels(tenant_id=tenant_id, model=model).inc(cost)

    return JSONResponse({
        "response": f"Processado: {message[:50]}",
        "tokens": {"input": int(input_tokens), "output": output_tokens},
        "cost_usd": round(cost, 6),
    })


@app.post("/v1/judge/review")
@track_request(tenant_id="system", endpoint="judge")
async def judge_review(request: Request):
    """Judge Revisor — métricas de revisão"""
    body = await request.json()
    tenant_id = body.get("tenant_id", "demo")
    verdict = body.get("verdict", "ok")  # ok | revise | block

    JUDGE_REVISIONS.labels(
        tenant_id=tenant_id,
        verdict=verdict
    ).inc()

    return {"acknowledged": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
```

### `agent/Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📊 Passo 2: Prometheus

### `prometheus/prometheus.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'nexus-prod'
    region: 'us-east-1'

# Load alert rules
rule_files:
  - "alerts/*.yml"

# Alertmanager
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

# Scrape configs
scrape_configs:
  # === Agente ===
  - job_name: 'nexus-agent'
    metrics_path: /metrics
    static_configs:
      - targets: ['agent:8000']
        labels:
          service: 'nexus-agent'
          env: 'production'

  # === Node Exporter (host) ===
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  # === cAdvisor (containers) ===
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  # === PostgreSQL ===
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  # === Redis ===
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

### `prometheus/alerts/agent_alerts.yml`

```yaml
groups:
  - name: nexus-agent
    interval: 30s
    rules:

      # === Latência ===
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum by (le, tenant_id) (rate(nexus_agent_request_latency_seconds_bucket[5m]))
          ) > 2
        for: 5m
        labels:
          severity: warning
          team: sre
        annotations:
          summary: "Latência p95 > 2s no tenant {{ $labels.tenant_id }}"
          description: "Latência p95 está em {{ $value }}s nos últimos 5min"
          runbook: "https://wiki.nexus.com/runbook/high-latency"

      - alert: CriticalLatency
        expr: |
          histogram_quantile(0.95,
            sum by (le, tenant_id) (rate(nexus_agent_request_latency_seconds_bucket[5m]))
          ) > 10
        for: 2m
        labels:
          severity: critical
          team: sre
        annotations:
          summary: "Latência p95 > 10s no tenant {{ $labels.tenant_id }}"
          description: "Latência crítica: {{ $value }}s"
          action: "Considerar rollback ou scale up"

      # === Erros ===
      - alert: HighErrorRate
        expr: |
          (
            sum by (tenant_id) (rate(nexus_agent_errors_total[5m]))
            /
            sum by (tenant_id) (rate(nexus_agent_requests_total[5m]))
          ) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Taxa de erro > 5% no tenant {{ $labels.tenant_id }}"

      - alert: AgentDown
        expr: nexus_agent_up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Agente Nexus está down!"
          action: "Página SRE - verificar container"

      # === Custo ===
      - alert: HighCostPerHour
        expr: |
          sum by (tenant_id) (
            increase(nexus_agent_cost_usd_total[1h])
          ) > 50
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Tenant {{ $labels.tenant_id }} gastou >$50/h"

      # === Dependências ===
      - alert: OpenAIDown
        expr: nexus_agent_dependencies_up{dependency="openai"} == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "OpenAI está inacessível"

      - alert: AnthropicDown
        expr: nexus_agent_dependencies_up{dependency="anthropic"} == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Anthropic está inacessível"
```

---

## 🚨 Passo 3: Alertmanager

### `alertmanager/alertmanager.yml`

```yaml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'tenant_id', 'severity']
  group_wait: 10s
  group_interval: 10m
  repeat_interval: 12h
  receiver: 'default'

  routes:
    - match:
        severity: critical
      receiver: 'pagerduty'
      continue: true

    - match:
        severity: warning
      receiver: 'slack-warning'

receivers:
  - name: 'default'
    webhook_configs:
      - url: 'http://hook.nexus.com/default'

  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: '${PAGERDUTY_KEY}'
        description: '{{ .GroupLabels.alertname }}: {{ .CommonAnnotations.summary }}'
        severity: '{{ .CommonLabels.severity }}'

  - name: 'slack-warning'
    slack_configs:
      - api_url: '${SLACK_WEBHOOK_URL}'
        channel: '#nexus-alerts'
        title: '⚠️ {{ .GroupLabels.alertname }}'
        text: '{{ .CommonAnnotations.summary }}\n{{ .CommonAnnotations.description }}'
```

---

## 📈 Passo 4: Grafana + Dashboards

### `grafana/provisioning/datasources/datasources.yml`

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true

  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
```

### `grafana/dashboards/agent_overview.json`

```json
{
  "dashboard": {
    "title": "Nexus Agent · Overview",
    "panels": [
      {
        "id": 1,
        "title": "Requests/s por Tenant",
        "type": "timeseries",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
        "targets": [{
          "expr": "sum by (tenant_id) (rate(nexus_agent_requests_total[1m]))",
          "legendFormat": "{{tenant_id}}"
        }]
      },
      {
        "id": 2,
        "title": "Latência p50/p95/p99",
        "type": "timeseries",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
        "targets": [
          {
            "expr": "histogram_quantile(0.50, sum by (le) (rate(nexus_agent_request_latency_seconds_bucket[5m])))",
            "legendFormat": "p50"
          },
          {
            "expr": "histogram_quantile(0.95, sum by (le) (rate(nexus_agent_request_latency_seconds_bucket[5m])))",
            "legendFormat": "p95"
          },
          {
            "expr": "histogram_quantile(0.99, sum by (le) (rate(nexus_agent_request_latency_seconds_bucket[5m])))",
            "legendFormat": "p99"
          }
        ]
      },
      {
        "id": 3,
        "title": "Custo Acumulado por Tenant (USD/h)",
        "type": "barchart",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
        "targets": [{
          "expr": "sum by (tenant_id) (increase(nexus_agent_cost_usd_total[1h]))",
          "legendFormat": "{{tenant_id}}"
        }]
      },
      {
        "id": 4,
        "title": "Taxa de Erro (%)",
        "type": "stat",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8},
        "targets": [{
          "expr": "sum(rate(nexus_agent_errors_total[5m])) / sum(rate(nexus_agent_requests_total[5m])) * 100"
        }],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 1},
                {"color": "red", "value": 5}
              ]
            }
          }
        }
      }
    ]
  }
}
```

---

## 🐳 Passo 5: Docker Compose

### `docker-compose.yml`

```yaml
version: '3.9'

services:
  # === Agente ===
  agent:
    build: ./agent
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
    logging:
      driver: loki
      options:
        loki-url: "http://loki:3100/loki/api/v1/push"
        loki-batch-size: "400"

  # === Prometheus ===
  prometheus:
    image: prom/prometheus:v2.55.0
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./prometheus/alerts:/etc/prometheus/alerts:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'
      - '--web.enable-lifecycle'
    restart: unless-stopped

  # === Grafana ===
  grafana:
    image: grafana/grafana:11.2.0
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
      - ./grafana/dashboards:/var/lib/grafana/dashboards:ro
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus
    restart: unless-stopped

  # === Loki ===
  loki:
    image: grafana/loki:3.2.1
    ports:
      - "3100:3100"
    volumes:
      - ./loki/loki-config.yml:/etc/loki/local-config.yaml:ro
      - loki_data:/loki
    restart: unless-stopped

  # === Promtail (envia logs para Loki) ===
  promtail:
    image: grafana/promtail:3.2.1
    volumes:
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - ./loki/promtail-config.yml:/etc/promtail/config.yml:ro
    depends_on:
      - loki
    restart: unless-stopped

  # === Alertmanager ===
  alertmanager:
    image: prom/alertmanager:v0.27.0
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager/alertmanager.yml:/etc/alertmanager/alertmanager.yml:ro
    environment:
      - SLACK_WEBHOOK_URL=${SLACK_WEBHOOK_URL}
      - PAGERDUTY_KEY=${PAGERDUTY_KEY}
    restart: unless-stopped

  # === Node Exporter ===
  node-exporter:
    image: prom/node-exporter:v1.8.2
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--path.rootfs=/rootfs'
    restart: unless-stopped

  # === cAdvisor ===
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:v0.49.1
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    restart: unless-stopped

  # === Redis ===
  redis:
    image: redis:7.4-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
  loki_data:
  redis_data:
```

### `.env`

```bash
# === LLM Keys ===
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# === Grafana ===
GRAFANA_PASSWORD=senha_segura_aqui

# === Alerts ===
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
PAGERDUTY_KEY=...
```

---

## 🚀 Passo 6: Deploy e Verificação

### 1. Subir o stack

```bash
cd nexus-agent-stack
docker compose up -d
docker compose ps
```

### 2. Verificar saúde

```bash
# Health do agente
curl http://localhost:8000/health

# Métricas Prometheus
curl http://localhost:8000/metrics | head -20

# Prometheus targets
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health}'

# Grafana
open http://localhost:3000  # admin / $GRAFANA_PASSWORD
```

### 3. Gerar carga de teste

```bash
# 100 requests em paralelo
for i in {1..100}; do
  curl -X POST http://localhost:8000/v1/agent/invoke \
    -H "Content-Type: application/json" \
    -d "{\"tenant_id\": \"tenant_a\", \"user_id\": \"user_$i\", \"message\": \"Teste $i\"}" &
done
wait

# Verificar métricas
curl http://localhost:8000/metrics | grep nexus_agent
```

### 4. Acessar dashboards

- **Grafana:** http://localhost:3000
- **Prometheus:** http://localhost:9090
- **Alertmanager:** http://localhost:9093

---

## 🔥 Passo 7: Deploy em Produção (k8s)

### `k8s/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nexus-agent
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nexus-agent
  template:
    metadata:
      labels:
        app: nexus-agent
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      containers:
        - name: agent
          image: nexus-registry.com/agent:1.3.0
          ports:
            - containerPort: 8000
          resources:
            requests:
              memory: "512Mi"
              cpu: "500m"
            limits:
              memory: "1Gi"
              cpu: "1000m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
          env:
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: nexus-secrets
                  key: openai-key
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nexus-agent-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nexus-agent
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Pods
      pods:
        metric:
          name: nexus_agent_request_latency_seconds
        target:
          type: AverageValue
          averageValue: "1"
```

---

## 💰 Estimativa de Custos (Cloud)

| Componente | Self-hosted | GCP | AWS | DigitalOcean |
|-----------|-------------|-----|-----|--------------|
| Agente (3 réplicas) | VPS $20 | GKE $50 | EKS $73 | DOKS $24 |
| Prometheus | Incluso | $30 | $35 | Incluso |
| Grafana | Incluso | $15 | $20 | Incluso |
| Loki | $10 storage | $25 | $30 | $10 |
| Redis | $5 | $15 | $20 | $5 |
| **Total/mês** | **$35** | **$135** | **$178** | **$39** |

**Recomendação:** comece com DigitalOcean (custo-benefício). Quando passar 1M req/dia, vá para k8s gerenciado.

---

## 🧪 Passo 8: Teste de Carga (k6)

### `load-test.js`

```javascript
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },  // ramp up
    { duration: '1m', target: 100 },  // hold
    { duration: '30s', target: 200 }, // stress
    { duration: '30s', target: 0 },   // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'],  // 95% < 2s
    http_req_failed: ['rate<0.01'],     // erro < 1%
  },
};

export default function () {
  const res = http.post(
    'http://localhost:8000/v1/agent/invoke',
    JSON.stringify({
      tenant_id: `tenant_${__VU % 10}`,
      user_id: `user_${__VU}_${__ITER}`,
      message: 'Olá, quero saber mais sobre o produto X',
    }),
    { headers: { 'Content-Type': 'application/json' } }
  );

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response has data': (r) => r.json('response') !== undefined,
  });
}
```

```bash
k6 run load-test.js
```

---

## 📚 Materiais Complementares

- `apostilas/19-observabilidade-sre-agentes-ia.md` — SRE para IA
- `apostilas/20-devops-iac-terraform-agentes.md` — IaC
- `tutoriais/14-deploy-api-ia-producao.md` — deploy básico
- `tutoriais/15-debugar-custos-openai-anthropic.md` — controle de custos
- `Lib-Nexus/best-practices/06-observabilidade-melhores-praticas.md`
- `producao/INCIDENT-RESPONSE-RUNBOOK.md` — resposta a incidentes
- `producao/NGINX-CDN-CONFIG.md` — proxy reverso

---

## 🔗 Links Externos

- Prometheus: https://prometheus.io/
- Grafana: https://grafana.com/
- Loki: https://grafana.com/oss/loki/
- FastAPI metrics: https://fastapi.tiangolo.com/
- k6 load testing: https://k6.io/

---

*AcademIA · Tutorial 23 · Deploy com Monitoramento · 2026*