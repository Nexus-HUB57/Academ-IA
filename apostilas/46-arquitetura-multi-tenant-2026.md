---
title: "Apostila 46 · Arquitetura Multi-Tenant para Agentes IA"
subtitle: "Como construir plataforma SaaS com isolamento, billing e federation para múltiplos clientes"
author: "Equipo Nexus · Ravi (CTO/AI) + Sir. Nexus Alencar"
version: "1.0.0"
date: 2026-07-30
pattern: "MMN_IA"
---

**Apostila 46 · Arquitetura Multi-Tenant para Agentes IA**

*O guia completo de 2026 para construir plataforma SaaS de agentes IA multi-tenant. Inclui modelos de isolamento, billing, rate limiting, observabilidade e federation.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 Por Que Esta Apostila é Crítica

**A maioria dos afiliados Nexus quer:**
- Atender **múltiplos clientes** com 1 plataforma
- Cada cliente com seus **dados isolados**
- **Billing por uso** (não por assinatura fixa)
- **Escalar** para 100+ tenants sem reescrever

**Multi-tenant mal feito:**
- ❌ Tenant A vê dados de Tenant B (LGPD art. 48 = multa)
- ❌ Tenant "barulhento" derruba todos os outros (noisy neighbor)
- ❌ Billing errado = churn + receita perdida
- ❌ Impossível escalar > 50 tenants

**Multi-tenant bem feito:**
- ✅ Isolamento perfeito (performance + dados)
- ✅ Billing automático por uso real
- ✅ Observabilidade por tenant
- ✅ Federation para escalar globalmente
- ✅ Onboarding self-serve

**Esta apostila é seu blueprint para chegar lá.**

---

## 📚 Sumário

1. Modelos de Multi-Tenancy
2. Isolamento de Dados
3. Isolamento de Performance
4. Identity & Access Management
5. Rate Limiting por Tenant
6. Billing & Metering
7. Observabilidade por Tenant
8. Federation Cross-Region
9. Migration de Single para Multi-Tenant
10. Casos Reais
11. Anti-patterns
12. Stack Recomendado

---

## 🏗️ 1. Modelos de Multi-Tenancy

### 1.1 — Os 3 Modelos Clássicos

**Modelo A: Database per Tenant**

```
┌─────────┐ ┌─────────┐ ┌─────────┐
│Tenant A │ │Tenant B │ │Tenant C │
│  DB     │ │  DB     │ │  DB     │
└────┬────┘ └────┬────┘ └────┬────┘
     │           │           │
     └───────────┴───────────┘
              │
         ┌────┴────┐
         │  App    │
         │ Server  │
         └─────────┘
```

**Vantagens:**
- Isolamento perfeito (performance + dados)
- Compliance facilitado (LGPD, HIPAA)
- Backup/restore por tenant fácil
- Customização por tenant (schema próprio)

**Desvantagens:**
- Custo alto (N databases para N tenants)
- Migração de schema complexa
- Operação pesada (N backups, N monitoring)
- Connection pool explode

**Quando usar:**
- Compliance crítico (saúde, finanças)
- Clientes enterprise (5-50 tenants)
- Customização por tenant necessária

---

**Modelo B: Schema per Tenant (mesma DB)**

```
┌─────────┐ ┌─────────┐ ┌─────────┐
│Tenant A │ │Tenant B │ │Tenant C │
│ Schema  │ │ Schema  │ │ Schema  │
└────┬────┘ └────┬────┘ └────┬────┘
     │           │           │
     └───────────┴───────────┘
              │
         ┌────┴────┐
         │Postgres│
         └─────────┘
```

**Vantagens:**
- Isolamento bom (queries filtered por schema)
- Custo menor (1 DB)
- Customização ainda possível
- Migração mais simples

**Desvantagens:**
- Ainda pesado para 1000+ tenants
- Backups por schema são tricky
- PostgreSQL limits (milhões de schemas?)

**Quando usar:**
- 50-500 tenants
- Compliance moderado
- Customização por tenant (campos extras)

---

**Modelo C: Row-Level Security (mesma tabela)**

```
┌─────────────────────────────────┐
│         users table             │
├─────────────────────────────────┤
│ id │ tenant_id │ name  │ email  │
├────┼───────────┼───────┼────────┤
│ 1  │ tenant_a  │ Ana   │ ana@   │
│ 2  │ tenant_b  │ Bruno │ bruno@ │
│ 3  │ tenant_a  │ Carla │ carla@ │
└─────────────────────────────────┘
         ▲
         │ RLS policy: WHERE tenant_id = current_tenant()
```

