---
version: "1.0-mavis-recovery"
recovery_note: "Versão recuperada após force-push de 2026-07-29. Coexiste com o canônico em tutoriais/(sem equivalente canônico).md"
title: "Tutorial 26 · Monitorar Erros com Sentry em Produção"
description: "Como capturar, agrupar e alertar sobre exceções em produção com Sentry"
tags: [tutorial, 26, sentry, observabilidade, error-tracking, alertas]
tier: "Master"
duracao_estimada: "20 min"
pre_requisitos: ["tutoriais/21-deploy-api-ia-producao.md", "tutoriais/23-deploy-monitoramento-prometheus.md"]
ultima_atualizacao: 2026-07-27
---

# Tutorial 26 · Monitorar Erros com Sentry em Produção

> **Por que importa**: Sentry captura exceções, contexto, breadcrumbs, e agrupa por fingerprint. Em produção, é essencial saber QUANDO, ONDE, e POR QUE algo quebrou.

## 🎯 O que você vai aprender

- Instalar e configurar Sentry SDK em FastAPI
- Adicionar contexto de usuário, request, e LLM
- Configurar alertas de erro no Slack

## ⏱️ Duração: 20 minutos

---

## 📋 Passo 1: Instalar Sentry

```bash
pip install sentry-sdk[fastapi]
```

## 📋 Passo 2: Inicializar no App

```python
# main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.openai import OpenAIIntegration
import os

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    environment=os.getenv('ENV', 'production'),
    release=os.getenv('RELEASE_SHA', 'unknown'),
    traces_sample_rate=0.1,  # 10% das transações
    profiles_sample_rate=0.1,
    integrations=[
        FastApiIntegration(),
        RedisIntegration(),
        OpenAIIntegration(),  # Captura chamadas LLM
    ],
    # Filtrar erros não-importantes
    before_send=filter_noise,
)

def filter_noise(event, hint):
    # Ignorar 4xx esperados
    if 'exc_info' in hint:
        exc_type, exc_value, _ = hint['exc_info']
        if isinstance(exc_value, (HTTPException,)) and 400 <= exc_value.status_code < 500:
            return None
    return event

from fastapi import FastAPI
app = FastAPI()
```

## 📋 Passo 3: Adicionar Contexto de Usuário

```python
import sentry_sdk

@app.middleware("http")
async def sentry_context_middleware(request: Request, call_next):
    # Pegar user_id do JWT
    auth = request.headers.get('Authorization', '')
    user_id = extract_user_id_from_jwt(auth) if auth else None

    if user_id:
        sentry_sdk.set_user({
            "id": user_id,
            "ip_address": request.client.host,
            "tier": get_user_tier(user_id)
        })

    # Contexto da request
    sentry_sdk.set_context("request", {
        "url": str(request.url),
        "method": request.method,
        "user_agent": request.headers.get('User-Agent', '')
    })

    response = await call_next(request)
    return response
```

## 📋 Passo 4: Capturar Contexto de LLM

```python
import sentry_sdk

@app.post("/v1/generate")
async def generate(request: GenerateRequest):
    with sentry_sdk.start_transaction(op="llm.generate", name=f"generate:{request.model}"):
        # Tag para filtros
        sentry_sdk.set_tag("llm.model", request.model)
        sentry_sdk.set_tag("llm.tier", request.tier)

        try:
            response = completion(
                model=request.model,
                messages=[{"role": "user", "content": request.prompt}],
                max_tokens=request.max_tokens,
            )

            # Métricas de LLM como "breadcrumbs"
            sentry_sdk.add_breadcrumb(
                category="llm",
                message=f"Generated {response.usage.total_tokens} tokens",
                level="info",
                data={
                    "model": request.model,
                    "input_tokens": response.usage.prompt_tokens,
                    "output_tokens": response.usage.completion_tokens,
                    "cost_usd": response._hidden_params.get('response_cost', 0)
                }
            )

            return {"response": response.choices[0].message.content}
        except Exception as e:
            # Captura com contexto rico
            sentry_sdk.capture_exception(e)
            raise HTTPException(status_code=500, detail=str(e))
```

## 📋 Passo 5: Capturar Mensagens Customizadas

```python
# Para eventos não-exceção
sentry_sdk.capture_message(
    "LLM latency exceeded 10s",
    level="warning",
    extras={
        "model": "gpt-4o",
        "latency_ms": 12500,
        "prompt_length": 4500
    }
)
```

## 📋 Passo 6: Configurar Alertas no Slack

No painel do Sentry (sentry.io):

1. **Settings → Integrations → Slack**
2. **Alerts → New Alert Rule**

Configuração recomendada:

```
When: An event is seen with these conditions
- The issue's level is "error" OR "fatal"
- The issue is first seen
Then: Send notification via #alerts-production
```

Regras adicionais:
- **Error spike**: mais de 50 errors em 5 min
- **Regression**: voltou a ocorrer após estar resolvido
- **User impact**: afeta >100 usuários únicos

## 📋 Passo 7: Visualizar no Painel

Após deploy, em 5-10 min:

1. **Issues**: lista de erros agrupados (deduplicados por stack trace)
2. **Performance**: traces com latência
3. **Releases**: comparação entre versões

URL: `https://sentry.io/organizations/your-org/issues/`

## 🎓 Próximo Passo

- **Tutoriais relacionados**:
  - `tutoriais/21-deploy-api-ia-producao.md`
  - `tutoriais/23-deploy-monitoramento-prometheus.md`
  - `tutoriais/24-implementar-rate-limiting.md`
- **Curso**: `cursos/master/05-deploy-em-producao.md`
- **Runbook**: Adicionar ao `producao/INCIDENT-RESPONSE-RUNBOOK.md`

---

**Tutorial criado em 2026-07-27** · Mavis Agent
**Versão 1.0** · Mantido em `tutoriais/26-monitorar-com-sentry.md`
