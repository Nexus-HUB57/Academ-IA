---
title: "Tutorial 31 · Circuit Breaker Pattern · Implementação Completa"
subtitle: "Como implementar o padrão circuit breaker para resiliência de sistemas distribuídos"
author: "Equipo Nexus · Ravi (CTO/AI)"
version: "1.0.0"
date: 2026-07-30
pattern: "MMN_IA"
---

**Tutorial 31 · Circuit Breaker Pattern · Implementação Completa**

*Tutorial de 1h implementando circuit breaker do zero. Cobre os 3 estados (Closed, Open, Half-Open), métricas, fallback, e integração com FastAPI.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 O que Você Vai Conquistar

Em 1h, você vai:

1. Entender o padrão circuit breaker conceitualmente
2. Implementar do zero (sem libs externas)
3. Adicionar métricas (Prometheus)
4. Integrar com FastAPI
5. Testar com cenário de falha
6. Comparar com libs (pybreaker, circuitbreaker)

**Pré-requisitos:**
- Python intermediário
- Async/await
- Conceito básico de APIs externas

---

## 🧠 Parte 1: Conceito

### 1.1 — O Problema: Cascading Failure

**Cenário sem circuit breaker:**

```
User → API Nexus → OpenAI API
                → Database
                → Cache (Redis)
                → API externa
```

**Se OpenAI cai:**
1. Request 1: tenta OpenAI, **timeout 30s**, retorna erro
2. Request 2: mesma coisa, **mais 30s perdidos**
3. Request 3-N: todas bloqueiam esperando OpenAI
4. **Connection pool esgota** (todas em uso)
5. **Até requests para DB e Redis param** (sistema trava)
6. **Usuários veem 504 Gateway Timeout**

**Resultado:** 1 serviço externo down → **toda a plataforma down**.

### 1.2 — Solução: Circuit Breaker

**Analogia:** disjuntor elétrico.

- **Circuito fechado (CLOSED):** eletricidade passa (request normal)
- **Circuito aberto (OPEN):** eletricidade bloqueada (request falha rápido)
- **Half-open (HALF_OPEN):** testando se serviço voltou

**Comportamento:**

```
CLOSED (normal):
  Request → sucesso → continua CLOSED
  Request → falha → conta falhas
  Se falhas >= threshold → vai para OPEN

OPEN (degradado):
  Request → falha IMEDIATA (sem chamar dependência)
  Após timeout → vai para HALF_OPEN

HALF_OPEN (testando):
  Request → tenta 1 chamada
  Se sucesso → volta para CLOSED
  Se falha → volta para OPEN
```

### 1.3 — Benefícios

✅ **Falha rápida:** request não espera 30s, falha em < 1ms
✅ **Isolamento:** problema em 1 serviço não afeta outros
✅ **Auto-recuperação:** testa periodicamente se voltou
✅ **Backpressure:** sinaliza que sistema está sobrecarregado
✅ **Métricas:** permite alertar sobre degradação

---

## 🔨 Parte 2: Implementação do Zero

### 2.1 — Versão Básica (Síncrona)

