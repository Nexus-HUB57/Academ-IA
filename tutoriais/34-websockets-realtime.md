---
title: "Tutorial 34 · WebSockets Real-Time · Implementação Completa"
subtitle: "Como implementar WebSockets escaláveis para chat, notificações e dashboards"
author: "Equipo Nexus · Ravi (CTO/AI)"
version: "1.0.0"
date: 2026-08-04
pattern: "MMN_IA"
---

**Tutorial 34 · WebSockets Real-Time · Implementação Completa**

*Tutorial de 1h implementando WebSockets escaláveis com FastAPI. Cobre autenticação, rooms, scaling horizontal, presence, e patterns avançados.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 O que Você Vai Conquistar

Em 1h, você vai:

1. Entender WebSocket vs HTTP
2. Implementar chat em tempo real
3. Autenticar conexões
4. Implementar rooms (grupos)
5. Lidar com scaling (Redis Pub/Sub)
6. Implementar presence (online/offline)
7. Reconexão automática
8. Testar com stress test

**Pré-requisitos:**
- Python intermediário
- Async/await
- FastAPI básico

---

## 🧠 Parte 1: Conceito

### 1.1 — HTTP vs WebSocket

**HTTP:**
- Request → Response
- Cliente inicia
- Stateless
- Overhead a cada request

**WebSocket:**
- Conexão persistente
- Bidirecional (qualquer lado envia)
- Stateful
- Overhead mínimo após handshake

### 1.2 — Quando Usar WebSocket

✅ **Use para:**
- Chat
- Notificações real-time
- Dashboards ao vivo
- Gaming
- Editores colaborativos
- Streaming de dados

❌ **Não use para:**
- Request/response simples (REST é melhor)
- Operações que não precisam tempo real
- Quando polling é aceitável

### 1.3 — Lifecycle

```
Client                                Server
  |                                      |
  |------ HTTP Upgrade Request --------->|  (handshake)
  |<----- 101 Switching Protocols -------|  (aceito)
  |                                      |
  |------ WebSocket frame -------------->|  (mensagem)
  |<----- WebSocket frame ---------------|  (mensagem)
  |<----- WebSocket frame ---------------|  (mensagem)
  |------ WebSocket frame -------------->|  (mensagem)
  |                                      |
  |------ Close frame ------------------>|  (encerra)
  |<----- Close frame -------------------|  (confirma)
```

---

## 🔨 Parte 2: Implementação Básica

### 2.1 — FastAPI WebSocket

```python
"""
WebSocket básico com FastAPI.
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Recebe mensagem
            data = await websocket.receive_text()
            # Echo back
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
```

### 2.2 — Conexão Manager

