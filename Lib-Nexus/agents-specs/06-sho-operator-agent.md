---
title: "Agent Spec · SHO Operator"
agent_code: AGENT-SHO-OPERATOR
version: "1.0.0"
category: operations
status: stable
owner: AcademIA / SRE Vertical
last_updated: 2026-07-22
pattern: "MMN_IA"
---

# 🛡️ Agent Spec — SHO Operator (AGENT-SHO-OPERATOR)

> **Agente especializado em operar o SHO** (Sistema de Higiene Operacional) em produção. Detecta, classifica, decide e age sobre incidentes — sempre sob supervisão humana para SEV-3+. O SHO Operator é o **braço executor** do SHO.

## 📋 Resumo

| Aspecto | Detalhe |
|---|---|
| **Função primária** | Detectar, classificar, decidir e agir sobre incidentes operacionais |
| **Modelos preferidos** | Claude Sonnet 4.5 (decisão), Claude Haiku (classificação rápida) |
| **Skills requeridas** | sho-classifier-v1, incident-runner, metrics-collector |
| **Latência alvo** | <30s para SEV-1/2, <90s para SEV-3 (com humano) |
| **Custo por execução** | R$0.01-0.10 |
| **Compliance** | LGPD, audit log imutável, observabilidade total |

## 🎯 Casos de uso

- Detectar **anomalia** em métricas de produção.
- Classificar **severidade** de incidente (SEV-0..4).
- Acionar **playbook** automático para SEV-1/2.
- **Escalar** para humano em SEV-3+.
- **Reportar** incidente em tempo real.
- **Executar** mitigação pré-aprovada.
- **Aprender** com cada incidente (postmortem).

## 🔧 Inputs

```typescript
interface SHOInput {
  // Contexto
  tenant_id: string;
  timestamp: string;          // ISO 8601
  
  // Sinais detectados
  signals: {
    latency?: { p50: number; p95: number; p99: number; p99_9: number };
    errors?: { count_4xx: number; count_5xx: number; rate: number };
    traffic?: { qps: number; baseline: number; ratio: number };
    resources?: { cpu: number; ram: number; disk: number; gpu?: number };
    cost?: { usd_hour: number; forecast: number; ratio: number };
    behavior?: { anomaly_score: number; loop_detected: boolean };
    content?: { pii_detected: boolean; jailbreak_score: number };
    business?: { conversion_drop: number; refund_spike: number };
    federated?: { reputation: number; gateway_load: number };
  };
  
  // Contexto adicional
  affected_tenants?: string[];
  history?: { recent_incidents: number; last_incident_at: string };
}
```

## 📤 Outputs

```typescript
interface SHOOutput {
  // Classificação
  severity: 'SEV-0' | 'SEV-1' | 'SEV-2' | 'SEV-3' | 'SEV-4';
  confidence: number;        // 0-1
  category: 'latency' | 'error' | 'cost' | 'security' | 'business' | 'unknown';
  
  // Diagnóstico
  diagnosis: {
    root_cause: string;
    affected_components: string[];
    estimated_impact: string;
  };
  
  // Ação
  action: {
    type: 'no_action' | 'playbook' | 'quarantine' | 'rollback' | 'kill_switch' | 'escalate';
    playbook_id?: string;
    requires_human_approval: boolean;
    estimated_resolution_time: string;
  };
  
  // Comunicação
  notification: {
    channels: string[];      // ['slack', 'email', 'in_app', 'status_page']
    recipients: string[];
    message: string;
  };
  
  // Audit
  audit_id: string;
  trace_id: string;
}
```

## 🧠 Comportamento detalhado

### Fase 1 — Recepção de Sinais

1. SHO Operator recebe **sinais** do metrics-collector.
2. Normaliza e **deduplica** sinais correlacionados.
3. Estabelece **contexto histórico** (últimas 24h, 7d, 30d).

### Fase 2 — Detecção de Anomalia

1. Compara sinal atual com **baseline**.
2. Calcula **z-score** (desvios padrão acima da média).
3. Se z > 3 em **3+ sinais correlacionados**: candidato a evento.
4. Aplica **regras de redundância** (3+ sinais = evento, 1 sinal = ruído).