```python
"""
Circuit Breaker básico.
Implementação didática (não-production).
"""
import time
from enum import Enum
from typing import Callable, Any
from dataclasses import dataclass, field


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5          # falhas para abrir
    success_threshold: int = 2          # sucessos para fechar (half-open)
    timeout: float = 60.0               # segundos aberto antes de testar
    expected_exceptions: tuple = (Exception,)


class CircuitBreaker:
    def __init__(self, name: str, config: CircuitBreakerConfig = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()

        # Estado
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.last_state_change = time.time()

        # Métricas
        self.total_calls = 0
        self.total_failures = 0
        self.total_successes = 0
        self.total_short_circuits = 0  # chamadas bloqueadas

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Executa função com proteção do circuit breaker"""
        self.total_calls += 1

        # Verificar estado
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._transition_to(CircuitState.HALF_OPEN)
            else:
                self.total_short_circuits += 1
                raise CircuitBreakerOpenError(
                    f"Circuit '{self.name}' is OPEN. "
                    f"Retry after {self.config.timeout}s"
                )

        # Tentar executar
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result

        except self.config.expected_exceptions as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.total_successes += 1

        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self._close()
        elif self.state == CircuitState.CLOSED:
            # Reset failure count
            self.failure_count = 0

    def _on_failure(self):
        self.total_failures += 1
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitState.HALF_OPEN:
            self._open()
        elif self.state == CircuitState.CLOSED:
            if self.failure_count >= self.config.failure_threshold:
                self._open()

    def _should_attempt_reset(self) -> bool:
        return (time.time() - self.last_failure_time) >= self.config.timeout

    def _open(self):
        self._transition_to(CircuitState.OPEN)
        self.success_count = 0

    def _close(self):
        self._transition_to(CircuitState.CLOSED)
        self.failure_count = 0
        self.success_count = 0

    def _transition_to(self, new_state: CircuitState):
        old_state = self.state
        self.state = new_state
        self.last_state_change = time.time()
        print(f"[{self.name}] {old_state.value} → {new_state.value}")

    def get_state(self) -> dict:
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "total_calls": self.total_calls,
            "total_failures": self.total_failures,
            "total_successes": self.total_successes,
            "total_short_circuits": self.total_short_circuits,
        }


class CircuitBreakerOpenError(Exception):
    pass


# =====================
# Teste
# =====================
if __name__ == "__main__":
    import random

    cb = CircuitBreaker("test", CircuitBreakerConfig(
        failure_threshold=3,
        timeout=5,
    ))

    def flaky_service():
        if random.random() < 0.7:
            raise Exception("Service unavailable")
        return "OK"

    # Simular 20 chamadas
    for i in range(20):
        try:
            result = cb.call(flaky_service)
            print(f"[{i}] Result: {result}")
        except CircuitBreakerOpenError as e:
            print(f"[{i}] BLOCKED: {e}")
        except Exception as e:
            print(f"[{i}] FAIL: {e}")
        time.sleep(0.5)

    print("\nFinal state:", cb.get_state())
```

### 2.2 — Versão Assíncrona (Produção)

```python
"""
Circuit Breaker assíncrono (compatível com FastAPI).
"""
import asyncio
import time
from enum import Enum
from typing import Callable, Any, Awaitable
from dataclasses import dataclass


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class AsyncCircuitBreakerConfig:
    failure_threshold: int = 5
    success_threshold: int = 2
    timeout: float = 60.0
    expected_exceptions: tuple = (Exception,)
    name: str = "default"


class AsyncCircuitBreaker:
    def __init__(self, config: AsyncCircuitBreakerConfig):
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None

        # Lock para thread-safety
        self._lock = asyncio.Lock()

        # Métricas
        self.stats = {
            "total_calls": 0,
            "total_successes": 0,
            "total_failures": 0,
            "total_short_circuits": 0,
        }

    async def call(self, func: Callable[..., Awaitable], *args, **kwargs) -> Any:
        """Executa função async com proteção"""
        async with self._lock:
            self.stats["total_calls"] += 1

            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self._transition_to(CircuitState.HALF_OPEN)
                else:
                    self.stats["total_short_circuits"] += 1
                    raise CircuitBreakerOpenError(
                        f"Circuit '{self.config.name}' is OPEN"
                    )

        # Executar (fora do lock para não bloquear)
        try:
            result = await func(*args, **kwargs)

            async with self._lock:
                await self._on_success()

            return result

        except self.config.expected_exceptions:
            async with self._lock:
                await self._on_failure()
            raise

    async def _on_success(self):
        self.stats["total_successes"] += 1

        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self._close()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0

    async def _on_failure(self):
        self.stats["total_failures"] += 1
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitState.HALF_OPEN:
            self._open()
        elif self.state == CircuitState.CLOSED:
            if self.failure_count >= self.config.failure_threshold:
                self._open()

    def _should_attempt_reset(self) -> bool:
        return (time.time() - self.last_failure_time) >= self.config.timeout

    def _open(self):
        self._transition_to(CircuitState.OPEN)
        self.success_count = 0

    def _close(self):
        self._transition_to(CircuitState.CLOSED)
        self.failure_count = 0
        self.success_count = 0

    def _transition_to(self, new_state: CircuitState):
        old_state = self.state
        self.state = new_state
        # Em produção, enviar para log/observabilidade
        print(f"[{self.config.name}] {old_state.value} → {new_state.value}")


# Uso
async def example():
    cb = AsyncCircuitBreaker(AsyncCircuitBreakerConfig(
        name="openai",
        failure_threshold=3,
        timeout=30,
    ))

    async def call_openai():
        # Em produção: openai_client.chat.completions.create(...)
        return "response"

    try:
        result = await cb.call(call_openai)
    except CircuitBreakerOpenError:
        # Fallback
        result = "cached_response"
```