```python
"""
Gerencia múltiplas conexões WebSocket.
"""
from fastapi import WebSocket
from typing import Dict, Set
import asyncio
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        # connections: client_id -> WebSocket
        self.connections: Dict[str, WebSocket] = {}
        # rooms: room_id -> set de client_ids
        self.rooms: Dict[str, Set[str]] = {}
        self.lock = asyncio.Lock()

    async def connect(self, client_id: str, websocket: WebSocket):
        """Aceita e registra conexão"""
        await websocket.accept()
        async with self.lock:
            self.connections[client_id] = websocket
        logger.info(f"Client connected: {client_id}")

    async def disconnect(self, client_id: str):
        """Remove conexão e sai de todas as rooms"""
        async with self.lock:
            if client_id in self.connections:
                del self.connections[client_id]
            # Sair de todas as rooms
            for room_clients in self.rooms.values():
                room_clients.discard(client_id)
        logger.info(f"Client disconnected: {client_id}")

    async def send_personal(self, client_id: str, message: dict):
        """Envia para um cliente"""
        if client_id in self.connections:
            try:
                await self.connections[client_id].send_json(message)
            except Exception as e:
                logger.error(f"Send to {client_id} failed: {e}")
                await self.disconnect(client_id)

    async def broadcast(self, message: dict, exclude: Set[str] = None):
        """Envia para todos os clientes conectados"""
        exclude = exclude or set()
        disconnected = []

        for client_id, ws in list(self.connections.items()):
            if client_id in exclude:
                continue
            try:
                await ws.send_json(message)
            except Exception:
                disconnected.append(client_id)

        # Cleanup
        for client_id in disconnected:
            await self.disconnect(client_id)

    async def join_room(self, client_id: str, room_id: str):
        """Adiciona cliente a uma room"""
        async with self.lock:
            if room_id not in self.rooms:
                self.rooms[room_id] = set()
            self.rooms[room_id].add(client_id)
        logger.info(f"Client {client_id} joined room {room_id}")

    async def leave_room(self, client_id: str, room_id: str):
        """Remove cliente de uma room"""
        async with self.lock:
            if room_id in self.rooms:
                self.rooms[room_id].discard(client_id)
                if not self.rooms[room_id]:
                    del self.rooms[room_id]
        logger.info(f"Client {client_id} left room {room_id}")

    async def broadcast_room(self, room_id: str, message: dict,
                            exclude: Set[str] = None):
        """Envia para todos os clientes em uma room"""
        exclude = exclude or set()
        if room_id not in self.rooms:
            return

        disconnected = []
        for client_id in list(self.rooms[room_id]):
            if client_id in exclude:
                continue
            if client_id in self.connections:
                try:
                    await self.connections[client_id].send_json(message)
                except Exception:
                    disconnected.append(client_id)

        for client_id in disconnected:
            await self.disconnect(client_id)

    def get_room_members(self, room_id: str) -> Set[str]:
        """Retorna membros de uma room"""
        return self.rooms.get(room_id, set()).copy()

    def get_online_count(self) -> int:
        """Retorna nº de clientes conectados"""
        return len(self.connections)


manager = ConnectionManager()
```

### 2.3 — Chat Endpoint

```python
"""
Endpoint de chat com WebSocket.
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
import json

app = FastAPI()


@app.websocket("/ws/chat/{room_id}")
async def chat_endpoint(
    websocket: WebSocket,
    room_id: str,
    token: str = Query(...),  # JWT
):
    # Autenticar
    user = await authenticate(token)
    if not user:
        await websocket.close(code=1008)  # Policy violation
        return

    user_id = user["id"]
    username = user["name"]

    # Conectar
    await manager.connect(user_id, websocket)
    await manager.join_room(user_id, room_id)

    # Notificar entrada
    await manager.broadcast_room(room_id, {
        "type": "user_joined",
        "user_id": user_id,
        "username": username,
        "room_id": room_id,
        "online_count": len(manager.get_room_members(room_id)),
    }, exclude={user_id})

    try:
        while True:
            # Recebe mensagem
            raw = await websocket.receive_text()
            message = json.loads(raw)

            # Processa baseado no tipo
            if message["type"] == "message":
                # Broadcast para room
                await manager.broadcast_room(room_id, {
                    "type": "message",
                    "user_id": user_id,
                    "username": username,
                    "text": message["text"],
                    "timestamp": message.get("timestamp"),
                })

            elif message["type"] == "typing":
                # Notifica "está digitando" (exceto o próprio)
                await manager.broadcast_room(room_id, {
                    "type": "typing",
                    "user_id": user_id,
                    "username": username,
                }, exclude={user_id})

            elif message["type"] == "private":
                # Mensagem privada
                target = message.get("to")
                if target:
                    await manager.send_personal(target, {
                        "type": "private",
                        "from": user_id,
                        "from_name": username,
                        "text": message["text"],
                    })

    except WebSocketDisconnect:
        pass
    finally:
        # Cleanup
        await manager.leave_room(user_id, room_id)
        await manager.broadcast_room(room_id, {
            "type": "user_left",
            "user_id": user_id,
            "username": username,
        })
        await manager.disconnect(user_id)


async def authenticate(token: str) -> dict:
    """Mock de autenticação JWT"""
    # Em produção: validar JWT, buscar user
    if token == "valid_token":
        return {"id": "user_1", "name": "Ana"}
    return None
```

---

## 🔐 Parte 3: Autenticação e Segurança

### 3.1 — JWT Authentication

