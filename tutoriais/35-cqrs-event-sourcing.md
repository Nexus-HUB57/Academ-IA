---
title: "Tutorial 35 · CQRS & Event Sourcing · Padrões Avançados"
subtitle: "Como implementar CQRS e Event Sourcing para sistemas complexos com audit log"
author: "Equipo Nexus · Ravi (CTO/AI)"
version: "1.0.0"
date: 2026-08-06
pattern: "MMN_IA"
---

**Tutorial 35 · CQRS & Event Sourcing · Padrões Avançados**

*Tutorial de 1h30 implementando CQRS e Event Sourcing com Python. Cobre conceitos, implementação prática, projections, sagas, e quando usar.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 O que Você Vai Conquistar

Em 1h30, você vai:

1. Entender 4 padrões avançados (CQRS, Event Sourcing, Saga, Outbox)
2. Implementar Event Store do zero
3. Implementar projeção (read model)
4. Implementar CQRS básico
5. Implementar Saga com Event Sourcing
6. Comparar tradeoffs com CRUD tradicional
7. Decidir quando usar

**Pré-requisitos:**
- Python avançado
- Async/await
- Conhecimento de banco de dados
- Tutorial 14 (event-driven) recomendado

---

## 🧠 Parte 1: Conceitos

### 1.1 — CRUD Tradicional (Baseline)

```
Client → API → DB (read + write no mesmo schema)
```

**Limitações:**
- Auditoria difícil (sem histórico de mudanças)
- Read model acoplado ao write model
- Escala limitada (read e write competem por lock)
- Event sourcing (replay) impossível

### 1.2 — Event Sourcing (ES)

**Conceito:** estado = sequência de eventos

**Exemplo: Conta bancária**

**CRUD tradicional:**
```
current_balance = 1000
UPDATE accounts SET balance = 800 WHERE id = 1
```

**Estado final:** balance = 800
**Histórico:** perdido

**Event Sourcing:**
```
event: AccountOpened, balance=0
event: MoneyDeposited, amount=1000
event: MoneyWithdrawn, amount=200

current_balance = sum(applied_events) = 800
```

**Estado final:** balance = 800
**Histórico:** completo

### 1.3 — CQRS (Command Query Responsibility Segregation)

**Conceito:** separar modelo de leitura (Query) do modelo de escrita (Command)

```
            Commands          Queries
             ↓                 ↑
Client → Command Bus → Write DB (events)
                          ↓
                       Event Bus
                          ↓
                       Read DB (projections)
                          ↓
Client ←───────────────────────
```

**Vantagens:**
- Read model otimizado (desnormalizado)
- Write model simples (foco em invariantes)
- Escala independente
- Múltiplas read models (1 write, N reads)

### 1.4 — Quando Usar

✅ **Use Event Sourcing quando:**
- Auditoria é crítica (finanças, saúde, legal)
- Precisa de replay (debug, BI, ML training)
- Time travel (estado em qualquer ponto no passado)
- Múltiplas projeções (1 write → N reads)

✅ **Use CQRS quando:**
- Read e write têm requisitos muito diferentes
- Read model precisa ser desnormalizado
- Escala diferente para read vs write
- Reporting pesado

❌ **Não use quando:**
- CRUD simples (overhead não compensa)
- Auditoria não importa
- Time/pequeno (complexidade operacional)
- Sem certeza de ROI

---

## 🔨 Parte 2: Event Store

### 2.1 — Schema do Event Store

```sql
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    aggregate_id UUID NOT NULL,
    aggregate_type VARCHAR(100) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    event_metadata JSONB DEFAULT '{}',
    version INT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    
    UNIQUE(aggregate_id, version)
);

CREATE INDEX idx_events_aggregate ON events(aggregate_id, version);
CREATE INDEX idx_events_type ON events(event_type);
CREATE INDEX idx_events_created ON events(created_at);
```

