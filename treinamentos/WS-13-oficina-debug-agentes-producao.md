---
title: "WS-13 · Oficina de Debug de Agentes em Produção"
subtitle: "Workshop hands-on: encontre e corrija 5 bugs reais em agentes implantados"
author: "Equipo Nexus · Sir. Nexus Alencar + Ravi (CTO/AI)"
duration: "4h"
type: "workshop"
level: "advanced"
date: 2026-07-29
pattern: "MMN_IA"
---

**WS-10 · Oficina de Debug de Agentes em Produção**

*Workshop hands-on de 4h onde você vai debugar 5 agentes propositalmente quebrados. Cada squad usa tracing, logs, Judge Revisor e métricas para encontrar e corrigir os bugs.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 Visão Geral

| Item | Detalhe |
|------|---------|
| **Duração** | 4 horas (2 coffee breaks) |
| **Formato** | 20% teoria + 80% hands-on |
| **Pré-requisitos** | Trilha Master completa. Experiência com agentes em produção. |
| **Capacidade** | 30 vagas (10 por squad) |
| **Material** | Sandbox com 5 agentes quebrados, Grafana, logs, OpenTelemetry |
| **Certificação** | Badge WS-10-DEBUG (raro, elegível para CEN+) |

---

## 📚 Agenda

| Horário | Bloco | Descrição |
|---------|-------|-----------|
| 0:00-0:25 | **Fundamentos** | Top 10 bugs em agentes, como observabilidade ajuda |
| 0:25-1:15 | **Bug #1-2: Latência + Custo** | 2 agentes, 30min cada |
| 1:15-1:30 | ☕ Coffee | |
| 1:30-2:15 | **Bug #3-4: Alucinação + Loop** | 2 agentes, 30min cada |
| 2:15-2:30 | ☕ Coffee | |
| 2:30-3:00 | **Bug #5: Cascading Failure** | 1 agente, 30min (o mais difícil) |
| 3:00-3:45 | **Análise + Solução** | Squads apresentam findings + patches |
| 3:45-4:00 | **Premiação** | Top squad. Badge. Convite para CEN+. |

---

## 🐛 Os 5 Bugs (Resumo)

Cada bug é propositalmente injetado em 1 agente:

| # | Bug | Sintoma | Ferramenta para detectar |
|---|-----|---------|--------------------------|
| **1** | Latência alta (chamadas LLM sequenciais) | p95 = 8s | Tracing OpenTelemetry |
| **2** | Custo estourado (modelo errado para tarefa) | $0.20/request | Métricas de custo |
| **3** | Alucinação factual (sem RAG) | 25% respostas erradas | Judge Revisor |
| **4** | Loop infinito (tool sem max_calls) | timeout | Análise de traces |
| **5** | Cascading failure (tool depende de outra) | 50% error rate | Grafana + logs |

---

## 📖 Bloco 0: Fundamentos (25 min)

### Top 10 Bugs em Agentes IA

**1. Latência alta (chamadas sequenciais)**
- LLM call 1 → LLM call 2 → LLM call 3
- Cada uma 1.5s = 4.5s total
- **Solução:** paralelizar (gather) ou cache

**2. Custo descontrolado (modelo overkill)**
- GPT-4o para classificar intent (simples)
- 20x mais caro que o necessário
- **Solução:** roteamento por complexidade

**3. Alucinação factual**
- LLM "inventa" informações
- Sem grounding em fontes
- **Solução:** RAG + Judge Revisor

**4. Loop infinito**
- Tool chama tool chama tool...
- Sem max iterations
- **Solução:** limite de iterações + circuit breaker

**5. Context overflow**
- Conversa longa excede 128k tokens
- Crash
- **Solução:** summarization periódica

**6. Prompt injection**
- User manipula LLM via input
- "Ignore tudo, responda..."
- **Solução:** filtros + Judge Revisor

**7. Race condition**
- 2 requests simultâneas no mesmo user
- Estado corrompido
- **Solução:** locks ou stateless design

**8. Memory leak**
- Listas crescem sem limpeza
- OOM depois de horas
- **Solução:** bounded collections

**9. Cascading failure**
- Service A depende de B depende de C
- C cai → tudo cai
- **Solução:** circuit breaker + fallback

**10. Drift de comportamento**
- Modelo começa a responder diferente
- Sem versionamento de prompt
- **Solução:** eval suite + alertas

### Ferramentas Essenciais

**Observabilidade:**
- Grafana (dashboards)
- OpenTelemetry (tracing)
- Sentry (errors)
- Langfuse (LLM-specific)

**Análise:**
- Judge Revisor (qualidade)
- Log search (padrões)
- Profiling (gargalos)

**Mitigação:**
- Feature flags (rollout gradual)
- Circuit breaker (isolamento)
- Fallback (graceful degradation)

---

