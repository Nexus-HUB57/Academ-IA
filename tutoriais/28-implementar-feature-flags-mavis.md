---
version: "1.0-mavis-recovery"
recovery_note: "Versão recuperada após force-push de 2026-07-29. Coexiste com o canônico em tutoriais/(sem equivalente canônico).md"
title: "Tutorial 28 · Implementar Feature Flags em Produção"
description: "Como usar feature flags (LaunchDarkly-style) para rollout gradual, A/B test, e kill switch"
tags: [tutorial, 28, feature-flags, rollout, ab-test, kill-switch, devops]
tier: "Master"
duracao_estimada: "25 min"
pre_requisitos: ["tutoriais/21-deploy-api-ia-producao.md", "tutoriais/24-implementar-rate-limiting.md"]
ultima_atualizacao: 2026-07-27
---

# Tutorial 28 · Implementar Feature Flags em Produção

> **Por que importa**: Feature flags desacoplam deploy de release. Permite rollout gradual, A/B test em produção, e kill switch instantâneo. Em vez de 1 deploy arriscado, 100% dos usuários em 1% → 10% → 50% → 100%.

## 🎯 O que você vai aprender

- Implementar sistema de feature flags com Redis
- Targeting por usuário, tier, e percentage rollout
- Kill switch para emergências
- A/B test integrado com métricas

## ⏱️ Duração: 25 minutos

---

## 📋 Passo 1: Modelo de Dados

```python
# feature_flags.py
from enum import Enum
from typing import Optional, Dict, List
from pydantic import BaseModel
import redis
import json
import hashlib
from datetime import datetime

class FlagStatus(str, Enum):
    DISABLED = "disabled"
    ENABLED = "enabled"
    PERCENTAGE = "percentage"  # rollout gradual
    TARGETED = "targeted"  # lista específica de usuários

class FeatureFlag(BaseModel):
    key: str
    description: str
    status: FlagStatus
    percentage: int = 0  # 0-100, usado quando status=percentage
    targeted_users: List[str] = []
    targeted_tiers: List[str] = []
    created_at: datetime
    updated_at: datetime
    owner: str  # email do responsável
```

## 📋 Passo 2: Storage em Redis

```python
class FeatureFlagStore:
    def __init__(self, redis_client: redis.Redis):
        self.r = redis_client
        self.prefix = "ff:"

    def get(self, key: str) -> Optional[FeatureFlag]:
        data = self.r.get(f"{self.prefix}{key}")
        if not data:
            return None
        return FeatureFlag(**json.loads(data))

    def set(self, flag: FeatureFlag):
        flag.updated_at = datetime.utcnow()
        self.r.set(f"{self.prefix}{flag.key}", flag.json())

    def all(self) -> List[FeatureFlag]:
        keys = self.r.keys(f"{self.prefix}*")
        flags = []
        for k in keys:
            data = self.r.get(k)
            if data:
                flags.append(FeatureFlag(**json.loads(data)))
        return flags

    def delete(self, key: str):
        self.r.delete(f"{self.prefix}{key}")

store = FeatureFlagStore(redis.Redis(host='localhost', port=6379, db=0))
```

## 📋 Passo 3: Avaliação de Flag

```python
def is_enabled(flag_key: str, user_context: dict) -> bool:
    """
    user_context = {
        'user_id': 'usr_123',
        'tier': 'premium',
        'email': 'user@example.com',
        'created_at': '2026-01-15'
    }
    """
    flag = store.get(flag_key)
    if not flag:
        return False  # Default: feature desligada se flag não existe

    if flag.status == FlagStatus.DISABLED:
        return False

    if flag.status == FlagStatus.ENABLED:
        return True

    if flag.status == FlagStatus.TARGETED:
        # Verificar lista de usuários
        if user_context.get('user_id') in flag.targeted_users:
            return True
        if user_context.get('tier') in flag.targeted_tiers:
            return True
        return False

    if flag.status == FlagStatus.PERCENTAGE:
        # Hash determinístico: mesmo user sempre cai no mesmo bucket
        user_id = user_context.get('user_id', '')
        if not user_id:
            return False
        hash_value = int(hashlib.md5(f"{flag_key}:{user_id}".encode()).hexdigest(), 16)
        bucket = (hash_value % 100) + 1  # 1-100
        return bucket <= flag.percentage

    return False
```

## 📋 Passo 4: Decorator para Código

```python
from functools import wraps
import sentry_sdk

def feature_flag(flag_key: str, fallback=None):
    """
    Decorator que só executa função se feature flag estiver enabled.
    Caso contrário, executa fallback (ou retorna None).
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_context = kwargs.get('user_context', {})
            if is_enabled(flag_key, user_context):
                # Tag para análise no Sentry
                sentry_sdk.set_tag(f"flag.{flag_key}", "on")
                return await func(*args, **kwargs)
            else:
                sentry_sdk.set_tag(f"flag.{flag_key}", "off")
                if fallback:
                    return await fallback(*args, **kwargs) if callable(fallback) else fallback
                return None
        return wrapper
    return decorator

# Uso
@app.post("/v1/generate")
@feature_flag("new_llm_model", fallback=old_generate)
async def generate(request: GenerateRequest, user_context: dict = Depends(get_user_context)):
    # Só executa se flag "new_llm_model" estiver on para este user
    return await call_new_model(request)
```

