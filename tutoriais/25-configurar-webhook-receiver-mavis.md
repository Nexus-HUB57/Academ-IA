---
version: "1.0-mavis-recovery"
recovery_note: "Versão recuperada após force-push de 2026-07-29. Coexiste com o canônico em tutoriais/(sem equivalente canônico).md"
title: "Tutorial 25 · Configurar Webhook Receiver Seguro"
description: "Como receber webhooks de provedores externos com validação HMAC + retry automático"
tags: [tutorial, 25, webhook, hmac, seguranca, integracao, retry]
tier: "Agente"
duracao_estimada: "25 min"
pre_requisitos: ["tutoriais/06-disparar-campanha-whatsapp.md"]
ultima_atualizacao: 2026-07-27
---

# Tutorial 25 · Configurar Webhook Receiver Seguro

> **Por que importa**: Webhooks sem validação são vetor de ataque. HMAC + retry garantem autenticidade e resiliência.

## 🎯 O que você vai aprender

- Criar endpoint que recebe webhooks com validação HMAC SHA-256
- Implementar fila de retry com backoff exponencial
- Idempotency keys para evitar duplicação

## ⏱️ Duração: 25 minutos

---

## 📋 Passo 1: Estrutura Base

```python
# webhook_server.py
from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib
from typing import Dict, Any
import json
import os
from datetime import datetime, timedelta

app = FastAPI()

# Secret compartilhado com o provedor
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'change-me-in-production')

# Storage de eventos processados (idempotency)
processed_events: Dict[str, datetime] = {}
IDEMPOTENCY_WINDOW = timedelta(hours=24)
```

## 📋 Passo 2: Validação HMAC

```python
def verify_hmac(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

@app.post("/webhooks/provider")
async def receive_webhook(request: Request):
    # 1. Ler raw body (importante: não usar await request.json() antes)
    payload = await request.body()
    signature = request.headers.get('X-Signature-SHA256', '')

    # 2. Verificar HMAC
    if not verify_hmac(payload, signature, WEBHOOK_SECRET):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # 3. Parse do JSON
    try:
        event = json.loads(payload)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # 4. Idempotency check
    event_id = event.get('id')
    if event_id in processed_events:
        return {"status": "already_processed", "event_id": event_id}

    # 5. Processar evento
    process_event(event)
    processed_events[event_id] = datetime.utcnow()

    # 6. Limpar cache antigo
    cutoff = datetime.utcnow() - IDEMPOTENCY_WINDOW
    for eid in list(processed_events.keys()):
        if processed_events[eid] < cutoff:
            del processed_events[eid]

    # 7. Responder 200 OK rapidamente
    return {"status": "received", "event_id": event_id}
```

## 📋 Passo 3: Processar com Retry (Producer/Consumer)

```python
# webhook_worker.py
import redis
import json
import time
from typing import Any

r = redis.Redis(host='localhost', port=6379, db=0)
WEBHOOK_QUEUE = 'webhook:queue'
WEBHOOK_DLQ = 'webhook:dlq'  # Dead Letter Queue

def enqueue_webhook(event: dict, max_retries: int = 5):
    """Enfileira evento para processamento assíncrono."""
    r.rpush(WEBHOOK_QUEUE, json.dumps({
        'event': event,
        'attempts': 0,
        'max_retries': max_retries,
        'first_seen': time.time()
    }))

def process_with_retry():
    """Worker que processa fila com backoff exponencial."""
    while True:
        item = r.blpop(WEBHOOK_QUEUE, timeout=5)
        if not item:
            continue

        data = json.loads(item[1])
        event = data['event']
        attempts = data['attempts']

        try:
            handler = get_handler(event.get('type'))
            handler(event)
        except Exception as e:
            attempts += 1
            if attempts >= data['max_retries']:
                # Dead letter queue
                r.rpush(WEBHOOK_DLQ, json.dumps({
                    'event': event,
                    'attempts': attempts,
                    'last_error': str(e)
                }))
                print(f"❌ DLQ: {event.get('id')} after {attempts} attempts")
            else:
                # Re-enfileirar com backoff
                delay = 2 ** attempts  # 2, 4, 8, 16, 32s
                time.sleep(delay)
                r.rpush(WEBHOOK_QUEUE, json.dumps({
                    **data,
                    'attempts': attempts
                }))
                print(f"⚠️ Retry {attempts}/{data['max_retries']} for {event.get('id')}")

# Handlers
def get_handler(event_type: str):
    handlers = {
        'payment.success': handle_payment_success,
        'payment.failed': handle_payment_failed,
        'subscription.canceled': handle_subscription_canceled,
        'whatsapp.message.received': handle_whatsapp_message,
    }
    return handlers.get(event_type, handle_unknown)

def handle_payment_success(event):
    print(f"💰 Payment OK: {event['data']['amount']}")

def handle_payment_failed(event):
    print(f"❌ Payment failed: {event['data']['reason']}")

def handle_subscription_canceled(event):
    print(f"🚪 Sub canceled: {event['data']['customer_id']}")

def handle_whatsapp_message(event):
    print(f"📱 WhatsApp: {event['data']['from']} → {event['data']['message']}")

def handle_unknown(event):
    print(f"❓ Unknown event type: {event.get('type')}")
```

## 📋 Passo 4: Testar com curl

```bash
# 1. Calcular HMAC
SECRET="change-me-in-production"
PAYLOAD='{"id":"evt_123","type":"payment.success","data":{"amount":1000}}'
SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" -hex | sed 's/^.* //')

# 2. Enviar webhook
curl -X POST http://localhost:8000/webhooks/provider \
  -H "Content-Type: application/json" \
  -H "X-Signature-SHA256: $SIGNATURE" \
  -d "$PAYLOAD"

# 3. Verificar fila DLQ
redis-cli LRANGE webhook:dlq 0 -1
```

## 🎓 Próximo Passo

- **Tutoriais relacionados**:
  - `tutoriais/21-deploy-api-ia-producao.md`
  - `tutoriais/22-criar-playbook-do-zero.md`
- **Curso**: `cursos/agente/` (integrações)
- **Playbook**: Criar `playbooks/PB-WEBHOOK-falha-receiver.md`

---

**Tutorial criado em 2026-07-27** · Mavis Agent
**Versão 1.0** · Mantido em `tutoriais/25-configurar-webhook-receiver.md`