**Conceitos:**
- `aggregate_id`: ID da entidade (account_id, order_id)
- `version`: sequência (1, 2, 3...) para evitar concorrência
- `event_type`: AccountOpened, MoneyDeposited
- `event_data`: payload em JSON
- `event_metadata`: contexto (user_id, correlation_id)

### 2.2 — Event Store em Python

```python
"""
Event Store com PostgreSQL.
"""
import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
import asyncpg


@dataclass
class Event:
    aggregate_id: str
    aggregate_type: str
    event_type: str
    event_data: dict
    version: int
    event_metadata: dict = None
    event_id: str = None
    created_at: datetime = None

    def to_dict(self) -> dict:
        return {
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "event_type": self.event_type,
            "event_data": self.event_data,
            "event_metadata": self.event_metadata or {},
            "version": self.version,
            "event_id": self.event_id or str(uuid.uuid4()),
            "created_at": self.created_at or datetime.now(),
        }


class EventStore(ABC):
    @abstractmethod
    async def append(self, event: Event) -> None: ...

    @abstractmethod
    async def get_events(self, aggregate_id: str, from_version: int = 0) -> List[Event]: ...

    @abstractmethod
    async def get_all_events(self, from_id: int = 0, limit: int = 100) -> List[Event]: ...


class PostgresEventStore(EventStore):
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.pool = None

    async def start(self):
        self.pool = await asyncpg.create_pool(self.db_url, min_size=5, max_size=20)

    async def stop(self):
        if self.pool:
            await self.pool.close()

    async def append(self, event: Event) -> None:
        """Adiciona evento com optimistic concurrency"""
        async with self.pool.acquire() as conn:
            try:
                await conn.execute(
                    """
                    INSERT INTO events (
                        aggregate_id, aggregate_type, event_type,
                        event_data, event_metadata, version
                    ) VALUES ($1, $2, $3, $4, $5, $6)
                    """,
                    event.aggregate_id,
                    event.aggregate_type,
                    event.event_type,
                    json.dumps(event.event_data),
                    json.dumps(event.event_metadata or {}),
                    event.version,
                )
            except asyncpg.UniqueViolationError:
                raise ConcurrencyError(
                    f"Concurrency error: aggregate {event.aggregate_id} "
                    f"version {event.version} already exists"
                )

    async def get_events(self, aggregate_id: str, from_version: int = 0) -> List[Event]:
        """Retorna eventos de um aggregate"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM events
                WHERE aggregate_id = $1 AND version >= $2
                ORDER BY version ASC
                """,
                aggregate_id,
                from_version,
            )
        return [self._row_to_event(row) for row in rows]

    async def get_all_events(self, from_id: int = 0, limit: int = 100) -> List[Event]:
        """Retorna todos os eventos (para projeções)"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM events
                WHERE id > $1
                ORDER BY id ASC
                LIMIT $2
                """,
                from_id,
                limit,
            )
        return [self._row_to_event(row) for row in rows]

    def _row_to_event(self, row) -> Event:
        return Event(
            event_id=str(row["id"]),
            aggregate_id=row["aggregate_id"],
            aggregate_type=row["aggregate_type"],
            event_type=row["event_type"],
            event_data=json.loads(row["event_data"]),
            event_metadata=json.loads(row["event_metadata"]),
            version=row["version"],
            created_at=row["created_at"],
        )


class ConcurrencyError(Exception):
    pass
```

### 2.3 — Aggregate (Domain Model)

