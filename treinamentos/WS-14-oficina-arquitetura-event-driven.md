---
title: "WS-14 · Oficina de Arquitetura Event-Driven"
subtitle: "Workshop hands-on: implementar sistema event-driven com Kafka, EventBridge e WebSockets"
author: "Equipo Nexus · Ravi (CTO/AI) + Sir. Nexus Alencar"
duration: "4h"
type: "workshop"
level: "advanced"
date: 2026-07-31
pattern: "MMN_IA"
---

**WS-14 · Oficina de Arquitetura Event-Driven**

*Workshop hands-on de 4h onde você vai construir um sistema event-driven completo: producer (FastAPI), broker (Kafka), consumer (Worker), e dashboard em tempo real (WebSocket).*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 Visão Geral

| Item | Detalhe |
|------|---------|
| **Duração** | 4 horas (2 coffee breaks) |
| **Formato** | 20% teoria + 80% hands-on |
| **Pré-requisitos** | Trilha Master completa. Conhece Python async. |
| **Capacidade** | 30 vagas (10 por squad) |
| **Material** | Docker Compose (Kafka + Zookeeper + Postgres), código base, dashboard |
| **Certificação** | Badge WS-14-EVENT (elegível para CEN+) |

---

## 📚 Agenda

| Horário | Bloco | Descrição |
|---------|-------|-----------|
| 0:00-0:25 | **Fundamentos** | Event-driven vs request-response, top 5 patterns |
| 0:25-1:15 | **Producer + Broker** | FastAPI → Kafka com 3 squads em paralelo |
| 1:15-1:30 | ☕ Coffee | |
| 1:30-2:15 | **Consumer + Saga** | Worker que processa eventos com saga pattern |
| 2:15-2:30 | ☕ Coffee | |
| 2:30-3:15 | **Realtime + Idempotency** | WebSocket dashboard + dedup keys |
| 3:15-4:00 | **Apresentações + Demos** | 3 squads, top squad recebe badge |

---

## 🧠 Bloco 0: Fundamentos (25 min)

### Top 5 Patterns Event-Driven

**1. Publish-Subscribe (Pub/Sub)**
- Producer publica evento
- Múltiplos consumers recebem
- Desacoplamento total

**2. Event Sourcing**
- Estado = sequência de eventos
- Audit log completo
- Replay para reconstruir

**3. CQRS (Command Query Responsibility Segregation)**
- Commands (write) separado de Queries (read)
- Read model otimizado
- Escalabilidade independente

**4. Saga Pattern**
- Transação distribuída = sequência de eventos
- Compensação em caso de falha
- Consistente (eventual)

**5. Event Carried State Transfer**
- Cada evento carrega estado completo
- Consumers não precisam de call de volta
- Maior throughput

### Quando Usar Event-Driven

✅ **Use quando:**
- Múltiplos consumidores precisam reagir ao mesmo evento
- Operações assíncronas (não precisa resposta imediata)
- Auditoria é importante
- Throughput alto (milhares de eventos/s)
- Acoplamento fraco entre serviços

❌ **Não use quando:**
- Operação síncrona (precisa resposta imediata)
- 1 consumer apenas (use REST)
- Trivial CRUD (overhead desnecessário)
- Consistência forte é crítica (use SQL transactions)

---

## 🛠️ Bloco 1: Producer + Broker (50 min)

### Setup: Docker Compose (Kafka)

```yaml
# docker-compose.yml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: nexus
      POSTGRES_DB: events
    ports:
      - "5432:5432"
```

### Producer (FastAPI)