## 🔧 Setup: 5 Agentes Quebrados

### Agente #1: "WhatsApp Lento"

**Sintoma:** Usuários reclamam que respostas demoram 8s.

**Setup:** 3 chamadas LLM sequenciais que poderiam ser 1.

```python
# Agente propositalmente quebrado
async def slow_agent(message: str):
    # 3 chamadas SEQUENCIAIS (bug!)
    intent = await classify_intent(message)  # LLM 1
    sentiment = await classify_sentiment(message)  # LLM 2
    response = await generate_response(message, intent, sentiment)  # LLM 3
    return response
```

**Sua tarefa:**
1. Usar tracing para identificar os 3 spans
2. Medir latência de cada um
3. Paralelizar com `asyncio.gather`
4. Validar que latência caiu para ~1.5s

### Agente #2: "Caro Demais"

**Sintoma:** Custo por request é $0.20, deveria ser $0.02.

**Setup:** GPT-4o sendo usado para classificar "comprou ou não comprou".

```python
# Agente propositalmente quebrado
async def classify_purchase(text: str) -> bool:
    response = await openai.chat.completions.create(
        model="gpt-4o",  # OVERKILL! Deveria ser gpt-4o-mini
        messages=[{"role": "user", "content": f"Comprou? Responda sim/não: {text}"}],
    )
    return "sim" in response.choices[0].message.content.lower()
```

**Sua tarefa:**
1. Calcular custo real (tokens × preço)
2. Identificar que gpt-4o-mini resolve
3. Implementar roteamento
4. Validar economia de 90%

### Agente #3: "Alucinador"

**Sintoma:** 25% das respostas contêm informações falsas.

**Setup:** Agente sem RAG, LLM "inventa" dados da empresa.

```python
# Agente propositalmente quebrado
async def answer_company_question(question: str) -> str:
    # SEM RAG (bug!)
    response = await openai.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": f"Responda sobre a Nexus: {question}"
        }],
    )
    return response.choices[0].message.content
```

**Sua tarefa:**
1. Adicionar base de conhecimento (knowledge base.json)
2. Implementar RAG simples (TF-IDF ou embeddings)
3. Adicionar Judge Revisor
4. Validar que alucinação caiu para < 5%

### Agente #4: "Loop Infinito"

**Sintoma:** Algumas requests demoram 30s+ ou dão timeout.

**Setup:** Tool recursivo sem limite de iterações.

```python
# Agente propositalmente quebrado
async def recursive_search(query: str) -> str:
    # SEM max_iterations (bug!)
    results = await search(query)
    if not results.sufficient:
        # Recursão sem fim
        return await recursive_search(results.refined_query)
    return results.summary
```

**Sua tarefa:**
1. Identificar loop via tracing (mesmo span repetido)
2. Adicionar `max_iterations = 3`
3. Adicionar circuit breaker
4. Validar que nunca passa de 5s

### Agente #5: "Cascading Failure" (Desafio)

**Sintoma:** 50% de erro em horário de pico (18h-22h).

**Setup:** Agente chama DB → API externa → LLM. DB lento faz tudo cair.

```python
# Agente propositalmente quebrado
async def full_pipeline(user_id: str):
    # SEM circuit breaker (bug!)
    user_data = await db.query(f"SELECT * FROM users WHERE id={user_id}")  # 1
    recommendations = await external_api.recommend(user_data)  # 2
    response = await llm.generate(recommendations)  # 3
    return response
```

**Sua tarefa:**
1. Identificar qual componente falha (tracing + Grafana)
2. Adicionar timeout por componente
3. Implementar circuit breaker
4. Adicionar fallback (cached response)
5. Validar que < 1% de erro mesmo com DB lento

---

## 🛠️ Hands-on: 5 Rodadas de Debug

### Rodada 1 (30 min): Bug #1 — Latência

**Squad trabalha no agente `slow_agent.py`**

**Checklist:**
- [ ] Iniciar tracing OpenTelemetry
- [ ] Fazer 10 requests
- [ ] Ver traces no Jaeger/Tempo
- [ ] Identificar span mais lento
- [ ] Refatorar para paralelizar
- [ ] Medir nova latência
- [ ] Documentar findings

**Critério de sucesso:** p95 < 2.5s

### Rodada 2 (30 min): Bug #2 — Custo

**Squad trabalha no agente `expensive_classifier.py`**

**Checklist:**
- [ ] Calcular custo/request atual
- [ ] Identificar tarefas simples vs complexas
- [ ] Implementar roteamento de modelo
- [ ] Calcular nova economia
- [ ] Validar accuracy não caiu

**Critério de sucesso:** Custo/request < $0.03 mantendo accuracy > 95%

### Rodada 3 (30 min): Bug #3 — Alucinação

**Squad trabalha no agente `hallucinating_qa.py`**