```python
"""
Aggregate: reconstrói estado a partir de eventos.
"""
from typing import List
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class Aggregate(ABC):
    def __init__(self, aggregate_id: str):
        self.aggregate_id = aggregate_id
        self.version = 0
        self._changes: List[Event] = []

    @abstractmethod
    def apply(self, event: Event) -> None: ...

    def load_from_history(self, events: List[Event]):
        """Reconstrói estado aplicando eventos"""
        for event in events:
            self.apply(event)
            self.version = event.version

    def emit(self, event_type: str, data: dict, metadata: dict = None):
        """Emite novo evento"""
        event = Event(
            aggregate_id=self.aggregate_id,
            aggregate_type=self.__class__.__name__,
            event_type=event_type,
            event_data=data,
            version=self.version + 1,
            event_metadata=metadata or {},
        )
        self.apply(event)
        self._changes.append(event)
        self.version += 1

    def get_uncommitted_changes(self) -> List[Event]:
        return self._changes.copy()

    def mark_changes_committed(self):
        self._changes.clear()


# Exemplo: BankAccount aggregate
@dataclass
class BankAccount(Aggregate):
    balance: float = 0
    is_open: bool = False
    owner: str = ""

    def open_account(self, owner: str, initial_deposit: float = 0):
        if self.is_open:
            raise ValueError("Account already open")
        if initial_deposit < 0:
            raise ValueError("Initial deposit must be >= 0")

        self.emit("AccountOpened", {
            "owner": owner,
            "initial_deposit": initial_deposit,
        })

    def deposit(self, amount: float):
        if not self.is_open:
            raise ValueError("Account not open")
        if amount <= 0:
            raise ValueError("Deposit must be > 0")

        self.emit("MoneyDeposited", {"amount": amount})

    def withdraw(self, amount: float):
        if not self.is_open:
            raise ValueError("Account not open")
        if amount <= 0:
            raise ValueError("Withdrawal must be > 0")
        if amount > self.balance:
            raise ValueError("Insufficient funds")

        self.emit("MoneyWithdrawn", {"amount": amount})

    # Apply: usado para reconstruir estado
    def apply(self, event: Event):
        if event.event_type == "AccountOpened":
            self.is_open = True
            self.owner = event.event_data["owner"]
            self.balance = event.event_data["initial_deposit"]
        elif event.event_type == "MoneyDeposited":
            self.balance += event.event_data["amount"]
        elif event.event_type == "MoneyWithdrawn":
            self.balance -= event.event_data["amount"]
        elif event.event_type == "AccountClosed":
            self.is_open = False
```

### 2.4 — Repository

```python
"""
Repository: gerencia aggregates e persiste eventos.
"""
class BankAccountRepository:
    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    async def get(self, account_id: str) -> BankAccount:
        """Carrega aggregate do event store"""
        account = BankAccount(account_id)
        events = await self.event_store.get_events(account_id)
        if not events:
            raise AggregateNotFoundError(f"Account {account_id} not found")
        account.load_from_history(events)
        return account

    async def save(self, account: BankAccount):
        """Persiste novos eventos"""
        changes = account.get_uncommitted_changes()
        for event in changes:
            await self.event_store.append(event)
        account.mark_changes_committed()

    async def create(self, account_id: str, owner: str, initial_deposit: float) -> BankAccount:
        """Cria novo aggregate"""
        account = BankAccount(account_id)
        account.open_account(owner, initial_deposit)
        await self.save(account)
        return account


class AggregateNotFoundError(Exception):
    pass
```

---

## 🔍 Parte 3: CQRS - Read Model (Projection)

### 3.1 — Conceito de Projeção

**Projeção = read model construído a partir de eventos**

```
Event Store → Projector → Read DB (otimizado para queries)
```

### 3.2 — Exemplo: Projeção de Saldo