```python
"""
Producer de eventos: API REST que publica em Kafka.
"""
import json
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from aiokafka import AIOKafkaProducer
import uuid


app = FastAPI()


class OrderEvent(BaseModel):
    """Schema do evento"""
    order_id: str
    customer_id: str
    items: list
    total: float
    timestamp: str = None


class EventProducer:
    def __init__(self):
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers="kafka:29092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda k: k.encode("utf-8") if k else None,
        )
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def publish(self, topic: str, key: str, event: dict):
        """Publica evento com idempotency key"""
        await self.producer.send_and_wait(
            topic=topic,
            key=key,
            value=event,
            headers=[
                ("event-id", str(uuid.uuid4()).encode()),
                ("event-type", event.get("type", "unknown").encode()),
                ("schema-version", b"1.0"),
            ],
        )


producer = EventProducer()


@app.on_event("startup")
async def startup():
    await producer.start()


@app.on_event("shutdown")
async def shutdown():
    await producer.stop()


@app.post("/orders")
async def create_order(order: OrderEvent):
    """Cria pedido e publica evento"""
    # Persistir no DB (mock)
    event = {
        "type": "OrderCreated",
        "order_id": order.order_id,
        "customer_id": order.customer_id,
        "items": order.items,
        "total": order.total,
        "timestamp": datetime.now().isoformat(),
    }

    # Publicar no Kafka
    await producer.publish(
        topic="orders",
        key=order.order_id,  # mesma key = mesma partição = ordem garantida
        event=event,
    )

    return {"status": "published", "order_id": order.order_id}
```

### Tarefa: Squad implementa producer

**Cada squad:**
1. Levanta docker-compose
2. Roda FastAPI
3. Cria 3 tipos de eventos:
   - `OrderCreated`
   - `PaymentProcessed`
   - `OrderShipped`
4. Testa publicando via curl
5. Confirma no Kafka (kafka-console-consumer)

---

## ⚙️ Bloco 2: Consumer + Saga (45 min)

### Consumer (Worker)

```python
"""
Consumer que processa eventos e aplica regras de negócio.
"""
import json
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError
import asyncio
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class EventConsumer:
    def __init__(self, group_id: str, topics: list[str]):
        self.group_id = group_id
        self.topics = topics
        self.consumer = None
        self.handlers = {}

    def register_handler(self, event_type: str, handler):
        """Registra handler para tipo de evento"""
        self.handlers[event_type] = handler

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            *self.topics,
            bootstrap_servers="kafka:29092",
            group_id=self.group_id,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            enable_auto_commit=False,  # manual commit para exactly-once
            auto_offset_reset="earliest",
        )
        await self.consumer.start()
        logger.info(f"Consumer started: group={self.group_id} topics={self.topics}")

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()

    async def run(self):
        """Loop principal"""
        try:
            async for message in self.consumer:
                event = message.value
                event_type = event.get("type")

                logger.info(
                    f"Event received: type={event_type} "
                    f"topic={message.topic} partition={message.partition} "
                    f"offset={message.offset}"
                )

                handler = self.handlers.get(event_type)
                if not handler:
                    logger.warning(f"No handler for {event_type}, skipping")
                    await self.consumer.commit()
                    continue

                try:
                    await handler(event)
                    await self.consumer.commit()  # commit só se sucesso
                except Exception as e:
                    logger.error(f"Handler failed: {e}")
                    # Não commit → mensagem será reprocessada
                    # Em produção: DLQ (Dead Letter Queue)
        except KafkaError as e:
            logger.error(f"Kafka error: {e}")


# Exemplo de uso: Fulfillment Service
async def handle_order_created(event: dict):
    """Quando pedido é criado, dispara fulfillment"""
    order_id = event["order_id"]
    customer_id = event["customer_id"]
    items = event["items"]

    logger.info(f"Fulfilling order {order_id} for {customer_id}")

    # Lógica de negócio...
    # - Verificar estoque
    # - Reservar itens
    # - Criar envio
    # - Enviar email

    # Publicar evento de follow-up
    await producer.publish(
        topic="orders",
        key=order_id,
        event={
            "type": "OrderFulfilled",
            "order_id": order_id,
            "fulfillment_id": "FUF-123",
            "timestamp": datetime.now().isoformat(),
        },
    )


async def handle_payment_processed(event: dict):
    """Quando pagamento é processado, atualiza pedido"""
    order_id = event["order_id"]
    amount = event["amount"]

    logger.info(f"Payment processed for {order_id}: R$ {amount}")

    # Lógica...


# Main
async def main():
    consumer = EventConsumer(
        group_id="fulfillment-service",
        topics=["orders"],
    )

    consumer.register_handler("OrderCreated", handle_order_created)
    consumer.register_handler("PaymentProcessed", handle_payment_processed)

    await consumer.start()
    await consumer.run()


if __name__ == "__main__":
    asyncio.run(main())
```

