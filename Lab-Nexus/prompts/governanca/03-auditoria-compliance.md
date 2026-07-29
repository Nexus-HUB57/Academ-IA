---
title: "Prompt — Auditoria de Compliance de IA"
description: "Prompt canônico para auditar sistema de IA contra frameworks regulatórios (LGPD, GDPR, AI Act)"
tags: [lab-nexus, prompt, governanca, compliance, auditoria, lgpd, gdpr, ai-act]
category: prompts/governanca
level: master
author: "Equipe Nexus"
version: "1.0"
last_review: "2026-07-23"
---

# 🔍 Prompt — Auditoria de Compliance de IA

Prompt canônico para auditar um **sistema de IA** contra frameworks regulatórios (LGPD, GDPR, AI Act EU, CCPA, HIPAA). Gera relatório estruturado com **gaps, riscos, e plano de remediação priorizado**.

## 🎯 Quando usar

- **Auditoria trimestral** de compliance.
- Antes de **go-live** de feature nova.
- Após **incidente** de segurança/PII.
- Em **due diligence** para parcerias/white-label.
- Em preparação para **auditoria externa** (ANPD, certificações).

## 📋 Variáveis de Entrada

```yaml
sistema: "Nome do sistema / agente / skill a ser auditado"
regulacoes: ["LGPD", "GDPR", "AI Act EU", "CCPA", "HIPAA"]
contexto_uso: "Descrição do uso real (dados processados, decisões tomadas, pessoas afetadas)"
documentacao: ["Link para docs técnicas", "Política de privacidade", "DPIA", "model card"]
dados_pii: ["Categorias de PII processadas (saúde, biométrico, etc.)"]
decisoes_automatizadas: ["Tipos de decisões tomadas pelo sistema"]
jurisdicoes: ["BR", "EU", "US", "etc."]
audiencia: ["interna", "regulador", "cliente enterprise"]
```

## 📦 Prompt Pronto

```text
# PAPEL
Você é auditor sênior de compliance de IA, com expertise em LGPD, GDPR,
AI Act EU, CCPA, HIPAA. Você já auditou +50 sistemas em produção.
Calibrado nos frameworks regulatórios atuais e atualizações 2026.

# OBJETIVO
Realizar auditoria completa de compliance do sistema abaixo, gerando
relatório estruturado com:
1. Escopo da auditoria
2. Conformidade por regulação
3. Gaps identificados
4. Riscos (probabilidade × impacto)
5. Plano de remediação priorizado
6. Recomendações de governança contínua

# INPUTS
Sistema: {{sistema}}
Regulações aplicáveis: {{regulacoes}}
Contexto de uso: {{contexto_uso}}
Documentação: {{documentacao}}
Dados PII processados: {{dados_pii}}
Decisões automatizadas: {{decisoes_automatizadas}}
Jurisdições: {{jurisdicoes}}
Audiência do relatório: {{audiencia}}

# ESTRUTURA DO RELATÓRIO

## 1. Escopo
[Quais aspectos do sistema foram auditados, quais não foram, limitações]

## 2. Conformidade por Regulação

### LGPD (se aplicável)
- Base legal para tratamento (Art. 7)
- Finalidade (Art. 6)
- Necessidade (Art. 6, §1)
- Direitos do titular (Art. 18)
- Encarregado/DPO (Art. 41)
- Segurança da informação (Art. 46)
- Relatório de impacto (Art. 38)
**Status**: [Conforme / Parcial / Não conforme]
**Gaps**: [lista]

### GDPR (se aplicável)
- Lawful basis (Art. 6)
- Data subject rights (Cap. III)
- DPIA (Art. 35)
- DPO (Art. 37-39)
- Cross-border transfers (Cap. V)
- Privacy by design (Art. 25)
**Status**: [conforme / parcial / não conforme]
**Gaps**: [lista]

### AI Act EU (se aplicável)
- Risk classification (Art. 5-7, Anexo III)
- High-risk requirements (Art. 8-17)
- Transparency (Art. 50)
- Human oversight (Art. 14)
- Quality of datasets (Art. 10)
**Status**: [conforme / parcial / não conforme]
**Gaps**: [lista]

### CCPA / HIPAA / outros (se aplicável)
[Análise específica por regulação]

## 3. Gaps Identificados (Top 10)

Para cada gap:
- Descrição
- Regulação violada
- Probabilidade de materialização (1-5)
- Impacto (1-5)
- Score de risco (P × I)
- Esforço de remediação (1-5)

## 4. Plano de Remediação

| Prioridade | Gap | Ação | Owner | Due date |
|------------|-----|------|-------|----------|
| 1 (P0) | [gap] | [ação] | [owner] | [data] |
| 2 (P1) | ... | ... | ... | ... |

## 5. Recomendações de Governança Contínua

- [Recomendação 1: processo, política, controle]
- [Recomendação 2]
- [Recomendação 3]

## 6. Score Final

Score de 0-100 representando nível de conformidade geral.
**Ações requeridas** se score < 80.

# REGRAS OBRIGATÓRIAS
- Conservador: na dúvida, marcar como gap
- Específico: cada gap com citação da regulação
- Acionável: cada gap com plano de ação concreto
- Auditável: o relatório em si deve ser referência futura
- Linguagem técnica mas acessível para C-level

# FORMATO DE SAÍDA
Markdown estruturado conforme template acima. Score em destaque.
```

