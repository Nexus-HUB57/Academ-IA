---
title: "AI Act EU — Guia de Conformidade"
code: "GOV-AI-ACT-EU"
version: "1.0.0"
status: "active"
owner: "DPO + Head Jurídico + CTO"
last_review: "2026-07-22"
next_review: "2027-01-22"
applies_to: "Todos os sistemas de IA com impacto em cidadãos EU ou em jurisdição EU"
tags: [governanca, ai-act, eu, regulacao, compliance, ia]
---

# 🇪🇺 AI Act EU — Guia de Conformidade

> **Guia canônico de conformidade com o AI Act da União Europeia** (Regulation (EU) 2024/1689) para a Plataforma Nexus. Documento vivo, atualizado conforme guias oficiais da EU AI Office.

## 🎯 Propósito

Centralizar a interpretação e aplicação do **AI Act EU** dentro da Plataforma Nexus, garantindo:

- Conformidade de todos os sistemas com impacto em cidadãos da UE.
- Classificação correta de risco de cada sistema.
- Implementação de controles por nível de risco.
- Preparação para auditoria da EU AI Office.

## 📜 Visão Geral do AI Act

O AI Act é o **primeiro regulamento horizontal de IA** do mundo, adotado em 2024 e em **aplicação faseada** (2025-2027). Estabelece 4 níveis de risco e obrigações proporcionais.

### Princípio Central

> *"Quanto maior o risco, mais rigorosas as regras."*

## 🚦 Os 4 Níveis de Risco

### 🔴 Risco Inaceitável (Art. 5) — PROIBIDO

**Sistemas proibidos** desde **2 de fevereiro de 2025**.

| Sistema | Proibição | Exceção |
|---------|-----------|---------|
| Manipulação subliminar | Total | Nenhuma |
| Exploração de vulnerabilidades | Total | Nenhuma |
| Social scoring governamental | Total | Nenhuma |
| Identificação biométrica em tempo real em espaços públicos | Parcial | Apenas para crimes graves, com autorização judicial |
| Categorização biométrica por raça, orientação sexual, etc. | Total | Nenhuma |
| Reconhecimento de emoções em trabalho/educação | Total | Exceção médica/segurança |
| Policiamento preditivo baseado em perfil | Total | Nenhuma |
| Scraping não-consentido de dados faciais | Total | Nenhuma |

**Ação Nexus:** Política formal de não desenvolver nenhum sistema nesta categoria.

### 🟠 Risco Alto (Anexo III)

**Sistemas de risco alto** têm obrigações a partir de **2 de agosto de 2026**.

**Categorias (Anexo III):**

1. **Biometria** (identificação, categorização, reconhecimento de emoções)
2. **Infraestrutura crítica** (tráfego, água, energia, saúde)
3. **Educação e formação profissional** (admissão, avaliação, monitoramento)
4. **Emprego e gestão de RH** (recrutamento, promoção, demissão)
5. **Serviços essenciais** (crédito, seguro, emergência)
6. **Aplicação da lei** (investigação, profiling, avaliação de risco)
7. **Migração e asilo** (avaliação de pedidos, vigilância)
8. **Justiça e democracia** (apoio a decisão judicial, interferência eleitoral)

**Obrigações (Art. 8-17):**

- Sistema de gestão de qualidade (Art. 9)
- Avaliação de risco contínua (Art. 9)
- Governança de dados (Art. 10) — datasets de treino validados
- Documentação técnica (Art. 11)
- Registro de eventos (logs) (Art. 12)
- Transparência e情報提供 (Art. 13)
- Oversight humano (Art. 14)
- Acurácia, robustez, segurança (Art. 15)
- Certificação por terceiro (quando aplicável)

### 🟡 Risco Limitado (Art. 50)

**Obrigações de transparência** a partir de **2 de agosto de 2026**.

Sistemas que interagem com pessoas ou geram conteúdo:

- **Disclosure** claro de que é IA.
- Marcação de **conteúdo sintético** (deepfakes, áudio gerado).
- Disclosure em **recomendações** algorítmicas.
- Disclosure em **biometria** quando aplicável.

**Exemplos:**
- Chatbots → "Você está conversando com uma IA."
- Copy gerada por IA → "Conteúdo gerado por IA."
- Deepfakes → Marcação visível.
- Reconhecimento de voz → "Áudio sintético."