```python
"""
Autenticação JWT em WebSocket.
"""
import jwt
from fastapi import WebSocket, status


async def authenticate_ws(websocket: WebSocket, token: str) -> dict:
    """Autentica via JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {
            "id": payload["sub"],
            "tenant_id": payload["tenant_id"],
            "permissions": payload["permissions"],
        }
    except jwt.ExpiredSignatureError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Token expired")
        return None
    except jwt.InvalidTokenError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token")
        return None
```

### 3.2 — Rate Limiting

```python
"""
Rate limit por conexão WebSocket.
"""
import time
from collections import defaultdict


class WSRateLimiter:
    def __init__(self, max_per_minute: int = 60):
        self.max_per_minute = max_per_minute
        self.messages: Dict[str, list] = defaultdict(list)

    def check(self, client_id: str) -> bool:
        """Retorna True se dentro do limite"""
        now = time.time()
        minute_ago = now - 60

        # Limpar mensagens antigas
        self.messages[client_id] = [
            t for t in self.messages[client_id] if t > minute_ago
        ]

        if len(self.messages[client_id]) >= self.max_per_minute:
            return False

        self.messages[client_id].append(now)
        return True


rate_limiter = WSRateLimiter(max_per_minute=60)


@app.websocket("/ws/chat/{room_id}")
async def chat_endpoint(websocket: WebSocket, room_id: str, token: str = Query(...)):
    user = await authenticate_ws(websocket, token)
    if not user:
        return

    user_id = user["id"]
    await manager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            # Rate limit check
            if not rate_limiter.check(user_id):
                await websocket.send_json({
                    "type": "error",
                    "message": "Rate limit exceeded",
                })
                continue

            # Process message...
    except WebSocketDisconnect:
        pass
    finally:
        await manager.disconnect(user_id)
```

### 3.3 — Origin Validation

```python
"""
Validação de origin para prevenir CSWSH.
"""
from fastapi import WebSocket, status

ALLOWED_ORIGINS = {
    "https://app.nexus.com",
    "https://nexus.com",
    "http://localhost:3000",  # dev
}


async def validate_origin(websocket: WebSocket) -> bool:
    """Valida Origin header"""
    origin = websocket.headers.get("origin")
    if origin not in ALLOWED_ORIGINS:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Origin not allowed",
        )
        return False
    return True


@app.websocket("/ws/chat/{room_id}")
async def chat_endpoint(websocket: WebSocket, room_id: str):
    if not await validate_origin(websocket):
        return
    # ... resto do handler
```

---

## 📡 Parte 4: Scaling Horizontal com Redis

### 4.1 — O Problema

**Single-server:** funciona até N=10k conexões
**Multi-server:** cliente A conecta no server 1, cliente B no server 2. Como se comunicam?

**Solução:** Redis Pub/Sub como message bus entre servers.

### 4.2 — Implementação com Redis

