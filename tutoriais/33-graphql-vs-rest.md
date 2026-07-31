---
title: "Tutorial 33 · GraphQL vs REST · Comparação Definitiva"
subtitle: "Como escolher entre GraphQL e REST para APIs de agentes IA"
author: "Equipo Nexus · Ravi (CTO/AI)"
version: "1.0.0"
date: 2026-07-31
pattern: "MMN_IA"
---

**Tutorial 33 · GraphQL vs REST · Comparação Definitiva**

*Tutorial de 1h comparando GraphQL e REST na prática, com implementação completa em FastAPI, análise de tradeoffs, e decisão de quando usar cada um.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 O que Você Vai Conquistar

Em 1h, você vai:

1. Entender 5 abordagens de API (REST, GraphQL, gRPC, tRPC, WebSocket)
2. Implementar uma API REST completa
3. Implementar uma API GraphQL completa
4. Comparar performance, DX, e manutenibilidade
5. Decidir qual usar para seu caso
6. Migrar REST para GraphQL (ou vice-versa)

**Pré-requisitos:**
- Python intermediário
- FastAPI básico
- Conceito de HTTP/JSON

---

## 🧠 Parte 1: Conceito

### 1.1 — O que é REST

**REST (Representational State Transfer):**
- Cada recurso tem 1 endpoint
- Verbos HTTP: GET, POST, PUT, PATCH, DELETE
- Stateless (cada request é independente)
- Retorna JSON (tipicamente)

**Exemplo:**

```http
GET    /api/users/123          → User 123
GET    /api/users/123/posts    → Posts do User 123
GET    /api/users/123/followers → Followers do User 123
POST   /api/users              → Criar user
PUT    /api/users/123          → Atualizar user
DELETE /api/users/123          → Deletar user
```

### 1.2 — O que é GraphQL

**GraphQL:**
- 1 endpoint único
- Cliente define o que quer (query)
- Schema type-safe
- Sem over-fetching nem under-fetching

**Exemplo:**

```graphql
query {
  user(id: 123) {
    name
    email
    posts {
      title
      createdAt
    }
    followers {
      name
    }
  }
}
```

### 1.3 — Diferença Fundamental

| Aspecto | REST | GraphQL |
|---------|------|---------|
| **Endpoints** | Múltiplos | 1 (/graphql) |
| **Cliente define** | Não (servidor decide) | Sim (cliente decide) |
| **Over-fetching** | Sim (campos extras) | Não |
| **Under-fetching** | Sim (múltiplos requests) | Não |
| **Versioning** | /v1/, /v2/ | Evolução natural |
| **Caching** | HTTP nativo (GET) | Custom |
| **Type safety** | Opcional (OpenAPI) | Nativo |
| **Learning curve** | Baixa | Média |
| **DX frontend** | Às vezes frustrante | Excelente |
| **DX backend** | Simples | Mais complexo |

### 1.4 — Casos de Uso Ideais

**REST:**
- API pública (simples, bem documentada)
- CRUD simples
- Caching é importante
- Múltiplos clientes heterogêneos

**GraphQL:**
- Múltiplos clientes com dados diferentes (mobile vs web)
- Relacionamentos complexos (social graph)
- Frontend evolui rápido
- Reduzir requests em mobile (3G/4G)

---

## 🔨 Parte 2: REST na Prática (FastAPI)

### 2.1 — Implementação Completa

```python
"""
API REST com FastAPI.
"""
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Nexus REST API", version="1.0.0")


# ========================
# Models
# ========================
class User(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime


class Post(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime


class Comment(BaseModel):
    id: int
    text: str
    post_id: int
    author_id: int
    created_at: datetime


# Mock database
users_db = {
    1: User(id=1, name="Ana", email="ana@nexus.com", created_at=datetime.now()),
    2: User(id=2, name="Bruno", email="bruno@nexus.com", created_at=datetime.now()),
}

posts_db = {
    1: Post(id=1, title="Post 1", content="...", author_id=1, created_at=datetime.now()),
    2: Post(id=2, title="Post 2", content="...", author_id=1, created_at=datetime.now()),
    3: Post(id=3, title="Post 3", content="...", author_id=2, created_at=datetime.now()),
}


# ========================
# Endpoints
# ========================
@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """GET single user"""
    if user_id not in users_db:
        raise HTTPException(404, "User not found")
    return users_db[user_id]


@app.get("/users", response_model=List[User])
async def list_users(skip: int = 0, limit: int = 10):
    """GET list of users"""
    return list(users_db.values())[skip:skip + limit]


@app.get("/users/{user_id}/posts", response_model=List[Post])
async def get_user_posts(user_id: int):
    """GET posts of user"""
    if user_id not in users_db:
        raise HTTPException(404, "User not found")
    return [p for p in posts_db.values() if p.author_id == user_id]


@app.get("/users/{user_id}/posts/{post_id}/comments")
async def get_post_comments(user_id: int, post_id: int):
    """N+1 problem: 3 levels deep"""
    if user_id not in users_db:
        raise HTTPException(404, "User not found")
    if post_id not in posts_db:
        raise HTTPException(404, "Post not found")
    # Comments logic...
    return []


# Mutations
class CreateUserRequest(BaseModel):
    name: str
    email: str


@app.post("/users", response_model=User, status_code=201)
async def create_user(user: CreateUserRequest):
    new_id = max(users_db.keys()) + 1
    new_user = User(
        id=new_id,
        name=user.name,
        email=user.email,
        created_at=datetime.now(),
    )
    users_db[new_id] = new_user
    return new_user
```