### 🟢 Risco Mínimo

Sem obrigações específicas além das gerais (LGPD, GDPR, etc.).

**Exemplos:** filtros de spam, jogos, IA em brinquedos.

**Recomendação Nexus:** seguir boas práticas voluntariamente.

## 🛡️ Obrigações por Nível — Checklist Nexus

### Para Sistemas de Risco Alto

```yaml
gestao_qualidade:
  - [ ] Política de qualidade documentada
  - [ ] Processos de design, desenvolvimento, validação
  - [ ] Sistema de gestão de risco contínuo
  - [ ] Procedimentos de data governance

avaliacao_risco:
  - [ ] Identificação de riscos conhecidos e razoavelmente previsíveis
  - [ ] Análise de risco em cada fase do ciclo de vida
  - [ ] Mitigação documentada

dados_treinamento:
  - [ ] Relevância e representatividade
  - [ ] Ausência de viés discriminatório (quando possível)
  - [ ] Fonte de dados documentada
  - [ ] Conformidade com GDPR
  - [ ] Processo de preparação de dados (limpeza, labeling)

documentacao_tecnica:
  - [ ] Finalidade e uso pretendido
  - [ ] Acurácia e robustez
  - [ ] Métricas de performance
  - [ ] Limitações conhecidas
  - [ ] Planos de mitigação

logs_eventos:
  - [ ] Logs automáticos durante operação
  - [ ] Rastreabilidade de decisão
  - [ ] Retenção de logs por período adequado
  - [ ] Proteção de integridade

transparencia:
  - [ ] Instruções de uso claras
  - [ ] Limitação de uso para usuários
  - [ ] Disclosure ao usuário final
  - [ ] Informação em formato acessível

oversight_humano:
  - [ ] Interface para humano intervir
  - [ ] Capacidade de override
  - [ ] Stop button / kill switch
  - [ ] Mecanismo de revisão

acuracia_robustez_seguranca:
  - [ ] Métricas de acurácia declaradas
  - [ ] Resiliência a adversarial attacks
  - [ ] Redundância e fail-safe
  - [ ] Plano de segurança

certificacao:
  - [ ] Avaliação de conformidade por terceiro (quando aplicável)
  - [ ] Marcação CE (quando aplicável)
  - [ ] Registro na base de dados EU
```

### Para Sistemas de Risco Limitado

```yaml
transparencia:
  - [ ] Disclosure "isto é gerado por IA"
  - [ ] Marcação de conteúdo sintético (Art. 50)
  - [ ] Disclosure em interações humano-IA
  - [ ] Disclosure em reconhecimento de emoções/biometria

documentacao:
  - [ ] Manual de uso com disclosure adequado
  - [ ] Limitação de uso documentada
```

## 🏗️ Classificação dos Sistemas Nexus

### Inventário Atual

| Sistema | Categoria | Risco | Compliance Status |
|---------|-----------|-------|------------------|
| WhatsApp Copy Agent | Marketing/Copy | 🟢 Mínimo | N/A |
| Cohort Analytics | Analytics | 🟢 Mínimo | N/A |
| Marketing Agent | Personalização | 🟡 Limitado | Pendente Art. 50 |
| Federation Gate | Routing | 🟢 Mínimo | N/A |
| Judge Revisor | Avaliação de copy | 🟡 Limitado | Pendente Art. 50 |
| Analytics Cohort | Analytics | 🟢 Mínimo | N/A |
| SHO Operator | Operacional | 🟢 Mínimo | N/A |
| **Copy Persuasivo** | Marketing/Persuasão | 🟠 **Alto** (potencial) | **A analisar** |
| **Price Personalization** | Pricing | 🟠 **Alto** (potencial) | **A analisar** |

### Em Análise

- **Copy Persuasivo** — pode ser risco alto se usar perfilamento.
- **Price Personalization** — pode ser risco alto se afetar acesso a bens essenciais.

## 📋 Processo de Classificação

### Fluxo

```
1. Novo sistema proposto
   ↓
2. Product Manager preenche "AI Risk Classification Form"
   ↓
3. DPO + CTO classificam (mínimo / limitado / alto / inaceitável)
   ↓
4. Se risco alto: triggering do processo de compliance completo
   ↓
5. Se risco limitado: apenas transparency disclosure
   ↓
6. Se risco mínimo: sem obrigações específicas
   ↓
7. Registro no "Sistema de IA" (Art. 49 - registro EU)
```