```python
"""
ConnectionManager com Redis Pub/Sub para scaling.
"""
import json
import asyncio
from typing import Dict, Set
import redis.asyncio as aioredis
import logging

logger = logging.getLogger(__name__)


class DistributedConnectionManager:
    def __init__(self, redis_url: str, server_id: str):
        self.connections: Dict[str, WebSocket] = {}
        self.rooms: Dict[str, Set[str]] = {}
        self.server_id = server_id
        self.redis = aioredis.from_url(redis_url)
        self.lock = asyncio.Lock()

    async def start(self):
        """Inicia subscriber do Redis"""
        self.pubsub = self.redis.pubsub()
        await self.pubsub.subscribe("ws:broadcast", "ws:room", "ws:personal")
        asyncio.create_task(self._listen_redis())

    async def _listen_redis(self):
        """Escuta mensagens do Redis e roteia para conexões locais"""
        async for message in self.pubsub.listen():
            if message["type"] != "message":
                continue

            channel = message["channel"].decode()
            data = json.loads(message["data"])

            if channel == "ws:broadcast":
                # Broadcast para todas as conexões LOCAIS
                exclude = set(data.get("exclude", []))
                await self._local_broadcast(data["message"], exclude)

            elif channel == "ws:room":
                # Broadcast para room LOCAL
                room_id = data["room_id"]
                exclude = set(data.get("exclude", []))
                await self._local_broadcast_room(
                    room_id, data["message"], exclude,
                )

            elif channel == "ws:personal":
                # Mensagem pessoal LOCAL
                target = data["target"]
                if target in self.connections:
                    await self._local_send(target, data["message"])

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        async with self.lock:
            self.connections[client_id] = websocket

    async def disconnect(self, client_id: str):
        async with self.lock:
            if client_id in self.connections:
                del self.connections[client_id]
            for room_clients in self.rooms.values():
                room_clients.discard(client_id)

    async def broadcast(self, message: dict, exclude: Set[str] = None):
        """Broadcast GLOBAL (via Redis)"""
        await self.redis.publish("ws:broadcast", json.dumps({
            "message": message,
            "exclude": list(exclude or []),
        }))

    async def broadcast_room(self, room_id: str, message: dict, exclude: Set[str] = None):
        """Broadcast para room (via Redis)"""
        await self.redis.publish("ws:room", json.dumps({
            "room_id": room_id,
            "message": message,
            "exclude": list(exclude or []),
        }))

    async def send_personal(self, target: str, message: dict):
        """Mensagem pessoal (via Redis)"""
        await self.redis.publish("ws:personal", json.dumps({
            "target": target,
            "message": message,
        }))

    async def _local_broadcast(self, message: dict, exclude: Set[str]):
        """Broadcast para conexões LOCAIS"""
        for client_id, ws in list(self.connections.items()):
            if client_id in exclude:
                continue
            try:
                await ws.send_json(message)
            except Exception:
                pass

    async def _local_broadcast_room(self, room_id: str, message: dict, exclude: Set[str]):
        """Broadcast room LOCAL"""
        if room_id not in self.rooms:
            return
        for client_id in list(self.rooms[room_id]):
            if client_id in exclude:
                continue
            if client_id in self.connections:
                try:
                    await self.connections[client_id].send_json(message)
                except Exception:
                    pass

    async def _local_send(self, target: str, message: dict):
        """Send pessoal LOCAL"""
        if target in self.connections:
            try:
                await self.connections[target].send_json(message)
            except Exception:
                pass
```

### 4.3 — Sticky Sessions (Load Balancer)

**Para o cliente sempre conectar no mesmo server:**

**Nginx:**
```nginx
upstream websocket_servers {
    ip_hash;  # sticky session by IP
    server server1:8000;
    server server2:8000;
    server server3:8000;
}

server {
    location /ws/ {
        proxy_pass http://websocket_servers;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;  # 24h
    }
}
```

**Ou:** usar Redis para coordenar (não precisa sticky).

---

## 🟢 Parte 5: Presence (Online/Offline)

### 5.1 — Implementação