**Vantagens:**
- Custo mínimo (1 DB, 1 schema)
- Escala massiva (10.000+ tenants)
- Operação simples
- Multi-region facilitado

**Desvantagens:**
- Risco de bug = vazamento entre tenants
- Customização por tenant impossível
- Backup/restore mais complexo
- Performance pode degradar sem índices adequados

**Quando usar:**
- 1000+ tenants
- Customização mínima
- Self-serve (B2B SaaS)

### 1.2 — Modelo Híbrido (Recomendado 2026)

**Tier-based:**

| Tier | Modelo | Customização | Quando |
|------|--------|--------------|--------|
| **Free** | Row-level | Mínima | Onboarding, auto-serve |
| **Pro** | Row-level | Mínima | 90% dos clientes |
| **Enterprise** | Schema ou DB | Total | 5-10 clientes premium |

**Vantagem:** otimiza custo para maioria, oferece isolamento para high-value.

### 1.3 — Comparativo

| Aspecto | DB per Tenant | Schema per Tenant | Row-Level |
|---------|---------------|-------------------|-----------|
| **Custo DB** | Alto | Médio | Baixo |
| **Isolamento** | Total | Alto | Médio |
| **Escala (nº tenants)** | 5-50 | 50-500 | 1000+ |
| **Compliance** | Excelente | Bom | OK |
| **Customização** | Total | Alta | Nenhuma |
| **Complexidade ops** | Alta | Média | Baixa |
| **Migração schema** | Difícil | Média | Fácil |
| **Onboarding** | Lento (provisiona DB) | Médio | Instantâneo |

---

## 🔒 2. Isolamento de Dados

### 2.1 — Row-Level Security (PostgreSQL)

```sql
-- Setup
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_users_tenant ON users(tenant_id);

-- Habilitar RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Policy: usuários só veem dados do seu tenant
CREATE POLICY tenant_isolation ON users
    USING (tenant_id = current_setting('app.current_tenant')::UUID);

-- Para service role (admin, migrations), bypass RLS
ALTER TABLE users FORCE ROW LEVEL SECURITY;  -- service role também obey
```

```python
# FastAPI middleware
from fastapi import Request
import asyncpg


async def set_tenant_context(request: Request, call_next):
    """Seta tenant_id na conexão para RLS"""
    tenant_id = request.state.tenant_id  # vem do JWT

    # Pegar conexão do pool
    async with request.app.state.db.acquire() as conn:
        # Setar contexto
        await conn.execute(
            "SET LOCAL app.current_tenant = $1",
            str(tenant_id)
        )

        # Adicionar conexão ao request
        request.state.db = conn

        response = await call_next(request)

    return response
```

### 2.2 — Schema per Tenant (PostgreSQL)

```python
"""
Schema per tenant com router.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TenantRouter:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.engines = {}  # cache de engines

    def get_engine(self, tenant_id: str):
        """Retorna engine SQLAlchemy para o schema do tenant"""
        if tenant_id not in self.engines:
            engine = create_engine(
                f"{self.base_url}/nexus_main",
                pool_size=5,
                max_overflow=10,
            )
            # Garantir schema existe
            with engine.begin() as conn:
                conn.execute(f"CREATE SCHEMA IF NOT EXISTS tenant_{tenant_id}")
                conn.execute(f"SET search_path TO tenant_{tenant_id}, public")

            self.engines[tenant_id] = engine

        return self.engines[tenant_id]


# Uso
router = TenantRouter("postgresql://user:pass@host:5432")

@app.get("/users")
async def get_users(request: Request):
    tenant_id = request.state.tenant_id
    engine = router.get_engine(tenant_id)
    Session = sessionmaker(bind=engine)
    session = Session()

    users = session.query(User).all()
    return users
```

### 2.3 — Encryption at Rest per Tenant