### Saga Pattern

```python
"""
Saga: sequência de transações que compensam em caso de falha.
"""
from enum import Enum
from dataclasses import dataclass
from typing import Callable, List


class SagaStepStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATED = "compensated"


@dataclass
class SagaStep:
    name: str
    action: Callable
    compensation: Callable  # rollback
    status: SagaStepStatus = SagaStepStatus.PENDING


class Saga:
    def __init__(self, name: str):
        self.name = name
        self.steps: List[SagaStep] = []

    def add_step(self, name: str, action: Callable, compensation: Callable):
        self.steps.append(SagaStep(name, action, compensation))
        return self

    async def execute(self):
        """Executa saga, compensando se alguma step falhar"""
        completed = []

        for step in self.steps:
            try:
                await step.action()
                step.status = SagaStepStatus.COMPLETED
                completed.append(step)
            except Exception as e:
                logger.error(f"Saga '{self.name}' failed at step '{step.name}': {e}")
                step.status = SagaStepStatus.FAILED

                # Compensar steps já completadas (em ordem reversa)
                for completed_step in reversed(completed):
                    try:
                        await completed_step.compensation()
                        completed_step.status = SagaStepStatus.COMPENSATED
                    except Exception as comp_e:
                        logger.error(f"Compensation failed: {comp_e}")

                return False

        return True


# Exemplo: Saga de Pedido
async def create_order_saga(order_data: dict):
    """Saga: OrderCreated → PaymentProcessed → InventoryReserved → OrderShipped"""

    saga = Saga(name="CreateOrder")

    # Step 1: Criar pedido
    saga.add_step(
        name="CreateOrder",
        action=lambda: db.execute(
            "INSERT INTO orders (id, customer_id, total) VALUES ($1, $2, $3)",
            order_data["order_id"], order_data["customer_id"], order_data["total"],
        ),
        compensation=lambda: db.execute(
            "DELETE FROM orders WHERE id = $1", order_data["order_id"],
        ),
    )

    # Step 2: Processar pagamento
    saga.add_step(
        name="ProcessPayment",
        action=lambda: payment_service.charge(
            order_data["customer_id"], order_data["total"],
        ),
        compensation=lambda: payment_service.refund(
            order_data["order_id"],
        ),
    )

    # Step 3: Reservar inventário
    saga.add_step(
        name="ReserveInventory",
        action=lambda: inventory_service.reserve(
            order_data["items"],
        ),
        compensation=lambda: inventory_service.release(
            order_data["items"],
        ),
    )

    # Step 4: Agendar envio
    saga.add_step(
        name="ScheduleShipment",
        action=lambda: shipping_service.schedule(
            order_data["order_id"],
        ),
        compensation=lambda: shipping_service.cancel(
            order_data["order_id"],
        ),
    )

    return await saga.execute()
```

### Tarefa: Squad implementa consumer + saga

**Cada squad:**
1. Roda consumer em background
2. Publica 5 orders via API
3. Confirma que consumer processou
4. Implementa saga para 1 caso (ex: order com pagamento)
5. Testa compensação: força falha no step 3, vê step 1-2 serem compensados

---

## 📡 Bloco 3: Realtime + Idempotency (45 min)

### WebSocket Dashboard