### 2.3 — Versão com Fallback

```python
"""
Circuit Breaker com fallback automático.
"""
from typing import Callable, Any, Optional


class AsyncCircuitBreakerWithFallback(AsyncCircuitBreaker):
    def __init__(self, config, fallback: Optional[Callable] = None):
        super().__init__(config)
        self.fallback = fallback

    async def call(self, func, *args, **kwargs):
        try:
            return await super().call(func, *args, **kwargs)
        except (CircuitBreakerOpenError, Exception) as e:
            if self.fallback:
                # Log + fallback
                print(f"[{self.config.name}] Falling back: {e}")
                if asyncio.iscoroutinefunction(self.fallback):
                    return await self.fallback(*args, **kwargs)
                else:
                    return self.fallback(*args, **kwargs)
            raise


# Uso
async def cached_response(*args, **kwargs):
    return "Resposta em cache (fallback)"


cb = AsyncCircuitBreakerWithFallback(
    config=AsyncCircuitBreakerConfig(name="openai", failure_threshold=3),
    fallback=cached_response,
)

# Quando OpenAI cai:
# 1. Circuit breaker detecta 3 falhas
# 2. Vai para OPEN
# 3. Próximas requests não chamam OpenAI
# 4. Fallback retorna "cached response"
# 5. Usuário vê resposta (mesmo que degradada)
```

---

## 📊 Parte 3: Métricas Prometheus

### 3.1 — Integração

```python
"""
Circuit Breaker com métricas Prometheus.
"""
from prometheus_client import Counter, Gauge, Histogram


class InstrumentedCircuitBreaker(AsyncCircuitBreaker):
    def __init__(self, config, registry=None):
        super().__init__(config)

        # Métricas
        self.calls_total = Counter(
            'circuit_breaker_calls_total',
            'Total de chamadas',
            labelnames=['name', 'outcome'],  # outcome: success | failure | short_circuit
            registry=registry,
        )

        self.state_gauge = Gauge(
            'circuit_breaker_state',
            'Estado atual (0=closed, 1=half_open, 2=open)',
            labelnames=['name'],
            registry=registry,
        )

        self.latency = Histogram(
            'circuit_breaker_call_duration_seconds',
            'Latência das chamadas',
            labelnames=['name', 'outcome'],
            registry=registry,
        )

    async def call(self, func, *args, **kwargs):
        start = time.time()
        outcome = "success"

        try:
            result = await super().call(func, *args, **kwargs)
            return result
        except CircuitBreakerOpenError:
            outcome = "short_circuit"
            raise
        except Exception:
            outcome = "failure"
            raise
        finally:
            duration = time.time() - start
            self.calls_total.labels(
                name=self.config.name,
                outcome=outcome,
            ).inc()
            self.latency.labels(
                name=self.config.name,
                outcome=outcome,
            ).observe(duration)
            self.state_gauge.labels(name=self.config.name).set(
                {"closed": 0, "half_open": 1, "open": 2}[self.state.value]
            )
```

### 3.2 — Alertas

```yaml
# prometheus-alerts.yml
groups:
  - name: circuit_breaker
    rules:
      - alert: CircuitBreakerOpen
        expr: circuit_breaker_state{name="openai"} == 2
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "OpenAI circuit breaker está OPEN"
          action: "Verificar status.openai.com, considerar fallback"

      - alert: HighShortCircuitRate
        expr: |
          rate(circuit_breaker_calls_total{outcome="short_circuit"}[5m]) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Alta taxa de short-circuits (CB abrindo)"

      - alert: HighFailureRate
        expr: |
          rate(circuit_breaker_calls_total{outcome="failure"}[5m])
          /
          rate(circuit_breaker_calls_total[5m]) > 0.5
        for: 5m
        labels:
          severity: warning
```

