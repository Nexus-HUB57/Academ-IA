---
title: "Best Practices · SRE & Observabilidade"
description: "Padrões canônicos de SRE para o ecossistema Nexus: SLIs, SLOs, error budgets, incident response"
tags: [lib-nexus, best-practices, sre, observability, sli, slo, error-budget, incident]
category: best-practices
version: "1.0"
last_review: "2026-07-22"
---

# 🔧 Best Practices · SRE & Observabilidade

> **Padrões canônicos** de engenharia de confiabilidade e observabilidade para o ecossistema Nexus. Este documento define SLIs, SLOs, error budgets, e o processo de incident response. Complementa `knowledge-base/08-kpis-oficiais-nexus.md` com foco em **operação de produção**.

---

## 🎯 Filosofia SRE Nexus

> **"Confiabilidade é feature."**

SRE Nexus opera sob 4 princípios:

1. **Service Level Objectives** acima de tudo — métricas de negócio, não de sistema.
2. **Error budget** como contrato — tempo de inatividade permitido é recurso finito.
3. **Automação** sobre manual — humans para decisões, automação para execução.
4. **Blameless postmortem** — cultura de aprendizado, não de culpa.

---

## 📏 SLIs (Service Level Indicators)

**SLI** = métrica observável que mede qualidade do serviço.

### SLIs Canônicos Nexus

| Categoria | SLI | Definição |
|-----------|-----|-----------|
| **Availability** | `successful_requests / total_requests` | % de requests que retornam 2xx (excluindo 4xx) |
| **Latency** | `fraction_requests < threshold` | % de requests com latência < threshold |
| **Throughput** | `requests_per_second` | volume de requests por segundo |
| **Error rate** | `failed_requests / total_requests` | % de requests que falham |
| **Freshness** | `time_since_last_update` | idade dos dados retornados |
| **Correctness** | `correct_responses / total_responses` | % de respostas que passam validação |

### Como definir SLI novo

```yaml
slis:
  - name: "campaign_dispatch_success_rate"
    definition: "successful_dispatches / total_dispatches"
    success_criteria: "2xx response within 30s"
    measurement_window: "1h rolling"
    owner: "sre-team"
```

---

## 🎯 SLOs (Service Level Objectives)

**SLO** = target numérico para um SLI em uma janela de tempo.

### SLOs Canônicos Nexus

| Serviço | SLI | Target | Janela |
|---------|-----|--------|--------|
| **API pública** | availability | 99.95% | 30d |
| **API pública** | p99 latency | <200ms | 30d |
| **Orquestrador** | availability | 99.95% | 30d |
| **Orquestrador** | p95 latency | <1s | 30d |
| **Marketplace** | availability | 99.9% | 30d |
| **Marketplace** | checkout success | 99% | 30d |
| **White-Label full** | availability | 99.99% | 30d |
| **SHO** | availability | 99.99% | 30d |
| **SHO** | detection latency SEV-3 | <90s | 30d |

### Como definir SLO novo

```yaml
slos:
  - service: "api-public"
    sli: "availability"
    target: 99.95
    window: "30d"
    error_budget: "21.9 min/month"  # 0.05% * 30d
    burn_rate_alert: 2x  # se consumindo 2x o budget, alerta
    owner: "sre-team"
```

---

## 💰 Error Budget

**Error budget** = tempo de inatividade permitido pelo SLO.

### Cálculo

```
error_budget = (1 - SLO) × window_time
```

Exemplos:

| SLO | Janela | Error Budget |
|-----|--------|--------------|
| 99.9% | 30 dias | 43.2 min/mês |
| 99.95% | 30 dias | 21.6 min/mês |
| 99.99% | 30 dias | 4.32 min/mês |

### Política de Error Budget

1. **< 50% consumido**: operação normal.
2. **50-80% consumido**: aumentar vigilância, priorizar reliability sobre features.
3. **80-100% consumido**: freeze de features, foco em reliability.
4. **100% consumido**: **incident review obrigatório**, freeze total até correção.
5. **Burn rate > 2x**: alerta automático, war room se crítico.

---

## 📊 Observabilidade

### Os 3 Pilares