```python
"""
WebSocket que recebe updates do Kafka e envia para frontend.
"""
from fastapi import FastAPI, WebSocket
import asyncio
import json
from aiokafka import AIOKafkaConsumer


app = FastAPI()
connected_clients: list[WebSocket] = []


@app.websocket("/ws/dashboard")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            # Mantém conexão viva
            data = await websocket.receive_text()
    except Exception:
        connected_clients.remove(websocket)


async def broadcast_event(event: dict):
    """Envia evento para todos clientes conectados"""
    dead = []
    for client in connected_clients:
        try:
            await client.send_text(json.dumps(event))
        except Exception:
            dead.append(client)
    for d in dead:
        connected_clients.remove(d)


# Task: lê do Kafka e broadcast via WebSocket
async def kafka_to_websocket():
    consumer = AIOKafkaConsumer(
        "orders",
        bootstrap_servers="kafka:29092",
        group_id="websocket-bridge",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )
    await consumer.start()

    try:
        async for message in consumer:
            event = message.value
            await broadcast_event(event)
    finally:
        await consumer.stop()


@app.on_event("startup")
async def startup():
    asyncio.create_task(kafka_to_websocket())


# Frontend (HTML simples)
HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Real-time Dashboard</title>
  <style>
    body { font-family: monospace; background: #0a0e1a; color: #e5edf5; padding: 20px; }
    .event { background: #131a2c; padding: 12px; margin: 8px 0; border-radius: 8px; }
    .event-id { color: #63eaff; font-weight: 700; }
  </style>
</head>
<body>
  <h1>🔴 Real-time Events</h1>
  <div id="events"></div>

  <script>
    const ws = new WebSocket("ws://localhost:8000/ws/dashboard");
    ws.onmessage = (e) => {
      const event = JSON.parse(e.data);
      const div = document.createElement("div");
      div.className = "event";
      div.innerHTML = `
        <div class="event-id">${event.type}</div>
        <pre>${JSON.stringify(event, null, 2)}</pre>
      `;
      document.getElementById("events").prepend(div);
    };
  </script>
</body>
</html>
"""


@app.get("/")
async def dashboard():
    from fastapi.responses import HTMLResponse
    return HTMLResponse(HTML)
```

### Idempotency

```python
"""
Idempotency keys: garantir que evento duplicado não seja processado 2x.
"""
import redis


class IdempotencyStore:
    def __init__(self):
        self.redis = redis.Redis(host="redis", port=6379)

    def is_processed(self, event_id: str) -> bool:
        """Retorna True se evento já foi processado"""
        return self.redis.exists(f"event:{event_id}")

    def mark_processed(self, event_id: str, ttl: int = 86400):
        """Marca evento como processado (TTL 24h)"""
        self.redis.setex(f"event:{event_id}", ttl, "1")


idempotency = IdempotencyStore()


async def handle_order_created_idempotent(event: dict):
    """Handler idempotente"""
    event_id = event.get("event_id")  # vem do header Kafka

    if not event_id:
        # Fallback: usa order_id + type como dedup key
        event_id = f"{event['type']}:{event['order_id']}"

    if idempotency.is_processed(event_id):
        logger.info(f"Event {event_id} already processed, skipping")
        return

    # Processa
    await handle_order_created(event)

    # Marca como processado
    idempotency.mark_processed(event_id)
```

### Exactly-Once Semantics

