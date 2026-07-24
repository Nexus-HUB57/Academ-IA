---
title: "Módulo Master-05 · Slides · Deploy de IA em Produção"
description: "[MAVIS-EXTENDIDO 12 cenas detalhadas] — Versão estendida. Padrão principal do remote (genspark_dev): 05-deploy-em-producao-slides.md — Slides visuais para acompanhar o vídeo do módulo 05 da Trilha Master"
tags: [slides, master, modulo-05, deploy, fastapi, docker, kubernetes, observabilidade]
modulo: master-05
trilha: Master
ordem: 5
total_slides: 11
pattern: "DEPLOY_IA"
---

> ⚠️ **VERSÃO ESTENDIDA MAVIS** (12 cenas, 60+ páginas) — complementar ao roteiro oficial do módulo em `05-deploy-em-producao-slides.md` (5 cenas). Mantido para uso em videoaulas longas, workshops, e sessões de mentoria 1:1.

# 📊 Slides · Master 05 · Deploy de IA em Produção

> Material visual para acompanhar o vídeo. Pipeline completo: API → Docker → Orquestração → Observabilidade.

## 🎨 Paleta de Cores

```
Primary:    #b78cff (purple — Master)
Secondary:  #63eaff (cyan)
Accent:     #facc15 (gold)
Success:    #10b981 (green — métricas saudáveis)
Error:      #ef4444 (red — incidentes)
```

---

## 📍 SLIDE 01 — Abertura (Alencar)

```
┌────────────────────────────────────────┐
│  DEPLOY DE IA EM PRODUÇÃO              │
│  FastAPI · Docker · K8s · Observabilidade│
│                                         │
│  Módulo 05 · Trilha Master              │
│  110 minutos · 11 cenas                 │
└────────────────────────────────────────┘
```

**Alencar:** "Módulo 04 foi sobre construir. Módulo 05 é sobre colocar no ar com SLA."

---

## 📍 SLIDE 02 — Stack Recomendada

```
┌─────────────────────────────────────┐
│ Cliente → FastAPI → LiteLLM → LLM   │
│            ↓                        │
│        Redis (cache)                │
│            ↓                        │
│     Langfuse (observabilidade)      │
│            ↓                        │
│        Logs (Loki/Datadog)          │
└─────────────────────────────────────┘
```

---

## 📍 SLIDE 03 — FastAPI Base

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="AcademIA LLM Gateway")

class Query(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini"
    max_tokens: int = 1000

@app.post("/v1/generate")
async def generate(query: Query):
    # implementação com retry, cache, logging
    ...
```

---

## 📍 SLIDE 04 — Cache com Redis (70% redução custo)

```
   Request → Check Redis (SHA256(prompt))
              ↓
            HIT? → return cached (1ms)
            ↓ MISS
            → LLM (3-5s)
            → Set cache TTL 24h
```

---

## 📍 SLIDE 05 — LiteLLM (100+ Provedores)

```python
from litellm import completion

response = completion(
  model="gpt-4o-mini",  # ou "claude-3-5-sonnet", "bedrock/llama3-70b"
  messages=[{"role": "user", "content": prompt}],
  api_key=os.getenv("OPENAI_API_KEY")
)
```

**Benefício**: Trocar OpenAI → Anthropic → AWS Bedrock com 1 linha.

---

## 📍 SLIDE 06 — Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**Build**: `docker build -t llm-gateway:v1.0 .`
**Run**: `docker run -p 8000:8000 --env-file .env llm-gateway:v1.0`

---

## 📍 SLIDE 07 — Orquestração

```
┌─────────────────────────────────────────┐
│  VPS única (Hetzner/Contabo)            │
│  • 100-1000 req/min                     │
│  • $20-50/mês                           │
│  • Zero DevOps                          │
├─────────────────────────────────────────┤
│  K8s (EKS/GKE/DigitalOcean)             │
│  • 1000+ req/min                        │
│  • $200-2000/mês                        │
│  • Auto-scaling, rolling update         │
├─────────────────────────────────────────┤
│  Serverless (Fly.io, Railway, Render)   │
│  • Protótipo/baixa escala               │
│  • $0-50/mês                            │
│  • Limitado a 5min timeout              │
└─────────────────────────────────────────┘
```

---

## 📍 SLIDE 08 — Observabilidade (Langfuse)

```python
from langfuse import Langfuse

langfuse = Langfuse(public_key="...", secret_key="...")

trace = langfuse.trace(name="generate_response")
span = trace.span(name="llm_call", input=prompt)
response = completion(...)
span.end(output=response.choices[0].message.content)
```

**Métricas capturadas**: latência, tokens, custo, prompts, respostas, scores, traces completos.

---

## 📍 SLIDE 09 — Métricas Essenciais (SLOs)

```
┌──────────────────────────────────────────┐
│  Latência p95:        < 3s               │
│  Latência p99:        < 8s               │
│  Throughput:          100+ req/s         │
│  Error rate:          < 0.5%             │
│  Uptime:              > 99.9%            │
│  Cache hit rate:      > 60%              │
│  Custo por 1k reqs:   < $0.50            │
└──────────────────────────────────────────┘
```

---

## 📍 SLIDE 10 — Custos Típicos (1M req/mês)

```
   VPS única + Redis:           $30-80/mês
   K8s básico (3 nodes):        $200-500/mês
   LLM API (gpt-4o-mini):       $500-1500/mês
   Langfuse Cloud:              $0-200/mês
   Redis gerenciado:            $30-50/mês
   ─────────────────────────────────
   Total escala pequena:        $800-2500/mês
   Total escala média:          $3000-8000/mês
```

---

## 📍 SLIDE 11 — Encerramento

**Alencar:** "Deploy é onde a IA encontra a realidade. Latência, custo, observabilidade, escalabilidade. Domine essas quatro dimensões e você terá um sistema que sobrevive ao contato com usuários reais."

> **Próximo**: Módulo 06 · Segurança, Jailbreaks e LGPD para IA