### 2.2 — Problema: Over/Under-fetching

**Cenário 1: Mobile precisa só de nome e avatar do user**

```http
GET /api/users/123

Response (REST):
{
  "id": 123,
  "name": "Ana",
  "email": "ana@nexus.com",
  "created_at": "2026-07-31",
  "updated_at": "2026-07-31",
  "preferences": { ... },
  "billing_info": { ... },
  "metadata": { ... }
}
```

**Mobile usa 5% do que veio. Over-fetching.**

**Cenário 2: Mostrar perfil com posts + comments + likes**

```http
GET /api/users/123
GET /api/users/123/posts
GET /api/posts/1/comments
GET /api/posts/1/likes
```

**4 requests. Latência somada. Under-fetching.**

**Solução GraphQL:** 1 request, só o que precisa.

---

## 🔨 Parte 3: GraphQL na Prática

### 3.1 — Implementação com Strawberry

```python
"""
API GraphQL com Strawberry + FastAPI.
"""
import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from datetime import datetime


# ========================
# Types
# ========================
@strawberry.type
class User:
    id: int
    name: str
    email: str
    created_at: datetime

    @strawberry.field
    async def posts(self) -> List["Post"]:
        """Resolver: posts deste user"""
        return [p for p in posts_db.values() if p.author_id == self.id]

    @strawberry.field
    async def followers(self) -> List["User"]:
        """Resolver: followers deste user"""
        # Mock: retorna todos os outros users
        return [u for u in users_db.values() if u.id != self.id]


@strawberry.type
class Post:
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime

    @strawberry.field
    async def author(self) -> User:
        """Resolver: autor do post"""
        return users_db[self.author_id]

    @strawberry.field
    async def comments(self) -> List["Comment"]:
        """Resolver: comments do post"""
        return [c for c in comments_db.values() if c.post_id == self.id]


@strawberry.type
class Comment:
    id: int
    text: str
    post_id: int
    author_id: int
    created_at: datetime

    @strawberry.field
    async def author(self) -> User:
        return users_db[self.author_id]


# ========================
# Query
# ========================
@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: int) -> Optional[User]:
        return users_db.get(id)

    @strawberry.field
    async def users(self) -> List[User]:
        return list(users_db.values())

    @strawberry.field
    async def post(self, id: int) -> Optional[Post]:
        return posts_db.get(id)


# ========================
# Mutation
# ========================
@strawberry.input
class CreateUserInput:
    name: str
    email: str


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, input: CreateUserInput) -> User:
        new_id = max(users_db.keys()) + 1
        new_user = User(
            id=new_id,
            name=input.name,
            email=input.email,
            created_at=datetime.now(),
        )
        users_db[new_id] = new_user
        return new_user


# ========================
# Schema
# ========================
schema = strawberry.Schema(query=Query, mutation=Mutation)


# ========================
# FastAPI integration
# ========================
from fastapi import FastAPI

app = FastAPI(title="Nexus GraphQL API", version="1.0.0")
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


# ========================
# Mock DB
# ========================
users_db = {
    1: User(id=1, name="Ana", email="ana@nexus.com", created_at=datetime.now()),
    2: User(id=2, name="Bruno", email="bruno@nexus.com", created_at=datetime.now()),
}
posts_db = {
    1: Post(id=1, title="Post 1", content="...", author_id=1, created_at=datetime.now()),
    2: Post(id=2, title="Post 2", content="...", author_id=1, created_at=datetime.now()),
    3: Post(id=3, title="Post 3", content="...", author_id=2, created_at=datetime.now()),
}
comments_db = {}
```

### 3.2 — Queries Poderosas

**Query 1: Apenas nome e avatar (mobile)**

```graphql
query {
  user(id: 1) {
    name
  }
}
```

**Response (1 campo):**
```json
{
  "data": {
    "user": {
      "name": "Ana"
    }
  }
}
```