## 💡 Exemplo de Saída (trecho)

**Input:**
```
Sistema: WhatsApp Copy Agent v2
Regulações: LGPD, AI Act EU
Contexto: gera copy marketing para WhatsApp, processa
  dados demográficos para personalização
Documentação: model card parcial, sem DPIA
Dados PII: idade, gênero, cidade, comportamento de compra
Decisões automatizadas: nenhuma (apenas geração de copy)
Jurisdições: BR
Audiência: interna
```

**Output (trechos):**

```markdown
## Relatório de Auditoria de Compliance

**Sistema:** WhatsApp Copy Agent v2
**Data:** 2026-07-23
**Auditor:** Claude (Playbook PB-AUDIT-COMPLIANCE)
**Score Final:** 62/100 ⚠️

## 1. Escopo

Auditoria cobriu: base legal, finalidade, segurança da informação,
direitos do titular, risco de IA.

Não cobriu: auditoria de segurança física dos data centers,
auditoria de fornecedores externos.

## 2. Conformidade por Regulação

### LGPD

**Status:** Parcialmente conforme
**Gaps:**

1. **Sem DPIA (Art. 38)** — impacto alto.
   - Probabilidade: 4 | Impacto: 4 | Score: 16
   - Esforço: 3
   - Ação: elaborar DPIA em 30 dias.

2. **Política de retenção não documentada (Art. 16)**
   - Probabilidade: 3 | Impacto: 3 | Score: 9
   - Esforço: 2
   - Ação: documentar política em 14 dias.

### AI Act EU

**Status:** Parcialmente conforme (sistema é risco limitado, mas pode
ser classificado como "uso em contexto de marketing" → pode subir
para risco alto).

**Gaps:**

1. **Falta transparency disclosure (Art. 50)**
   - Provável: 5 | Impacto: 3 | Score: 15
   - Esforço: 2
   - Ação: adicionar "isso é gerado por IA" nos outputs.

## 3. Gaps Top 10 (resumo)

| Rank | Gap | Score | Esforço | Prioridade |
|------|-----|-------|---------|------------|
| 1 | Sem DPIA | 16 | 3 | P0 |
| 2 | Sem transparency disclosure | 15 | 2 | P0 |
| 3 | Política de retenção não documentada | 9 | 2 | P1 |
| ... | ... | ... | ... | ... |

## 4. Plano de Remediação

| Pri | Gap | Ação | Owner | Due |
|-----|-----|------|-------|-----|
| 1 | Sem DPIA | Elaborar DPIA com DPO | DPO | 2026-08-22 |
| 2 | Sem transparency | Adicionar disclosure | Product | 2026-08-01 |
| 3 | Política retenção | Documentar | DPO | 2026-08-06 |
| ... | ... | ... | ... | ... |

## 5. Recomendações de Governança

- Implementar **auditoria trimestral** automatizada via este prompt.
- Criar **dashboard de compliance** com status por regulação.
- Nomear **DPO adjunto** para cobrir ausências.

## 6. Score Final: 62/100 ⚠️

**Ação requerida:** tratar gaps P0 em 30 dias. Re-auditoria em 60 dias.
```

## 📊 Score Típico

| Faixa | Status | Ação |
|-------|--------|------|
| 90-100 | Excelente | Manter |
| 75-89 | Bom | Melhorias incrementais |
| 60-74 | Aceitável | Plano de remediação 60d |
| 40-59 | Preocupante | Plano de remediação 30d, congelar features |
| <40 | Crítico | Parar operação até resolver gaps P0 |

## ⚠️ Erros Comuns

- ❌ Marcar como "conforme" sem evidência
- ❌ Ignorar AI Act mesmo em sistemas "menores"
- ❌ Não diferenciar gap técnico vs gap de processo
- ❌ Sem plano de remediação priorizado
- ❌ Relatório sem score final

## 🔗 Próximos Prompts

- → `04-decisao-etica-ia.md` — para dilemas éticos
- → `02-postmortem-incidente.md` — para incidentes
- → `01-decisao-csuite-ratificar.md` — para ratificação C-level

---

*Versão 1.0 · Atualizado 2026-07-23 · Mantido pela Equipe Nexus*