```python
"""
Cada tenant tem chave de encryption própria.
Compliance: LGPD art. 46, HIPAA.
"""
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os


class TenantEncryption:
    def __init__(self, master_key: bytes):
        self.master_key = master_key

    def derive_tenant_key(self, tenant_id: str, salt: bytes) -> bytes:
        """Deriva chave única por tenant"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
        )
        key = base64.urlsafe_b64encode(
            kdf.derive(self.master_key + tenant_id.encode())
        )
        return key

    def encrypt(self, data: str, tenant_id: str) -> bytes:
        """Encrypt dados com chave do tenant"""
        salt = os.urandom(16)
        key = self.derive_tenant_key(tenant_id, salt)
        f = Fernet(key)
        encrypted = f.encrypt(data.encode())
        return salt + encrypted  # prefix com salt

    def decrypt(self, encrypted_data: bytes, tenant_id: str) -> str:
        """Decrypt com chave do tenant"""
        salt = encrypted_data[:16]
        encrypted = encrypted_data[16:]
        key = self.derive_tenant_key(tenant_id, salt)
        f = Fernet(key)
        return f.decrypt(encrypted).decode()


# Uso
enc = TenantEncryption(master_key=os.environ["MASTER_KEY"].encode())
encrypted = enc.encrypt("CPF: 123.456.789-00", tenant_id="acme")
decrypted = enc.decrypt(encrypted, tenant_id="acme")
```

---

## ⚡ 3. Isolamento de Performance

### 3.1 — O Problema: Noisy Neighbor

**Cenário:**
- Tenant A: rodando job pesado (10k requests/min)
- Tenant B: rodando 100 requests/min
- Sem isolamento: Tenant B tem latência 10x pior

### 3.2 — Solução: Resource Pools por Tier

```python
"""
Pool de workers/conexões por tier.
"""
import asyncio
from contextlib import asynccontextmanager


class TenantResourcePool:
    def __init__(self):
        self.pools = {
            "free": {"concurrency": 5, "queue_size": 50},
            "pro": {"concurrency": 50, "queue_size": 500},
            "enterprise": {"concurrency": 500, "queue_size": 5000},
        }
        self.semaphores = {
            tier: asyncio.Semaphore(config["concurrency"])
            for tier, config in self.pools.items()
        }
        self.queues = {
            tier: asyncio.Queue(maxsize=config["queue_size"])
            for tier, config in self.pools.items()
        }

    @asynccontextmanager
    async def acquire(self, tenant_tier: str):
        """Adquire slot no pool do tier"""
        sem = self.semaphores[tenant_tier]
        await sem.acquire()
        try:
            yield
        finally:
            sem.release()


# Uso
pool = TenantResourcePool()


@app.post("/invoke")
async def invoke(request: Request):
    tier = request.state.tenant_tier

    async with pool.acquire(tier):
        result = await llm_call(request.message)

    return result
```

### 3.3 — Rate Limiting por Tenant

```python
"""
Rate limit baseado em tokens (token bucket).
Cada tenant tem bucket próprio.
"""
import time
from collections import defaultdict


class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.tokens = capacity
        self.last_refill = time.time()

    def consume(self, tokens: int = 1) -> bool:
        """Tenta consumir tokens. Retorna True se sucesso"""
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


class RateLimiter:
    def __init__(self):
        self.buckets = defaultdict(lambda: TokenBucket(
            capacity=100,  # burst
            refill_rate=10,  # 10 req/s sustained
        ))

    def check(self, tenant_id: str, tokens: int = 1) -> bool:
        return self.buckets[tenant_id].consume(tokens)


# Limites por tier
TIER_LIMITS = {
    "free": {"capacity": 100, "refill_rate": 1},      # 1 req/s, burst 100
    "pro": {"capacity": 1000, "refill_rate": 50},     # 50 req/s, burst 1000
    "enterprise": {"capacity": 10000, "refill_rate": 500},  # 500 req/s, burst 10k
}


limiter = RateLimiter()


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    tenant_id = request.state.tenant_id
    tier = request.state.tenant_tier
    limits = TIER_LIMITS[tier]

    # Reconfigurar bucket do tenant com tier-specific limits
    if tenant_id not in limiter.buckets:
        limiter.buckets[tenant_id] = TokenBucket(
            capacity=limits["capacity"],
            refill_rate=limits["refill_rate"],
        )

    if not limiter.buckets[tenant_id].consume():
        return JSONResponse(
            status_code=429,
            content={"error": "rate_limit_exceeded", "retry_after": 1},
        )

    return await call_next(request)
```

### 3.4 — Circuit Breaker por Tenant

```python
"""
Circuit breaker isolado por tenant.
Se tenant X está com problemas, não afeta os outros.
"""
import time
from enum import Enum


class CircuitState(Enum):
    CLOSED = "closed"  # normal
    OPEN = "open"      # falhou, bloqueia
    HALF_OPEN = "half_open"  # testando se recuperou


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = CircuitState.CLOSED
        self.failures = 0
        self.last_failure = None

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure > self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker OPEN")

        try:
            result = func(*args, **kwargs)
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure = time.time()
            if self.failures >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise


# Pool de circuit breakers por tenant
class TenantCircuitBreakers:
    def __init__(self):
        self.breakers = {}

    def get(self, tenant_id: str) -> CircuitBreaker:
        if tenant_id not in self.breakers:
            self.breakers[tenant_id] = CircuitBreaker()
        return self.breakers[tenant_id]


tenant_breakers = TenantCircuitBreakers()
```