---

## 🚀 Parte 4: Integração com FastAPI

### 4.1 — Setup Completo

```python
"""
FastAPI app com circuit breakers para dependências externas.
"""
import httpx
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager


# Circuit breakers por dependência
openai_cb = InstrumentedCircuitBreaker(AsyncCircuitBreakerConfig(
    name="openai",
    failure_threshold=5,
    success_threshold=2,
    timeout=60,
    expected_exceptions=(httpx.TimeoutException, httpx.HTTPStatusError),
))

anthropic_cb = InstrumentedCircuitBreaker(AsyncCircuitBreakerConfig(
    name="anthropic",
    failure_threshold=5,
    success_threshold=2,
    timeout=60,
))

db_cb = InstrumentedCircuitBreaker(AsyncCircuitBreakerConfig(
    name="database",
    failure_threshold=3,
    success_threshold=1,
    timeout=30,
    expected_exceptions=(asyncpg.PostgresError,),
))


# Clientes
http_client = httpx.AsyncClient(timeout=httpx.Timeout(10.0))


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await http_client.aclose()


app = FastAPI(lifespan=lifespan)


# Endpoint com CB
@app.post("/v1/llm/invoke")
async def invoke_llm(message: str):
    try:
        result = await openai_cb.call(
            call_openai,
            message=message,
        )
        return {"response": result}
    except CircuitBreakerOpenError:
        # Fallback para Anthropic
        try:
            result = await anthropic_cb.call(
                call_anthropic,
                message=message,
            )
            return {"response": result, "model": "claude-fallback"}
        except CircuitBreakerOpenError:
            raise HTTPException(
                status_code=503,
                detail="All LLM providers unavailable",
            )


# Funções chamadas pelos CBs
async def call_openai(message: str) -> str:
    response = await http_client.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_KEY}"},
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": message}],
        },
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


async def call_anthropic(message: str) -> str:
    response = await http_client.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
        },
        json={
            "model": "claude-haiku-4-5",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": message}],
        },
    )
    response.raise_for_status()
    return response.json()["content"][0]["text"]
```

### 4.2 — Endpoint de Status

```python
@app.get("/v1/circuit-breakers/status")
async def cb_status():
    """Retorna status de todos os circuit breakers"""
    return {
        "openai": openai_cb.get_state(),
        "anthropic": anthropic_cb.get_state(),
        "database": db_cb.get_state(),
    }


@app.post("/v1/circuit-breakers/{name}/reset")
async def reset_cb(name: str):
    """Reset manual de um CB"""
    breakers = {
        "openai": openai_cb,
        "anthropic": anthropic_cb,
        "database": db_cb,
    }
    if name not in breakers:
        raise HTTPException(404, "Breaker not found")

    cb = breakers[name]
    cb._close()  # force close
    return {"message": f"{name} reset to CLOSED"}
```

---

## 🧪 Parte 5: Testes

### 5.1 — Teste de Integração