```python
"""
Projeção: conta de saldo por cliente.
"""
import asyncpg


class AccountBalanceProjection:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.pool = None

    async def start(self):
        self.pool = await asyncpg.create_pool(self.db_url)

        # Criar tabela de read model
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS account_balances (
                    account_id UUID PRIMARY KEY,
                    owner TEXT NOT NULL,
                    balance NUMERIC(15, 2) NOT NULL,
                    last_event_id BIGINT NOT NULL,
                    updated_at TIMESTAMPTZ DEFAULT now()
                );

                CREATE INDEX IF NOT EXISTS idx_balances_owner
                    ON account_balances(owner);
            """)

    async def apply_event(self, event: Event):
        """Aplica evento ao read model"""
        async with self.pool.acquire() as conn:
            if event.event_type == "AccountOpened":
                await conn.execute(
                    """
                    INSERT INTO account_balances (account_id, owner, balance, last_event_id)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (account_id) DO NOTHING
                    """,
                    event.aggregate_id,
                    event.event_data["owner"],
                    event.event_data["initial_deposit"],
                    event.event_id,
                )
            elif event.event_type == "MoneyDeposited":
                await conn.execute(
                    """
                    UPDATE account_balances
                    SET balance = balance + $1, last_event_id = $2, updated_at = now()
                    WHERE account_id = $3
                    """,
                    event.event_data["amount"],
                    event.event_id,
                    event.aggregate_id,
                )
            elif event.event_type == "MoneyWithdrawn":
                await conn.execute(
                    """
                    UPDATE account_balances
                    SET balance = balance - $1, last_event_id = $2, updated_at = now()
                    WHERE account_id = $3
                    """,
                    event.event_data["amount"],
                    event.event_id,
                    event.aggregate_id,
                )

    async def get_balance(self, account_id: str) -> dict:
        """Query otimizada"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM account_balances WHERE account_id = $1",
                account_id,
            )
        if not row:
            return None
        return {
            "account_id": str(row["account_id"]),
            "owner": row["owner"],
            "balance": float(row["balance"]),
            "updated_at": row["updated_at"],
        }
```

### 3.3 — Projector (Aplica Eventos)

```python
"""
Projector: consome eventos do event store e atualiza projeções.
"""
class Projector:
    def __init__(self, event_store: EventStore, projections: list):
        self.event_store = event_store
        self.projections = projections
        self.last_processed_id = 0
        self.running = False

    async def start(self):
        """Loop: pega eventos novos e aplica"""
        self.running = True
        while self.running:
            events = await self.event_store.get_all_events(
                from_id=self.last_processed_id,
                limit=100,
            )
            for event in events:
                # Aplica a TODAS as projeções
                for projection in self.projections:
                    try:
                        await projection.apply_event(event)
                    except Exception as e:
                        logger.error(f"Projection {projection.__class__.__name__} failed: {e}")
                self.last_processed_id = int(event.event_id)

            if not events:
                await asyncio.sleep(1)  # poll interval

    async def stop(self):
        self.running = False
```

---

## 🧮 Parte 4: CQRS com Commands e Queries

### 4.1 — Command Bus

```python
"""
Command: intenção de mudar estado.
Command Bus: roteia commands para handlers.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Command:
    pass


@dataclass
class OpenAccountCommand(Command):
    account_id: str
    owner: str
    initial_deposit: float


@dataclass
class DepositMoneyCommand(Command):
    account_id: str
    amount: float


@dataclass
class WithdrawMoneyCommand(Command):
    account_id: str
    amount: float


class CommandHandler(ABC):
    @abstractmethod
    async def handle(self, command: Command) -> None: ...


class OpenAccountHandler(CommandHandler):
    def __init__(self, repository: BankAccountRepository):
        self.repository = repository

    async def handle(self, command: OpenAccountCommand):
        account = await self.repository.create(
            account_id=command.account_id,
            owner=command.owner,
            initial_deposit=command.initial_deposit,
        )
        return {"account_id": account.aggregate_id, "balance": account.balance}


class DepositMoneyHandler(CommandHandler):
    def __init__(self, repository: BankAccountRepository):
        self.repository = repository

    async def handle(self, command: DepositMoneyCommand):
        account = await self.repository.get(command.account_id)
        account.deposit(command.amount)
        await self.repository.save(account)
        return {"balance": account.balance}


class WithdrawMoneyHandler(CommandHandler):
    def __init__(self, repository: BankAccountRepository):
        self.repository = repository

    async def handle(self, command: WithdrawMoneyCommand):
        account = await self.repository.get(command.account_id)
        account.withdraw(command.amount)
        await self.repository.save(account)
        return {"balance": account.balance}


class CommandBus:
    def __init__(self):
        self.handlers = {}

    def register(self, command_type: type, handler: CommandHandler):
        self.handlers[command_type] = handler

    async def dispatch(self, command: Command):
        handler = self.handlers.get(type(command))
        if not handler:
            raise ValueError(f"No handler for {type(command).__name__}")
        return await handler.handle(command)
```