---

## 🆔 4. Identity & Access Management

### 4.1 — JWT Multi-Tenant

```python
"""
JWT com tenant_id, role, permissions.
"""
import jwt
from datetime import datetime, timedelta
from typing import Literal


def create_jwt(user_id: str, tenant_id: str, role: str,
              permissions: list, expires_in: int = 3600) -> str:
    """Cria JWT com claims multi-tenant"""
    payload = {
        "sub": user_id,
        "tenant_id": tenant_id,
        "role": role,  # admin, member, viewer
        "permissions": permissions,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(seconds=expires_in),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_jwt(token: str) -> dict:
    """Decodifica e valida JWT"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")


# Middleware
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()


async def auth_middleware(request: Request, call_next):
    auth = await security(request)
    payload = decode_jwt(auth.credentials)

    request.state.user_id = payload["sub"]
    request.state.tenant_id = payload["tenant_id"]
    request.state.role = payload["role"]
    request.state.permissions = payload["permissions"]

    return await call_next(request)


# Decorator para verificar permissão
def require_permission(permission: str):
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            if permission not in request.state.permissions:
                raise HTTPException(status_code=403, detail="Forbidden")
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator


@app.post("/agents/{agent_id}/invoke")
@require_permission("agent:invoke")
async def invoke_agent(agent_id: str, request: Request):
    # request.state.tenant_id disponível
    ...
```

### 4.2 — RBAC (Role-Based Access Control)

```python
"""
Roles padrão para Nexus:
- owner: tudo (criou o tenant)
- admin: gerencia membros, billing, settings
- member: usa agentes, vê seus dados
- viewer: read-only
"""

ROLE_PERMISSIONS = {
    "owner": ["*"],
    "admin": [
        "tenant:read", "tenant:update",
        "user:invite", "user:remove", "user:list",
        "agent:create", "agent:update", "agent:delete", "agent:invoke",
        "billing:read", "billing:update",
    ],
    "member": [
        "agent:invoke", "agent:read",
        "data:read:own", "data:write:own",
    ],
    "viewer": [
        "agent:read", "data:read:own",
    ],
}


def check_permission(role: str, permission: str) -> bool:
    if "*" in ROLE_PERMISSIONS.get(role, []):
        return True
    return permission in ROLE_PERMISSIONS.get(role, [])
```

### 4.3 — API Keys por Tenant

```python
"""
API keys para integração server-to-server.
Cada tenant pode ter múltiplas keys.
"""
import secrets
import hashlib


class APIKeyManager:
    def create_key(self, tenant_id: str, name: str) -> dict:
        """Cria API key para tenant"""
        # Gerar key (32 bytes = 64 chars hex)
        raw_key = f"nxs_{secrets.token_urlsafe(32)}"

        # Hash para armazenar (nunca plaintext)
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

        # Salvar no DB
        api_key = {
            "id": str(uuid.uuid4()),
            "tenant_id": tenant_id,
            "name": name,
            "key_hash": key_hash,
            "prefix": raw_key[:12],  # "nxs_abc12345" para display
            "created_at": datetime.utcnow(),
            "last_used": None,
        }
        db.insert(api_key)

        # Retornar raw key APENAS UMA VEZ
        return {**api_key, "raw_key": raw_key}

    def verify_key(self, raw_key: str) -> dict:
        """Verifica key e retorna info do tenant"""
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        api_key = db.query("SELECT * FROM api_keys WHERE key_hash = ?", key_hash)

        if not api_key:
            raise Exception("Invalid API key")

        # Update last_used
        db.execute(
            "UPDATE api_keys SET last_used = ? WHERE id = ?",
            datetime.utcnow(), api_key["id"],
        )

        return api_key
```

---

## 💰 5. Billing & Metering

### 5.1 — Métricas de Billing

**O que cobrar:**
- **API calls** (nº de requests)
- **Tokens consumidos** (input + output)
- **Storage** (GB de dados armazenados)
- **Compute time** (tempo de execução)
- **Features premium** (advanced analytics, etc)

**Pricing tiers típicos:**

