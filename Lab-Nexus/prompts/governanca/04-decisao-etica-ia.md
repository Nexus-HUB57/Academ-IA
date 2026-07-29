---
title: "Prompt — Decisão Ética de IA"
description: "Framework para analisar dilemas éticos em decisões de produto/uso de IA"
tags: [lab-nexus, prompt, governanca, etica, ia-responsavel, dilema]
category: prompts/governanca
level: master
author: "Equipe Nexus"
version: "1.0"
last_review: "2026-07-23"
---

# ⚖️ Prompt — Decisão Ética de IA

Framework estruturado para analisar **dilemas éticos** em decisões sobre produtos, features ou usos de IA. Complementa o prompt de auditoria de compliance com foco em **trade-offs** e **tomada de decisão** quando há tensões éticas legítimas (ex: personalização vs privacidade, automação vs emprego).

## 🎯 Quando usar

- Decidir **lançar ou não** feature com implicações éticas.
- Avaliar **trade-off** entre personalização e privacidade.
- Resolver **conflito** entre stakeholders sobre uso de IA.
- Documentar **decisão difícil** para accountability futura.
- Em **incident review** de decisão que gerou polêmica.

## 📋 Variáveis de Entrada

```yaml
dilema: "Descrição do dilema ético em uma frase"
contexto: "Contexto de negócio, técnico, social"
stakeholders: ["lista de grupos afetados e seus interesses"]
trade_offs: ["lista de trade-offs identificados"]
decisao_proposta: "A decisão que está sendo proposta (ou em análise)"
consequencias: ["consequências esperadas de cada caminho"]
valores_negocio: ["valores da empresa que devem orientar"]
precedentes: ["casos similares internos ou externos"]
urgencia: "baixa | média | alta | crítica"
```

## 📦 Prompt Pronto

```text
# PAPEL
Você é consultor sênior em ética de IA, com background em filosofia
moral, IA responsável, e governança corporativa. Você já assessorou
+30 empresas em decisões de IA controversas. Calibrado em frameworks
como AI Ethics Framework (IEEE), OECD AI Principles, e UNESCO
Recommendation on the Ethics of AI.

# OBJETIVO
Analisar o dilema ético abaixo, fornecendo:
1. Frame do dilema (stakeholders, valores em tensão, trade-offs)
2. Análise multi-framework (utilitarista, deontológico, virtuosa, cuidados)
3. Avaliação de riscos éticos (não apenas legais)
4. Recomendação de decisão (com caminhos alternativos)
5. Salvaguardas requeridas
6. Mecanismo de revisão futura

# INPUTS
Dilema: {{dilema}}
Contexto: {{contexto}}
Stakeholders: {{stakeholders}}
Trade-offs identificados: {{trade_offs}}
Decisão proposta: {{decisao_proposta}}
Consequências esperadas: {{consequencias}}
Valores de negócio: {{valores_negocio}}
Precedentes: {{precedentes}}
Urgência: {{urgencia}}

# ESTRUTURA DA ANÁLISE

## 1. Frame do Dilema

### 1.1. Quem são os stakeholders afetados?
[Mapear todos os grupos, seus interesses, e seu poder/voz na decisão]

### 1.2. Quais valores estão em tensão?
[Identificar os princípios éticos que competem entre si.
Ex: privacidade vs personalização, automação vs emprego,
eficiência vs equidade, lucro vs bem-estar]

### 1.3. Qual a natureza do dilema?
- [ ] Conflito entre direitos (ex: privacidade vs segurança)
- [ ] Conflito entre consequências (curto vs longo prazo)
- [ ] Distribuição desigual de benefícios/riscos
- [ ] Dilema de agência (decisão por outro sem consulta)
- [ ] Incerteza epistêmica (não sabemos o impacto)
- [ ] Outro: [especificar]

## 2. Análise Multi-Framework

### 2.1. Perspectiva Utilitarista (consequências)
[Maximizar bem-estar agregado. Quais ações geram mais valor/ menos dano líquido?]
- Análise: ...
- Risco de falhar: ...

### 2.2. Perspectiva Deontológica (regras/direitos)
[Existem regras, direitos, ou deveres que devem ser respeitados independentemente das consequências?]
- Análise: ...
- Risco de falhar: ...

### 2.3. Perspectiva das Virtudes (caráter)
[Que tipo de organização queremos ser? Que ação seria virtuosa?]
- Análise: ...
- Risco de falhar: ...

### 2.4. Perspectiva do Cuidado (relações)
[Como a decisão afeta as relações com stakeholders? Há grupos vulneráveis desproporcionalmente afetados?]
- Análise: ...
- Risco de falhar: ...

## 3. Avaliação de Riscos Éticos

| Risco | Probabilidade | Impacto | Score | Mitigação |
|-------|---------------|---------|-------|-----------|
| Viés discriminatório | 1-5 | 1-5 | P×I | [mitigação] |
| Exclusão de grupos vulneráveis | ... | ... | ... | ... |
| Perda de autonomia | ... | ... | ... | ... |
| Opacidade / falta de explicabilidade | ... | ... | ... | ... |
| Concentração de poder | ... | ... | ... | ... |
| Impacto ambiental | ... | ... | ... | ... |
| [outros riscos específicos] | ... | ... | ... | ... |

## 4. Recomendação de Decisão

### 4.1. Decisão Recomendada
[Qual caminho escolher, com justificativa]

### 4.2. Caminhos Alternativos Considerados
- **Caminho A** (recomendado): [descrição]
  - Prós: ...
  - Contras: ...
- **Caminho B** (alternativa): [descrição]
  - Prós: ...
  - Contras: ...
- **Caminho C** (não fazer): [descrição]
  - Prós: ...
  - Contras: ...

### 4.3. Quem Decide
[CEO, comitê de ética, conselho, etc. — e por quê]

## 5. Salvaguardas Requeridas

Para a decisão recomendada, que mecanismos garantem que os riscos
éticos identificados são mitigados:

- [Salvaguarda 1: processo, controle, comitê]
- [Salvaguarda 2]
- [Salvaguarda 3]

## 6. Mecanismo de Revisão Futura

- Quando reavaliar: [3 meses, 6 meses, 1 ano]
- Quem reavalia: [DPO, comitê de ética, etc.]
- Critérios de reavaliação: [métricas, eventos gatilho]
- Condição de reversão: [o que faria mudar de decisão]

## 7. Comunicação

Como comunicar a decisão para stakeholders internos e externos,
preservando confiança e accountability.

# REGRAS OBRIGATÓRIAS
- Não simplificar trade-offs: nomear tensões reais
- Considerar vozes de grupos afetados (não apenas shareholders)
- Distinguir ético de legal (algo pode ser legal e antiético)
- Considerar longo prazo, não apenas curto
- Ser explícito sobre incerteza
- Recomendar accountability clara

# FORMATO DE SAÍDA
Markdown estruturado. Decisão final em destaque. Salvaguardas em lista.
```