### AI Risk Classification Form

Campos obrigatórios:

- [ ] Nome e descrição do sistema.
- [ ] Finalidade e uso pretendido.
- [ ] Categorias de pessoas afetadas.
- [ ] Decisões tomadas pelo sistema.
- [ ] Dados processados.
- [ ] Modelo(s) de IA utilizados.
- [ ] Biometria envolvida (sim/não).
- [ ] Categorização de pessoas (sim/não).
- [ ] Risco de profiling.
- [ ] Uso por autoridades públicas.
- [ ] Categorias do Anexo III aplicáveis (se houver).
- [ ] Nível de risco auto-avaliado.
- [ ] Justificativa da classificação.

## 🌐 Multilingual & Cross-Border

### Quando o AI Act Aplica

| Cenário | Aplica? |
|---------|---------|
| Sistema usado por cidadão EU | Sim |
| Sistema usado por empresa EU | Sim |
| Output usado em decisão sobre pessoa EU | Sim |
| Sistema desenvolvido fora da EU, afeta EU | Sim |
| Sistema puramente interno fora da EU | Não |

**Nexus Policy:** assumimos aplicação do AI Act para qualquer sistema com **potencial impacto** em EU (regra cautelosa).

## 📅 Cronograma de Aplicação

| Data | Marco |
|------|-------|
| **1 ago 2024** | AI Act entra em vigor |
| **2 fev 2025** | Proibições生效 (Art. 5) |
| **2 ago 2025** | Obrigações de governance (Cap. I, Art. 1-4) |
| **2 ago 2026** | Maioria das obrigações (Cap. II, III, IV, V, VII) |
| **2 ago 2027** | Sistemas em produtos regulados (Anexo I) |

**Status atual (julho 2026):** estamos a 1 mês da fase 3 (maioria das obrigações).

## 🔐 Penalidades

| Tipo | Multa Máxima |
|------|--------------|
| Uso de sistema proibido | €35M ou 7% do faturamento global |
| Não conformidade com risco alto | €15M ou 3% do faturamento global |
| Informação incorreta a autoridade | €7.5M ou 1% do faturamento global |
| PME | Menor entre percentual e valor fixo |

## 🤖 Governance de Modelos (GPAI)

Modelos de IA de uso geral (GPAI) têm obrigações específicas (Art. 51-55):

### Modelos com Risco Sistêmico (>10^25 FLOPs)

- Avaliação de risco contínua
- Reportar incidentes sérios à EU AI Office
- Cibersegurança reforçada
- Eficiência energética reportada

### Outros Modelos GPAI

- Documentação técnica
- Política de copyright
- Resumo de dados de treinamento

**Nexus:** estamos implementando controles para classificação e reporte de modelos GPAI.

## 📚 Documentos Complementares

- [`04-politica-ia-responsavel.md`](04-politica-ia-responsavel.md) — Política geral de IA Responsável
- [`C-SUITE-AI.md`](C-SUITE-AI.md) — Princípios para uso de IA por executivos
- [`../Lib-Nexus/knowledge-base/03-conformidade-lgpd.md`](../Lib-Nexus/knowledge-base/03-conformidade-lgpd.md) — LGPD
- [`../Lab-Nexus/prompts/governanca/03-auditoria-compliance.md`](../Lab-Nexus/prompts/governanca/03-auditoria-compliance.md) — Auditoria de compliance
- [`../Lab-Nexus/prompts/governanca/04-decisao-etica-ia.md`](../Lab-Nexus/prompts/governanca/04-decisao-etica-ia.md) — Decisão ética

## 🔗 Links Externos

- [AI Act (texto oficial)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689)
- [EU AI Office](https://digital-strategy.ec.europa.eu/en/policies/ai-office)
- [AI Act Explorer](https://artificialintelligenceact.eu/)

## 👥 Ownership

- **Owner:** DPO + Head Jurídico + CTO
- **Aprovação:** Comitê de Ética
- **Contato:** ai-act@nexus.io

---

*Nexus Affil'IA'te · GOV-AI-ACT-EU · v1.0.0 · Julho 2026*