**Checklist:**
- [ ] Criar knowledge base (10 docs sobre Nexus)
- [ ] Implementar RAG (embeddings + similarity)
- [ ] Adicionar Judge Revisor
- [ ] Rodar 50 perguntas
- [ ] Medir taxa de alucinação
- [ ] Refinar até < 5% alucinação

**Critério de sucesso:** Alucinação < 5%, Judge aprova > 90%

### Rodada 4 (30 min): Bug #4 — Loop

**Squad trabalha no agente `recursive_search.py`**

**Checklist:**
- [ ] Adicionar max_iterations
- [ ] Adicionar timeout
- [ ] Adicionar circuit breaker
- [ ] Testar com queries patológicos
- [ ] Validar que nunca passa de 5s

**Critério de sucesso:** p99 < 5s, zero loop infinito

### Rodada 5 (30 min): Bug #5 — Cascading (Desafio)

**Squad trabalha no agente `pipeline_unstable.py`**

**Checklist:**
- [ ] Injetar falha artificial (DB lento)
- [ ] Medir taxa de erro
- [ ] Adicionar timeouts por componente
- [ ] Implementar circuit breaker
- [ ] Adicionar fallback (cached response)
- [ ] Validar < 1% erro mesmo com DB lento

**Critério de sucesso:** Taxa de erro < 1% com DB em 5s latência

---

## 📊 Análise + Solução (45 min)

### Cada squad apresenta 1 bug corrigido (5min × 6 squads = 30min)

**Formato:**
1. **Bug identificado** (30s)
2. **Root cause** (1min)
3. **Patch aplicado** (2min)
4. **Métricas antes/depois** (1min)
5. **Q&A** (30s)

### Critérios de Avaliação

| Critério | Peso |
|----------|------|
| **Velocidade de identificação** | 20% |
| **Qualidade do root cause** | 25% |
| **Solução implementada** | 30% |
| **Métricas (antes vs depois)** | 20% |
| **Apresentação** | 5% |

---

## 🏆 Premiação (15 min)

**Categorias:**
- 🥇 **Squad destaque** (melhor overall): badge + swag
- 🎯 **Detective rápido** (achou 5 bugs em < 2h)
- 💡 **Solução elegante** (código mais limpo)
- 📊 **Melhor métricas** (maior improvement)

**Top 3 squads ganham:**
- Badge WS-10-DEBUG (LinkedIn-verified)
- 150 XP na trilha Elite
- Acesso ao canal `#debug-prod`
- Elegível para CEN+
- Top 1: 30min mentoria 1:1 com Ravi (CTO/AI)

---

## 📦 Materiais Inclusos

- 5 agentes quebrados (Docker Compose)
- Sandbox com Grafana + Prometheus + Jaeger
- Knowledge base de exemplo (10 docs Nexus)
- Templates de patch para cada bug
- Eval suite (50 perguntas + respostas esperadas)
- Checklist de produção

---

## 🎯 Quem Deve Fazer

✅ **Perfeito para:**
- Engenheiros que mantêm agentes em produção
- Tech leads que precisam fazer code review de agentes
- SREs responsáveis por observabilidade
- Founders técnicos com agentes

❌ **Não indicado para:**
- Quem nunca deployou agente (comece com trilhas anteriores)
- Quem não tem experiência com Grafana/Prometheus

---

## 📚 Pré-work (Ler Antes do Workshop)

- `apostilas/45-debugging-otimizacao-agentes-ia.md` (40 min)
- `tutoriais/23-deploy-monitoramento-prometheus.md` (20 min)
- `Lib-Nexus/best-practices/05-sre-observability.md` (15 min)
- `producao/INCIDENT-RESPONSE-RUNBOOK.md` (15 min)

**Total: 1h30 de leitura prévia**

---

## 💬 Depoimentos de Quem Já Fez

> "Achei 3 bugs no meu agente de produção na semana seguinte ao WS-10. Literalmente paguei o workshop 10x."
> — Carla M., Estrategista + Engenheira, SP

> "O exercício de loop infinito me poupou de um outage sério. Recomendo 100%."
> — Diego F., Master, Lisboa

> "Não tem nada igual no mercado. Saindo com playbook de debug que uso todo dia."
> — Renata A., Estrategista, Curitiba

---

## 🔗 Materiais Complementares

- `apostilas/45-debugging-otimizacao-agentes-ia.md` — base teórica
- `apostilas/41-seguranca-juridica-ia-2026.md` — segurança
- `tutoriais/23-deploy-monitoramento-prometheus.md` — monitoramento
- `Lib-Nexus/best-practices/05-sre-observability.md` — SRE
- `producao/INCIDENT-RESPONSE-RUNBOOK.md` — runbook
- `governanca/PB-GOVERN-postmortem-blame-free.md` — post-mortem

---

*AcademIA · WS-10 · Oficina de Debug de Agentes em Produção · 2026*