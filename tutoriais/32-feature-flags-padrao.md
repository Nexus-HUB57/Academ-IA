---
title: "Tutorial 32 · Feature Flags · Padrão Completo"
subtitle: "Como implementar feature flags para rollout gradual, A/B testing e kill switches"
author: "Equipo Nexus · Ravi (CTO/AI) + Niko (CEO/AI)"
version: "1.0.0"
date: 2026-07-30
pattern: "MMN_IA"
---

**Tutorial 32 · Feature Flags · Padrão Completo**

*Tutorial de 1h implementando feature flags para rollout gradual, A/B testing, e kill switches. Cobre tipos, providers, e integração com FastAPI + LaunchDarkly/Statsig/UNLEASH.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 O que Você Vai Conquistar

Em 1h, você vai:

1. Entender 4 tipos de feature flags
2. Implementar FF custom (sem dependência externa)
3. Integrar com LaunchDarkly/Statsig (SaaS)
4. Implementar A/B testing baseado em FF
5. Usar para kill switches e rollout gradual
6. Testar com pytest

**Pré-requisitos:**
- Python intermediário
- FastAPI básico

---

## 🧠 Parte 1: Conceito

### 1.1 — O que é Feature Flag

**Definição:** mecanismo para ativar/desativar funcionalidades **sem deploy**.

**Tradicional:**
```
Nova feature → merge → deploy → 100% dos usuários
```

**Com feature flag:**
```
Nova feature → merge atrás de flag → deploy
↓
Ativar flag para 1% (canary)
↓
Ativar para 10% (early adopters)
↓
Ativar para 50%
↓
Ativar para 100%
```

### 1.2 — Benefícios

✅ **Trunk-based development:** merge diário, sem branches longas
✅ **Rollout gradual:** minimizar blast radius de bugs
✅ **Rollback instantâneo:** desligar flag, sem deploy
✅ **A/B testing:** flag = "treatment" vs "control"
✅ **Kill switch:** desabilitar feature em incidente
✅ **Beta testing:** flag ativa para early adopters

### 1.3 — Tipos

**1. Release Toggle (deploy vs release)**
- Curta duração (dias/semanas)
- Remove após 100% rollout
- Ex: nova feature beta

**2. Experiment Toggle (A/B test)**
- Média duração (semanas/meses)
- Múltiplas variantes
- Ex: testar 2 UIs

**3. Ops Toggle (kill switch)**
- Longa duração (meses/anos)
- Nunca removido
- Ex: desabilitar integração com serviço problemático

**4. Permission Toggle (acesso por usuário)**
- Longa duração
- Baseado em tier/role
- Ex: feature premium só para Pro+

### 1.4 — Anti-patterns

❌ **Muitas flags:** se você tem 100 flags ativas, ninguém sabe o que está ligado
❌ **Flags permanentes sem limpeza:** tech debt cresce
❌ **Flags sem auditoria:** "quem ligou isso?"
❌ **Flags sem fallback:** quando flag falha, sistema quebra
❌ **Flags para config:** não use flag para "qual é o timeout?" — use env var

---

## 🔨 Parte 2: Implementação Custom

### 2.1 — Feature Flag Manager Simples