```python
"""
Sistema de presence: online/offline/away.
"""
import time
from enum import Enum
from typing import Dict


class PresenceStatus(str, Enum):
    ONLINE = "online"
    AWAY = "away"
    BUSY = "busy"
    OFFLINE = "offline"


class PresenceTracker:
    def __init__(self, redis_url: str):
        self.redis = aioredis.from_url(redis_url)
        self.heartbeat_timeout = 60  # segundos

    async def set_online(self, user_id: str, status: PresenceStatus = PresenceStatus.ONLINE):
        """Marca user como online"""
        await self.redis.setex(
            f"presence:{user_id}",
            self.heartbeat_timeout,
            status.value,
        )
        # Publica mudança
        await self.redis.publish("presence:updates", json.dumps({
            "user_id": user_id,
            "status": status.value,
            "timestamp": time.time(),
        }))

    async def heartbeat(self, user_id: str):
        """Renova TTL (chamado a cada 30s pelo cliente)"""
        current = await self.redis.get(f"presence:{user_id}")
        if current:
            await self.redis.expire(f"presence:{user_id}", self.heartbeat_timeout)

    async def set_status(self, user_id: str, status: PresenceStatus):
        """Define status customizado (away, busy, etc)"""
        await self.set_online(user_id, status)

    async def get_status(self, user_id: str) -> PresenceStatus:
        """Retorna status atual"""
        status = await self.redis.get(f"presence:{user_id}")
        if status:
            return PresenceStatus(status.decode())
        return PresenceStatus.OFFLINE

    async def get_online_users(self, user_ids: list) -> Dict[str, PresenceStatus]:
        """Retorna status de múltiplos users"""
        statuses = {}
        for user_id in user_ids:
            statuses[user_id] = await self.get_status(user_id)
        return statuses


presence = PresenceTracker("redis://localhost:6379")


@app.websocket("/ws/chat/{room_id}")
async def chat_with_presence(websocket: WebSocket, room_id: str, token: str = Query(...)):
    user = await authenticate_ws(websocket, token)
    if not user:
        return

    user_id = user["id"]

    # Marca online
    await presence.set_online(user_id, PresenceStatus.ONLINE)

    # Heartbeat task
    async def heartbeat_task():
        while True:
            try:
                await asyncio.sleep(30)
                await presence.heartbeat(user_id)
            except asyncio.CancelledError:
                break

    hb_task = asyncio.create_task(heartbeat_task())

    await manager.connect(user_id, websocket)
    await manager.join_room(user_id, room_id)

    # Broadcast: user online
    await manager.broadcast_room(room_id, {
        "type": "presence",
        "user_id": user_id,
        "status": "online",
    })

    try:
        while True:
            data = await websocket.receive_json()

            if data["type"] == "set_status":
                new_status = PresenceStatus(data["status"])
                await presence.set_status(user_id, new_status)
                await manager.broadcast_room(room_id, {
                    "type": "presence",
                    "user_id": user_id,
                    "status": new_status.value,
                })

            # ... outros tipos
    except WebSocketDisconnect:
        pass
    finally:
        # Cleanup
        await presence.set_status(user_id, PresenceStatus.OFFLINE)
        await manager.broadcast_room(room_id, {
            "type": "presence",
            "user_id": user_id,
            "status": "offline",
        })
        await manager.disconnect(user_id)
        hb_task.cancel()
```

### 5.2 — Frontend (Heartbeat)

```javascript
// WebSocket client com heartbeat
class NexusWebSocket {
  constructor(url, token) {
    this.url = url;
    this.token = token;
    this.ws = null;
    this.heartbeatInterval = null;
    this.reconnectAttempts = 0;
  }

  connect() {
    this.ws = new WebSocket(`${this.url}?token=${this.token}`);

    this.ws.onopen = () => {
      console.log("Connected");
      this.reconnectAttempts = 0;
      this.startHeartbeat();
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleMessage(data);
    };

    this.ws.onclose = () => {
      console.log("Disconnected");
      this.stopHeartbeat();
      this.scheduleReconnect();
    };

    this.ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  }

  startHeartbeat() {
    this.heartbeatInterval = setInterval(() => {
      if (this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: "heartbeat" }));
      }
    }, 30000);  // 30s
  }

  stopHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  scheduleReconnect() {
    const delay = Math.min(30000, 1000 * Math.pow(2, this.reconnectAttempts));
    this.reconnectAttempts++;
    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
    setTimeout(() => this.connect(), delay);
  }

  send(data) {
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  handleMessage(data) {
    switch (data.type) {
      case "message":
        this.onMessage?.(data);
        break;
      case "presence":
        this.onPresence?.(data);
        break;
      case "user_joined":
        this.onUserJoined?.(data);
        break;
      // ... outros
    }
  }
}

// Uso
const ws = new NexusWebSocket("wss://api.nexus.com/ws/chat/room_123", token);
ws.onMessage = (data) => console.log(`${data.username}: ${data.text}`);
ws.onPresence = (data) => console.log(`${data.user_id} is now ${data.status}`);
ws.connect();
```

---

## 🧪 Parte 6: Testes

### 6.1 — Teste Unitário

