---
title: "API Docs · SDK Python & TypeScript"
description: "Documentação canônica dos SDKs oficiais Nexus para Python e TypeScript"
tags: [lib-nexus, api-docs, sdk, python, typescript, cliente]
category: api-docs
version: "1.0"
last_review: "2026-07-23"
---

# 📦 API Docs · SDK Python & TypeScript

> **Documentação canônica** dos SDKs oficiais Nexus para Python e TypeScript. SDKs são o caminho recomendado para integração em produção — abstraem autenticação, retry, rate limiting, e tipos.

---

## 🎯 Filosofia dos SDKs

Os SDKs Nexus seguem 4 princípios:

1. **Idiomático** — usa padrões da linguagem (não traduz REST 1:1).
2. **Type-safe** — tipos fortes em compile-time (TS) / type hints (Python).
3. **Async-first** — todas operações I/O são assíncronas.
4. **Resiliente** — retry automático, circuit breaker, backoff exponencial.

---

## 🐍 SDK Python

### Instalação

```bash
pip install nexus-ai
```

Requer Python 3.10+.

### Setup

```python
import os
from nexus import NexusClient

client = NexusClient(
    api_key=os.environ["NEXUS_API_KEY"],
    # opcional
    environment="production",  # 'production' | 'staging' | 'local'
    timeout=30,  # segundos
    max_retries=3,
)
```

### Operações Comuns

#### Listar agentes

```python
agents = client.agents.list(
    tenant_id="tenant-123",
    status="ACTIVE",
    limit=20,
)
for agent in agents:
    print(f"{agent.name} ({agent.id}) - {agent.status}")
```

#### Criar agente

```python
new_agent = client.agents.create(
    name="WhatsApp Copy Agent",
    persona="Premium copywriter specialized in e-commerce",
    skills=["whatsapp-copy-v3", "ab-test-judge"],
    config={
        "temperature": 0.7,
        "max_tokens": 2000,
    },
)
print(f"Created agent: {new_agent.id}")
```

#### Executar skill

```python
result = client.skills.execute(
    skill_id="whatsapp-copy-v3",
    input={
        "produto": "vestido floral",
        "publico": "mulheres 25-35",
        "tom": "acolhedor",
    },
)
print(f"Copy: {result.output['copy_principal']}")
print(f"Variations: {len(result.output['variacoes'])}")
```

#### Streaming de execuções

```python
async for event in client.agents.stream_executions(agent_id="agent-123"):
    print(f"Event: {event.type} at {event.timestamp}")
    if event.type == "completed":
        print(f"Output: {event.output}")
```

#### Webhook handler

```python
from nexus import WebhookHandler

@WebhookHandler.handler(event="agent.execution.completed")
async def on_execution_complete(event):
    print(f"Execution {event.execution_id} completed")
    # process output
    await send_to_slack(event.output)

webhook = WebhookHandler(secret=os.environ["WEBHOOK_SECRET"])
webhook.register(on_execution_complete)
```

### Type Hints Completos

```python
from nexus.types import (
    Tenant,
    Agent,
    AgentStatus,
    Skill,
    ExecutionResult,
    Incident,
    Severity,
)
```

### Tratamento de Erros

```python
from nexus.exceptions import (
    NexusError,
    RateLimitError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
)

try:
    agent = client.agents.get("invalid-id")
except NotFoundError:
    print("Agent not found")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
except NexusError as e:
    print(f"Generic error: {e}")
```

### Async / Concorrência

```python
import asyncio
from nexus import AsyncNexusClient

async def fetch_multiple_agents():
    async with AsyncNexusClient(api_key="...") as client:
        tasks = [
            client.agents.get(f"agent-{i}")
            for i in range(100)
        ]
        agents = await asyncio.gather(*tasks)
        return agents

agents = asyncio.run(fetch_multiple_agents())
```

---

## 🟦 SDK TypeScript

### Instalação

```bash
npm install @nexus-ai/sdk
# ou
pnpm add @nexus-ai/sdk
```

Requer Node 18+ ou Deno 1.40+.

### Setup

```typescript
import { NexusClient } from "@nexus-ai/sdk";

const client = new NexusClient({
  apiKey: process.env.NEXUS_API_KEY!,
  environment: "production", // 'production' | 'staging' | 'local'
  timeout: 30000, // ms
  maxRetries: 3,
});
```

### Operações Comuns

#### Listar agentes

```typescript
const agents = await client.agents.list({
  tenantId: "tenant-123",
  status: "ACTIVE",
  limit: 20,
});

for (const agent of agents) {
  console.log(`${agent.name} (${agent.id}) - ${agent.status}`);
}
```

#### Criar agente

```typescript
const newAgent = await client.agents.create({
  name: "WhatsApp Copy Agent",
  persona: "Premium copywriter specialized in e-commerce",
  skills: ["whatsapp-copy-v3", "ab-test-judge"],
  config: {
    temperature: 0.7,
    maxTokens: 2000,
  },
});

console.log(`Created agent: ${newAgent.id}`);
```

#### Executar skill