```python
"""
Feature Flag Manager in-memory (didático).
Em produção: usar LaunchDarkly, Statsig, ou Unleash.
"""
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
import hashlib
import time


@dataclass
class FeatureFlag:
    name: str
    enabled: bool
    rollout_pct: float = 0.0  # 0.0 a 1.0
    user_whitelist: List[str] = None
    user_blacklist: List[str] = None
    tenant_whitelist: List[str] = None
    tenant_blacklist: List[str] = None
    conditions: List[Callable] = None
    created_at: float = None
    updated_at: float = None


class FeatureFlagManager:
    def __init__(self):
        self.flags: Dict[str, FeatureFlag] = {}

    def create_flag(self, name: str, **kwargs) -> FeatureFlag:
        """Cria flag"""
        flag = FeatureFlag(
            name=name,
            enabled=kwargs.get("enabled", False),
            rollout_pct=kwargs.get("rollout_pct", 0.0),
            user_whitelist=kwargs.get("user_whitelist"),
            user_blacklist=kwargs.get("user_blacklist"),
            tenant_whitelist=kwargs.get("tenant_whitelist"),
            tenant_blacklist=kwargs.get("tenant_blacklist"),
            conditions=kwargs.get("conditions"),
            created_at=time.time(),
            updated_at=time.time(),
        )
        self.flags[name] = flag
        return flag

    def update_flag(self, name: str, **kwargs):
        """Atualiza flag"""
        if name not in self.flags:
            raise KeyError(f"Flag '{name}' not found")

        flag = self.flags[name]
        for key, value in kwargs.items():
            if hasattr(flag, key):
                setattr(flag, key, value)
        flag.updated_at = time.time()

    def is_enabled(self, name: str, user_id: str = None,
                   tenant_id: str = None, attributes: dict = None) -> bool:
        """Avalia se flag está ativa para o contexto"""
        if name not in self.flags:
            return False  # default OFF

        flag = self.flags[name]

        # Master switch
        if not flag.enabled:
            return False

        # Blacklists (sempre bloqueia)
        if user_id and flag.user_blacklist and user_id in flag.user_blacklist:
            return False
        if tenant_id and flag.tenant_blacklist and tenant_id in flag.tenant_blacklist:
            return False

        # Whitelists (sempre permite)
        if user_id and flag.user_whitelist and user_id in flag.user_whitelist:
            return True
        if tenant_id and flag.tenant_whitelist and tenant_id in flag.tenant_whitelist:
            return True

        # Rollout percentual (hash-based, sticky)
        if flag.rollout_pct > 0:
            if not self._is_in_rollout(name, user_id or tenant_id, flag.rollout_pct):
                return False

        # Custom conditions
        if flag.conditions:
            ctx = {
                "user_id": user_id,
                "tenant_id": tenant_id,
                **(attributes or {}),
            }
            for condition in flag.conditions:
                if not condition(ctx):
                    return False

        return True

    def _is_in_rollout(self, flag_name: str, identifier: str, pct: float) -> bool:
        """Hash-based rollout (sticky)"""
        if not identifier:
            return False
        h = int(hashlib.md5(f"{flag_name}-{identifier}".encode()).hexdigest(), 16) % 10000
        return (h / 10000) < pct

    def get_variant(self, name: str, user_id: str,
                   variants: List[str]) -> Optional[str]:
        """Para A/B testing: retorna variante baseado em hash"""
        if not variants:
            return None
        h = int(hashlib.md5(f"{name}-variant-{user_id}".encode()).hexdigest(), 16)
        return variants[h % len(variants)]


# Singleton
ff_manager = FeatureFlagManager()


# Helpers para uso
def is_enabled(flag_name: str, **kwargs) -> bool:
    return ff_manager.is_enabled(flag_name, **kwargs)


def get_variant(flag_name: str, user_id: str, variants: List[str]) -> str:
    return ff_manager.get_variant(flag_name, user_id, variants)
```

### 2.2 — Setup Inicial

```python
"""
Configuração inicial de flags (executar no startup).
"""
def setup_default_flags():
    # Release toggle
    ff_manager.create_flag(
        "new_dashboard_v2",
        enabled=True,
        rollout_pct=0.10,  # 10% dos usuários
        user_whitelist=["user_123", "user_456"],  # early adopters
    )

    # Ops toggle (kill switch)
    ff_manager.create_flag(
        "stripe_integration",
        enabled=True,  # normalmente on
    )

    # Permission toggle
    ff_manager.create_flag(
        "advanced_analytics",
        enabled=True,
        conditions=[
            lambda ctx: ctx.get("tier") in ["pro", "enterprise"],
        ],
    )

    # A/B test
    ff_manager.create_flag(
        "checkout_flow_v2",
        enabled=True,
        rollout_pct=0.50,  # 50% dos usuários
    )
```

---

## 🚀 Parte 3: Integração com FastAPI

### 3.1 — Middleware

```python
"""
FastAPI app com feature flags.
"""
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_default_flags()
    yield


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def ff_middleware(request: Request, call_next):
    """Disponibiliza user_id e tenant_id para handlers"""
    # Extrair do JWT (simplificado)
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth[7:]
        # Decodificar JWT (em produção)
        # payload = jwt.decode(token, ...)
        request.state.user_id = "user_123"  # mock
        request.state.tenant_id = "tenant_a"  # mock
        request.state.tier = "pro"  # mock
    else:
        request.state.user_id = None
        request.state.tenant_id = None
        request.state.tier = "free"

    return await call_next(request)
```

### 3.2 — Decorator