```python
import pytest
from fastapi.testclient import TestClient


def test_websocket_connect():
    client = TestClient(app)
    with client.websocket_connect("/ws/chat/room_1?token=valid_token") as ws:
        ws.send_json({"type": "message", "text": "Hello"})
        data = ws.receive_json()
        assert data["type"] == "message"
        assert data["text"] == "Hello"


def test_websocket_invalid_token():
    client = TestClient(app)
    with pytest.raises(Exception):
        with client.websocket_connect("/ws/chat/room_1?token=invalid") as ws:
            ws.receive_text()
```

### 6.2 — Stress Test

```python
"""
Teste de carga: 1000 conexões simultâneas.
"""
import asyncio
import websockets
import time


async def client(ws_id: int, messages_to_send: int = 10):
    uri = "ws://localhost:8000/ws/chat/stress_test?token=valid_token"
    async with websockets.connect(uri) as ws:
        for i in range(messages_to_send):
            await ws.send(f'{{"type": "message", "text": "msg_{ws_id}_{i}"}}')
            await ws.recv()


async def stress_test(n_clients: int = 1000):
    start = time.time()
    tasks = [client(i) for i in range(n_clients)]
    await asyncio.gather(*tasks)
    duration = time.time() - start
    print(f"{n_clients} clients, {n_clients * 10} messages: {duration:.2f}s")
    print(f"Throughput: {n_clients * 10 / duration:.0f} msg/s")


if __name__ == "__main__":
    asyncio.run(stress_test(1000))
```

---

## 📊 Parte 7: Métricas e Monitoramento

### 7.1 — Métricas

```python
"""
Métricas Prometheus para WebSocket.
"""
from prometheus_client import Counter, Gauge, Histogram

ws_connections_total = Counter(
    "ws_connections_total",
    "Total de conexões WebSocket estabelecidas",
    labelnames=["endpoint"],
)

ws_connections_active = Gauge(
    "ws_connections_active",
    "Conexões ativas",
    labelnames=["endpoint"],
)

ws_messages_total = Counter(
    "ws_messages_total",
    "Total de mensagens",
    labelnames=["endpoint", "direction", "type"],
)

ws_message_duration = Histogram(
    "ws_message_duration_seconds",
    "Tempo de processamento de mensagem",
    labelnames=["endpoint"],
)

ws_errors_total = Counter(
    "ws_errors_total",
    "Erros em WebSocket",
    labelnames=["endpoint", "error_type"],
)
```

---

## 🏆 Boas Práticas

### 1. Use WSS (TLS)

```python
# Nunca WS em produção
ws = new WebSocket("ws://...");  # ❌

ws = new WebSocket("wss://...");  # ✅
```

### 2. Implemente Heartbeat

- Cliente → servidor: ping a cada 30s
- Servidor detecta conexão morta (sem ping há 60s) e fecha

### 3. Limite Tamanho de Mensagem

```python
MAX_MESSAGE_SIZE = 10_000  # 10KB

async def receive(self):
    data = await super().receive()
    if len(data) > MAX_MESSAGE_SIZE:
        await self.close(code=1009, reason="Message too big")
        return None
    return data
```

### 4. Idempotência

- Use message_id para deduplicar
- Cliente pode reenviar após reconexão

### 5. Backpressure

- Se cliente lento, descarte mensagens antigas
- Ou desconecte (cliente vai reconectar)

---

## 📚 Materiais Complementares

- `tutoriais/31-circuit-breaker-padrao.md` — circuit breaker
- `apostilas/45-debugging-otimizacao-agentes-ia.md` — debug
- `apostilas/46-arquitetura-multi-tenant-2026.md` — multi-tenant
- `treinamentos/WS-14-oficina-arquitetura-event-driven.md` — Kafka
- `Lib-Nexus/api-docs/01-webhooks.md` — webhooks

---

## 🔗 Links Externos

- MDN WebSocket: https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
- FastAPI WebSocket: https://fastapi.tiangolo.com/advanced/websockets/
- Socket.IO: https://socket.io/
- Ably Realtime: https://ably.com/
- Pusher: https://pusher.com/

---

*AcademIA · Tutorial 34 · WebSockets Real-Time · 2026*