1. **Métricas** (Prometheus + Grafana)
   - Counter, Gauge, Histogram, Summary.
   - Cardinalidade controlada.
   - Retention: 30d hot, 1y cold.

2. **Logs** (Loki + structured logging)
   - JSON estruturado.
   - Correlation ID em todo request.
   - Sampling baseado em erro.

3. **Traces** (OpenTelemetry + Jaeger)
   - Distributed tracing.
   - Spans em todo hop federado.
   - Sampling 100% para erros, 1% para sucesso.

### Os 3 Sinais de Ouro (USE)

Para cada recurso:

- **Utilization**: quanto está sendo usado.
- **Saturation**: quanto trabalho está na fila.
- **Errors**: taxa de erros.

### Os 4 Sinais de Ouro (RED)

Para cada serviço:

- **Rate**: requests/segundo.
- **Errors**: % com erro.
- **Duration**: latência.
- **Damage**: % de respostas com degradação não-óbvia.

---

## 🚨 Incident Response

### Severidade (alinhada com SHO)

- **SEV-1**: Info, log apenas.
- **SEV-2**: Warning, alerta amarelo.
- **SEV-3**: Alert, alerta laranja. Acionar playbook.
- **SEV-4**: Incident, alerta vermelho. Acionar war room.
- **SEV-5**: Outage, página imediato.

### Fluxo de Incident Response

```
1. Detectar
   ↓
2. Triagem (classificar SEV)
   ↓
3. Conter (isolamento, rollback, kill switch)
   ↓
4. Erradicar (root cause)
   ↓
5. Recuperar (validar, restaurar)
   ↓
6. Comunicar (stakeholders, status page)
   ↓
7. Postmortem (blameless, <5 dias úteis)
```

### War Room

Para **SEV-4 ou superior**:

- Canal dedicado: `#incident-{YYYYMMDD}-{slug}`.
- Incident Commander: alguém com autoridade técnica + política.
- Scribe: registra decisões em tempo real.
- Communications Lead: status page + stakeholders.
- Subject Matter Experts: conforme necessário.

### Postmortem (Blameless)

Template:

```markdown
# Postmortem — {INCIDENT-ID}

## Resumo (1 parágrafo)
[O que aconteceu, em linguagem não-técnica]

## Impacto
- Duração total
- Usuários afetados
- Receita perdida (estimada)
- Reputação (qualitativa)

## Timeline (UTC)
- HH:MM — Evento
- HH:MM — Detecção
- HH:MM — Triagem
- HH:MM — Ações
- HH:MM — Resolução
- HH:MM — Comunicação

## Root Cause
[5 Whys aplicado]

## O que deu certo
[Bullets]

## O que pode melhorar
[Bullets]

## Action Items
- [ ] AI-1: descrição, owner, due date
- [ ] AI-2: ...

## Lessons Learned
[Bullets]
```

---

## 🔄 Capacity Planning

### Inputs

- Crescimento projetado (tenant, GMV, tráfego).
- SLO targets.
- Headroom desejado (recomendado: 30% acima do pico).
- Tendência sazonal.

### Outputs

- Projeção de capacidade (CPU, RAM, storage, rede).
- Plano de scaling (horizontal/vertical).
- Budget de infraestrutura aprovado.

### Cadência

- **Trimestral**: capacity review.
- **Anual**: capacity planning completo.
- **Contínuo**: alertas de saturação (USE).

---

## 📚 Documentos Relacionados

- [Knowledge-base: `08-kpis-oficiais-nexus.md`](../knowledge-base/08-kpis-oficiais-nexus.md)
- [Knowledge-base: `07-modelo-sho.md`](../knowledge-base/07-modelo-sho.md)
- [Knowledge-base: `01-modelo-ioaid.md`](../knowledge-base/01-modelo-ioaid.md)
- [Best-practice: `01-error-handling.md`](01-error-handling.md)
- [Best-practice: `02-performance.md`](02-performance.md)
- [Playbook: PB-CRISES-*](../../playbooks/)

## 👥 Ownership

- **Owner:** SRE Lead
- **Reviewers:** Head de Operações, Tech Lead
- **Cadência:** Trimestral

---

*Nexus Affil'IA'te · Lib-Nexus · best-practices/05-sre-observability.md · v1.0 · Julho 2026*