```python
"""
Decorator para condicionar endpoint por flag.
"""
from functools import wraps
from fastapi import HTTPException


def feature_flag(flag_name: str, fallback_value=None):
    """Decorator que bloqueia endpoint se flag off"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request") or args[0]
            ctx = {
                "user_id": getattr(request.state, "user_id", None),
                "tenant_id": getattr(request.state, "tenant_id", None),
                "tier": getattr(request.state, "tier", None),
            }

            if is_enabled(flag_name, **ctx):
                return await func(*args, **kwargs)
            else:
                if fallback_value is not None:
                    return fallback_value
                raise HTTPException(
                    status_code=404,
                    detail="Feature not available",
                )
        return wrapper
    return decorator


# Uso
@app.post("/v1/dashboard/v2")
@feature_flag("new_dashboard_v2")
async def new_dashboard(request: Request):
    return {"dashboard": "v2"}


@app.get("/v1/analytics/advanced")
@feature_flag("advanced_analytics", fallback_value={"data": "upgrade_required"})
async def advanced_analytics(request: Request):
    return {"data": "premium"}
```

### 3.3 — Inline Check

```python
@app.post("/v1/checkout")
async def checkout(request: Request, item_id: str):
    ctx = {
        "user_id": request.state.user_id,
        "tenant_id": request.state.tenant_id,
    }

    if is_enabled("checkout_flow_v2", **ctx):
        # Nova versão
        return await checkout_v2(item_id)
    else:
        # Versão antiga
        return await checkout_v1(item_id)
```

### 3.4 — A/B Test com Variantes

```python
@app.post("/v1/checkout")
async def checkout(request: Request, item_id: str):
    user_id = request.state.user_id
    variant = get_variant("checkout_flow_v2", user_id, ["v1", "v2"])

    if variant == "v2":
        return await checkout_v2(item_id, track_event=True)
    else:
        return await checkout_v1(item_id, track_event=True)
```

---

## 🏢 Parte 4: LaunchDarkly / Statsig / Unleash

### 4.1 — LaunchDarkly (SaaS)

```python
"""
LaunchDarkly SDK para Python.
"""
import ldclient
from ldclient import Context
from ldclient.config import Config


ld_client = ldclient.get()
ld_client.initialize(Config("sdk-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"))


def is_enabled_ld(flag_key: str, user_id: str, **attributes) -> bool:
    """Check flag via LaunchDarkly"""
    ctx = Context.create(user_id, attributes)
    return ld_client.variation(flag_key, ctx, default=False)


def get_variant_ld(flag_key: str, user_id: str, **attributes) -> str:
    """Get variant via LaunchDarkly"""
    ctx = Context.create(user_id, attributes)
    return ld_client.variation(flag_key, ctx, default="control")


# Uso
@app.post("/v1/checkout")
async def checkout(request: Request, item_id: str):
    user_id = request.state.user_id

    if is_enabled_ld("new-checkout", user_id, custom={"tier": "pro"}):
        return await checkout_v2(item_id)
    else:
        return await checkout_v1(item_id)
```

### 4.2 — Statsig (alternativa popular)

```python
from statsig import statsig


statsig.initialize("secret-xxxxxxxx")


def is_enabled_statsig(gate_name: str, user_id: str, **attributes) -> bool:
    user = {"userID": user_id, **attributes}
    return statsig.check_gate(gate_name, user)


def get_experiment_variant(experiment_name: str, user_id: str) -> str:
    user = {"userID": user_id}
    result = statsig.get_experiment(experiment_name, user)
    return result.get("variant", "control")
```

### 4.3 — Unleash (self-hosted)

```python
from UnleashClient import UnleashClient


unleash = UnleashClient(
    url="https://unleash.nexus.com/api/",
    app_name="nexus-api",
    custom_headers={"Authorization": "unleash-api-token"},
)


def is_enabled_unleash(feature_name: str, context: dict = None) -> bool:
    return unleash.is_enabled(feature_name, context or {})
```

### 4.4 — Comparação

| Feature | LaunchDarkly | Statsig | Unleash | Custom |
|---------|--------------|---------|---------|--------|
| **Pricing** | $$$ | $$ | Free (self-hosted) | Free |
| **Setup time** | 5 min | 5 min | 30 min | 30 min |
| **UI dashboard** | Excelente | Excelente | Bom | Não |
| **A/B testing** | Sim | Excelente | Limitado | Manual |
| **Self-hosted** | Não | Não | Sim | Sim |
| **Audit log** | Sim | Sim | Sim | Manual |
| **Vendor lock-in** | Alto | Alto | Baixo | Nenhum |

**Recomendação:**
- **Startup pequeno:** Custom ou Unleash
- **Scale-up:** Statsig (melhor A/B)
- **Enterprise:** LaunchDarkly (mais features)

---