```typescript
const result = await client.skills.execute({
  skillId: "whatsapp-copy-v3",
  input: {
    produto: "vestido floral",
    publico: "mulheres 25-35",
    tom: "acolhedor",
  },
});

console.log(`Copy: ${result.output.copy_principal}`);
console.log(`Variations: ${result.output.variacoes.length}`);
```

#### Streaming de execuções

```typescript
const stream = client.agents.streamExecutions({ agentId: "agent-123" });

for await (const event of stream) {
  console.log(`Event: ${event.type} at ${event.timestamp}`);
  if (event.type === "completed") {
    console.log(`Output: ${event.output}`);
  }
}
```

#### Webhook handler (Express)

```typescript
import express from "express";
import { WebhookHandler } from "@nexus-ai/sdk";

const app = express();
const webhook = new WebhookHandler({ secret: process.env.WEBHOOK_SECRET! });

webhook.on("agent.execution.completed", async (event) => {
  console.log(`Execution ${event.executionId} completed`);
  await sendToSlack(event.output);
});

app.post("/webhooks/nexus", webhook.expressMiddleware());
app.listen(3000);
```

### TypeScript Types Completos

```typescript
import type {
  Tenant,
  Agent,
  AgentStatus,
  Skill,
  ExecutionResult,
  Incident,
  Severity,
} from "@nexus-ai/sdk";
```

### Tratamento de Erros

```typescript
import {
  NexusError,
  RateLimitError,
  AuthenticationError,
  NotFoundError,
  ValidationError,
} from "@nexus-ai/sdk";

try {
  const agent = await client.agents.get("invalid-id");
} catch (e) {
  if (e instanceof NotFoundError) {
    console.log("Agent not found");
  } else if (e instanceof RateLimitError) {
    console.log(`Rate limited, retry after ${e.retryAfter}s`);
  } else if (e instanceof NexusError) {
    console.log(`Generic error: ${e.message}`);
  }
}
```

### React / Next.js Integration

```tsx
import { NexusProvider, useAgent } from "@nexus-ai/sdk/react";

function App() {
  return (
    <NexusProvider client={client}>
      <AgentDashboard />
    </NexusProvider>
  );
}

function AgentDashboard() {
  const { data, error, isLoading } = useAgent("agent-123");

  if (isLoading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;
  return <AgentCard agent={data} />;
}
```

---

## 🔄 Versionamento dos SDKs

Os SDKs seguem **Semantic Versioning** (semver):

- **MAJOR** (v2 → v3): breaking changes.
- **MINOR** (v2.1 → v2.2): features backwards-compatíveis.
- **PATCH** (v2.1.0 → v2.1.1): bugfixes.

**Política de suporte:**

- Última MAJOR: suporte ativo, features novas.
- Penúltima MAJOR: bugfixes por 12 meses.
- Mais antigas: sem suporte.

---

## 🛠️ Configuração Avançada

### Custom HTTP Client

```python
import httpx
from nexus import NexusClient

http_client = httpx.AsyncClient(
    timeout=60,
    limits=httpx.Limits(max_connections=100),
)

client = NexusClient(
    api_key="...",
    http_client=http_client,
)
```

### Custom Retry Policy

```typescript
const client = new NexusClient({
  apiKey: "...",
  retry: {
    maxRetries: 5,
    backoff: "exponential",
    initialDelayMs: 100,
    maxDelayMs: 10000,
    retryOn: [429, 502, 503, 504],
  },
});
```

### Custom Logger

```python
import logging
from nexus import NexusClient

logger = logging.getLogger("nexus")

client = NexusClient(
    api_key="...",
    logger=logger,
)
```

---

## 📦 Versionamento Canônico

| SDK | Versão | Status | Última release |
|-----|--------|--------|----------------|
| Python | v2.3.0 | Stable | 2026-06-15 |
| TypeScript | v2.3.0 | Stable | 2026-06-15 |
| Go | v1.0.0 | Beta | 2026-05-01 |
| Ruby | v0.9.0 | Alpha | 2026-04-10 |

---

## 🔐 Segurança nos SDKs

- **API keys** nunca são logadas.
- **TLS 1.3** obrigatório.
- **Certificate pinning** opcional.
- **Audit log** de toda chamada.
- **PII redaction** automática em logs.

---

## 📚 Documentos Relacionados

- [api-docs: `00-trpc-overview.md`](00-trpc-overview.md)
- [api-docs: `01-webhooks.md`](01-webhooks.md)
- [api-docs: `02-rest-public.md`](02-rest-public.md)
- [api-docs: `03-graphql-schema.md`](03-graphql-schema.md)
- [knowledge-base: `01-modelo-ioaid.md`](../knowledge-base/01-modelo-ioaid.md)
- [best-practices: `01-error-handling.md`](../best-practices/01-error-handling.md)

## 👥 Ownership

- **Owner:** Backend Lead + Frontend Lead
- **Reviewers:** DPO, SRE Lead
- **Cadência:** Mensal (release), Trimestral (revisão)

---

*Nexus Affil'IA'te · Lib-Nexus · api-docs/04-sdk-python-typescript.md · v1.0 · Julho 2026*