```python
"""
Teste de circuit breaker com serviço flaky.
"""
import pytest
import httpx
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_circuit_breaker_opens_after_failures():
    """Testa que CB abre após N falhas"""
    cb = InstrumentedCircuitBreaker(AsyncCircuitBreakerConfig(
        name="test",
        failure_threshold=3,
    ))

    # Mock que sempre falha
    failing_func = AsyncMock(side_effect=httpx.TimeoutException("timeout"))

    # 3 falhas devem abrir o CB
    for i in range(3):
        with pytest.raises(httpx.TimeoutException):
            await cb.call(failing_func)

    assert cb.state == CircuitState.OPEN

    # 4ª chamada deve ser bloqueada imediatamente
    with pytest.raises(CircuitBreakerOpenError):
        await cb.call(failing_func)

    # Verificar que função não foi chamada (short-circuit)
    assert failing_func.call_count == 3  # não 4


@pytest.mark.asyncio
async def test_circuit_breaker_recovers():
    """Testa que CB se recupera após timeout"""
    cb = InstrumentedCircuitBreaker(AsyncCircuitBreakerConfig(
        name="test",
        failure_threshold=2,
        timeout=1,  # 1 segundo para teste
    ))

    # Fase 1: Falhas para abrir
    failing = AsyncMock(side_effect=Exception("fail"))
    for _ in range(2):
        with pytest.raises(Exception):
            await cb.call(failing)

    assert cb.state == CircuitState.OPEN

    # Fase 2: Esperar timeout
    await asyncio.sleep(1.1)

    # Fase 3: Função agora funciona
    succeeding = AsyncMock(return_value="OK")
    result = await cb.call(succeeding)

    assert result == "OK"
    assert cb.state == CircuitState.HALF_OPEN

    # Mais 1 sucesso deve fechar
    await cb.call(succeeding)
    assert cb.state == CircuitState.CLOSED


@pytest.mark.asyncio
async def test_circuit_breaker_half_open_failure_reopens():
    """Testa que falha em half-open reabre o CB"""
    cb = InstrumentedCircuitBreaker(AsyncCircuitBreakerConfig(
        name="test",
        failure_threshold=2,
        timeout=0.5,
    ))

    # Abrir
    failing = AsyncMock(side_effect=Exception("fail"))
    for _ in range(2):
        with pytest.raises(Exception):
            await cb.call(failing)

    await asyncio.sleep(0.6)

    # Half-open + falha → reopen
    with pytest.raises(Exception):
        await cb.call(failing)

    assert cb.state == CircuitState.OPEN
```

### 5.2 — Teste com HTTP Mock

```python
"""
Teste E2E com servidor que falha intermitentemente.
"""
import respx
import httpx


@pytest.mark.asyncio
@respx.mock
async def test_circuit_breaker_with_real_http():
    """Testa CB com servidor HTTP mockado"""
    respx.post("https://api.openai.com/v1/chat/completions").mock(
        side_effect=httpx.TimeoutException
    )

    cb = InstrumentedCircuitBreaker(AsyncCircuitBreakerConfig(
        name="openai",
        failure_threshold=3,
    ))

    # Fazer 5 chamadas
    for i in range(5):
        try:
            await cb.call(call_openai, message="test")
        except (CircuitBreakerOpenError, httpx.TimeoutException):
            pass

    # Após 3 falhas, CB deve estar OPEN
    assert cb.state == CircuitState.OPEN
```

---

## 📚 Parte 6: Libs Externas

### 6.1 — pybreaker

```python
"""
Usando pybreaker (lib mais popular).
"""
import pybreaker


# Configurar
breaker = pybreaker.CircuitBreaker(
    fail_max=5,         # máx falhas antes de abrir
    reset_timeout=60,   # segundos para tentar reset
    exclude=[],         # exceções a ignorar
    name="openai",
)


@breaker
def call_external_api():
    """Decorador protege a função"""
    response = httpx.get("https://api.example.com/data")
    response.raise_for_status()
    return response.json()


# Estado
print(breaker.current_state)  # 'closed' | 'open' | 'half-open'
print(breaker.fail_counter)
print(breaker.success_counter)


# Listeners (callbacks para state changes)
class Listener(pybreaker.CircuitBreakerListener):
    def state_change(self, cb, old_state, new_state):
        print(f"State changed: {old_state.name} → {new_state.name}")

    def failure(self, cb, exc):
        print(f"Failure: {exc}")

    def success(self, cb):
        print("Success!")

breaker.add_listener(Listener())
```

### 6.2 — circuitbreaker (mais simples)

```python
from circuitbreaker import circuit


@circuit(failure_threshold=5, recovery_timeout=60)
def call_external_api():
    response = httpx.get("https://api.example.com/data")
    response.raise_for_status()
    return response.json()
```

### 6.3 — Comparação