**Query 2: Perfil completo (web)**

```graphql
query {
  user(id: 1) {
    name
    email
    created_at
    posts {
      title
      created_at
      comments {
        text
        author {
          name
        }
      }
    }
  }
}
```

**Response (tudo em 1 request):**
```json
{
  "data": {
    "user": {
      "name": "Ana",
      "email": "ana@nexus.com",
      "created_at": "2026-07-31T...",
      "posts": [
        {
          "title": "Post 1",
          "created_at": "2026-07-31T...",
          "comments": [
            {
              "text": "Ótimo post!",
              "author": { "name": "Bruno" }
            }
          ]
        }
      ]
    }
  }
}
```

### 3.3 — Mutation

```graphql
mutation {
  createUser(input: { name: "Carla", email: "carla@nexus.com" }) {
    id
    name
    email
  }
}
```

---

## 📊 Parte 4: Comparação Detalhada

### 4.1 — Performance

**Cenário: App mobile mostra feed**

| | REST | GraphQL |
|--|------|---------|
| **Requests** | 5 (user, posts, comments, likes, shares) | 1 |
| **Latência total** | 5 × 200ms = 1000ms | 200ms |
| **Dados transferidos** | 50KB (com over-fetch) | 15KB (só o que precisa) |
| **Battery (mobile)** | Alto | Baixo |

**Cenário: API pública simples (sem mobile)**

| | REST | GraphQL |
|--|------|---------|
| **Requests** | 1 | 1 |
| **Latência** | 100ms | 120ms (parse de query) |
| **Overhead** | Baixo | Médio |

### 4.2 — Developer Experience

**REST:**
```python
# Frontend dev precisa de 5 endpoints:
GET /users/123
GET /users/123/posts
GET /posts/1/comments
GET /posts/1/likes
GET /posts/1/shares
```

**GraphQL:**
```graphql
# 1 query, 1 endpoint, dados que quiser
query {
  user(id: 123) {
    posts {
      comments
      likes
      shares
    }
  }
}
```

**Vencedor:** GraphQL para DX frontend.

### 4.3 — Backend Complexity

**REST:**
- 5 endpoints, 5 funções
- Schema simples (Pydantic)
- OpenAPI auto-gerado
- **~50 linhas de código**

**GraphQL:**
- 1 schema, 1 endpoint
- Resolvers (N+1 problem)
- Precisa de dataloader
- **~150 linhas de código**

**Vencedor:** REST para backend simples.

### 4.4 — Caching

**REST:** HTTP caching nativo.
```http
Cache-Control: max-age=3600
ETag: "abc123"
```

**GraphQL:** Custom (Apollo, Relay, ou manual).
- POST sempre (não GET)
- Precisa de normalized cache
- **Mais complexo**

**Vencedor:** REST.

---

## 🎯 Parte 5: Quando Usar Cada Um

### 5.1 — Use REST se:

✅ API pública (consumida por terceiros)
✅ Operações CRUD simples
✅ Caching é crítico
✅ Equipe pequena (1-5 devs backend)
✅ Múltiplos clientes heterogêneos (iOS, Android, web, terceiros)
✅ Não quer complexidade de schema GraphQL

### 5.2 — Use GraphQL se:

✅ Múltiplos clientes com dados diferentes (mobile, web, TV)
✅ Relacionamentos complexos (social graph, dashboards)
✅ Reduzir bandwidth é crítico (mobile em 3G)
✅ Frontend evolui rápido
✅ Equipe tem senioridade para manter schema
✅ Múltiplas fontes de dados (microsserviços)

### 5.3 — Use Ambos (BFF Pattern)

**Backend For Frontend:**
- API interna: GraphQL (agregação de microsserviços)
- API pública: REST (simples para terceiros)

**Arquitetura:**

```
[ Web App ] ──> [ GraphQL BFF ] ──> [ Microservice A ]
[ Mobile  ] ──>                    ──> [ Microservice B ]
                                      ──> [ Database ]
[ Partners]──> [ REST API ] ────────>
```

---

## 🚀 Parte 6: Migração REST → GraphQL

### 6.1 — Estratégia Incremental

**Fase 1: Adicionar endpoint GraphQL (1 sprint)**
- Não substituir REST ainda
- GraphQL como read-only (queries)
- Clientes novos podem usar GraphQL, antigos continuam em REST

**Fase 2: Mutations em GraphQL (1 sprint)**
- Mover mutations para GraphQL
- Manter REST para queries legadas

**Fase 3: Deprecar REST (2 sprints)**
- Marcar REST como deprecated
- Comunicar para clientes
- Fornecer timeline

**Fase 4: Remover REST (quando 0 clientes)**
- Remover endpoints REST
- Manter só GraphQL