### 4.2 — Query Bus

```python
"""
Query: pergunta sobre estado (não muda).
"""
@dataclass
class Query:
    pass


@dataclass
class GetBalanceQuery(Query):
    account_id: str


@dataclass
class GetAllBalancesQuery(Query):
    owner: str


class QueryHandler(ABC):
    @abstractmethod
    async def handle(self, query: Query) -> dict: ...


class GetBalanceHandler(QueryHandler):
    def __init__(self, projection: AccountBalanceProjection):
        self.projection = projection

    async def handle(self, query: GetBalanceQuery):
        return await self.projection.get_balance(query.account_id)


class GetAllBalancesHandler(QueryHandler):
    def __init__(self, db_url: str):
        self.db_url = db_url

    async def handle(self, query: GetAllBalancesQuery):
        async with asyncpg.create_pool(self.db_url) as pool:
            async with pool.acquire() as conn:
                rows = await conn.fetch(
                    "SELECT * FROM account_balances WHERE owner = $1 ORDER BY balance DESC",
                    query.owner,
                )
        return [dict(row) for row in rows]


class QueryBus:
    def __init__(self):
        self.handlers = {}

    def register(self, query_type: type, handler: QueryHandler):
        self.handlers[query_type] = handler

    async def dispatch(self, query: Query):
        handler = self.handlers.get(type(query))
        if not handler:
            raise ValueError(f"No handler for {type(query).__name__}")
        return await handler.handle(query)
```

### 4.3 — API Endpoints

```python
"""
API com Command Bus (writes) e Query Bus (reads).
"""
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Setup
event_store = PostgresEventStore("postgresql://...")
projection = AccountBalanceProjection("postgresql://...")

repository = BankAccountRepository(event_store)

command_bus = CommandBus()
command_bus.register(OpenAccountCommand, OpenAccountHandler(repository))
command_bus.register(DepositMoneyCommand, DepositMoneyHandler(repository))
command_bus.register(WithdrawMoneyCommand, WithdrawMoneyHandler(repository))

query_bus = QueryBus()
query_bus.register(GetBalanceQuery, GetBalanceHandler(projection))
query_bus.register(GetAllBalancesQuery, GetAllBalancesHandler("postgresql://..."))


# Commands (writes)
@app.post("/accounts")
async def open_account(account_id: str, owner: str, initial_deposit: float = 0):
    command = OpenAccountCommand(
        account_id=account_id,
        owner=owner,
        initial_deposit=initial_deposit,
    )
    return await command_bus.dispatch(command)


@app.post("/accounts/{account_id}/deposit")
async def deposit(account_id: str, amount: float):
    command = DepositMoneyCommand(account_id=account_id, amount=amount)
    return await command_bus.dispatch(command)


@app.post("/accounts/{account_id}/withdraw")
async def withdraw(account_id: str, amount: float):
    command = WithdrawMoneyCommand(account_id=account_id, amount=amount)
    try:
        return await command_bus.dispatch(command)
    except ValueError as e:
        raise HTTPException(400, str(e))


# Queries (reads)
@app.get("/accounts/{account_id}/balance")
async def get_balance(account_id: str):
    query = GetBalanceQuery(account_id=account_id)
    result = await query_bus.dispatch(query)
    if not result:
        raise HTTPException(404, "Account not found")
    return result
```

