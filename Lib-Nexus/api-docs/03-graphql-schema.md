---
title: "API Docs · GraphQL Schema"
description: "Schema GraphQL canônico da plataforma Nexus para queries federadas e real-time"
tags: [lib-nexus, api-docs, graphql, schema, real-time, federation]
category: api-docs
version: "1.0"
last_review: "2026-07-23"
---

# 🔌 API Docs · GraphQL Schema

> **Documentação canônica** do schema GraphQL da plataforma Nexus. Usado para queries federadas, real-time subscriptions, e integração avançada com frontends.

---

## 🎯 Quando usar GraphQL

GraphQL é recomendado quando:

- Cliente precisa de **queries flexíveis** (diferentes campos por view).
- Você quer **evitar over-fetching** de REST.
- Precisa de **subscriptions real-time** (WebSocket).
- Frontend tem **múltiplas visões** da mesma entidade.

**REST ainda é recomendado** para:

- Operações simples (CRUD).
- Cache de HTTP é importante.
- Clientes legacy não suportam GraphQL.

---

## 📍 Endpoint

| Ambiente | URL | Auth |
|----------|-----|------|
| Produção | `https://api.nexus.io/graphql` | Bearer token (JWT) |
| Staging | `https://staging-api.nexus.io/graphql` | Bearer token (JWT) |
| WebSocket (subscriptions) | `wss://api.nexus.io/graphql` | Bearer token (JWT) via `connectionParams` |

---

## 🔐 Autenticação

```http
POST /graphql HTTP/1.1
Host: api.nexus.io
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

JWT claims:
- `sub`: user_id
- `tenant_id`: tenant_id
- `roles`: ["admin", "operator", "viewer", ...]
- `exp`: expiration timestamp

---

## 📐 Schema Canônico

### Tipos Base

```graphql
scalar DateTime
scalar JSON
scalar UUID

enum Severity {
  SEV_0
  SEV_1
  SEV_2
  SEV_3
  SEV_4
}

enum AgentStatus {
  ACTIVE
  PAUSED
  QUARANTINED
  KILLED
}
```

### Tipos de Domínio

```graphql
type Tenant {
  id: UUID!
  name: String!
  status: String!
  plan: String!
  createdAt: DateTime!
  agents: [Agent!]!
  skills: [Skill!]!
  metrics: TenantMetrics!
}

type Agent {
  id: UUID!
  name: String!
  persona: String
  status: AgentStatus!
  version: String!
  skills: [Skill!]!
  lastExecution: DateTime
  metrics: AgentMetrics!
  createdAt: DateTime!
}

type Skill {
  id: UUID!
  name: String!
  version: String!
  description: String!
  author: String!
  category: String!
  rating: Float
  downloadCount: Int!
  publishedAt: DateTime
}

type AgentMetrics {
  totalExecutions: Int!
  successRate: Float!
  avgLatencyMs: Float!
  p99LatencyMs: Float!
  costUsdTotal: Float!
}

type TenantMetrics {
  mrrUsd: Float!
  activeAgents: Int!
  totalExecutions: Int!
  costUsdMonth: Float!
}

type Incident {
  id: UUID!
  severity: Severity!
  category: String!
  status: String!
  startedAt: DateTime!
  resolvedAt: DateTime
  summary: String!
  affectedTenants: [Tenant!]!
}
```

### Queries

```graphql
type Query {
  # Tenant
  tenant(id: UUID!): Tenant
  myTenant: Tenant!  # From JWT
  
  # Agent
  agent(id: UUID!): Agent
  agents(
    tenantId: UUID
    status: AgentStatus
    limit: Int = 20
    offset: Int = 0
  ): [Agent!]!
  
  # Skill
  skill(id: UUID!): Skill
  skills(
    category: String
    minRating: Float
    limit: Int = 20
    offset: Int = 0
  ): [Skill!]!
  
  # Incident
  incident(id: UUID!): Incident
  incidents(
    severity: Severity
    status: String
    since: DateTime
    limit: Int = 50
  ): [Incident!]!
  
  # Metrics
  agentMetrics(agentId: UUID!, since: DateTime): AgentMetrics!
  tenantMetrics(tenantId: UUID!, since: DateTime): TenantMetrics!
}
```

### Mutations

```graphql
type Mutation {
  # Agent
  createAgent(input: CreateAgentInput!): Agent!
  updateAgent(id: UUID!, input: UpdateAgentInput!): Agent!
  pauseAgent(id: UUID!): Agent!
  resumeAgent(id: UUID!): Agent!
  quarantineAgent(id: UUID!, reason: String!): Agent!
  killAgent(id: UUID!, reason: String!): Agent!
  
  # Skill
  installSkill(agentId: UUID!, skillId: UUID!): Agent!
  uninstallSkill(agentId: UUID!, skillId: UUID!): Agent!
  
  # Incident
  acknowledgeIncident(id: UUID!): Incident!
  resolveIncident(id: UUID!, resolution: String!): Incident!
}