| Tier | Mensal | Incluso | Overage |
|------|--------|---------|---------|
| **Free** | R$ 0 | 1k requests + 100k tokens | - |
| **Pro** | R$ 297 | 100k requests + 10M tokens | R$ 0.001/request |
| **Enterprise** | Custom | Custom | Custom |

### 5.2 — Usage Tracking

```python
"""
Rastreia uso por tenant em tempo real.
"""
from datetime import datetime
import redis


class UsageTracker:
    def __init__(self):
        self.redis = redis.Redis()

    def record_usage(self, tenant_id: str, metric: str, value: float):
        """Registra uso (atomic increment)"""
        month_key = datetime.now().strftime("%Y-%m")
        key = f"usage:{tenant_id}:{month_key}:{metric}"
        self.redis.incrbyfloat(key, value)

        # Expirar após 90 dias
        self.redis.expire(key, 90 * 24 * 3600)

    def get_usage(self, tenant_id: str, month: str = None) -> dict:
        """Retorna uso agregado do mês"""
        if month is None:
            month = datetime.now().strftime("%Y-%m")

        metrics = ["requests", "tokens_in", "tokens_out", "storage_gb"]
        usage = {}
        for metric in metrics:
            key = f"usage:{tenant_id}:{month}:{metric}"
            value = self.redis.get(key)
            usage[metric] = float(value) if value else 0

        return usage


# Uso
tracker = UsageTracker()


@app.post("/invoke")
async def invoke(request: Request):
    tenant_id = request.state.tenant_id

    # Fazer invoke
    response = await llm_call(request.message)

    # Registrar uso
    tracker.record_usage(tenant_id, "requests", 1)
    tracker.record_usage(tenant_id, "tokens_in", response.usage.prompt_tokens)
    tracker.record_usage(tenant_id, "tokens_out", response.usage.completion_tokens)

    return response
```

### 5.3 — Invoice Generation

```python
"""
Gera invoice mensal baseado em usage tracking.
"""
from dataclasses import dataclass


@dataclass
class Invoice:
    tenant_id: str
    month: str
    base_fee: float
    overage_charges: dict
    total: float


class BillingService:
    PRICING = {
        "free": {"base": 0, "included": {"requests": 1000, "tokens": 100_000}},
        "pro": {"base": 297, "included": {"requests": 100_000, "tokens": 10_000_000}},
    }

    OVERAGE_RATES = {
        "requests": 0.001,  # R$ 0.001/request
        "tokens": 0.0001,   # R$ 0.0001/token (1k tokens = R$ 0.10)
    }

    def generate_invoice(self, tenant_id: str, tier: str, month: str) -> Invoice:
        """Gera invoice do mês"""
        usage = tracker.get_usage(tenant_id, month)
        pricing = self.PRICING[tier]
        included = pricing["included"]

        # Calcular overage
        overage_requests = max(0, usage["requests"] - included["requests"])
        overage_tokens = max(0, usage["tokens_in"] + usage["tokens_out"] - included["tokens"])

        overage_charges = {
            "requests": overage_requests * self.OVERAGE_RATES["requests"],
            "tokens": overage_tokens * self.OVERAGE_RATES["tokens"],
        }

        total_overage = sum(overage_charges.values())
        total = pricing["base"] + total_overage

        return Invoice(
            tenant_id=tenant_id,
            month=month,
            base_fee=pricing["base"],
            overage_charges=overage_charges,
            total=total,
        )
```

### 5.4 — Stripe Integration

```python
"""
Sincroniza invoices com Stripe.
"""
import stripe

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]


class StripeBilling:
    def create_customer(self, tenant_id: str, email: str) -> str:
        """Cria customer no Stripe"""
        customer = stripe.Customer.create(
            email=email,
            metadata={"tenant_id": tenant_id},
        )
        return customer.id

    def create_subscription(self, customer_id: str, tier: str) -> str:
        """Cria subscription com tier"""
        price_ids = {
            "pro": "price_xxx_pro",
            "enterprise": "price_xxx_ent",
        }
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": price_ids[tier]}],
        )
        return subscription.id

    def report_usage(self, subscription_id: str, quantity: int):
        """Reporta usage (metered billing)"""
        stripe.SubscriptionItem.create_usage_record(
            subscription_id,
            quantity=quantity,
            timestamp=int(time.time()),
            action="increment",
        )

    def generate_invoice_pdf(self, customer_id: str, month: str) -> str:
        """Gera PDF do invoice"""
        invoice = stripe.Invoice.create(
            customer=customer_id,
            collection_method="send_invoice",
            days_until_due=30,
        )
        return invoice.invoice_pdf
```