## 🧪 Parte 5: Padrões de Uso

### 5.1 — Canary Release

```python
# Gradual rollout
ROLLOUT_STAGES = [
    {"pct": 0.01, "duration_hours": 24},   # 1% por 24h
    {"pct": 0.05, "duration_hours": 24},   # 5% por 24h
    {"pct": 0.25, "duration_hours": 48},   # 25% por 48h
    {"pct": 0.50, "duration_hours": 48},   # 50% por 48h
    {"pct": 1.00, "duration_hours": None}, # 100% final
]

# Setup via LaunchDarkly/Statsig UI
# ff_manager.create_flag("new_algorithm", rollout_pct=0.01)
```

### 5.2 — A/B Test

```python
# 4 variantes: control, variant_a, variant_b, variant_c
VARIANTS = ["control", "variant_a", "variant_b", "variant_c"]


@app.post("/v1/landing-page")
async def landing_page(request: Request):
    user_id = request.state.user_id
    variant = get_variant("homepage_redesign", user_id, VARIANTS)

    if variant == "control":
        return render_homepage_v1()
    elif variant == "variant_a":
        return render_homepage_v2_red()
    elif variant == "variant_b":
        return render_homepage_v2_green()
    else:
        return render_homepage_v2_blue()


# Track conversion
@app.post("/v1/signup")
async def signup(request: Request):
    user_id = request.state.user_id
    variant = get_variant("homepage_redesign", user_id, VARIANTS)

    # Track para análise
    analytics.track("signup", user_id=user_id, variant=variant)
    ...
```

### 5.3 — Kill Switch

```python
# Flag sempre presente, desliga em incidente
ff_manager.create_flag(
    "payment_stripe",
    enabled=True,  # normalmente on
    # Se Stripe tiver problema, ops liga flag=false
)


@app.post("/v1/payment")
async def process_payment(request: Request):
    if not is_enabled("payment_stripe", user_id=request.state.user_id):
        # Fallback para outro provider
        return await process_payment_pagarme(request)

    return await process_payment_stripe(request)
```

### 5.4 — Permission Tier

```python
# Feature por tier
@app.post("/v1/agents/{agent_id}/clone")
async def clone_agent(request: Request, agent_id: str):
    tier = request.state.tier
    user_id = request.state.user_id

    if not is_enabled("clone_agents", user_id=user_id, tier=tier):
        raise HTTPException(402, "Upgrade to Pro to clone agents")

    # ... clone logic
```

### 5.5 — Maintenance Mode

```python
# Em manutenção, bloquear features não-críticas
ff_manager.create_flag("maintenance_mode", enabled=False)


@app.middleware("http")
async def maintenance_middleware(request: Request, call_next):
    user_id = getattr(request.state, "user_id", None)
    is_admin = getattr(request.state, "is_admin", False)

    if is_enabled("maintenance_mode", user_id=user_id) and not is_admin:
        return JSONResponse(
            status_code=503,
            content={"error": "Service under maintenance. Try again later."},
        )

    return await call_next(request)
```

---

## 📊 Parte 6: Métricas e Auditoria

### 6.1 — Logging de Avaliações

```python
"""
Log de cada avaliação de flag.
"""
import structlog

log = structlog.get_logger()


def is_enabled_audited(flag_name: str, **ctx) -> bool:
    result = is_enabled(flag_name, **ctx)
    log.info(
        "feature_flag_evaluated",
        flag=flag_name,
        result=result,
        user_id=ctx.get("user_id"),
        tenant_id=ctx.get("tenant_id"),
    )
    return result


# Métricas
flag_eval_total = Counter(
    'feature_flag_evaluations_total',
    'Total de avaliações de feature flag',
    labelnames=['flag', 'result'],
)

flag_eval_users = Gauge(
    'feature_flag_active_users',
    'Usuários com flag ativa',
    labelnames=['flag'],
)


def is_enabled_metrics(flag_name: str, **ctx) -> bool:
    result = is_enabled(flag_name, **ctx)
    flag_eval_total.labels(flag=flag_name, result=str(result).lower()).inc()
    return result
```

### 6.2 — Audit Log

```python
"""
Log de mudanças em flags (quem ligou/desligou).
"""
@app.post("/admin/flags/{name}/update")
async def update_flag(name: str, updates: dict, request: Request):
    user_id = request.state.user_id
    is_admin = getattr(request.state, "is_admin", False)

    if not is_admin:
        raise HTTPException(403, "Admin only")

    # Log antes
    old_state = ff_manager.flags[name]

    # Update
    ff_manager.update_flag(name, **updates)

    # Log depois
    log.warning(
        "feature_flag_changed",
        flag=name,
        changed_by=user_id,
        old_enabled=old_state.enabled,
        new_enabled=updates.get("enabled"),
        old_rollout=old_state.rollout_pct,
        new_rollout=updates.get("rollout_pct"),
    )

    return {"status": "updated"}
```