input CreateAgentInput {
  name: String!
  persona: String
  skills: [UUID!]
  config: JSON
}

input UpdateAgentInput {
  name: String
  persona: String
  config: JSON
}
```

### Subscriptions (Real-time)

```graphql
type Subscription {
  # Streaming de eventos
  agentExecution(agentId: UUID!): ExecutionEvent!
  incidentUpdates(tenantId: UUID!): Incident!
  metricsStream(agentId: UUID!, intervalSec: Int = 10): MetricSample!
  shoAlerts(severity: Severity): Incident!
}

type ExecutionEvent {
  executionId: UUID!
  agentId: UUID!
  status: String!
  startedAt: DateTime!
  finishedAt: DateTime
  output: JSON
  error: String
}

type MetricSample {
  ts: DateTime!
  metric: String!
  value: Float!
  tags: JSON
}
```

---

## 💡 Exemplos de Uso

### Query 1 — Buscar agente com métricas

```graphql
query GetAgentWithMetrics($id: UUID!) {
  agent(id: $id) {
    id
    name
    status
    version
    skills {
      name
      version
    }
    metrics {
      totalExecutions
      successRate
      p99LatencyMs
    }
  }
}
```

**Resposta:**

```json
{
  "data": {
    "agent": {
      "id": "agent-123",
      "name": "WhatsApp Copy Agent",
      "status": "ACTIVE",
      "version": "2.1.0",
      "skills": [
        { "name": "whatsapp-copy-v3", "version": "3.0.0" }
      ],
      "metrics": {
        "totalExecutions": 12450,
        "successRate": 0.94,
        "p99LatencyMs": 187
      }
    }
  }
}
```

### Mutation 1 — Quarentenar agente

```graphql
mutation QuarantineAgent($id: UUID!, $reason: String!) {
  quarantineAgent(id: $id, reason: $reason) {
    id
    status
  }
}
```

**Variáveis:**

```json
{
  "id": "agent-123",
  "reason": "Anomalia detectada: 5x latência normal"
}
```

### Subscription 1 — Streaming de execuções

```graphql
subscription WatchAgent($id: UUID!) {
  agentExecution(agentId: $id) {
    executionId
    status
    finishedAt
    error
  }
}
```

---

## 🔐 Autorização (AuthZ)

Resolução por **Policy Engine** baseado em:

- `tenant_id` do JWT
- `roles` do JWT
- `attributes` do recurso solicitado
- `policy` do tenant

Exemplo de regra:

```yaml
rule:
  roles: ["operator", "admin"]
  resource: "Agent"
  action: ["read", "pause", "resume"]
  conditions:
    - "JWT.tenant_id == Agent.tenant_id"
```

---

## ⚠️ Rate Limiting

| Operação | Limite |
|----------|--------|
| Queries | 1000/min por token |
| Mutations | 100/min por token |
| Subscriptions | 10 ativas por token |

Resposta 429 com `Retry-After` header quando excedido.

---

## 📊 Observabilidade

- **Tracing distribuído** via Apollo Studio / OpenTelemetry.
- **Caching** via Apollo Cache (configurável por query).
- **Persisted queries** para reduzir bandwidth.
- **Subscriptions** com heartbeat a cada 30s.

---

## 🛠️ Ferramentas Recomendadas

- **Apollo Studio** (graph manager).
- **GraphQL Playground** (debug).
- **Altair** (cliente desktop).
- **Postman** (com GraphQL support).

---

## 📚 Documentos Relacionados

- [api-docs: `00-trpc-overview.md`](00-trpc-overview.md)
- [api-docs: `01-webhooks.md`](01-webhooks.md)
- [api-docs: `02-rest-public.md`](02-rest-public.md)
- [knowledge-base: `01-modelo-ioaid.md`](../knowledge-base/01-modelo-ioaid.md)
- [best-practices: `05-sre-observability.md`](../best-practices/05-sre-observability.md)

## 👥 Ownership

- **Owner:** Head de Arquitetura + Backend Lead
- **Reviewers:** DPO, SRE Lead
- **Cadência:** Trimestral

---

*Nexus Affil'IA'te · Lib-Nexus · api-docs/03-graphql-schema.md · v1.0 · Julho 2026*
