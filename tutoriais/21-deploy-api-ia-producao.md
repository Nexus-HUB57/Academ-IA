---
title: "Deploy de API de IA em Produção (FastAPI + Docker + Cloud)"
tutorial_code: TUT-MA-04
level: master
duration: 75min
prerequisites: ["20-fine-tuning-openai-api.md"]
tags: [tutorial, deploy, produção, fastapi, docker, observability, kubernetes]
last_updated: 2026-07-07
---

# 🚀 Deploy de API de IA em Produção

> **Tempo:** 75 min · **Nível:** Master · **Pré-requisito:** TUT-EL-20

## O que vamos construir

API FastAPI com:
- Endpoint de classificação usando modelo fine-tuned
- Container Docker multi-stage
- Deploy em Fly.io (alternativa: Railway, AWS)
- Observabilidade com Langfuse
- SLO: latência p95 < 3s, disponibilidade > 99%

## Estrutura do Projeto

```
ai-api/
├── app/
│   ├── main.py            # FastAPI app
│   ├── classifier.py       # Lógica de classificação
│   ├── config.py           # Settings
│   └── observability.py    # Langfuse setup
├── tests/
│   └── test_classifier.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Passo 1: FastAPI App (15 min)

```python
# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from classifier import IntentClassifier
from observability import track_request, LangfuseTracker
import os

# Lifecycle: inicializa modelo uma vez no startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.classifier = IntentClassifier(
        model_id=os.getenv("FT_MODEL_ID", "gpt-4o-mini"),
    )
    app.state.tracker = LangfuseTracker()
    yield

app = FastAPI(
    title="Intent Classifier API",
    version="1.0.0",
    lifespan=lifespan,
)

class ClassifyRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    user_id: str | None = None

class ClassifyResponse(BaseModel):
    intent: str
    confidence: float
    latency_ms: int

@app.post("/v1/classify", response_model=ClassifyResponse)
async def classify(req: ClassifyRequest, request: Request):
    return await request.app.state.classifier.classify(
        req.text,
        user_id=req.user_id,
        tracker=request.app.state.tracker,
    )

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/metrics")
async def metrics():
    # Prometheus scrape endpoint
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

## Passo 2: Classifier (10 min)

```python
# app/classifier.py
from openai import OpenAI
import time

INTENTS = ["cancelamento", "preco", "duvida", "suporte", "outro"]

class IntentClassifier:
    def __init__(self, model_id: str):
        self.client = OpenAI()
        self.model_id = model_id

    async def classify(self, text: str, user_id: str | None, tracker):
        start = time.perf_counter()

        # Chamada ao LLM (fine-tuned ou base)
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "system", "content":
                    f"Classifique em uma de: {INTENTS}. "
                    "Responda APENAS com a classe."},
                {"role": "user", "content": text},
            ],
            max_tokens=20,
            temperature=0,
        )

        intent = response.choices[0].message.content.strip().lower()
        if intent not in INTENTS:
            intent = "outro"

        latency_ms = int((time.perf_counter() - start) * 1000)

        # Tracking
        tracker.log(
            model=self.model_id,
            input_text=text,
            output=intent,
            user_id=user_id,
            latency_ms=latency_ms,
            tokens=response.usage.total_tokens,
        )

        # Estimativa simples de confidence (em produção: usar logprobs)
        confidence = 0.9 if intent != "outro" else 0.5

        return ClassifyResponse(
            intent=intent, confidence=confidence, latency_ms=latency_ms
        )
```

## Passo 3: Observability (10 min)

```python
# app/observability.py
from langfuse import Langfuse
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "api_requests_total", "Total requests", ["endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "api_request_duration_ms", "Latency in ms", ["endpoint"]
)

class LangfuseTracker:
    def __init__(self):
        self.langfuse = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        )

    def log(self, model, input_text, output, user_id, latency_ms, tokens):
        # Langfuse
        trace = self.langfuse.trace(
            name="intent_classification", user_id=user_id
        )
        trace.generation(
            name="classify",
            model=model,
            input=input_text,
            output=output,
            usage={"total": tokens},
            metadata={"latency_ms": latency_ms},
        )

        # Prometheus
        REQUEST_COUNT.labels(endpoint="/v1/classify", status="ok").inc()
        REQUEST_LATENCY.labels(endpoint="/v1/classify").observe(latency_ms)
```