```python
"""
Garantir exactly-once com Kafka transactions.
"""
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json


class ExactlyOnceProcessor:
    def __init__(self, group_id: str):
        self.group_id = group_id
        self.consumer = None
        self.producer = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            "orders",
            bootstrap_servers="kafka:29092",
            group_id=self.group_id,
            enable_auto_commit=False,
            isolation_level="read_committed",  # só lê committed
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )

        self.producer = AIOKafkaProducer(
            bootstrap_servers="kafka:29092",
            enable_idempotence=True,  # deduplica no producer
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

        await self.consumer.start()
        await self.producer.start()

    async def process(self):
        async for message in self.consumer:
            event = message.value

            try:
                # Processa e produz follow-up atomicamente
                async with self.producer.transaction():
                    # Sua lógica
                    result = await process_event(event)

                    # Produz follow-up
                    await self.producer.send(
                        "orders-processed",
                        value=result,
                    )

                # Commit offset APÓS transaction
                await self.consumer.commit()

            except Exception as e:
                # Transaction é aborted automaticamente
                # Offset não é commit → mensagem será reprocessada
                logger.error(f"Failed: {e}")
```

### Tarefa: Squad implementa realtime

**Cada squad:**
1. Implementa WebSocket que recebe do Kafka
2. Adiciona idempotency ao consumer
3. Testa com 10 eventos duplicados (mesmo event_id)
4. Confirma que processou 1x (não 10x)
5. Dashboard mostra eventos em tempo real

---

## 📊 Bloco 4: Apresentações + Demos (45 min)

### Cada squad apresenta (10min × 3 squads = 30min)

**Demo:**
1. **Producer:** Postman/curl cria 3 orders
2. **Consumer:** log mostra processamento
3. **Saga:** simula falha, mostra compensação
4. **Realtime:** dashboard atualiza ao vivo
5. **Idempotency:** mostra evento duplicado sendo ignorado

**Critérios:**
- Funciona end-to-end (40%)
- Saga compensa corretamente (25%)
- Idempotency funciona (20%)
- Apresentação (15%)

### Premiação

- 🥇 **Top squad:** badge + swag + 30min mentoria com Ravi
- 🎯 **Melhor saga:** destaque técnico
- 🛡️ **Melhor idempotência:** destaque técnico

---

## 📦 Materiais Inclusos

- Docker Compose (Kafka + Zookeeper + Postgres + Redis)
- Código base (FastAPI + Worker + WebSocket)
- Dashboard HTML
- Scripts de teste
- Templates de eventos
- Runbook de troubleshooting

---

## 🎯 Quem Deve Fazer

✅ **Perfeito para:**
- Engenheiros de backend
- Arquitetos de software
- Tech leads
- Founders com background técnico

❌ **Não indicado para:**
- Quem nunca usou message broker (comece com trilhas anteriores)
- Quem não tem experiência com async Python

---

## 📚 Pré-work

- `apostilas/46-arquitetura-multi-tenant-2026.md` (30 min)
- `tutoriais/31-circuit-breaker-padrao.md` (20 min)
- `Lib-Nexus/api-docs/03-graphql-schema.md` (10 min)
- `producao/INCIDENT-RESPONSE-RUNBOOK.md` (10 min)

**Total: ~70 min de leitura prévia**

---

## 💬 Depoimentos

> "O workshop me fez entender Kafka de verdade. Antes era só buzzword."
> — Carla M., Estrategista + Engenheira, SP

> "Saga pattern mudou como penso em transações distribuídas. Indispensável."
> — Diego F., Master, Lisboa

> "Idempotency parece simples até você implementar. Workshop me poupou meses de bugs."
> — Renata A., Estrategista, Curitiba

---

## 🔗 Materiais Complementares

- `apostilas/46-arquitetura-multi-tenant-2026.md` — arquitetura
- `tutoriais/31-circuit-breaker-padrao.md` — circuit breaker
- `tutoriais/33-graphql-vs-rest.md` — APIs
- `tutoriais/23-deploy-monitoramento-prometheus.md` — monitoramento
- `Lib-Nexus/best-practices/05-sre-observability.md` — SRE
- `Lib-Nexus/api-docs/03-graphql-schema.md` — GraphQL
- `Lib-Nexus/agents-specs/06-sho-operator-agent.md` — SHO
- `producao/INCIDENT-RESPONSE-RUNBOOK.md` — runbook

---

*AcademIA · WS-14 · Arquitetura Event-Driven · 2026*