---
version: "1.0-mavis-recovery"
recovery_note: "Versão recuperada após force-push de 2026-07-29. Coexiste com o canônico em tutoriais/24-redes-neurais-zero-hero.md"
title: "Tutorial 24 · Implementar Rate Limiting em API de IA"
description: "Como proteger API de LLM com rate limiting distribuído (Redis + sliding window)"
tags: [tutorial, 24, rate-limiting, redis, llm, api, seguranca]
tier: "Master"
duracao_estimada: "30 min"
pre_requisitos: ["tutoriais/21-deploy-api-ia-producao.md", "tutoriais/06-disparar-campanha-whatsapp.md"]
ultima_atualizacao: 2026-07-27
---

# Tutorial 24 · Implementar Rate Limiting em API de IA

> **Por que importa**: APIs de LLM são caras e alvo de abuso. Rate limiting protege contra custos descontrolados, ataques, e uso não-autorizado.

## 🎯 O que você vai aprender

- Implementar rate limiting distribuído com Redis
- Usar algoritmo sliding window (mais preciso que fixed window)
- Configurar diferentes limites por tier de usuário
- Bloquear abuso sem impactar UX

## ⏱️ Duração: 30 minutos

---

## 📋 Passo 1: Instalar Dependências

```bash
pip install fastapi uvicorn redis slowapi
```

## 📋 Passo 2: Implementar Sliding Window com Redis

```python
# rate_limiter.py
import redis
import time
from typing import Optional

class SlidingWindowLimiter:
    def __init__(self, redis_client: redis.Redis, window_seconds: int = 60, max_requests: int = 60):
        self.redis = redis_client
        self.window = window_seconds
        self.max = max_requests

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        pipe = self.redis.pipeline()
        # Remove entries older than window
        pipe.zremrangebyscore(key, 0, now - self.window)
        # Count current entries
        pipe.zcard(key)
        # Add current request
        pipe.zadd(key, {f"{now}:{id(object)}": now})
        # Set TTL
        pipe.expire(key, self.window)
        results = pipe.execute()
        current_count = results[1]
        return current_count < self.max

# Initialize
r = redis.Redis(host='localhost', port=6379, db=0)
limiter = SlidingWindowLimiter(r, window_seconds=60, max_requests=60)
```

## 📋 Passo 3: Integrar com FastAPI

```python
# main.py
from fastapi import FastAPI, Request, HTTPException
from rate_limiter import SlidingWindowLimiter
import redis

app = FastAPI()
r = redis.Redis(host='localhost', port=6379, db=0)

TIER_LIMITS = {
    'anonymous': (60, 10),      # 10 req/min
    'free': (60, 30),          # 30 req/min
    'authenticated': (60, 100), # 100 req/min
    'premium': (60, 500),       # 500 req/min
    'enterprise': (60, 5000),   # 5000 req/min
}

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Determine tier from user (JWT, API key, etc.)
    tier = request.headers.get('X-User-Tier', 'anonymous')
    user_id = request.headers.get('X-User-ID', request.client.host)

    window, max_req = TIER_LIMITS.get(tier, TIER_LIMITS['anonymous'])
    limiter = SlidingWindowLimiter(r, window, max_req)

    key = f"rl:{tier}:{user_id}"
    if not limiter.is_allowed(key):
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: {max_req} req/{window}s",
            headers={'Retry-After': str(window)}
        )

    response = await call_next(request)
    return response
```

## 📋 Passo 4: Expor Headers de Rate Limit

```python
@app.get("/v1/generate")
async def generate(request: Request):
    tier = request.headers.get('X-User-Tier', 'anonymous')
    user_id = request.headers.get('X-User-ID', request.client.host)
    window, max_req = TIER_LIMITS[tier]
    key = f"rl:{tier}:{user_id}"

    # Get current usage
    now = time.time()
    r.zremrangebyscore(key, 0, now - window)
    current = r.zcard(key)
    remaining = max(0, max_req - current - 1)

    # ... process request ...

    return JSONResponse(
        content={...},
        headers={
            'X-RateLimit-Limit': str(max_req),
            'X-RateLimit-Remaining': str(remaining),
            'X-RateLimit-Reset': str(int(now + window))
        }
    )
```

## 📋 Passo 5: Testar

```bash
# Should allow 10 requests in 60s for anonymous
for i in {1..12}; do
  curl -i http://localhost:8000/v1/generate \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Hello"}'
done
# Last 2 should return 429
```

## 🎓 Próximo Passo

- **Tutoriais relacionados**: 
  - `tutoriais/21-deploy-api-ia-producao.md` (deploy base)
  - `tutoriais/22-criar-playbook-do-zero.md` (playbook de rate limit em crise)
- **Curso**: `cursos/master/05-deploy-em-producao.md`
- **Playbook**: Implementar `playbooks/PB-RATE-LIMIT-abuso.md`

---

**Tutorial criado em 2026-07-27** · Mavis Agent
**Versão 1.0** · Mantido em `tutoriais/24-implementar-rate-limiting.md`