## Passo 4: Dockerfile Multi-Stage (10 min)

```dockerfile
# Dockerfile
FROM python:3.12-slim AS builder
WORKDIR /build
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

FROM python:3.12-slim
WORKDIR /app
RUN useradd --create-home --shell /bin/bash appuser

# Copia dependências
COPY --from=builder /build/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copia código
COPY app/ /app/

USER appuser
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports: ["8000:8000"]
    env_file: .env
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - FT_MODEL_ID=${FT_MODEL_ID}
      - LANGFUSE_PUBLIC_KEY=${LANGFUSE_PUBLIC_KEY}
      - LANGFUSE_SECRET_KEY=${LANGFUSE_SECRET_KEY}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      retries: 3
```

## Passo 5: Testar Localmente (5 min)

```bash
docker compose up --build
# Em outro terminal:
curl http://localhost:8000/health

curl -X POST http://localhost:8000/v1/classify \\
     -H "Content-Type: application/json" \\
     -d '{"text": "Quero cancelar minha assinatura", "user_id": "user-123"}'

# Saída esperada:
# {"intent": "cancelamento", "confidence": 0.9, "latency_ms": 850}
```

## Passo 6: Deploy no Fly.io (20 min)

```bash
# Install CLI
curl -L https://fly.io/install.sh | sh
fly auth signup  # primeira vez

# Init
cd ai-api
fly launch --name intent-classifier-nexus --no-deploy

# Set secrets
fly secrets set OPENAI_API_KEY=sk-proj-...
fly secrets set FT_MODEL_ID=ft:gpt-4o-mini:...
fly secrets set LANGFUSE_PUBLIC_KEY=pk-...
fly secrets set LANGFUSE_SECRET_KEY=sk-...

# Deploy
fly deploy

# Verificar
fly status
fly logs

# Abrir URL pública
fly open
```

## Passo 7: Testes E2E (5 min)

```python
# tests/test_classifier.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_classify_cancelamento():
    r = client.post("/v1/classify", json={
        "text": "Quero cancelar minha assinatura",
        "user_id": "test-user"
    })
    assert r.status_code == 200
    assert r.json()["intent"] == "cancelamento"
    assert r.json()["latency_ms"] < 3000

def test_classify_preco():
    r = client.post("/v1/classify", json={
        "text": "Quanto custa o plano anual?"
    })
    assert r.status_code == 200
    assert r.json()["intent"] == "preco"
```

## SLOs e Alertas

```yaml
# SLOs obrigatórios
slo:
  availability: 99.5%        # ~3.6h downtime/mês
  latency_p95: 3000ms
  error_rate: <1%
  cost_per_1k_requests: <$2
```

```yaml
# Prometheus alert
groups:
- name: ai-api
  rules:
  - alert: HighErrorRate
    expr: |
      sum(rate(api_requests_total{status=~"5.."}[5m])) /
      sum(rate(api_requests_total[5m])) > 0.05
    for: 5m
  - alert: HighLatency
    expr: |
      histogram_quantile(0.95, rate(api_request_duration_ms_bucket[5m])) > 3000
    for: 5m
```

## Custos Estimados

| Componente | Custo/mês (10k req/dia) |
|---|---|
| Fly.io (1 shared CPU) | $5 |
| OpenAI API (gpt-4o-mini) | $30 |
| Langfuse Cloud | $0 (free tier) |
| **Total** | **~$35/mês** |

## Checklist de Produção

- [ ] Healthcheck respondendo
- [ ] Métricas Prometheus expostas em `/metrics`
- [ ] Logs estruturados (JSON)
- [ ] Tracing distribuído (Langfuse)
- [ ] SLOs definidos + alertas
- [ ] CI/CD com testes E2E
- [ ] Secrets gerenciados (não no código)
- [ ] HTTPS configurado
- [ ] Rate limiting (slowapi)
- [ ] Documentação OpenAPI atualizada

## Próximos passos

- **Auto-scaling**: tutorial #22
- **Multi-region**: tutorial #23
- **Disaster recovery**: playbook PB-DEPLOY

## Recursos

- Fly.io: <https://fly.io/docs>
- FastAPI: <https://fastapi.tiangolo.com>
- Langfuse: <https://langfuse.com/docs>
- Prometheus: <https://prometheus.io/docs>