### Fase 3 — Classificação de Severidade

```python
def classify(signal, context):
    if signal.severity == "informational":
        return "SEV-0"
    if signal.value < threshold_warning:
        return "SEV-1"
    if signal.value < threshold_alert:
        return "SEV-2"
    if signal.affects_users > 1000 or signal.business_impact > 0.3:
        return "SEV-3"
    return "SEV-4"
```

### Fase 4 — Decisão de Ação

| Severidade | Ação Default |
|-----------|--------------|
| **SEV-0** | No action (log only) |
| **SEV-1** | Notify in-app |
| **SEV-2** | Auto-playbook + notify ops |
| **SEV-3** | Playbook (with approval) + escalate on-call |
| **SEV-4** | Kill switch + page CEO + DPO |

### Fase 5 — Execução

1. Aciona **playbook** correspondente.
2. Captura **evidência** (logs, métricas, trace).
3. **Aplica mitigação** (quarantine, rollback, kill switch).
4. **Notifica** stakeholders via canais apropriados.
5. **Aguarda** validação humana para SEV-3+.

### Fase 6 — Aprendizado

1. Após resolução, **postmortem automático** é gerado.
2. Playbook é **atualizado** se houve gap.
3. **Sensor** é recalibrado se houve FN/FP.
4. **Knowledge base** é atualizada com caso.

## 🔌 Skills integradas

| Skill | Uso |
|-------|-----|
| `sho-classifier-v1` | Classificação de severidade |
| `incident-runner` | Execução de playbooks |
| `metrics-collector` | Coleta de sinais |
| `notification-dispatcher` | Envio de alertas |
| `audit-logger` | Registro de ações |

## 🛡️ Policy

**Bloqueado:**
- Quarantine ou kill switch sem **playbook correspondente**.
- Ação irreversível sem **human-in-the-loop** (SEV-3+).
- **PII exposure** em logs ou notificações.
- **Acesso a dados de outros tenants**.

**Requer aprovação humana:**
- **Quarantine** de skill com >10 tenants.
- **Rollback** de skill em produção.
- **Kill switch** de nó federado.
- Qualquer ação **cross-region**.

**Rate limit:**
- 1000 ações automáticas/hora por nó.
- 10 escalações/hora para humano (anti-spam).

## 📊 Métricas

| Métrica | Target |
|---------|--------|
| Latência p99 de detecção | <60s |
| False Positive Rate | <5% |
| False Negative Rate | <1% |
| Auto-resolution rate | >60% (SEV-1/2) |
| Mean Time To Acknowledge | <2min |
| Postmortem completion | <24h |

## 🧪 Testes

- [ ] test_basic_anomaly_detection
- [ ] test_severity_classification
- [ ] test_playbook_execution
- [ ] test_human_escalation
- [ ] test_audit_logging
- [ ] test_rollback
- [ ] test_quarantine
- [ ] test_kill_switch
- [ ] test_false_positive_handling
- [ ] test_false_negative_recovery

## 🔁 Versioning

| Versão | Data | Mudanças |
|--------|------|----------|
| 1.0.0 | 2026-07-22 | Release inicial |

## 📂 Recursos

- **Knowledge-base SHO:** [`../knowledge-base/07-modelo-sho.md`](../knowledge-base/07-modelo-sho.md)
- **Knowledge-base SRE:** [`../best-practices/05-sre-observability.md`](../best-practices/05-sre-observability.md)
- **Playbook Operação:** [`../../../playbooks/PB-CRISES-gestao-crise-data-loss.md`](../../../playbooks/PB-CRISES-gestao-crise-data-loss.md)
- **Apostila SHO:** [`../../../apostilas/11-sho-em-producao.md`](../../../apostilas/11-sho-em-producao.md)

## 👥 Ownership

- **Owner:** AcademIA / SRE Vertical
- **Reviewers:** SHO Lead, Head de Operações, DPO
- **Slack:** `#sho-operator`

---

*Nexus Affil'IA'te · AGENT-SHO-OPERATOR · v1.0.0 · Julho 2026*