| Lib | Prós | Contras |
|-----|------|---------|
| **Custom (nossa)** | Total controle, sem dependência | Mais código para manter |
| **pybreaker** | Maduro, listeners, métricas | Não async nativo |
| **circuitbreaker** | Simples, decorator-based | Menos features |
| **purgatory** | Async nativo | Menos popular |
| **aiobreaker** | Async + thread-safe | API complexa |

**Recomendação:** use lib se já tem; implemente custom se precisa de features específicas (métricas custom, multi-tenant, etc).

---

## 🎯 Casos de Uso Reais

### Caso 1: Multi-Provider LLM com Fallback

**Problema:** OpenAI às vezes cai, deixar usuário sem resposta é ruim.

**Solução:** CB em OpenAI + fallback para Anthropic.

```python
async def smart_llm_call(message: str) -> str:
    try:
        return await openai_cb.call(call_openai, message=message)
    except (CircuitBreakerOpenError, Exception) as e:
        # OpenAI falhou ou CB aberto
        try:
            return await anthropic_cb.call(call_anthropic, message=message)
        except (CircuitBreakerOpenError, Exception):
            # Ambos falharam
            return await cached_response_for(message)  # cache local
```

### Caso 2: Database com Read Replicas

**Problema:** DB primária sobrecarregada, queries lentas.

**Solução:** CB em primária, fallback para replicas.

```python
async def read_query(sql: str):
    try:
        return await primary_db_cb.call(primary_db.fetch, sql)
    except CircuitBreakerOpenError:
        # Primária sobrecarregada, vai para replica
        return await replica_db.fetch(sql)
```

### Caso 3: API Externa com Cache

**Problema:** API de pagamento flaky.

**Solução:** CB + cache de últimas respostas válidas.

```python
@cached(ttl=300)  # 5 min cache
async def get_exchange_rate():
    return await external_api.get_rate()


async def safe_exchange_rate():
    try:
        return await external_cb.call(get_exchange_rate)
    except CircuitBreakerOpenError:
        # Usa último valor cacheado
        return cache.get("last_rate", default=1.0)
```

---

## 🏆 Boas Práticas

### 1. Escolha Thresholds Certos

- **failure_threshold:** muito baixo = falsos positivos. muito alto = cascade. Comece com 5.
- **timeout:** baseado em SLA do serviço downstream. Se é 99% em 1s, timeout 5-10s.
- **success_threshold:** 1-3. Mais alto = mais conservador.

### 2. Monitore Estado

- **Alerta** quando CB abre (PagerDuty)
- **Dashboard** com % tempo em cada estado
- **Histórico** de aberturas (correlacionar com deploys)

### 3. Tenha Fallback Sensato

- Cache de última resposta
- Resposta default ("Serviço temporariamente indisponível")
- Versão degradada (sem features avançadas)

### 4. Não Use CB Para Tudo

**Use CB para:**
- Chamadas a APIs externas
- DB queries lentas
- Operações com dependência de rede

**NÃO use para:**
- Operações locais (sempre rápido)
- Operações críticas (não pode falhar)
- Operações com retry próprio (pode duplicar)

### 5. Teste em Produção (Chaos Engineering)

- Mate uma dependência aleatória
- Veja se CB abre corretamente
- Veja se fallback funciona
- Documente em runbook

---

## 📚 Materiais Complementares

- `apostilas/45-debugging-otimizacao-agentes-ia.md` — debug
- `apostilas/46-arquitetura-multi-tenant-2026.md` — multi-tenant
- `tutoriais/30-criar-dashboard-grafana-mavis.md` — monitoramento
- `treinamentos/WS-13-oficina-debug-agentes-producao.md` — debug prod
- `Lib-Nexus/best-practices/05-sre-observability.md` — SRE
- `Lib-Nexus/best-practices/01-error-handling.md` — error handling
- `producao/INCIDENT-RESPONSE-RUNBOOK.md` — incidentes

---

## 🔗 Links Externos

- Martin Fowler: https://martinfowler.com/bliki/CircuitBreaker.html
- pybreaker: https://github.com/danielfm/pybreaker
- Netflix Hystrix (referência): https://github.com/Netflix/Hystrix/wiki
- Microsoft Azure docs: https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker

---

*AcademIA · Tutorial 31 · Circuit Breaker Pattern · 2026*