### 6.2 — Wrapper: REST como GraphQL

**Se você tem REST e quer GraphQL sem reescrever backend:**

```python
"""
GraphQL que resolve via REST (proxy).
"""
@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: int) -> Optional[User]:
        # Chama API REST existente
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.nexus.com/users/{id}")
            if response.status_code == 404:
                return None
            data = response.json()
            return User(
                id=data["id"],
                name=data["name"],
                email=data["email"],
            )
```

---

## 📋 Parte 7: Outras Alternativas

### 7.1 — gRPC

**O que é:** RPC (Remote Procedure Call) com Protobuf.

**Prós:**
- Performance extrema (binário)
- Type-safe (protobuf)
- Streaming nativo
- Multi-linguagem

**Contras:**
- Não human-readable (binário)
- Não é HTTP-friendly (firewalls)
- Complexo para web

**Quando usar:**
- Microsserviço interno
- Performance crítica
- Streaming

### 7.2 — tRPC

**O que é:** RPC type-safe para TypeScript.

**Prós:**
- Type safety end-to-end
- Zero codegen
- Excelente DX (TS)

**Contras:**
- TypeScript only
- Não é universal
- Novo (menos maduro)

**Quando usar:**
- Stack TypeScript full
- App interno

### 7.3 — WebSocket

**O que é:** conexão bidirecional persistente.

**Quando usar:**
- Real-time (chat, notificações)
- Streaming de dados
- Gaming

**Não substitui REST/GraphQL** — complementa.

---

## 🛠️ Parte 8: Boas Práticas GraphQL

### 1. Resolva N+1 com DataLoader

```python
"""
DataLoader para evitar N+1 em resolvers.
"""
from strawberry.dataloader import DataLoader


async def load_posts_by_author(author_ids: list[int]) -> list[list[Post]]:
    """Carrega posts de múltiplos autores em 1 query"""
    posts = await db.fetch_all(
        "SELECT * FROM posts WHERE author_id = ANY($1)",
        author_ids,
    )
    # Agrupar por author_id
    by_author = {author_id: [] for author_id in author_ids}
    for post in posts:
        by_author[post.author_id].append(post)
    return [by_author[aid] for aid in author_ids]


posts_loader = DataLoader(load_fn=load_posts_by_author)


@strawberry.type
class User:
    @strawberry.field
    async def posts(self) -> List[Post]:
        return await posts_loader.load(self.id)
```

### 2. Limite Profundidade

```python
# Prevenir queries muito profundas
from strawberry.extensions import MaxDepthLimiter

schema = strawberry.Schema(
    query=Query,
    extensions=[
        MaxDepthLimiter(max_depth=5),
    ],
)
```

### 3. Persisted Queries (APQ)

```python
"""
Em vez de enviar query inteira a cada request,
usa hash da query + variáveis.
"""
```

### 4. Monitoring

```python
"""
Log de queries lentas.
"""
import time
from strawberry.extensions import SchemaExtension


class QueryTimer(SchemaExtension):
    async def on_request_end(self):
        duration = time.time() - self.execution_context.start_time
        if duration > 1.0:  # > 1s
            logger.warning("slow_query", duration=duration)
```

---

## 📊 Decisão: REST vs GraphQL vs Ambos

| Caso | Recomendação |
|------|--------------|
| API pública de SaaS B2B | **REST** (simples, caching, docs) |
| App mobile + web com dados diferentes | **GraphQL** |
| Dashboard B2B com dados complexos | **GraphQL** |
| Microsserviço interno | **gRPC** |
| Real-time (chat, notificações) | **WebSocket** (complementa) |
| API pública + app próprio | **REST + GraphQL** (BFF) |
| Startup, 1-3 devs | **REST** (comece simples) |

---

## 📚 Materiais Complementares

- `Lib-Nexus/api-docs/03-graphql-schema.md` — schema GraphQL
- `Lib-Nexus/api-docs/04-sdk-python-typescript.md` — SDK
- `Lib-Nexus/api-docs/00-trpc-overview.md` — tRPC
- `Lib-Nexus/api-docs/01-webhooks.md` — webhooks
- `tutoriais/31-circuit-breaker-padrao.md` — resiliência
- `apostilas/46-arquitetura-multi-tenant-2026.md` — multi-tenant

---

## 🔗 Links Externos

- GraphQL Spec: https://spec.graphql.org/
- Strawberry: https://strawberry.rocks/
- GraphQL vs REST: https://www.apollographql.com/blog/graphql/basics/graphql-vs-rest/
- gRPC: https://grpc.io/
- tRPC: https://trpc.io/
- Postman State of API: https://www.postman.com/state-of-api/

---

*AcademIA · Tutorial 33 · GraphQL vs REST · 2026*