## 💡 Exemplo de Saída (trecho)

**Input:**
```
Dilema: "Devemos usar IA para personalizar precificação em tempo real
por perfil de consumidor?"

Contexto: Marketplace com +100k produtos. Personalização de preço pode
aumentar margem em ~15% mas gera percepção de injustiça.

Stakeholders: consumidores (negativo), investidores (positivo), DPO
(neutro/precaução), reguladores (desconfiados), concorrência (já faz).

Trade-offs: margem vs percepção de injustiça, personalização vs
discriminação, inovação vs reputação.

Decisão proposta: implementar em tier-1 de produtos (eletrônicos)
com transparência para o consumidor.

Urgência: alta (concorrência já implementou)
```

**Output (trechos):**

```markdown
## Análise Ética — Personalização Dinâmica de Preço

**Dilema:** Implementar personalização de preço via IA.
**Data:** 2026-07-23
**Score de risco ético agregado:** 18/25 — Moderado-Alto

## 1. Frame do Dilema

### 1.1. Stakeholders

- **Consumidores finais:** risco de tratamento injusto, percepção
  de manipulação, mas potencialmente acesso a preços mais baixos
  para perfis sensíveis.
- **Investidores/acionistas:** interesse em margem maior.
- **DPO/CISO:** preocupação com uso de dados demográficos.
- **Reguladores (CADE, Procon, ANPD):** crescente atenção ao tema.
- **Concorrência:** já pratica, criando pressão competitiva.
- **Comunidade:** percepção pública negativa pode afetar marca.
- **Funcionários:** moral em vender prática questionável.

### 1.2. Valores em Tensão

- **Eficiência econômica** (maximizar margem, alocar preço por WTP)
- **Justiça distributiva** (mesmo produto, mesmo preço)
- **Transparência** (consumidor saber que preço é personalizado)
- **Autonomia do consumidor** (escolha informada)
- **Inovação** (uso legítimo de dados para benefício mútuo)
- **Confiança** (relações de longo prazo)

### 1.3. Natureza do Dilema

[✓] Distribuição desigual de benefícios/riscos (perfis de alta renda
    podem ser sobrecarregados)
[✓] Incerteza epistêmica (impacto real é difícil de prever)
[ ] Conflito entre direitos — não há direito fundamental violado
[ ] Dilema de agência — não aplicável
[ ] Conflito entre consequências — sim, curto vs longo prazo

## 2. Análise Multi-Framework

### 2.1. Utilitarista
Maximizar bem-estar agregado: ganho de margem pode ser reinvesto
em preços menores para todos OU em features. Resultado depende de
governança do uso do ganho.

**Risco de falhar:** assumir que todo ganho é reinvestido eticamente.

### 2.2. Deontológica
Direito do consumidor a não ser enganado. Se personalização for
opaca, viola dever de transparência. Se explícita, pode ser aceitável.

**Risco de falhar:** assumir que "transparente" basta (pode ser
informada mas não compreendida).

### 2.3. Virtuosa
Que tipo de empresa queremos ser? A que pratica preços justos
ou a que maximiza margem a qualquer custo?

**Risco de falhar:** normalizar a prática por inércia competitiva.

### 2.4. Cuidado
Consumidores mais vulneráveis (renda baixa, urgência médica, baixa
literacia digital) podem ser desproporcionalmente prejudicados por
personalização agressiva.

**Risco de falhar:** não envolver vozes de grupos vulneráveis
no design.

## 3. Avaliação de Riscos Éticos

| Risco | P | I | Score | Mitigação |
|-------|---|---|-------|-----------|
| Discriminação por perfil | 4 | 5 | 20 | Floor/ceiling de preço, auditoria |
| Perda de confiança | 3 | 5 | 15 | Disclosure explícito, opt-out |
| Reação regulatória | 4 | 4 | 16 | Conformidade proativa |
| Impacto em grupos vulneráveis | 3 | 4 | 12 | Exclusão de categorias sensíveis |
| Reputação em crise | 2 | 5 | 10 | Comunicação transparente |

**Score agregado: 18/25 — Moderado-Alto**

## 4. Recomendação

### 4.1. Decisão Recomendada
**Implementar com salvaguardas robustas.**

### 4.2. Caminhos

- **Caminho A (recomendado):** Implementar com:
  - Floor/ceiling de preço (variação máx 8%)
  - Disclosure explícito ao consumidor
  - Exclusão de categorias sensíveis (saúde, alimentação, educação)
  - Auditoria mensal de viés
  - Opt-out para consumidor (mostra preço "neutro")
  - Comitê de ética revisa a cada 3 meses
- **Caminho B (alternativa):** Implementar apenas em B2B (lojistas),
  onde decisão é mais racional.
- **Caminho C (não fazer):** Manter preço fixo, perder margem.

### 4.3. Quem Decide
**CEO + Comitê de Ética + Conselho** (decisão de alto impacto).

## 5. Salvaguardas

1. Floor/ceiling: preço personalizado varia no máximo 8% do preço base.
2. Disclosure: "Este preço pode ser personalizado com base no seu
   perfil. Veja o preço de referência."
3. Exclusão: saúde, alimentação básica, educação fora da personalização.
4. Auditoria mensal: análise de viés por faixa de renda, raça, gênero.
5. Opt-out: consumidor pode ver preço "neutro" se preferir.
6. Kill switch: suspender se viés > X% sem justificativa de mercado.

## 6. Revisão Futura

- **Quando:** 3 meses após lançamento.
- **Quem:** Comitê de Ética + DPO.
- **Critérios:** variação de preço por perfil, complaints, auditoria
  de viés.
- **Reversão:** se viés > 5% ou complaints > 0.5%.

## 7. Comunicação

**Interna:** explicar rationale, ouvir concerns, treinar times.
**Externa:** comunicado à imprensa sobre compromisso com fairness,
publicar relatório anual de fairness de preço.
**Consumidor:** disclosure no checkout + página de transparência.
```

## 📊 Score de Risco Ético

| Faixa | Nível | Recomendação |
|-------|-------|--------------|
| 0-5 | Baixo | Implementar com monitoramento padrão |
| 6-10 | Moderado | Implementar com salvaguardas reforçadas |
| 11-15 | Alto | Implementar com comitê de ética + revisão trimestral |
| 16-20 | Muito alto | Considerar não implementar ou piloto limitado |
| 21-25 | Crítico | Não implementar |

## ⚠️ Erros Comuns

- ❌ Tratar ético como "cumprir a lei"
- ❌ Não envolver grupos afetados no processo
- ❌ Decidir com pressão de tempo excessiva
- ❌ Comunicar após implementar, não antes
- ❌ Sem mecanismo de reversão
- ❌ Sem salvaguarda explícita

## 🔗 Próximos Prompts

- → `03-auditoria-compliance.md` — para validar conformidade legal
- → `01-decisao-csuite-ratificar.md` — para ratificação C-level
- → `02-postmortem-incidente.md` — para revisar decisões passadas

---

*Versão 1.0 · Atualizado 2026-07-23 · Mantido pela Equipe Nexus*