## 📋 Passo 5: CLI para Gerenciar Flags

```python
# flags_cli.py
import typer
from feature_flags import FeatureFlag, FeatureFlagStore, FlagStatus, store
from datetime import datetime

app = typer.Typer(help="Gerenciador de feature flags")

@app.command("create")
def create(
    key: str = typer.Argument(...),
    description: str = typer.Option(..., "--desc"),
    owner: str = typer.Option(..., "--owner", help="Email do responsável")
):
    """Cria nova feature flag (default: disabled)."""
    flag = FeatureFlag(
        key=key,
        description=description,
        status=FlagStatus.DISABLED,
        owner=owner,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    store.set(flag)
    typer.echo(f"✓ Flag '{key}' criada (disabled)")

@app.command("enable")
def enable(
    key: str = typer.Argument(...),
    percentage: int = typer.Option(100, "--p", help="Porcentagem de rollout (0-100)")
):
    """Ativa flag com percentage rollout."""
    flag = store.get(key)
    if not flag:
        typer.echo(f"❌ Flag '{key}' não existe")
        raise typer.Exit(1)

    flag.status = FlagStatus.PERCENTAGE
    flag.percentage = percentage
    store.set(flag)
    typer.echo(f"✓ Flag '{key}' enabled para {percentage}% dos usuários")

@app.command("target")
def target(
    key: str = typer.Argument(...),
    user_id: str = typer.Option(None, "--user"),
    tier: str = typer.Option(None, "--tier")
):
    """Adiciona targeting específico."""
    flag = store.get(key)
    if not flag:
        typer.echo(f"❌ Flag '{key}' não existe")
        raise typer.Exit(1)

    flag.status = FlagStatus.TARGETED
    if user_id and user_id not in flag.targeted_users:
        flag.targeted_users.append(user_id)
    if tier and tier not in flag.targeted_tiers:
        flag.targeted_tiers.append(tier)

    store.set(flag)
    typer.echo(f"✓ Targeting atualizado: users={flag.targeted_users}, tiers={flag.targeted_tiers}")

@app.command("kill")
def kill(key: str = typer.Argument(...)):
    """KILL SWITCH — desliga flag instantaneamente."""
    flag = store.get(key)
    if not flag:
        typer.echo(f"❌ Flag '{key}' não existe")
        raise typer.Exit(1)

    flag.status = FlagStatus.DISABLED
    store.set(flag)
    typer.echo(f"🛑 Flag '{key}' DESLIGADA (kill switch)")

@app.command("list")
def list_all():
    """Lista todas as flags."""
    from rich.table import Table
    from rich.console import Console
    console = Console()

    flags = store.all()
    table = Table(title=f"Feature Flags ({len(flags)})")
    table.add_column("Key", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Percentage", justify="right")
    table.add_column("Owner")

    for f in flags:
        table.add_row(f.key, f.status.value, str(f.percentage), f.owner)
    console.print(table)
```

```bash
# Workflow típico de rollout
flags_cli.py create new_payment_flow --desc "Novo fluxo de pagamento" --owner="cto@nexus.com"
flags_cli.py target new_payment_flow --tier internal
# Testar internamente
flags_cli.py enable new_payment_flow --p 1      # 1% canary
flags_cli.py enable new_payment_flow --p 10     # 10%
flags_cli.py enable new_payment_flow --p 50     # 50%
flags_cli.py enable new_payment_flow --p 100    # 100% full
# OU se algo der errado:
flags_cli.py kill new_payment_flow              # Instantâneo
```

## 📋 Passo 6: Métricas de Feature Flag

```python
# Adicionar tracking
from prometheus_client import Counter, Histogram

flag_evaluations = Counter(
    'feature_flag_evaluations_total',
    'Total feature flag evaluations',
    ['flag_key', 'result']
)

flag_evaluation_duration = Histogram(
    'feature_flag_evaluation_duration_seconds',
    'Time to evaluate feature flag'
)

@flag_evaluation_duration.time()
def is_enabled_tracked(flag_key: str, user_context: dict) -> bool:
    result = is_enabled(flag_key, user_context)
    flag_evaluations.labels(flag_key=flag_key, result=str(result)).inc()
    return result
```

## 🎓 Próximo Passo

- **Tutoriais relacionados**:
  - `tutoriais/24-implementar-rate-limiting.md` (controle de tráfego)
  - `tutoriais/26-monitorar-com-sentry.md` (rastrear impacto)
  - `tutoriais/08-primeiro-ab-test.md` (A/B test)
- **Curso**: `cursos/master/05-deploy-em-producao.md`
- **Playbook**: Criar `playbooks/PB-FEATURE-ROLLBACK.md` (processo de rollback)

---

**Tutorial criado em 2026-07-27** · Mavis Agent
**Versão 1.0** · Mantido em `tutoriais/28-implementar-feature-flags.md`