---

## 📊 6. Observabilidade por Tenant

### 6.1 — Métricas Segmentadas

```python
"""
Prometheus metrics por tenant.
"""
from prometheus_client import Counter, Histogram, Gauge

REQUEST_COUNT = Counter(
    'nexus_requests_total',
    'Total de requests',
    labelnames=['tenant_id', 'endpoint', 'status'],
)

REQUEST_LATENCY = Histogram(
    'nexus_request_latency_seconds',
    'Latência de requests',
    labelnames=['tenant_id', 'endpoint'],
    buckets=(0.1, 0.5, 1, 2, 5, 10),
)

ACTIVE_USERS = Gauge(
    'nexus_active_users',
    'Usuários ativos (5min)',
    labelnames=['tenant_id'],
)

TOKEN_USAGE = Counter(
    'nexus_tokens_total',
    'Tokens consumidos',
    labelnames=['tenant_id', 'model', 'direction'],
)

COST_USD = Counter(
    'nexus_cost_usd_total',
    'Custo em USD',
    labelnames=['tenant_id', 'model'],
)
```

### 6.2 — Grafana Dashboard por Tenant

```json
{
  "dashboard": {
    "title": "Tenant {{tenant_id}} · Overview",
    "templating": {
      "list": [
        {
          "name": "tenant_id",
          "type": "query",
          "query": "label_values(nexus_requests_total, tenant_id)"
        }
      ]
    },
    "panels": [
      {
        "title": "Requests/s",
        "targets": [{
          "expr": "sum(rate(nexus_requests_total{tenant_id=\"$tenant_id\"}[5m]))"
        }]
      },
      {
        "title": "Latência p95",
        "targets": [{
          "expr": "histogram_quantile(0.95, sum by (le) (rate(nexus_request_latency_seconds_bucket{tenant_id=\"$tenant_id\"}[5m])))"
        }]
      },
      {
        "title": "Custo acumulado (mês)",
        "targets": [{
          "expr": "sum(increase(nexus_cost_usd_total{tenant_id=\"$tenant_id\"}[30d]))"
        }]
      }
    ]
  }
}
```

### 6.3 — Log Aggregation

```python
"""
Structured logging com tenant_id em todos os logs.
"""
import structlog


def get_logger(tenant_id: str):
    return structlog.get_logger().bind(tenant_id=tenant_id)


# Middleware
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    tenant_id = getattr(request.state, "tenant_id", "anonymous")
    log = get_logger(tenant_id)

    log.info("request_started", method=request.method, path=request.url.path)

    response = await call_next(request)

    log.info(
        "request_completed",
        status=response.status_code,
        duration_ms=response.headers.get("X-Process-Time"),
    )

    return response
```

---

## 🌍 7. Federation Cross-Region

### 7.1 — Por Que Federation

**Cenários:**
- Latência: cliente em SP, agente em US-EAST → 150ms
- Compliance: dados europeus devem ficar na UE
- Resiliência: US-EAST cai, falha tudo

### 7.2 — Estratégia: Active-Active

```
Tenant Global
├── US-EAST (Virginia)
│   ├── DB primária
│   ├── Cache (Redis)
│   └── API instances
├── EU-WEST (Ireland)
│   ├── DB replica
│   ├── Cache
│   └── API instances
└── AP-SE (Singapore)
    ├── DB replica
    ├── Cache
    └── API instances
```

**Implementação:**
- GeoDNS (Route 53 / Cloudflare) roteia para região mais próxima
- DB cross-region replication
- Session state em Redis global

### 7.3 — Cross-Region Replication

```python
"""
PostgreSQL cross-region replication.
"""
import asyncpg


class CrossRegionDB:
    def __init__(self):
        self.regions = {
            "us-east": "postgresql://user:pass@us-east.db:5432/main",
            "eu-west": "postgresql://user:pass@eu-west.db:5432/main",
            "ap-se": "postgresql://user:pass@ap-se.db:5432/main",
        }
        self.pools = {
            region: asyncpg.create_pool(url, min_size=5, max_size=20)
            for region, url in self.regions.items()
        }

    async def write(self, region: str, query: str, *args):
        """Write vai para primária da região"""
        async with self.pools[region].acquire() as conn:
            return await conn.fetch(query, *args)

    async def read(self, region: str, query: str, *args):
        """Read vai para replica mais próxima"""
        async with self.pools[region].acquire() as conn:
            return await conn.fetch(query, *args)


# Uso
db = CrossRegionDB()


@app.post("/users")
async def create_user(tenant_id: str, user_data: dict):
    region = get_user_region(tenant_id)  # based on IP/setting
    user = await db.write(region, "INSERT INTO users ...", ...)
    return user
```