---

## 🧪 Parte 7: Testes

### 7.1 — Teste Unitário

```python
import pytest


def test_flag_creation():
    fm = FeatureFlagManager()
    fm.create_flag("test", enabled=True, rollout_pct=0.5)

    assert fm.is_enabled("test", user_id="user_1")  # 50% chance


def test_flag_whitelist():
    fm = FeatureFlagManager()
    fm.create_flag(
        "test",
        enabled=True,
        rollout_pct=0.0,
        user_whitelist=["user_special"],
    )

    # Whitelist user
    assert fm.is_enabled("test", user_id="user_special")

    # Non-whitelist user (rollout 0)
    assert not fm.is_enabled("test", user_id="user_normal")


def test_flag_blacklist():
    fm = FeatureFlagManager()
    fm.create_flag(
        "test",
        enabled=True,
        rollout_pct=1.0,
        user_blacklist=["user_banned"],
    )

    # Blacklist sempre bloqueia
    assert not fm.is_enabled("test", user_id="user_banned")

    # Outros users passam
    assert fm.is_enabled("test", user_id="user_normal")


def test_flag_rollout_deterministic():
    """Mesmo user sempre recebe mesmo resultado (sticky)"""
    fm = FeatureFlagManager()
    fm.create_flag("test", enabled=True, rollout_pct=0.5)

    user_id = "user_123"
    results = [fm.is_enabled("test", user_id=user_id) for _ in range(100)]
    # Mesma resposta sempre
    assert len(set(results)) == 1
```

### 7.2 — Teste de Integração

```python
from fastapi.testclient import TestClient


def test_endpoint_with_flag_on(client: TestClient):
    ff_manager.create_flag("test_feature", enabled=True, rollout_pct=1.0)

    response = client.post("/v1/test-feature", headers={"Authorization": "Bearer ..."})
    assert response.status_code == 200


def test_endpoint_with_flag_off(client: TestClient):
    ff_manager.update_flag("test_feature", enabled=False)

    response = client.post("/v1/test-feature", headers={"Authorization": "Bearer ..."})
    assert response.status_code == 404
```

---

## 🎯 Boas Práticas

### 1. Naming Convention

```
[category]_[name]_[variant]
new_dashboard_v2
stripe_integration_killswitch
checkout_flow_ab_test
advanced_analytics_pro
```

### 2. Limpeza Periódica

- Remover flags 100% rollout após 2 semanas
- Auditar flags ativas mensalmente
- Documentar quem é owner de cada flag

### 3. Documentação

```yaml
# flags.yml
flags:
  new_dashboard_v2:
    type: release
    owner: "carla@nexus.com"
    created: "2026-07-15"
    expected_removal: "2026-08-15"
    description: |
      Novo dashboard com métricas em tempo real.
      Rollout gradual: 1% → 10% → 50% → 100%
      Métrica de sucesso: tempo médio de sessão > 5min
    rollback_plan: "Desligar flag. Sem impacto em produção."
```

### 4. Tests Flags

- Sempre tenha `enabled=False` como default seguro
- Tests devem funcionar com flag off E on
- Não dependa de flag para lógica crítica (security)

### 5. Monitoring

- Dashboard com % de usuários por variante
- Alerta quando flag está off há muito tempo (deprecation)
- Métricas de conversão por variante (A/B)

---

## 📚 Materiais Complementares

- `apostilas/45-debugging-otimizacao-agentes-ia.md` — debug
- `apostilas/46-arquitetura-multi-tenant-2026.md` — multi-tenant
- `tutoriais/31-circuit-breaker-padrao.md` — circuit breaker
- `Lib-Nexus/best-practices/01-error-handling.md` — error handling
- `governanca/PB-GOVERN-postmortem-blame-free.md` — post-mortem

---

## 🔗 Links Externos

- Martin Fowler: https://martinfowler.com/articles/feature-toggles.html
- LaunchDarkly: https://launchdarkly.com/
- Statsig: https://statsig.com/
- Unleash: https://www.getunleash.io/
- OpenFeature (padrão CNCF): https://openfeature.dev/

---

*AcademIA · Tutorial 32 · Feature Flags · 2026*