---

## 🔄 Parte 5: Saga com Event Sourcing

### 5.1 — Saga de Pedido

**Processo:** OrderCreated → InventoryReserved → PaymentProcessed → OrderShipped

```python
"""
Saga: order fulfillment com compensação.
"""
class OrderFulfillmentSaga:
    def __init__(self, event_store: EventStore, projection: OrderSagaProjection):
        self.event_store = event_store
        self.projection = projection
        self.handlers = {
            "OrderCreated": self.handle_order_created,
            "InventoryReserved": self.handle_inventory_reserved,
            "InventoryReservationFailed": self.handle_inventory_failed,
            "PaymentProcessed": self.handle_payment_processed,
            "PaymentFailed": self.handle_payment_failed,
        }

    async def handle(self, event: Event):
        handler = self.handlers.get(event.event_type)
        if handler:
            await handler(event)

    async def handle_order_created(self, event: Event):
        """Quando pedido é criado, tenta reservar inventário"""
        order_id = event.aggregate_id
        items = event.event_data["items"]

        # Reservar inventário (idempotente)
        try:
            await self.projection.reserve_inventory(order_id, items)
        except InsufficientStockError as e:
            # Compensar: cancelar pedido
            await self.cancel_order(order_id, str(e))

    async def handle_inventory_reserved(self, event: Event):
        """Inventário reservado, processar pagamento"""
        order_id = event.aggregate_id
        amount = event.event_data["total"]

        # Processar pagamento
        try:
            await self.projection.process_payment(order_id, amount)
        except PaymentFailedError as e:
            # Compensar: liberar inventário
            await self.projection.release_inventory(order_id)

    async def handle_payment_processed(self, event: Event):
        """Pagamento processado, agendar envio"""
        order_id = event.aggregate_id
        await self.projection.schedule_shipment(order_id)

    async def handle_inventory_failed(self, event: Event):
        """Falha no inventário, cancelar pedido"""
        order_id = event.aggregate_id
        await self.cancel_order(order_id, "Out of stock")

    async def handle_payment_failed(self, event: Event):
        """Falha no pagamento, liberar inventário"""
        order_id = event.aggregate_id
        await self.projection.release_inventory(order_id)

    async def cancel_order(self, order_id: str, reason: str):
        # Emite OrderCancelled
        order = Order(order_id)
        order.cancel(reason)
        await self.event_store.append(order.get_uncommitted_changes()[0])
```

---

## 🚀 Parte 6: Outbox Pattern

### 6.1 — O Problema

**Como garantir que evento é publicado de forma confiável?**

**Sem outbox:**
```python
# 1. Save to DB
db.save(order)

# 2. Publish to Kafka (pode falhar!)
kafka.publish(event)
# Se Kafka cai, evento é perdido
```

**Com outbox:**
```python
# 1. Save order + outbox event (mesma transação!)
db.save(order)
db.save(outbox_event)  # mesma transação

# 2. Background job lê outbox e publica
# Se Kafka cai, retenta depois
```

### 6.2 — Implementação

```python
"""
Outbox pattern.
"""
class OutboxProcessor:
    def __init__(self, db_url: str, kafka_producer):
        self.db_url = db_url
        self.kafka = kafka_producer

    async def start(self):
        """Loop: lê outbox e publica"""
        while True:
            async with asyncpg.create_pool(self.db_url) as pool:
                async with pool.acquire() as conn:
                    # Atomic: SELECT FOR UPDATE + UPDATE
                    async with conn.transaction():
                        events = await conn.fetch("""
                            SELECT * FROM outbox
                            WHERE published_at IS NULL
                            ORDER BY created_at ASC
                            LIMIT 100
                            FOR UPDATE SKIP LOCKED
                        """)

                        for event in events:
                            try:
                                await self.kafka.send(
                                    topic=event["topic"],
                                    key=event["aggregate_id"],
                                    value=json.loads(event["event_data"]),
                                )
                                await conn.execute(
                                    "UPDATE outbox SET published_at = now() WHERE id = $1",
                                    event["id"],
                                )
                            except Exception as e:
                                logger.error(f"Publish failed: {e}")
                                # Will retry next loop

            await asyncio.sleep(1)  # poll interval
```