### 7.4 — Session Stickiness

```python
"""
Session deve ser sticky para a região onde foi criada.
"""
import redis
import json


class SessionManager:
    def __init__(self):
        # Redis cluster global (Elasticache, Memorystore, etc)
        self.redis = redis.RedisCluster(...)

    def create_session(self, user_id: str, region: str, data: dict) -> str:
        session_id = secrets.token_urlsafe(32)
        session = {
            "user_id": user_id,
            "region": region,
            "data": data,
            "created_at": time.time(),
        }
        self.redis.setex(f"session:{session_id}", 3600, json.dumps(session))
        return session_id

    def get_session(self, session_id: str) -> dict:
        session = json.loads(self.redis.get(f"session:{session_id}"))
        # Se request chega em região diferente, redirecionar
        request_region = get_current_region()
        if session["region"] != request_region:
            # Redirecionar para região da session
            raise RedirectToRegion(session["region"])
        return session
```

---

## 🔄 8. Migration de Single para Multi-Tenant

### 8.1 — Estratégia Incremental

**Fase 1: Adicionar tenant_id em tudo (1 sprint)**
- Adicionar coluna `tenant_id` em todas as tabelas
- Backfill com tenant_id default para dados existentes
- Adicionar índices

**Fase 2: RLS (1 sprint)**
- Habilitar RLS nas tabelas
- Implementar middleware de tenant context
- Adicionar testes de isolamento

**Fase 3: Auth multi-tenant (1 sprint)**
- JWT com tenant_id
- API keys por tenant
- RBAC

**Fase 4: Billing (1 sprint)**
- Usage tracking
- Invoice generation
- Stripe integration

**Fase 5: Federation (2 sprints, opcional)**
- Multi-region
- GeoDNS
- Cross-region replication

### 8.2 — Backfill de Dados

```sql
-- 1. Adicionar coluna
ALTER TABLE users ADD COLUMN tenant_id UUID;

-- 2. Backfill com tenant default
UPDATE users SET tenant_id = '00000000-0000-0000-0000-000000000001';

-- 3. Adicionar constraint
ALTER TABLE users ALTER COLUMN tenant_id SET NOT NULL;
ALTER TABLE users ADD CONSTRAINT fk_users_tenant
    FOREIGN KEY (tenant_id) REFERENCES tenants(id);

-- 4. Índice
CREATE INDEX idx_users_tenant ON users(tenant_id);
```

### 8.3 — Migração de Schema

```python
"""
Migração zero-downtime.
"""
import asyncio
from datetime import datetime


class ZeroDowntimeMigration:
    def migrate_users_table(self):
        """Migra single-tenant para multi-tenant em 4 steps"""

        # Step 1: Adicionar coluna (instantâneo, sem lock)
        self.db.execute("""
            ALTER TABLE users ADD COLUMN tenant_id UUID;
        """)

        # Step 2: Backfill em batches (sem lock)
        last_id = None
        while True:
            query = """
                UPDATE users
                SET tenant_id = '00000000-0000-0000-0000-000000000001'
                WHERE id > $1 AND tenant_id IS NULL
                ORDER BY id
                LIMIT 1000
                RETURNING id;
            """
            params = [last_id] if last_id else [""]
            batch = self.db.execute(query, *params)
            if not batch:
                break
            last_id = batch[-1][0]
            print(f"Migrated up to id {last_id}")

        # Step 3: NOT NULL constraint (lock curto)
        self.db.execute("""
            ALTER TABLE users ALTER COLUMN tenant_id SET NOT NULL;
        """)

        # Step 4: Habilitar RLS (lock curto)
        self.db.execute("""
            ALTER TABLE users ENABLE ROW LEVEL SECURITY;
        """)

        print("Migration completed!")
```

---

## 📚 9. Casos Reais

### Caso 1: SaaS Vertical para Clínicas

**Empresa:** HealthBot (fictícia)

**Desafio:** 60 clínicas, dados sensíveis (LGPD + CFM).

**Solução:**
- DB per tenant (compliance)
- 60 databases PostgreSQL
- 1 API instance com router de schema
- Billing fixo mensal (R$ 497/clínica)