**Schema do outbox:**
```sql
CREATE TABLE outbox (
    id BIGSERIAL PRIMARY KEY,
    topic VARCHAR(100) NOT NULL,
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    published_at TIMESTAMPTZ,
    
    INDEX idx_outbox_unpublished (published_at, created_at) WHERE published_at IS NULL
);
```

---

## 📊 Parte 7: Comparação de Padrões

| Aspecto | CRUD | Event Sourcing | CQRS | Event Sourcing + CQRS |
|---------|------|----------------|------|------------------------|
| **Auditoria** | ❌ | ✅ Perfeita | ❌ | ✅ Perfeita |
| **Replay** | ❌ | ✅ | ❌ | ✅ |
| **Read perf** | ⚠️ Média | ❌ (precisa reprojetar) | ✅ Otimizada | ✅ Otimizada |
| **Write perf** | ⚠️ Média | ✅ Append-only | ✅ | ✅ Append-only |
| **Complexidade** | ✅ Baixa | ⚠️ Média | ⚠️ Média | ❌ Alta |
| **Time-to-market** | ✅ Rápido | ⚠️ Mais lento | ⚠️ Mais lento | ❌ Muito lento |
| **Debug** | ⚠️ Difícil | ✅ Replay | ⚠️ | ✅ Replay + read models |
| **Escala** | ⚠️ Limitada | ✅ Excelente | ✅ Excelente | ✅ Excelente |

---

## 🏆 Quando Usar Cada Combinação

### CRUD Simples
- 1-3 devs
- CRUD puro
- Sem auditoria crítica
- **Use:** CRUD

### CRUD + Audit Log
- Precisa de histórico
- Read model = write model
- **Use:** CRUD com trigger de audit

### Event Sourcing
- Auditoria crítica (finanças, saúde)
- Time travel necessário
- Domain rico
- **Use:** Event Sourcing

### CQRS
- Read e write muito diferentes
- Read precisa de denormalização
- Escala diferente
- **Use:** CQRS

### Event Sourcing + CQRS
- Tudo acima junto
- Sistema crítico (banco, hospital)
- Compliance rigoroso
- **Use:** ES + CQRS + Saga + Outbox

---

## ⚠️ Tradeoffs

### Prós
- Auditoria perfeita
- Time travel
- Read model otimizado
- Event-driven por natureza
- Múltiplas projeções

### Contras
- Complexidade operacional alta
- Eventual consistency (read model fica atrasado)
- Curva de aprendizado
- Dificuldade de "delete" (LGPD)
- Performance de rebuild (replay N eventos)
- Teste mais complexo

---

## 📚 Materiais Complementares

- `tutoriais/31-circuit-breaker-padrao.md` — circuit breaker
- `treinamentos/WS-14-oficina-arquitetura-event-driven.md` — event-driven
- `apostilas/46-arquitetura-multi-tenant-2026.md` — multi-tenant
- `apostilas/45-debugging-otimizacao-agentes-ia.md` — debug
- `Lib-Nexus/best-practices/05-sre-observability.md` — SRE
- `governanca/PB-GOVERN-postmortem-blame-free.md` — post-mortem

---

## 🔗 Links Externos

- Martin Fowler - Event Sourcing: https://martinfowler.com/eaaDev/EventSourcing.html
- Greg Young - CQRS: https://www.cqrs.nu/
- Microsoft - CQRS Pattern: https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs
- EventStore: https://www.eventstore.com/
- Axon Framework (Java): https://www.axoniq.io/

---

*AcademIA · Tutorial 35 · CQRS & Event Sourcing · 2026*