**Resultado:**
- R$ 30k MRR (60 × R$ 497)
- Churn 2%/mês (compliance = sticky)
- LTV R$ 25k/clínica

### Caso 2: Plataforma Self-Serve B2B

**Empresa:** AgentCloud (fictícia)

**Desafio:** 2.000+ clientes, self-serve, variabilidade alta.

**Solução:**
- Row-level security
- Stripe metered billing (por uso)
- 3 tiers (Free, Pro, Enterprise)
- API keys por tenant

**Resultado:**
- 2.000 tenants
- ARPU R$ 350/mês
- ARR R$ 8.4M

### Caso 3: Multi-Region para Latência

**Empresa:** GlobalLLM (fictícia)

**Desafio:** Clientes em 3 continentes, latência 200ms+.

**Solução:**
- 3 regiões (US, EU, AP)
- Cross-region replication
- GeoDNS
- Session stickiness

**Resultado:**
- p95 latência: 250ms → 45ms
- Expansão para 3 novos mercados

---

## ⚠️ 10. Anti-patterns

### ❌ 1. Tenant ID na URL mas não validado

```python
# ERRADO: confia no path parameter
@app.get("/tenants/{tenant_id}/users")
async def get_users(tenant_id: str):
    return db.query("SELECT * FROM users WHERE tenant_id = ?", tenant_id)
    # Tenant A pode ver dados de Tenant B se souber o ID!
```

```python
# CORRETO: usar tenant_id do JWT
@app.get("/users")
async def get_users(request: Request):
    tenant_id = request.state.tenant_id  # do JWT, validado
    return db.query("SELECT * FROM users WHERE tenant_id = ?", tenant_id)
```

### ❌ 2. Sem RLS em queries "extras"

```python
# ERRADO: query sem WHERE tenant_id
def get_user_email(user_id: str):
    return db.query("SELECT email FROM users WHERE id = ?", user_id)
    # Sem RLS, retorna email de qualquer tenant!
```

**Sempre use RLS + WHERE explícito.**

### ❌ 3. Cache compartilhado entre tenants

```python
# ERRADO
cache_key = f"user:{user_id}"
# Tenant A pode acessar cache de Tenant B!
```

```python
# CORRETO
cache_key = f"user:{tenant_id}:{user_id}"
```

### ❌ 4. Logs sem tenant_id

```python
# ERRADO
logger.info("user_logged_in", user_id=user_id)

# CORRETO
logger.info("user_logged_in", tenant_id=tenant_id, user_id=user_id)
```

---

## 🛠️ 11. Stack Recomendado

**Application:**
- FastAPI (Python) ou NestJS (TypeScript)
- PostgreSQL (DB + RLS)
- Redis (cache + rate limit)
- LangChain / LlamaIndex (orquestração)

**Observability:**
- Grafana + Prometheus (métricas)
- Loki / Elasticsearch (logs)
- Jaeger / Tempo (traces)
- Sentry (errors)

**Billing:**
- Stripe (pagamentos + subscription)
- Metoro / Custom (usage tracking)
- Lago / Custom (invoice generation)

**Auth:**
- Auth0 / Clerk / Supabase Auth (managed)
- OU custom (JWT + bcrypt)

**Multi-region:**
- AWS (RDS + ElastiCache + Route 53)
- GCP (Cloud SQL + Memorystore + Cloud DNS)
- Cloudflare (CDN + Workers + KV)

---

## 📚 Materiais Complementares

- `treinamentos/WS-12-oficina-arquitetura-multi-tenant.md` — workshop
- `apostilas/45-debugging-otimizacao-agentes-ia.md` — debug
- `Lib-Nexus/api-docs/04-sdk-python-typescript.md` — SDK
- `Lib-Nexus/agents-specs/06-sho-operator-agent.md` — SHO
- `Lib-Nexus/knowledge-base/05-modelo-federation.md` — federation
- `Lib-Nexus/best-practices/05-sre-observability.md` — observability
- `playbooks/PB-FEDERATION-operacao-cross-region.md` — playbook

---

## 🔗 Links Externos

- PostgreSQL RLS: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- Stripe Billing: https://stripe.com/docs/billing
- AWS Multi-Region: https://aws.amazon.com/getting-started/hands-on/build-multi-region-application/
- Auth0 Multi-Tenancy: https://auth0.com/docs/get-started/architecture-scenarios/multiple-tenant-apps

---

*AcademIA · Apostila 46 · Arquitetura Multi-Tenant · 2026*